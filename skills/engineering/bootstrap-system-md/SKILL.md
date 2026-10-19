---
name: bootstrap-system-md
description: 'Explore a codebase and generate its first SYSTEM.md, a single tool-agnostic living reference any coding agent (Claude Code, Codex, Cursor, Aider, Gemini CLI) reads before working on the repo, or upgrade an existing SYSTEM.md to the current contract. Use when the user asks to "create a SYSTEM.md", "document this codebase for agents", "set up project context", "generate a CLAUDE.md / AGENTS.md", "upgrade my SYSTEM.md", or complains that agents keep re-learning the same things. Any language or size; ceremony scales to the repo. Output: SYSTEM.md, root shims, and a sized hygiene gate script.'
license: MIT
compatibility: Any coding agent with read/write access to the repo. The generated hygiene gate is a Python 3 script.
metadata:
  author: AjeyDS
  version: '1.0'
---

# Bootstrap SYSTEM.md

Generate the first SYSTEM.md for a repository by exploring it autonomously, then hand future agents a living document they are contractually obligated to keep updated **and compressed**. One dense file of true, load-bearing facts beats scattered docs: it stays internally consistent, survives tool churn, and is cheap to keep honest.

The file is operational memory for agents, auditable by a human: entities and lifecycles, invariants pinned to the tests that enforce them, commands that actually work, and ledgers of lessons paid for.

## Scale the ceremony to the repo (decide this first)

Everything below has a small, medium, and large form. Pick the level from repo signals during Phase 1 and **say which level you chose and why** in the delivery summary. Over-instrumenting a small repo gets the whole system deleted; under-instrumenting a large one lets it rot.

| Signal | Small | Medium | Large |
|---|---|---|---|
| Source files | < ~50 | 50–500 | > 500 or monorepo |
| Tests | few / none | a real suite | large suite, CI present |
| Contributors / agents | 1 person, 1 agent | 1–3 people | multiple people or parallel agent lanes (worktrees, handoff docs) |
| **SYSTEM.md** | 60–150 lines, 5–7 sections | 150–400 lines | 400–1000 lines, two-tier (orientation root + reference docs) |
| **Ledgers** | Gotchas only | + Deferred (trigger-required) | + Active migrations (when anything is built twice) |
| **Gate** | length + accretion + shipped-in-deferred; run manually | + per-section budgets, two-threshold warn/fail; pre-commit or CI | + enforcement-point verification, `--reason` re-baselining, merge checklist; CI required |
| **Contract header** | 5 terse rules | 5 rules + link to rationale doc | same, plus multi-lane merge rule |

## The failure modes this design counters

Every artifact exists because a real constitution failed one of these ways in production:

1. **Decay** — descriptions go stale. Counter: update-after-change, executed by the agent that did the work.
2. **Accretion** — agents honor the contract by appending dated paragraphs; the file becomes a changelog. Counter: integrate-don't-append; dates only in ledgers; accretion detector in the gate.
3. **Audience drift** — agent-maintained prose stops being human-scannable, so the human can't audit it. Counter: TOC, bold-lead-term rule bullets, present tense, preserved "because" clauses.
4. **Discovery failure** — the file is right but never opened; nothing auto-loads it. Counter: mandatory root shims.
5. **Interface ossification** — section numbers get cited from code/docs, then a grooming pass renumbers them. Counter: anchors or frozen numbers from day one; no ordinals inside the contract text.
6. **Merge falseness** — parallel lanes each update what they know; the merge describes neither branch. Counter (large only): merge checklist + enforcement verification.
7. **Ledger graveyarding** — append-only ledgers without eviction become the new bloat; deferred items with no trigger are read every session and acted on never. Counter: gotcha lifecycle (evict on enforcement), trigger-required deferred items, ledgers named as shrinking sections.
8. **Metric gaming** — once the size gate has teeth, agents satisfy its letter and defeat its purpose: a line cap is met by widening lines (200-character bullets cost the same tokens and read worse). Classic Goodhart; it only appears after the gate starts failing. Counter: cap measured in bytes, with line count kept only as a readability signal; a long-line check; and gate-written metadata so no stamp depends on a human remembering.
9. **Deferred extraction** — a flagged extraction candidate that survives audit after audit is how an orientation file silently becomes reference material; the warning is read and never acted on. Counter: an extraction warning that persists across two gate baselines escalates to FAIL.

## Ground rules

1. **Grounded claims only.** Never infer from stack defaults. Unverifiable → omit or `TODO(verify): <what>`.
2. **Autonomous first pass.** No interviewing. Gaps become TODO markers and empty ledger structure.
3. **Adaptive sections.** `references/section-catalog.md` is a menu. Skip anything that would be empty or generic.
4. **Dense and scannable.** Short declarative lines; paths in backticks; every rule bullet opens with a **bolded subject**; one rule per bullet; keep the one-clause "because". Delete any sentence true of a different project.
5. **Never write secret values.** The file is committed and injected into every agent's context. Document env var *names*, config *locations*, and port *numbers* — never credentials, tokens, connection strings, or API keys, even "example" ones that are real.
6. **Anchors, never ordinals.** External references (code, configs, handoff docs) use markdown anchors or stable rule IDs (`SYSTEM.md#inv-<slug>`). If the repo prefers numbered sections, numbers are **frozen** from day one — never renumbered, gaps allowed. The contract text itself refers to sections by name, never "§N".
7. **Tool-agnostic root.** `SYSTEM.md` at repo root; shims for every tool that auto-loads a differently-named file.
8. **Version-stamped contract.** The header carries `contract: v5`. Upgrade mode keys on it.

## Workflow

### Phase 1 — Survey and level selection

- `ls` root; read README/CONTRIBUTING, build files, package manifests, compose files, CI configs
- Count source files, tests, recent contributors (`git shortlog -sn --since="3 months ago"`); look for worktrees, `docs/plans/`-style handoff docs, multiple agent config files → **pick the level**
- Harvest existing agent context (`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursor/rules`, `docs/`) — absorb, mark superseded
- Map top-level directories; locate the data layer

### Phase 2 — Deep read (priority order; stop at diminishing returns)

1. **Entry points** — main/app/server, routers, CLI definitions
2. **Domain models** — status enums, timestamps, soft-delete flags imply lifecycles
3. **Write paths** — validation guards, transaction boundaries, defensive checks: this is where invariants live, and each one has an enforcement point nearby (a test, a type, a constraint)
4. **Tests** — names inventory intended behavior; skipped/xfail tests reveal known problems
5. **Config/env** — variable names, ports, external services, flags (names, never values)
6. **Git archaeology** — `git log --oneline -30`; commits matching `fix|revert|hotfix` (candidate gotchas); `TODO|FIXME|HACK` comments (candidate deferred items); anything implemented twice (candidate migration rows)

Scratch list headings: **entities**, **invariants + their enforcement points**, **commands that work**, **suspected gotchas**, **in-flight migrations**.

### Phase 3 — Write SYSTEM.md

From the catalog, always include:

- **Contract header** — the five rules, terse (≤15 lines). Medium/large: link a `docs/system-md-contract.md` holding the rationale (generated from `references/contract-rationale.md`) so agents read rules every session but the *why* stays in-repo for human auditors, not in every context window.
- **Table of contents** — one line per section, anchor-linked, one clause of scope
- **Routing table** — directly under the TOC, ≤10 lines: which sections a session reads for which kind of work ("extension work: Agent surfaces, Gotchas; backend write path: Workflow, Invariants, Dev env; planning: Architecture, Workflow, Invariants"). Agents already read in slices; the table makes the slice explicit so a copy fix does not pay for the whole file. Derive it from the sections actually emitted; small repos may omit it.
- **What this is**, **Repo layout**, **Dev & test environment** (verified commands; names not values)
- **Cross-cutting invariants** — every entry: `**name** (\`inv-<slug>\`): rule. Enforced by \`<test/module>\`; because <why>.` A rule with no enforcement point is visibly a wish: give it one or demote it to a convention note. Medium/large: register `inv-<slug>` → `{path, symbol}` in `.system_md_enforcement.json`.
- **Gotchas that have bitten** — dated `symptom → cause → rule`, ≤3 lines each, **with its lifecycle rule in the section header**: a gotcha is evicted when its cause becomes enforced (test, type, lint, or invariant with enforcement point) — it promotes into the invariants section or the enforcement map rather than accumulating.
- Level-gated: **Deferred items** (each item MUST carry a trigger — "do when X"; items with no trigger after 30 days are given one or deleted; keep the file's list to ≤7, overflow to `docs/deferred.md` under the same contract); **Active migrations** (only when something is built twice; rows carry removal triggers; the section meant to reach zero).

- **Design-decision record** (medium/large) — one line per owner decision: `<date> — <decision>; superseded <alternative> because <one clause>`. Seed from ADRs, design docs, and revert commits. The alternative-and-why is the part agents most often lack when planning, and if the repo does not own it, it ends up in a vendor's per-user memory store instead of git.

Everything else (architecture flow, entity lifecycles, workflow, agent surfaces, UI conventions) only when the repo supplies real content.

**Two tiers (medium/large):** the root file is the *orientation tier* — what/layout/architecture/invariants/env/workflow/ledgers — and stays single-file. *Reference-tier* sections (entity lifecycles, UI conventions, agent-surface catalogs) are consulted per task and extract to `docs/<section>/*.md` with an anchor-linked index left in the root. Extraction candidate = the largest section that is both reference-shaped and fast-changing. Extract deliberately at the warn threshold, not under fail pressure.

Style calibration:

```
- **Dedup rules** (`inv-dedup-hash`): exact hash always; URL fallback ONLY
  when raw text is absent. Enforced by `tests/test_jobs.py::test_dedup`;
  because careers pages reuse URLs across postings.
```

No dates outside ledgers. History lives in `git log`.

### Phase 4 — Verify

- Commands runnable (execute where possible) or `TODO(verify)`-marked; referenced paths exist
- No generic filler; no secret values; no "§N" inside contract text
- Bold-lead compliance on rule bullets; 5-rule scannability spot-check
- Every invariant has an enforcement point or is demoted
- Length within the level's band

### Phase 5 — Gate, shims, delivery

1. Write `SYSTEM.md` to root.
2. **Generate `scripts/check_system_md.py`** from `references/gate-template.py`, configured to the level (`LEVEL = "small"|"medium"|"large"`). All levels: **the cap is in BYTES** (lines are reported, never gated — a line cap is gamed by widening lines), **WARN at 90%, FAIL at 100%**, the warn naming the extraction candidate; a long-line readability check (WARN over 160 chars outside tables/code); accretion detector; shipped-in-deferred; trigger-less deferred items. Medium+: per-section byte budgets FAIL; **an extraction warning that persisted across the last two recorded baselines escalates to FAIL**; the gate **writes the revision stamp** (`--stamp` rewrites the header's last-revision line from git, so no human-maintained stamp exists to go stale). Large: enforcement-point verification, **plus a WARN for every invariant id in the file with no entry in the enforcement map** (a pinned-looking rule with no pin is the worst case — it reads as checked); `--update-baselines --reason "<text>"` required. Initial cap ≈ 1.15 × generated bytes. Wire to CI if CI exists (medium+); otherwise document manual invocation.
3. **Emit shims — mandatory.** Root `CLAUDE.md` and `AGENTS.md` (offer `GEMINI.md` and `.cursor/rules/system.mdc` if those tools are evidenced):
   ```
   Read SYSTEM.md at the repo root before doing anything. It is the
   authoritative project reference. Keep it updated per its header contract.
   ```
   Framework-owned files in subdirectories coexist; a root file with real content gets absorbed into SYSTEM.md and reduced to the shim line.
4. Summarize: level chosen and why, sections included/skipped, TODO(verify) count, invariants with/without enforcement points, seeded ledger entries, cap and thresholds.

## The self-maintenance contract (what the header says)

1. **Update after change** — a change altering any described entity, invariant, endpoint, workflow step, or convention updates this file in the same change set.
2. **Integrate, don't append** — rewrite descriptions in present tense; dates only in the ledger sections (named, not numbered).
3. **Log lessons** — after a session, add gotchas that cost real time and deferred items you chose not to fix (with a trigger). Add a section for any area you worked in that this file doesn't cover.
4. **Ledgers shrink** — deferred items leave when shipped or when 30 days pass without a trigger; migration rows leave when complete; gotchas leave when their cause becomes enforced.
5. **Caps are earned** — the size cap (bytes) rises only right after a grooming or extraction pass that failed to get under it, with a recorded reason. The gate, not a hand, writes the revision stamp.

Rules 1 and 3 counter decay; 2, 4, 5 counter accretion and graveyarding; shims counter discovery failure; anchors counter ossification; the gate enforces what is greppable and the human audits the rest.

## Upgrade mode (existing SYSTEM.md → current contract)

Trigger: a SYSTEM.md already exists. **Do not regenerate.** The file holds paid-for facts; the upgrade touches only the scaffolding around them.

1. **Detect the version.** Read the header for `contract: vN`. Absent → treat as pre-v4 (v1–v3 had no stamp). v4 → apply the v4→v5 rows. Read the gate script if present and note its checks.
2. **Diff against the current contract**, rule by rule and artifact by artifact, using `references/upgrade-matrix.md`. Produce a plan listing each delta with its class: *header text*, *section structure* (e.g. gotcha lifecycle line in the section header, trigger field on deferred items), *new artifact* (rationale doc, enforcement map), *gate config*, *shim*. Every delta must be content-preserving; if applying a delta would require rewriting or deleting a fact, it is out of scope — flag it as a follow-up grooming item instead.
3. **Apply in that order**, one commit per class, so any class is independently revertable. Never renumber sections. Never move content between tiers as part of an upgrade — extraction is a separate, human-approved grooming step, even when the new gate flags it.
4. **Regenerate the gate** from the current template with the repo's existing CONFIG values (cap, level, paths) carried over — never reset a cap downward silently; if the current template would fail on the existing file, run the gate, report the failures, and leave them as the human's grooming backlog.
5. **Stamp** `contract: v<N>` in the header and record the upgrade in the rationale doc's changelog line (replace, don't accrete).
6. **Verify**: line-level diff shows only scaffolding changes; every fact line in the old file exists verbatim in the new one; the gate runs (pass or fail is reported, not hidden).

The stamp is what makes v5, v6 upgrades cheap: each future contract version ships an upgrade-matrix row, and the skill applies only the rows newer than the stamp.

## Edge cases

- **Existing partial docs**: absorb verified content, mark superseded, ask before deleting files.
- **Repo you can't run**: generate anyway; all commands `TODO(verify)`; say so.
- **Multi-lane / parallel agents (large)**: add a merge-checklist line to the dev section — "on merge, list SYSTEM.md sections whose subject files changed on both sides and re-verify each." Note in the summary that the contract bounds staleness to one round, not to zero: the file is accurate at merge boundaries and can drift mid-round.
- **Monorepo**: one root orientation file with per-package blocks; reference-tier extraction per package.
- **Tiny repo**: 60 lines is correct. Do not pad; do not emit a deferred or migration ledger with nothing in it.
