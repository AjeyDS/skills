# Upgrade matrix — contract versions and the deltas between them

Upgrade mode applies every row newer than the file's `contract:` stamp.
Each delta is content-preserving: it changes scaffolding, never facts.
Rows marked (grooming) are reported as a backlog item, not applied.

## unstamped (v1–v3) → v4

| Class | Delta |
|---|---|
| header | Replace the header block with the v4 terse form; carry over the project name and last-revision date. Move any rationale prose found in the old header into `docs/system-md-contract.md`. |
| header | Replace any "§N–§M" references inside contract text with section names. Do NOT renumber sections. |
| header | Add `contract: v4`. |
| structure | Gotchas section header gains "(ledger — evict when the cause becomes enforced)". Existing entries untouched. |
| structure | Deferred section header gains the trigger rule and the ≤7 / `docs/deferred.md` overflow rule. Existing items untouched; items lacking a "do when" trigger are reported (grooming). |
| structure | Invariants without an `inv-<slug>` id: report as (grooming) — assigning ids and enforcement points requires reading code and is a human-reviewed change. |
| artifact | Create `docs/system-md-contract.md` from `contract-rationale.md` if absent. |
| artifact | Large level: create `.system_md_enforcement.json` skeleton from any existing `{#inv-...}` ids found, with `path`/`symbol` left as TODO(verify) unless the invariant text names them explicitly. |
| gate | Regenerate `scripts/check_system_md.py` from the v4 template. Carry over CAP_LINES, LEVEL, SYSTEM_MD path, sidecar paths. Add WARN_AT=0.90. Run it; report results. |
| shim | Ensure root `CLAUDE.md` and `AGENTS.md` shims exist; create if absent; leave subdirectory framework-owned files alone. |
| (grooming) | Sections over budget, items without triggers, shipped items in deferred, extraction candidates — listed for the human, never auto-applied. |

## v4 → v5

| Class | Delta |
|---|---|
| header | Rule 5 wording: cap in bytes; gate writes the stamp. Replace the hand-maintained "Last revision" line with the gate-written form. `contract: v5`. |
| structure | Insert the routing table under the TOC, derived from the sections present (grooming item if a human should tune the rows). |
| structure | Design-decision record: if present and lineage-only, report as (grooming): "add one line per owner decision with the superseded alternative". Never invent decisions. |
| gate | Regenerate from the v5 template: byte cap (convert the existing line cap at the file's current bytes-per-line ratio, round up, record the conversion as the `--reason`), long-line WARN, escalating extraction FAIL, unpinned-id WARN, `--stamp`. Carry LEVEL and paths. Run; report. |
| (grooming) | Any extraction candidate the new gate names; any invariant id with no pin; lines over 160 chars outside tables. |

## v5 → v6 (reserved)

Add rows here when the contract changes. Keep deltas content-preserving.
