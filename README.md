# Custom Claude Code skills.

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `codebase-improve` | `/codebase-improve [scope] [focus]` | Audits a codebase and proposes the top 5 improvements ranked by severity, with file:line citations. Read-only — never modifies code. |
| `bootstrap-docs` | `/bootstrap-docs [--scaffold] [stack] [focus]` | Researches and recommends a documentation-site stack for the current codebase (Phase 1, read-only), then scaffolds it with real starter content from README and source on confirmation (Phase 2). GitHub Pages deploy only. |

## Installation

Claude Code reads skills from `~/.claude/skills/<name>/SKILL.md` (user scope — available in every session) or `<project>/.claude/skills/<name>/SKILL.md` (project scope).

To install without cloning this repo, download and run the interactive installer:

```sh
curl -fsSLo /tmp/install-claude-skills.py https://raw.githubusercontent.com/rsnemmen/claude-skills/main/install-skills.py && python3 /tmp/install-claude-skills.py
```

The installer lists available skills and copies your selections to `~/.claude/skills/<skill-name>/`.

For development, clone this repo and symlink the skills you want:

```sh
git clone https://github.com/rsnemmen/claude-skills.git ~/claude-skills
ln -s ~/claude-skills/codebase-improve ~/.claude/skills/codebase-improve
```

Symlinking (rather than copying) means `git pull` updates your installed skills automatically. For project scope, symlink under `<project>/.claude/skills/` instead.

## Usage

Type `/<skill-name>` in a Claude Code session to invoke a skill.

### Examples

`codebase-improve` accepts an optional `[scope] [focus]` argument:

```
/codebase-improve
```
No arguments — broad sweep across the whole codebase.

```
/codebase-improve fortran/ performance
```
Scoped to the `fortran/` directory, performance focus.

```
/codebase-improve perl/ maintainability
```
Scoped to the `perl/` wrappers, maintainability focus.
