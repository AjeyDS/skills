"""Run whatever deterministic analyzers are installed, merge, rank by cost.

Three verbs:
  scan      one-shot picture, ranked, token-cheap
  baseline  freeze current numbers to .slop-baseline.json
  check     compare against baseline; non-zero exit on regression

`check` is the point. A one-shot audit tells you a codebase is bad; a ratchet
stops it getting worse. The measured failure mode of agentic development is a
slope, not a level -- quality guidance moves the intercept and leaves the slope
alone -- so the intervention has to be a slope intervention.

Missing tools degrade to "unavailable" rather than failing. Only pyast.py
(stdlib) is required.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import pyast  # noqa: E402
import graph_signals  # noqa: E402

BASELINE = ".slop-baseline.json"
CONFIG = ".slopconfig.json"

DEFAULT_CONFIG = {
    "entry_points": [],
    # Duplication in test code is expected and swamps everything else: measured
    # 11 of 12 clones in a test-heavy fixture were test-to-test, at 83% overall.
    "duplication_ignore": ["**/tests/**", "**/test_*.py", "**/*_test.py",
                           "**/conftest.py", "**/__snapshots__/**", "**/*.spec.ts",
                           "**/*.test.ts", "**/migrations/**"],
    # Clone pairs already adjudicated as deliberate. Each needs a reason, so the
    # next agent cannot silently "fix" a duplication that exists on purpose.
    "allowed_clones": [],
    "gate_test_loc": False,
}


def load_config(root: Path) -> dict:
    cfg = dict(DEFAULT_CONFIG)
    path = root / CONFIG
    if path.exists():
        cfg.update(json.loads(path.read_text()))
    return cfg


def _allowed(clone: dict, allowed: list[dict]) -> bool:
    a = clone.get("firstFile", {}).get("name", "")
    b = clone.get("secondFile", {}).get("name", "")
    for rule in allowed:
        pair = {rule.get("a", ""), rule.get("b", "")}
        if any(x and x in a for x in pair) and any(x and x in b for x in pair):
            return True
    return False

SKIP = ["**/node_modules/**", "**/.git/**", "**/dist/**", "**/build/**",
        "**/.venv/**", "**/venv/**", "**/__pycache__/**", "**/*.min.js",
        "**/*.lock", "**/migrations/**", "**/.next/**", "**/coverage/**"]


def _run(cmd: list[str], cwd: Path, timeout: int = 300):
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return None


def duplication(root: Path, min_tokens: int, cfg: dict) -> dict:
    """jscpd. Percentage is meaningless without pinning min_tokens -- on a small
    sample it swung 29%-39% across settings, so the config travels with the number."""
    if not shutil.which("jscpd"):
        return {"available": False, "reason": "jscpd not installed (npm i -g jscpd)"}
    with tempfile.TemporaryDirectory() as tmp:
        res = _run(["jscpd", ".", "-r", "json", "-o", tmp, "--min-tokens", str(min_tokens),
                    "--mode", "weak",
                    "-i", ",".join(SKIP + cfg["duplication_ignore"])], root)
        if res is None:
            return {"available": False, "reason": "jscpd failed to run"}
        report = Path(tmp) / "jscpd-report.json"
        if not report.exists():
            return {"available": False, "reason": "no jscpd report produced"}
        data = json.loads(report.read_text())

    total = data.get("statistics", {}).get("total", {})
    raw = data.get("duplicates", [])
    clones = [c for c in raw if not _allowed(c, cfg["allowed_clones"])]
    suppressed = len(raw) - len(clones)
    hot: dict[str, int] = {}
    for c in clones:
        for side in ("firstFile", "secondFile"):
            name = c.get(side, {}).get("name")
            if name:
                hot[name] = hot.get(name, 0) + 1
    return {
        "available": True,
        "config": {"min_tokens": min_tokens, "mode": "weak"},
        "percentage": round(total.get("percentage", 0.0), 2),
        "duplicated_lines": sum(c.get("lines", 0) for c in clones),
        "clones": len(clones),
        "allowlisted_clones": suppressed,
        "worst_files": sorted(hot.items(), key=lambda kv: -kv[1])[:15],
    }


def js_dead_code(root: Path) -> dict:
    """knip, for TS/JS. Entry-point config is load-bearing: miss entries and live
    code reads as dead; over-broaden and dead code hides."""
    if not (root / "package.json").exists():
        return {"available": False, "reason": "no package.json"}
    if not shutil.which("knip"):
        return {"available": False, "reason": "knip not installed (npm i -D knip)"}
    res = _run(["knip", "--reporter", "json", "--no-exit-code"], root)
    if res is None or not res.stdout.strip():
        return {"available": False, "reason": "knip produced no output"}
    try:
        data = json.loads(res.stdout)
    except json.JSONDecodeError:
        return {"available": False, "reason": "knip output not parseable"}
    files = data.get("files", [])
    issues = data.get("issues", [])
    return {
        "available": True,
        "unused_files": len(files),
        "unused_files_sample": files[:15],
        "unused_exports": sum(len(i.get("exports", {})) for i in issues),
        "unused_dependencies": sum(len(i.get("dependencies", {})) for i in issues),
    }


def rank(findings: dict) -> list[dict]:
    """Order by what each defect costs to live with, not by how many there are.

    Deletable dead code is near-free to remove and shrinks the surface, so it
    outranks cosmetics even though it is boring. Comment noise is last: it is
    the cheapest thing to detect, which is exactly why it crowds out the rest.
    """
    out = []
    ast_r = findings["structure"]
    dup = findings["duplication"]

    orphan_loc = ast_r["orphan_loc"]
    if orphan_loc:
        out.append({
            "rank": "P1", "signal": "orphan_modules",
            "detail": f"{len(ast_r['orphan_modules'])} modules unreachable from entry points "
                      f"({orphan_loc} LOC, {round(100 * orphan_loc / max(ast_r['total_loc'], 1), 1)}% of tree)",
            "why": "Pure subtraction. Deleting shrinks the codebase with no behaviour change.",
            "action": "Verify entry points are declared, confirm no dynamic import, delete.",
        })
    if dup.get("available") and dup["percentage"] > 5:
        out.append({
            "rank": "P1", "signal": "duplication",
            "detail": f"{dup['percentage']}% duplicated lines across {dup['clones']} clones "
                      f"(min_tokens={dup['config']['min_tokens']})",
            "why": "Propagation tax: every edit to one copy obliges finding all siblings.",
            "action": "Consolidate the highest-count files first; they are the reuse candidates.",
        })
    if ast_r["hotspot_count"]:
        worst = ast_r["complexity_hotspots"][:1]
        w = f" worst: {worst[0]['file']}:{worst[0]['line']} cc={worst[0]['complexity']}" if worst else ""
        out.append({
            "rank": "P2", "signal": "complexity_concentration",
            "detail": f"{ast_r['hotspot_count']} function(s) over threshold.{w}",
            "why": "Complexity mass concentrating in few functions is the erosion signature.",
            "action": "Decompose the top 3. Do not touch the tail.",
        })
    if ast_r["error_masking_count"]:
        out.append({
            "rank": "P2", "signal": "error_masking",
            "detail": f"{ast_r['error_masking_count']} bare/swallowed exception handlers",
            "why": "Converts loud failures into silent wrong answers; hides the next defect.",
            "action": "Narrow the exception type or re-raise. Never leave a bare pass.",
        })
    if ast_r["imports_per_module"] < 1.0 and ast_r["modules"] > 10:
        out.append({
            "rank": "P2", "signal": "low_connectivity",
            "detail": f"{ast_r['imports_per_module']} internal imports per module",
            "why": "New code that calls nothing existing is usually code that reinvented it.",
            "action": "Check recent modules against existing utilities before they calcify.",
        })
    if ast_r.get("test_only_reachable"):
        out.append({
            "rank": "P2", "signal": "test_only_reachable",
            "detail": f"{len(ast_r['test_only_reachable'])} modules reachable only from tests: "
                      + ", ".join(ast_r["test_only_reachable"][:5]),
            "why": "Production callers are already zero; only test call sites hold it alive.",
            "action": "Repoint the test call sites, then delete. Cheapest deletions available.",
        })
    graph = findings.get("graph", {})
    if graph.get("available") and graph.get("duplicate_symbol_count"):
        top = graph["duplicate_symbols"][0]
        out.append({
            "rank": "P2", "signal": "duplicate_symbol_names",
            "detail": f"{graph['duplicate_symbol_count']} symbols defined in multiple files "
                      f"(e.g. {top['symbol']} in {len(top['files'])} files)",
            "why": "Name-collision hint from the code graph. Catches drifted copies that "
                   "token clone detection loses once bodies diverge; verify each by eye.",
            "action": "Diff the definitions. Same purpose -> consolidate; different purpose "
                      "-> rename one, so the collision stops masking real drift.",
        })
    js = findings.get("js_dead_code", {})
    if js.get("available") and js.get("unused_files"):
        out.append({
            "rank": "P1", "signal": "js_dead_code",
            "detail": f"{js['unused_files']} unused files, {js['unused_exports']} unused exports, "
                      f"{js['unused_dependencies']} unused deps",
            "why": "Same as orphan modules: subtraction, not refactoring.",
            "action": "Confirm knip entry config first, then delete.",
        })
    return out


def scan(root: Path, entries: list[str], min_tokens: int, cc: int) -> dict:
    cfg = load_config(root)
    entries = list(entries) + [e for e in cfg["entry_points"] if e not in entries]
    structure = pyast.analyze(root, entries, cc_threshold=cc)
    findings = {
        "structure": structure,
        "duplication": duplication(root, min_tokens, cfg),
        "js_dead_code": js_dead_code(root),
        "graph": graph_signals.load(root),
    }
    findings["config"] = cfg
    findings["ranked"] = rank(findings)
    findings["metrics"] = {
        "total_loc": structure["total_loc"],
        "src_loc": structure["src_loc"],
        "test_loc": structure["test_loc"],
        "modules": structure["modules"],
        "orphan_loc": structure["orphan_loc"],
        # Percentage is reported but NOT gated. Verified failure: adding a fourth
        # near-identical service moved duplication from 28.57% to 20.48% while
        # clones went 2 -> 3, because the denominator grew faster than the
        # counted duplicate lines. A ratio gate passes the commit that made
        # things worse. On a growing codebase, gate absolutes.
        "duplication_pct": findings["duplication"].get("percentage"),
        "duplicated_lines": findings["duplication"].get("duplicated_lines"),
        "clone_count": findings["duplication"].get("clones"),
        "complexity_hotspots": structure["hotspot_count"],
        "error_masking": structure["error_masking_count"],
        "imports_per_module": structure["imports_per_module"],
    }
    return findings


# Metrics where an increase is a regression, with tolerance before it trips.
GATES = {
    # src_loc, never total_loc: gating total punishes writing tests.
    "src_loc": ("rel", 0.10),
    "orphan_loc": ("abs", 0),
    "duplicated_lines": ("abs", 0),   # absolute, not %; see metrics note above
    "clone_count": ("abs", 0),
    "complexity_hotspots": ("abs", 0),
    "error_masking": ("abs", 0),
}


def check(root: Path, current: dict) -> int:
    bpath = root / BASELINE
    if not bpath.exists():
        print(f"no baseline at {bpath} -- run `baseline` first", file=sys.stderr)
        return 2
    base = json.loads(bpath.read_text())["metrics"]
    cur = current["metrics"]
    failures = []
    for key, (mode, tol) in GATES.items():
        b, c = base.get(key), cur.get(key)
        if b is None or c is None:
            continue
        limit = b * (1 + tol) if mode == "rel" else b + tol
        if c > limit:
            failures.append(f"  {key}: {b} -> {c} (limit {round(limit, 2)})")
    if failures:
        print("SLOP RATCHET FAILED -- these moved the wrong way:")
        print("\n".join(failures))
        print("\nEither fix, or re-baseline deliberately with a reason.")
        return 1
    print("slop ratchet OK -- no metric regressed beyond tolerance")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("verb", choices=["scan", "baseline", "check"])
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--entry", action="append", default=[],
                    help="Entry-point module/path, repeatable. Declare these or orphan "
                         "detection is guesswork.")
    ap.add_argument("--min-tokens", type=int, default=50)
    ap.add_argument("--cc-threshold", type=int, default=10)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    root = Path(args.path).resolve()
    result = scan(root, args.entry, args.min_tokens, args.cc_threshold)

    if args.verb == "baseline":
        (root / BASELINE).write_text(json.dumps(result, indent=2))
        print(f"baseline written to {root / BASELINE}")
        print(json.dumps(result["metrics"], indent=2))
        return 0

    if args.verb == "check":
        return check(root, result)

    if args.json:
        print(json.dumps(result, indent=2))
        return 0

    m = result["metrics"]
    print(f"== {root.name}: {m['src_loc']} src LOC + {m['test_loc']} test LOC "
          f"across {m['modules']} modules ==")
    if result["duplication"].get("allowlisted_clones"):
        print(f"   ({result['duplication']['allowlisted_clones']} clone(s) allowlisted)")
    print()
    if not result["ranked"]:
        print("No structural findings above threshold.")
    for f in result["ranked"]:
        print(f"[{f['rank']}] {f['signal']}: {f['detail']}")
        print(f"     why: {f['why']}")
        print(f"     do:  {f['action']}\n")
    for name in ("duplication", "js_dead_code", "graph"):
        if not result[name].get("available"):
            print(f"(skipped {name}: {result[name].get('reason')})")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:  # piping into head/less is normal usage
        sys.exit(0)
