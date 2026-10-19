"""Evaluate deprecation-ledger removal triggers automatically.

A hand-maintained migration ledger is the best dead-code tool there is, because
it records *why* something survives and what would make it safe to delete --
which no analyzer can infer. Its weakness is decay: triggers are written as
prose and re-verified by hand, so a row silently rots into claiming a deletion
is safe without evidence.

Most triggers are already executable predicates in disguise:
    "grep -rn pdflatex backend/app returns only comments"
    "zero callers in frontend/, extension/, mcp_server/"
    "tsc --noEmit and npm run build green"
    "script prints jobs_touched=0"

Declare those in .slopledger.json and this runs them. Rows whose predicates all
pass are reported as ready-to-cut with evidence attached; rows that regress are
reported as newly blocked.

Predicate kinds:
  absent          pattern must not appear in paths (comment-only hits ignored
                  when "ignore_comments": true)
  count_at_most   pattern appears in at most N places
  command         shell command must exit 0
  command_stdout  shell command stdout must contain a string
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

LEDGER = ".slopledger.json"

COMMENT_PREFIXES = ("#", "//", "*", "<!--", '"""', "'''")


def _rg(pattern: str, paths: list[str], root: Path, ignore_comments: bool) -> list[str]:
    """Prefer ripgrep, fall back to grep. Returns matching lines as file:line:text."""
    for cmd in (["rg", "-n", "--no-heading", pattern, *paths],
                ["grep", "-rn", "-E", pattern, *paths]):
        try:
            res = subprocess.run(cmd, cwd=root, capture_output=True, text=True, timeout=120)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
        if res.returncode > 1:  # 1 == no matches, which is a valid answer
            continue
        hits = [ln for ln in res.stdout.splitlines() if ln.strip()]
        if ignore_comments:
            kept = []
            for ln in hits:
                body = ln.split(":", 2)[-1].strip()
                if not body.startswith(COMMENT_PREFIXES):
                    kept.append(ln)
            hits = kept
        return hits
    return ["<no grep available>"]


def check_predicate(pred: dict, root: Path) -> tuple[bool, str]:
    kind = pred.get("kind")

    if kind in ("absent", "count_at_most"):
        hits = _rg(pred["pattern"], pred.get("paths", ["."]), root,
                   pred.get("ignore_comments", False))
        limit = 0 if kind == "absent" else pred.get("max", 0)
        ok = len(hits) <= limit
        if ok:
            return True, f"{len(hits)} hit(s) <= {limit}"
        sample = "; ".join(h[:90] for h in hits[:3])
        return False, f"{len(hits)} hit(s) > {limit}: {sample}"

    if kind in ("command", "command_stdout"):
        try:
            res = subprocess.run(pred["cmd"], cwd=root, shell=True,
                                 capture_output=True, text=True,
                                 timeout=pred.get("timeout", 600))
        except subprocess.TimeoutExpired:
            return False, "timed out"
        if kind == "command":
            return res.returncode == 0, f"exit {res.returncode}"
        needle = pred["contains"]
        ok = needle in res.stdout
        return ok, f"{'found' if ok else 'missing'}: {needle!r}"

    return False, f"unknown predicate kind {kind!r}"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--id", help="check a single row")
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero if any row's recorded status disagrees with reality")
    args = ap.parse_args()

    root = Path(args.path).resolve()
    lpath = root / LEDGER
    if not lpath.exists():
        print(f"no ledger at {lpath}", file=sys.stderr)
        return 2

    rows = json.loads(lpath.read_text())["rows"]
    if args.id:
        rows = [r for r in rows if r["id"] == args.id]

    drift = 0
    for row in rows:
        preds = row.get("triggers", [])
        if not preds:
            print(f"?  {row['id']:<28} no machine-checkable trigger "
                  f"(recorded: {row.get('status', '?')}) -- verify by hand")
            continue

        results = [(p, *check_predicate(p, root)) for p in preds]
        met = all(ok for _, ok, _ in results)
        recorded = row.get("status", "unknown")
        expected_green = recorded == "ready-to-cut"

        if met and not expected_green:
            mark, note = "^", f"trigger now MET (recorded: {recorded}) -> promote to ready-to-cut"
            drift += 1
        elif met:
            mark, note = "OK", "trigger met, still ready-to-cut"
        elif expected_green:
            mark, note = "!!", "recorded ready-to-cut but trigger NO LONGER met -> stale row"
            drift += 1
        else:
            mark, note = "--", f"blocked as recorded ({recorded})"

        print(f"{mark:<3}{row['id']:<28}{note}")
        for pred, ok, detail in results:
            if not ok or mark in ("^", "!!"):
                label = pred.get("pattern") or pred.get("cmd", "")
                print(f"       {'pass' if ok else 'FAIL'}  {label[:60]:<62}{detail}")

    print(f"\n{len(rows)} row(s) checked, {drift} disagreeing with recorded status")
    return 1 if (args.strict and drift) else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        sys.exit(0)
