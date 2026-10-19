---
name: synthesize-research-insights
description: Use after a RAW research pass (or when the user asks to synthesize, interpret, find patterns, or learn what actually works from collected sources). Reads sources/<topic>/ without modifying them and writes a plain-language insights/<topic>.md — easy explanations, low jargon, with pointers back to RAW files for depth.
license: MIT
compatibility: Local file access. Reads the sources/<topic>/ folder that saving-raw-sources produces.
metadata:
  author: AjeyDS
  version: '1.0'
---

# Synthesize Research Insights

Turn a RAW source dossier into a **plain-language, evidence-grounded** insights note. Companion to `saving-raw-sources`.

**Hard rule:** Never edit, rewrite, merge, or delete files under `sources/`. Insights are a separate artifact. The RAW files keep the jargon and detail; this note explains what they mean in simple words.

**Goal:** What actually appears to work across the dossier — explained so a smart non-expert can follow — not a remix of commonly repeated advice, and not a jargon dump. Keep rare high-signal outliers visible; do not average them away.

## Voice (non-negotiable)

Write like you're explaining to a curious friend, not a paper review board.

- Short sentences. Everyday words.
- If a technical term is needed once, define it in plain English on first use (e.g. "retrieval — looking up relevant text from a library of documents").
- Prefer "what happens / why it helps / when it fails" over paper-speak.
- No stacked acronyms. No scoring jargon in the note body — surface confidence as "strong / medium / weak evidence."
- Do not paste dense quotes from papers. Point to the source file for depth: "Details: `filename`."
- The insights file is the **easy layer**. The sources folder is the **deep layer**.

## When to run

After `sources/<topic-slug>/` has enough material (usually 3+ sources), or when the user asks to synthesize, interpret, find patterns, extract what works, or learn from the accumulated research.

## Inputs

- Topic slug (or path to `sources/<topic-slug>/`)
- Read every source file in that folder (and nested folders if present). Use `index.md` as the inventory; still open each file.
- Prefer full text over titles. Skim is not enough for claim extraction.

## Method (do in order)

Do the analysis carefully; **write the output simply**.

1. **Inventory** — List every source file with `source_url`, type (paper / textbook / official guide / talk notes / secondary article), and approximate depth.
2. **Extract claims** — For each source, pull concrete claims about what works, what fails, and *why*. Tag internally with source file, claim type, and evidence strength. You do not need to dump these tags into the final note.
3. **Cluster by how it works** — Group claims that share the same underlying idea (the "why"), not the same slogan. Name each cluster in plain language (e.g. "practice with real feedback beats practicing alone"), never tip-speak ("practice a lot") and never jargon labels unless defined.
4. **Judge strength** — How many independent sources? Papers/field guides beat tip lists. Note disagreements.
5. **Separate the rehash** — Widely repeated advice with no clear "why" or only tip-list support goes under **Popular advice that isn't well backed**.
6. **Surface outliers** — Rare but useful ideas go under **Unusual ideas that still look strong**.
7. **Write the insights doc** — Path: `insights/<topic-slug>.md` (or the vault folder the user uses for insights). Overwrite that topic’s file unless they ask to keep history.
8. **Reply** — Path + short section list. Do not paste the full note in chat unless asked.

## Output template (`insights/<topic-slug>.md`)

```markdown
---
topic: <topic-slug>
synthesized: YYYY-MM-DD
source_folder: sources/<topic-slug>/
source_count: N
note: Plain-language summary. RAW sources are unchanged. Go to those files for full detail.
---

# Insights — <Topic title>

## In plain words — what we can learn

Half a page max. Short paragraphs. Only what the sources actually support. Each idea should match a pattern below.

## What seems to work (and why)

For each idea:
- **In plain words:** …
- **Why it helps:** …
- **How sure are we:** strong / medium / weak (and roughly how many independent sources)
- **Where to read more:** `filename` (and another if useful)
- **Where sources disagree:** … (or "no major disagreement")

## Evidence at a glance

| Idea | How many sources | Best kind of evidence | Confidence |
| --- | --- | --- | --- |
| … | … | study / field guide / tips | strong / medium / weak |

## Popular advice that isn't well backed

Common tips that show up a lot but lack a clear mechanism or only appear in tip lists. Say why we're not treating them as proven.

## Unusual ideas that still look strong

Rare findings that shouldn't be averaged away. Say when they might matter.

## What's missing or unclear

Conflicts, thin spots, and what would change our mind.

## Sources used

| File | URL | Type |
| --- | --- | --- |
| … | … | … |
```

## Quality bar

- **Simple on the page; rigorous underneath.**
- Prefer "how it works" over "hot tip."
- Prefer independent sources over the same advice copied many times.
- One tip blog ≠ one research paper.
- If a popular claim isn't supported, say so under missing/unclear — don't invent evidence.
- Never rewrite RAW source wording into this file as uncited deep analysis.
- If a sentence needs a glossary to parse, rewrite it.

## Pairing with saving-raw-sources

1. Run `saving-raw-sources` for the topic.
2. Run this skill on `sources/<topic-slug>/`.
3. If gaps matter, collect more RAW sources, then re-run this skill.

Do not fold synthesis into the RAW-saving skill.
