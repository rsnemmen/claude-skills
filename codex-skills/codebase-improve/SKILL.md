---
name: codebase-improve
description: Research and propose improvements to the current codebase, cited with file:line evidence. Use when the user asks for an audit, refactoring proposal, performance/security/maintainability/test-coverage/dead-code/type-safety/error-handling/DX review, or general "what could we improve here" questions. Produces recommendations only; does not modify code.
metadata:
  short-description: Audit a codebase and propose concrete improvements
---

# Codebase Improvement Proposal

Research the codebase and surface the issues that actually matter, grouped by theme. Do not modify any files.

## Request handling

Interpret the user's request as free text describing scope (a directory, module, or "the whole codebase") and focus (one or more of: performance, security, maintainability, test coverage, dead code, type safety, error handling, DX, or anything else the user names).

If the request does not name a scope or focus, do a broad sweep of the whole codebase before asking for clarification.

## Method

### 1. Understand the codebase first

Read `AGENTS.md`, `README.md`, `CLAUDE.md`, or equivalent project documentation to understand what the code does, its domain, and its architecture. This context is essential; without it, recommendations will be generic.

### 2. Explore with specific questions

Use fast repo inspection tools such as `rg`, `rg --files`, and targeted file reads. If the active Codex instructions allow subagents and the task benefits from parallel exploration, launch up to 3 explorer agents in one batch, each targeting a concrete question about this codebase drawn from what you just learned. Do not ask generic questions like "are there any bugs?" Ask things specific to the actual code.

### 3. Read the files that matter

Open the most important files yourself. For any finding you are considering, read the full surrounding function or block so you can judge context accurately.

### 4. Find real issues, not checklist items

A finding is real if it is specific to this codebase and would surprise a careful developer who had not looked closely. A finding is not real if it could appear verbatim in a review of any random codebase.

For each candidate finding, ask: "Could I paste this into a review of a completely different project?" If yes, either discard it or make it concrete enough that the answer becomes no.

Every finding must include a short quote or paraphrase of the actual code being criticized. A line reference alone is not enough.

### 5. Group findings by theme, lead with what matters most

Cluster related findings into 2-4 themes that emerged from this codebase, such as "Numerical edge cases in the integrator" or "Error propagation across the I/O boundary". Theme names must be specific to what you found; never use generic buckets like "Maintainability" or "Code quality".

Lead with the highest-impact theme. Within each theme, lead with the highest-impact finding. Convey priority through ordering and language; do not attach severity labels.

Soft cap: 5-8 findings total across all themes. If you found fewer real issues, report fewer. If you genuinely found more, use judgment.

## Constraints

- Cite evidence inline. When you describe an issue, weave the file:line reference and a short quote or paraphrase of the actual code into the same sentence. If you cannot cite it, do not claim it.
- No generic advice. "Add more tests" without naming the specific untested function is not a finding.
- Read-only. Do not edit files, write files, or run mutating commands.

## Output style

Write the review as themed sections, not a templated list.

Open with one short paragraph that conveys what you read and the single most important takeaway. Skip a formal "Scope and focus" header; let the opening paragraph do that work.

For each theme:

- Use a short, specific `###` heading drawn from what you actually found.
- Write each finding as 1-3 sentences of prose that weave together: what is wrong, file:line evidence and a quote or paraphrase, why it matters in this specific codebase, and a concrete suggestion if one is obvious.

If a finding genuinely needs domain knowledge to judge, phrase it as a question inline within its theme.

If you noticed an area but deliberately did not pursue it, mention it in one sentence at the end of the relevant theme or in a single closing line.

Optionally close with a one-line priority order or a brief "what is solid" note only if it adds value.

If no meaningful issues exist, say so plainly.
