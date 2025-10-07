# Example Development Workflow

This is an example workflow procedure that demonstrates template variables and structured steps.

## 1. Issue Selection & Planning

**Tools:** GitHub issue tracker, TodoWrite tool

**Protocol:**
- Review open issues in {REPO_OWNER}/{REPO_NAME}
- Check issue description and acceptance criteria
- Create todo list BEFORE starting work
- Identify which components will be affected

**Example:**
```bash
# Get issue details
mcp__github__get_issue owner:"{REPO_OWNER}" repo:"{REPO_NAME}" issue_number:42

# Create task list with TodoWrite tool
TodoWrite: Break down issue into actionable steps
```

## 2. Branch Creation & Checkout

**Tools:** Git commands

**Protocol:**
- ALWAYS create branch from {DEFAULT_BRANCH}
- ALWAYS checkout branch BEFORE making changes
- NEVER commit to {DEFAULT_BRANCH} directly
- Double-check branch with git status before editing

**Branch naming convention:**
```
feature/<description>-issue-<number>   # New features
fix/<description>-issue-<number>       # Bug fixes
refactor/<description>-issue-<number>  # Refactoring
docs/<description>-issue-<number>      # Documentation
```

**Example:**
```bash
# Create and checkout branch
git checkout -b feature/add-login-issue-42

# Verify you're on the correct branch
git status
```

## 3. Development Work

**Tools:** Read, Edit, Write, Bash (for compilation)

**Protocol:**
- Read files before editing to understand context
- Make focused changes addressing specific issue
- Verify compilation/tests after changes
- Update todo list: in_progress → completed
- Keep changes atomic and related to issue

**Example:**
```bash
# Read files to understand current implementation
Read file_path:"src/auth/login.ts"

# Make changes
Edit/Write as needed

# Verify compilation
npm run typecheck

# Mark todos as in_progress, then completed
TodoWrite: Update task status
```

## 4. Git Add & Commit

**Tools:** Git commands

**Protocol:**
- Verify you're on feature branch BEFORE committing
- Use conventional commit format
- Reference issue number in commit
- Include "Resolves #N" for auto-close on merge

**Commit Message Format:**
```
<type>: <short description> (Issue #N)

<detailed changes>

Resolves #N
```

**Types:** `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

**Example:**
```bash
# Verify you're on feature branch
git status  # Must show "On branch feature/..."

# Stage changes
git add src/auth/login.ts src/auth/types.ts

# Commit with conventional format
git commit -m "feat: add user login functionality (Issue #42)

- Implement login form component
- Add authentication API integration
- Add form validation

Resolves #42"
```

## 5. Push & PR Creation

**Tools:** Git push, GitHub PR tools

**Protocol:**
- Push with `-u` flag for tracking
- Link to issue with "Fixes #N"
- Include acceptance criteria checklist
- Add testing verification section

**PR Description Template:**
```markdown
## Description
Fixes #{ISSUE_NUMBER}

## Changes
- Change 1
- Change 2

## Testing
- [ ] Tests pass
- [ ] No console errors
- [ ] Feature works as expected

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
```

**Example:**
```bash
# Push to remote
git push -u origin feature/add-login-issue-42

# Create PR (using GitHub CLI or web interface)
gh pr create \
  --title "feat: Add user login functionality (Issue #42)" \
  --body "Fixes #42

## Changes
- Implement login form component
- Add authentication API integration
- Add form validation

## Testing
- [x] TypeScript compilation passes
- [x] All tests pass
- [x] Manual testing completed"
```

## 6. Code Review & Merge

**Protocol:**
- Request review from team
- Address any feedback
- Wait for approval before merge
- Squash commits if needed

## 7. Post-Merge Cleanup

**Protocol:**
- ALWAYS switch to {DEFAULT_BRANCH} after merge
- ALWAYS pull to sync with remote
- Delete local feature branch (cleanup)
- Verify issue was auto-closed by merge

**Example:**
```bash
# Switch to main
git checkout {DEFAULT_BRANCH}

# Pull latest (includes merged PR)
git pull origin {DEFAULT_BRANCH}

# Delete local feature branch
git branch -d feature/add-login-issue-42

# Verify issue closed
gh issue view 42
```

## Error Recovery Protocols

### Wrong Branch Commit

If you committed to the wrong branch:

```bash
# Find commit SHA
git log

# Checkout correct branch
git checkout feature/correct-branch

# Cherry-pick the commit
git cherry-pick <SHA>

# Reset wrong branch
git checkout {DEFAULT_BRANCH}
git reset --hard origin/{DEFAULT_BRANCH}
```

### Forgot to Create Branch

If you made changes without creating a branch:

```bash
# Stash changes
git stash push -m "WIP: Description"

# Create and checkout branch
git checkout -b feature/description-issue-N

# Apply stashed changes
git stash pop
```

## Quality Gates

### Before Commit:
- [ ] On correct feature branch (verify with git status)
- [ ] Code compiles/builds successfully
- [ ] Changes address issue acceptance criteria
- [ ] Todo list updated

### Before PR:
- [ ] Pushed to remote
- [ ] PR description complete with acceptance criteria
- [ ] Issue linked with "Fixes #N"
- [ ] Ready for code review

### Before Merge:
- [ ] Code review completed and approved
- [ ] All tests pass
- [ ] No merge conflicts
- [ ] CI/CD passes (if configured)

### After Merge:
- [ ] Switched to {DEFAULT_BRANCH}
- [ ] Pulled latest changes
- [ ] Deleted local feature branch
- [ ] Issue verified closed

## Common Patterns

### New Feature Development
1. Select issue → TodoWrite plan
2. Create feature branch
3. Implement with regular todo updates
4. Verify compilation/tests
5. Commit with conventional format
6. Push and create PR
7. Request review
8. Merge after approval
9. Cleanup (switch to main, pull, delete branch)

### Bug Fix
Same as feature, but use `fix/` prefix and focus on:
- Root cause analysis
- Regression testing
- Prevention of similar bugs

### Refactoring
Same as feature, but use `refactor/` prefix and emphasize:
- No functional changes
- Backward compatibility
- Code quality improvements
