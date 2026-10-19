---
name: ai-slop-detector
description: Audit a codebase for AI-generated quality decay and fix it, using deterministic analyzers first and reading second. Use this whenever the user wants to review, audit, or clean up code that AI agents wrote; complains that a codebase is bloating, sprawling, growing faster than it should, or "keeps getting bigger"; asks about AI slop, code duplication, dead code, over-engineering, or hallucinated/phantom packages (slopsquatting); wants a quality gate on agent output; or asks whether a given model's output can be trusted. Trigger even when the words "slop" or "AI" are absent -- "why is this repo so big", "clean up this codebase", "find dead code", "is this over-engineered", "review what Claude Code did", "the agent keeps duplicating things" all belong here. Also use when calibrating how hard to review a specific model's work, since a frontier model and a small model fail in opposite directions and need opposite checks.
license: MIT
compatibility: 'Python 3.9+ for the bundled scripts. Optional analyzers: lizard, vulture, radon, import-linter, pip-audit (pip) and knip, jscpd, dependency-cruiser (npm); missing ones are skipped.'
metadata:
  author: AjeyDS
  version: '1.0'
---

# AI Slop Detector

Find and remove the quality decay that AI-assisted development introduces, with
effort spent in proportion to what each defect actually costs.

## The one thing to get right

**Measure with tools first. Read code second. Never read first.**

Reading files to find slop feels like the job and is the wrong move at codebase
scale. Three of the four defects that matter most are whole-graph properties --
is this module reachable at all, does this block exist elsewhere, does complexity
concentrate here -- and no amount of sequential file reading answers them
reliably. Reading gives you an unrepresentative sample, non-reproducible results,
and a token bill proportional to repo size.

Deterministic analyzers give complete coverage, reproducible numbers, and a
ranked shortlist. Then read the top of that list, where judgment is the scarce
input. The division of labour:

| Tools do | You do |
|---|---|
| Find every clone, orphan, hotspot | Decide which duplication is accidental vs. deliberate |
| Produce numbers that repeat | Decide whether an abstraction earns its keep |
| Gate regressions in CI | Design the consolidation and write the fix |

Neither half works alone. Tools emit thousands of findings with no priority.
Reading alone produces confident findings with no coverage.

## Pick a mode

**Audit** — a whole codebase, first time or periodically. Run the full scan,
work the ranked list top-down, stop when the remaining items cost less to live
with than to fix. Finish by writing a baseline.

**Gate** — continuous. A baseline exists; each change must not regress it. This
is the mode that solves bloat, and most requests that sound like audits are
really requests for this.

**Triage** — one PR, branch, or agent handoff. Scan the diff's blast radius
rather than the tree, and check the model-specific failure mode first
(`references/model-tier-failure-modes.md`).

If the user's complaint is about *growth* — bigger every week, sprawling,
accreting — go to `references/bloat-playbook.md` before anything else. A
one-shot audit does not fix a slope.

## Workflow

### 0. Configure once, per repo

Create `.slopconfig.json` at the repo root. Without it the first scan on any
real project is mostly noise:

```json
{
  "entry_points": ["app.main", "mcp_server.server", "app.scripts.some_cli"],
  "allowed_clones": [
    {"a": "schemas/status.py", "b": "lib/status.ts",
     "reason": "cross-boundary enum mirror; needs a contract test, not consolidation"}
  ]
}
```

**Every** entry point must be listed: web app, MCP or RPC server, CLI scripts,
worker processes. A live surface that nothing imports reads as dead. Measured on
a FastAPI-plus-MCP-shaped tree, declaring only the web app produced 5 orphans of
which 3 were false; declaring all three entry points produced 2, both real.

`allowed_clones` is where deliberate duplication gets recorded. Cross-boundary
mirrors (a Python enum and its TypeScript twin), paired validators that must
agree, and hand-synced vocabularies are all legitimate duplication that a
detector will flag forever. Record the reason, or the next agent "fixes" it.

Test paths are excluded from duplication by default and counted separately in
LOC. This is not cosmetic: on a test-heavy tree, test code was 87% of total LOC
and 11 of 12 detected clones were test-to-test at 83% overall duplication. Gating
on totals punishes writing tests, and the real finding drowns.

### 1. Establish the ground truth

```bash
python3 scripts/slop_scan.py scan .
```

Entry points come from the config; `--entry` still works for one-offs. This is load-bearing: reachability analysis with wrong
entry points reports live code as dead, which is the failure mode that destroys
trust in dead-code tooling. If unsure, ask the user rather than guessing.

The scan runs whatever is installed and reports what it skipped. It needs
nothing beyond Python's stdlib to produce a useful result; external tools
(jscpd, knip, semgrep) add coverage. See `references/toolchain.md` for install
commands, per-language equivalents, and the config values that matter.

### 2. Verify the dependencies exist

Frontier models still name packages that do not exist, at roughly 4-6% of
recommendations, and different vendors' models invent *the same* names. Using a
good model is not a defence. Check every third-party import introduced by AI:

```bash
pip index versions <pkg>     # or: pip download --no-deps -d /tmp <pkg>
npm view <pkg> versions
```

Treat a package that does not resolve as a stop-the-line finding, not a typo to
fix. Do not install it to see what happens. Details and the specific
high-frequency confabulations are in `references/evidence.md`.

### 3. Work the ranked list, not the raw findings

The scan orders findings by cost. Respect that order, and note what it puts
last.

- **P1 Orphan modules / dead files.** Pure subtraction: deleting shrinks the
  codebase with no behaviour change. Boring, and the highest ratio of benefit to
  risk available. Do this first.
- **P1 Duplication.** Each clone imposes a propagation tax on every future edit.
  Consolidate the files that appear in the most clones.
- **P2 Complexity concentration.** Decompose the worst two or three. Leave the
  tail alone; a long list of mildly complex functions is not a problem worth
  spending on.
- **P2 Error masking.** Bare `except:` and swallowed exceptions turn loud
  failures into silent wrong answers. Cheap to fix, disproportionately harmful
  to leave.
- **P2 Test-only-reachable modules.** Production callers are already zero; only
  test call sites hold the code alive. These are the cheapest deletions
  available — repoint the tests, then delete.
- **P3 Comment and naming noise.** Hollow claims ("optimized for performance"
  with no measurement), comments restating the function name, marketing
  adjectives in technical docs.

### 4. Fix, then lock the gain in

A fix that is not gated will be undone by the next agent iteration. After
remediating:

```bash
python3 scripts/slop_scan.py baseline .          # freeze current numbers
python3 scripts/slop_scan.py check . --entry ... # non-zero exit on regression
```

Wire `check` into the command the agent runs after every change, not only into
CI. A signal an agent sees during its loop gets fixed on the next iteration; a
signal that only appears in CI after the PR opens never reaches it.

## If the repo already has a migration ledger

Some codebases carry a hand-maintained deprecation ledger: what is being
replaced, what survives, and the condition that would make removal safe. That is
strictly better than anything an analyzer produces, because it records *why*
code survives, which cannot be inferred.

Do not duplicate it. Make it self-verifying instead. Most removal triggers are
executable predicates written as prose — "grep returns only comments", "zero
callers in these directories", "the script prints 0", "the build is green".
Declare them in `.slopledger.json` and run:

```bash
python3 scripts/ledger_check.py .          # report drift
python3 scripts/ledger_check.py . --strict # non-zero exit on drift
```

`command` predicates run as shell commands, so only run this on a ledger you or
the user wrote. Read an unfamiliar repo's `.slopledger.json` before running it.

It reports three conditions, and the third is the one that matters: a row
recorded as ready-to-cut whose trigger no longer holds. A stale green row is
worse than no row, because it asserts a deletion is safe without evidence. Rows
with no machine-checkable trigger are reported as needing hand verification
rather than silently passing.

A caveat worth knowing: a `command` predicate cannot distinguish "the script
reported zero" from "the script crashed". Both are reported as not-met, which is
the safe direction, but read the detail line before concluding a row regressed.

## Calibrate review depth to the model

Different model tiers produce opposite defects, so a single checklist misses
half of them. Read `references/model-tier-failure-modes.md` before reviewing a
specific agent's output. In short:

- **Small / non-reasoning models** produce *surface* slop: copy-paste,
  reimplemented helpers, filler comments, higher package-hallucination rates.
  Cheap to detect. Linters and clone detection catch most of it.
- **Frontier / reasoning models** produce *structural* slop: bloated methods
  that handle every edge case in one block, speculative abstractions, God
  classes, and modules split into files without being split into
  responsibilities. It passes tests, has type hints and docstrings, and reads as
  professional work. Cosmetic checks rate it clean. This is the expensive kind.
- **Agentic loops** produce *accretion* slop regardless of model: quality
  degrades monotonically as the agent extends its own prior output. This is a
  slope, and measured evidence says better prompting moves the starting point
  without changing the slope.

The practical consequence: **do not relax review because a strong model wrote
the code.** Change what you look for.

## What not to spend effort on

Comment cosmetics are the cheapest thing to detect, which is exactly why they
crowd out everything else. An audit that returns forty buzzword hits and no
structural findings has failed, however thorough it looks. If a report is mostly
comment noise, the analysis did not run deep enough.

Also skip: chasing a duplication *percentage* target (it falls as a codebase
grows even while absolute duplication rises — verified), and Maintainability
Index (a formula whose absolute values are not comparable across languages or
tools).

Do not delete anything flagged as unreachable without confirming there is no
dynamic import, reflection, plugin registry, or framework auto-discovery
reaching it. Reachability analysis is blind to all four.

## Reference files

- `references/model-tier-failure-modes.md` — the three failure signatures, which
  checks catch each, and why detection difficulty rises with model capability.
- `references/toolchain.md` — what to install per language, which config values
  change the answer, known false-positive traps.
- `references/bloat-playbook.md` — for codebases growing faster than their
  functionality. Baseline, ratchet, consolidation order.
- `references/evidence.md` — the measurements behind every claim here, with
  sources and their limitations.

## Scripts

- `scripts/slop_scan.py` — `scan` | `baseline` | `check`. Orchestrates available
  tools, ranks by cost, gates regressions.
- `scripts/pyast.py` — stdlib-only Python analyzer: import-graph reachability
  (production vs test-only), complexity, error masking, connectivity. Works with
  zero dependencies installed.
- `scripts/ledger_check.py` — evaluates declared removal triggers from
  `.slopledger.json` and reports rows whose recorded status disagrees with
  reality.
- `scripts/graph_signals.py` — optional adapter: if `graphify-out/graph.json`
  exists (from the Graphify tool, PyPI package `graphifyy`), derives god-node
  ranking, duplicate-symbol-name hints, and cross-surface coupling from it.
  Degrades silently when absent. The duplicate-symbol hint is the complement of
  token clone detection: it catches same-named copies *after* their bodies have
  drifted apart (when clone tools lose them) and misses renamed copies — treat
  it as a diff-these-by-eye list, never a gate, since shared method names
  (`fetch`, `create`) across sibling services are a pattern, not a defect.

## Known limits

Reachability follows static import edges. It cannot see dynamic imports,
string-keyed registries, or framework auto-discovery. Decorator registration
(`@router.get`, `@mcp.tool`) is fine as long as the module is imported
somewhere, which is why declaring every entry point matters more than any other
setting.

Template languages (Jinja, Typst, `.tex.j2`) do not tokenize usefully for clone
detection. Duplication across templates needs review, not tooling.

Divergent duplicates — two copies that have drifted apart — are the hardest
case. Clone detection finds them while they are still similar and loses them
once they diverge, which is exactly when they become dangerous. A contract test
pinning both to the same source of truth is the real fix.
