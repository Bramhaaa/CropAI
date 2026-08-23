# Start Workflow

## Purpose
Load the project memory and restore the agent’s working context so new work can begin with minimal re-discovery.

## When It Should Be Used
Use this when starting a new session on an existing repository after initialization or after a prior shutdown.

## Steps the AI Should Execute
1. Read the persistent memory files in the required order.
2. Summarize the current project state, current feature, and next recommended task.
3. Identify any blockers, active decisions, or recent changes that matter to the next step.
4. Read only the minimum additional repository files needed to answer the user’s immediate request.
5. Wait for the user’s instruction unless the request already includes a concrete task.

## Files to Read
- `AGENT.md`
- `.agent/memory/overview.md`
- `.agent/memory/architecture.md`
- `.agent/memory/index.md`
- `.agent/memory/current.md`
- `.agent/memory/decisions.md`
- `.agent/memory/sessions/YYYY-MM-DD.md` if needed

## Files to Update
- None by default

## Rules to Follow
- Treat memory as a summary, not a source of truth.
- Confirm details against the repository before acting on them.
- Keep the startup summary short and factual.
- Do not rewrite memory during start unless the user explicitly asks.

## Expected Output
- A short project-state summary.
- The current feature and next recommended task.
- A readiness checkpoint for the next user request.
