---
description: Verify generated code and content actually works, not just exists
---

# Output Verification Rules

Before declaring any task complete, verify the output at four levels:

1. **Exists** — The file was actually created or modified (check with git status or ls)
2. **Substantive** — The content is real, not stubs (grep for TODO, FIXME, placeholder, "fill in later", hardcoded test values)
3. **Wired** — The output is connected to the rest of the system (imported, referenced, routed, linked)
4. **Functional** — The output works when executed (builds, passes tests, renders correctly)

- Never declare "done" after only creating the file — at minimum verify it's substantive
- Run the build after code changes to catch syntax and type errors immediately
- Run related tests after modifying tested code
- For UI changes, verify the component renders without errors
- For API changes, verify the endpoint responds correctly
- Check that new files are imported where needed — orphan files are invisible

**Examples of violations:**
- Creating a new component but not importing it in the parent → orphan file
- Writing a function with `// TODO: implement` → not substantive
- Adding a route handler but not registering the route → not wired
- Claiming "tests pass" without running them → not verified