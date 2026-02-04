---
description: "Best practices guide for using Hefesto with Git version control including worktrees and submodules"
category: "documentation"
type: "guide"
topic: "git-integration"
last_updated: "2026-02-04"
version: "1.0.0"
---

# Git Integration Guide

**Purpose**: Best practices for using Hefesto with Git version control  
**Last Updated**: 2026-02-04

---

## Overview

Hefesto is designed to work seamlessly with Git. This guide covers:
- What to commit
- What to ignore
- Git worktree handling
- Submodule considerations
- Team collaboration

---

## Files to Commit

### Always Commit

These files should be tracked in version control:

```gitignore
# ✅ Commit these
CONSTITUTION.md          # Governance rules
MEMORY.md                # Project state
AGENTS.md                # AI agent bootstrap guide
.gitignore               # Git ignore patterns

# CLI skill directories (commit skills, not infrastructure)
.claude/skills/**/SKILL.md
.gemini/skills/**/SKILL.md
.opencode/skills/**/SKILL.md
.cursor/skills/**/SKILL.md
# (etc. for all CLIs)
```

**Rationale**:
- **CONSTITUTION.md**: Team needs same governance rules
- **MEMORY.md**: Shared project state (CLIs, skills)
- **Skills**: Share generated skills across team

### Never Commit

These files/patterns should be ignored:

```gitignore
# ❌ Don't commit these
MEMORY.md.backup.*       # Recovery backups
.hefesto/cache/          # Runtime cache (future)
.hefesto/debug.log       # Debug logs (future)
*.tmp
*.swp
```

---

## Recommended .gitignore

Add these patterns to your project's `.gitignore`:

```gitignore
# Hefesto - Backup files
MEMORY.md.backup.*
CONSTITUTION.md.backup.*

# Hefesto - Cache and logs (future)
.hefesto/cache/
.hefesto/debug.log
.hefesto/*.tmp

# OS-specific
.DS_Store
Thumbs.db
*.tmp
*.swp

# IDE
.vscode/
.idea/
*.iml

# Environment
.env*

# Logs
*.log
```

**Note**: CLI skill directories (`.claude/`, `.gemini/`, etc.) should be committed to share skills with team.

---

## Initial Setup (New Repository)

### Option 1: Initialize Hefesto First

```bash
# 1. Create repository
git init

# 2. Initialize Hefesto
/hefesto.init

# 3. Add .gitignore
cat > .gitignore <<'EOF'
MEMORY.md.backup.*
.DS_Store
*.log
.env*
EOF

# 4. Commit initial state
git add .
git commit -m "Initialize Hefesto Foundation"
```

### Option 2: Clone Existing Repository

```bash
# 1. Clone repository
git clone https://github.com/team/project.git
cd project

# 2. Hefesto already initialized?
if [ -f MEMORY.md ]; then
  echo "Hefesto already set up"
  /hefesto.list
else
  echo "Initialize Hefesto"
  /hefesto.init
fi

# 3. Verify state
/hefesto.list
```

---

## Team Collaboration

### Sharing Hefesto State

**MEMORY.md is shared across team**:
- Contains detected CLIs
- Contains skill registry
- Helps team coordinate skill development

**Best Practices**:
1. Commit MEMORY.md after generating skills
2. Pull before generating new skills
3. Resolve conflicts like normal Git files

### Handling MEMORY.md Conflicts

```bash
# Scenario: Merge conflict in MEMORY.md

# 1. Check conflict
git status
# both modified: MEMORY.md

# 2. View conflict
cat MEMORY.md
# <<<<<<< HEAD
# | skill-a | claude | ...
# =======
# | skill-b | gemini | ...
# >>>>>>> feature-branch

# 3. Option A: Manual resolution
# Edit MEMORY.md to include both skills
nano MEMORY.md

# 4. Option B: Rebuild from filesystem
rm MEMORY.md
/hefesto.init
# System rebuilds from skill directories

# 5. Verify and commit
/hefesto.list
git add MEMORY.md
git commit -m "Merge skill changes"
```

### Sharing Skills

**All team members get same skills**:

```bash
# Developer A: Create skill
/hefesto.create api-docs
git add .claude/skills/api-docs/
git commit -m "Add api-docs skill for Claude"
git push

# Developer B: Pull skill
git pull
/hefesto.list  # Shows api-docs skill
# Skill automatically available in .claude/skills/
```

---

## Git Worktrees

### How Hefesto Handles Worktrees

**Each worktree gets independent MEMORY.md**:
- Separate state per worktree
- Different CLIs can be detected per worktree
- Different skills can exist per worktree

**CONSTITUTION.md is shared**:
- Symlinked or copied from main worktree
- Same governance rules everywhere
- Modifications affect all worktrees

### Setup Example

```bash
# Main worktree
cd ~/projects/my-app
git worktree add ../my-app-feature feature-branch

# In main worktree
/hefesto.init
# Creates MEMORY.md, CONSTITUTION.md

# In feature worktree
cd ../my-app-feature
/hefesto.init
# Creates separate MEMORY.md
# Shares CONSTITUTION.md (symlink or copy)

# Verification
ls -la CONSTITUTION.md
# lrwxr-xr-x ... CONSTITUTION.md -> ../my-app/CONSTITUTION.md
```

### Best Practices for Worktrees

1. **Initialize each worktree separately**:
   ```bash
   cd feature-worktree
   /hefesto.init
   ```

2. **Don't commit worktree-specific MEMORY.md**:
   ```bash
   # Add to .git/info/exclude in feature worktree
   echo "MEMORY.md" >> .git/info/exclude
   ```

3. **Share CONSTITUTION.md**:
   ```bash
   # Main worktree has master copy
   # Feature worktrees symlink to it
   ln -s ../main-worktree/CONSTITUTION.md CONSTITUTION.md
   ```

4. **Coordinate skill development**:
   - Develop different skills in different worktrees
   - Merge skills back to main
   - Each worktree has independent skill set

---

## Git Submodules

### Submodules Can Have Own Hefesto

**Each submodule is independent**:
- Submodule can have its own Hefesto initialization
- Separate MEMORY.md and CONSTITUTION.md
- Own set of CLIs and skills

### Setup Example

```bash
# Parent repository
cd ~/projects/parent-app
/hefesto.init
git submodule add https://github.com/team/library.git libs/library

# Submodule
cd libs/library
/hefesto.init  # Independent initialization
cd ../..

# Commit submodule Hefesto state
cd libs/library
git add MEMORY.md CONSTITUTION.md
git commit -m "Initialize Hefesto in submodule"
git push

# Update parent to track submodule change
cd ~/projects/parent-app
git add libs/library
git commit -m "Update submodule with Hefesto"
```

### Best Practices for Submodules

1. **Initialize submodules independently**:
   - Each submodule has own `/hefesto.init`
   - Own CLI detection
   - Own skill set

2. **Share CONSTITUTION.md via parent** (optional):
   ```bash
   # Link submodule to parent's CONSTITUTION.md
   cd libs/library
   ln -s ../../CONSTITUTION.md CONSTITUTION.md
   ```

3. **Coordinate across boundaries**:
   - Skills in parent can reference submodule skills
   - Use consistent naming conventions
   - Document cross-boundary dependencies

---

## Branching Strategies

### Feature Branches

**MEMORY.md stays in sync**:

```bash
# Create feature branch
git checkout -b feature/new-skill
/hefesto.list  # Shows current skills

# Generate new skill
/hefesto.create new-feature
git add .claude/skills/new-feature/ MEMORY.md
git commit -m "Add new-feature skill"

# Merge to main
git checkout main
git merge feature/new-skill
# MEMORY.md updated with new skill
```

### Long-Running Branches

**Handle MEMORY.md divergence**:

```bash
# Development branch has different skills than main
git checkout develop
/hefesto.list  # 10 skills

git checkout main
/hefesto.list  # 8 skills

# Merge develop to main
git merge develop
# Resolve conflicts in MEMORY.md
# Result: main has 10 skills
```

---

## CI/CD Integration

### Pre-Commit Checks

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Validate Hefesto state before commit
/hefesto.list > /dev/null || {
  echo "Error: Hefesto state invalid"
  exit 1
}

# Check for backup files
if ls MEMORY.md.backup.* 2>/dev/null; then
  echo "Warning: Backup files found - clean up before commit"
  exit 1
fi

exit 0
```

### CI Pipeline

```yaml
# .github/workflows/hefesto.yml
name: Hefesto Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Validate Hefesto State
        run: |
          /hefesto.list
          /hefesto.list --check-sync
      
      - name: Check No Orphaned Skills
        run: |
          if /hefesto.list --check-sync | grep -q "Orphaned"; then
            echo "Error: Orphaned skills detected"
            exit 1
          fi
```

---

## Migration and Upgrades

### Upgrading Hefesto Version

```bash
# Check current version
grep "hefesto_version:" MEMORY.md
# hefesto_version: "1.0.0"

# After Hefesto upgrade
/hefesto.init --force
# Updates MEMORY.md with new version

# Verify upgrade
grep "hefesto_version:" MEMORY.md
# hefesto_version: "1.1.0"

# Commit version upgrade
git add MEMORY.md
git commit -m "Upgrade Hefesto to v1.1.0"
```

### Migrating Existing Project

```bash
# Project without Hefesto
cd existing-project

# Initialize Hefesto
/hefesto.init

# Commit Hefesto files
git add MEMORY.md CONSTITUTION.md AGENTS.md .gitignore
git commit -m "Add Hefesto Skill Generator"

# Push to remote
git push origin main
```

---

## Troubleshooting Git Issues

### Issue: MEMORY.md Merge Conflicts

**Solution**: Rebuild from filesystem

```bash
git checkout --theirs MEMORY.md  # Or --ours
/hefesto.init --force
git add MEMORY.md
git commit
```

### Issue: CONSTITUTION.md Modified by Git

**Solution**: Restore and re-validate

```bash
git restore CONSTITUTION.md
/hefesto.list  # Validates CONSTITUTION.md
```

### Issue: Skills Out of Sync

**Solution**: Use filesystem sync check

```bash
/hefesto.list --check-sync
# Fix orphaned/missing skills
git add .
git commit -m "Sync skills with MEMORY.md"
```

---

## Advanced: Git Hooks

### Post-Merge Hook

```bash
# .git/hooks/post-merge
#!/bin/bash

# Re-detect CLIs after merge (in case team added new CLI)
/hefesto.detect --force > /dev/null

# Verify state consistency
/hefesto.list --check-sync || {
  echo "Warning: Filesystem inconsistencies after merge"
  echo "Run '/hefesto.list --check-sync' to review"
}
```

### Pre-Push Hook

```bash
# .git/hooks/pre-push
#!/bin/bash

# Ensure no backup files being pushed
if git diff --cached --name-only | grep -q ".backup."; then
  echo "Error: Attempting to push backup files"
  exit 1
fi

# Validate state before push
/hefesto.list > /dev/null || {
  echo "Error: Invalid Hefesto state"
  exit 1
}
```

---

## References

- **Research**: specs/001-hefesto-foundation/research.md (#8 Git Integration)
- **Edge Case**: spec.md (Git worktrees/submodules handling)
- **Requirements**: FR-015 (Git repository compatibility)
