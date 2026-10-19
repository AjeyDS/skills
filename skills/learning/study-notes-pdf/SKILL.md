---
name: study-notes-pdf
description: Build a researched, layered study guide on any topic and deliver it as a polished PDF. The notes go big-picture first, then zoom into the details needed to fully understand the concept or flow, with diagrams (fetched from good sources or drawn), memorable examples, and mental models. Use this skill whenever the user asks for study material, study notes, revision notes, a cheat sheet, a primer, a "prep doc", "help me understand X" as a document, "make notes on X", "explain X and give it to me as a PDF", exam/certification prep on a topic, or interview-prep material on a concept, system, or one of their own projects. Trigger even when the user does not say "PDF" or "notes" but clearly wants a reusable, readable learning document rather than a chat answer (e.g. "put together something I can read on OAuth flows", "I need to learn Kafka this weekend"). Do NOT use for live tutoring dialogue, quick one-line definitions, or task work (coding, debugging, writing an essay).
license: MIT
compatibility: Web access for research and diagrams. PDF build needs Python 3 with markdown and playwright (Chromium); poppler's pdftoppm is optional for previews.
metadata:
  author: AjeyDS
  version: '1.0'
---

# Study Notes → PDF

You are producing a study document someone will read to actually understand a topic — often before an
interview, an exam, or a deep-dive at work. The document has to do two things at once: give a clear
top-down picture fast, and then carry the reader down into enough detail that the concept or flow
holds together in their head afterward. Everything below serves that.

The flow is: **scope → research → outline → write → visuals → build PDF → verify → deliver.** Keep
moving; the user asked for a document, not a conversation.

## 1. Scope (one short round of questions)

Ask *before* research, in one message, using the multiple-choice question tool if it is available
(AskUserQuestion). Only ask what changes the document. Pick from these; usually 2–4 questions is right:

- **Goal** — interview prep / exam or certification / understand it for work / curiosity. This sets
  the register: interview prep wants spoken-plain-English explanations and "how would you say this
  out loud" framing; exam prep wants blueprint coverage and gotchas; work wants the practical flow.
- **Current familiarity** — never heard of it / know the basics / use it but fuzzy on internals. This
  decides how much of the ladder to skip.
- **Depth or time budget** — quick refresher (~15 min read), solid understanding (~45 min), thorough
  (an hour-plus, reference-quality). Depth scales page count; see §5.
- **Angle or sub-topics** — anything specific to include, exclude, or emphasise (e.g. "focus on the
  token refresh part", "compare with Kafka").

If the request already answers these, skip the questions. If the session is unattended (scheduled, or
the user said they'll check back), pick sensible defaults, state them at the top of your reply, and go.

## 2. Research

Search the web and read a handful of good sources before writing anything. Aim for a mix of
authoritative and explanatory: official docs or specs, a well-regarded engineering blog or Medium
article, a paper or textbook chapter if the topic has one, plus one source that explains it well for
beginners. Pull out: the definitions, the actual mechanism or sequence of steps, numbers worth
remembering, common misconceptions, and the failure modes or trade-offs experts talk about.

While reading, note **image candidates**: a diagram in a source that shows the flow well. Record its
URL and what it shows; you will try to fetch it in step 6. Also note things that *deserve* a diagram
even if no source has a good one.

For the user's own projects (interview prep), research means reading the project files or memory
context they point you to, not the web — and the register is "explain it to someone who has never
seen the codebase, no internal names without a plain-words gloss first."

Keep a `sources` list (title + URL); it goes at the end of the PDF.

## 3. Outline: the ladder

Structure every document as a ladder from wide to narrow. The reader should be able to stop at any
rung and still have a coherent (if shallow) picture. A dependable rung order:

1. **The one-paragraph answer** — what it is, what problem it solves, why anyone cares. If the reader
   reads nothing else, this is enough to hold a two-minute conversation.
2. **The mental model** — one analogy or picture that the rest of the document hangs on. Choose it
   carefully; a good one makes the details feel inevitable rather than arbitrary.
3. **The parts** — the main components or actors and what each is responsible for. A diagram lives
   here.
4. **The flow** — how the parts interact, step by step, in the normal case. Sequence diagram or
   numbered walk-through with one concrete example threaded through.
5. **The details that make it actually work** — the rules, edge cases, configuration, internals that
   the previous rungs glossed over. This is the deep section; split it into sub-sections per idea.
6. **Where it breaks / trade-offs / comparisons** — failure modes, what to watch for, how it compares
   to the obvious alternative.
7. **Recap + "say it out loud"** — a half-page summary, a memory hook list, and (for interview or
   exam goals) 3–5 likely questions with model answers.

Adapt the rungs to the topic — a history topic has "timeline" where a system has "flow" — but keep the
wide-to-narrow direction. Write the outline down and, when the topic is large or the scope was fuzzy,
show it to the user in a few lines before writing. For a small, clearly-scoped topic just proceed.

Read `references/structure.md` for the per-section pattern, the pedagogy rules, and how to write
examples and mental models that stick.

## 4. Write (Markdown)

Write the document as a single Markdown file (`notes.md`) in the working directory. Conventions the
builder script understands:

- `# Title` once at top; `## ` for rungs, `### ` for details within a rung. Don't number headings
  yourself — the builder numbers them and builds the contents page. Avoid quotes and apostrophes in
  headings (they can render as entities in the contents page).
- Callout boxes via blockquote prefixes: `> **Mental model:** …`, `> **Example:** …`,
  `> **Remember:** …`, `> **Gotcha:** …`, `> **Interview answer:** …`. Use them — they are the parts
  people re-read.
- Diagrams as fenced `mermaid` blocks (flowchart, sequenceDiagram, stateDiagram, classDiagram,
  timeline). Images as normal Markdown images with a caption line in italics below.
- Tables for comparisons. Code blocks only where code *is* the concept.
- Every piece of jargon gets a plain-words gloss the first time it appears. Write as if explaining to
  a smart colleague who doesn't know this area — natural spoken flow, short sentences, no filler.

Each detail sub-section follows the same beat so the reader can find their footing: *what it is →
why it exists → how it works → a concrete example → one line to remember.*

## 5. Length scales with the topic and the depth chosen

Budgets count **body pages** (the cover and contents page are extra, and a short document should skip
the contents page with `--no-toc`). Roughly: quick refresher 3–5 body pages; solid understanding of one
concept 6–10; a multi-part system or flow 10–16; a whole exam domain 18+, and at that size prefer
several PDFs (one per sub-domain) over one monster. When the user says "quick", "short", "night
before", or "not a monster", treat the low end as a hard cap — a beginner who asked for a quick read
will not open a 13-page document twice. Density matters more than page count: a page with a diagram,
one callout, and 300 words beats a wall of text. If you are over budget, cut detail sub-sections and
secondary comparisons, never the mental model, the running example, or the diagrams. Check the page
count the builder prints against the budget before verifying.

## 6. Visuals

Every "parts" and "flow" rung needs a picture; details get one when the idea has shape (a state
machine, a data layout, a comparison). Order of preference:

1. **Fetch** a good source diagram noted in research with `scripts/fetch_image.py <url> <out.png>`.
   It validates the download (real image, reasonable size, not a tracking pixel or a logo). This is
   for the user's personal study use; still credit the source in the caption. Sites often block
   fetches — that's fine, fall through. Give it at most one attempt per figure and stop trying
   altogether after two failures in a row (the network is probably blocked); drawing is cheap.
2. **Draw** with Mermaid inside the Markdown — fastest and it always renders. Prefer this for flows,
   sequences, hierarchies, state machines.
3. **Draw** with matplotlib or hand-written SVG when Mermaid can't express it (a curve, a memory
   layout, a grid, an annotated timeline). Save PNG/SVG beside `notes.md` and reference it.

`references/visuals.md` has Mermaid patterns that render well on a PDF page and the sizing rules that
keep diagrams legible. The short version: the page is portrait, so a left-to-right flow with more than
five nodes shrinks to unreadable text, and a top-to-bottom flow with more than eight nodes gets
capped in height and shrinks too. Split anything bigger into an overview diagram plus a zoomed one.

## 7. Build the PDF

```bash
python3 <skill-path>/scripts/build_pdf.py notes.md --out "<Topic> — Study Notes.pdf" [--title "…"] [--subtitle "…"]
```

The script converts Markdown → styled HTML (cover block, table of contents, callouts, page numbers),
renders Mermaid blocks to SVG (via `mmdc` if installed, else in-browser Mermaid), and prints to PDF
with headless Chromium through Playwright. It prints the page count. If Playwright/Chromium is missing
it falls back to `wkhtmltopdf`; if that is missing too it tells you what to install.

## 8. Verify before delivering

A PDF that looks wrong is worse than none. Render a few pages to images
(`pdftoppm -png -r 60 -f 1 -l 4 out.pdf /tmp/page`) and look at them with the Read tool: the cover,
one page with a diagram, one with a callout. Check that diagrams are not clipped or tiny, that
headings don't strand at page bottoms, that images actually appear, and that no page is mostly blank
because a figure was pushed to the next page (if so, move the figure or a paragraph so the page fills). Fix and rebuild if needed. Also
skim the text once for the things that quietly ruin study notes: a term used before it's explained,
a step in the flow that's missing, an example that doesn't match the text.

## 9. Deliver

Send the PDF to the user (SendUserFile, or whatever file-delivery tool exists). If a folder on their
computer is connected, also write it there and say where. Accompany it with two or three sentences:
what the document covers, how it is layered, and one thing you chose to emphasise or leave out and
why. Offer, in one line, to go deeper on any rung or to produce a companion (flashcards, a one-page
cheat sheet, a quiz).

## Things that go wrong

- **Starting narrow.** Opening with configuration flags or API signatures before the reader knows
  what the thing is for. The first page must work for someone who has never heard of the topic.
- **Analogy that fights the mechanism.** A cute analogy that breaks on the second detail confuses more
  than it helps. Test the mental model against the details section before committing to it.
- **Examples that are abstract.** "Suppose a client requests a resource" teaches nothing; "your phone's
  weather app asks the server for Austin's forecast at 7:02 am, carrying token `abc…`" does. Use one
  running example with named actors and real-looking values, and reuse it across sections.
- **Unglossed jargon.** Especially for interview prep — the user must be able to say every sentence
  out loud to someone outside the project.
- **Decorative visuals.** A diagram that restates a heading is noise. Each one should show a
  relationship, sequence, or structure the text can't carry alone.
- **Skipping verification.** Mermaid syntax errors render as red text; fetched images 404 silently.
  Look at the pages.
