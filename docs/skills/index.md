# Skills

Type `/<skill-name>` in a Claude Code session to invoke the Claude version. In Codex CLI, install the Codex copy and issue a natural-language request matching the skill description.

| Skill | Claude trigger | Codex trigger | Description |
|-------|----------------|---------------|-------------|
| [`codebase-improve`](codebase-improve.md) | `/codebase-improve [scope] [focus]` | Ask for a codebase audit, refactoring proposal, or focused improvement review | Audits a codebase and proposes concrete improvements with file:line citations. Read-only; never modifies code. |
| [`bootstrap-docs`](bootstrap-docs.md) | `/bootstrap-docs [--scaffold] [stack] [focus]` | Ask to set up docs, choose a docs stack, or scaffold a docs site | Researches and recommends a documentation-site stack, then scaffolds it with real starter content from README and source on confirmation. |
