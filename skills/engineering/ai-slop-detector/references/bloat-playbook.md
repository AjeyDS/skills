# Bloat playbook

For a codebase that keeps getting bigger. This is a different problem from a
codebase that is bad, and it needs a different intervention.

**Contents**
1. [Diagnose before cutting](#1-diagnose-before-cutting)
2. [Subtract before refactoring](#2-subtract-before-refactoring)
3. [Consolidate in dependency order](#3-consolidate-in-dependency-order)
4. [Install the ratchet](#4-install-the-ratchet)
5. [Choosing gate metrics](#5-choosing-gate-metrics)
6. [Preventing regrowth](#6-preventing-regrowth)

---

## Why growth is its own problem

Code volume is the strongest single predictor of architectural decay. In
measured agent-generated systems, total lines of code correlated with
architectural smells at ρ = 0.94 — close to a straight line — and with
structural and code-level smells at 0.59 and 0.53. File count correlated at
0.72. Growth is not a symptom of decay sitting alongside it; growth is the
mechanism.

That means shrinking the codebase is a quality intervention on its own, before
any refactoring happens, and that a one-time cleanup without a gate buys you a
few weeks.

The industry-scale trend backs this up. Across roughly 623 million analysed
changes from 2023 to 2026: block duplication up 81% to a record high;
within-commit copy/paste up 41%; refactoring line-moves down 70%; cross-file
function connectivity down 35%; long-term legacy maintenance down 74%.
Developers are now around 5x more likely to duplicate than to refactor, having
been 2x more likely to refactor than duplicate in 2022. New code increasingly
stands alone rather than connecting to what exists — the structural signature of
reinvention beating reuse.

---

## 1. Diagnose before cutting

Get the numbers before touching anything, and get them reproducibly.

```bash
python3 scripts/slop_scan.py scan . --entry <your_entry_module> --json > /tmp/slop.json
```

Read four figures:

| Figure | Question it answers |
|---|---|
| `orphan_loc` / `total_loc` | How much of this can simply go? |
| `duplicated_lines`, `clone_count` | How much is the same thing written repeatedly? |
| `imports_per_module` | Is new code connecting to old code, or standing alone? |
| `complexity_hotspots` | Is complexity concentrating or spread? |

Low `imports_per_module` on a large codebase is the reinvention signal, and it
is the one most people never look at. Files that import almost nothing internal
are usually files that rebuilt something the repo already had.

If a git history is available, get the trend rather than the level — whether
these numbers are rising is more actionable than what they are:

```bash
git log --format='%H %ad' --date=short --reverse | awk 'NR%25==1' | while read sha date; do
  git stash -q 2>/dev/null; git checkout -q "$sha" 2>/dev/null || continue
  loc=$(git ls-files '*.py' '*.ts' '*.tsx' '*.js' | xargs cat 2>/dev/null | wc -l)
  echo "$date $sha $loc"
done > /tmp/loc-trend.txt
git checkout -q -
```

Plot LOC against shipped functionality. Volume rising while capability is flat
is accretion, not progress.

---

## 2. Subtract before refactoring

Deletion is the highest-leverage move available and it is consistently
skipped, because it feels like less work than it is worth.

Order:

1. **Orphan modules.** Unreachable from any entry point. Pure subtraction.
2. **Unused exports.** Public surface nobody consumes. Unexport rather than
   delete when the function is still used internally — this shrinks the API
   surface without touching behaviour.
3. **Unused dependencies.** Each one is supply-chain surface and upgrade burden.
4. **Superseded implementations.** The `_v2` alongside the `_v1`, the "new"
   helper next to the old one. Agents add; they rarely retire.

Before deleting anything flagged unreachable, confirm none of these apply:

- Dynamic import (`importlib`, `__import__`, `require()` with a computed path)
- Reflection or registry lookup by string name
- Framework auto-discovery — Django apps, pytest fixtures, Celery tasks, FastAPI
  routers included by convention, Alembic migrations
- Entry points declared in `pyproject.toml` / `package.json`
- Referenced only from templates, configs, or CI

Static reachability is blind to every one of these. The tool proposes; you
verify. Deleting live code once will cost you more trust in the tooling than
the cleanup was worth.

A safe deletion loop:

```bash
git checkout -b slop/subtract
# delete one coherent group
pytest -q && python3 scripts/slop_scan.py scan . --entry <module>
git commit -m "remove unreachable X (was N LOC)"
```

Small commits. If something was reachable after all, you want a cheap revert.

---

## 3. Consolidate in dependency order

Now the duplication. Take the files appearing in the most clones — the scan's
`worst_files` — and work down.

For each clone group, decide which case it is:

- **Accidental duplication.** Same logic, same reason to change. Consolidate.
  This is most of it.
- **Coincidental similarity.** Same shape today, different reasons to change.
  Leave it. Merging these creates a shared abstraction with two masters, which
  is worse than the duplication.
- **Deliberate duplication.** Copied to decouple. Leave it, and comment why —
  an uncommented deliberate duplicate will be "fixed" by the next agent.

The distinguishing question is not "does this look the same" but "would a change
to one require the same change to the other." That question needs judgment, which
is why this step is not automatable and the detection step is.

When consolidating, extract to where the dependency arrow already points. New
shared code placed at the wrong level creates cycles, and cycles are harder to
undo than the duplication was.

---

## 4. Install the ratchet

Without this, everything above regrows. Agent-driven degradation is monotonic;
better prompting reduces where it starts but not how fast it climbs.

```bash
python3 scripts/slop_scan.py baseline .
git add .slop-baseline.json && git commit -m "freeze slop baseline"
```

Then wire the check into three places, in decreasing order of value:

**1. The agent's own verification command.** Highest leverage by a distance. If
an agent sees the failure inside its loop, it fixes it on the next iteration. If
the signal only appears in CI after the PR opens, the agent never sees it and
the human absorbs the cost.

In `CLAUDE.md` / `AGENTS.md` / `SYSTEM.md`:

```markdown
After any change, run:
  pytest -q && python3 scripts/slop_scan.py check . --entry <module>
Both must pass. If the slop check fails, fix the regression -- do not
re-baseline to make it green.
```

**2. A pre-commit hook.**

```bash
#!/bin/sh
python3 scripts/slop_scan.py check . --entry <module> || {
  echo "Slop ratchet failed. Fix, or re-baseline with a stated reason."; exit 1; }
```

**3. CI.** Last line of defence, not the primary one.

Re-baselining is allowed and sometimes correct — a genuine feature does add
lines. Require a reason in the commit message. The discipline being enforced is
noticing, not never growing.

---

## 5. Choosing gate metrics

**Gate absolute counts, not ratios.** This is verified, not theoretical. In a
controlled test, adding a fourth near-identical service moved duplication from
28.57% to 20.48% while clone count went 2 → 3 and duplicated lines 40 → 60. The
percentage *improved* because the denominator grew faster than the counted
duplicate lines. A team gating on "duplication % must not rise" would have
passed the commit that made things worse.

Any ratio metric has this property on a growing codebase. Use them for reporting,
never for gating.

Defaults in `slop_scan.py`, and why:

| Metric | Tolerance | Reasoning |
|---|---|---|
| `total_loc` | +10% | Real features add code. Catches runaway, permits work. |
| `orphan_loc` | 0 | New dead code has no legitimate cause. |
| `duplicated_lines` | 0 | Absolute. Rising means copies accumulating. |
| `clone_count` | 0 | Catches new clone groups even if short. |
| `complexity_hotspots` | 0 | A new function over threshold is a design decision worth defending. |
| `error_masking` | 0 | Never a good reason to add a bare `except`. |

Tune tolerances to a real project, but tune them once and then leave them.
A gate quietly loosened whenever it fires is not a gate.

---

## 6. Preventing regrowth

Detection is downstream of the thing that actually reduces bloat, which is
giving the agent enough context to reuse instead of rebuild.

- **Point at existing utilities explicitly.** Most reinvention happens because
  the agent did not know the helper existed. A short inventory of shared modules
  in `SYSTEM.md` prevents more duplication than any linter catches.
- **Ask for the smallest change that works.** Comprehensiveness is the default
  failure mode of capable models; the counterweight is an explicit budget.
- **Constrain the diff, not just the outcome.** "Do not add new files unless the
  logic has no existing home" is a more effective instruction than "write
  maintainable code."
- **Enforce boundaries mechanically** where the architecture matters:
  `import-linter` (Python) or `dependency-cruiser` (TS/JS) turn layering rules
  into failing checks. See `references/toolchain.md`.
- **Budget for deletion.** Long-term maintenance of old code has fallen 74%
  industry-wide since 2023. If nothing on the plan is ever "retire X," the
  codebase only grows by construction.

Expect these to reduce the problem, not eliminate it. Prompt-side interventions
measurably move the intercept and leave the slope. The ratchet is what holds.
