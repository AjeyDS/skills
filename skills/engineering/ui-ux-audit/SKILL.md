---
name: ui-ux-audit
description: Audit a frontend repo against core UI/UX basics (states, accessibility, tokens, spacing, type, color, depth, hierarchy) and report fixes with file:line. Use for UI reviews, design polish, or UX quality checks.
license: MIT
compatibility: Any coding agent with access to a frontend repo. A browser tool is optional, for checking the running app.
metadata:
  author: AjeyDS
  version: '1.0'
---

# UI/UX Audit

Check a frontend codebase against a small set of UI/UX basics. First scan the code with search tools, which gives facts. Then look at the running UI if possible, which gives judgment. Report findings. Do not change code unless the user asks.

## Rules
- The numbers below are guidelines, not laws. Flag outliers and inconsistency, not every small deviation.
- Prefer one fix at the theme or token level over many fixes inside components.
- Every finding needs a location (`file:line`) and a concrete fix.
- Skip checks that don't apply (for example, no dark mode in the app means no dark mode check).

## Step 1: Map the styling setup
Find out, before checking anything:
- Styling method: Tailwind (`tailwind.config.*` or `@theme` in CSS), plain CSS/SCSS, CSS-in-JS, or a component library (shadcn, MUI, Chakra).
- Where tokens live: theme file, CSS variables on `:root`, or the Tailwind config.
- How dark mode works, if it exists.
- The main screens and the shared components (Button, Input, Card, Modal).

## Step 2: Code scan

### 1. Feedback and states (highest priority)
Every user action needs a visible response.
- **Buttons**: hover, pressed/active, focus-visible, disabled. Add loading when the button starts async work.
- **Inputs**: focus, error (red border plus a message), disabled. Add a warning state where it fits.
- **Async screens**: loading (spinner or skeleton), empty state, error state, success confirmation.
- **Invisible actions** (copy, save, delete, add to list): a small confirmation such as a toast, chip, or checkmark.
- How to check: open the shared Button and Input components. Search for data calls (`fetch`, `useQuery`, `useMutation`, `axios`) and confirm each one handles loading, error, and empty.

### 2. Accessibility
- Focus ring on every interactive element. Flag `outline: none` or `outline-none` without a replacement.
- Text contrast at least 4.5:1, or 3:1 for large text. Light gray text and placeholders often fail.
- Tap targets at least 44x44px on mobile.
- Icon-only buttons have `aria-label`. Images have `alt`.
- Meaning is never shown by color alone. Pair color with an icon or text.
- Animations respect `prefers-reduced-motion`.

### 3. Tokens over hardcoded values
- Search for hex colors outside theme files: `rg -n "#[0-9a-fA-F]{3,8}\b" -g '!*theme*' -g '!*tailwind.config*'`
- Search for Tailwind arbitrary values: `rg -n "\w-\[[^\]]+\]"`
- Pass: colors and spacing come from tokens, with only a few justified one-offs.

### 4. Spacing
- Spacing should sit on a 4px scale (4, 8, 12, 16, 24, 32...). Tailwind's default scale already does this. 1px and 2px are fine for borders.
- Search: `rg -n "(margin|padding|gap)[^;]*\d+px"` and flag values not divisible by 4.
- Related items should sit closer together than unrelated ones. Sections need room to breathe.

### 5. Typography
- One font family. A second monospace font for code is fine. Search `font-family` and `fontFamily`.
- Count distinct font sizes. Aim for 6 or fewer on websites. On dashboards, text rarely goes above 24px.
- Large headings (about 32px and up): letter-spacing about -0.02em to -0.03em, line-height about 1.1 to 1.2.
- Body text line-height about 1.5.

### 6. Color
- One primary brand color, with lighter shades for backgrounds and darker shades for text (a color ramp).
- Semantic colors carry meaning: green for success, yellow for warning, red for danger/error, blue for info or trust.
- Flag decorative use of semantic colors (red that isn't an error) and errors shown without red.

### 7. Depth (shadows and dark mode)
- Shadows: low opacity (about 5 to 15%) with a larger blur. Flag card shadows above about 25% opacity. Popovers and modals get stronger shadows than cards.
- Dark mode: show depth by making cards lighter than the background, not with shadows. Keep borders subtle. Lower the brightness and saturation of chips and badges.

### 8. Icons and buttons
- Icon size about equals the text line-height next to it (for example, 24px icon with 24px line-height). Flag icons clearly bigger than nearby text.
- Button padding: horizontal about 2x vertical.
- Primary and secondary buttons look clearly different. Use ghost buttons (no background until hover) for secondary actions and nav.

### 9. Text on images
- Text over images uses a gradient overlay that fades into a readable background, optionally with a blur. Flag raw text on images and flat full-image dark overlays.

## Step 3: Visual pass (only if the app can run)
If a dev server can start and a browser tool is available, open the main screens in light and dark mode, at desktop and mobile widths. Judge:
- **Signifiers**: can you tell what's clickable, selected, grouped, or disabled without any instructions?
- **Hierarchy**: on each card and screen, is the most important thing the biggest, highest, or most colorful? Does your eye go there first?
- **Whitespace**: do sections breathe? Are related items grouped?
- **Shadow test**: if a shadow is the first thing you notice, it's too strong.
- Actually trigger states: hover, focus with the keyboard, submit an empty form, load with no data.

If the app can't run, say so in the report and judge hierarchy from the component code only.

## Report format
1. A short table: each of the 9 areas plus Visual, marked Pass, Needs work, or Fail.
2. Findings grouped by priority. One line each: `file:line — problem — fix`.
   - **High**: missing states, accessibility failures, contrast failures.
   - **Medium**: consistency problems (hardcoded colors, off-scale spacing, too many fonts or sizes).
   - **Low**: polish (heading letter-spacing, shadow softness, icon size).
3. The top 3 fixes with the biggest impact.
4. Offer to apply fixes, starting at the theme/token level.
