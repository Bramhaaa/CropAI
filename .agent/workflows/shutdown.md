# Shutdown Workflow

## Purpose
Capture the outcome of the current work session and update persistent memory so the next session can resume accurately.

## When It Should Be Used
Use this when pausing work, finishing a task, or handing the repository back to the user.

## Steps the AI Should Execute
1. Review the current conversation for the work that was discussed and completed.
2. Inspect the modified files, new files, and deleted files to understand the actual repository changes.
3. Check `git diff` if Git is available, then compare it with the current repository state.
4. Determine which memory files are affected by the verified changes.
5. Update only the affected memory files, keeping unchanged memory untouched.
6. Append a concise session summary to the latest session log.
7. Provide a brief end-of-session summary to the user.

## Files to Read
- `AGENT.md`
- The current conversation context
- Modified files
- New files
- Deleted files
- `git diff` if available
- Current repository state
- `.agent/memory/current.md`
- `.agent/memory/index.md`
- `.agent/memory/decisions.md`
- `.agent/memory/sessions/YYYY-MM-DD.md` or the latest session file
- Any repository files needed to confirm the verified changes

## Files to Update
- `.agent/memory/current.md`
- `.agent/memory/decisions.md` if needed
- `.agent/memory/index.md` if the repository structure changed
- `.agent/memory/sessions/YYYY-MM-DD.md` or the latest session file

## Rules to Follow
- Do not rely only on conversation history when the repository state is available.
- Do not overwrite historical session notes.
- Keep memory updates concise and focused on durable facts.
- Do not add unrelated changes during shutdown.
- Verify the final state against the repository before summarizing it.
- Do not rewrite unchanged memory.

## Expected Output
- Updated working memory.
- A short shutdown summary.
- A clear next-step handoff for the next session.
