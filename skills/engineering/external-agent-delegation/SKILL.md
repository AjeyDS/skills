---
name: external-agent-delegation
description: Delegate repo work to parallel external coding agents (Codex CLI, Cursor CLI, Gemini or Antigravity CLI, or others) and calibrate how hard to review what they return. Use whenever the user says an external agent can pitch in, hands off a doc/task to one, reports a branch landed from one, asks whether an agent can handle a task, or wants to split a task across several agents. Also use when the main agent calls Codex or Cursor mid-session (codex exec / codex review, the Cursor plugin's cursor-rescue agent or /cursor:* commands, cursor-agent) for exploration, review, a second opinion, diagnosis or a bounded implementation slice ("ask codex", "have cursor review this"); when the user wants to refresh model knowledge or asks what coding model just came out ("refresh the models", "is there a newer Grok"); and to pick a review depth matched to the specific model that did the work instead of a blanket full re-check.
license: MIT
compatibility: For sessions that run other coding-agent CLIs (Codex CLI, Cursor CLI, Gemini or Antigravity CLI) in parallel or call them in-session. The model notes in references/ are dated field notes; replace them with your own.
metadata:
  author: AjeyDS
  version: '1.0'
---

# External Agent Delegation

The user delegates repo work to parallel external coding agents outside the
main session. Typical ones:

- **Codex CLI** (OpenAI): branches usually land as `codex/*`. Several
  selectable models; the one that ran matters more than the wrapper.
- **Antigravity CLI** (`agy`, Google's successor to Gemini CLI) or **Gemini
  CLI**: branch prefix varies, confirm if unclear.
- **Cursor CLI** (`agent` / `cursor-agent` binary): fronts many model
  families, so always confirm which model and effort level ran.

**Per-user setup lives in `references/your-setup.local.md`** (private;
create it from the template `references/your-setup.md`): which agents the
user runs, their nicknames for them, which models they use through which
tool, and branch prefixes. Read it first. If only the blank template
exists, ask the user the few questions it lists and offer to write the
`.local` copy.

Treat any "external agent" or named tool (codex, gemini, agy, cursor, a
model name, or a nickname from the setup file) doing concurrent repo work
as this pattern, even if unlisted.

## In-session channels: the main agent calls another agent directly

Codex and Cursor can also be called **from inside the main session** and
used like subagents. The main agent sends a prompt, gets the answer in the
same turn, and there's no handoff doc or branch. This suits exploration,
review, second opinions, diagnosis, and bounded implementation slices. The
handoff/branch pattern below is still the better fit for long jobs.

- **Codex via `codex exec` in Bash.** There is no Codex MCP server any
  more: `codex mcp-server` was removed in 0.154.0. Run
  `codex exec -s read-only|workspace-write -o <file> --json "<prompt>" </dev/null`.
  Always redirect stdin, or exec can wait on it. The `thread_id` from the
  first JSON event feeds `codex exec resume <id> "<follow-up>"` for
  multi-turn.
- **Cursor via its Claude Code plugin.** The plugin's `cursor:cursor-rescue`
  agent / `/cursor:task` are callable by the main agent, but they default to
  Cursor's own Composer model, so **pass `--model <name>`** when you want a
  specific model. The plugin takes the bare model name (no effort suffix).
  They are write-capable unless `--propose-only` is passed and have no
  resume. `/cursor:review` and `/cursor:adversarial-review` are locked to
  Auto model selection.
- **Raw CLIs through Bash** fill the gaps: `codex exec`, `codex review`, and
  `cursor-agent -p --mode ask|plan --model <model-with-effort>` give a
  chosen effort level, read-only runs, `--resume`, and worktrees.

The model that actually ran decides which capability profile applies, and
the defaults are often not the model you'd assume. Parameters, a
job→channel map, and verified quirks are in
`references/in-session-channels.md`.

## Companion skill

`goal-anchored-delegation` layers on top of this one: it adds a Goal Card
(the user's goal + decision principles) to every handoff, grades executor
autonomy by capability parity, and defines the escalation/goal-critique
loop. Use it whenever writing a handoff doc or when planner and executor
are different models.

## Shared methodology layer (e.g. Superpowers)

If the external agents run a methodology skill pack such as
[Superpowers](https://github.com/obra/superpowers), skills like
`test-driven-development`, `systematic-debugging`, and
`verification-before-completion` self-activate on matching tasks, so an
agent running under it does part of the review job before the branch
lands. That is a calibration signal *additive* to the model-capability
profile:

- **Evidence the relevant skill actually ran** (red-green-refactor commit
  pattern, explicit verification step) → supports a lighter review tier.
  Check the branch history; don't assume it fired just because installed.
- **Should have fired but didn't** (no tests, no verification, work just
  declared done) → stronger flag than normal; lean toward full adversarial
  review, and log the recurrence in the capability notes.
- Unsure whether it's active for a given agent/session → ask the user;
  installs drift out of sync.

## When this triggers

- "[agent] can pitch in", "give [agent] a doc/task"
- "divide/split this across [agents]": multi-agent split setup
- A branch from an external agent landed and needs review
- "is [agent] capable of X", "can I trust [agent] with this"

## The core workflow (agent-agnostic)

1. **Handoff docs live in `docs/plans/`**, committed to the base branch
   before the agent starts, named
   `YYYY-MM-DD-<short-task-slug>-<agent>-<model>.md`. Date+task+agent+model
   makes parallel handoffs unambiguous and traceable to a
   capability-profile entry. Include a Goal Card
   (see `goal-anchored-delegation`).
2. **The external agent never merges.** It pushes its branch; merging is a
   human/main-session decision after review.
3. **Every landed branch gets a review before merge**, with depth calibrated
   (below), not maximal by default.
4. **The shared ground truth doc** (SYSTEM.md/CLAUDE.md/AGENTS.md) is what
   both sides read first and update after; point the agent at it in the
   handoff doc.

## Splitting across multiple agents at once

Trigger: the user names more than one available agent ("divide this
between codex and gemini", "use whichever models are available").

1. **Confirm which agent+model combos are in play**, and the effort level
   where the model has one. "All the listed" means every combo in the
   user's setup file; ask which model per agent if unstated. Consider cheap
   tiers deliberately, not as a fallback: "the small model does the
   high-volume narrow pass, a frontier model finishes" often beats routing
   everything to the priciest tier.
2. **One handoff file per agent+model**: a combined doc invites scope
   collisions and muddies ownership.
3. **Divide along a real seam**, informed by the capability notes: a
   task-shape split matching each model's strong zone, and non-overlapping
   file/module boundaries. If it doesn't split cleanly, say so and propose
   the single best-fit agent instead.
4. **Standard structure per file** (task, scope boundaries, Goal Card,
   ground-truth pointer, explicit "don't touch X, other agent's file")
   plus the target model, for future capability lookups.
5. **Produce a ready-to-paste kickoff message per agent**: handoff file
   path, one-line task summary, scope boundary, ground-truth pointer,
   autonomy grade, labeled by agent/model.
6. **State the split and reasoning to the user**: which agent got what
   and why, as a visible decision.

## Calibrating review depth: the actual hard part

The failure mode being fixed: defaulting to full re-verification of every
delegated task, which erases delegation's savings. **Key the review tier
off the specific model that did the work**: "Codex"/"Cursor" are wrappers;
capability depends on the underlying model, which changes over time.

1. **Identify the model, not just the agent** (ask, or check
   session/branch metadata). Unknown → treat as low-confidence.
2. **Look up its profile** in the capability notes: strong zones,
   weak/untested zones, and the comparison against the main agent's model.
3. **Pick a tier:**
   - **Strong zone** → light-touch: diff scan for scope creep, run tests,
     skim. No adversarial pass.
   - **Weak/untested zone or unknown model** → full adversarial review
     (a strong model finds issues, a cheaper one verifies each finding).
   - **High-stakes regardless** (security, data migration, money/auth/prod
     config) → full adversarial review, no strong-zone shortcut.
   - **Methodology-pack adjustment**: evidence a skill engaged nudges
     lighter; evidence it should have but didn't nudges fuller.
   - **Models with reduced reasoning-trace monitorability** change the
     review *kind*, not just the depth: audit the diff and tool results
     rather than the reasoning transcript, and give dependency, lockfile,
     CI-config or install-script changes a full pass regardless of tier.
   - **Unlogged deviations from the handoff plan** → full review
     regardless of tier (see `goal-anchored-delegation`).
4. **Log surprises into the capability notes.** Strong-zone task came back
   wrong, or weak-zone came back clean → the profile is stale; update it
   rather than reverting to distrust-everything.

## Assessing "can this agent handle this" before a new handoff

1. Check the capability notes against the task's shape (long-horizon vs
   single-file, novel vs well-trodden, broad context vs narrow scope).
2. Weak or unknown zone → say so plainly and suggest a small pilot slice
   before full delegation.
3. Capability claims are time-sensitive: these products swap default
   models every few weeks. If the notes are more than about a month old,
   say so and offer a model refresh (below) before a consequential handoff.
   Also check the benchmark index version before comparing any two scores:
   indexes like Artificial Analysis's rescale between versions, so a
   cross-version comparison is worse than no comparison.

## Refreshing model knowledge (optional)

When the user asks what's new, names a model the notes don't cover, or a
CLI's model list shows an unknown slug, a refresh pass can fill the gap,
even for a model released a few hours ago. Start from the CLIs' own model
catalogs (`codex debug models`, `cursor-agent models`) to see what is
actually selectable. Then search each new model in parallel (cheap
web-search subagents if available): vendor launch posts and changelogs
first, then independent boards as they catch up. Record the result as a
dated, confidence-labelled entry in the capability notes. A new model
starts on full review until it has its own rounds, however good its
launch numbers look. Sources, search tactics for same-day releases, and
the comparison rules are in `references/model-refresh.md`.

## Reference files

- `references/your-setup.local.md` (template: `your-setup.md`): the user's
  agents, nicknames, model rules and branch prefixes.
- `references/in-session-channels.md`: how to call Codex (`codex exec`,
  resume, review) and Cursor (plugin + `cursor-agent`) from inside the main
  session, with flags, defaults, and what only the user can invoke. Read it
  before the first in-session call in a session.
- `references/model-refresh.md`: the optional refresh pass: local model
  catalogs, where new-model benchmarks appear and how fast, finding
  same-day releases, and how to weigh and record what comes back.
- `references/field-notes.md`: the skill author's dated capability notes
  and correction log (Codex, Antigravity, Cursor with Grok, Claude
  baseline) from real delegation rounds in 2026. Useful as a worked example
  and a starting prior; your own record should replace it over time.
