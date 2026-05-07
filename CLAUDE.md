# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A collection of custom Claude Code skills (slash commands) and Codex CLI skills for personal use. Claude Code skills live under `skills/`; Codex-compatible copies live under `codex-skills/`. Installed copies live outside the repo under `~/.claude/skills/` and `${CODEX_HOME:-$HOME/.codex}/skills/`.

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

YAML frontmatter is parsed strictly. Quote long or punctuation-heavy scalar values, especially `description` and `argument-hint` values containing `:`, `#`, `[ ]`, `{ }`, quotes, slash-command examples, or other syntax-like text. Validate new or edited skills with:

```sh
python3 -c 'import pathlib, yaml; [yaml.safe_load(p.read_text().split("---", 2)[1]) for p in pathlib.Path(".").glob("**/SKILL.md")]'
```

## Adding a new skill

1. Create `skills/<skill-name>/SKILL.md` following the format above.
2. Create the Codex copy at `codex-skills/<skill-name>/SKILL.md`.
3. Update the skills table in `README.md` and docs.
4. Symlink to install for Claude: `ln -s ~/cc-skills/skills/<skill-name> ~/.claude/skills/<skill-name>`.
5. Symlink to install for Codex: `ln -s ~/cc-skills/codex-skills/<skill-name> ${CODEX_HOME:-$HOME/.codex}/skills/<skill-name>`.

## Converting Claude skills to Codex

When a user creates or updates a Claude Code skill in `skills/<skill-name>/SKILL.md`, keep that file as the Claude source and convert a copy for Codex:

1. Copy the skill directory to `codex-skills/<skill-name>/`.
2. Keep `name` and `description` frontmatter.
3. Remove Claude-only frontmatter fields such as `argument-hint` and `allowed-tools`.
4. Add `metadata.short-description`.
5. Add or update `agents/openai.yaml` with quoted `interface.display_name`, `interface.short_description`, and `interface.default_prompt` values.
6. Replace `$ARGUMENTS` with instructions to interpret the user's request.
7. Replace slash-command wording such as `/<skill-name>` with natural-language Codex triggering.
8. Replace Claude tool names (`Read`, `Glob`, `Grep`, `Write`, `Edit`, `Agent`, `Explore`) with Codex-compatible process guidance such as `rg`, targeted shell inspection, `apply_patch`, and subagents only when active Codex instructions allow them.
9. Keep behavior, constraints, and output shape aligned across the Claude and Codex copies unless a platform difference requires divergence.

## Testing a skill

There is no automated test harness. Test Claude skills by invoking `/<skill-name>` inside a Claude Code session pointed at a real project. Test Codex skills by installing them into `${CODEX_HOME:-$HOME/.codex}/skills/`, restarting Codex, and issuing natural-language requests that should trigger the skill.

## Repo conventions

- One subdirectory per skill per platform; the directory name must match the `name` frontmatter field.
- Skill prompts are executable instructions to an AI agent. Write them precisely, with explicit constraints and output format requirements.
- Keep `README.md` in sync whenever a skill is added, renamed, or removed.
