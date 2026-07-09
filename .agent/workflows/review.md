# Review Workflow

## Purpose
Evaluate the repository or recent work for correctness, completeness, consistency, and alignment with the agent’s memory.

## When It Should Be Used
Use this when the user asks for a review, when you need to verify a completed task, or when you want a structured check before handoff.

## Steps the AI Should Execute
1. Read the relevant memory files and the files related to the work under review.
2. Compare the implementation or repository state against the stated goal.
3. Identify gaps, regressions, inconsistencies, or missing validation.
4. Report findings in priority order, with the most important issues first.
5. Update memory only if the review confirms durable project-state changes that should be remembered.

## Files to Read
- `AGENT.md`
- `.agent/memory/overview.md`
- `.agent/memory/architecture.md`
- `.agent/memory/index.md`
- `.agent/memory/current.md`
- `.agent/memory/decisions.md`
- The files directly involved in the review

## Files to Update
- `.agent/memory/current.md` if the review changes the understood current state
- `.agent/memory/decisions.md` if the review confirms a durable new decision
- `.agent/memory/sessions/YYYY-MM-DD.md` if the review outcome should be logged

## Rules to Follow
- Focus on evidence, not assumptions.
- Distinguish between confirmed issues and residual risks.
- Keep the review concise and actionable.
- Do not modify unrelated files during review unless explicitly asked to fix something.

## Expected Output
- A prioritized review summary.
- Clear findings, or an explicit statement that no issues were found.
- Any recommended follow-up checks or fixes.
