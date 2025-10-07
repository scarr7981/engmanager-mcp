# Trowel.io Development Workflow Protocol

## 1. Issue Selection & Planning

**Tools:** `mcp__github__list_issues`, `mcp__github__get_issue`

```bash
# Review open issues
mcp__github__list_issues owner:"scarr7981" repo:"trowel" state:"OPEN"

# Get detailed issue info
mcp__github__get_issue owner:"scarr7981" repo:"trowel" issue_number:<number>

# Create task list with TodoWrite tool
TodoWrite: Break down issue into actionable steps
```

**Protocol:**
- Review issue description and acceptance criteria
- Check issue comments for context
- Create todo list BEFORE starting work
- Identify which service(s) will be affected

## 2. Branch Creation & Checkout

**Tools:** `mcp__git__git_create_branch`, `mcp__git__git_checkout`

```bash
# Branch naming convention
feature/<description>-issue-<number>   # New features
fix/<description>-issue-<number>       # Bug fixes
refactor/<description>-issue-<number>  # Refactoring
docs/<description>-issue-<number>      # Documentation

# CRITICAL: Create AND checkout branch BEFORE any edits
mcp__git__git_create_branch branch_name:"feature/description-issue-N" base_branch:"main"
mcp__git__git_checkout branch_name:"feature/description-issue-N"

# Verify you're on the correct branch
mcp__git__git_status
```

**Protocol:**
- ALWAYS create branch from main
- ALWAYS checkout branch BEFORE making changes
- NEVER commit to main directly
- Double-check branch with git status before editing

## 3. Development Work

**Tools:** `Read`, `Edit`, `Write`, `Bash` (for npm/compilation)

```bash
# Read files to understand current implementation
Read file_path:"<path>"

# Make changes
Edit/Write as needed

# Verify TypeScript compilation
cd services/web-builder && npm run typecheck

# Mark todos as in_progress, then completed
TodoWrite: Update task status
```

**Protocol:**
- Read files before editing to understand context
- Make focused changes addressing specific issue
- Verify compilation after changes
- Update todo list: in_progress → completed
- Keep changes atomic and related to issue

## 4. Git Add & Commit

**Tools:** `mcp__git__git_add`, `mcp__git__git_commit`, `mcp__git__git_status`

```bash
# CRITICAL: Verify you're on feature branch
mcp__git__git_status  # Must show "On branch feature/..."

# Stage changes
mcp__git__git_add files:["path/to/file1", "path/to/file2"]

# Commit with conventional commit format
mcp__git__git_commit message:"feat: description of changes (Issue #N)

- Detailed change 1
- Detailed change 2
- Resolves #N"
```

**Commit Message Format:**
```
<type>: <short description> (Issue #N)

<detailed changes>

Resolves #N
```

**Types:** `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

**Protocol:**
- Verify branch BEFORE committing (learned from mistakes)
- Use conventional commit format
- Reference issue number in commit
- Include "Resolves #N" for auto-close on merge

## 5. Push & PR Creation

**Tools:** `Bash(git push)`, `mcp__github__create_pull_request`

```bash
# Push to remote
git push -u origin feature/description-issue-N

# Create PR with structured description
mcp__github__create_pull_request
  owner:"scarr7981"
  repo:"trowel"
  title:"feat: Short description (Issue #N)"
  head:"feature/description-issue-N"
  base:"main"
  body:"## Description
Fixes #N

## Changes
- Change 1
- Change 2

## Testing
- [ ] TypeScript compilation passes
- [ ] No console errors
- [ ] Feature works as expected

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2"
```

**PR Description Template:**
```markdown
## Description
Fixes #<issue_number>

## Changes
- Detailed change 1
- Detailed change 2

## Testing
- [ ] TypeScript compilation passes
- [ ] No console errors
- [ ] Feature works as expected

## Acceptance Criteria
- [ ] Criterion from issue
- [ ] Criterion from issue
```

**Protocol:**
- Push with `-u` flag for tracking
- Link to issue with "Fixes #N"
- Include acceptance criteria checklist
- Add testing verification section

## 6. Code Review Request

**Tools:** `mcp__ultrareview__ask_copilot` (preferred) or `mcp__ultrareview__ask_codex`

```bash
mcp__ultrareview__ask_copilot prompt:"Review PR #<number>:

Repository: scarr7981/trowel
PR: https://github.com/scarr7981/trowel/pull/<number>

Please evaluate:
1. Code Quality: [specific aspects]
2. Type Safety: [TypeScript concerns]
3. [Feature-specific concerns]
4. Breaking Changes: Any potential issues?
5. Ready to Merge: Overall assessment

[Brief description of changes]

Please provide a quality score and merge recommendation."
```

**Protocol:**
- Request Copilot review immediately after PR creation
- Include PR link and specific evaluation points
- Wait for review before user merges
- Address any concerns raised in review

## 7. Post-Merge Cleanup

**Tools:** `mcp__git__git_checkout`, `Bash(git pull)`, `Bash(git branch -d)`

```bash
# Switch to main
mcp__git__git_checkout branch_name:"main"

# Pull latest (includes merged PR)
git pull origin main

# Delete local feature branch
git branch -d feature/description-issue-N

# Verify issue auto-closed
mcp__github__get_issue owner:"scarr7981" repo:"trowel" issue_number:<N>
```

**Protocol:**
- ALWAYS switch to main after merge
- ALWAYS pull to sync with remote
- Delete local feature branch (cleanup)
- Verify issue was auto-closed by merge
- If not auto-closed, close manually with comment

## 8. Error Recovery Protocols

### **Wrong Branch Commit**
```bash
# If committed to wrong branch
git log  # Find commit SHA

# Checkout correct branch
mcp__git__git_checkout branch_name:"feature/correct-branch"

# Cherry-pick the commit
git cherry-pick <SHA>

# Push correct branch
git push origin feature/correct-branch

# Reset wrong branch
git checkout main
git reset --hard origin/main
```

### **Forgot to Create Branch**
```bash
# Stash changes
git stash push -m "WIP: Description"

# Create and checkout branch
mcp__git__git_create_branch branch_name:"feature/description-issue-N"
mcp__git__git_checkout branch_name:"feature/description-issue-N"

# Apply stashed changes
git stash pop
```

## 9. Tool Selection Rules

**Git Operations:**
- ✅ `mcp__git__*` tools (preferred)
- ✅ `Bash(git ...)` for operations not in MCP
- ❌ Never manual git commands without tools

**GitHub Operations:**
- ✅ `mcp__github__*` tools (always)
- ✅ `Bash(gh ...)` CLI as fallback
- ❌ Never web UI operations

**Code Review:**
- ✅ `mcp__ultrareview__ask_copilot` (preferred, faster)
- ✅ `mcp__ultrareview__ask_codex` (if Copilot fails)
- ❌ Never skip code review

**Development:**
- ✅ `Read`, `Edit`, `Write` for code changes
- ✅ `Bash(npm ...)` for build/compile verification
- ✅ `TodoWrite` for task tracking (mandatory)
- ❌ Never bash commands for file operations

## 10. Quality Gates

**Before Commit:**
- [ ] On correct feature branch (verify with git status)
- [ ] TypeScript compilation passes
- [ ] Changes address issue acceptance criteria
- [ ] Todo list updated

**Before PR:**
- [ ] Pushed to remote
- [ ] PR description complete with acceptance criteria
- [ ] Issue linked with "Fixes #N"
- [ ] Ready for code review

**Before Merge:**
- [ ] Copilot/Codex review completed
- [ ] Quality score ≥ 8.5/10 or concerns addressed
- [ ] User approval obtained
- [ ] CI/CD passes (if configured)

**After Merge:**
- [ ] Switched to main
- [ ] Pulled latest changes
- [ ] Deleted local feature branch
- [ ] Issue verified closed

## 11. Session Management

**Start of Session:**
```bash
# Check project status
mcp__github__list_issues owner:"scarr7981" repo:"trowel" state:"OPEN"

# Review recent PRs
mcp__github__list_pull_requests owner:"scarr7981" repo:"trowel" state:"all" perPage:5

# Create daily todo list
TodoWrite: List high-priority issues
```

**End of Session:**
```bash
# Verify clean state
mcp__git__git_status  # Should be on main, clean

# Document progress
mcp__memory__add_observations: Session work summary
```

## 12. Common Patterns

### **New Feature Development**
1. Select issue → TodoWrite plan
2. Create feature branch
3. Implement with regular todo updates
4. Verify compilation
5. Commit with conventional format
6. Push and create PR
7. Request Copilot review
8. User merges
9. Cleanup (main, pull, delete branch)

### **Bug Fix**
Same as feature, but use `fix/` prefix and focus on regression testing

### **Refactoring**
Same as feature, but use `refactor/` prefix and emphasize:
- No functional changes
- Backward compatibility
- Code reduction metrics

### **Documentation**
Use `docs/` prefix, simpler workflow, but still:
- Feature branch
- PR with review
- Merge and cleanup

## 13. Critical Lessons Learned

1. **ALWAYS verify branch before changes** (made this mistake twice)
2. **Create AND checkout branch before editing** (not just create)
3. **Use MCP tools over bash** (consistency, audit trail)
4. **TodoWrite is mandatory** (helps track progress)
5. **Request review immediately after PR** (don't wait)
6. **Standard cleanup after merge** (main, pull, delete branch)
7. **Conventional commits** (enables automation)
8. **Link issues in commits** (enables auto-close)

## 14. MCP Server Implementation Suggestions

**Server Name:** `trowel-workflow-mcp`

**Tools to Expose:**
1. `start_issue` - Validates issue, creates branch, sets up todos
2. `commit_changes` - Verifies branch, stages, commits with format
3. `create_pr` - Pushes, creates PR with template
4. `request_review` - Calls Copilot/Codex review
5. `post_merge_cleanup` - Switches to main, pulls, deletes branch
6. `recover_wrong_branch` - Cherry-pick recovery workflow

**Resources:**
- PR description templates
- Commit message templates
- Quality gate checklists
- Common error recovery procedures

**Prompts:**
- "Start work on Issue #N"
- "Ready to commit and PR"
- "Review PR #N"
- "Cleanup after merge"

This protocol represents the refined workflow developed through practical experience on Trowel.io.
