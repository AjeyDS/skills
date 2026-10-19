# Structure and pedagogy reference

Read this once before writing `notes.md`. It covers how each section should be built, how to write
mental models and examples that people actually remember, and how to adapt the ladder to different
goals.

## The per-section beat

Every detail sub-section (`###`) follows the same five beats. Readers learn the rhythm after two
sections and can then skim to whichever beat they need.

1. **What it is** — one or two plain sentences. Name it, gloss any jargon.
2. **Why it exists** — the problem it solves or what would go wrong without it. This is the beat
   most notes skip, and it's the one that makes the mechanism feel necessary instead of arbitrary.
3. **How it works** — the actual mechanism, in order. Numbered steps when there is a sequence.
4. **Example** — the running example applied to this piece, with concrete values.
5. **Remember** — one line. The thing to be able to say six weeks from now.

Beats 4 and 5 go in callout boxes (`> **Example:**`, `> **Remember:**`) so they stand out on the page.

## Mental models that hold up

A mental model is a compression: one picture that lets the reader re-derive the details instead of
memorising them. Good ones share three properties:

- **Structural match.** The analogy's parts map one-to-one onto the real parts, and the analogy's
  behaviour predicts the real behaviour. "A Kafka topic is a log file that many readers can each keep
  their own bookmark in" predicts partitions, offsets, and consumer groups. "Kafka is a post office"
  predicts nothing.
- **Named mapping.** After giving the analogy, spell out the mapping in a short table or list:
  *bookmark → consumer offset; reader → consumer; log file → partition.* Readers won't do this
  themselves, and without it the analogy stays decorative.
- **Declared limits.** Say where the analogy breaks ("unlike a real log file, the head gets trimmed
  by retention"). This prevents the model from creating a misconception later.

Place the primary mental model at rung 2 and refer back to it by name in later sections ("in the
log-file picture, this is…"). Secondary models can appear inside detail sections when a sub-mechanism
has its own shape.

## Examples that stick

- **One running example.** Choose a single concrete scenario in the scoping step and thread it
  through every rung. Name the actors (a person, an app, a service), give real-looking values (IDs,
  timestamps, sizes). Re-using the same scenario means each new section costs the reader nothing to
  set up.
- **Values, not variables.** `user_id=4821`, `TTL=300s`, `3 replicas`, "the 7:02 am request". A
  reader remembers numbers attached to a story far better than symbols.
- **Show the failure too.** For each important rule, one line on what happens when it's violated:
  "if the refresh token has also expired, the app has to send the user back to the login screen."
- **Interview or exam register.** Add a `> **Interview answer:**` box where a section is a classic
  question, written as it would be spoken in 30–45 seconds. For exam prep, add a `> **Exam tip:**`
  box for the distinction the exam likes to test.

## Memory hooks

At the recap, give a short list of hooks — mnemonics, contrasts, "the three things", a sentence
template. Hooks work when they encode a *distinction* the reader is likely to blur (e.g. "authentication
= who you are, authorization = what you may do; the N in authe**N**tication is for **N**ame"). Don't
force a mnemonic on every item; three or four strong ones beat ten weak ones.

## Adapting the ladder to the goal

| Goal | Emphasise | Trim | Extra section |
|---|---|---|---|
| Interview prep | plain spoken explanations, "why", trade-offs, the user's own decisions if it's their project | exhaustive config/API detail | "Likely questions and how to answer them" |
| Exam / certification | blueprint coverage, distinctions the exam tests, limits and numbers | narrative history | "Exam traps" list, quick self-check MCQs with answers at the very end |
| Understand for work | the flow, operational details, failure modes, how to debug | comparisons with alternatives unless asked | "How to check this in practice" (commands, dashboards, logs) |
| Curiosity / general | story, why it was invented, the elegant idea | edge cases | "Where to go next" |

For a user's own project (interview prep), the "parts" rung is the architecture, the "flow" rung is
one user action traced end to end, and the "details" rungs are the decisions they made and why — each
one phrased so it can be said aloud without internal names.

## Ordering inside the details rung

Order detail sub-sections by dependency, not by importance: if B needs A to make sense, A comes first
even if B is the thing the user asked about. When two ideas are independent, put the more commonly
asked one first. If a sub-section only makes sense after the "where it breaks" rung, move it there.

## Tone

Plain, direct, warm. Short sentences. "This trips people up" rather than "this is easy". No
cheerleading, no emoji. Second person is fine ("you'll see this in the logs as…"). Explain the why
behind rules instead of just stating them.
