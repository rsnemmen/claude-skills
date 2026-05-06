# cc-skills

Custom Claude Code skills.

## Skills

| Skill | Trigger | Description |
|-------|---------|-------------|
| `codebase-improve` | `/codebase-improve [scope] [focus]` | Audits a codebase and proposes the top 5 improvements ranked by severity, with file:line citations. Read-only — never modifies code. |

## Usage

Skills live in subdirectories, each containing a `SKILL.md` that defines the skill's behavior. Claude Code picks them up automatically when this directory is configured as a skill source.

To invoke a skill, type `/skill-name` in a Claude Code session.
