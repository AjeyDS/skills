# Research Notes — Goal-Anchored Delegation

Compiled 2026-08-12. Read when justifying a design choice; not needed for
routine use. Each claim below is load-bearing for a specific rule in
SKILL.md.

## 1. The gap in existing stacks is real, not assumed

Superpowers' `writing-plans` explicitly instructs the planner to write for
an executor assumed to have zero codebase context and questionable taste —
a deliberately low-trust executor model. Its pipeline (brainstorm → design
doc → plan → subagent-driven execution with per-task review) passes the
*plan* downstream; the user's goal lives only in the upstream brainstorm
session and is not restated in executor prompts. mattpocock/skills
(grilling, to-prd, to-issues, TDD, handoff — the pack several of the
user's installed skills come from) enforces process discipline but
likewise hands executors work items, not intent.
Sources: github.com/obra/superpowers (writing-plans, executing-plans
SKILL.md), deepwiki.com/obra/superpowers, claude.com/plugins/mattpocock-skills.

## 2. Heterogeneous planner/executor pairs outperform homogeneous ones

- An empirical study of planning representations for LLM web agents found
  mixed planner–executor pairs generally outperform homogeneous setups,
  and that separating the roles reveals complementary model strengths;
  plan *representation* also materially affects the executor
  (checklist vs prose vs pseudocode suits different model families).
  → supports cross-vendor pairing; also a reason the Goal Card is short
  prose (portable across model families) while the plan can be structured.
  Source: arxiv.org/pdf/2605.29927.
- "Specialize Roles, Mix Deployments" (arxiv.org/pdf/2606.20629) extends
  plan–execute to planner/verifier/executor and finds three heterogeneous
  agents the strongest configuration. Its verifier design note is the
  origin of our critique rule: because self-correcting LLMs over-flag
  false issues (Self-Refine literature), the verifier defaults to
  approving unless it finds a concrete defect.
- Cross-vendor review value: different models have measurably different
  vulnerability/defect detection profiles shaped by training, so
  single-model pipelines compound the same bias at generation and review;
  a different model's training distribution provides epistemic diversity
  manifesting as complementary blind spots (LLM Consortium controlled
  experiment, arxiv.org/pdf/2606.01490; MindStudio cross-vendor review
  analysis; liatrio-labs model-routing research survey — which also
  cautions the field has more practitioner intuition than rigorous
  published evidence, so treat as directional).

## 3. Goal drift in long sessions is documented

- "Telephone game" effect: across long sessions an agent's internal goal
  representation mutates incrementally; in logged multi-day runs drift
  became apparent around the two-hour mark, with agents inventing
  unrequested subtasks or rewriting working code from hallucinated
  requirements (sitepoint.com 13-day agent guide, citing Simon Last's
  logged sessions).
- Mechanism: pattern-matching inertia and token-position bias — early
  instructions remain textually present but their effective influence
  decays as context grows; session resumes/compactions reconstruct stale
  intent (tianpan.co intent-drift analysis; Zylos long-horizon goal
  persistence survey: each restart is a degradation opportunity, and
  aggressive subgoal optimization drifts from parent intent).
- "Asymmetric Goal Drift in Coding Agents Under Value Conflict"
  (ICLR 2026, arxiv.org/pdf/2603.03456): agents drift more readily from
  constraints opposing their trained values, under environmental pressure
  from the codebase itself. Implication: a written goal restated at
  checkpoints is an external anchor; also, don't assume the executor's
  compliance is uniform across constraint types.
- → these motivate: Goal Card written from the user's ask (not post-hoc),
  copied verbatim (not paraphrased — paraphrase is the telephone game),
  and re-read at checkpoints/compaction/resume.

## 4. Peer-tier pairing candidates are genuinely peer-tier (as of Aug 2026)

- Kimi K3 (Moonshot, 2.8T MoE, 1M context): AA Intelligence Index 57.1 —
  #4 configuration, behind Claude Fable 5 (59.9) and GPT-5.6 Sol max
  (58.9), above Opus 4.8 (55.7) and Grok 4.5 (53.8). Across ~14 shared
  benchmarks Fable 5 wins ~8, K3 wins ~6 including long-horizon agentic
  coding, Terminal-Bench 2.1 (88.3 vs 84.6) and SWE Marathon. Caveats:
  Moonshot's launch table mixes harnesses (Kimi Code / Claude Code /
  Codex), several results lacked independent reproduction at launch, and
  Semgrep measured weak grounded security reasoning on its largest
  enterprise-scale repo (~6% F1) — so K3-as-peer-executor holds for
  coding/agentic tasks, weaker for large-repo security judgment.
  Sources: kimi.com/blog/kimi-k3, Artificial Analysis via kingy.ai and
  bleap.finance reviews, nxcode.io benchmark guide, semgrep.dev.
- Harness sensitivity is large (e.g. 17–26 pt SWE-bench spreads between
  vendor scaffold and standardized harness for Opus 4.8 / Gemini 3.1
  Pro) — one more reason autonomy grade should key off the model *and*
  task shape, and why surprises should be logged back into
  external-agent-delegation's capability notes rather than trusted as stable.

## 5. What this file deliberately does not claim

No published study tests "goal prose in executor prompt" as an isolated
intervention; that specific mechanism is a design synthesis of §1–§3, not
a measured result. Log outcomes (deviation notes accepted vs rejected,
goal-critique findings that were real vs noise) to build local evidence.
