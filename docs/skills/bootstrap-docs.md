# bootstrap-docs

!!! info "Skill metadata"
    - **Name:** `bootstrap-docs`
    - **Argument hint:** `[--scaffold] [stack] [focus]` — empty for Phase 1; `--scaffold` to accept recommendation; `--scaffold <mkdocs|docusaurus|sphinx|hugo|starlight|vitepress|readme>` to override
    - **Allowed tools:** `Read`, `Glob`, `Grep`, `Bash`, `Write`, `Edit`, `Agent`

## What it does

Research, recommend, and scaffold a documentation website for the current codebase. Two-phase: Phase 1 recommends a stack with rationale (read-only); Phase 2 scaffolds files with real content only after the user confirms or passes `--scaffold`.

## Arguments

Parse arguments as free text. Recognize:

- **empty** → Phase 1, broad stack research.
- **`--scaffold` alone** → Phase 2 with the stack just recommended in this conversation (or MkDocs Material if no recommendation is in scope).
- **`--scaffold <stack>`** → skip Phase 1 entirely; scaffold the named stack (`mkdocs`, `docusaurus`, `sphinx`, `hugo`, `starlight`, `vitepress`, `readme`).
- **bare stack name** → bias Phase 1 toward that stack but still run the research and push back with evidence if the codebase doesn't fit.
- **trailing focus word** (`api-only`, `tutorial-heavy`, `minimal`) → influence the stack choice and the nav shape in Phase 2.

## Phases

- **Phase 1 — Research and recommend (read-only):** Reads project docs and source structure, weighs docs stacks against a rubric (MkDocs+Material, Docusaurus, Sphinx, Hugo, Starlight, VitePress, plain README), and delivers a recommendation in themed prose with `file:line` evidence and honest tradeoffs. Writes no files.
- **Phase 2 — Scaffold (write-mode):** Triggered by `--scaffold`. Re-reads the codebase fresh, plans the nav, and writes `mkdocs.yml` + all `docs/` pages with content drawn from real sources only (README, comments, docstrings, `--help` output). Never overwrites existing files — proposes a diff instead.

## Constraints

- **Phase 1 is strictly read-only.** No `Write`, no `Edit`, no `mkdir`, no `pip install`, no `npm install`, no mutating `Bash` command.
- **Phase 2 must not overwrite.** If `mkdocs.yml`, `docs/index.md`, or any target page already exists, read it, compare against what would be written, and propose the diff inline rather than overwriting.
- **Never invent content.** Every description, code block, and prose sentence must trace to real source: README, comments, docstrings, or `--help` output. When no real source exists, write "TODO: describe" — not plausible-sounding guesses.
- **Never execute deploy or install commands.** `mkdocs gh-deploy`, `git push`, `pip install`, `npm install` — print these for the user; do not run them.
- **Respect a stack override.** If the user passed `--scaffold sphinx` for a shell-script repo, scaffold Sphinx and note the mismatch in the post-scaffold summary — do not refuse or silently substitute.
