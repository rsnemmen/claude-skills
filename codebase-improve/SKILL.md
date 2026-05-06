---
name: codebase-improve
description: Research and propose improvements to the current codebase, cited with file:line evidence. Use when the user asks for an audit, refactoring proposal, performance/security/maintainability/test-coverage/dead-code/type-safety/error-handling/DX review, or general "what could we improve here" questions. Produces recommendations only — does not modify code.
argument-hint: [scope] [focus] — e.g. "fortran/ performance" or "whole codebase maintainability"
allowed-tools: [Read, Glob, Grep, Bash, Agent]
---

# Codebase Improvement Proposal

Research the codebase and propose improvements with evidence for every claim. Do not modify any files.

## Arguments

The user invoked this skill with: $ARGUMENTS

Parse `$ARGUMENTS` as free text describing **scope** (a directory, module, or "the whole codebase") and **focus** (one or more of: performance, security, maintainability, test coverage, dead code, type safety, error handling, DX, or anything else the user names).

If `$ARGUMENTS` is empty or ambiguous, ask the user one clarifying question — what scope and what focus — before proceeding.

## Method

1. **Explore in parallel.** Launch up to 3 `Explore` agents in a single message, each with a distinct angle drawn from the requested focus. Example for a performance focus: one agent for hot loops, one for I/O and allocation patterns, one for algorithmic choices. Pass each agent the scope and a specific question.

2. **Read critical files yourself.** Once agents return findings, open the files they cite to confirm — Explore agents read excerpts and may miss surrounding context.

3. **Synthesize.** Group findings into themes. For each finding, write:
   - **What** — the issue in one sentence
   - **Where** — `path/to/file.ext:line` (always cite — no vibes)
   - **Why it matters** — concrete impact
   - **Suggested change** — minimal and targeted, not a rewrite

4. **Separate questions from recommendations.** If intent is unclear anywhere (a function with no obvious caller, an undocumented flag, a hand-rolled algorithm that may be load-bearing), list it under **Open questions** instead of recommending a change.

## Constraints

- **No large architectural rewrites** unless clearly justified by a small fix being impossible.
- **Cite evidence for every claim.** File path + line number. If you can't cite it, don't claim it.
- **Read-only.** Do not edit, write, or run mutating commands.
- **Don't pad.** If you found three real issues, return three. Don't manufacture findings to fill space.

## Output format

```
## Scope and focus
<one paragraph restating what was reviewed and against which lens>

## Findings
### <theme 1>
- **What:** ...
- **Where:** path/file.ext:42-58
- **Why it matters:** ...
- **Suggested change:** ...

### <theme 2>
...

## Open questions
- <question 1>
- <question 2>

## Out of scope (noted but not pursued)
- <thing noticed but not investigated, with brief reason>
```

If no meaningful issues exist, say so plainly — a short honest report beats a long padded one.
