---
description: Git commit and branching standards
---

# Git Workflow Rules

- Write descriptive commit messages explaining *why*, not just *what*
- Keep commits atomic — one logical change per commit
- Never force-push to shared branches without explicit approval
- Never skip pre-commit hooks (no --no-verify)
- Create new commits rather than amending existing ones unless asked
- Stage specific files rather than using git add -A
- Never commit generated files, build artifacts, or dependencies
- Branch naming: `feature/`, `fix/`, `chore/` prefixes with short descriptions

**Examples of violations:**
- `"fix stuff"` → `"fix: prevent duplicate form submissions on slow connections"`
- Committing both a feature and a refactor in one commit → split into two
- `git add .` when only 2 files changed → `git add src/auth.ts src/auth.test.ts`