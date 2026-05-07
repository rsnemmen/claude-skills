# Repository Guidelines

## Project Structure & Module Organization

This repository stores custom Claude Code skills. Each skill lives in its own directory under `skills/` and contains a `SKILL.md` file, for example `skills/codebase-improve/SKILL.md`. Repository-level documentation lives in `README.md` and `CLAUDE.md`; keep both aligned with any skill additions or behavior changes. There is no separate source, test, or asset tree at present.

## Build, Test, and Development Commands

There is no build step for this Markdown-only repository. Useful commands are:

```sh
rg --files
```

Lists tracked project files quickly when checking structure.

```sh
ln -s ~/cc-skills/skills/<skill-name> ~/.claude/skills/<skill-name>
```

Installs a skill for local Claude Code use by symlinking the skill directory.

```sh
git diff -- README.md CLAUDE.md skills/<skill-name>/SKILL.md
```

Reviews documentation and prompt changes before committing.

## Coding Style & Naming Conventions

Use one directory per skill, and make the directory name match the `name` field in the `SKILL.md` frontmatter. Skill files must start with YAML frontmatter containing `name`, `description`, `argument-hint`, and `allowed-tools`, followed by Markdown prompt instructions. Keep descriptions precise because Claude Code uses them for skill triggering. Prefer short headings, direct instructions, and explicit output constraints.

## Testing Guidelines

There is no automated test harness. Test manually by installing the skill with a symlink and invoking `/<skill-name>` inside Claude Code against a realistic project. Check trigger accuracy, argument handling, output format, and whether allowed tools match the prompt’s needs. For new skills, document example invocations in `README.md`.

## Commit & Pull Request Guidelines

Recent commits use concise imperative messages, such as `Add CLAUDE.md with skill format and contribution guidance` and `Restyle codebase-improve output: themed prose over rigid template`. Follow that style: start with a verb and summarize the user-visible change. Pull requests should include a brief description, affected skill names, manual test notes, and any README or installation changes. Link related issues when available.

## Agent-Specific Instructions

When editing skills, keep changes scoped to the target skill and related documentation. Do not modify installed copies under `~/.claude/skills`; update this repository and let symlinks carry the change. Skill prompts are executable instructions, so avoid vague guidance that cannot be verified in output.
