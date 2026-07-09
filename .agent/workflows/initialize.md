# Initialize Workflow

## Purpose
Set up the agent’s long-term working context for a repository by analyzing the project and creating the persistent memory files that future sessions will rely on.

## When It Should Be Used
Use this at the beginning of a new repository or when `.agent/memory/` does not yet contain a usable project summary.

## Steps the AI Should Execute
1. Read `AGENT.md` and the existing `.agent/memory/` files in the order defined there.
2. Inspect the repository at a high level to identify the project’s purpose, main technologies, architecture, important folders, and notable workflows.
3. Create the initial memory set with concise, high-signal summaries.
4. Record the current working state and the first recommended follow-up task.
5. Create the first session log entry for the current date.
6. Stop after initialization and wait for user direction.

## Files to Read
- `AGENT.md`
- `.agent/memory/overview.md`
- `.agent/memory/architecture.md`
- `.agent/memory/index.md`
- `.agent/memory/current.md`
- `.agent/memory/decisions.md`
- `.agent/memory/sessions/YYYY-MM-DD.md` if it exists
- Repository files needed to understand the project at a high level

## Files to Update
- `.agent/memory/overview.md`
- `.agent/memory/architecture.md`
- `.agent/memory/index.md`
- `.agent/memory/current.md`
- `.agent/memory/decisions.md`
- `.agent/memory/sessions/YYYY-MM-DD.md`

## Rules to Follow
- Do not invent project details.
- Keep memory concise and high level.
- Prefer repository evidence over assumptions.
- Do not write implementation code during initialization unless the user explicitly requests it.
- Avoid broad scanning once enough context has been gathered.

## Expected Output
- A populated persistent memory baseline.
- A brief summary of the project state.
- A clear next recommended task.
- A newly created session log entry.
