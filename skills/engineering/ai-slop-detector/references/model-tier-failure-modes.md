# Model-tier failure modes

Read this before reviewing a specific agent's output, or when deciding how hard
to review at all.

**Contents**
1. [The core asymmetry](#the-core-asymmetry)
2. [Signature A: surface slop](#signature-a-surface-slop-small--non-reasoning-models)
3. [Signature B: structural slop](#signature-b-structural-slop-frontier--reasoning-models)
4. [Signature C: accretion slop](#signature-c-accretion-slop-any-model-in-an-agentic-loop)
5. [What does not vary by tier](#what-does-not-vary-by-tier)
6. [Review depth table](#review-depth-table)

---

## The core asymmetry

Capability does not reduce defects. It changes their shape, and it moves them
from cheap-to-detect to expensive-to-detect.

The measured pattern is a *reasoning-complexity trade-off*: as models get more
capable, they produce more bloated and more tightly coupled code, not less.
Weaker models score better on some length-based smell metrics for the wrong
reason — they fail before producing enough code to trip the threshold. A model
that writes nothing writes nothing bloated.

The practical inversion this creates:

> The better the model, the more professional the slop looks, and the less
> likely a cosmetic review is to catch it.

Frontier output has type hints, docstrings, consistent naming, structured error
handling, and passing tests. Every signal a comment-and-naming checklist looks
for comes back clean. The defect is in the shape of the design, which only shows
up in graph-level measurement or careful reading of the top-ranked hotspots.

So the rule is not "review strong models less." It is "review them for different
things."

---

## Signature A: surface slop (small / non-reasoning models)

**What it looks like**

- Copy-paste with light variation instead of parameterising
- Helpers reimplemented inline rather than extracted or imported
- Comments that restate the function name (`# Create parser` above
  `create_parser`)
- Hollow performance claims with no measurement backing them
- Filler adjectives in docs: seamless, robust, powerful, enterprise-grade
- Under-engineering: plausible code that does not handle the real cases
- Historically the highest package-hallucination rates

**Why it happens**

Weaker pattern completion with less capacity to hold the existing codebase in
mind. The model reaches for the shape of a solution it has seen rather than the
one this repo already has.

**How to catch it**

Almost entirely mechanical. Clone detection, linters, and grep get most of it.

```bash
jscpd . --min-tokens 50 --mode weak
# comment noise, once the structural work is done:
grep -rnE '(^|[[:space:]])#[[:space:]]*(Create|Handle|Process|Initialize|Setup|Enable) ' --include='*.py' .
grep -rniE '\b(optimized|blazing|seamless|robust|enterprise-grade|production-ready)\b' --include='*.md' .
```

**Cost profile:** high volume, low individual severity, cheap to detect, cheap
to fix. Do not let its visibility consume the review budget.

---

## Signature B: structural slop (frontier / reasoning models)

**What it looks like**

- **Long Method / procedural bloat.** The model handles every edge case it can
  think of, and puts all of it in one procedural block. Measured: a 480B-class
  model produced 11 long-method violations on a task set where the human
  baseline produced 1.
- **God class.** Logic centralised into a `Manager`/`Handler`/`Service` class
  that responds to everything, rather than delegated.
- **Modular mirage.** The single most useful concept here. The agent splits code
  into many files — structural modularity — without achieving semantic cohesion.
  Related behaviour ends up scattered across the tree. It *looks* well
  organised. Directory listings look great. Nothing that belongs together lives
  together.
- **Speculative generality.** Abstractions, config hooks, strategy interfaces,
  and plugin points built for requirements that do not exist. Each is defensible
  in isolation, which is what makes it hard to push back on.
- **Redundant reimplementation.** Rewriting invocation logic inline at each call
  site instead of encapsulating it — copy-paste style expressed through a
  competent model.
- **Unstable dependency.** Modules depending on things that change more often
  than they do.

**Why it happens**

Comprehensiveness is rewarded. A more capable model generates a more thorough
solution, and thoroughness expressed without architectural restraint is volume.
It is also genuinely hard: keeping a coherent architectural vision across a
growing system is the thing current agents are worst at. They behave like
capable junior developers — precise instruction-following, no senior-architect
foresight about system-wide consequences.

**Why prompting does not save you**

This is the counterintuitive part and worth internalising. In controlled
comparisons, structured few-shot prompting with explicit coding standards did
**not** reduce long-method violations — it increased them (11 → 13 for one
model, 5 → 8 for another). Increasing requirement specificity across four
escalating prompt stages had no statistically significant effect on any smell
category (p > 0.8). The hypothesised mechanism: extra context reads as a request
for a more comprehensive solution.

So a better-written skill or a more detailed CLAUDE.md is not sufficient. It is
worth doing, and it is not a control. Measurement is the control.

**How to catch it**

Mechanical detection gets you to the shortlist; reading closes it.

```bash
python3 scripts/slop_scan.py scan . --entry <module>   # hotspots, orphans, connectivity
lizard . -C 10 -a 5                                     # complexity + arity
```

Then read the top hotspots and ask, in this order:

1. **Does this abstraction have two real callers today?** One caller plus a
   hypothetical is speculative generality. Inline it.
2. **Did this reimplement something that exists?** Search for the operation, not
   the name the agent chose. Falling internal-import density is the tell.
3. **Do these files represent responsibilities, or just size?** If moving one
   function requires touching four files, the split was cosmetic — modular
   mirage.
4. **Which of these branches came from a real requirement?** Edge-case handling
   for cases that cannot occur is the most common form of frontier bloat.

**Cost profile:** low volume, high individual severity, expensive to detect,
expensive to fix. This is where review budget belongs.

---

## Signature C: accretion slop (any model, in an agentic loop)

The failure mode that matches "my codebase keeps getting bigger." It is not a
property of a single generation; it is a property of iteration.

**What the measurements show**

Benchmarking coding agents across long-horizon tasks — where the agent
repeatedly extends its own prior solution under evolving specs — found:

- Verbosity rose across roughly three-quarters to nine-tenths of trajectories;
  structural erosion across roughly 77-80%. Direction was consistent across
  every model tested.
- High-complexity functions per codebase grew from about 4 at the start to about
  37 by the final checkpoint. Peak cyclomatic complexity roughly 27 → 68.
- Agent code ended around 2.2-2.3x more verbose and about 2x more eroded than
  maintained human repositories, and **the gap widened every iteration**. Human
  repos stayed roughly flat.
- Quality-focused prompting cut initial verbosity and erosion by up to a third
  but **did not change the rate of degradation** — it moved the intercept and
  left the slope.
- Test suites do not see it. Core tests stayed passable while error-handling and
  regression tests collapsed; by the final checkpoint core tests were up to 13x
  easier to pass than the full suite.

That last point is why this goes unnoticed. Green tests are not evidence of
structural health, and a codebase can decay through a hundred individually
reasonable commits.

**How to catch it**

Only by measuring the slope. A point-in-time audit cannot distinguish a
codebase that is bad from one that is getting worse, and the second is the
actionable condition.

```bash
python3 scripts/slop_scan.py baseline .
# ...after each agent iteration:
python3 scripts/slop_scan.py check . --entry <module>
```

Full treatment in `references/bloat-playbook.md`.

**Cost profile:** invisible per-commit, compounding across commits. Cheapest
defect class to prevent, most expensive to remediate late.

---

## What does not vary by tier

**Package hallucination.** Do not treat this as a small-model problem. A 2026
replication across five frontier models measured 4.62%-6.10% hallucinated
package references — compressed from the 5.2%-21.7% spread seen in the 2024
cohort, but not eliminated, and no 2026 frontier model beat the best 2024
commercial result. More importantly, 127 package names were invented
*identically by all five models*, across four different vendors. Convergent
error means vendor diversity is not a mitigation and neither is model quality.
Verify every AI-introduced dependency.

**Correctness is decoupled from structure.** Code that runs is about as likely
to be structurally flawed as code that fails. Passing tests tells you nothing
about maintainability.

---

## Review depth table

| Wrote the code | Read closely for | Can mostly automate | Do not bother |
|---|---|---|---|
| Small / fast model | Reimplemented helpers, wrong-shaped solutions, phantom packages | Clone detection, linting, comment noise | Deep architecture review — it rarely built enough architecture to be wrong |
| Frontier model, single task | Speculative abstraction, long methods, modular mirage | Complexity hotspots, orphan detection | Comment cosmetics — it will be clean and tell you nothing |
| Frontier model, agentic loop | Everything above, plus the trend | Ratchet on every iteration | One-shot audits — they miss the slope, which is the actual problem |
| Multiple agents in parallel | Divergent duplicate solutions to the same problem | Cross-branch clone detection before merge | Per-agent style consistency |

The last row is worth a note if work is split across agents: two agents solving
adjacent problems independently will each build their own version of the shared
helper. Run clone detection across the merged result, not per branch — per
branch it is invisible by construction.
