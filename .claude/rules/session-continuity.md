---
description: Ensure key workspace files stay current across sessions — the next session should never need a briefing on what happened in the last one
---

# Session Continuity

The workspace should carry context forward between sessions. When a session ends, the files should reflect what happened so the next session starts informed.

## Files to Keep Current

| File | Update when... | What changes |
|------|---------------|-------------|
| `CLAUDE.md` | Architecture, conventions, or structure changed | Add new directories, update tables, revise instructions |
| `context/roadmap.md` | Priorities shifted, items completed, new items emerged | Move items between sections, add new priorities |
| `context/` files | New decisions, constraints, or context surfaced | Add facts the next session will need |
| `.claude/skills/*/LEARNINGS.md` | A skill was used this session | Append what worked, what didn't |
| `plans/` | A plan was started, progressed, or completed | Update status, check off completed steps |

## The Rule

**The next session should never have to ask "what happened last time?"** If it would need to, something wasn't saved.

## Quick Check (30 seconds)

Before ending a session:

1. Did any workspace conventions or structure change? → Update CLAUDE.md
2. Did priorities shift or items get completed? → Update roadmap
3. Were new decisions made that affect future work? → Update relevant context file
4. Did I use a skill that has a LEARNINGS.md? → Append a learning entry
5. Is there an active plan? → Update its status