# Contributing

## Project structure

This repository stores custom Claude Code and Codex CLI skills. Claude Code skills live under `skills/`; Codex-compatible copies live under `codex-skills/`. Repository-level documentation lives in `README.md`, `CLAUDE.md`, and `AGENTS.md`; keep all three aligned with any skill additions or behavior changes.

## Adding a new skill

1. Create `skills/<skill-name>/SKILL.md` following the format below.
2. Create the Codex copy at `codex-skills/<skill-name>/SKILL.md`.
3. Update the skills table in `README.md` and docs.
4. Symlink to install for Claude: `ln -s ~/cc-skills/skills/<skill-name> ~/.claude/skills/<skill-name>`.
5. Symlink to install for Codex: `ln -s ~/cc-skills/codex-skills/<skill-name> ${CODEX_HOME:-$HOME/.codex}/skills/<skill-name>`.

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

Use one directory per skill per platform, and make the directory name match the `name` field in the `SKILL.md` frontmatter. Claude Code skill files must start with YAML frontmatter containing `name`, `description`, `argument-hint`, and `allowed-tools`, followed by Markdown prompt instructions. Codex skill files must include `name` and `description`, should include `metadata.short-description`, and should not include Claude-only fields. Keep descriptions precise because both agents use them for skill triggering. Prefer short headings, direct instructions, and explicit output constraints.

## Converting Claude skills to Codex

When a user creates or updates a Claude Code skill, keep `skills/<skill-name>/SKILL.md` as the Claude source and convert a copy for Codex:

1. Copy the skill directory to `codex-skills/<skill-name>/`.
2. Keep `name` and `description` frontmatter.
3. Remove Claude-only frontmatter fields such as `argument-hint` and `allowed-tools`.
4. Add `metadata.short-description`.
5. Add or update `agents/openai.yaml` with quoted `interface.display_name`, `interface.short_description`, and `interface.default_prompt` values.
6. Replace `$ARGUMENTS` with instructions to interpret the user's request.
7. Replace slash-command wording such as `/<skill-name>` with natural-language Codex triggering.
8. Replace Claude tool names (`Read`, `Glob`, `Grep`, `Write`, `Edit`, `Agent`, `Explore`) with Codex-compatible process guidance such as `rg`, targeted shell inspection, `apply_patch`, and subagents only when active Codex instructions allow them.
9. Keep behavior, constraints, and output shape aligned across the Claude and Codex copies unless a platform difference requires divergence.

## Testing

There is no automated test harness. Test manually by installing the skill with a symlink and invoking `/<skill-name>` inside Claude Code or a natural-language trigger inside Codex CLI against a realistic project. Check trigger accuracy, argument handling, output format, and whether platform-specific tool guidance matches the prompt's needs. For new skills, document example invocations in `README.md`.

Use the `/skill-creator` meta-skill (built into CC) to run evals or benchmark a skill's trigger accuracy.

## Commit and PR conventions

Recent commits use concise imperative messages, such as `Add CLAUDE.md with skill format and contribution guidance` and `Restyle codebase-improve output: themed prose over rigid template`. Follow that style: start with a verb and summarize the user-visible change. Pull requests should include a brief description, affected skill names, manual test notes, and any README or installation changes. Link related issues when available.

When editing skills, keep changes scoped to the target skill and related documentation. Do not modify installed copies under `~/.claude/skills` or `${CODEX_HOME:-$HOME/.codex}/skills`; update this repository and let symlinks carry the change. Skill prompts are executable instructions, so avoid vague guidance that cannot be verified in output.
