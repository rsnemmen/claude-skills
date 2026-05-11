# codebase-improve

!!! info "Skill metadata"
    - **Name:** `codebase-improve`
    - **Claude path:** `skills/codebase-improve/SKILL.md`
    - **Codex path:** `codex-skills/codebase-improve/SKILL.md`
    - **Argument hint:** `[scope] [focus]` — e.g. "fortran/ performance"

## What it does

Analyze a scope/focus and surface high-impact, codebase-specific improvements cited with file:line evidence. Read-only; never modifies code.

## Usage

Claude Code:

```
/codebase-improve
```

```
/codebase-improve fortran/ performance
```

Codex CLI:

```text
Review this repository for high-impact improvements.
```

```text
Audit the fortran/ directory for performance problems.
```

## Method

1. Read `CLAUDE.md`/`README.md` to understand the domain.
2. Launch up to 3 `Explore` agents using concrete, domain-specific questions. Use `Read` on key files for full context.
3. Discard generic advice ("add tests", "improve error handling"). Report only issues specific to *this* codebase that would surprise a careful developer.

Output is grouped into themed `###` sections (up to 8 findings), ordered by impact.
