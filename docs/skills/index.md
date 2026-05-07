# Skills

Type `/<skill-name>` in a Claude Code session to invoke a skill.

| Skill | Trigger | Argument hint | Description |
|-------|---------|---------------|-------------|
| [`codebase-improve`](codebase-improve.md) | `/codebase-improve` | `[scope] [focus]` — e.g. "fortran/ performance" or "whole codebase maintainability" | Audits a codebase and proposes the top 5 improvements ranked by severity, with file:line citations. Read-only — never modifies code. |
| [`bootstrap-docs`](bootstrap-docs.md) | `/bootstrap-docs` | `[--scaffold] [stack] [focus]` — empty for Phase 1; `--scaffold` to accept recommendation; `--scaffold <mkdocs\|docusaurus\|sphinx\|hugo\|starlight\|vitepress\|readme>` to override | Researches and recommends a documentation-site stack for the current codebase (Phase 1, read-only), then scaffolds it with real starter content from README and source on confirmation (Phase 2). GitHub Pages deploy only. |
