---
name: goal-anchored-delegation
description: Layer skill that propagates the user's GOAL (not just the plan) into every plan, design doc, and executor handoff, and grades how much freedom the executing agent gets. Use whenever a plan/spec/handoff doc is being written for another agent or session to execute (Superpowers writing-plans, mattpocock to-prd/to-issues, external-agent-delegation handoffs, or any plan→execute split); whenever planner and executor are different models — especially peer-capable ones from different vendors (e.g. a Claude model planning while a GPT, Kimi or Grok model executes); whenever an executor hits a blocker the plan doesn't cover, wants to deviate, or suggests a plan change; when reviewing a finished plan against what the user originally asked for; or when a long planning session risks drifting from the original goal. Trigger even if the user only says 'add the goal to the handoff', 'let the executor push back', or 'check this plan against what I actually wanted'.
license: MIT
compatibility: Any agent. Pairs with plan-writing skills (e.g. superpowers writing-plans) and with external-agent-delegation.
metadata:
  author: AjeyDS
  version: '1.0'
---

# Goal-Anchored Delegation

A layer on top of any plan→execute workflow (Superpowers, mattpocock
skills, `external-agent-delegation` handoffs). It fixes one structural gap:
those stacks pass the **plan** downstream but not the **goal**, and they
assume a low-trust executor ("zero context, questionable taste"). Correct
for weak executors; wasteful when the executor is a peer-capable model
with a different training distribution, whose divergent POV is signal.

Two mechanisms: (1) a **Goal Card** that travels with every plan and
handoff, (2) an **autonomy grade** for the executor keyed to capability
parity. Research grounding lives in `references/research-notes.md` — read
it when you need to justify a design choice, not routinely.

## The Goal Card

A short block written at planning time, placed at the top of the plan and
copied verbatim into every executor handoff doc:

```
## Goal Card
Goal: <1–3 sentences of the user's actual objective, in prose>
Principles: <optional, 2–4 bullets — how to decide when the plan is
  ambiguous or wrong, e.g. "correctness over speed", "no new deps">
Non-goals: <optional, 1–2 bullets — what NOT to optimize or expand into>
Autonomy: <peer | sub-tier — see grading below>
```

Rules:
- **Written from the user's ask, before/during planning — never derived
  from the finished plan.** Deriving it post-hoc launders plan drift into
  the goal. If the user's ask is vague, ask them one clarifying question
  rather than inventing intent.
- Prose, not a spec. It carries *why*, the plan carries *what/how*.
- Principles earn their place only when a real decision fork exists.

## Grading executor autonomy

Key the grade off capability parity between planner and executor models —
check the capability notes kept by `external-agent-delegation` if
available, or current independent benchmarks (Artificial Analysis) if not:

- **Peer** (executor within roughly one tier of the planner, e.g. a
  frontier Claude model plans and a frontier GPT, Kimi or Grok model
  executes):
  *adapt-and-advise* license. May adapt implementation details when the
  plan conflicts with repo reality, must log every deviation with a
  one-line justification, and is explicitly invited to flag loopholes
  and suggest plan improvements against the Goal Card.
- **Sub-tier** (executor clearly weaker, e.g. a vendor's small or
  "lite" tier):
  *flag-only* license. Follows the plan; when blocked or when something
  looks wrong, stops and escalates — no improvisation.
- Cross-vendor peer pairs are the high-value case: different training
  distributions produce complementary blind spots, so a peer executor's
  objection is evidence, not insubordination.
- Either way: **scope is never self-expanded.** Freedom covers *how*
  within the plan's scope, never *what*.

State the grade in the Goal Card and in the kickoff message, so the
executor knows its license explicitly instead of guessing.

## Escalation protocol (for the executor)

When the plan meets a blocker or looks wrong:

1. Check the Goal Card. If the plan step contradicts the goal or
   principles, that's an escalation, not a workaround.
2. Peer executors may locally adapt *how* (log it); anything touching
   scope, interfaces other tasks depend on, or the goal itself goes back
   to the planner as a short **deviation note**: what was planned, what
   was found, proposed change, which Goal Card line motivates it.
3. Never silently rewrite scope, and never push a branch whose deviations
   aren't logged — an unlogged deviation converts a light-touch review
   into a full adversarial one (see `external-agent-delegation`).

## Goal-critique step (for the planner)

Run twice: after the plan is drafted, and after execution lands.

- Critique the artifact **against the Goal Card, not against the plan** —
  checking a plan against itself always passes.
- **Default to approve unless there is a concrete, nameable defect.**
  LLM critics over-flag; vague unease is not a finding. A finding names
  the Goal Card line violated and the artifact section violating it.
- Findings → planner patches the plan (or hands the patch decision to the
  user if it changes scope). Executor deviation notes and suggestions get
  adjudicated here too: accept into the plan, or decline with a one-line
  reason back to the executor.

## Anti-drift anchor (for the planner itself)

Long planning/orchestration sessions drift: the goal representation
mutates incrementally while the original wording sits inert in early
context. Countermeasure: re-read the Goal Card aloud (restate it in the
session) at every checkpoint — before dispatching each handoff, after any
context compaction/resume, and whenever the session pivots. If the
current direction no longer traces to a Goal Card line, stop and
reconcile with the user before proceeding.

## Layering on existing stacks

- **Superpowers**: Goal Card goes at the top of the brainstorm design doc
  and the `writing-plans` output; the plan-document-reviewer critique gets
  the Goal Card as an extra input; `executing-plans` / subagent prompts
  get the Card + autonomy grade prepended.
- **mattpocock skills**: Goal Card feeds `to-prd` as the north-star
  paragraph and rides along into `to-issues` output (one Card shared
  across the issue set); `grill-me` is a good generator for Principles.
- **external-agent-delegation**: Goal Card is a required section of each
  handoff file in `docs/plans/`; autonomy grade derives from its
  capability notes; deviation notes feed the review-tier
  decision and surprise log.
