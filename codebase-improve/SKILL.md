---
name: codebase-improve
description: Research and propose improvements to the current codebase, cited with file:line evidence. Use when the user asks for an audit, refactoring proposal, performance/security/maintainability/test-coverage/dead-code/type-safety/error-handling/DX review, or general "what could we improve here" questions. Produces recommendations only — does not modify code.
argument-hint: [scope] [focus] — e.g. "fortran/ performance" or "whole codebase maintainability"
allowed-tools: [Read, Glob, Grep, Bash, Agent]
---

# Codebase Improvement Proposal

Research the codebase and propose the **top 5 improvements, ranked by severity**. Do not modify any files.

## Arguments

The user invoked this skill with: $ARGUMENTS

Parse `$ARGUMENTS` as free text describing **scope** (a directory, module, or "the whole codebase") and **focus** (one or more of: performance, security, maintainability, test coverage, dead code, type safety, error handling, DX, or anything else the user names).

If `$ARGUMENTS` is empty, do a broad sweep of the whole codebase before asking for clarification.

## Method

### 1. Understand the codebase first

Read `CLAUDE.md`, `README.md`, or equivalent project documentation to understand what the code does, its domain, and its architecture. This context is essential — without it you'll produce generic advice that applies to any project rather than this one.

### 2. Explore with specific questions

Launch up to 3 `Explore` agents in a single message, each targeting a concrete question about *this* codebase drawn from what you just learned. Don't ask generic questions like "are there any bugs?" — ask things specific to the actual code (e.g., "does the Runge-Kutta integrator handle NaN propagation?" or "is the eigenvalue search loop bounded?").

### 3. Read the files that matter

Open the most important files yourself with the Read tool. Explore agents read excerpts and miss context. For any finding you're considering, read the full surrounding function or block — you need to see the actual code to say anything specific.

### 4. Find real issues, not checklist items

A finding is real if it's specific to *this* codebase and would surprise a careful developer who hadn't looked closely. A finding is not real if it could appear verbatim in a review of any random codebase ("consider adding more tests", "improve error handling").

For each candidate finding, ask: "Could I paste this into a review of a completely different project?" If yes, either discard it or make it concrete enough that the answer becomes no.

Every finding must include a short quote or paraphrase of the actual code being criticized. A line reference alone is not enough.

### 5. Rank and cut to the top 5

Assign every finding a severity:

| Severity | Meaning |
|----------|---------|
| **Critical** | Correctness bug, data loss, or silently wrong results |
| **High** | Likely to cause failures or significant wasted effort |
| **Medium** | Real problem but workaround exists or impact is bounded |
| **Low** | Polish or clarity — worth fixing but not urgent |

Keep only the top 5 by severity. If you found fewer than 5 real issues, report fewer — don't pad.

## Constraints

- **Cite evidence for every claim.** File path + line number + a short quote or paraphrase of the actual code. If you can't cite it, don't claim it.
- **No generic advice.** "Add more tests" without naming the specific untested function is not a finding.
- **Read-only.** Do not edit, write, or run mutating commands.
- **Top 5 max.** Quality over quantity.

## Output format

```
## Scope and focus
<one paragraph: what was reviewed and through which lens>

## Findings (ranked by severity)

### 1. [Severity] — <short title>
- **What:** <one sentence describing the issue, quoting or paraphrasing the actual code>
- **Where:** path/file.ext:42–58
- **Why it matters:** <concrete impact on correctness, performance, or maintainability>
- **Suggested change:** <description of the fix>

### 2. ...

## Open questions
- <thing that looks suspicious but needs domain knowledge to judge — phrase as a question>

## Out of scope (noted but not pursued)
- <area noticed but deliberately not investigated, with brief reason>
```

If no meaningful issues exist, say so plainly.
