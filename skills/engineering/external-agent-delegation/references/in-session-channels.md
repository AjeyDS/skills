# In-session channels: calling Codex and Cursor from the main session

Verified 2026-09-25 on the author's machine (Codex CLI 0.157.0, cursor-agent
2026.09.23, Cursor plugin `xmartlabs-cursor` 0.1.0). These channels are
separate from the handoff-doc/branch pattern in SKILL.md. Here the external
model works like a subagent: Claude sends a prompt, gets text back in the
same turn, and decides what to do with it.

**Examples use the author's rule: Cursor only for Grok models.** Every
Cursor call names its model explicitly, because neither the plugin's
default (Composer) nor Auto may be the model you meant. Swap in the models
from `your-setup.md`. In the author's setup other families go through their
own channels: GPT through Codex, and Claude natively.

## Quick map: what to reach for

| Job | Codex (GPT) | Cursor (examples use Grok) |
|---|---|---|
| Explore / answer a question about the repo (read-only) | `codex exec -s read-only` | `cursor-agent -p --mode ask --model grok-4.7-high` (Bash), or `/cursor:task --model grok-4.7 --propose-only` |
| Review the working tree or a branch | `codex review --uncommitted` / `--base <br>`, or `codex exec -s read-only` with a review prompt | raw `cursor-agent --mode ask --model grok-4.7-xhigh` with a review prompt. **Not** `/cursor:review`, which is locked to Auto |
| Second opinion on a diagnosis or a design | `codex exec`, then `codex exec resume <id>` to push back on the answer | `cursor-agent -p --mode plan --model grok-4.7-…` |
| Implement a bounded slice | `codex exec -s workspace-write` | `cursor:cursor-rescue` agent / `/cursor:task` **with `--model grok-4.7`** |
| Multi-turn back-and-forth | `codex exec resume <thread_id>` | raw CLI `--resume <chatId>` (the plugin has no resume) |
| Run in parallel with Claude's own work | `codex exec` via Bash `run_in_background` | `cursor:cursor-rescue` with `run_in_background`, or background Bash |

Outputs from these channels are claims, not facts. Review them with the same
model-calibrated tiers as a landed branch (SKILL.md, "Calibrating review
depth"). The capability profiles apply keyed on the **model that ran**, and
Grok 4.6 and Grok 4.7 have separate records.

## Codex via `codex exec` (Bash)

**There is no Codex MCP server any more.** `codex mcp-server` was deprecated
in 0.149.1 and removed in **0.154.0** (2026-09-09). On 0.154+,
`claude mcp add … codex mcp-server` fails to connect, and running it by hand
prints "stdin is not a terminal" because the word is parsed as a prompt.
`codex mcp` was never the server; it manages Codex's *own* MCP list. Other
Claude-side tools (trailofbits second-opinion, claude-delegator, quest)
moved to `codex exec` too. `app-server` speaks Codex's own JSON-RPC
protocol, not MCP.

**One-shot call** (verified on 0.157.0 with the config default, GPT-6 Astra;
a trivial prompt took about 8s):

```
codex exec -s read-only -C <dir> -o <answer.txt> --json "<prompt>" </dev/null > <events.jsonl>
```

- **Always redirect stdin (`</dev/null`).** exec prints "Reading additional
  input from stdin…" and would otherwise wait on an open stdin.
- `-s read-only | workspace-write | danger-full-access`: use read-only for
  exploration and review, workspace-write for implementation. Writes land
  directly in the working tree with no branch, so keep scope disjoint from
  Claude's files or use a worktree.
- `-m gpt-6.1-sol` needs Codex CLI ≥ 0.159 (`codex update`); older CLIs reject it.
- `-m <model>` overrides the config default (`gpt-6-astra`, effort `high`
  in `~/.codex/config.toml`). `-c model_reasoning_effort=low|…|max` sets
  the effort level.
- `-o <file>` writes only the final message, which is the clean thing to
  read back. `--json` streams events: the first line is
  `{"type":"thread.started","thread_id":"…"}`. Keep that ID for follow-ups.
- `--output-schema <file>` gives a structured final answer (e.g. review
  findings as JSON). Other useful flags: `--ephemeral` (no saved session),
  `--skip-git-repo-check` outside a git repo, `--add-dir <dir>` (extra
  writable root).

**Multi-turn:** `codex exec resume <thread_id> -o <file> "<follow-up>" </dev/null`
continues the thread with full context (verified: it recalled its previous
answer). `--last` resumes the most recent thread. `codex exec fork <id>`
branches a thread. Use resume to challenge a finding or ask for evidence
without re-sending context.

**Review:** `codex exec review` or `codex review` with
`--uncommitted | --base <branch> | --commit <sha>` and optional extra
instructions runs Codex's built-in review.

**Parallel:** run exec with Bash `run_in_background`, or from a background
`Agent`. Each run is its own process, so several can go at once if their
write scopes don't overlap.

## Cursor via the plugin (examples use Grok)

The plugin wraps `cursor-agent` over ACP through
`scripts/cursor-companion.mjs`. The readiness check is
`node <plugin>/scripts/cursor-companion.mjs setup`, where `<plugin>` is
`~/.claude/plugins/cache/xmartlabs-cursor/cursor/0.1.0`. On 2026-09-25 it
reported: auth ok, ready.

**Always pass `--model grok-4.7` (or `grok-4.6`).** Without it, `task` runs
**Composer**, Cursor's own model. The plugin resolves models by
their **ACP names**, which are bare family names with no effort suffix:
`grok-4.7`, `grok-4.6`, `grok-4.5`. The CLI IDs such as `grok-4.7-high` are
rejected: "model unavailable; have: Auto, grok-4.7, grok-4.6, …". The
plugin has no effort flag, so the effort it runs at is Cursor's default for
that model. When effort matters (the capability record's Grok 4.7 rounds
were xhigh), use the raw CLI below.

Verified 2026-09-25:
`cursor-companion.mjs task --model grok-4.7 --propose-only "…"` returned in
about 9s.

**What Claude can call vs. what the user must type:**
- `cursor:cursor-rescue` (Agent `subagent_type`) and `/cursor:task` are
  model-invocable. Flags: `--model <name>`, `--propose-only`, and
  `--background`/`--wait`, which are Claude-side and stripped before
  forwarding. The rescue agent's own instructions say "leave model unset
  unless the user asks". If the user's setup pins a model for Cursor, they
  have in effect always asked, so put `--model <name>` in the prompt passed
  to the agent.
- `/cursor:review` and `/cursor:adversarial-review` are **locked to Auto**
  (no `--model`), so they can't honor a model pin. Use a raw-CLI review
  instead. `/cursor:status`, `/cursor:result`, `/cursor:cancel` and
  `/cursor:setup` are user-typed only (`disable-model-invocation`).

**Other plugin behavior:**
- `task` is **write-capable by default** (ACP "agent" mode). With
  `--propose-only` it runs in "plan" mode, which is read-only.
- No resume: every `task` is a fresh session. Write each prompt
  self-contained (task, done-criteria, output shape, scope limits). The
  plugin's `composer-prompting` skill holds a prompt recipe; it is written
  for Composer but applies as well to Grok's one-shot runs.
- The opt-in stop-time review gate (`/cursor:setup --enable-review-gate`)
  runs the Auto-model review, which ignores any model pin. Leave it off.
- The plugin's result-handling rules say: present findings verbatim and
  **ask the user before fixing any of them**, and don't turn a failed
  rescue into a Claude-side implementation.

## Cursor via the raw CLI (`cursor-agent`): Grok with a chosen effort

This is the channel for Grok reviews, read-only Q&A, multi-turn work, and
any run where the effort level matters. Run it through Bash:

```
cursor-agent -p --trust --output-format text --mode ask --model grok-4.7-xhigh "<prompt>"
```

- `--mode ask` = read-only Q&A; `--mode plan` = read-only planning. Omit
  the mode to get agent mode, which is write-capable. `--force`/`--yolo`
  allows commands without asking
- `--output-format text|json|stream-json` (only with `-p`)
- `--resume [chatId]` / `--continue` give multi-turn, `-w [name]` runs in
  an isolated git worktree, `--worktree-base <branch>` picks the base
- Headless startup is about 15s before the model does anything (measured
  2026-09-25)

**Grok CLI IDs on 2026-09-25** (`cursor-agent --list-models | grep -i grok`):
- `grok-4.7-{low,medium,high,xhigh}` (4.7 has no `cursor-` prefix)
- `cursor-grok-4.6-{low,medium,xhigh}`, plus `cursor-grok-4.6-high`, whose
  display name is plain "Grok 4.6"
- `cursor-grok-4.5-*`
- each ID also has a `-fast` variant

Re-run the list before relying on it, because the prefix convention already
differs between 4.6 and 4.7.

## Picking a channel: rules of thumb, not a procedure

- **Cheap cross-model second opinion:** read-only Codex (GPT) or Cursor
  `ask` mode (Grok). A different model family catches different things,
  and nothing touches the tree.
- **Review with a known model:** `codex review`, or raw
  `cursor-agent --mode ask --model grok-4.7-xhigh` with a review prompt.
  The plugin's review commands are Auto-only and out of bounds.
- **Parallel implementation:** give each agent a disjoint file set, or a
  worktree (`cursor-agent -w`, or Codex `cwd` pointed at a worktree). Both
  channels write straight into the tree they're given.
- **Big or long-running jobs** still fit the handoff-doc/branch pattern
  better. That pattern gives a Goal Card, a reviewable branch, and a record
  in the capability log.
