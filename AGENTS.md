# Repository Guidelines

## Project Structure & Module Organization

This repository stores custom Claude Code and Codex CLI skills. Claude Code skills live in `skills/<skill-name>/SKILL.md`; Codex-compatible copies live in `codex-skills/<skill-name>/SKILL.md`. Repository-level documentation lives in `README.md`, `CLAUDE.md`, and `AGENTS.md`; keep them aligned with any skill additions or behavior changes.

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
ln -s ~/cc-skills/codex-skills/<skill-name> ${CODEX_HOME:-$HOME/.codex}/skills/<skill-name>
```

Installs a skill for local Codex CLI use by symlinking the Codex-compatible skill directory.

```sh
python3 install-skills.py --target codex
```

Installs selected Codex-compatible skills with the interactive installer.

```sh
git diff -- README.md CLAUDE.md AGENTS.md skills/<skill-name>/SKILL.md codex-skills/<skill-name>/SKILL.md
```

Reviews documentation and prompt changes before committing.

## Coding Style & Naming Conventions

Use one directory per skill per platform, and make the directory name match the `name` field in the `SKILL.md` frontmatter. Claude Code skill files must start with YAML frontmatter containing `name`, `description`, `argument-hint`, and `allowed-tools`. Codex skill files must include `name` and `description`, should include `metadata.short-description`, and should not include Claude-only fields. Keep descriptions precise because both agents use them for skill triggering. Prefer short headings, direct instructions, and explicit output constraints.

YAML frontmatter is parsed strictly. Quote long or punctuation-heavy scalar values, especially `description` and `argument-hint` values containing `:`, `#`, `[ ]`, `{ }`, quotes, slash-command examples, or other syntax-like text. Validate new or edited skills with:

```sh
python3 -c 'import pathlib, yaml; [yaml.safe_load(p.read_text().split("---", 2)[1]) for p in pathlib.Path(".").glob("**/SKILL.md")]'
```

## Converting Claude Skills to Codex

When a user creates or updates a Claude Code skill in `skills/<skill-name>/SKILL.md`, keep that file as the Claude source and convert a copy for Codex:

1. Copy the skill directory to `codex-skills/<skill-name>/`.
2. Keep `name` and `description` frontmatter.
3. Remove Claude-only frontmatter fields such as `argument-hint` and `allowed-tools`.
4. Add `metadata.short-description`.
5. Add or update `agents/openai.yaml` with `display_name`, `short_description`, and `default_prompt`.
6. Replace `$ARGUMENTS` with instructions to interpret the user's request.
7. Replace slash-command wording such as `/<skill-name>` with natural-language Codex triggering.
8. Replace Claude tool names (`Read`, `Glob`, `Grep`, `Write`, `Edit`, `Agent`, `Explore`) with Codex-compatible process guidance such as `rg`, targeted shell inspection, `apply_patch`, and subagents only when active Codex instructions allow them.
9. Keep behavior, constraints, and output shape aligned across the Claude and Codex copies unless a platform difference requires divergence.

## Testing Guidelines

There is no automated test harness. Test manually by installing the skill with a symlink and invoking `/<skill-name>` inside Claude Code or a natural-language trigger inside Codex CLI against a realistic project. Check trigger accuracy, argument handling, output format, and whether platform-specific tool guidance matches the prompt's needs. For new skills, document example invocations in `README.md`.

## Commit & Pull Request Guidelines

Recent commits use concise imperative messages, such as `Add CLAUDE.md with skill format and contribution guidance` and `Restyle codebase-improve output: themed prose over rigid template`. Follow that style: start with a verb and summarize the user-visible change. Pull requests should include a brief description, affected skill names, manual test notes, and any README or installation changes. Link related issues when available.

## Agent-Specific Instructions

When editing skills, keep changes scoped to the target skill and related documentation. Do not modify installed copies under `~/.claude/skills` or `${CODEX_HOME:-$HOME/.codex}/skills`; update this repository and let symlinks carry the change. Skill prompts are executable instructions, so avoid vague guidance that cannot be verified in output.
