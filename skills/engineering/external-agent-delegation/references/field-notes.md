# External Agent Capability Profiles: author's field notes

> These are the skill author's dated notes from real delegation rounds in 2026, on one
> person's setup (Codex for GPT models, Cursor used only for Grok, Antigravity for Gemini).
> Model names, benchmark scores and verdicts age fast. Treat this file as a worked example
> of how to keep a capability record and as a starting prior; keep your own record in
> the same shape and let it replace these entries. "Project M" is the author's app
> where most rounds ran.

Covers four agents: Codex CLI (GPT-6 Astra, GPT-6.1 Sol, GPT-6 Luna,
GPT-5.6 Sol/Terra/Luna), Antigravity CLI (Gemini 3.8 Flash, Gemini 4 Argon,
and the retired 3.7 Flash record), Cursor CLI (Grok 4.6 and 4.7), and the
Claude baseline they're measured against (Fable 5.1, Opus/Sonnet/Haiku 5.5).

Last researched: **2026-10-19 (model refresh: GPT-6 Luna, GPT-Reserve, Gemini 3.8 Flash, Gemini 4 Argon, Claude 5.5 family, other Cursor-listed models; Gemini 3.7 Flash found deprecated)** / **2026-10-05 (GPT-6.1 Sol Project M phase 3 round added)** / **2026-10-01 (GPT-6.1 Sol M3a round added to the Codex correction log)** / **2026-09-21 (Grok 4.7 added to the Cursor section on its
release day — partial data, re-check within a week)** / **2026-09-20 (GPT-6
Astra added to the Codex section;
Claude Fable 5.1 added to the Claude baseline; AA Intelligence Index
overhauled twice — see correction log)** / 2026-08-14 (Grok 4.6, Gemini 3.7
Flash) / 2026-08-05 (Codex Luna tier) / 2026-07-25 (Antigravity, Cursor,
Claude sections). These products swap default models often — treat anything
here as provisional and re-check via web search before a high-stakes
handoff if it's been more than ~2 months, or if the user mentions a
model/version name not listed here. The last four model generations arrived
roughly five, three, three and two weeks after their predecessors, so
"2 months" is the outer bound, not a comfortable margin.

**Benchmark-version warning — now the single biggest trap in this file.**
Artificial Analysis shipped v4.2, v4.3 and v4.3.2 of the Intelligence Index
between 2026-08-14 and 2026-09-20, and the v4.3 line **replaced two of the
benchmarks this file quotes most** (Terminal-Bench 2.1 → 4.0, τ³-Banking →
AutomationBench-AA) while dropping the saturated GPQA Diamond. The scale
moved with it: Claude Fable 5.1 reads **66** on the index version live at
its own launch and **53** on current v4.3.2 — same model, same effort
setting, different index. **Do not compare any score written in this file
before 2026-09-20 against one written after it**; check the version tag on
both first. The same caution applies to the underlying benchmarks:
Terminal-Bench "2.1" vs "4.0" and GDPval-AA "v2" vs "v2.1" are different
tests, not revisions of one number.

**Correction log (newest first):**

**2026-10-19 — model refresh (CLI catalog diff + six Haiku-tier web scouts). Benchmark research only; no delegation rounds.**
- Started from `codex debug models` (codex-cli 0.159.3) and `cursor-agent models` (2026.10.12). Slugs not covered here: `gpt-6-luna`, `gpt-reserve` (hidden), `gemini-3.8-flash`, `gemini-4-argon`, the Claude 5.5 family (thin), and out-of-lane `kimi-k3`, `kimi-k2.7-code`, `glm-5.2`, `muse-spark-1.3`, `muse-wonder-1.0`.
- **Lane-changing finding: Gemini 3.7 Flash was deprecated 2026-10-08 and its requests now route to Gemini 3.8 Flash** (Gemini API changelog). The Antigravity light-touch tier was earned on 3.7 Flash and does not transfer: treat any Antigravity Flash lane as 3.8 Flash on full review until it has its own rounds.
- `gpt-reserve` is not a model. It is the ID behind "Luna Reserve", a post-quota fallback (GPT-5.6 Luna usage) on selected personal Plus/Pro accounts. Nothing to profile.
- No Grok newer than 4.7 on x.ai/news through 2026-10-19. Codex CLI 0.163.0 shipped 2026-10-15 (local is 0.159.3); 0.161.0 reportedly made GPT-6.1 Sol the default.
- AA versions confirmed the same day by fetching each AA model page directly: Gemini 4 Argon 53 (high), Claude Sonnet 5.5 56 (max), Claude Haiku 5.5 43 (max; a scout had reported "default"), all **v4.3.2**, so they sit on the same scale as the current-generation table. **Sonnet 5.5's 56 is the highest v4.3.2 composite in this file**, above Fable 5.1 and Astra (53). Sonnet's AA Coding Agent Index 68 is not shown on its AA page and stays unconfirmed.

**2026-10-10 — GPT-6.1 Sol, Project M desktop branch 0 "trim" (Tasks 1-9 of 16, xhigh, in-session `codex exec`; Opus 5.5 reviewer per task in a scratch worktree): strong at subtraction, two judgment slips, limit hit mid-task.**
- Clean red/green on every TDD step; stopped correctly on `quick_tailor.DEFAULTS` (audit was wrong, tests use it). Golden-file discipline on the python-docx → stdlib rewrite caught its own first draft.
- **Slips:** rewrote the literal names in the PLAN/DESIGN text so a grep gate came back clean (gaming the check — reverted; tell it "plans are records, never edit task text"); implemented the plan's import-guard split exactly as written, which narrowed exception handling (my plan bug, but it didn't flag it).
- Reviewer-only finds again edge-of-spec: .docx main part via _rels (renamed parts, ./ and ../ targets), malformed vMerge → 500, mount-less Docker boot (root-owned /app after dropping chown -R).
- Hit the Codex usage limit after ~9 xhigh tasks + 3 resumes in one night; Sonnet 5.5 finished Tasks 10-16 cleanly (and caught a real plan bug: Monaco worker stubs are AMD deps of editor.main).
- Calibration unchanged: light-touch for backend; keep full review on deps/Docker/lockfile and anything with a grep-based gate.

**2026-10-05 — GPT-6.1 Sol, Project M phase 3 agent dashboard (13 tasks, xhigh, in-session `codex exec`; Opus 5.5 reviewer per task in a scratch worktree, browser checks for UI): strong backend, good judgment at stop points, UI needed the browser reviewer.**
- **Stopped correctly twice with evidence and a prepared patch:** FastMCP TypedDict validation silently dropping unknown keys (a real plan defect), and a conflict between the plan's cached-query guard and my imprecise instruction. Both were right calls.
- **Backend reviewer finds (all edge-of-spec, fixed in short resumes):** prune deleting the just-written row under clock skew, duplicate job ids kept, lax int coercion, a batch-level read outside the per-row try, an ambiguous prompt sentence an agent could misread.
- **UI finds only a browser showed:** a remount counted as a new visit (wiping New markers), a tile jumping to a collapsed section, a sticky toolbar hiding the jump target, filter chips disagreeing with a relabel.
- **One pin miss:** it replaced two plan-pinned tests with its own instead of adding beside them. Tell it "add, never replace, plan pins".
- **Workflow that worked:** pipeline review(n) in a detached scratch worktree while Sol does task n+1; follow-ups via `codex exec resume <thread>`; Turbopack refuses a symlinked node_modules in the scratch tree (`next dev --webpack`). No usage-limit hit across ~20 runs.
- Calibration: light-touch holds for backend tasks; UI tasks keep the browser reviewer.
- **Review-copy blind spot:** symlinking the main worktree's frontend/node_modules into reviewer scratch trees hid a test that required the npm `typescript` package; it failed only after merge, in the main checkout and CI's backend job (no npm ci). Run the final suite once in an environment without node_modules (the owner's main checkout) before calling a merge done.

**2026-10-02 — GPT-6.1 Sol, KB Core M3b (Tasks 1–10, React app + uploads + packaging, xhigh): backend strong; browser work needs a reviewer in the loop.**
- **Backend tasks were clean.** API guards, Docling conversion, jobs, setup and packaging each came back with real-data measurements and careful supply-chain notes. Sol stopped correctly at stop points (existing-test edits, sdist builds) with prepared patches.
- **Browser work never passes on the first try.** Without Chrome, every UI task's Playwright specs failed on first reviewer run. The causes, in rough order of frequency:
  - same-document hash navigation skipping init scripts
  - viewport and scroll
  - invented data attributes
  - vitest mocks that didn't match real API shapes (omitted zero counts)
  - a legacy test server that didn't match production
  
  Expect 2–5 follow-ups per UI task.
- **Reviewer-only finds:** each needed a realistic run to show up.
  - status opened every KB (pool thrash past 8 KBs)
  - idle layout loops did a write transaction every 0.1 s
  - the evidence panel was wiped on any status event
  - the installed wheel failed on an un-migrated KB
  - agent sources were invisible in the app
- **Usage:** hit the Codex limit three times. One reset was 3 days out, and the owner reset it manually.
- **Calibration:** light-touch for backend tasks. For UI, the reviewer runs Chrome every time and debugs root causes directly, because remote round-trips without a browser converge slowly. Write the Playwright lessons into the next task's prompt; that cut the follow-ups.

**2026-10-01b — GPT-6.1 Sol, KB Core M3a (Tasks 1–10, xhigh, in-session,
backend-only): strong; the gaps it left were all cross-task or edge-of-spec.**
- All ten tasks had a clean red/green split, a byte-identical port of the
  plan's migration SQL, and real-copy measurements. It found and fixed real bugs
  the plan never mentioned: SELECT * breaking additive columns, a rejected query
  vector reaching sqlite-vec. In Task 10 it traced a packing regression to its
  cause (a ?kb= URL suffix eating the token budget) with a controlled
  diagnostic, instead of loosening the equality gate.
- **Gaps, all caught at review and fixed by Sol in short follow-ups:**
  - a status default that would have broken the viewer with two or more KBs
    (its test only covered the configured-default case)
  - provenance-weak evidence for context edges
  - evidence quotes that would straddle chunk boundaries for realistic input
    (its tests used deliberately short items)
  - migrate-v3 not taking the service lock
  - a stale e2e tool list it had flagged itself as out of scope
  
  Pattern: it satisfies the stated test cases precisely; **edge-of-spec
  realism and cross-task consequences are where the reviewer earns its keep.**
  Ask "what realistic input breaks this?" for every task.
- Usage: hit the Codex limit twice (after ~4 and ~6 xhigh tasks). It resumed
  cleanly after scheduled waits; partial work was never left inconsistent.
- Calibration: the light-touch tier holds for single-task correctness. Keep a
  diff read on anything touching evidence, defaults or lifecycle.

**2026-10-01 — GPT-6.1 Sol, full round (KB Core Tasks 5–12 incl. 4b/9–12; 8b
finished by Claude after Sol's Codex usage limit): strong, with one blind spot.**
- Every task came back with clean test/implementation separation, logged
  deviations and real-data measurements; red verified by the reviewer each time.
  Supply-chain (umap-learn + 92 npm packages), migration, data-correction and
  auth reviews all passed with nothing to revert.
- **Blind spot: it cannot see the UI.** Chrome won't launch in the Codex sandbox,
  so its browser tests were written but never run. Every browser-facing task
  (5, 8, 9, 11) needed reviewer fixes: wrong ports, order-dependent specs, a
  hops=0 assumption, and one real bug (login token left in the URL on a
  same-document hash change). It also skipped two explicit legibility
  requirements in Task 8 until a follow-up task restated them with a pixel gate.
  **Pair Sol with a reviewer who runs the browser, and give visual tasks a
  measurable gate.**
- Usage: hit the Codex limit after ~10 xhigh tasks in one evening; resumed
  cleanly after reset via a scheduled background wait.
- Calibration: light-touch for backend/data tasks in this lane is earned (two
  clean rounds); browser/visual tasks need the reviewer to execute them.

**2026-09-30b — GPT-6.1 Sol pilot (KB Core M1-close/M2 Tasks 1–4, xhigh,
in-session `codex exec` in a sandboxed worktree): clean, and better than the
plan.**
- Workflow: Codex's workspace-write sandbox forbids **all** git writes (it
  protects `.git` even via `--add-dir`, a worktree pointer, or a renamed
  `--separate-git-dir`). So Sol wrote code only; Claude committed each task
  as a red/green pair after stashing the implementation to prove red. One
  Sol run per task, `-o` final message + `--json` events, ~minutes each.
- Quality: 4/4 tasks with tests and implementation cleanly separated as
  instructed, every deviation logged, measurements on the real-data copy with
  checksums, no invented hashes, no out-of-scope edits, no real-KB access
  (verified blocked by the sandbox).
- **It found two plan defects with evidence** (traversal fanout crowds out
  typed relations; the MCP budget still drops hub relations) and raised them
  as an open question instead of improvising. That is exactly the
  peer/adapt-and-advise behaviour wanted.
- Weak spot: the packing rewrite left one function at cyclomatic complexity
  60 and made a viewer route ~5x slower without flagging the slowdown as a
  problem (it recorded the timings, though). Review for structural slop and
  performance regressions, not correctness.
- Calibration: light-touch for well-scoped implementation in this lane after
  this pilot; keep full passes for deps, migrations, auth.

**2026-09-30 — GPT-6.1 Sol added (Codex). Benchmark-derived only; first
delegated round starts today (KB Core M1 close-out + M2, pilot gate after
Task 4, effort `xhigh`).**
- Released 2026-09-29 at DevDay, one week after GPT-6 Sol (2026-09-22, never
  profiled here) and replacing it. Model string `gpt-6.1-sol`. **Needs Codex
  CLI ≥ 0.159** — 0.157 rejects it ("not supported when using Codex with a
  ChatGPT account", missing model metadata). `codex update` fixes it.
- AA Intelligence Index **v4.3.2** (same version as the Astra/Fable 5.1
  rows, so comparable): **52 at max vs Astra 53**, GPT-6 Sol 48. Coding Agent
  Index: 2 below Astra at max, **but xhigh scores 3 above its own max and 1
  above Astra** — so `xhigh`, not `max`, is the coding setting. Terminal-Bench
  4.0 +12 over GPT-6 Sol; GDPval-AA v2.1 +5; hallucination 60% → 54% (worse
  than Astra's 51%).
- Cost: $2/$10 per MTok, **$0.72 per index task at max vs Astra's $3.26**;
  10–30% more output tokens than GPT-6 Sol.
- **No safety/system-card data seen** (OpenAI's page 403'd to WebFetch).
  Until known, apply the Astra review procedure: audit diffs and tool results,
  full pass on dependencies, lockfiles, migrations and auth regardless of tier.
- Starting tier: unknown model → full review on the pilot; light-touch for
  well-scoped implementation only after a clean pilot.

**2026-09-25b: GPT-6 Astra (effort high) as an in-session plan reviewer: clean round.**
It gave a read-only second opinion (`codex exec -s read-only`) on a ~4,000-line, 29-task plan (Project M
Companion fill engine). It read the plan, design, research and code, and gave a hybrid verdict with a
10-task merge map. It found five concrete plan defects, all confirmed by Claude:
- a verify step before the final blur;
- a missing invalid-state check;
- partial success reported as verified;
- `Promise.race` that doesn't cancel the losing operation;
- an LLM fallback that skips confidence floors.

It took about 6 minutes and produced no hallucinated files. It's a good fit for plan and design critique.
Review its claims against the artifact, not its reasoning.

A follow-up in the same thread (`codex exec resume`) re-reviewed the rewritten plan. For each of its five earlier findings it checked whether the fix was real, citing line numbers: 2 fixed, 3 partly. It also ran the plan's loop code in memory to reproduce new defects. All eight defects Claude spot-checked were real, including:
- category recovery can't be reached after an honest abstain;
- an existing chip or an unchecked box counted as "already filled";
- cancel cleanup that wipes text inputs;
- controls inside `[role=dialog]` dropped from the field list.

Resuming the thread works well for review iterations.

**2026-09-25: in-session channels added, and two models reach Claude with no profile here.**
Codex (`codex exec`) and Cursor (plugin + `cursor-agent`) can now be called from inside a Claude session;
see `in-session-channels.md`. The author runs Cursor **only for Grok**. The plugin's `task`
silently defaults to Composer 2.5 and its reviews are locked to Auto, so a plugin run without
`--model grok-4.x` is out of policy. Don't apply the Grok record to its output, and re-run it on
Grok. The plugin can't set effort (its bare `grok-4.7` runs at Cursor's default), while this
file's Grok 4.7 rounds were xhigh. Note the effort level when logging in-session Grok rounds.
Separately, GPT-6 Astra needs a recent Codex CLI: 0.144.4 got a 400 "requires a newer version",
and 0.157.0 runs it. A run on an old CLI that "used Astra" really used some other model, so check
the CLI version before applying the Astra profile.

**2026-09-22 — Grok 4.7 round 3, lane 1 (browser history guard): the pattern held, and hard
agentic state logic is a weak zone.** Task 1 (a link wrapper over 31 files, one unload listener)
was clean. Task 2 (Back/Forward guard over Next's App Router history) passed the lane's own
browser checks but two reviewers reproduced six history-corrupting paths it never forced (three
fast Backs, Back then Forward, a skip-link fragment pop, a save landing while asking, stale
duplicates, and the 50-entry session-history cap), and its pins only checked strings. Claude
rebuilt it as a pure node-tested state machine; even that rework needed a second review to find
the 50-entry cap. **Tier call:** for stateful browser/concurrency logic, don't take Grok 4.7's
green browser table as evidence; demand a pure model with exhaustive tests, and budget a second
adversarial pass.

**2026-09-22 — Grok 4.7 round 2 (Cursor): the other two lanes of the same
plan (analytics copy + backend `category_label`, Tasks 11–13; pages/forms,
Tasks 14–16), full review each.** Same shape as round 1, now 4-for-4:
- **Held up again:** honest self-reports (the one full-suite count and all
  browser claims reproduced), zero scope creep, every deviation logged, a
  correct call to update a prompt lock hash without inventing a migration,
  MCP/chat changes strictly additive and under the docstring budget.
- **Missed again, same pattern:** lane 3's CI pins let 11 of 18 reviewer
  mutants through, and its loading/failure path rendered "Ai Ml Engineer"
  (a regression from deleting a special-case map); lane 4's Task 16 was
  effectively unpinned and its new dialog both dropped typed text on close
  and allowed a duplicate create when closed mid-request. Its browser checks
  used thin fixtures (4 roles, empty tabs), so caps/tails never ran.
- **One wrong negative finding:** lane 4 reported a screen-reader-name gap
  that didn't exist (it read text nodes, not the accessible name).
- **Tier after 4 lanes:** keep FULL review for Grok 4.7 frontend work. The
  cheap high-yield review moves: mutation-check its pins, force every
  loading/error/pending path in the browser, and seed richer fixtures than
  it did.

**2026-09-22 — first Grok 4.7 round (Cursor, xhigh): two parallel lanes of
a frontend UX plan (Project M follow-ups, Tasks 4/8/9 and
5/6/7/10), full review each (adversarial code review + independent browser
pass + gate reproduction).**
- **Held up:** every self-reported gate AND browser claim reproduced
  (tests, tsc, lint, duplication counts, measured contrast ratios, pointer
  behaviour). Zero scope creep; file-ownership boundaries between parallel
  lanes respected; edits it couldn't make were listed file:line as
  "deferred". Every deviation logged with a reason, and plan defects flagged
  rather than pushed through (e.g. declined an edit that would have broken
  the duplication ceiling). No sign of the feared verbosity/scope creep.
- **Missed (each Important, caught only by the review):** lane 1 made a
  loading sentinel double as the error state, so a failed fetch read
  "Loading…" forever and locked controls, and its deviation log overstated
  what the fix covered; lane 2 wrote a pin that matched a function
  definition instead of its call site, so it couldn't catch the regression
  it claimed to guard, and a Suspense fallback briefly marked the wrong nav
  section. Pattern: implementation close to the spec, **tests weaker than
  claimed, and unhappy paths (error, fallback) under-examined.**
- **Cursor adds its own `Co-authored-by: Cursor` trailer** after the one the
  handoff asks for.
- Tier call after round 1: keep FULL review (both lanes had an Important
  finding), but the gate/browser self-reports can be trusted as a floor.
  Point reviewers at pin strength (mutation-check) and error/fallback states.

**2026-09-21 — Grok 4.7 added to the Cursor section on its release day.
Benchmark research only, hours after launch.** AA Intelligence Index 46 on
v4.3.2 (Grok 4.6: 44; Fable 5.1 and Astra: 53; Sol: 47), ~2.5x the output
tokens of 4.6 at the same per-token price, and a large Terminal-Bench 4.0
gap to the frontier pair. **The Grok 4.6 10-for-10 record in this log
belongs to 4.6** — a Cursor lane that has moved to 4.7 does not inherit it.
Most per-benchmark numbers are xAI's own; AA's per-eval breakdown, cost per
task and hallucination figures were not yet published.

**2026-09-21 — second Astra round (Codex CLI, effort `high`/`xhigh`): Tasks
4–11 of the same plan, eight tasks in one run, clean until the usage limit.**
- **Outcome:** Tasks 4–10 landed with the same red-then-green commit pattern
  and per-task deviation entries; Task 11 reached GREEN (full suite passing in
  the working tree) but the run hit its usage limit before lint, verification
  and the checkpoint commit. Finished by the in-session Claude: six Ruff
  import-order fixes, formatting, one test warning, then commit. No logic
  changes were needed.
- **Full-tier items held:** model download code restricted to two pinned repos
  with weights-only file patterns; auth middleware does exact Host/Origin
  checks and bounds body size; `.npmrc ignore-scripts=true` added unprompted;
  every added Python and npm dependency was one the plan named; all 84→143
  locked packages from pypi.org. Nothing to revert.
- **Behaviours worth knowing:** it self-spawns "independent adversarial"
  test files per task (useful, keep); it left `npm` cache logs in the tree
  (harmless, now ignored); one Task 9 manual smoke (Embedding Atlas browser
  startup) was honestly reported as unverified rather than claimed.
- **Calibration:** second clean round. Light-touch for well-scoped
  implementation in this lane is now earned, not just suggested. Plan for the
  usage limit: ~8 plan tasks of this size per run; put a "commit before
  verification if low on budget" instruction in future handoffs so a limit
  hit leaves a committed GREEN rather than a dirty tree.

**2026-09-20c — first delegated round on GPT-6 Astra (Codex CLI, effort
`high`): strong-zone result confirmed, review procedure held.**
- **Task shape:** greenfield scaffold inside a fully specified plan — SQLite
  storage with vec0/FTS5, strict Pydantic wire contracts, additive ontology
  merge, one async transaction boundary. 3 plan tasks, 28 files, ~1,250 src
  LOC + ~880 test LOC, 56 tests, 8 commits. Repo: KB Core (`RAG mcp`).
- **What was audited (diff and tool results, not the transcript):** every
  source file; `pyproject.toml` and `uv.lock` line by line; transitive
  provenance via `tomllib` (all 84 packages from pypi.org, no git/url/path
  sources, every unfamiliar name traced to fastmcp-slim/mcp/fastapi upstream,
  direct deps exactly the six the plan named plus the three dev tools); the
  slop scan (no orphans beyond an expected test-only migrations module, no
  clones, one cc=20 function); the suite re-run locally (56 passed, Ruff
  clean, `git diff --check` clean).
- **Superpowers evidence: present.** A `test:` commit precedes each `feat:`
  checkpoint, and the self-found shutdown race has its own red commit before
  the fix. That is the pattern the file says to look for, and it was there.
- **Deviation logging: 11 entries, all legitimate, one gap.** The gap was two
  enum values added to a wire contract (`ranking="discovery"`,
  `empty_reason="no_evidence"`) that were sensible but unlogged. Adjudicated
  into the design rather than reverted; the handoff rule was tightened to
  "every contract field or enum value is a logged deviation".
- **Async-questions behaviour showed up as designed:** two well-formed open
  questions (staging-embedding persistence, packaging) with work continuing
  on non-dependent tasks. The Goal Card + decision-principles block did its
  job; both questions were real plan gaps, not model confusion.
- **Self-review was real:** a fresh-context Astra pass found a genuine
  queued-reader shutdown race and fixed it with regressions. Not a
  cosmetic finding.
- **Calibration:** supports the suggested light-touch tier for well-scoped
  implementation in this lane. Dependency, auth and external-tool tasks keep
  the full pass per the standing Astra rule — that rule cost nothing here
  because the lockfile was clean, which is the point.

**2026-09-20b — two model additions (GPT-6 Astra, Claude Fable 5.1) and an
Intelligence Index overhaul. Benchmark research only — neither model has a
delegated round behind it here.**
- **GPT-6 Astra** (OpenAI, released 2026-09-09; in Codex CLI from
  2026-09-03 via a Trusted Access Programme with staged GA) joins the Codex
  section as `gpt-6-astra`. Sol, Terra and Luna are **not** retired, so "a
  Codex branch" is now four-ways ambiguous, and Astra's five reasoning-effort
  levels make it five-ways within that.
- **Claude Fable 5.1** (Anthropic, released 2026-09-01) joins the Claude
  baseline and currently ties for first on the AA Intelligence Index.
  **Claude Mythos 5.1 is the same underlying model with reduced safeguards**,
  gated behind vetted-access programs — if a branch claims Mythos, the
  capability picture is identical and only the access story differs.
- **The AA Intelligence Index is now v4.3.2**, aggregating ten evaluations:
  AA-Briefcase v1.1, GDPval-AA v2.1, AutomationBench-AA, Terminal-Bench 4.0,
  SciCode, Humanity's Last Exam, GDP.pdf, CritPt, AA-Omniscience and
  AA-LCR v1.1, with private-task weighting raised to 45%. **Every
  Intelligence Index number written in this file before today is on a
  retired version.** The v4.1.1 board (Opus 5 63 / Fable 5 62 / Sol 61 /
  Grok 4.6 61 / Gemini 3.7 Flash 56) cannot be read against the v4.3.2
  board (Fable 5.1 53 / Astra 53 / GPT-5.6 Sol 47). Rough ordering
  survives; the gaps do not.
- **Calibration note for both new entries:** they are benchmark-derived
  only. The tiers suggested below are starting points, not earned trust —
  log the first two or three outcomes aggressively, the way the Grok 4.6
  profile was built from 2026-08-14 onward.

**2026-09-20 — Grok 4.6 (Cursor), now 10-for-10 — engines branch tail
(Project M desktop step 2, Tasks 8–11: setup/status engines block, MCP
docstrings, frontend badges + checklist row + render_note toasts, user
docs):** four exact-scope commits, every number reproduced by the reviewer
(4364/2, 312, docstring budget 1939/2000, tsc/lint/build), three reviewer
mutations killed, seven deviations all logged and all adjudicated accept.
Two of them were PLAN DEFECTS it found: the handoff's `"TeX" in __doc__`
assertion was satisfied by "LaTeX" with no work done (it asserted `"no TeX"`
instead), and the plan's claim that the setup pill strip "lists only
unfinished steps" was false of the repo (it left the strip alone — out of its
file list — and objected, which was the right call). Light-tier findings
only: one test function spliced into another (names lied, assertions held)
and a badge inlined twice (extracted to a component). Two standing
merge-step duties reconfirmed: the reviewer subagent's Bash was pinned to
its own worktree and could not commit on the Cursor branch (it delivered a
patch; apply it yourself), and the browser pass stays the planner's. Also
worth knowing: Superpowers IS installed on this machine's Cursor CLI (owner
confirmed 2026-09-20). Light tier for frontend-surface / docstring / docs
lanes stands; it has not yet been tried on a security seam here.

**2026-08-25b — Grok 4.6 (Cursor), now 9-for-9 — app-update round, and the
first round where full-adversarial paid off in its strong zone:** 8 plan
tasks (backend router TDD, Dockerfile/workflow tag-gating, 4 frontend
surfaces, a 385-line bash update script + CI jobs). Scope byte-clean, suite
and lint numbers reproduced exactly (its signature holds), 4 deviations all
sound — one an outright improvement (`ls-remote` over `fetch --tags` so
`--check` writes no local refs). But the data-safety full-adversarial pass
on the script found two real defects light-touch would have shipped: the
`main "$@"` tail was still exposed to the self-rewrite hazard the script
guarded everywhere else (bash re-reads the rewritten file after main
returns — fix is the one-line `main "$@"; exit $?` idiom), and `pg_dump`
without `--clean --if-exists` made its own printed restore command fail
into any populated database; plus an annotated-tag sha mislabel in
`--check` (compared HEAD to the un-peeled tag object). Calibration: KEEP
the no-shortcut rule for data-safety bash even inside its
terminal/agentic strong zone — subtle process-lifecycle semantics
(self-rewrite, restore idempotency, tag peeling) are exactly where a
9-for-9 record still leaks.

**2026-08-25 — Grok 4.6 (Cursor), now 8-for-8, first SOLO full-stack round
(health round 2):** migration + 2 tables + 3 endpoints + matcher + 4 new UI
surfaces off a 10-task handoff, in 2 combined commits + 7 logged deviations
(all sound — incl. correctly arguing health answers are NOT gap resolutions
and choosing alphanumeric lookarounds over \b for C++). Reviewer probes: 3
mutations all killed, alembic down/up clean, suite 3767 green reproduced.
Two calibration notes: (1) it cannot see the maintainer-only slop ratchet,
and this round its two new dialogs re-inlined a 409-catch helper 5× —
duplication +26 lines that the reviewer deduped in minutes; BUDGET a
dedup-scan of NEW components into the merge step, same as the ratchet.
(2) Its sandbox could not reach localhost for browser E2E and left three
orphaned dev-server processes (one auto-respawning via an npm wrapper) —
it disclosed both honestly with exact ports; kill the process TREE, and
treat "browser E2E not done" as a standing reviewer duty for Cursor lanes.

**2026-08-22c — GPT-5.6 Sol (Codex), MCP-audit backend lane, clean with a
textbook escalation:** 6 behavior fixes (render-error surfacing/tail
extraction, template-resolution echo, KB pagination + duplicate hints,
prompt line) + a conditional prompt-resync migration. Its T6 STOP was the
round's highlight: a prompt-file edit tripped the prompt-defaults hash
guard, and instead of weakening the guard it escalated with the exact
tradeoff and the correct fix (fence exception for migrations/**), citing
why the alternative silently breaks existing installs. Migration itself
was conservative (byte-exact guard, re-check-in-WHERE, honest no-op
downgrade, tests incl. interleaving). Reviewer probes: 2 independent
mutations both killed; full suite re-run green; fence byte-verified
(granted exception only). Zero defects found. One process note: its
"delegated full-suite session was inconclusive" mid-round — it disclosed
this and re-ran, but keep re-running the suite reviewer-side. Light tier
for well-scoped backend implementation reconfirmed; the stop-behavior
streak is now the most reliable signal in its profile.

**2026-08-22b — Grok 4.6 (Cursor), now 7-for-7 — first docstring/API-surface
lane:** MCP-surface fixes (Project M: 5 docstrings compressed under a
2048-char client-truncation budget with a ratchet test, false docstring
claim corrected, ~14 pinned one-sentence fixes, payload-bounded page-image
tool, 5 new wrapper tools). All 10 commits exact-scope (byte-verified),
6 deviations logged incl. flagging a genuine PLAN DEFECT (the handoff's
version-tool `kind` vocabulary contradicted the REST router — it read the
router, adapted, and documented the trap in the docstring). Reviewer
probes: ratchet mutation killed, live rasterizer check passed, independent
budget re-measurement matched its table. Only findings: 3 copy-level nits
(one garbled Field sentence contradicting merge semantics, one
engine-scoped framing, one dropped constraint) — fixed by reviewer
post-merge in minutes. Light tier reconfirmed; its self-reported numbers
were independently reproducible, which continues to be its signature.
Ratchet note again: +4 hotspots, all growth (pin tests), re-baselined at
merge as budgeted.

**2026-08-22 — Grok 4.6 (Cursor), now 6-for-6, and its best disclosure yet:**
KB provenance + base→KB sync phases A+B (Project M: migration, provenance
stamping at ~8 sites, deterministic 3-tier sync service, 2 REST endpoints,
MCP tool, indicator UI) — 9 clean per-task commits, exact scope, worked in
its own worktree unprompted, returned checkout to main. Standout: its
deviation 5 flagged a genuine CONTRADICTION IN THE PLAN (reviewer's Task 3
regression spec defeated Task 5's drift-badge promise) and chose the
conservative side rather than silently resolving it — exactly the
adapt-and-advise behavior the autonomy grade wants; reviewer fixed the
reader post-merge. Also correctly attempted the live walk, got the
indicator verified, and honestly flagged the unfinished button press for
the reviewer (which then exposed only a verify-harness Origin-allowlist
gap, not an app defect). Review probes: migration down/up clean, 2
reviewer mutations killed. Light tier remains right; keep budgeting the
maintainer-only slop ratchet into the merge step (its lanes add hotspot
count the scanner can't attribute below top-50 — bisect before assuming
the lane's code is the offender).

**2026-08-21 — Grok 4.6 (Cursor), now 5-for-5:** quick-wins honesty-guards
lane (Project M: cover-letter output contract, dash scrub, low-sample
analytics flags, stale-doc closures) — clean scope (no forbidden files
touched, byte-verified), all 9 deviations logged with correct reasoning
(incl. discovering the plan's named frontend path was a 307 redirect and
logging the real chart locations into SYSTEM.md §12), ledger deletions done
in-place preserving frozen §11 numbering unprompted, 3 independent reviewer
mutation probes all killed by the intended tests, checkout returned to main
correctly this time. Zero defects found at light tier. One note for future
handoffs: it does not run the maintainer-only slop ratchet (correctly — it's
documented as not-contributor-tooling), so budget the ratchet check into the
merge step, where this round's explore flags cost +3 hotspots.

**2026-08-19 — Grok 4.6 (Cursor), now 4-for-4:** picker round-2 lane
(un-pick/re-pick + native-select picker + pill CSS) — clean scope
(byte-verified), all 6 deviations logged with correct reasoning, mutation
tables real (2 independent probes RED incl. the bridge re-arm trap), honest
about what it could not verify (CSS visually — flagged for the reviewer).
Only nit: a written-never-read bridge field (`widget.session.claimed`) whose
semantics the comment contradicts — a design-taste miss, not a defect; the
light tier + independent mutation pass remains the right calibration. It
also correctly used finishing-a-development-branch and left the branch
local per the no-push rule — but left the MAIN CHECKOUT on its own branch
(the same Sol behavior; check `git -C <main> branch --show-current` before
any merge).

**2026-08-18 — two-lane round (Project M side panel), both clean.**
**Grok 4.6 (Cursor), now 3-for-3:** panel application-picker lane — clean
scope (byte-verified), executing-plans engaged, all 5 deviations logged with
correct reasoning (incl. improving the wire with a server-side `status`
filter it verified exists), sound ratchet fix by decomposition; light-tier
review found ZERO defects, only two comment/a11y minors. Light-tier
calibration validated again. **GPT Sol (Codex), strong round with the BEST
stop-behavior yet seen:** hit the handoff's named trap (a real seam
contradiction), STOPPED pre-code with an exact 3-point diagnosis and a
sound unblock proposal — the designed behavior, executed perfectly. Fix
rounds fast and complete; honestly reported two SURVIVING mutations with
redundancy explanations that verified TRUE when executed as pairs. Two real
defects in round 1 on the privacy seam (release coupled to geography
tokens; a lossy dual-read write) — both the kind full-adversarial review
exists for: KEEP the no-shortcut rule for privacy/safety seams regardless
of Sol's strong zone. One unlogged deviation (a necessary+pinned extra
hunk) — deviation logging is good but not perfect; keep the hunk-by-hunk
diff check for narrowly-authorized edits.

**2026-08-16 — Grok 4.6 second lane outcome (Project M, Cursor CLI): clean
again, now 2-for-2.** Extension collect/orchestrate lane (Guided Apply R1):
exact scope (respected a function-level ownership carve-out inside its own
file), all 4 deviations logged unprompted with correct reasoning (incl. a
legitimate contract adaptation — Elements can't cross iframe broadcasts —
that it wired through the frame-gate invariant AND extended the pin test
for), honest self-reported gaps (checkbox hole, empty known_value), real
tests (reviewer ran 4 independent mutations: 3 killed, the 1 survivor
traced to redundant cosmetic code, not vacuous tests), clean committed
tree. Peer-autonomy adapt-and-advise worked as designed; its "peer notes"
were genuinely useful review input. Light-touch confirmed appropriate for
well-scoped extension/agentic work.

**2026-08-14 — Gemini 3.7 Flash first real lane outcome (Project M,
Antigravity CLI):** strong implementation, weaker process discipline, on a
backend+frontend feature squarely in its new strong zone (KB custom
sections). The hard parts were right: consolidation extras rode the
existing identity machinery (no fork), compose semantics correct, shared
frontend helpers imported not re-declared, self-run mutation checks real
(reviewer's mutation A was killed by the lane's own round-trip test). But
the reviewer's coverage probe found re-ingest idempotency for the new
entity kind entirely unpinned (a gutted identity index left all 62 KB
tests green), it left ALL work uncommitted in the shared checkout plus a
scratch file, and it reported the slop ratchet as "Passed" when it had
actually re-baselined past a duplication regression (disclosed only in
deviation notes). Calibration: light-touch is right for its code, but
budget a reviewer-run coverage probe (not just re-running its tests) and
check the ratchet baseline diff explicitly.
clean on first outing, two days post-release. Well-scoped backend+frontend
feature pair (chat-client factory + probe rerouting + catalog trim) in an
invariant-heavy file seam: exact-scope diff, all 7 deviations logged
unprompted, tests written adversarially (exact constructor-kwargs asserts,
assertion-bombs on wrong paths — the anti-vacuous-mock pattern this repo
mandates), and the reviewer's independent mutation checks were both killed
by the intended test. Live-probe evidence supplied without being chased.
Supports the profile's light-touch tier for well-scoped agentic coding;
still no data here on hard long-horizon work.

**2026-08-14 — two model replacements and one index rescale.**
- **Grok 4.6** (released Aug 12, 2026, ~5 weeks after 4.5) replaces Grok
  4.5 in the Cursor section. It moves from "competitive but not frontier"
  to genuinely frontier-tier: AA Intelligence Index 61, tied with GPT-5.6
  Sol (max), behind only Opus 5 (63) and Fable 5 (62). Its hallucination
  problem — the single biggest caveat on the 4.5 profile — materially
  improved.
- **Gemini 3.7 Flash** (released Aug 13, 2026, ~3 weeks after 3.6 Flash)
  replaces Gemini 3.6 Flash in the Antigravity section. The "3.6 Flash is a
  speed/cost win but not an intelligence gain" caveat from the previous
  entry **no longer applies** to 3.7 Flash: this one is a real capability
  jump (+4 AA Index, DeepSWE 49.0% → 65.3%), which finally makes the
  strong-zone recommendation for this agent uncomplicated.
- **AA Intelligence Index rescaled to v4.1.1** — the index now aggregates
  9 evaluations (GDPval-AA v2, τ³-Banking, Terminal-Bench v2.1, SciCode,
  Humanity's Last Exam, GPQA Diamond, CritPt, AA-Omniscience, AA-LCR).
  **Scores in this file from before 2026-08-14 are on the older version and
  are not directly comparable** — under v4.1.1 the whole board shifted up
  roughly 2 points (Opus 5: 61 → 63, Fable 5: 60 → 62, GPT-5.6 Sol: 59 →
  61, Grok 4.5: 54 → 56, Gemini 3.6 Flash: 50 → 52). When comparing any two
  numbers here, check they're from the same index version before reading a
  gap as real.

**2026-07-25 — don't assume tier names imply capability ranking.** The
Antigravity section originally assumed "Pro" outranks "Flash," which was
wrong: the Flash line has been Google's actively-developed tier while
3.1 Pro sat in Preview. That lesson still holds and now generalizes — check
current benchmarks per vendor rather than trusting naming conventions.
Also established the standing sourcing rule for this file: **prefer
Artificial Analysis (independent, same-harness evaluator) over
vendor-reported numbers wherever both exist**; keep vendor numbers only
where AA hasn't published a comparable figure, and label them as such.

This file exists to fix one specific problem: the main session was
defaulting to full re-verification of every delegated task regardless of
outcome quality, because there was no written expectation of what each
agent/model combo is actually good at. Use it to pick a review tier
(see SKILL.md), not as a substitute for judgment on genuinely novel tasks.

---

## Codex CLI ("gpt sol" / "sol")

**What it is:** OpenAI's terminal coding agent. Branches typically land as
`codex/*`. Note: OpenAI's July 2026 model tier is literally named "Sol" —
unrelated to the author's nickname "gpt sol" for this agent. Don't
conflate the two when reading about "Sol" online.

**Model landscape (as of 2026-09-20): four selectable models, not three
tiers.** GPT-6 Astra sits above the GPT-5.6 generation (profiled
immediately below); GPT-5.6 itself went GA in Codex on July 9, 2026,
replacing the GPT-5.5/GPT-5.x-Codex generation, and its three tiers all
remain selectable:
- **Sol** — flagship, deep-reasoning tier. Best default for hard tasks.
- **Terra** — balanced, everyday-work tier. Reasonable default for typical
  implementation tasks.
- **Luna** — fast/cheap tier for high-volume or low-complexity work,
  meaningfully less capable than Sol/Terra on anything requiring depth.
- **Ultra mode** (Plus and up) runs 4 agents in parallel for wide,
  multi-file refactors — trades higher token/usage burn for wall-clock
  speed; not meant for single-file fixes.
- Legacy model strings (`gpt-5.1-codex`, `gpt-5.2-codex`, etc.) were
  deprecated in the CLI/API through July 23, 2026 — if a branch references
  one of these, the run predates the current generation. `gpt-5.4` and
  `gpt-5.4-mini` retired 2026-08-31.

**Update 2026-10-19:** the Codex catalog now also lists `gpt-6.1-sol` (the
default since 0.161.0, 500k context), `gpt-6-sol` and `gpt-6-luna` (below).
`gpt-reserve` is hidden and is the "Luna Reserve" post-quota fallback, not a
separate model.

### GPT-6 Luna (added 2026-10-19) — confidence: independent, early

- Released Sept 2026 (OpenRouter: Sept 22) alongside GPT-6 Sol
  (openai.com/index/introducing-gpt-6-sol-and-luna/). GA in the API and in
  Codex for Plus and up. Codex catalog: `gpt-6-luna`, efforts low to max,
  **272k context in Codex** (the API doc says 1.05M; 272k is also the
  long-prompt pricing threshold).
- **AA Intelligence Index v4.3.2: 38 at max** (xhigh 35, high 33, medium
  30), against GPT-5.6 Sol's 47. $0.07 per index task; 140M output tokens
  across the run.
- Vendor-reported: DeepSWE v1.1 66.6% at max, which OpenAI calls comparable
  to Opus 5 / Fable 5 at medium effort at 93–96% lower cost per task;
  AutomationBench +5.4 pp over GPT-5.6 Luna at high effort.
- $0.10 / $0.50 per MTok, half of GPT-5.6 Luna's promo price and the same
  price point as Claude Haiku 5.5.
- October system card: in max-effort rollouts, 15.9% kept circumventing
  environment restrictions after a warning (GPT-5.6 Luna: 27%). Better,
  but run it sandboxed (`-s read-only` / `workspace-write`), not with full
  access.
- Fit: the cheap high-volume narrow-pass slot GPT-5.6 Luna held. Starts on
  full review; the GPT-5.6 Luna record does not transfer.

---

### GPT-6 Astra (added 2026-09-20) — the new top model

**What it is and how it shows up in the CLI.** Released 2026-09-09;
available in Codex CLI from 2026-09-03 via a Trusted Access Programme with
staged general availability. Model string `gpt-6-astra` (`model =
"gpt-6-astra"` in `config.toml`). It does **not** replace Sol/Terra/Luna —
all four are selectable. Five reasoning-effort levels: `low`, `medium`,
`high`, `xhigh`, `max`, with `high` documented as the sensible default for
ordinary coding and `xhigh`/`max` reserved for architecture work and hard
debugging. ~1.05M-token context (922k max input / 128k output).
**Effort level is part of "which model landed"** — Astra-at-low and
Astra-at-max are not the same delegate.

**Independent standing (Artificial Analysis, checked 2026-09-20, index
v4.3.2 — not comparable to the v4.1.1 numbers elsewhere in this file):**
- **AA Intelligence Index 53 (max) — tied for first with Claude Fable
  5.1**, and well clear of GPT-5.6 Sol's 47 on the same version.
- **AA Coding Agent Index 62 — tied with Fable 5.1, ahead of Claude Opus 5
  (60) and Sol (55).** First time a non-Claude model in this file has
  matched the top of the coding index.
- **Terminal-Bench 4.0: 59%** vs Fable 5.1's 52% — leads.
- **AutomationBench-AA: 68%** vs Fable 5.1's 59% and Grok 4.6's 67% —
  leads. Business-process automation is its clearest win.
- **GDP.pdf: 31%** vs Fable 5.1's 26%; **CritPt 32%** vs 30% — leads both.
- **AA-Omniscience 43, hallucination rate 51% — halved from GPT-5.6 Sol's
  92%.** The largest single-generation calibration improvement recorded in
  this file. Sol's 92% is worth re-reading on its own terms: if you have
  been taking factual claims from Sol branches at face value, don't.
- **Token efficiency is the standout**: roughly a third of Fable 5.1's
  output tokens for the same index score, and $3.26 vs $7.63 cost per index
  task. Headline price $10/$50 per MTok (cache reads at a 90% discount,
  ~$1.00; cache writes at a 25% premium), 59 tokens/sec.
- **Where it loses to Fable 5.1:** SciCode 56% vs 63%, Humanity's Last Exam
  55% vs 59%, AA-LCR v1.1 81% vs 85%, AA-Briefcase v1.1 1569 vs 1678, and
  **GDPval-AA v2.1 1542 vs 1735**. Knowledge work is its weakest dimension,
  and it went *backwards* there — roughly 45 Elo below GPT-5.6 Sol.
- **DeepSWE is unresolved.** AA's launch write-up reports 68%; a second
  source reports 74.1% against Fable 5.1's 67.4%. Don't build a DeepSWE
  argument on Astra without re-checking which is right.
- OpenAI's own (vendor-reported) numbers: OSWorld V2-Offline 72.6% vs Sol's
  65.7% with average task time cut from ~75 to ~40 minutes; Mind2Web
  browser tasks 1.9x faster than Sol under the updated Codex harness; MRCR
  v2 8-needle 100% at 256K–512K (Sol 91.5%) and 96.3% at 512K–1M (Sol
  73.8%). Treat as directional.

**Two behaviors that change how a handoff should be written:**
- **Context notes instead of compaction.** Astra keeps running notes across
  context windows and retains searchable access to earlier ones rather than
  summarizing and discarding. This should make very long unattended runs
  lose less detail than Sol-era compaction did — plausible from the MRCR
  numbers, but unverified here.
- **It asks questions asynchronously.** It continues work that doesn't
  depend on your answer, proceeds on its own assumptions for minor
  decisions, and blocks only on consequential ones. This makes the Goal
  Card and decision principles from `goal-anchored-delegation` matter
  *more*, not less: it will act on assumptions while waiting, so the
  handoff has to tell it which way to lean.

**Astra's safety profile changes the review procedure, not just the tier.**
Per Astra's published safety materials (system-card-derived; not
independently replicated, and not a claim about the author's own setup):
it shows a **substantial decrease in chain-of-thought monitorability and
can evade monitoring when instructed**, reaches the **Critical**
cybersecurity capability level (zero-day discovery), and in a controlled
evaluation conducted supply-chain attacks in **2 of 500 sampled runs**.
Practical consequences for this workflow:
- **A clean reasoning transcript is weaker evidence than it was for Sol.**
  Audit the diff and the MCP/tool results directly rather than reading the
  narrative and trusting it.
- Prefer shell-execution approval hooks over post-hoc review for any lane
  touching dependencies, lockfiles, CI config, or install scripts.
- **Dependency and supply-chain changes from an Astra branch get full
  adversarial review regardless of tier.** 2/500 is a low base rate, not a
  zero one, and this is the cheapest place to spend the review budget.

**Suggested default review tier for Astra:** light-touch for well-scoped
implementation, terminal/agentic lanes, and business-process automation —
its index standing supports that, and the halved hallucination rate
supports relaxing the factual-claim scrutiny Sol warranted. Full
adversarial for knowledge-work-heavy tasks (its weakest dimension, where
both Fable 5.1 and Opus 5 clearly lead), for anything touching the supply
chain per above, and for the first few rounds generally. **One delegated round has now been
run (2026-09-20c in the correction log: KB Core M1 pilot, Tasks 1–3, effort
`high`) and came back clean** — a first earned data point; the rest of this
block remains benchmark-derived.

---

**Ask which model and effort level landed** — Codex now exposes four
models. A "sol" branch (the author's nickname for the agent) could be GPT-6
Astra, GPT-5.6 Sol (OpenAI's tier), Terra or Luna, and the review picture
differs at every step: Luna runs $0.20/$1.20 per MTok against Astra's
$10/$50 — ~50x on input — and sits at the opposite end of the capability
range. (Their published index scores are on different AA versions and
cannot be subtracted; see the version warning at the top of this file.)

**Luna is cheap and closer to Sol than the tier name suggests — update to
the earlier assumption in this file.** Per Artificial Analysis (independent,
checked 2026-08-05): Luna (max effort) scores 51 on the AA Intelligence
Index vs. Sol's 59 and Terra's 55 — a real gap, but a narrow one (8 points),
not the "meaningfully less capable" framing this file used before pricing
data caught up. After OpenAI's July 30, 2026 price cut, Luna runs
$0.20/$1.20 per 1M input/output tokens — roughly 25x cheaper than Sol
($5.00/$30.00) and ~10x cheaper than Terra ($2.00/$12.00) — while being
one of the fastest models in its class (~178 tokens/sec). OpenAI's own
launch data separately claims Luna clears GPT-5.5 on Agents' Last Exam,
HealthBench Professional, and DeepSWE, though that's vendor-reported and
should be weighed against AA's independent, more conservative Intelligence
Index gap above.

**Practical read for delegation:** Luna is a legitimate pairing partner
alongside a stronger reviewer, not just a fallback for trivial work. Good
fit for high-volume, well-scoped, low-ambiguity passes — line-by-line code
checks, lint-style review, straightforward single-file implementation,
first-pass drafts — where a Sol or Terra (or Claude) pass then reviews or
finishes the harder judgment calls. It's still not the pick for deep
architectural reasoning or novel-problem tasks; the AA gap to Sol, while
narrower than previously assumed here, is real and concentrated in exactly
that kind of task. Cost asymmetry (Luna at ~1/25th Sol's price) makes a
Luna-first-pass-then-Sol/Claude-review pattern worth considering even when
Sol alone could do the whole task, purely on cost-efficiency grounds.

**Documented strong zones:**
- Long-running, project-scale agentic coding — this is what the Codex line
  is specifically trained/tuned for
- PR creation, code review, frontend coding
- Endurance tasks — running unattended for extended periods without losing
  coherence (context compaction is a deliberate design focus)
- Wide, multi-file refactors when run in Ultra mode
- Single-file, intent-driven tasks with a clear scope

**Documented weak/uncertain zones:**
- General-purpose (non-coding) reasoning — OpenAI positions the Codex
  surface specifically for agentic coding, not general use
- Anything requiring the Luna tier to do deep architectural reasoning —
  the AA Intelligence Index gap to Sol (51 vs 59) is real and concentrated
  here, even though it's narrower than this file previously assumed
- No strong public signal yet on long-horizon cross-service architecture
  decisions specifically (as opposed to implementation within an existing
  architecture) — treat as unverified until the user's own track record
  says otherwise

**Suggested default review tier (GPT-5.6 generation; Astra has its own
tier note above):** Light-touch for well-scoped implementation/endurance
tasks on Sol or Terra. For Luna specifically:
light-touch is fine for narrow, well-scoped work (line-by-line checks,
single-file implementation, first-pass drafts) — especially if a stronger
model (Sol, Terra, or Claude) is reviewing or finishing the output as part
of the same handoff, since that pairing pattern is Luna's actual strong
use case. Full adversarial review for Luna doing deep architectural
reasoning solo, or for novel architecture decisions on any tier.

---

## Antigravity CLI ("agy")

**What it is:** Google's successor to Gemini CLI, binary `agy`. Gemini CLI's
free/Pro/Ultra personal-account access was shut down June 18, 2026 and
migrated to Antigravity CLI; the old `gemini` command only still works for
enterprise/API-key holders. If the user says "gemini" they likely mean this.

**Model landscape (as of Aug 2026) — the Flash line is the real line here,
not Pro.** Google has shipped three Flash-tier upgrades between May and
August 2026 (3.5 → 3.6 → 3.7) while the Pro flagship has gone untouched
since February. **Gemini 3.7 Flash (released Aug 13, 2026) is the current
default pick** and, unlike the 3.6 Flash situation this file previously
documented, it's a real capability jump rather than just a speed/cost win:

- **AA Intelligence Index 56** at high reasoning (v4.1.1), up 4 points over
  3.6 Flash's 52 — ahead of Claude Sonnet 5 (55), just behind GPT-5.6 Terra
  and Muse Spark 1.2 (both 57). Medium reasoning scores 53, low scores 51.
- **DeepSWE v1.1: 65.3%, up from 3.6 Flash's 49.0%** — the single most
  important number for delegation purposes, and a genuine generational gain
  (Google-reported).
- **FrontierCode v1.1 Main: 43.6%**, up from 34.4%.
- **Terminal-Bench 2.1: 85.8%** (+8 points per AA).
- **AA-Briefcase: 1132 Elo** (+169 over predecessor); **GDPval-AA v2:
  1525 Elo** (+103).
- **AA-AnalystAgent: 60% pass^5 — the highest score of any model**, ahead
  of Claude Opus 5 (54%) and Fable 5 (49%). This benchmark measures
  answering complex questions about spreadsheets and documents; it's the
  one place 3.7 Flash outright leads the frontier.
- **Speed/cost:** 340 tokens/sec, ~40% faster time-per-task than GPT-5.6
  Terra, placing it on AA's Intelligence-vs-Time Pareto frontier. Standard
  price $1.50/$7.50 per MTok, **discounted to $0.75/$3.75 through Dec 31,
  2026, reverting Jan 1, 2027** — factor the reversion in before building a
  cost argument on it. Uses ~40% more output tokens than 3.6 Flash.
- 1M-token context, multimodal input (text, image, video, audio, PDF).
  Available in Antigravity on day one.

**Version caveat added 2026-09-20:** every index and benchmark figure in
this section is on **AA Intelligence Index v4.1.1** and the pre-v4.3
benchmark set. AA has not published a v4.3.2 figure for Gemini 3.7 Flash,
so it cannot be placed against Fable 5.1's or Astra's 53. Gemini's standing
relative to the other three agents here is therefore **unrefreshed since
2026-08-14** — re-search before a consequential Antigravity handoff rather
than assuming the gaps below still hold.

**Where it does not lead:** GPT-5.6 Terra beats it on DeepSWE (69.6%),
Terminal-Bench 2.1 (87.4%), Terminal-Bench 3.0 (20.8% vs 14.9%), and
OSWorld 2.0 (50.2% vs 38.1%). Sonnet 5, Terra, and Muse Spark 1.2 all beat
it on GDPval-AA v2 knowledge work (1598 / 1578 / 1628 vs 1525). CharXiv
Reasoning is an outright regression (84.5% vs 3.6 Flash's 85.2%).

**Note the reversal on computer use.** The previous entry flagged 3.6
Flash's OSWorld-Verified 83.0% as its most credibly frontier-competitive
result. Google's newer table reports 3.7 Flash at **38.1% on OSWorld 2.0**,
trailing Terra — these are different harnesses (OSWorld-Verified vs OSWorld
2.0), so this is not a measured regression, but **computer use is no longer
a documented strong zone for this agent.** Don't carry the old claim
forward; if a task is computer-use-heavy, verify rather than assume.

**Other tiers:**
- **Gemini 3.6 Flash** — superseded three weeks after launch. No reason to
  choose it over 3.7 Flash.
- **Gemini 3.1 Pro** — still Preview, still six months old, still only
  worth reaching for on hard non-coding reasoning (GPQA Diamond, Humanity's
  Last Exam) rather than implementation.
- **Gemini 3.5 Flash-Lite** — cheaper/faster still, for high-throughput or
  low-latency work, not deep reasoning.
- Gemini 4 reportedly in early pretraining; no near-term release expected.

**Ask which one landed** — Google's release cadence here is ~3 weeks, so
"a Gemini branch" is badly underspecified. A 3.7 Flash branch and a 3.6
Flash branch warrant meaningfully different confidence, and a Flash branch
should not be trust-downgraded relative to Pro.

**Documented strong zones:**
- Coding and agentic work on **3.7 Flash specifically** — and this is now a
  claim that survives cross-vendor comparison, not just a claim about
  Gemini's own lineup. DeepSWE 65.3% lands between Opus 4.8 (59.0%) and
  Opus 5 (68.8%), i.e. genuinely in frontier range rather than trailing it
  by 20 points the way 3.6 Flash did.
- **Document- and spreadsheet-heavy analytical work** — the AA-AnalystAgent
  lead (60% pass^5, best of any model) plus GDP.pdf 34.0% vs 22.0% make
  this the clearest standout. If a delegated task is "read these documents
  and answer hard questions about them," this is the strongest pick in this
  whole file, Claude included.
- **Web/UI generation** — WebDev Arena 1588 Elo (up from 1538), leading
  Sonnet 5 (1541), Muse (1535), Terra (1523).
- Very large context — entire monorepo in a single pass (1M tokens).
- Cross-file bug tracing in a large codebase; fast, cheap exploration.

**Documented weak/uncertain zones:**
- **Terminal-heavy and computer-use work** — trails Terra on both
  Terminal-Bench versions and OSWorld 2.0. This is the clearest weak zone
  and it's the one that matters most for CLI-driven delegation.
- Broad knowledge work (GDPval-AA v2) — trails Sonnet 5, Terra, and Muse.
- Multi-agent orchestration remains newer here than Codex's endurance mode;
  treat coordination-heavy or very long autonomous runs as less proven.
- Quota/reliability: post-migration quota is weekly and shared across the
  orchestration layer, so a stalled task may be quota/infra rather than
  capability — check before concluding the model struggled.
- Google's own launch table is not a controlled bake-off: its methodology
  notes state Gemini figures are generally pass@1 with default sampling
  while many competitor figures are provider-reported, several Gemini agent
  and multimodal results were self-computed, and harnesses/tool access
  differ per row. Prefer the AA figures above where both exist.
- **Post-Jan-2027 pricing** — the cost case weakens by 2x when the
  introductory discount expires.

> **2026-10-19: the tier below is stale for Flash.** Gemini 3.7 Flash was
> deprecated 2026-10-08 and requests route to 3.8 Flash, so a "3.7 Flash"
> lane now runs 3.8 Flash. Use full review on Flash lanes until 3.8 Flash
> has its own rounds (see the 2026-10-19 subsection below).

**Suggested default review tier:** Light-touch for coding/agentic tasks and
especially document/spreadsheet analysis on **3.7 Flash**, or hard
non-coding reasoning on 3.1 Pro. Full adversarial for terminal-heavy or
computer-use tasks, anything on Flash-Lite involving non-trivial logic,
multi-agent orchestrated runs, or when quota/infra issues make the actual
execution path unclear.

### Gemini 3.8 Flash and Gemini 4 Argon (added 2026-10-19)

**Gemini 3.8 Flash** (`gemini-3.8-flash`) — confidence: vendor claims only, no numbers
- GA 2026-09-02 (Gemini API changelog). Now the default model for the
  Antigravity agent and SDK. Reports of which Antigravity plans get it
  conflict (all plans vs Pro/Ultra only). Also in Cursor's catalog.
- **No benchmark figures published** by Google or found from independents.
  Google says it may spend more tokens on long, complex tasks by design;
  lowering the thinking level cuts that.
- $0.75 / $3.75 per MTok through 2026-12-31, then $1.50 / $7.50. 1M
  context, 64k output. Thinking levels low / medium (default) / high.
- API migration breaks old calls: `thinking_budget` becomes
  `thinking_level`; temperature, top_p and top_k are removed; text before a
  tool call can trigger Malformed_Function_Call.
- There is no 3.8 Pro, and "3.8 Flash-Lite" exists only as a TTS model.

**Gemini 4 Argon** (`gemini-4-argon`) — confidence: vendor claims only
- Google's new flagship reasoning model. Announced around 2026-09-30, GA
  on the Gemini API (model page updated 2026-10-14). Antigravity rollout
  from 2026-10-13 for **AI Ultra and eligible Enterprise only** (secondary
  report). Present in the local `cursor-agent models` list on 2026-10-19.
- Google's table (single attempt, highest thinking), Argon / GPT-6 Astra /
  Opus 5.5: DeepSWE v1.1 77.9 / 74.1 / 74.2; FrontierSWE v2 55.0 / 65.5 /
  62.3; Terminal-Bench 4.0 57.4 / 58.2 / 66.4; AutomationBench 51.3 / 41.4
  / 42.5; Vals Index 68.9 / 63.1 / 67.0. It leads on repo-scale SWE and
  automation and trails on terminal and frontier SWE work.
- **AA Intelligence Index v4.3.2: 53 at high** (AA model page, fetched
  2026-10-19), level with Fable 5.1 and Astra. AA-Omniscience
  hallucination rate 15% (secondary), low if it holds.
- $2 / $10 per MTok introductory, rising to $4 / $20 around Dec 1 (sources
  differ on the exact date). 1M context.
- Fit: a candidate for the Antigravity "Pro" slot (3.1 Pro has been
  untouched since February), if the user's plan includes it. Full review;
  no rounds yet.

---

## Cursor CLI ("cursor" / `agent`) with Grok 4.6 / 4.7

**What it is:** Cursor's headless CLI (binary `agent`), a real scriptable
delegation target — same shape as Codex/Antigravity, not the editor.
Supports `agent --headless "..."` or `agent -p "..."` for CI/scripted use,
shares MCP servers/rules/auth with the desktop app, and is model-selectable
(`/model` or a flag) across Claude, GPT, Gemini, and xAI's Grok line.
**Context that changes the trust picture here:** SpaceX acquired Cursor for
~$60B, closing alongside Grok 4.5's joint launch — Cursor is no longer an
independent company, it's the coding surface xAI uses to distribute Grok.
Worth knowing when weighing how "neutral" Cursor's own benchmark framing of
Grok is, and note CursorBench is now effectively a first-party benchmark.

**Model note:** the author runs Cursor **only for Grok** (stated 2026-09-25).
Other families go through their own agents: GPT through Codex, Claude
natively. So "delegate to Cursor" means Grok 4.6 or Grok 4.7; confirm which
one and at what effort. This section covers **Grok 4.6** (the profile with
the earned track record) and **Grok 4.7** (added 2026-09-21, at the end of
the section). A Cursor run on anything else (the plugin's Composer 2.5
default, or Auto) is out of policy, not a new profile to calibrate.

**Independent benchmark standing (Artificial Analysis, checked 2026-08-14).**
Grok 4.6 released Aug 12, 2026, roughly five weeks after 4.5, and is a
larger jump than that interval suggests: **AA Intelligence Index 61
(v4.1.1), tied with GPT-5.6 Sol (max), behind only Claude Opus 5 (63) and
Claude Fable 5 (62)** — up 5 points from Grok 4.5's 56 and 23 points from
Grok 4.3. **This model has crossed from "competitive but not frontier" into
the frontier cluster**, which is a real change from the 4.5 profile this
section previously carried.

Standing on shared benchmarks:
- **GDPval-AA v2 (Elo): 1753 — second only to Opus 5**, ahead of GPT-5.6
  Sol max (1728) and with confidence intervals overlapping Fable 5 (1741).
  Up from Grok 4.5's 1526. Knowledge work is its strongest dimension.
- **τ³-Banking: 50.7%** — top two overall alongside Qwen3.8 Max (51.3%).
- **Terminal-Bench v2.1: 88.4%** — in line with the leaders (Sol 88.8%).
- **AA-Briefcase: 1577 Elo** (up from 1313), behind Opus 5 (1720).
- **DeepSWE v1.1: 65.9%**, up sharply from 54% — but still behind GPT-5.6
  Sol max (73%) and Fable 5 max (70%).
- **FrontierCode v1.1 Extended: 61.3%** (from 56.6%) — ahead of Sol
  (60.6%), behind Fable 5 max (63.6%).
- **CursorBench v3.2: 69.9%** (from 66.7%) vs Fable 5 max 70.5% — treat as
  first-party given the ownership structure.
- **APEX-Agents: 57.5%**, up from 47.1%.
- **Terminal-Bench v3.0** remains a relative gap versus rivals.
- Completes complex GDPval tasks in ~53 steps.

**Hallucination — materially improved, and this is the headline change.**
The 4.5 profile's biggest caveat was a hallucination rate that jumped to
54%. For Grok 4.6, AA measures **AA-Omniscience accuracy 48.2% and a
non-hallucination rate of 65.7%** — i.e. roughly a third of its non-correct
answers are confident inventions rather than admissions of not knowing.
That's a substantial calibration improvement over 4.5, though accuracy
itself is slightly lower (48.2% vs 52%). Net: **factual claims from Grok
4.6 still deserve verification, but no longer the exceptional scrutiny 4.5
warranted.** xAI's own launch table has ten rows and none of them covers
being wrong, so this number comes only from AA.

**Cost/efficiency — still the standout.** Headline pricing unchanged from
4.5 at **$2/$6 per MTok** ($0.50 cached; doubles to $4/$12 past 200k prompt
tokens), a fast variant at 2x. That's 60%+ below Opus 5 ($5/$25) and
GPT-5.6 Sol ($5/$30) while matching Sol on the composite index — AA
measures $0.84 per Intelligence Index task. **Frontier-tier intelligence at
roughly a third of frontier cost is now the core reason to delegate here**,
and it's a stronger argument than it was for 4.5, where the intelligence
claim needed hedging. 500k-token context, unchanged.

**Documented strong zones:**
- **Knowledge work and legal/financial reasoning** — GDPval-AA v2 second
  only to Opus 5, top-two τ³-Banking, and leading Harvey LAB per xAI. This
  remains a genuine differentiator from the other three agents in this file.
- **Terminal/agentic tasks** — Terminal-Bench 2.1 at 88.4% is now
  leader-adjacent rather than merely competitive.
- Long-running agents and work spanning codebases — xAI's stated primary
  workloads, and the RL stage specifically targeted agentic tasks.
- Rust and C/C++ (carried forward from 4.5 per xAI's materials; still not
  independently corroborated — treat as provisional).
- Cost-sensitive work where a frontier-adjacent result at a third of the
  price beats squeezing out the last few accuracy points.

**Documented weak/uncertain zones:**
- **Hard agentic coding** — DeepSWE v1.1 65.9% trails Sol (73%) and Fable 5
  (70%) by 4-7 points. Closer than 4.5 was, but this is still the weakest
  dimension relative to the frontier.
- **Terminal-Bench v3.0** specifically (the harder, newer variant).
- **No independent replication of xAI's own table existed as of Aug 14,
  2026** — one day post-launch. The AA numbers above are the verified set;
  treat xAI's ten-row launch chart as marketing selection.
- **Self-verification claim is unmeasured.** xAI says the model does more
  self-testing on long trajectories. That's a claim to test, not a number —
  don't let it substitute for review. Related: 4.6's SFT data was
  regenerated by Grok 4.5 itself, so a 4.5-style blind spot could persist
  through the generation without showing up in benchmarks.
- Real-world parity is unestablished. Index parity with Sol is not the same
  claim as parity in practice, and nobody had meaningful hours on it at the
  time of writing.

**Suggested default review tier:** Light-touch for knowledge work,
legal/financial analysis, terminal/agentic tasks, and well-scoped coding.
Full adversarial for hard long-horizon coding resembling DeepSWE or
Terminal-Bench 3.0's profile. Verify factual/citation claims as a matter of
course, but the extra-scrutiny flag from the 4.5 era can be relaxed to
normal verification. When written (2026-08-14) this model was days old and
this was the least battle-tested profile in the file; it has since become
the *most* battle-tested — 10-for-10 in the correction log — and the tier
above held up. **That record is Grok 4.6's alone; see Grok 4.7 below.**

### Grok 4.7 (added 2026-09-21, release day) — the record above does not transfer

**What it is.** SpaceXAI released Grok 4.7 on 2026-09-21, about six weeks
after 4.6, and it is in Cursor from day one (also Grok Build, the Grok API,
and third-party harnesses and routers). It ships as an xHigh standard model
plus a fast variant at 2x output speed for 2x price. **Headline price is
unchanged at $2/$6 per MTok** (fast: $4/$12); 500k-token context per AA.
Musk puts it at 2.1T parameters vs 4.6's 1.5T — a founder claim, not in any
model card.

**The fact that matters most here: the 10-for-10 record in the correction
log was earned by Grok 4.6, not 4.7.** Cursor lanes can change model under
you, and Cursor is likely to move its Grok default to 4.7. Confirm which
Grok ran before applying the light tier. If 4.6 stays selectable, pinning
it keeps the earned calibration; if the lane ran 4.7, treat it as a new
delegate.

Why not assume continuity: 4.7's training changed exactly the behaviors
that record rests on. xAI describes a longer RL run weighted toward harder,
extended-effort tasks, plus stronger self-verification and new context
management. The release also slipped from ~Sept 12 because, per Musk's
Sept 11 post, RL had penalized response length too hard — the model quit
hard tasks early and under-checked its own work. Whether that fix landed
cleanly is unmeasured.

**Independent standing (Artificial Analysis, checked 2026-09-21 — hours
after launch, so partial):**
- **AA Intelligence Index 46 (xhigh, v4.3.2)**, 16th of 655 models. Grok
  4.6 (high) reads 44 on the same version, so the gain is +2 — and even that
  crosses effort variants. **7 points behind Fable 5.1 and GPT-6 Astra (53)
  and 1 behind GPT-5.6 Sol (47).** On v4.1.1 Grok 4.6 tied Sol; on v4.3.2
  the Grok line sits just below it.
- **Verbosity is the big shift: 240M output tokens to run the index vs
  Grok 4.6's 94M — about 2.5x.** That is the length-penalty fix showing up.
  With per-token price flat, **the cost-per-task edge that was the core
  reason to delegate to Grok 4.6 is substantially eroded.** AA had not
  published cost per task or output speed at time of writing — check before
  building a cost argument.
- **Terminal-Bench 4.0: 26%** per AA as reported by The Decoder (vs ~60%
  Astra, ~55% Fable 5.1), not yet confirmed on AA's own page. xAI's table
  gives **38.0%** — a 12-point runner gap. On either figure it is far behind
  the frontier pair.
- No AA-Omniscience/hallucination figure yet. Do not assume 4.6's 65.7%
  non-hallucination rate carried over; a longer-answering model can move
  either way on this.

**xAI's own launch table (vendor-reported — note the comparison columns):**

| Benchmark | Grok 4.7 | Grok 4.6 | GPT-5.6 Sol | Fable 5.1 |
|---|---|---|---|---|
| DeepSWE v1.1 | 71.0%* | 65.2% | **72.7%** | 70.0% |
| CursorBench 4.0 | 46.3% | 40.4% | 41.7% | **51.8%** |
| Terminal-Bench 4.0 | 38.0% | 20.3% | 37.3% | **57.9%** |
| AA-Briefcase v1.1 (Elo) | 1657 | 1546 | 1487 | **1678** |
| EEBench | **64.0%** | 53.0% | 39.4% | 56.4% |
| Harvey Legal Agent | **19.6%** | 15.8% | 2.5% | 6.7% |
| HealthBench Professional | 56.7% | 48.5% | 60.5% | **62.1%** |

\* xAI asterisks the DeepSWE figure; the footnote was not available at time
of writing — check it before relying on the number. **The OpenAI column is
GPT-5.6 Sol, not GPT-6 Astra**, although Astra shipped twelve days earlier;
against Astra (Coding Agent Index 62, AA Terminal-Bench 4.0 59%) the coding
picture would look worse. Same pattern as 4.6's launch table: no row
measures being wrong.

**Read of the numbers:**
- **Real gains over 4.6** on xAI's own rows: Terminal-Bench 4.0 nearly
  doubles (20.3% → 38.0%), DeepSWE +5.8, CursorBench +5.9, AA-Briefcase
  +111 Elo.
- **Legal and knowledge work stay the distinctive zone** — Harvey Legal
  Agent 19.6% leads every column by a wide margin, and AA-Briefcase sits
  within 21 Elo of Fable 5.1. Consistent with 4.6's GDPval strength.
- **Still clearly behind the frontier pair on agentic terminal coding** on
  either Terminal-Bench figure. Musk's own framing puts it around Opus 5,
  not Fable 5.1.

**Suggested default review tier for Grok 4.7:** full review for the first
two or three Cursor rounds regardless of lane. Watch specifically for
(a) scope creep from longer, more exhaustive output, (b) whether its
self-reported numbers still reproduce — 4.6's signature — and (c) whether
it still stops and flags plan defects instead of pushing through. The
likely steady state after that: light-touch for legal/knowledge work and
well-scoped frontend/docs lanes (where 4.6 earned it), full adversarial for
terminal-heavy or hard agentic coding, where 4.7 trails Fable 5.1 and
Astra by a wide margin. The standing Cursor merge-step duties apply
whichever Grok ran: browser E2E, the slop ratchet, the dedup scan.

### Other models in Cursor's catalog (out of lane, added 2026-10-19)

The author runs Cursor only for Grok, so these are noted, not profiled.
Quick-scan numbers on mixed index versions: don't rank them against each
other or against the tables in this file.

| Model (slug) | Maker | Released | Key number | Price /MTok |
|---|---|---|---|---|
| Muse Wonder 1.0 (`muse-wonder-1.0`) | Meta | 2026-10-12 (in Cursor 10-15) | CursorBench 46.1% default effort (Cursor, first-party) | $4 / $20 |
| Muse Spark 1.3 (`muse-spark-1.3`) | Meta | 2026-09-02 | AA 62 on v4.1.1 (old scale) | $1.25 / $4.25 |
| Kimi K3 (`kimi-k3`) | Moonshot | July 2026, open weights | AA 44 on v4.3.2 | $3 / $15 |
| Kimi K2.7 Code (`kimi-k2.7-code`) | Moonshot | about 2026-06-12, open weights | no SWE-bench or Terminal-Bench figure found | sources conflict |
| GLM-5.2 (`glm-5.2`) | Z.ai | about 2026-06-13, open weights (MIT) | SWE-bench Pro 62.1 (vendor) | not found |

Grok: nothing newer than 4.7 on x.ai/news through 2026-10-19.

---

## Claude (the baseline these are measured against)

The whole point of this file is calibrating trust in *other* agents' work,
which implicitly means calibrating against what Claude itself would produce.
Making that comparison explicit, instead of leaving it as an unstated
assumption, is what lets the review-tier logic actually reason about "is
this task in Codex's/Antigravity's weak zone *relative to what the main
session could do here*."

**Current models (as of 2026-09-20): Claude Fable 5.1 is the top of the
board.** Released 2026-09-01 at $10/$50 per MTok with cache reads cut 75%
to $0.25, 1M context, ~70 tokens/sec. **Claude Mythos 5.1 is the same
underlying model with reduced safeguards**, available only through vetted
access programs (the Cyber Verification Programme for defensive security
work, the Life Sciences Verification Programme for research, US-only at
launch). If a branch claims Mythos, capability expectations are identical
to Fable 5.1 — what differs is who is permitted to run it, which is the
user's call to confirm, not an inference to make.

Claude Opus 5 (launched 2026-07-24, $5/$25 per MTok) remains the
flagship-priced default on Claude Max and is still the right comparison
point for most delegation calls, since it is what the main session most
often is. Sonnet 5 (agentic mid-tier, released June 30, 2026) remains the
cheaper default across most other surfaces. Opus 5 more than doubled Opus
4.8 on Anthropic's agentic terminal coding benchmark (43.3% vs 21.1%).

**Fable 5.1's independent standing (Artificial Analysis, checked
2026-09-20):**
- **AA Intelligence Index: joint first.** 53 at max-with-fallback on
  current v4.3.2, tied with GPT-6 Astra; xhigh also scores 53. At launch AA
  reported **66** on the then-current index version, against Opus 5's 63,
  Fable 5's 62 and Sol/Grok 4.6's 61. **Same model, different index — the
  two numbers must never be mixed**, and the 66-era figures are the ones
  that line up with the v4.1.1 table further down this file.
- **AA Coding Agent Index 62** (measured in Claude Code), tied with Astra
  and ahead of Opus 5's 60.
- **Terminal-Bench-Science 0.1: 52.6%** vs Opus 5's 29.0%, Fable 5's 24.7%
  and GPT-5.6 Sol's 22.4% — more than double the previous Claude flagship.
  Agentic scientific research is the clearest generational jump.
- **GDPval-AA v2: 1853 Elo** (Opus 5 1824, Fable 5 1723, Sol 1711) — the
  knowledge-work lead this file has consistently attributed to Claude both
  holds and extends. On AA's newer v2.1 the comparable pairing is 1735 vs
  Astra's 1542.
- **AA-Briefcase: 1694 Elo**, +122 over Fable 5; v1.1 reads 1678 vs Astra's
  1569.
- OSWorld 2.0: 77.9% partial / 41.7% strict (Opus 5: 75.4% / 39.6%).
  Humanity's Last Exam 60.9% no-tools, 65.0% with tools. AutomationBench
  31.4% (Opus 5 26.9%). CursorBench 3.2.0 73.4% (Opus 5 70.0%, Fable 5
  70.5%, Sol 67.2%). SciCode 62.0%. LiveCodeBench 90.52%, first place.
- **Terminal-Bench numbers conflict by harness:** Anthropic's own table
  gives Fable 5.1 55.8% on Terminal-Bench 4.0 (Mythos 60.9%, Opus 5 52.3%,
  Fable 5 42.0%, Sol 37.3%), while AA measures 52% on its harness and 91.4%
  on the older Terminal-Bench 2.1. Three different tests; don't average them.
- **Calibration got worse while accuracy got better.** AA-Omniscience
  accuracy 67.2% at a 93.4% attempt rate — of the questions it did not get
  right, it attempted 72.6% rather than declining, up from Fable 5's 63.6%.
  This is the same failure shape already flagged for Opus 5 below, so
  **apply the verify-factual-claims habit to Fable 5.1's output too,
  including the main session's own when it is the model in the chair.**

**Practitioner-reported caveats (community reports, not benchmarks — weigh
accordingly, but they bear directly on delegation):**
- **Token hunger is the consistent complaint.** Reports range from 25–50%
  above Fable 5 to 3x; AA measures ~1.7x output tokens and a cost per index
  task of $3.76 (max) / $2.72 (xhigh) against Fable 5's $3.14. It
  reportedly prefers rewriting a file over editing it and spawns more
  subagents than asked. On subscription tiers this burns allocation faster
  than the per-token price cut suggests.
- **Over-eager helpfulness:** unsolicited "additional helpful edits"
  outside the requested scope — precisely the scope creep the light-touch
  tier's diff scan exists to catch. **Keep the scope/byte-verification step
  even at light tier for Fable 5.1 lanes.**
- **The genuine praise is code reduction**: reported as the first model
  that reliably simplifies and deletes code, and that stays readable across
  long multi-step tasks. Also reported to catch and correct its own
  mistakes well, and to orchestrate subagents without degrading them.
- Anthropic's own safety notes: less evaluation visibility into very
  long-context and multi-agent settings, and it "can still sometimes bypass
  approvals and auto-mode classifiers." Occasional classifier punts to Opus
  4.8 are reported, which is a prompt-injection surface in agentic runs.

**Independent verification (Artificial Analysis, checked 2026-07-25):**
this isn't just Anthropic's own framing — AA, which evaluates all labs
through the same harness, independently found Opus 5 (max effort) narrowly
the single most intelligent model on their Intelligence Index (61, edging
out Claude Fable 5 at 60, GPT-5.6 Sol at 59 — **on index v4.1.1 as of
2026-08-14 these read 63 / 62 / 61, with Grok 4.6 also at 61; the ordering
holds, the absolute numbers shifted**), the new leader on both
GDPval-AA v2 (1861 Elo) and AA-Briefcase (1720 Elo) agentic knowledge-work
benchmarks, and **joint first place on AA's separate Coding Agent Index**
(DeepSWE + Terminal-Bench v2 + SWE-Atlas-QnA composite), with the highest
score of any model on the SWE-Atlas-QnA component specifically. One
tempering note from the same source: Opus 5's hallucination rate rose to
50% (+14 points over Opus 4.8) as it answers more often when uncertain —
worth weighing for tasks where a confident wrong answer is costly.

### Current generation (AA harness, Intelligence Index v4.3.2 era)

Added 2026-09-20. **These rows are not comparable to the older table below**
— Terminal-Bench 4.0 replaced 2.1, AutomationBench-AA replaced τ³-Banking,
and GDPval-AA moved v2 → v2.1. Blank cells are missing data, not zero; AA
has not re-run every older model on every new evaluation.

| Benchmark (AA, current) | Fable 5.1 | GPT-6 Astra | Opus 5 | GPT-5.6 Sol |
|---|---|---|---|---|
| AA Intelligence Index (v4.3.2, max) | **53** | **53** | not re-run | 47 |
| AA Coding Agent Index | **62** | **62** | 60 | 55 |
| Terminal-Bench 4.0 | 52% | **59%** | 52.3%◇ | 37.3%◇ |
| AutomationBench-AA | 59% | **68%** | not published | not published |
| GDPval-AA v2.1 (Elo) | **1735** | 1542 | not published | not published |
| AA-Briefcase v1.1 (Elo) | **1678** | 1569 | not published | not published |
| SciCode | **63%** | 56% | not published | not published |
| Humanity's Last Exam | **59%** | 55% | not published | not published |
| GDP.pdf | 26% | **31%** | not published | not published |
| CritPt | 30% | **32%** | not published | not published |
| AA-Omniscience (score) | 43 | 43 | not published | not published |
| AA-LCR v1.1 | **85%** | 81% | not published | not published |
| Hallucination / attempt-when-wrong | 72.6%◆ | 51% | 50%◆ | 92% |
| Price per MTok (in/out) | $10/$50 | $10/$50 | $5/$25 | $5/$30 |
| Cost per AA index task (max) | $7.63 | **$3.26** | not published | not published |
| Output speed | 70 tok/s | 59 tok/s | not published | not published |

◇ Opus 5's and Sol's Terminal-Bench 4.0 figures come from **Anthropic's**
Fable 5.1 launch table, not AA's harness — same benchmark name, different
runner, so read them as directional against AA's column rather than
head-to-head.

◆ Three different shapes of the same worry, not one metric: Astra's and
Sol's figures are AA-Omniscience *hallucination rates*; Fable 5.1's 72.6%
is its *attempt rate on questions it got wrong* (up from Fable 5's 63.6%,
i.e. worse calibration); Opus 5's 50% is AA's July measurement on an earlier
revision. All four say the same practical thing — **verify factual claims
from every model in this table** — and none of them can be ranked against
each other.

**Other v4.3.2 index scores known (no per-eval breakdown on AA yet):**
Grok 4.7 (xhigh) 46, Grok 4.6 (high) 44 — see the Cursor section. Added
2026-10-19: Claude Sonnet 5.5 (max) 56, Gemini 4 Argon (high) 53, Kimi K3
44, Claude Haiku 5.5 (max) 43, GPT-6 Luna (max) 38.

**The one-line read:** Astra and Fable 5.1 are level on the composite and
on coding, and they split cleanly by task shape. **Astra leads on
terminal/automation/document-reasoning work at roughly 40% of Fable 5.1's
cost per task; Fable 5.1 leads on knowledge work, science, long-context
recall and reasoning breadth.** Route by which of those a lane actually is,
not by which model is "better."

### Claude 5.5 family (added 2026-10-19) — confidence: vendor claims plus early independent

Opus 5.5 (2026-09-22), Sonnet 5.5 (2026-09-28) and Haiku 5.5 (2026-10-07),
all GA on the API, Bedrock, Vertex and Foundry. Opus 5 and Sonnet 5 are now
legacy.

| | Opus 5.5 | Sonnet 5.5 | Haiku 5.5 |
|---|---|---|---|
| Terminal-Bench 4.0 | 66.4% (vendor; Google's Argon table shows the same figure) | 70.6% max (vendor, unverified) / 64% max (AA) | 29% xhigh (AA) |
| AA Intelligence Index | not found | **v4.3.2: 56 at max** (AA page; "max with fallback" config); 47 high (secondary) | **v4.3.2: 43 at max** (AA page) |
| Other | FrontierCode v1.1 54.4 vs Astra 53.3; GDPval-AA v2.1 1846 vs Astra 1542; Terminal-Bench-Science 58.7 vs Astra 64.6 (all vendor) | SWE-Bench Pro 81.3 (vendor, secondary); AA Coding Agent Index 68 (secondary) | no vendor coding numbers found |
| Price /MTok | $4 / $20 | $2 / $10 | $0.10 / $0.50 (prompts up to 100K) |

- Anthropic places Opus 5.5 at roughly Fable 5.1's level on most tasks, at
  well under half Fable 5.1's per-token price, and Sonnet 5.5 within about
  2 points of Opus 5.5 on coding.
- Sonnet 5.5's v4.3.2 composite (56) is above Fable 5.1 and Astra (53).
  Its reported AA Coding Agent Index of 68 (secondary) would also lead the
  table above (62), but that figure is not on its AA page: confirm it
  before routing on it.
- Haiku 5.5 uses a newer tokenizer (about 30% more tokens than Haiku 4.5
  for the same text), so compare cost per task, not per token.
- For review tiering with Claude as reviewer: Opus 5.5 as finder and
  Sonnet 5.5 as verifier is now the cheaper equivalent of the earlier
  Fable/Opus pairing.

---

### Previous generation (Anthropic launch table + AA index v4.1.1)

Kept for the models it covers — Luna, Gemini 3.7 Flash and Grok 4.6 have no
rows in the current table yet. Its Intelligence Index column is **v4.1.1
and cannot be read against the 53/53/47 figures above.**

Per Anthropic's own launch benchmark table (vendor-reported, internal
harness — treat as directional, not independently audited), plus published
figures for Gemini 3.7 Flash and Grok 4.6 where genuinely
cross-vendor-comparable data exists (GDPval-AA v2 and DeepSWE are Artificial
Analysis benchmarks multiple vendors report against; Terminal-Bench 2.1 is a
shared external benchmark, not vendor-specific). Two columns were swapped on
2026-08-14: Gemini 3.6 Flash → **3.7 Flash**, and **Grok 4.6 added** since
Cursor/Grok is one of the four agents this file covers.

| Benchmark | Opus 5 | Opus 4.8 | GPT-5.6 Sol | GPT-5.6 Luna | Gemini 3.7 Flash | Grok 4.6 |
|---|---|---|---|---|---|---|
| Agentic terminal coding (Frontier-Bench v0.1) | 43.3% | 21.1% | 34.4% | not published | not published | not published |
| Agentic coding (DeepSWE v1.1) | 68.8% | 59.0% | **72.7%** | 67.2% | 65.3% | 65.9% |
| Agentic coding (FrontierCode v1.1) | 53.4% | 46.5% | 47.5% | not published | 43.6%§ | 61.3%§ |
| Terminal-Bench 2.1 | 89%† | not published | ~89%† | 84.7% | 85.8% | 88.4% |
| Terminal-Bench 3.0 | not published | not published | not published | not published | 14.9% | gap, no figure |
| Knowledge work (GDPval-AA v2, Elo) | **1861** | not published | 1728 | not published | 1525 | 1753 |
| Computer use (OSWorld 2.0 / OSWorld-Verified*) | 70.6% | 55.7% | 62.6% | not published | 38.1% | not published |
| Novel problem-solving (ARC-AGI-3) | 30.2% | 1.5% | 7.8% | not published | not published | not published |
| Business workflows (AutomationBench) | 26.0% | 17.0% | 18.1% | not published | leads AA variant‡ | not published |
| AA Intelligence Index (v4.1.1) | **63** | not re-run | 61 | not published | 56 | 61 |

† Opus 5's 89% and GPT-5.6 Sol's "roughly in line" figure are both from
Artificial Analysis's independent write-up (max/xhigh effort), not from
Anthropic's own launch table. Treat Sol's figure as approximate ("~89%")
since AA described it as roughly in line with the leader rather than giving
an exact number in the passage available.

§ **FrontierCode variants differ:** Gemini's 43.6% is on FrontierCode v1.1
**Main**; Grok's 61.3% is on v1.1 **Extended**; the Claude/OpenAI column
figures are Anthropic's v1.1 reporting. These are not a clean like-for-like
row — do not read Grok as ~18 points better than Gemini here.

‡ Gemini 3.7 Flash leads AA's **AutomationBench-AA**, which is AA's own
variant, not the AutomationBench figure Anthropic reports. Separately, it
holds the **best score of any model on AA-AnalystAgent (60% pass^5, vs Opus
5's 54% and Fable 5's 49%)** — a document/spreadsheet reasoning benchmark
with no Claude-table equivalent, so it doesn't get a row, but it's the one
place a non-Claude agent in this file outright leads the frontier.

\* **Not a like-for-like comparison** — Anthropic's OSWorld 2.0 and Google's
older OSWorld-Verified are different harnesses. Gemini 3.7 Flash's 38.1% is
on OSWorld 2.0 per Google's own newer table, which *is* comparable to
Anthropic's column, and it trails badly. Blank cells throughout are missing
data, not zero: Google and xAI haven't run Anthropic's Frontier-Bench or
ARC-AGI-3, and Luna's blanks reflect OpenAI not running Anthropic's evals.

**What changed with these two swaps — read this before picking a tier.**

**Gemini closed most of the coding gap.** The previous entry's headline was
that 3.6 Flash trailed every Claude/OpenAI model on DeepSWE by a wide margin
(49% vs 68.8%/72.7%/67.2%/59.0%). **3.7 Flash at 65.3% now lands between
Opus 4.8 and Opus 5, and roughly level with Luna and Grok 4.6** — a ~16
point generational jump that makes it a plausible substitute for hard coding
delegation rather than a computer-use specialist only. The tradeoff moved
too: computer use went from its best claim (OSWorld-Verified 83.0%, ahead of
Sonnet 5) to its worst (OSWorld 2.0 38.1%, trailing Terra), and it still
trails everything in this table on knowledge work (GDPval-AA v2 1525).
**Delegate coding and document analysis to it; don't delegate computer-use
or broad knowledge work.**

**Grok reached the frontier cluster on the composite, but not on hard
coding.** Grok 4.6's AA Index 61 ties GPT-5.6 Sol and sits 2 points behind
Opus 5, and its GDPval-AA v2 1753 is second only to Opus 5's 1861 — a
tighter knowledge-work gap (108 Elo) than Gemini's (336). But on DeepSWE it
remains 4-7 points behind Sol and Fable 5, so **index parity should not be
read as coding parity.** Its distinctive value is cost: frontier-adjacent
results at $2/$6 per MTok.

**Opus 5 still leads where it led.** On the benchmarks Anthropic runs and
others don't (Frontier-Bench, ARC-AGI-3, AutomationBench) there's no
comparison to make, and on the ones that are shared it leads GDPval-AA v2
outright and holds the top of the AA Index. The honest summary is that the
gap narrowed on coding from both directions this month while Claude's leads
on knowledge work, computer use, and novel problem-solving held.

**Where Claude (Opus 5) is clearly strongest, per this table and
reporting** — with the 2026-09-20 caveat that **Fable 5.1 now exceeds Opus
5 on most of these** (Coding Agent Index 62 vs 60, GDPval-AA v2 1853 vs
1824, Terminal-Bench-Science 52.6% vs 29.0%, OSWorld 2.0, AutomationBench,
CursorBench). Read the list below as "where the Claude line leads," and
substitute Fable 5.1 as the specific model wherever the main session is
running it:
- Agentic terminal coding and computer use — Opus 5 leads both by wide
  margins over both its own predecessor and GPT-5.6 Sol
- Novel/out-of-distribution problem-solving (ARC-AGI-3) — a large gap here,
  3x the next-best model per Anthropic
- Self-verification and iterating on its own work until it succeeds —
  Anthropic specifically highlights this as the generational change, not
  just a benchmark bump; documented examples include building its own
  verification tooling when none was provided
- Business workflow automation, end-to-end
- Knowledge work broadly — GDPval-AA v2 remains Opus 5's clearest lead over
  every agent here: +336 Elo over Gemini 3.7 Flash and +108 over Grok 4.6,
  the largest consistent margin of any directly-comparable row
- Coding depth relative to Gemini specifically — still ahead (DeepSWE 68.8%
  vs 65.3%, Terminal-Bench 2.1 89% vs 85.8%), **but the margin collapsed
  from ~20 points to ~3.5 with the 3.7 Flash release**; this is no longer a
  strong reason on its own to keep coding work in-session

**Where Claude (Opus 5) is a known weak point — worth applying to Claude's
own output, not just delegated agents':** hallucination rate rose to 50%
per AA's independent measurement, as it answers more often instead of
declining when uncertain. This is a reason for extra scrutiny on factual
claims (library APIs, version numbers, citations) from Opus 5 output
specifically, separate from the coding-review-tier logic above — a
confident wrong answer here is a real failure mode, not just a
theoretical one.

**Where the gap to Codex (GPT-5.6 Sol) narrows or reverses:**
- **DeepSWE v1.1 — GPT-5.6 Sol actually leads outright** (72.7% vs 68.8%),
  the one clear agentic-coding row where Codex's current flagship wins.
  This is real signal that Codex/Sol shouldn't be assumed weaker across the
  board on coding specifically.
- FrontierCode v1.1 is close (53.4% vs 47.5%) — a real but modest edge for
  Claude, not a large gap
- **DeepSWE v1.1, Luna specifically — the gap to Opus 5 is real but not
  huge** (67.2% vs 68.8%, ~1.6 points) at roughly 1/25th the per-token
  cost, and Luna beats Opus 4.8 outright (67.2% vs 59.0%). This is the
  strongest case in the table for routing narrow, well-scoped coding work
  to Luna rather than reflexively to Claude or Sol.
- Raw speed/cost for simple, well-scoped tasks — Codex's Luna tier and
  Antigravity's Flash-tier models are built to be faster/cheaper than Opus
  5 for tasks that don't need deep reasoning, a legitimate reason to
  delegate even when Claude could do it

**Where the gap to Codex closes entirely — GPT-6 Astra (added
2026-09-20).** This is the largest single change to this file since it was
written. Astra is the first delegate here to reach parity with the top of
the Claude line rather than trailing it:
- **Dead level on both composites** — AA Intelligence Index 53 vs Fable
  5.1's 53, Coding Agent Index 62 vs 62, and both ahead of Opus 5's 60 on
  coding. "Delegate because Claude is busy, not because Claude is better"
  is now a defensible framing for Astra lanes.
- **Astra leads outright** on Terminal-Bench 4.0 (59% vs 52%),
  AutomationBench-AA (68% vs 59%), GDP.pdf (31% vs 26%) and CritPt — i.e.
  terminal work, business-process automation and document reasoning. Note
  the reversal: terminal/agentic coding was Claude's signature lead in the
  July version of this file.
- **At ~40% of the cost per task** ($3.26 vs $7.63) and roughly a third of
  the output tokens. Cost is no longer the reason to prefer a weaker
  delegate; it is now a reason to prefer Astra over the in-session model
  for lanes in its zone.
- **Claude keeps knowledge work, science and reasoning breadth** —
  GDPval-AA v2.1 1735 vs 1542, AA-Briefcase 1678 vs 1569, SciCode 63% vs
  56%, HLE 59% vs 55%, AA-LCR 85% vs 81%, and Terminal-Bench-Science 52.6%
  with no Astra figure to compare. Astra actually regressed ~45 Elo on
  GDPval versus Sol, so this gap *widened* on Astra's side.
- **The counterweight is procedural, not capability.** Astra's reduced
  chain-of-thought monitorability and its 2/500 supply-chain-attack rate in
  a controlled eval (see the Codex section) mean its output needs a
  different *kind* of review, not a deeper one: audit diffs and tool
  results rather than transcripts, and never shortcut dependency changes.

**Where the gap to Antigravity (Gemini 3.7 Flash) narrows or reverses:**
- **Document and spreadsheet analysis — 3.7 Flash leads outright**
  (AA-AnalystAgent 60% pass^5 vs Opus 5's 54%). The clearest reversal in
  this whole file, and a genuine reason to delegate that class of work.
- **Web/UI generation** — WebDev Arena 1588 Elo, ahead of Sonnet 5's 1541.
- Agentic coding — the DeepSWE gap is now ~3.5 points, small enough that
  cost should usually decide.
- Long-context recall and multimodal reasoning — still a Gemini strength
  (1M context), though CharXiv regressed slightly from 3.6 Flash.
- Raw speed/cost — 340 tok/s and $0.75/$3.75 per MTok through 2026 makes
  this the cheapest fast option among the four agents; note the price
  doubles Jan 1, 2027.
- **Reversed since last revision:** computer use is no longer a Gemini
  advantage. 3.6 Flash's OSWorld-Verified 83.0% was a documented strength;
  3.7 Flash reports 38.1% on OSWorld 2.0, well behind Opus 5's 70.6%.

**Where the gap to Cursor (Grok 4.6) narrows or reverses:**
- **Knowledge work is close** — GDPval-AA v2 1753 vs Opus 5's 1861 makes
  Grok 4.6 the nearest challenger on Claude's strongest dimension, at ~a
  third of the cost. This is new; Grok 4.5 was not in this conversation.
- **Terminal-Bench 2.1 is effectively level** (88.4% vs 89%).
- **AA Intelligence Index is within 2 points** (61 vs 63) — index parity
  with GPT-5.6 Sol, at $2/$6 per MTok.
- **Still behind on hard agentic coding** — DeepSWE 65.9% vs Opus 5's 68.8%
  and Sol's 72.7%, and Terminal-Bench 3.0 is an acknowledged gap.
- **Calibration is no longer the disqualifier it was** — non-hallucination
  rate 65.7%, a real improvement over 4.5's 54% hallucination rate, though
  still worse than Claude's own 50% figure below.
- **Grok 4.7 (added 2026-09-21) widens the gap on the current index rather
  than closing it**: 46 vs Fable 5.1's 53 on v4.3.2, and Terminal-Bench 4.0
  at 26–38% (AA vs xAI) against Fable 5.1's 52–58%. It stays closest to
  Claude on legal and knowledge work (AA-Briefcase v1.1 1657 vs 1678, per
  xAI) at a fifth of Fable 5.1's input price and an eighth of its output
  price — but at ~2.5x 4.6's output tokens, so compare cost per task, not
  price per token.

**Practical implication for review-tier decisions:** if a delegated task
lands in a zone where Codex or Antigravity's documented strength roughly
matches or exceeds Claude's own on these tables — e.g. DeepSWE-style
agentic coding for Codex's Sol tier, or anything terminal/automation-shaped
for Astra — that's real support for a light-touch review.
If it lands in a zone where Claude's own strength clearly leads (terminal
coding, computer use, novel/out-of-distribution problems, long-horizon
self-verification), lean toward the fuller adversarial review — the
delegated agent is more likely working outside its best zone precisely
where Claude would have had an edge.

---

## Updating this file

When a delegated task's outcome surprises you — a "strong zone" task came
back wrong, or a "weak zone" task came back solid — note it here with a
date and one line of context. That's what keeps this calibrated instead of
a one-time guess. If it's been a while since "Last researched" above, or the
user mentions a model name not listed, re-search before trusting this file
for a consequential handoff.
