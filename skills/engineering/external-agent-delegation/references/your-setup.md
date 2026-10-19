# Your delegation setup

Template. Copy it to `your-setup.local.md` in this folder and fill that in
(or let the agent write it after asking you). SKILL.md reads the `.local`
copy first, so your nicknames and model rules override the generic
defaults, and updating the skill never overwrites your copy.

## Agents you run

| Agent / CLI | Your nickname for it | Models you use through it | Branch prefix | Methodology pack installed? |
|---|---|---|---|---|
| Codex CLI | e.g. "codex", "gpt" | e.g. GPT top tier at high effort, small tier for bulk passes | `codex/*` | e.g. Superpowers |
| Cursor CLI (`cursor-agent`) | e.g. "cursor" | e.g. only Grok, always named explicitly | varies | |
| Gemini / Antigravity CLI (`gemini` / `agy`) | e.g. "gemini" | e.g. Flash for narrow tasks | varies | |

## Rules

- Which model families go through which tool (e.g. "Cursor only for Grok;
  GPT always through Codex").
- Default effort level per model, if it matters to you.
- Anything the main agent must never do (e.g. "never use Auto model
  selection", "external agents never push to main").

## Where your capability record lives

Default: append dated entries to `field-notes.md` in this folder, in the
same shape as the author's entries (date, agent+model+effort, task shape,
outcome, what it changes about the review tier). Once you have a few of
your own, delete the author's entries.
