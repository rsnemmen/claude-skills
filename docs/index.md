# Claude Code Skills

A collection of custom Claude Code skills (slash commands) for personal use. Each skill lives in its own subdirectory under `skills/` as a `SKILL.md` file and is installed by symlinking that directory into `~/.claude/skills/`.

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| [`codebase-improve`](skills/codebase-improve.md) | `/codebase-improve [scope] [focus]` | Audits a codebase and proposes the top 5 improvements ranked by severity, with file:line citations. Read-only — never modifies code. |
| [`bootstrap-docs`](skills/bootstrap-docs.md) | `/bootstrap-docs [--scaffold] [stack] [focus]` | Researches and recommends a documentation-site stack for the current codebase (Phase 1, read-only), then scaffolds it with real starter content from README and source on confirmation (Phase 2). GitHub Pages deploy only. |

- [Installation](installation.md) — how to install skills via the one-line installer or by cloning the repo.
- [Contributing](contributing.md) — skill file format, naming conventions, and how to add a new skill.

---

To preview locally: `mkdocs serve`. To publish to GitHub Pages: `mkdocs gh-deploy`.
