# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A collection of custom Claude Code skills (slash commands) for personal use. Each skill lives in its own subdirectory as a `SKILL.md` file and is installed by symlinking that directory into `~/.claude/skills/`.

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

## Adding a new skill

1. Create `<skill-name>/SKILL.md` following the format above.
2. Update the skills table in `README.md`.
3. Symlink to install: `ln -s ~/cc-skills/<skill-name> ~/.claude/skills/<skill-name>`.

## Testing a skill

There is no automated test harness. Test by invoking `/<skill-name>` inside a Claude Code session pointed at a real project and evaluating output quality manually. Use the `/skill-creator` meta-skill (built into CC) to run evals or benchmark a skill's trigger accuracy.

## Repo conventions

- One subdirectory per skill; the directory name must match the `name` frontmatter field.
- Skill prompts are instructions to a Claude executor — write them precisely, with explicit constraints and output format requirements.
- Keep `README.md` in sync whenever a skill is added, renamed, or removed.
