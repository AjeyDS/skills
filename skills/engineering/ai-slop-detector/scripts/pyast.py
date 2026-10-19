"""Stdlib-only Python AST analysis for structural slop.

Exists because the two things that matter most for codebase bloat -- whether a
module is reachable at all, and where complexity is concentrated -- are
whole-graph properties. No amount of file-by-file reading answers them, and
heuristic dead-code tools answer them badly (vulture at --min-confidence 60
flags live entry points; at 80 it finds nothing).

Emits facts only. Judgment is the caller's job.
"""

from __future__ import annotations

import ast
import json
import sys
from collections import defaultdict
from pathlib import Path

# Branch-introducing nodes, for a McCabe-style count.
_BRANCH = (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With,
           ast.Assert, ast.comprehension, ast.IfExp, ast.Match)


def _complexity(fn: ast.AST) -> int:
    score = 1
    for node in ast.walk(fn):
        if isinstance(node, _BRANCH):
            score += 1
        elif isinstance(node, ast.BoolOp):
            score += len(node.values) - 1
        elif isinstance(node, getattr(ast, "match_case", ())):
            score += 1
    return score


TEST_MARKERS = ("test_", "_test", "conftest", "tests", "spec_", "_spec", "fixtures")


def _is_test(path: Path) -> bool:
    """Test code is repetitive and grows on purpose. Counting it in the same
    bucket as source makes every quality metric a function of test volume:
    measured on a test-heavy fixture, tests were 87% of total LOC, so 40 new
    tests tripped a +10% growth gate on their own."""
    parts = [seg.lower() for seg in path.parts]
    return any(m in seg for seg in parts for m in TEST_MARKERS)


def _module_name(path: Path, root: Path) -> str:
    rel = path.relative_to(root).with_suffix("")
    parts = list(rel.parts)
    if parts and parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _resolve(node: ast.AST, this_module: str, known: set[str]) -> set[str]:
    """Map an import statement to internal module names it could refer to."""
    hits: set[str] = set()
    candidates: list[str] = []

    if isinstance(node, ast.Import):
        candidates = [a.name for a in node.names]
    elif isinstance(node, ast.ImportFrom):
        if node.level:  # relative import
            base = this_module.split(".")
            base = base[: len(base) - node.level + 1] if node.level <= len(base) else []
            prefix = ".".join(base)
            head = f"{prefix}.{node.module}" if node.module else prefix
        else:
            head = node.module or ""
        candidates = [head] + [f"{head}.{a.name}" for a in node.names if head]

    for cand in candidates:
        # Longest-prefix match: `from pkg.mod import thing` -> pkg.mod
        parts = cand.split(".")
        for i in range(len(parts), 0, -1):
            probe = ".".join(parts[:i])
            if probe in known:
                hits.add(probe)
                break
    return hits


def analyze(root: Path, entry_points: list[str], max_params: int = 5,
            cc_threshold: int = 10, long_fn: int = 50) -> dict:
    root = root.resolve()
    files = [
        p for p in root.rglob("*.py")
        if not any(seg in {".git", "node_modules", ".venv", "venv", "__pycache__",
                           "build", "dist", ".tox", ".mypy_cache", "migrations"}
                   for seg in p.parts)
    ]

    modules: dict[str, Path] = {}
    trees: dict[str, ast.Module] = {}
    for f in files:
        try:
            trees[_module_name(f, root)] = ast.parse(f.read_text(encoding="utf-8", errors="replace"))
            modules[_module_name(f, root)] = f
        except SyntaxError:
            continue

    known = set(modules)
    imports: dict[str, set[str]] = defaultdict(set)
    hotspots: list[dict] = []
    masking: list[dict] = []
    external_calls: dict[str, int] = defaultdict(int)

    for mod, tree in trees.items():
        rel = str(modules[mod].relative_to(root))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                imports[mod] |= _resolve(node, mod, known)

            # Error masking: bare `except:` or a handler whose body is only pass/...
            elif isinstance(node, ast.ExceptHandler):
                body = node.body
                silent = len(body) == 1 and (
                    isinstance(body[0], ast.Pass)
                    or (isinstance(body[0], ast.Expr)
                        and isinstance(body[0].value, ast.Constant)
                        and body[0].value.value is Ellipsis)
                )
                if node.type is None or silent:
                    masking.append({
                        "file": rel, "line": node.lineno,
                        "kind": "bare_except" if node.type is None else "swallowed_exception",
                    })

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                cc = _complexity(node)
                nparams = len(node.args.args) + len(node.args.kwonlyargs)
                length = (getattr(node, "end_lineno", node.lineno) or node.lineno) - node.lineno + 1
                if cc >= cc_threshold or nparams > max_params or length > long_fn:
                    hotspots.append({
                        "file": rel, "line": node.lineno, "name": node.name,
                        "complexity": cc, "params": nparams, "lines": length,
                    })

            # Connectivity proxy: calls to a namespaced attribute (obj.method()).
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                external_calls[mod] += 1

    # --- Reachability from declared entry points -------------------------
    seeds = set()
    for ep in entry_points:
        ep = ep.replace("/", ".").removesuffix(".py")
        seeds |= {m for m in known if m == ep or m.startswith(ep + ".")}
    if not seeds:  # fall back to conventional roots
        seeds = {m for m in known
                 if m.split(".")[-1] in {"main", "app", "cli", "__main__", "server", "wsgi", "asgi"}
                 or "." not in m}

    def _closure(start: set[str]) -> set[str]:
        seen, stack = set(start), list(start)
        while stack:
            for nxt in imports.get(stack.pop(), ()):
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return seen

    reachable = _closure(seeds)
    # Reached from tests but not from production = kept alive only by its own
    # tests. Distinct from dead, and distinct from live: it is a deletion
    # candidate whose only blocker is repointing test call sites.
    test_seeds = {m for m, p in modules.items() if _is_test(p)}
    test_only = sorted(
        {m for m in _closure(test_seeds) - reachable
         if not _is_test(modules[m]) and modules[m].name != "__init__.py"}
    )

    def _orphan_candidates():
        for m in known - reachable:
            path = modules[m]
            # Package markers (__init__.py) are structure, not code -- reporting
            # them as orphans buries the real finding in noise.
            if path.name == "__init__.py":
                continue
            if "test" in m.lower():
                continue
            loc = len([ln for ln in path.read_text(encoding="utf-8", errors="replace").splitlines()
                       if ln.strip() and not ln.strip().startswith("#")])
            if loc == 0:
                continue
            yield {"module": m, "file": str(path.relative_to(root)), "loc": loc}

    orphans = sorted(_orphan_candidates(), key=lambda d: -d["loc"])

    def _loc(p: Path) -> int:
        return len(p.read_text(encoding="utf-8", errors="replace").splitlines())

    src_loc = sum(_loc(p) for p in modules.values() if not _is_test(p))
    test_loc = sum(_loc(p) for p in modules.values() if _is_test(p))
    total_loc = src_loc + test_loc
    internal_edges = sum(len(v) for v in imports.values())

    return {
        # Basename only. This value is never read back, but it lands in a
        # COMMITTED .slop-baseline.json -- an absolute path there leaks the
        # author's username and local directory layout into a public repo.
        "root": root.name,
        "modules": len(modules),
        "total_loc": total_loc,
        "src_loc": src_loc,
        "test_loc": test_loc,
        "orphan_modules": orphans,
        "test_only_reachable": test_only,
        "orphan_loc": sum(o["loc"] for o in orphans),
        "complexity_hotspots": sorted(hotspots, key=lambda d: -d["complexity"])[:50],
        "hotspot_count": len(hotspots),
        "error_masking": masking,
        "error_masking_count": len(masking),
        # Falling connectivity is GitClear's strongest reuse signal: new code
        # that calls nothing existing is code that reinvented something.
        "internal_import_edges": internal_edges,
        "imports_per_module": round(internal_edges / max(len(modules), 1), 2),
        "entry_points_used": sorted(seeds),
    }


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="Structural slop facts for a Python tree.")
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--entry", action="append", default=[],
                    help="Entry-point module or path; repeatable. Wrong entry points are "
                         "the #1 cause of false orphans -- always pass them explicitly.")
    ap.add_argument("--cc-threshold", type=int, default=10)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    result = analyze(Path(args.path), args.entry, cc_threshold=args.cc_threshold)

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    print(f"modules={result['modules']} loc={result['total_loc']} "
          f"imports/module={result['imports_per_module']}")
    print(f"orphan modules: {len(result['orphan_modules'])} ({result['orphan_loc']} LOC)")
    for o in result["orphan_modules"][:10]:
        print(f"  {o['file']:<45} {o['loc']:>5} LOC")
    print(f"complexity hotspots: {result['hotspot_count']}")
    for h in result["complexity_hotspots"][:10]:
        print(f"  {h['file']}:{h['line']} {h['name']}  cc={h['complexity']} "
              f"params={h['params']} lines={h['lines']}")
    print(f"error masking: {result['error_masking_count']}")
    for m in result["error_masking"][:10]:
        print(f"  {m['file']}:{m['line']} {m['kind']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
