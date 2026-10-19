#!/usr/bin/env python3
"""Print a Jupyter notebook as readable text: every cell's source AND its text outputs.

Outputs matter as much as source — printed metrics, shapes and fold scores live there,
and they are the numbers the talk track has to get right.

Usage:
    python3 dump_notebook.py path/to/notebook.ipynb [--max-chars 2500] [--no-outputs]
"""
import argparse
import json
import sys


def cell_outputs(cell, max_chars):
    chunks = []
    for out in cell.get("outputs", []):
        t = out.get("output_type")
        if t == "stream":
            chunks.append("".join(out.get("text", [])))
        elif t in ("execute_result", "display_data"):
            data = out.get("data", {})
            if "text/plain" in data:
                chunks.append("".join(data["text/plain"]))
        elif t == "error":
            chunks.append(f"[ERROR] {out.get('ename')}: {out.get('evalue')}")
    text = "\n".join(c for c in chunks if c.strip())
    return text[:max_chars] + (" …[truncated]" if len(text) > max_chars else "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("notebook")
    ap.add_argument("--max-chars", type=int, default=2500, help="per-cell cap for source and for outputs")
    ap.add_argument("--no-outputs", action="store_true")
    a = ap.parse_args()

    nb = json.load(open(a.notebook))
    print(f"{'=' * 20} {a.notebook} ({len(nb['cells'])} cells) {'=' * 20}")
    for i, c in enumerate(nb["cells"]):
        src = "".join(c.get("source", []))
        print(f"\n--- cell {i} [{c['cell_type']}] ---")
        print(src[: a.max_chars] + (" …[truncated]" if len(src) > a.max_chars else ""))
        if not a.no_outputs and c["cell_type"] == "code":
            out = cell_outputs(c, a.max_chars)
            if out:
                print(f"--- cell {i} OUTPUT ---")
                print(out)


if __name__ == "__main__":
    sys.exit(main())
