# AGENT.md

This document defines the permanent operating rules for the AI agent working on this repository.

Its purpose is to:

- Maintain consistency across sessions.
- Reduce unnecessary repository scanning.
- Preserve project context.
- Make minimal, high-quality code changes.
- Keep project memory accurate and concise.

Repository source code is always the ultimate source of truth.

---

# 1. Think Before Coding

Don't assume.

Don't hide uncertainty.

Surface tradeoffs.

Before implementing:

- State assumptions explicitly.
- If multiple interpretations exist, present them instead of silently choosing one.
- If a simpler solution exists, explain it.
- If requirements are unclear, stop and ask.
- Explain important design decisions before implementing them.

---

# 2. Simplicity First

Always prefer the simplest solution that satisfies the requirements.

Avoid:

- speculative features
- unnecessary abstractions
- premature optimization
- excessive configurability
- code written "for the future"

Ask yourself:

> Would an experienced engineer consider this over-engineered?

If yes, simplify.

---

# 3. Surgical Changes

Modify only what is necessary.

When editing existing code:

- Match existing style.
- Preserve formatting where practical.
- Do not refactor unrelated code.
- Do not rename unrelated variables.
- Do not reorganize folders unless requested.
- Mention unrelated issues instead of fixing them.

If your changes leave unused code behind:

- Remove imports introduced by your changes.
- Remove variables introduced by your changes.
- Remove functions introduced by your changes.

Never remove unrelated code unless requested.

Every modified line should directly support the requested task.

---

# 4. Goal Driven Execution

Before implementing:

Define success criteria.

Examples:

Fix bug

↓

Write a failing test

↓

Fix bug

↓

Verify test passes

For larger tasks provide a short execution plan.

Example

1. Update API
2. Update service layer
3. Update tests
4. Verify

Always verify your work before declaring completion.

---

# 5. Repository Source of Truth

Repository code has highest priority.

Memory exists only to reduce search time.

If repository and memory disagree:

Trust the repository.

Update memory when appropriate.

Never force repository code to match outdated memory.

---

# 6. Persistent Project Memory

This repository contains persistent project memory.

Location:

.agent/memory/

Memory is intended to help future sessions quickly understand the project.

Memory contains summaries.

Memory never replaces source code.

Memory should remain concise.

Never store large code snippets.

Never duplicate repository contents.

---

# 7. Memory Loading Order

At the beginning of every new session:

Load memory in this order.

1. overview.md
2. architecture.md
3. index.md
4. current.md
5. decisions.md
6. The most recent date-stamped file inside sessions/ (Format: YYYY-MM-DD.md)

After reading memory:

Summarize current project state.

Identify current feature.

Identify next recommended task.

Wait for user instructions.

---

# 8. Memory Responsibilities

overview.md

Project description.

Main goals.

Major technologies.

Rarely changes.

---

architecture.md

High-level architecture.

Major modules.

Data flow.

Update only after architecture changes.

---

index.md

Semantic map of repository.

Contains:

- Features
- Responsibilities
- Important folders
- Important files

Never make this a directory tree.

Future searches should begin here.

---

current.md

Current working memory.

Contains:

- current feature
- completed work
- next task
- blockers
- current branch (if known)

Updated during shutdown.

---

decisions.md

Architectural decisions.

Append new decisions.

Never rewrite history.

---

sessions/

Chronological work log.

One markdown file per work session or day.

Contains summaries only.

---

# 9. Repository Search Strategy

Always minimize repository scanning.

Search priority:

1. Read index.md
2. Identify relevant feature
3. Read relevant folders
4. Expand search only if necessary
5. Scan the entire repository only as a last resort

Never perform unnecessary repository-wide searches.

---

# 10. Memory Update Rules

Do not continuously rewrite memory.

Only update memory when:

- initializing project memory
- executing shutdown workflow
- executing refresh workflow
- explicitly instructed

Update only the files affected.

Avoid rewriting unchanged files.

Avoid duplicate information.

- Keep current.md and index.md highly focused. 
- If index.md exceeds ~150 lines, group minor features into broader modules rather than listing every atomic file.
- Treat memory as a high-level map, not a database of your code lines.


---

# 11. Initialization Rules

If project memory does not exist:

Analyze the repository.

Create:

- overview.md
- architecture.md
- index.md
- current.md
- decisions.md

Create today's session log.

Wait for user review before continuing.

Never generate placeholder information.

Base everything on repository analysis.

---

# 12. Workflow Definitions

Initialize

Repository analysis.

Create project memory.

---

Start

Load project memory.

Summarize current state.

Wait for user instructions.

---

Checkpoint

Update current working state.

Append session summary.

Do not rewrite architecture.

---

Shutdown

Update:

- current.md
- decisions.md (if needed)
- latest session
- index.md (only if project structure changed)

Provide end-of-session summary.

---

Refresh

Re-analyze repository.

Update architecture.

Rebuild semantic index.

Preserve session history.

---

# 13. Architecture Rules

Prefer existing architecture.

Reuse existing modules.

Avoid introducing new frameworks.

Avoid unnecessary dependencies.

Avoid changing project structure without justification.

Prefer consistency over novelty.

---

# 14. Working Rules

Treat the current conversation as temporary working memory.

Treat .agent/memory as long-term project memory.

Treat repository code as the ultimate source of truth.

Always verify assumptions against the repository.

---

# 15. Confidence Rules

State confidence whenever making architectural assumptions.

Confidence levels:

High

Medium

Low

If confidence is Low:

Search before answering.

Never invent repository structure.

Never assume files exist.

---

# 16. Communication Style

Be direct.

Be concise.

Explain important reasoning.

Mention assumptions.

Point out risks.

Suggest simpler alternatives when appropriate.

Do not overwhelm with unnecessary detail.

---

# 17. Completion Checklist

Before declaring a task complete:

✓ Requirements satisfied

✓ No unnecessary code added

✓ Changes limited to requested scope

✓ Existing architecture respected

✓ Memory updated (only if appropriate)

✓ Verification completed

Only then declare the task finished.