---
name: codebase-improve
description: Propose codebase improvements (audit, refactoring, performance, security, etc.) cited with file:line evidence. Read-only.
argument-hint: '[scope] [focus] — e.g. "fortran/ performance"'
allowed-tools: [Read, Glob, Grep, Bash, Agent]
---

# Codebase Improvement Proposal

Analyze `$ARGUMENTS` (scope/focus) and surface high-impact, codebase-specific issues. **Do not modify files.**

## Execution
1. **Context:** Read `CLAUDE.md`/`README.md` first to understand the domain.
2. **Investigate:** Launch up to 3 `Explore` agents using concrete, domain-specific questions. Use `Read` on key files to get full surrounding context.
3. **Filter:** Discard generic advice (e.g., "add tests", "improve error handling"). Only report issues specific to *this* codebase that would surprise a careful developer.

## Output Format
- **Intro:** One short paragraph stating what was reviewed and the main takeaway. No boilerplate headers.
- **Themed Sections (`###`):** Group 5–8 findings into 2–4 highly specific themes (e.g., "RK4 Edge Cases", not "Maintainability"). Order by impact.
- **Findings:** Write 1–3 sentences of prose per finding. You **must** weave together the issue, a **file:line citation**, a **short code quote/paraphrase**, and a concrete fix. If you can't cite it, don't claim it.
- **No Fluff:** No "Out of scope", "Open questions", or templated lists. Integrate domain questions or omissions inline. If no meaningful issues exist, say so plainly.