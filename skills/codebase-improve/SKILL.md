---
name: codebase-improve
description: Propose codebase improvements (audit, refactoring, performance, security, etc.) cited with file:line evidence. 
argument-hint: '[scope] [focus] — e.g. "fortran/ performance"'
---

# Codebase Improvement Proposal

Analyze `$ARGUMENTS` (scope/focus) and surface high-impact, codebase-specific issues.

## Execution
1. **Context:** Read `CLAUDE.md`/`README.md` first to understand the domain.
2. **Investigate:** Launch up to 3 `Explore` agents using concrete, domain-specific questions. Use `Read` on key files to get full surrounding context.
3. **Filter:** Discard generic advice (e.g., "add tests", "improve error handling"). Only report issues specific to *this* codebase that would surprise a careful developer.

## Output Format
- **Themed Sections (`###`):** Group up to 8 findings into specific themes. Order by impact.
