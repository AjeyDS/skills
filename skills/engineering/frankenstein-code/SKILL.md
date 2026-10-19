---
name: frankenstein-code
description: Find open-source code that already solves part of a goal (new build, refactor or fix), vet it, take only the needed pieces, and stitch them in with provenance recorded.
license: MIT
compatibility: Needs web and GitHub search. Uses parallel subagents when the agent supports them.
metadata:
  author: AjeyDS
  version: '1.0'
---

# Frankenstein Code

Goal: before writing something from scratch, find open-source pieces that already do part of the job, pick the best one for each part, take only what is needed, and stitch it into the project cleanly.

Use when the user invokes this skill, or asks things like "is there something open-source for this", "don't reinvent this", "find a library that does X", while building, refactoring or fixing.

Difference from `freshness-check`: that one checks a plan for newer tools and ideas. This one sources actual code and transplants it. Each skill works on its own; when both are used, run freshness-check first and this skill reuses its finds (see Step 2).

## Step 1. Pin the goal and break it into parts

- Write the goal in one line: what we are building or fixing, and what "done" looks like.
- Note constraints: language, framework, runtime, commercial or not (affects license), size limits.
- If the project is reachable, read it first: language, existing dependencies, patterns, how errors and logging are done.
- Split the goal into a parts list. Each part is one job, described as a job, not a product. Example: "turn a PDF into text with layout kept", not "PDF library".
- Some parts are the core of the product. Mark them. Those usually stay our own code.
- Ask at most one question if the goal is unclear.

## Step 2. Search each part

**If a freshness-check brief exists in this conversation, start from it.** Take the tools, libraries and repos it named, map each to a part, and vet those first in Step 3. Only search further for parts the brief did not cover, or where its candidates fail vetting. Do not repeat searches it already did. If there is no brief, do the full search below.

Search per part, in parallel (one cheap subagent per part if available). Each returns at most 3 candidates.

Where to look:
- Package registries (npm, PyPI, crates.io, Go packages): best when the piece can be installed.
- GitHub repo search: filter by language, topic, stars and recent push date. Also check "awesome-<topic>" lists.
- GitHub code search: for a single function or algorithm, the smallest piece we could lift.
- Hugging Face and Papers with Code: for ML models and methods.
- Practitioner posts (Hacker News, Reddit, dev blogs): to see what people actually use and regret.
- For a bug fix: search the issue trackers of our dependencies for the error message first.

Query tips: phrase it as the problem ("diff two json documents"), try "alternative to <known tool>", add the language name.

## Step 3. Vet every candidate

Read the README and the actual code. Never trust a name or a search snippet.

| Check | Pass | Flag |
|---|---|---|
| License | MIT, Apache 2.0, BSD, ISC | GPL, AGPL, SSPL, no license (do not copy into a closed project) |
| Health | commits in the last ~6 months, releases, issues answered | archived, single abandoned maintainer |
| Fit | same language, API shape close to what we need | needs a big framework we don't use |
| Weight | small dependency tree | pulls in many heavy deps for one function |
| Safety | no open advisories (osv.dev, deps.dev), package name matches the real repo | look-alike names, very low downloads, install scripts |

Also confirm the functions we plan to use actually exist in the current version.

## Step 4. Choose how to take it (cheapest first)

1. **Install as a dependency.** Default when the project is healthy and we use a good share of it.
2. **Install but use only a submodule.** When the library is modular.
3. **Extract only the needed files (vendor).** When the library is huge, abandoned, or we must change its internals.
4. **Write our own, using it as a reference.** When the license blocks reuse or the piece is tiny. Learn the approach from docs or papers; do not rewrite copyleft code line by line.
5. **Build it ourselves.** When nothing fits, or the glue would be bigger than the piece.

Pause and get the user's OK before adding dependencies or vendoring code.

## Step 5. Extract (option 3 only)

- Shallow-clone into a temp folder and note the commit SHA.
- Start from the entry function we need and follow its imports. Keep only what is actually reached.
- Copy those files into `third_party/<name>/`.
- Keep the LICENSE file and copyright headers.
- Delete unused functions, files, config and tests for removed parts.
- Swap their heavy dependencies for ones we already have, where easy.
- Run their relevant tests, or write one small test, before changing anything.
- Delete the temp clone.

## Step 6. Stitch it in

- Put each piece behind our own small interface (an adapter). The rest of the code calls our interface, never the third-party code directly, so the piece can be swapped later.
- Convert data shapes, errors and logging at that boundary. Don't rewrite the insides unless needed.
- Add tests at the boundary.
- Record provenance in `THIRD_PARTY.md`: name, URL, commit or version, license, what was taken, what was changed.

## Step 7. Report

Keep it short. For each part:

- Pick and why (one line)
- How taken: install / submodule / extract / reference / build
- License
- Risks or open questions

List parts with no good match as "build ourselves". End with the proposed next step and wait for approval if anything gets installed or vendored.

## Rules

- Never copy copyleft code into a project that isn't released under a compatible license.
- Never vendor code without its license file.
- Fewer, healthier parts beat many small ones.
- If the glue is bigger than the piece, write the piece ourselves.
- Core product logic stays ours; reuse is for the plumbing around it.
