---
name: saving-raw-sources
description: Use when the user asks to collect, research, scrape, or save RAW source files, one file per source, web research notes, or structurally cleaned documents about any topic. Use when they say save raw, keep the original text, don't change the wording, one file per source, or store data from the source.
license: MIT
compatibility: Web fetch and local file writes.
metadata:
  author: AjeyDS
  version: '1.0'
---

# Saving RAW Sources

Save **RAW** files: original source wording, one file per source. Clean means structural edits only.

**RAW** = the source's own sentences. Not a summary, paraphrase, translation, or rewrite.

## Do this

1. Take the topic (or URL). Slug it: lowercase, hyphens.
2. Create `sources/<topic-slug>/` in the current workspace (create `sources/` if missing).
3. Find **primary sources** (official pages, papers, open textbooks, first-party docs). Follow each claim to the page that owns it.
4. Fetch each original page or PDF. If the fetch tool summarized, that dump is **not RAW** — fetch again, use a PDF/text download, or quote from a dump that still has the original sentences.
5. Structural-clean only (see below). Do not change context texts.
6. Write **one markdown file per source** using [template.md](template.md). Filename: `<source-slug>.md`.
7. Add or update `sources/<topic-slug>/index.md` with one row per file: filename + `source_url`.
8. Reply with the folder path and the file list. Do not recap the source content.

## Structural clean (allowed)

Remove or restore layout. Do not rewrite sentences.

- Site nav, footers, cookie banners, ads, share buttons (`Tweet`), login chrome
- Duplicate consecutive titles
- Fetch-tool wrappers (`Content from https://...`)
- Empty table-of-contents chrome that is not the source's own TOC
- Restore original part/chapter breaks (`Part 2` on its own line) when the fetch flattened them

Keep: body text, headings that belong to the source, captions, tables, quotes, footnotes, license lines that are part of the work.

## Not RAW — stop and redo

- Paraphrase, bullet-condense, "key takeaways", or grammar fixes
- Merging two URLs into one file
- Using a search-snippet or encyclopedia recap instead of the page
- Keeping a tool-generated chapter summary in place of the chapter

| Excuse | Reality |
| --- | --- |
| "More readable if I summarize" | RAW is the source text. |
| "Fetch gave a summary, close enough" | Not RAW. Get the original. |
| "I'll combine sources" | One file per source. |
| "I'll fix typos" | Do not change context texts. |

## Where files go

```
sources/<topic-slug>/
  index.md
  <source-slug>.md
```

If `sources/` already has files for this topic at the top level, keep writing into that existing layout instead of duplicating a subfolder.

## After save

List paths and source URLs. Do not rewrite the collected text in chat.
