# codebase-improve

!!! info "Skill metadata"
    - **Name:** `codebase-improve`
    - **Claude path:** `skills/codebase-improve/SKILL.md`
    - **Codex path:** `codex-skills/codebase-improve/SKILL.md`
    - **Argument hint:** `[scope] [focus]` — e.g. "fortran/ performance" or "whole codebase maintainability"
    - **Allowed tools:** `Read`, `Glob`, `Grep`, `Bash`, `Agent`

## What it does

Research and propose improvements to the current codebase, cited with file:line evidence. Use when the user asks for an audit, refactoring proposal, performance/security/maintainability/test-coverage/dead-code/type-safety/error-handling/DX review, or general "what could we improve here" questions. Produces recommendations only — does not modify code.

## Usage

Claude Code:

```
/codebase-improve
```
No arguments — broad sweep across the whole codebase.

```
/codebase-improve fortran/ performance
```
Scoped to the `fortran/` directory, performance focus.

```
/codebase-improve perl/ maintainability
```
Scoped to the `perl/` wrappers, maintainability focus.

Codex CLI:

```text
Review this repository for high-impact improvements.
```

```text
Audit the fortran/ directory for performance problems.
```

## Arguments

Parse arguments as free text describing **scope** (a directory, module, or "the whole codebase") and **focus** (one or more of: performance, security, maintainability, test coverage, dead code, type safety, error handling, DX, or anything else the user names).

If arguments are empty, the skill does a broad sweep of the whole codebase before asking for clarification.

## Method

### 1. Understand the codebase first

Read `AGENTS.md`, `CLAUDE.md`, `README.md`, or equivalent project documentation to understand what the code does, its domain, and its architecture. This context is essential — without it you'll produce generic advice that applies to any project rather than this one.

### 2. Explore with specific questions

Launch up to 3 `Explore` agents in a single message, each targeting a concrete question about *this* codebase drawn from what you just learned. Don't ask generic questions like "are there any bugs?" — ask things specific to the actual code (e.g., "does the Runge-Kutta integrator handle NaN propagation?" or "is the eigenvalue search loop bounded?").

### 3. Read the files that matter

Open the most important files yourself with the Read tool. Explore agents read excerpts and miss context. For any finding you're considering, read the full surrounding function or block — you need to see the actual code to say anything specific.

### 4. Find real issues, not checklist items

A finding is real if it's specific to *this* codebase and would surprise a careful developer who hadn't looked closely. A finding is not real if it could appear verbatim in a review of any random codebase ("consider adding more tests", "improve error handling").

For each candidate finding, ask: "Could I paste this into a review of a completely different project?" If yes, either discard it or make it concrete enough that the answer becomes no.

Every finding must include a short quote or paraphrase of the actual code being criticized. A line reference alone is not enough.

### 5. Group findings by theme, lead with what matters most

Cluster related findings into 2–4 themes that emerged from *this* codebase (e.g., "Numerical edge cases in the integrator", "Error propagation across the I/O boundary", "Hot-path allocations"). Theme names must be specific to what you found — never generic buckets like "Maintainability" or "Code quality".

Lead with the highest-impact theme. Within each theme, lead with the highest-impact finding. Convey priority through ordering and language ("the most consequential issue here is…", "minor but worth flagging…") — do not attach severity labels.

Soft cap: 5–8 findings total across all themes. If you found fewer real issues, report fewer — don't pad. If you genuinely found more, use judgment.

## Constraints

- **Cite evidence inline.** When you describe an issue, weave the file:line reference and a short quote or paraphrase of the actual code into the same sentence — not in a separate field. If you can't cite it, don't claim it.
- **No generic advice.** "Add more tests" without naming the specific untested function is not a finding.
- **Read-only.** Do not edit, write, or run mutating commands.

## Output style

Write the review as **themed sections**, not a templated list.

Open with **one short paragraph** that conveys what you read and the single most important takeaway. Skip a formal "Scope and focus" header — let the opening paragraph do that work.

For each theme:

- Use a short, specific `###` heading drawn from what you actually found ("Numerical edge cases in the RK4 step", not "Correctness").
- Write each finding as 1–3 sentences of prose that weave together: what's wrong (with file:line and a quote or paraphrase of the actual code), why it matters in this specific codebase, and a concrete suggestion if one is obvious. Do not use a rigid sub-template — a finding can be one paragraph or a couple of sentences.

If a finding genuinely needs domain knowledge to judge, phrase it as a question inline within its theme — no separate "Open questions" section.

If you noticed an area but deliberately didn't pursue it, mention it in one sentence at the end of the relevant theme or in a single closing line — no formal "Out of scope" section.

Optionally close with a one-line priority order or a brief "What's solid" note — only if it adds real value.

If no meaningful issues exist, say so plainly.
