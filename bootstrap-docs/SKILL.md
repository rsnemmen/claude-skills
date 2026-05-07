---
name: bootstrap-docs
description: Research, recommend, and scaffold a documentation website for the current codebase. Use when the user asks to "set up docs", "add a docs site", "bootstrap documentation", "make a documentation website", "publish docs to GitHub Pages", "add MkDocs/Docusaurus/Sphinx/Starlight to this repo", or asks which docs generator fits this project. Two-phase: Phase 1 recommends a stack with rationale (read-only); Phase 2 scaffolds files with real content only after the user confirms or passes --scaffold.
argument-hint: [--scaffold] [stack] [focus] — empty for Phase 1; --scaffold to accept recommendation; --scaffold <mkdocs|docusaurus|sphinx|hugo|starlight|vitepress|readme> to override
allowed-tools: [Read, Glob, Grep, Bash, Write, Edit, Agent]
---

# Documentation Site Bootstrap

Research the right docs stack for this codebase, recommend it with honest tradeoffs, and on confirmation scaffold a starter site with real content drawn from the repo — never fabricated.

## Arguments

The user invoked this skill with: $ARGUMENTS

Parse `$ARGUMENTS` as free text. Recognize:

- **empty** → Phase 1, broad stack research.
- **`--scaffold` alone** → Phase 2 with the stack just recommended in this conversation (or MkDocs Material if no recommendation is in scope).
- **`--scaffold <stack>`** → skip Phase 1 entirely; scaffold the named stack (`mkdocs`, `docusaurus`, `sphinx`, `hugo`, `starlight`, `vitepress`, `readme`).
- **bare stack name** → bias Phase 1 toward that stack but still run the research and push back with evidence if the codebase doesn't fit.
- **trailing focus word** (`api-only`, `tutorial-heavy`, `minimal`) → influence the stack choice and the nav shape in Phase 2.

## Phase detection

Determine which phase to run by checking in this order:

1. `$ARGUMENTS` contains `--scaffold` → **Phase 2.**
2. The working directory already has `mkdocs.yml`, `docusaurus.config.js`, `conf.py` alongside a `docs/`, `astro.config.*` (with Starlight), or `.vitepress/` → **Phase 2-augment**: add missing pages and update nav; never overwrite existing config or pages.
3. Otherwise → **Phase 1.**

Do not infer Phase 2 from a prior recommendation in the conversation without the explicit `--scaffold` flag.

## Phase 1 — Research and recommend (read-only)

### 1. Read the project context

Read `README.md`, `CLAUDE.md`/`AGENTS.md`, the top-level directory listing, any existing `docs/` folder, and the primary package manifest (`pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`). If the language is still unclear after these, sample 5–10 source files. Note `.github/workflows/` for any existing deploy hints.

### 2. Explore with codebase-specific questions

Launch up to 3 `Explore` agents in a single message, each focused on a concrete question about *this* codebase: what is the public surface (CLI scripts, library API, web routes, notebooks)? Is there existing prose worth migrating? Are there docstrings or inline comments rich enough to justify autodoc?

### 3. Weigh the stacks

Evaluate at least: MkDocs+Material, Docusaurus, Sphinx, Hugo, Astro Starlight, VitePress, plain README/GitHub Wiki. Apply this rubric:

- **Python library with rich docstrings** → Sphinx autodoc earns its setup cost; Furo or sphinx-rtd-theme as the default theme.
- **Shell scripts, data pipelines, notebooks, mixed-language tools** → MkDocs+Material; autodoc contributes nothing here; user's stated bias toward "simplicity to maintain" weights this upward.
- **JS/TS library or React app** → Docusaurus or Astro Starlight.
- **Tiny repo (<10 files, <500 LOC total)** → recommend a polished `README.md` + optional GitHub Wiki; don't bootstrap a full site.
- **Monorepo with multiple top-level packages** → ask in the Phase 1 output whether the site should cover the umbrella or one package; default to umbrella with a section per package.
- **No `README.md`** → say so; recommend writing one first; do not proceed to scaffold.
- User's stated bias toward "simplicity to maintain" weights MkDocs upward when fit is roughly equal across stacks.

### 4. Deliver the recommendation

Write the recommendation in themed prose (see Output style). Cover in any order that reads well: what you found in the codebase (with `file:line` evidence), the recommended stack in one short rationale paragraph, 1–2 honest alternatives each in one paragraph naming the specific tradeoff — not a feature list, the deploy story in one line (e.g. `mkdocs gh-deploy`), and close with: *"Re-invoke with `--scaffold` to accept, or `--scaffold <stack>` to override."*

**Stop here.** Do not write any files, create directories, run `pip install` or `npm install`, or execute any mutating command.

## Phase 2 — Scaffold (write-mode)

### 1. Re-read the codebase

Read `README.md` and the top-level directory listing fresh. Do not rely on Phase 1 memory alone.

### 2. Plan the nav

Each top-level source directory or major README section becomes one page. Hand-curate a `nav:` block — no `awesome-pages` plugin, no auto-discovery. If the codebase is too large (hundreds of modules) to scaffold fully in one turn, cover the top two nav levels and append a short "Next pages to add" list at the end of `docs/index.md` rather than attempting everything at once.

### 3. MkDocs Material scaffold (worked example — the most likely pick)

Write these files, derived from real codebase content only:

**`mkdocs.yml`** — use this structure:

```yaml
site_name: <project name from README H1 or repository directory name>
site_description: <first sentence of README, or a one-line description>
site_author: <git config user.name if readable via Bash; omit if not>
site_url: <inferred from git remote get-url origin; comment out with a TODO line if no remote>

theme:
  name: material
  features:
    - navigation.sections
    - navigation.top
    - search.highlight
    - content.code.copy

nav:
  - Overview: index.md
  # one entry per section page

markdown_extensions:
  - tables
  - fenced_code
```

**`docs/index.md`**:
- H1 title
- One paragraph sourced verbatim or lightly adapted from the README's opening description
- A Categories table: `| [Section title](page.md) | Source directory or module | One-line description |`
- Optional Dependencies Summary table if external tools are enumerable from README or source
- At the bottom: *"To preview locally: `mkdocs serve`. To publish to GitHub Pages: `mkdocs gh-deploy`."*

**`docs/<page>.md`** for each nav entry:
- H1 matching the nav label
- `**Dependencies:** tool1, tool2, …` sourced from README or source files; omit if none apply
- A summary table: `| Item | Description |` — descriptions drawn from existing comments, docstrings, or `--help` output; write "TODO: describe" when no real source is available
- `---` separator
- `## Usage` header
- One `### item-name` subsection per item, each with a fenced `sh` or language-appropriate code block showing invocation, followed by 1–3 sentences of prose. All content must trace to real README text, source comments, or help output. When no real text exists, write a one-line "TODO: add description" — never invent plausible-sounding content.

### 4. Other stacks

For **Docusaurus, Astro Starlight, VitePress**: do not run `npx create-*` (interactive and requires network). Write the config file (`docusaurus.config.js` / `astro.config.mjs` / `.vitepress/config.ts`) and the `docs/` content tree directly following the same content-from-real-sources rule, then print the exact `npm install` and dev-server commands for the user to run.

For **Sphinx**: write `conf.py`, `index.rst`, `Makefile`, and one autodoc-driven `.rst` page per top-level Python package. Print `pip install sphinx <theme>` for the user; do not execute it.

For **Hugo**: write `hugo.toml`, `content/_index.md`, and per-section content pages. Print the theme-install step for the user; do not execute it.

For **README/Wiki**: rewrite `README.md` as a richer single-file guide with anchored sections and a table of contents. Do not create a site or generator config.

### 5. Post-scaffold summary

Print: the list of files created, what the user should review for correctness (especially item descriptions sourced from sparse comments), the exact command to preview locally, and — if the user passed a stack that didn't match the Phase 1 recommendation — a one-sentence note on the tradeoff accepted.

## Constraints

- **Phase 1 is strictly read-only.** No `Write`, no `Edit`, no `mkdir`, no `pip install`, no `npm install`, no mutating `Bash` command.
- **Phase 2 must not overwrite.** If `mkdocs.yml`, `docs/index.md`, or any target page already exists, read it, compare against what would be written, and propose the diff inline rather than overwriting.
- **Never invent content.** Every description, code block, and prose sentence must trace to real source: README, comments, docstrings, or `--help` output. When no real source exists, write "TODO: describe" — not plausible-sounding guesses.
- **Never execute deploy or install commands.** `mkdocs gh-deploy`, `git push`, `pip install`, `npm install` — print these for the user; do not run them.
- **Respect a stack override.** If the user passed `--scaffold sphinx` for a shell-script repo, scaffold Sphinx and note the mismatch in the post-scaffold summary — do not refuse or silently substitute.
- **Cite evidence in Phase 1** inline, the same way `codebase-improve` does: weave `file:line` references and short quotes or paraphrases into sentences, not into separate fields.

## Output style

**Phase 1:** Themed prose — no rigid template. Lead with the single most important takeaway. Weave `file:line` evidence into sentences (e.g. "60+ scripts across 10 directories (`README.md:18-29`) cluster naturally into per-category pages…"). Each alternative gets one paragraph naming its specific tradeoff, not a feature list. No severity labels, no emojis, no formal "Alternatives considered" header. If no meaningful docs gap exists (tiny repo, everything already documented), say so plainly.

**Phase 2:** Concrete and procedural — state what each file contains as you create it, then print the summary. One short paragraph at the end naming what to review. No padding.
