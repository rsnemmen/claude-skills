# Contributing

## Project structure

This repository stores custom Claude Code skills. Each skill lives in its own directory under `skills/` and contains a `SKILL.md` file, for example `skills/codebase-improve/SKILL.md`. Repository-level documentation lives in `README.md` and `CLAUDE.md`; keep both aligned with any skill additions or behavior changes. There is no separate source, test, or asset tree at present.

## Adding a new skill

1. Create `skills/<skill-name>/SKILL.md` following the format below.
2. Update the skills table in `README.md`.
3. Symlink to install: `ln -s ~/cc-skills/skills/<skill-name> ~/.claude/skills/<skill-name>`.

## Skill file format

Every skill is a Markdown file with a YAML frontmatter block followed by the prompt body:

```
---
name: skill-name
description: <one-line description used by CC to decide when to trigger the skill>
argument-hint: <shown to the user as autocomplete hint>
allowed-tools: [Read, Glob, Grep, Bash, Agent, ...]
---

# Skill Title

<prompt body — written as instructions to the Claude instance that will execute the skill>
```

The `description` field is the most important: Claude Code uses it to decide whether to auto-trigger the skill. Write it to match the natural language a user would type.

## Style and naming

Use one directory per skill, and make the directory name match the `name` field in the `SKILL.md` frontmatter. Skill files must start with YAML frontmatter containing `name`, `description`, `argument-hint`, and `allowed-tools`, followed by Markdown prompt instructions. Keep descriptions precise because Claude Code uses them for skill triggering. Prefer short headings, direct instructions, and explicit output constraints.

## Testing

There is no automated test harness. Test manually by installing the skill with a symlink and invoking `/<skill-name>` inside Claude Code against a realistic project. Check trigger accuracy, argument handling, output format, and whether allowed tools match the prompt's needs. For new skills, document example invocations in `README.md`.

Use the `/skill-creator` meta-skill (built into CC) to run evals or benchmark a skill's trigger accuracy.

## Commit and PR conventions

Recent commits use concise imperative messages, such as `Add CLAUDE.md with skill format and contribution guidance` and `Restyle codebase-improve output: themed prose over rigid template`. Follow that style: start with a verb and summarize the user-visible change. Pull requests should include a brief description, affected skill names, manual test notes, and any README or installation changes. Link related issues when available.

When editing skills, keep changes scoped to the target skill and related documentation. Do not modify installed copies under `~/.claude/skills`; update this repository and let symlinks carry the change. Skill prompts are executable instructions, so avoid vague guidance that cannot be verified in output.
