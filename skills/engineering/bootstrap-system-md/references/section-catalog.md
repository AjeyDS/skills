# SYSTEM.md Section Catalog (v4)

A menu. Pick what the repo supports with real content, sized to the level
chosen in Phase 1. If numbering sections, freeze the numbers from day one.

## Contract header (ALWAYS — terse form, ≤15 lines)

```markdown
# <Project Name> — System Reference

> **Living document — contract for any agent or human changing this repo.**
> 1. **Update after change.** If your change alters an entity, invariant,
>    endpoint, workflow step, or convention described here, update this
>    file in the same change set.
> 2. **Integrate, don't append.** Rewrite descriptions in present tense.
>    Dates belong in `git log` and in the ledger sections (Gotchas,
>    Deferred, Migrations) — nowhere else.
> 3. **Log lessons.** After a session: gotchas that cost real time; deferred
>    items you chose not to fix (each with a trigger); a new section for any
>    area you worked in that isn't covered.
> 4. **Ledgers shrink.** Deferred leaves when shipped or 30 days without a
>    trigger; migration rows leave when complete; gotchas leave when their
>    cause becomes enforced by a test, type, lint, or pinned invariant.
> 5. **Caps are earned.** `scripts/check_system_md.py` gates size in bytes;
>    raise the cap only right after a grooming/extraction pass that failed
>    to get under it, with `--reason`. The gate writes the revision stamp.
> Reference by anchor or rule ID, never "§N". Rationale:
> `docs/system-md-contract.md`. contract: v5. Last revision: <gate-written>.
```

Small repos may drop the rationale link and the migrations mention.

## Table of contents (ALWAYS)

`- [Title](#anchor) — <one clause of scope>`, ≤16 lines.

## Routing table (medium/large — directly under the TOC)

```markdown
**Read for your task** (then grep; do not read the whole file for a one-line fix)
| Working on | Read |
|---|---|
| backend write path | Workflow, Invariants, Dev env, Gotchas |
| <surface> | <sections> |
| planning a feature | Architecture, Workflow, Invariants, Decision record |
| any merge | Dev env (merge checklist) + sections whose subject files changed |
```
≤10 rows, derived from the sections actually emitted.

## What this is (ALWAYS)

2–4 sentences: what it does, surfaces, one-line data-flow. No adjectives.

## Repo layout (ALWAYS)

Annotated tree, purpose per entry, including non-code dirs that matter.

## Architecture at a glance (≥2 moving parts)

ASCII flow under 15 lines; where state lives.

## Core entities and their lifecycles (when there is a domain model)

`### Entity (path)` per entity; key fields; status vocabulary and legal
transitions; dedup rules; derived-state definitions. Bold-lead bullets,
present tense. **Reference tier**: medium/large repos extract to
`docs/entities/<entity>.md` at the warn threshold, leaving an index here.

## The main workflow, end to end (primary user journey)

Numbered steps naming route/endpoint/command at each.

## Cross-cutting invariants (ALWAYS)

```markdown
- **<name>** (`inv-<slug>`): <rule>. Enforced by `<test or module>`;
  because <one clause>.
```

No enforcement point → give it one or demote to a convention note. Register
IDs in `.system_md_enforcement.json` (medium/large) so the gate verifies
they still exist.

## Agent surfaces (when the repo exposes MCP/chat/LLM integrations)

Location, toolset, deliberate capability differences per surface. Usually
the fastest-changing reference-shaped section — first extraction candidate
in large repos.

## Frontend / UI conventions (when there is a UI)

Framework quirks, token locations, single-source-of-vocabulary components,
naming rules. Reference tier.

## Dev & test environment (ALWAYS)

Runtime, install, DB/container names + ports, test command with env var
NAMES, suite baseline, "never verify against X" traps, gate invocation.
Large: the merge-checklist line. **Never values for secrets.**

## Design-decision record (medium/large)

One line per owner decision, newest last:
`- <date> — <decision>; superseded <alternative> because <one clause>.`
Pointer to ADRs/design docs for the long form; never inline the full
rationale. The superseded alternative is the line agents most need when
planning and most often lack. Seed from ADRs, design docs, revert commits.

## Gotchas that have bitten (ALWAYS — ledger with lifecycle)

```markdown
## Gotchas that have bitten (ledger — evict when the cause becomes enforced)

- **<name>**: <symptom>. Cause: <cause>. Rule: <do this instead>. (<date>)
```

Lifecycle: observed → documented here → enforced (test/type/lint/pinned
invariant) → evicted. On eviction, promote into Invariants with the
enforcement point, or into the enforcement map.

## Deferred items (medium/large — ledger, trigger-required)

```markdown
## Deferred items (ledger — ≤7 here, overflow in docs/deferred.md; each
## needs a trigger; 30 days without one → give it one or delete)

1. **<item>** — why deferred; **do when** <trigger>. (<date>)
```

A deferred item with no trigger is a graveyard entry by construction.

## Active migrations & deprecation ledger (only when something is built twice)

```markdown
| Old | New | Still on old | Remove when |
```

The section meant to reach zero rows. Large: mirror rows in a JSON sidecar
the gate checks.

## Style reminders

Backtick identifiers; imperative rules with enforcement points; bold-lead
bullets; keep the "because"; no dates outside ledgers; no secret values;
no "§N" in text that outlives a renumbering.
