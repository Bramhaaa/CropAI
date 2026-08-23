# Refresh Workflow

## Purpose
Rebuild the agent’s understanding of the repository when the project has changed enough that the existing memory may be stale.

## When It Should Be Used
Use this after significant repository changes, new architecture decisions, major refactors, or when memory no longer matches the codebase.

## Steps the AI Should Execute
1. Re-read the repository with emphasis on changed areas and high-level structure.
2. Compare the repository against the current memory for stale or missing information.
3. Update the memory files that are affected by the verified changes.
4. Preserve session history and append a concise refresh note if appropriate.
5. Leave unrelated memory untouched.

## Files to Read
- `AGENT.md`
- `.agent/memory/overview.md`
- `.agent/memory/architecture.md`
- `.agent/memory/index.md`
- `.agent/memory/current.md`
- `.agent/memory/decisions.md`
- Relevant repository files that changed or now matter

## Files to Update
- `.agent/memory/overview.md` if the project description or goals changed
- `.agent/memory/architecture.md` if the architecture changed
- `.agent/memory/index.md` if the semantic map changed
- `.agent/memory/current.md` if the current state changed
- `.agent/memory/decisions.md` if new durable decisions were made
- `.agent/memory/sessions/YYYY-MM-DD.md` if a refresh note should be logged

## Rules to Follow
- Update only what is verified to be stale.
- Keep the refresh focused on durable facts, not speculative notes.
- Preserve prior session history.
- Prefer the smallest memory edit that restores accuracy.

## Expected Output
- Refreshed memory aligned with the repository.
- A brief explanation of what changed and why.
