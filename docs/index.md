# Claude Code and Codex CLI Skills

A collection of custom Claude Code skills and Codex CLI skills for personal use. Claude Code skills live under `skills/`; Codex-compatible copies live under `codex-skills/`.

## Skills

| Skill | Claude Code trigger | Codex CLI trigger | Description |
|-------|---------------------|-------------------|-------------|
| [`codebase-improve`](skills/codebase-improve.md) | `/codebase-improve [scope] [focus]` | Natural-language audit or improvement request | Audits a codebase and proposes concrete improvements with file:line citations. Read-only; never modifies code. |

- [Installation](installation.md) — how to install skills via the one-line installer or by cloning the repo.
- [Contributing](contributing.md) — skill file format, naming conventions, and how to add a new skill.

---

To preview locally: `mkdocs serve`. To publish to GitHub Pages: `mkdocs gh-deploy`.
