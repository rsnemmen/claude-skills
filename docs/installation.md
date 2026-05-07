# Installation

Claude Code reads skills from `~/.claude/skills/<name>/SKILL.md` (user scope, available in every session) or `<project>/.claude/skills/<name>/SKILL.md` (project scope). Codex CLI reads user skills from `${CODEX_HOME:-$HOME/.codex}/skills/<name>/SKILL.md`.

## One-line install

To install Claude Code skills without cloning this repo, download and run the interactive installer:

```sh
curl -fsSLo /tmp/install-claude-skills.py https://raw.githubusercontent.com/rsnemmen/claude-skills/main/install-skills.py && python3 /tmp/install-claude-skills.py
```

To install Codex CLI skills:

```sh
curl -fsSLo /tmp/install-skills.py https://raw.githubusercontent.com/rsnemmen/claude-skills/main/install-skills.py && python3 /tmp/install-skills.py --target codex
```

To install both variants:

```sh
curl -fsSLo /tmp/install-skills.py https://raw.githubusercontent.com/rsnemmen/claude-skills/main/install-skills.py && python3 /tmp/install-skills.py --target both
```

The installer lists available skills and copies your selections to the selected platform's user skills directory.

## From a clone

```sh
git clone https://github.com/rsnemmen/claude-skills.git ~/claude-skills
ln -s ~/claude-skills/skills/codebase-improve ~/.claude/skills/codebase-improve
ln -s ~/claude-skills/codex-skills/codebase-improve ${CODEX_HOME:-$HOME/.codex}/skills/codebase-improve
```

Symlinking (rather than copying) means `git pull` updates your installed skills automatically. For Claude project scope, symlink under `<project>/.claude/skills/` instead.

## Installer options

| Flag | Description |
|------|-------------|
| `--archive-url URL` | Zip archive URL to install from. Default: `https://github.com/rsnemmen/claude-skills/archive/refs/heads/main.zip` |
| `--target claude\|codex\|both` | Install target. Omit for interactive target selection; defaults to `claude` for status/non-interactive compatibility. |
| `--install-dir PATH` | Single-target install destination override. Cannot be used with `--target both`. |
| `--claude-install-dir PATH` | Claude Code install destination. Default: `~/.claude/skills` |
| `--codex-install-dir PATH` | Codex CLI install destination. Default: `${CODEX_HOME:-$HOME/.codex}/skills` |
| `--source PATH` | Use a local checkout as the source instead of downloading. |
| `--status` | Print install status for every skill and exit without installing. |
| `--no-color` | Disable ANSI color output. |
| `--no-tui` | Force the text-based numeric menu instead of the interactive TUI. |
| `--link` | Install as symlinks (default when source is local). |
| `--copy` | Install as copies (default when source is downloaded). |
