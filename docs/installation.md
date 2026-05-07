# Installation

Claude Code reads skills from `~/.claude/skills/<name>/SKILL.md` (user scope — available in every session) or `<project>/.claude/skills/<name>/SKILL.md` (project scope).

## One-line install

To install without cloning this repo, download and run the interactive installer:

```sh
curl -fsSLo /tmp/install-claude-skills.py https://raw.githubusercontent.com/rsnemmen/claude-skills/main/install-skills.py && python3 /tmp/install-claude-skills.py
```

The installer lists available skills and copies your selections to `~/.claude/skills/<skill-name>/`.

## From a clone

```sh
git clone https://github.com/rsnemmen/claude-skills.git ~/claude-skills
ln -s ~/claude-skills/skills/codebase-improve ~/.claude/skills/codebase-improve
```

Symlinking (rather than copying) means `git pull` updates your installed skills automatically. For project scope, symlink under `<project>/.claude/skills/` instead.

## Installer options

| Flag | Description |
|------|-------------|
| `--archive-url URL` | Zip archive URL to install from. Default: `https://github.com/rsnemmen/claude-skills/archive/refs/heads/main.zip` |
| `--install-dir PATH` | Install destination. Default: `~/.claude/skills` |
| `--source PATH` | Use a local checkout as the source instead of downloading. |
| `--status` | Print install status for every skill and exit without installing. |
| `--no-color` | Disable ANSI color output. |
| `--no-tui` | Force the text-based numeric menu instead of the interactive TUI. |
| `--link` | Install as symlinks (default when source is local). |
| `--copy` | Install as copies (default when source is downloaded). |
