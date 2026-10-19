"""Optional signals from a Graphify graph.json, if one exists in the repo.

Graphify's AST pass gives two things the stdlib Python walker cannot:
function-level nodes across ~36 tree-sitter grammars (so TS/JS/SQL surfaces
join the same graph as Python), and resolved cross-module call edges.

Measured caveats, from running graphify 0.9.32 on a controlled fixture:
- The code-only pass is mostly containment: 326 of 369 edges were `contains`,
  16+16 import edges, and only 2 resolved `calls` edges. Rich semantic edges
  come from the LLM pass, which costs API calls and is not assumed here.
- Raw degree ranking is dominated by test files exactly like every other
  metric, so the same test filtering applies.

Signals derived:
  god_nodes           highest-degree non-test symbols (complexity concentration
                      cross-check for the AST hotspot list)
  duplicate_symbols   same function/class name defined in multiple non-test
                      files -- a *name-collision hint*, not clone detection:
                      it catches the drifted-copy case (same name, diverged
                      bodies) that token-based clone tools lose after drift,
                      and misses copies that were renamed.
  cross_surface       files whose symbols are referenced from a different
                      top-level directory (candidate contract-test sites).
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

GRAPH = "graphify-out/graph.json"

_TEST_MARKERS = ("test", "spec", "fixture", "conftest")


def _is_test(path: str) -> bool:
    low = path.lower()
    return any(m in low for m in _TEST_MARKERS)


def load(root: Path) -> dict:
    gpath = root / GRAPH
    if not gpath.exists():
        return {"available": False, "reason": f"no {GRAPH} (run graphify extract)"}
    try:
        g = json.loads(gpath.read_text())
        nodes = {n["id"]: n for n in g["nodes"]}
        edges = g["edges"]
    except (json.JSONDecodeError, KeyError) as exc:
        return {"available": False, "reason": f"unreadable graph.json: {exc}"}

    deg: dict[str, int] = defaultdict(int)
    for e in edges:
        # containment edges say "file has a function" -- structure, not coupling.
        if e.get("relation") == "contains":
            continue
        deg[e["source"]] += 1
        deg[e["target"]] += 1

    god = []
    for nid, d in sorted(deg.items(), key=lambda kv: -kv[1]):
        n = nodes.get(nid)
        if not n:
            continue
        src = str(n.get("source_file") or "")
        if not src or _is_test(src):
            continue
        god.append({"symbol": n.get("label", nid), "file": src, "degree": d})
        if len(god) >= 15:
            break

    # Same symbol name defined in more than one non-test file.
    by_name: dict[str, set[str]] = defaultdict(set)
    for n in g["nodes"]:
        label = str(n.get("label", ""))
        src = str(n.get("source_file") or "")
        if label.endswith("()") and src and not _is_test(src):
            by_name[label].add(src)
    dup_symbols = sorted(
        ({"symbol": name, "files": sorted(files)}
         for name, files in by_name.items()
         if len(files) > 1 and not name.startswith(("__", "main(", "test"))),
        key=lambda d: -len(d["files"]),
    )

    # Edges whose endpoints live under different top-level directories.
    def _top(path: str) -> str:
        return path.split("/", 1)[0] if "/" in path else path

    cross: dict[tuple, int] = defaultdict(int)
    for e in edges:
        if e.get("relation") == "contains":
            continue
        a = nodes.get(e["source"], {}).get("source_file") or ""
        b = nodes.get(e["target"], {}).get("source_file") or ""
        if a and b and not _is_test(a) and not _is_test(b) and _top(a) != _top(b):
            cross[(_top(a), _top(b))] += 1
    cross_surface = [{"from": a, "to": b, "edges": c}
                     for (a, b), c in sorted(cross.items(), key=lambda kv: -kv[1])]

    return {
        "available": True,
        "nodes": len(nodes),
        "edges": len(edges),
        "god_nodes": god[:10],
        "duplicate_symbols": dup_symbols[:20],
        "duplicate_symbol_count": len(dup_symbols),
        "cross_surface": cross_surface[:10],
    }
