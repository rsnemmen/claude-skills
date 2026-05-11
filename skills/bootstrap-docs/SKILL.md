---
name: bootstrap-docs
description: 'Research, recommend, and scaffold a documentation website for the current codebase. Use when the user asks to set up docs, add a docs site, bootstrap documentation, make a documentation website, publish docs to GitHub Pages, add MkDocs/Docusaurus/Sphinx/Starlight to this repo, or asks which docs generator fits this project. Two-phase: Phase 1 recommends a stack with rationale; Phase 2 scaffolds files with real content only after the user confirms.'
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion]
---

# Documentation Site Bootstrap

Research the right docs stack for this codebase, recommend it with honest tradeoffs, and on confirmation scaffold a starter site with real content drawn from the repo. Never fabricate content.

## Request handling

Recognize:

- Empty or general docs request: Phase 1, broad stack research.
- Explicit scaffold request: Phase 2 with the stack just recommended in this conversation, or MkDocs Material if no recommendation is in scope.
- Explicit stack request while asking to scaffold: skip Phase 1 and scaffold the named stack.
- Bare stack preference without a scaffold request: bias Phase 1 toward that stack but still run the research and push back with evidence if the codebase does not fit.

## Phase detection

Determine which phase to run:

1. The user explicitly asks to scaffold or create files → Phase 2.
2. The working directory already has `mkdocs.yml`, `docusaurus.config.js`, `conf.py` alongside `docs/`, or `astro.config.*` with Starlight → Phase 2-augment: add missing pages and update nav; never overwrite existing config or pages.
3. Otherwise → Phase 1.

Do not infer Phase 2 from a prior recommendation unless the user explicitly confirms.

## Phase 1 — Research and recommend

### 1. Read the project context

Read `README.md`, `CLAUDE.md`, the top-level directory listing, any existing `docs/` folder, and the primary package manifest (`pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`). If the language is still unclear, sample 5–10 source files. Note `.github/workflows/` for deploy hints.

### 2. Weigh the stacks

Evaluate at least: MkDocs+Material, Docusaurus, Sphinx, Astro Starlight, VitePress, plain README/GitHub Wiki. Apply this rubric:

- Python library with rich docstrings → Sphinx autodoc; Furo or sphinx-rtd-theme.
- Shell scripts, data pipelines, notebooks, mixed-language → MkDocs+Material.
- JS/TS library or React app → Docusaurus or Astro Starlight.
- Tiny repo (<500 LOC total) → polished `README.md`; do not bootstrap a full site.
- Monorepo with multiple packages → ask whether the site covers the umbrella or one package.
- No `README.md` → say so, recommend writing one first, do not proceed to scaffold.

### 3. Deliver the recommendation

Open with:

```
## Recommended: <Stack Name>

<One sentence: the single strongest reason this stack fits this codebase, with a file:line cite.>
Deploy: `<deploy command>`
```

Then write a short rationale paragraph with `file:line` evidence, 1–2 alternatives with specific tradeoffs, and a compact options table.

Use `AskUserQuestion` to let the user confirm or switch stacks before proceeding.

Stop after Phase 1. Do not write files, create directories, install dependencies, or run mutating commands.

## Phase 2 — Scaffold

### 1. Re-read the codebase

Read `README.md` and the top-level directory listing fresh. Do not rely on Phase 1 memory alone.

### 2. Announce the plan before writing

```
## Scaffold plan — <Stack Name>

Files to create:
- `mkdocs.yml` — site config with nav
- `docs/index.md` — overview from README
- `docs/<page>.md` — <description> (×N)

Preview: `<dev-server command>`
Deploy:  `<deploy command>`

Creating files now…
```

### 3. Stack-specific scaffold

**MkDocs Material** — write `mkdocs.yml` (theme: material, nav, plugins: [search], repo_url if detectable), `docs/index.md` drawn from README, one page per major section. Include `requirements-docs.txt` with `mkdocs-material`.

**Sphinx** — write `docs/conf.py` (extensions: autodoc, napoleon; theme: furo), `docs/index.rst` with toctree, stub `.rst` files per section. Include `requirements-docs.txt`.

**Docusaurus / Astro Starlight / VitePress** — write config and content files directly. Print the exact install and dev-server commands for the user; do not run install commands yourself.

**README/Wiki** — rewrite `README.md` as a richer single-file guide: badges, anchored ToC, Installation, Usage, API reference, Contributing, License. Do not create a generator config.

### 4. Post-scaffold summary

List files created, what the user should review for correctness, the exact preview command, and a one-sentence note if they chose a stack that does not match the Phase 1 recommendation.

## Constraints

- Phase 1 is strictly read-only.
- Phase 2 must not overwrite existing target files. If a target exists, read it, compare, and propose the diff inline instead of overwriting.
- Never invent content. Every sentence must trace to README, comments, docstrings, or `--help` output. Write `TODO: describe` when no real source exists.
- Never execute deploy or install commands.
- Cite evidence in Phase 1 with `file:line` references.
