# Checkpoint Workflow

## Purpose
Save the current working state during an active session so progress is preserved without closing the session.

## When It Should Be Used
Use this after a meaningful unit of work, before switching tasks, or before any interruption where you want to preserve context.

## Steps the AI Should Execute
1. Record what was completed since the last checkpoint.
2. Update `current.md` with the current feature state, completed work, blockers, and immediate next action.
3. Append a short checkpoint note to the current session log.
4. Leave architecture and broader memory unchanged unless a verified structural change occurred.
5. Resume work or hand control back to the user after the checkpoint is saved.

## Files to Read
- `AGENT.md`
- `.agent/memory/current.md`
- `.agent/memory/sessions/YYYY-MM-DD.md` or the latest session file
- Relevant files touched in the current task

## Files to Update
- `.agent/memory/current.md`
- `.agent/memory/sessions/YYYY-MM-DD.md` or the latest session file

## Rules to Follow
- Keep checkpoint updates short.
- Do not rewrite untouched memory files.
- Do not use checkpoints to restate the whole repository state.
- Preserve session history instead of replacing it.

## Expected Output
- An updated current-state snapshot.
- A short checkpoint note in the session log.
