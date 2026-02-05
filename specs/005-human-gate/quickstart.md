# Feature 005: Human Gate - Quickstart Guide

> **Version**: 1.0.0  
> **Status**: Production Ready  
> **Audience**: Developers and AI agents using Hefesto

---

## What is Human Gate?

Human Gate is Hefesto's approval workflow that enforces **T0-HEFESTO-02**: No files are written without explicit human approval. Every skill creation, extraction, or adaptation goes through a mandatory review step before persistence.

---

## 5 Quick Usage Examples

### Example 1: Basic Skill Creation with Human Gate

```bash
# Command
/hefesto.create "Skill for code refactoring with inline comments"

# What happens:
# 1. Hefesto generates skill content in memory
# 2. Validates against Agent Skills spec
# 3. Displays formatted preview showing:
#    - Skill name and description
#    - Target CLIs (claude, opencode, gemini, etc.)
#    - File paths to be created
#    - Total file count and size
#    - First 50 lines of SKILL.md
# 4. Prompts: [approve] [expand] [edit] [reject]

# User types: approve

# Result:
# ✓ Skill 'code-refactoring-comments' created successfully!
# Created files:
#   ✓ .claude/skills/code-refactoring-comments/SKILL.md
#   ✓ .opencode/skills/code-refactoring-comments/SKILL.md
#   ✓ .gemini/skills/code-refactoring-comments/SKILL.md
# Total: 3 CLIs, 3 files, 4.2 KB
```

**Key takeaway**: Human Gate prevents accidental file creation by requiring explicit approval.

---

### Example 2: Wizard Mode for Guided Skill Creation

```bash
# Command (no description argument triggers wizard)
/hefesto.create

# Wizard steps through 4 inputs:
# Step 1/4: Skill Name (kebab-case)
# > api-error-handler

# Step 2/4: Description (one sentence)
# > Handles API errors with retry logic and graceful degradation

# Step 3/4: Instructions (core workflow, 2-5 sentences)
# > When API calls fail, log the error, retry up to 3 times with exponential backoff.
# > If all retries fail, return cached data or default fallback response.

# Step 4/4: Resources (optional)
# > [Press Enter to skip or enter resource type: scripts/references/assets]
# [Pressed Enter]

# Final Review displayed with all collected inputs
# User confirms: yes

# Proceeds to Human Gate with generated preview
# User types: approve

# Result:
# ✓ Skill 'api-error-handler' created successfully!
```

**Key takeaway**: Wizard Mode guides beginners through structured input collection before Human Gate.

---

### Example 3: Expanding Skills with JIT Resources

```bash
# Command
/hefesto.create "Database migration skill"

# Human Gate displays preview
# User types: expand

# Expansion workflow:
# Add resources to skill (iterative):
#   [scripts] - Executable scripts (bash, python, etc.)
#   [references] - Documentation snippets (markdown, txt)
#   [assets] - Static files (json, yaml, csv)
#   [done] - Finish expansion

# User types: scripts
# Enter script filename: migrate.sh
# Enter script content (end with Ctrl+D on Unix, Ctrl+Z on Windows):
# #!/bin/bash
# alembic upgrade head
# ^D

# Add another resource? [scripts/references/assets/done]: references
# Enter reference filename: migration-guide.md
# Enter reference content:
# # Database Migration Best Practices
# - Always backup before migration
# - Test in staging first
# ^D

# Add another resource? [scripts/references/assets/done]: done

# Updated preview displayed with resources shown:
#   Resources:
#     scripts/migrate.sh (45 bytes)
#     references/migration-guide.md (112 bytes)

# User types: approve

# Result:
# ✓ Skill 'database-migration' created successfully!
# Created files:
#   ✓ .claude/skills/database-migration/SKILL.md
#   ✓ .claude/skills/database-migration/scripts/migrate.sh
#   ✓ .claude/skills/database-migration/references/migration-guide.md
```

**Key takeaway**: `[expand]` option allows adding scripts, references, and assets without restarting.

---

### Example 4: Inline Editing with Validation

```bash
# Command
/hefesto.create "Authentication skill"

# Human Gate displays preview
# User types: edit

# Hefesto opens SKILL.md in $EDITOR (vim/nano/notepad)
# User modifies content, saves, and closes editor

# Hefesto re-validates edited content against Agent Skills spec
# Validation passed! Displaying updated preview...

# New preview displayed with changes
# User types: approve

# Result:
# ✓ Skill 'authentication-skill' created successfully!

# --- Alternative scenario: Validation failure ---

# User types: edit
# Editor opens, user introduces invalid YAML frontmatter
# Saves and closes editor

# Hefesto re-validates:
# Validation failed after editing:
#   • Invalid YAML frontmatter: mapping values are not allowed here
#   • Missing required field: 'description'

# Options:
#   [retry-edit] - Fix validation errors in editor
#   [discard-changes] - Discard edits and return to original
#   [abort] - Cancel entire operation

# User types: retry-edit
# Editor reopens with invalid content for correction
# User fixes errors, saves, closes

# Validation passed!
# User types: approve

# Result:
# ✓ Skill 'authentication-skill' created successfully!
```

**Key takeaway**: `[edit]` option enables power users to fine-tune skills with automatic validation.

---

### Example 5: Collision Handling and Wizard Timeout Recovery

```bash
# Scenario A: Collision Detection
# User accidentally tries to create skill with existing name

/hefesto.create "api-error-handler"

# Hefesto detects collision:
# ⚠️  Collision detected: 'api-error-handler' already exists
# Existing skill:
#   Name: api-error-handler
#   Description: Handles API errors with retry logic
#   Created: 2026-02-04 10:30:00
#   Size: 3.1 KB

# Resolution options:
#   [overwrite] - Replace with new skill (backup created)
#   [merge] - Merge sections interactively
#   [cancel] - Abort operation

# User types: overwrite

# Backup created: .hefesto/backups/api-error-handler-2026-02-05T14-30-45.tar.gz
# Human Gate displays preview
# User types: approve

# Result:
# ✓ Skill 'api-error-handler' overwritten successfully!
# Backup: .hefesto/backups/api-error-handler-2026-02-05T14-30-45.tar.gz

# --- Scenario B: Wizard Timeout Recovery ---

/hefesto.create

# Wizard starts:
# Step 1/4: Skill Name
# > complex-data-pipeline

# Step 2/4: Description
# > Processes streaming data with transformations and validation

# Step 3/4: Instructions
# > [User gets distracted, doesn't respond for 5 minutes]

# Human Gate timed out after 5 minutes.
# Operation automatically cancelled.
# State saved to: .hefesto/temp/wizard-state-2026-02-05T14-30-00.json

# User returns and resumes:
/hefesto.resume .hefesto/temp/wizard-state-2026-02-05T14-30-00.json

# Resuming wizard session...
# State file: wizard-state-2026-02-05T14-30-00.json

# Wizard resumes at Step 3/4:
# Step 3/4: Instructions (core workflow, 2-5 sentences)
# > [User completes remaining steps]

# Wizard Complete - Proceeding to Human Gate
# User types: approve

# Result:
# ✓ Skill 'complex-data-pipeline' created successfully!
```

**Key takeaway**: Hefesto handles collisions gracefully with backups, and wizard timeouts are recoverable via `/hefesto.resume`.

---

## Decision Flow Summary

```
/hefesto.create → Generate → Validate → Preview → Human Gate
                                                      ↓
                                    ┌─────────────────┼─────────────────┐
                                    ↓                 ↓                 ↓
                              [approve]          [expand]          [edit]          [reject]
                                    ↓                 ↓                 ↓                 ↓
                            Persist files    Add resources    Open editor      Cancel (no files)
                                    ↓                 ↓                 ↓
                                Success      Updated preview   Re-validate
                                             → Human Gate     → Human Gate
```

---

## Key Features Reference

| Feature | Command Option | Purpose | User Story |
|---------|----------------|---------|------------|
| **Human Gate** | Auto (all commands) | Mandatory approval before file writes | US1 (P1) |
| **Wizard Mode** | `/hefesto.create` (no args) | Guided 4-step input for beginners | US2 (P2) |
| **JIT Expansion** | `[expand]` at Human Gate | Add scripts/references/assets iteratively | US3 (P2) |
| **Collision Detection** | Auto (if skill exists) | Overwrite/merge/cancel with backup | US4 (P2) |
| **Inline Editing** | `[edit]` at Human Gate | Fine-tune SKILL.md with validation | US5 (P3) |
| **Timeout Recovery** | `/hefesto.resume <path>` | Resume interrupted wizard sessions | US2 (P2) |

---

## File Locations

### Created Skills
```
.claude/skills/{skill-name}/SKILL.md
.opencode/skills/{skill-name}/SKILL.md
.gemini/skills/{skill-name}/SKILL.md
```

### Backups (on overwrite)
```
.hefesto/backups/{skill-name}-{timestamp}.tar.gz
```

### Wizard State (on timeout)
```
.hefesto/temp/wizard-state-{timestamp}.json
```

### Audit Logs
```
.hefesto/logs/operations.jsonl  # Structured operation log
.hefesto/logs/security.log      # Security events (T0-HEFESTO-11)
```

---

## Success Criteria Verification

| Criterion | How to Test | Expected Result |
|-----------|-------------|-----------------|
| **SC-001**: Human Gate blocks writes | Type `[reject]` at preview | No files created, confirmation message |
| **SC-002**: Wizard collects 4 inputs | Run `/hefesto.create` without args | 4-step workflow, final review displayed |
| **SC-003**: Expansion adds resources | Type `[expand]` → add script | Updated preview shows resources |
| **SC-004**: Collision creates backup | Create existing skill → overwrite | `.tar.gz` backup in `.hefesto/backups/` |
| **SC-005**: Inline edit validates | Type `[edit]` → introduce error | Validation errors shown, retry offered |
| **SC-006**: Response < 2 seconds | Run any command | Preview appears within 2s |
| **SC-009**: Atomic rollback works | Simulate disk full during write | All files rolled back, error message |
| **SC-010**: Timeout saves state | Start wizard, wait 5 min | State saved, `/hefesto.resume` path shown |

---

## Troubleshooting

### Preview not displaying colors?
- **Cause**: Terminal doesn't support ANSI codes
- **Solution**: Hefesto auto-detects and falls back to plain text

### Wizard timing out too quickly?
- **Cause**: 5-minute default timeout (FR-005)
- **Solution**: Resume with `/hefesto.resume <path>` (state preserved)

### Editor not launching?
- **Cause**: `$EDITOR` not set
- **Solution**: Set `export EDITOR=vim` (or nano/notepad) in shell config

### Validation errors after editing?
- **Cause**: Invalid frontmatter or missing required fields
- **Solution**: Type `[retry-edit]` to fix in editor, or `[discard-changes]` to revert

### Backup restore needed?
- **Cause**: Accidentally overwrote skill
- **Solution**: Extract `.hefesto/backups/{skill-name}-{timestamp}.tar.gz`

---

## Next Steps

1. **Read Full Spec**: See `specs/005-human-gate/spec.md` for complete feature documentation
2. **View Contracts**: Check `specs/005-human-gate/contracts/` for API details
3. **Check Data Model**: Review `specs/005-human-gate/data-model.md` for object structures
4. **Explore Examples**: Run commands above to experience Human Gate workflow

---

**Quickstart Guide** | Feature 005 Human Gate | v1.0.0 | 2026-02-05
