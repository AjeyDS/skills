# Model refresh (optional)

Model lineups now turn over every few weeks, and a lane can switch models
the day one ships. This is an optional pass that finds out what is new and
what the evidence says about it, including models released hours ago. Run
it when the user asks ("refresh the models", "is there a newer Grok", "what
just came out"), or offer it when:

- a model name comes up that the capability notes don't cover,
- a CLI's model list shows a slug the notes don't cover (step 1),
- the notes are more than about a month old and the handoff matters.

## 1. Start with what the user can actually run

Local model catalogs show new models before most web coverage does, and
they say what is selectable on this account:

| CLI | Command | Notes |
|---|---|---|
| Codex | `codex debug models` | JSON list; `slug`, `display_name`, `supported_reasoning_levels`, `context_window`, `visibility` (verified on codex-cli 0.159) |
| Cursor | `cursor-agent models` (or `--list-models`) | One `id - Display Name` per line, effort and `-fast` variants as separate ids (verified on 2026.10.12) |
| Gemini / Antigravity | check `--help` for a models command | Otherwise the vendor's model docs page |

Diff the slugs against the user's setup file and the capability notes. Every
new slug, and every model the user names, becomes a refresh target. A model
in the news that no CLI lists yet is worth noting but can't be delegated to.

## 2. Search, one target at a time, in parallel

If the agent can spawn subagents, give each target to a cheap one with web
search and launch them together; the main model weighs the results. Give
each scout today's date, a budget of about five searches or fetches, and
this return shape:

```
Model: <exact name and API slug>
Released: <date, with source>  Status: announced | GA | preview | rumor
Where: <which of the user's CLIs/plans expose it, if stated>
Benchmarks: <name, version, score, effort/harness, source, vendor-reported or independent>
Pricing / tokens: <per-token price, and output-token use vs predecessor if reported>
Known issues: <early complaints, regressions, safety or monitorability notes>
Not found: <what you looked for and didn't find>
```

### Where the numbers show up, fastest first

- **Within hours (vendor-reported):** the launch post, model card or system
  card, API changelog and pricing page, CLI release notes (e.g. the
  `openai/codex` GitHub releases, Cursor's changelog), and the vendor's
  own social posts. Launch tables often mix harnesses and effort levels;
  record them as claims.
- **Hours to days (independent, early):** Artificial Analysis
  (artificialanalysis.ai: Intelligence Index, per-eval scores, cost to run,
  output tokens), OpenRouter (availability, pricing, context), LMArena
  (needs days of votes before a rank settles).
- **Days to weeks (independent, agentic coding):** Terminal-Bench
  (tbench.ai), SWE-bench Verified / Pro (swebench.com, Scale's SEAL
  boards), Vals.ai, METR time-horizon reports, ARC Prize.
- **Be wary of first-party benchmarks** published by a tool that sells the
  model (e.g. CursorBench for Cursor's own lineup).

### Finding a model released a few hours ago

- Search the exact name in quotes with "announcing", "release" or
  "launch" and today's date, and use a news or past-24-hours filter when
  the search tool has one. General web indexes lag by hours to a day.
- Fetch the vendor pages directly (newsroom/blog, docs changelog, models
  page, pricing page, GitHub releases). They update before search results.
- Developer chatter (Hacker News, X, Reddit) often has the first hands-on
  impressions and the first bug reports. Treat these as anecdotes.
- No results in the first day doesn't mean the model doesn't exist. If
  the vendor's own pages show nothing either, record it as
  "user-reported, unconfirmed" and move on.
- Keep leaks and rumored names apart from announcements.

## 3. Weigh and record

- Compare scores only within the same benchmark **version**, harness and
  effort level. Indexes like Artificial Analysis's rescale between
  versions, so a cross-version comparison misleads.
- Note the output-token count and cost per task, not only the score. A
  model that spends 2–3x the tokens of its predecessor can cost more per
  task at the same per-token price.
- **A new model doesn't inherit its predecessor's track record**, even
  within one family. Until it has real delegation rounds, its profile is
  benchmark-derived only: start it on full review regardless of how
  strong the numbers look.
- Add a dated entry to the capability notes with a confidence label:
  `vendor claims only` → `independent, early` → `independent, settled` →
  `own rounds`. Update the label when the numbers firm up or rounds
  accumulate.
- If the model changes what the user would pick for a lane, say so and
  suggest a small pilot slice.

## What to tell the user

A short table, newest first, then one or two lines of what changed:

| Model | Available in | Released | Key numbers (source, version) | Confidence | Starting review tier |
|---|---|---|---|---|---|
