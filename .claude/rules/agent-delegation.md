---
description: Guidelines for when and how to delegate work to sub-agents
globs:
  - ".claude/agents/**"
---

# Agent Delegation Rules

- Use agents for tasks that benefit from isolation: parallel research, code review, testing
- Read-only tasks (research, review, audit) should restrict tools to Read, Grep, Glob only
- Agents that need to run commands should get Bash but not Write or Edit
- Never give agents more tools than they need — principle of least privilege
- Set appropriate maxTurns: 5-10 for focused tasks, 15-20 for complex research
- Agents cannot see conversation history — provide all necessary context in the prompt
- Prefer agents over inline work when the task would consume significant context
- For time-sensitive tasks, run multiple agents in parallel rather than sequentially

**Examples of violations:**
- Giving a code reviewer agent Write permissions → it should only Read and report
- Setting maxTurns to 50 for a simple search → use 5-10
- Spawning an agent for a single-file lookup → just use Read directly
- Not providing context files in the agent prompt → agent will miss critical info