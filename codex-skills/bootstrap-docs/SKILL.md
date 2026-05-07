---
name: bootstrap-docs
description: 'Research, recommend, and scaffold a documentation website for the current codebase. Use when the user asks to set up docs, add a docs site, bootstrap documentation, make a documentation website, publish docs to GitHub Pages, add MkDocs/Docusaurus/Sphinx/Starlight to this repo, or asks which docs generator fits this project. Two-phase: Phase 1 recommends a stack with rationale; Phase 2 scaffolds files with real content only after the user confirms.'
metadata:
  short-description: Recommend and scaffold a documentation site
---

# Documentation Site Bootstrap

Research the right docs stack for this codebase, recommend it with honest tradeoffs, and on confirmation scaffold a starter site with real content drawn from the repo. Never fabricate content.

## Request handling

Interpret the user's request as free text. Recognize:

- Empty or general docs request: Phase 1, broad stack research.
- Explicit scaffold request: Phase 2 with the stack just recommended in this conversation, or MkDocs Material if no recommendation is in scope.
- Explicit stack request while asking to scaffold: skip Phase 1 and scaffold the named stack (`mkdocs`, `docusaurus`, `sphinx`, `hugo`, `starlight`, `vitepress`, `readme`).
- Bare stack preference without a scaffold request: bias Phase 1 toward that stack but still run the research and push back with evidence if the codebase does not fit.
- Focus words such as `api-only`, `tutorial-heavy`, or `minimal`: use them to influence the stack choice and nav shape.

## Phase detection

Determine which phase to run by checking in this order:

1. The user explicitly asks to scaffold or create files: Phase 2.
2. The working directory already has `mkdocs.yml`, `docusaurus.config.js`, `conf.py` alongside `docs/`, `astro.config.*` with Starlight, or `.vitepress/`: Phase 2-augment. Add missing pages and update nav; never overwrite existing config or pages.
3. Otherwise: Phase 1.

Do not infer Phase 2 from a prior recommendation unless the user explicitly confirms scaffolding or asks to create the files.

## Phase 1 - Research and recommend

### 1. Read the project context

Read `README.md`, `AGENTS.md`/`CLAUDE.md`, the top-level directory listing, any existing `docs/` folder, and the primary package manifest (`pyproject.toml`, `package.json`, `Cargo.toml`, `go.mod`). If the language is still unclear after these, sample 5-10 source files. Note `.github/workflows/` for deploy hints.

### 2. Explore with codebase-specific questions

Use `rg`, `rg --files`, and targeted file reads to identify the public surface, existing prose worth migrating, and whether docstrings or comments are rich enough to support autodoc. If active Codex instructions allow subagents and parallel exploration is useful, launch up to 3 explorer agents in one batch with concrete codebase-specific questions.

### 3. Weigh the stacks

Evaluate at least: MkDocs+Material, Docusaurus, Sphinx, Hugo, Astro Starlight, VitePress, plain README/GitHub Wiki. Apply this rubric:

- Python library with rich docstrings: Sphinx autodoc earns its setup cost; Furo or sphinx-rtd-theme is the default theme.
- Shell scripts, data pipelines, notebooks, mixed-language tools: MkDocs+Material; autodoc contributes nothing here.
- JS/TS library or React app: Docusaurus or Astro Starlight.
- Tiny repo under 10 files and 500 LOC total: recommend a polished `README.md` plus optional GitHub Wiki; do not bootstrap a full site.
- Monorepo with multiple top-level packages: ask whether the site should cover the umbrella or one package; default to umbrella with a section per package.
- No `README.md`: say so, recommend writing one first, and do not proceed to scaffold.
- A stated bias toward simplicity to maintain weights MkDocs upward when fit is roughly equal.

### 4. Deliver the recommendation

Open with this block:

```markdown
## Recommended: <Stack Name>

<One sentence: the single strongest reason this stack fits this codebase, with a file:line cite.>
Deploy: `<deploy command>`
```

Then write one short rationale paragraph with `file:line` evidence, 1-2 worthwhile alternatives with specific tradeoffs, and a compact options table showing the recommended stack first.

Stop after Phase 1. Do not write files, create directories, install dependencies, or run mutating commands.

## Phase 2 - Scaffold

### 1. Re-read the codebase

Read `README.md` and the top-level directory listing fresh. Do not rely on Phase 1 memory alone.

### 2. Announce the file plan before writing

Before creating any file, print:

```markdown
## Scaffold plan - <Stack Name>

Files to create:
- `mkdocs.yml` - site config with nav
- `docs/index.md` - overview page from README
- `docs/<page>.md` - <one-phrase description> (xN)

Run command to preview: `<dev-server command>`
Run command to deploy: `<deploy command>`

Creating files now...
```

Then proceed.

### 3. Plan the nav

Each top-level source directory or major README section becomes one page. Hand-curate nav; do not use auto-discovery. If the codebase is too large to scaffold fully in one turn, cover the top two nav levels and append a short "Next pages to add" list at the end of `docs/index.md`.

### 4. Stack-specific scaffold

For MkDocs Material, write `mkdocs.yml`, `docs/index.md`, and one page per nav entry using real README/source content only.

For Docusaurus, Astro Starlight, VitePress, Sphinx, and Hugo, write config and content files directly. Do not run network-backed generators or install commands. Print the exact install and dev-server commands for the user.

For README/Wiki, rewrite `README.md` as a richer single-file guide with anchored sections and a table of contents. Do not create a site or generator config.

### 5. Post-scaffold summary

Print the files created, what the user should review for correctness, the exact preview command, and a one-sentence note if the user chose a stack that does not match the Phase 1 recommendation.

## Constraints

- Phase 1 is strictly read-only.
- Phase 2 must not overwrite existing target files. If a target exists, read it, compare against what would be written, and propose the diff inline instead of overwriting.
- Never invent content. Every description, code block, and prose sentence must trace to README, comments, docstrings, or `--help` output. Write "TODO: describe" when no real source exists.
- Never execute deploy or install commands.
- Respect a stack override and note the tradeoff.
- Cite evidence in Phase 1 inline with file:line references.

## Output style

Phase 1: Lead with the `## Recommended:` block, then rationale, alternatives, and options table.

Phase 2: Concrete and procedural. State what each file contains as you create it, then print the summary.
