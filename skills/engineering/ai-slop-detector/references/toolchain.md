# Toolchain

What to install, what each tool actually answers, and the settings that change
the answer.

**Contents**
1. [Why tools and not just reading](#why-tools-and-not-just-reading)
2. [Minimum viable setup](#minimum-viable-setup)
3. [By capability](#by-capability)
4. [Per language](#per-language)
5. [Verified traps](#verified-traps)
6. [Structural search with AST patterns](#structural-search-with-ast-patterns)

---

## Why tools and not just reading

A prompt or a skill document alone cannot do codebase-scale analysis, for three
concrete reasons rather than one vague one:

1. **Coverage.** Duplicate detection is all-pairs across the repo; reachability
   is a graph traversal from entry points; cycle detection is a graph property.
   Sequential file reading samples; it does not compute these.
2. **Reproducibility.** A ratchet needs the same input to yield the same number
   twice. Model judgment does not guarantee that; a parser does.
3. **Cost.** Reading a repo to find clones costs tokens proportional to repo
   size, every time. A tokeniser does it in milliseconds.

This is not a claim that tools replace judgment. Deciding whether a duplication
is accidental or deliberate, or whether an abstraction earns its keep, is not
mechanisable and is exactly what the tools free up budget for.

Worth noting that the research measuring agent-generated verbosity used AST
pattern-matching density as its metric (0.32 violations for agents vs 0.11 for
humans) rather than an LLM judge — the people building slop benchmarks reached
for parsers.

---

## Minimum viable setup

`scripts/pyast.py` needs nothing but Python's standard library and covers
reachability, complexity, error masking, and connectivity for Python. Start
there; everything below is additive.

```bash
# highest value per minute of setup
npm  install -g jscpd                    # duplication, 200+ languages
pip  install --break-system-packages lizard vulture   # complexity, dead-code hints
npm  install -D knip                     # TS/JS dead code (per-project)
```

---

## By capability

| Need | Tool | Notes |
|---|---|---|
| Duplicate blocks | `jscpd` | Language-agnostic, tokeniser-based. v5 is a Rust engine and much faster than v4. |
| Dead code (TS/JS) | `knip` | Mark-and-sweep over the module graph. Successor to `ts-prune` and `tsr`, both archived and pointing at knip. |
| Dead code (Python) | `pyast.py`, then `vulture` | Reachability first; see the vulture trap below. |
| Complexity | `lizard` | Multi-language, one binary. `radon` for Python-only detail. |
| Structural patterns | `ast-grep` | Fast, patterns look like the code they match. |
| Security patterns | `semgrep` | Larger curated ruleset; slower. |
| Layer/cycle enforcement | `import-linter` (Py), `dependency-cruiser` (JS/TS) | Turns architecture into a failing check. |
| Dependency vulnerabilities | `pip-audit`, `npm audit` | Does not catch phantom packages — see below. |
| Line counting | `cloc` | For trend tracking. |

---

## Per language

### Python

```bash
pip install --break-system-packages lizard vulture radon import-linter pip-audit

python3 scripts/pyast.py . --entry myapp        # reachability, hotspots, masking
lizard . -C 10 -a 5                              # complexity > 10, arity > 5
vulture . --min-confidence 80                    # see trap below
lint-imports                                     # layer contracts, if configured
pip-audit                                        # known CVEs
```

`import-linter` is the highest-value addition for a project with real layering.
Six lines of config turn "domain must not import adapters" into a failing check:

```ini
[importlinter]
root_package = myapp

[importlinter:contract:layers]
name = Layered architecture
type = layers
exhaustive = true
containers = myapp
layers = api services domain
```

`exhaustive = true` matters: a new subpackage must be explicitly placed, so the
architecture cannot quietly grow a layer.

### TypeScript / JavaScript

```bash
npm install -D knip dependency-cruiser
npx knip                                   # unused files, exports, deps
npx depcruise src --validate               # layer + cycle rules
npx jscpd src --min-tokens 50 --mode weak
npm audit
```

`knip --fix` will remove most dead exports automatically. Review the diff;
dynamic patterns need human eyes.

### Other languages

`jscpd` (200+ languages) and `lizard` (most mainstream languages) work
everywhere and cover duplication and complexity without per-language setup. For
reachability, the language's own tooling is usually better: `go vet` and
`staticcheck` for Go, `cargo udeps` for Rust, ArchUnit for Java.

---

## Verified traps

These were measured on a controlled fixture, not assumed.

### vulture has a confidence cliff

On a tree with genuinely orphaned modules:

| `--min-confidence` | Findings |
|---|---|
| 60 | 12 — including live API handlers and every service class |
| 80 | 0 |
| 90 | 0 |
| 100 | 0 |

At 60 it flags live entry points as dead. At 80 it misses genuinely dead
modules. There is no setting that gives a usable answer for library-shaped code,
because it reasons about names rather than reachability. Use import-graph
reachability (`pyast.py`) as the primary signal and vulture only as a secondary
hint about unused locals.

### jscpd's percentage is a function of its config

Same code, only `--min-tokens` varied:

| `--min-tokens` | Duplication | Clones |
|---|---|---|
| 20 | 36.08% | 5 |
| 30 | 38.51% | 5 |
| 40 | 35.14% | 4 |
| 50 | 28.99% | 2 |
| 100 | 28.99% | 2 |

A 10-point swing, non-monotonic. Any target like "keep duplication under 3%" is
meaningless unless the config is pinned alongside it. Pick a setting, commit
`.jscpd.json`, and compare only like to like.

Also: the percentage falls as a codebase grows even while absolute duplication
rises. Gate `duplicated_lines` and `clone_count`, not the percentage. See
`references/bloat-playbook.md`.

Useful flags: `--mode weak` skips comment tokens, so reformatted comments do not
register as clones. The `ai` reporter emits a much more compact report intended
for feeding to a model.

### knip's entry-point config is load-bearing

Miss an entry point and live code reads as dead. Over-broaden it and real dead
code hides. Configure `entry` and `project` explicitly and re-check after adding
any new build target. This is the single biggest source of knip false positives,
and it is a configuration problem, not a tool problem.

### `sg` is not ast-grep on Linux

`sg` is a coreutils binary for running a command with a different group ID, and
it shadows ast-grep's short alias. Verified present at `/usr/bin/sg` on a stock
Ubuntu image. Invoke `ast-grep` by its full name in any script.

### Audit tools do not catch phantom packages

`npm audit` and `pip-audit` check installed packages against vulnerability
databases. A hallucinated package that nobody has registered yet is not in any
database, is not installed, and produces a clean audit. Verify existence
separately:

```bash
pip index versions <pkg>
npm view <pkg> versions
```

If an attacker *has* registered it, audit still returns clean — the package is
new, not known-vulnerable. Existence is not safety. Check registration date and
publisher history for anything an agent introduced that you have not heard of.

---

## Structural search with AST patterns

`ast-grep` matches syntax rather than text, so it finds patterns that grep
cannot express without false positives. Patterns are written as code with
metavariables:

```bash
# swallowed exceptions, regardless of formatting or exception type
ast-grep --pattern 'try { $$$ } catch ($E) { }' --lang ts

# a promise chain with no rejection handler
ast-grep --pattern '$A.then($B)' --lang ts

# Python: bare except
ast-grep --pattern 'try:
    $$$
except:
    $$$' --lang python
```

Reach for this when you have identified a slop pattern specific to your codebase
and want to find every instance and gate against new ones. It is the right tool
for "we keep doing X, stop us" — write the rule once, run it forever. A `sgconfig.yml`
with a `ruleDirs` entry turns a set of these into a project linter.

Use `semgrep` instead when the concern is security and you want a maintained
ruleset rather than rules you write yourself.
