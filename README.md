# Custom Claude Code and Codex CLI skills

Personal collection of custom Claude Code slash commands and Codex CLI skills. Full docs: <https://rsnemmen.github.io/claude-skills/>.

## Skills

- **`codebase-improve`** — audit a codebase and propose ranked improvements with file:line citations. Read-only.

## Quick install

Claude Code:

```sh
curl -fsSLo /tmp/install-claude-skills.py https://raw.githubusercontent.com/rsnemmen/claude-skills/main/install-skills.py && python3 /tmp/install-claude-skills.py
```

Codex CLI:

```sh
curl -fsSLo /tmp/install-skills.py https://raw.githubusercontent.com/rsnemmen/claude-skills/main/install-skills.py && python3 /tmp/install-skills.py --target codex
```

For the clone/symlink workflow, installer flags, and per-skill usage, see the [docs](https://rsnemmen.github.io/claude-skills/).

## Contributing

Skill file format and how to add a new skill: <https://rsnemmen.github.io/claude-skills/contributing/>.
