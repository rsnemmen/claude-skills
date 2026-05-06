# cc-skills

Custom Claude Code skills.

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `codebase-improve` | `/codebase-improve [scope] [focus]` | Audits a codebase and proposes the top 5 improvements ranked by severity, with file:line citations. Read-only — never modifies code. |

## Installation

Claude Code reads skills from `~/.claude/skills/<name>/SKILL.md` (user scope — available in every session) or `<project>/.claude/skills/<name>/SKILL.md` (project scope).

Clone this repo and symlink the skills you want:

```sh
git clone https://github.com/rsnemmen/cc-skills.git ~/cc-skills
ln -s ~/cc-skills/codebase-improve ~/.claude/skills/codebase-improve
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
