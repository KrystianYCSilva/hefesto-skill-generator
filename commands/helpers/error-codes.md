---
description: "Complete reference of Hefesto error codes with causes, resolutions, and diagnostic procedures"
category: "helper"
type: "reference"
audience: ["users", "ai-agents"]
version: "1.0.0"
---

# Error Codes Reference

**Purpose**: Complete reference of Hefesto error codes, causes, and resolutions  
**Audience**: Users and AI agents troubleshooting issues

---

## Error Code Format

```text
ERR-XXX: Error Category - Specific Issue

Error codes follow this structure:
- ERR-001 to ERR-099: File system and permission errors
- ERR-100 to ERR-199: State management errors  
- ERR-200 to ERR-299: Validation errors
- ERR-300 to ERR-399: CLI detection errors
- ERR-400 to ERR-499: Skill generation errors (future)
```

---

## Critical Errors (Block Operations)

### ERR-001: Permission Denied

**Category**: Filesystem  
**Severity**: Medium (partial success allowed)  
**Exit Code**: 0 (continues with other CLIs)

**Cause**:
- Insufficient permissions to create directory
- Parent directory is read-only
- Filesystem mounted read-only

**Error Message**:
```text
❌ Permission Error: {CLI Name}
   Cannot create directory: {path}
   Reason: Permission denied

Fix:
- Run: chmod +w {parent_directory}
- Or manually create: mkdir -p {path} && chmod +w {path}
- Or run with appropriate permissions
```

**Resolution**:
1. Check permissions: `ls -la {parent_directory}`
2. Fix permissions: `chmod +w {parent_directory}`
3. Or manually create directory with correct permissions
4. Re-run command

**References**: FR-017, error-handling.md

---

### ERR-002: Corrupted MEMORY.md

**Category**: State Management  
**Severity**: High (auto-recoverable)  
**Exit Code**: 0 (auto-recovery)

**Cause**:
- Invalid YAML syntax in frontmatter
- Malformed Markdown tables
- Missing required fields
- Manual editing errors

**Error Message**:
```text
⚠️ State Recovery: MEMORY.md corrupted

Backup created: MEMORY.md.backup.{timestamp}
Rebuilt state from filesystem:
- Detected {cli_count} CLI directories
- Found {skill_count} skills

✅ State recovered successfully
```

**Resolution**:
- Automatic: System backs up corrupted file and rebuilds from filesystem
- Manual: Review backup if original data needed
- Prevention: Don't manually edit MEMORY.md

**References**: FR-016, memory-recovery.md, Edge case clarification #1

---

### ERR-003: Missing CONSTITUTION.md

**Category**: Governance  
**Severity**: High (auto-recoverable)  
**Exit Code**: 0 (auto-restoration)

**Cause**:
- CONSTITUTION.md manually deleted
- File missing from project
- Incomplete project clone

**Error Message**:
```text
⚠️ Governance Recovery: CONSTITUTION.md missing

Restored from Hefesto bundle (v{version})
All T0 rules intact

**Action**: None required (automatic recovery)
```

**Resolution**:
- Automatic: System restores from bundled copy
- Manual: Review restored file if customizations were lost
- Prevention: Don't delete CONSTITUTION.md (tracked in version control)

**References**: FR-010, constitution-recovery.md, Edge case clarification #4

---

### ERR-004: Invalid CONSTITUTION.md

**Category**: Governance  
**Severity**: Critical (blocks all operations)  
**Exit Code**: 1 (abort)

**Cause**:
- T0 rules missing or modified
- Invalid YAML frontmatter
- Manual unauthorized modifications

**Error Message**:
```text
❌ Constitutional Violation: T0 rules missing or invalid

Missing rules:
- T0-HEFESTO-01: Agent Skills Standard
- T0-HEFESTO-03: Progressive Disclosure

**Action Required**:
1. Review CONSTITUTION.md for unauthorized changes
2. Restore from backup: git restore CONSTITUTION.md
3. Or force restore: /hefesto.restore-constitution --force

All operations blocked until resolved.
```

**Resolution**:
1. Check CONSTITUTION.md for modifications
2. Restore from version control: `git restore CONSTITUTION.md`
3. Or force restore: `/hefesto.restore-constitution --force`
4. Verify all 11 T0 rules present
5. Re-run command

**References**: FR-010, constitution-validator.md, User Story 4

---

### ERR-005: No CLIs Detected

**Category**: CLI Detection  
**Severity**: Medium (requires user input)  
**Exit Code**: 0 (manual specification)

**Cause**:
- No AI CLIs installed
- CLIs not in PATH
- Config directories not found

**Error Message**:
```text
⚠️ No AI CLIs detected automatically

Which AI CLI do you use? (Select numbers, comma-separated)
1. Claude Code
2. Gemini CLI
3. OpenAI Codex
4. VS Code/Copilot
5. OpenCode
6. Cursor
7. Qwen Code

Enter selection: _
```

**Resolution**:
1. Install at least one AI CLI
2. Ensure CLI is in PATH: `which {cli-name}`
3. Or use manual specification when prompted
4. Re-run `/hefesto.detect` after installation

**References**: FR-013, cli-detection-strategy.md

---

### ERR-006: Disk Space Insufficient

**Category**: Filesystem  
**Severity**: Critical (blocks operations)  
**Exit Code**: 1 (abort)

**Cause**:
- Less than 100MB free disk space
- Disk full during directory creation

**Error Message**:
```text
❌ Insufficient Disk Space

Required: ~100MB
Available: {available_space}MB

**Action**: Free up disk space and retry
```

**Resolution**:
1. Check disk space: `df -h .`
2. Free up at least 100MB
3. Remove unnecessary files
4. Re-run command

**References**: error-handling.md, Assumption about disk space

---

### ERR-007: Invalid Skill Name

**Category**: Validation  
**Severity**: Low (input error)  
**Exit Code**: 1 (reject input)

**Cause**:
- Skill name contains uppercase letters
- Skill name contains special characters
- Skill name too long (> 64 characters)
- Invalid format (not matching Agent Skills spec)

**Error Message**:
```text
❌ Invalid Skill Name: "{name}"

Requirements:
- Lowercase letters and numbers only
- Hyphens allowed (not at start/end)
- Max 64 characters
- Examples: code-review, api-docs, test-generator

Suggestion: "{suggested_name}"
```

**Resolution**:
1. Use only lowercase letters, numbers, and hyphens
2. Keep name under 64 characters
3. Follow pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`
4. Use suggested name or create valid name

**References**: T0-HEFESTO-07, data-model.md (Skill Registry Entry validation)

---

## Warning Codes (Non-Blocking)

### WARN-001: CLI Config Only (Not in PATH)

**Category**: CLI Detection  
**Severity**: Low (non-blocking)  
**Impact**: Skills can be generated but may not work

**Cause**:
- CLI config directory exists (`~/.{cli}/`)
- CLI executable not found in PATH
- CLI was installed but later removed/uninstalled

**Warning Message**:
```text
⚠️ Warning: {CLI Name}

Config directory found but executable not in PATH
- Config: {config_path}
- Impact: Skills can be generated but may not work until CLI is reinstalled

Fix: Install {CLI Name} and ensure it's in PATH, then run /hefesto.detect
```

**Resolution**:
- Install or reinstall the CLI
- Add CLI to PATH environment variable
- Run `/hefesto.detect` to update status
- Or ignore if CLI no longer used

**References**: FR-025, Edge case clarification #5

---

### WARN-002: MEMORY.md Not Initialized

**Category**: State Management  
**Severity**: Low (expected on first run)  
**Impact**: Need to run initialization

**Warning Message**:
```text
ℹ️  Hefesto not initialized

Run /hefesto.init to set up Hefesto in this project
```

**Resolution**:
- Run `/hefesto.init` to initialize
- This is expected on first use

**References**: All commands check for MEMORY.md existence

---

### WARN-003: Filesystem Inconsistency Detected

**Category**: State Synchronization  
**Severity**: Low (informational)  
**Impact**: State may not match filesystem

**Warning Message**:
```text
⚠️ Filesystem inconsistencies detected:

Orphaned skills (in filesystem, not tracked):
- .claude/skills/old-skill/

Missing skills (tracked but deleted from filesystem):
- api-docs (expected in .cursor/skills/)

Recommendation: Run /hefesto.sync to reconcile state
```

**Resolution**:
- Review inconsistencies
- Run `/hefesto.sync` to fix (future command)
- Or manually reconcile filesystem and MEMORY.md

**References**: state-sync.md, FR-038

---

### WARN-004: Version Mismatch

**Category**: CLI Detection  
**Severity**: Low (informational)  
**Impact**: Version info outdated

**Warning Message**:
```text
ℹ️  CLI Version Update Detected:

{CLI Name}
- Tracked: v{old_version}
- Current: v{new_version}

Run /hefesto.detect --force to update version
```

**Resolution**:
- Run `/hefesto.detect --force` to update versions
- Or ignore if version doesn't matter

**References**: state-sync.md

---

### WARN-005: Structure Warning

**Category**: Validation  
**Severity**: Low (non-critical)  
**Impact**: Cosmetic issues only

**Warning Message**:
```text
⚠️ CONSTITUTION.md Structure Warning

Non-critical issues detected:
- Heading hierarchy irregular (skipped H2)
- T0-HEFESTO-09 description may be incomplete

Operations will continue, but consider reviewing CONSTITUTION.md

**Action**: Review and fix if needed (non-blocking)
```

**Resolution**:
- Review CONSTITUTION.md structure
- Fix heading hierarchy if desired
- Complete incomplete descriptions
- Or ignore (non-blocking)

**References**: constitution-validator.md

---

## Info Codes (Informational)

### INFO-001: Already Initialized

**Category**: Initialization  
**Severity**: None (informational)  
**Impact**: None

**Message**:
```text
ℹ️  Hefesto already initialized

Initialized: {timestamp}
CLIs: {count}
Skills: {count}

Use /hefesto.init --force to re-initialize
Use /hefesto.list to see current state
```

**Action**: None needed (expected behavior)

**References**: hefesto.init.md (idempotency check)

---

### INFO-002: No New CLIs Detected

**Category**: CLI Detection  
**Severity**: None (informational)  
**Impact**: None

**Message**:
```text
ℹ️  No new CLIs detected

{count} CLIs already configured:
- {CLI 1}
- {CLI 2}
...

No changes needed. All CLIs already detected.
```

**Action**: None needed (expected behavior)

**References**: hefesto.detect.md

---

### INFO-003: No Skills Generated Yet

**Category**: State  
**Severity**: None (informational)  
**Impact**: None

**Message**:
```text
## Skills

No skills generated yet. Run /hefesto.create to generate your first skill.
```

**Action**: Run `/hefesto.create` to generate skills (future)

**References**: hefesto.list.md

---

## Recovery Procedures

### Standard Recovery Flow

```markdown
1. Identify error code from message
2. Check error severity:
   - Critical → Operations blocked, manual fix required
   - High → Auto-recovery attempted
   - Medium → Partial success, some operations may proceed
   - Low → Warning only, operations proceed

3. Follow resolution steps for specific error
4. Re-run command after fix
5. Verify success with /hefesto.list
```

### Auto-Recovery Errors

These errors trigger automatic recovery:
- **ERR-002**: Corrupted MEMORY.md (backs up, rebuilds from filesystem)
- **ERR-003**: Missing CONSTITUTION.md (restores from bundle)

### Manual Intervention Required

These errors require manual fixes:
- **ERR-004**: Invalid CONSTITUTION.md (restore from version control or bundle)
- **ERR-006**: Disk space insufficient (free up space)
- **ERR-007**: Invalid skill name (correct name format)

---

## Error Prevention

### Best Practices

1. **Don't manually edit MEMORY.md**
   - Use commands to modify state
   - Let system manage state files

2. **Don't delete CONSTITUTION.md**
   - Keep in version control
   - System will auto-restore if missing

3. **Check permissions before running**
   - Ensure write access to project directory
   - Run with appropriate privileges if needed

4. **Ensure sufficient disk space**
   - Keep at least 100MB free
   - Monitor disk usage in large projects

5. **Install CLIs properly**
   - Add to PATH environment variable
   - Verify with `which {cli-name}`

6. **Use version control**
   - Commit MEMORY.md and CONSTITUTION.md
   - Easy rollback on issues

---

## Diagnostic Commands

### Check System Status

```bash
# Check if initialized
/hefesto.list

# Check CONSTITUTION validity
# (automatically checked by all commands)

# Check filesystem sync
/hefesto.list --check-sync

# Re-detect CLIs
/hefesto.detect
```

### Check Permissions

```bash
# Unix/macOS
ls -la .
ls -la .claude/

# Windows
dir /a

# Check directory writability
touch .test && rm .test
```

### Check Disk Space

```bash
# Unix/macOS
df -h .

# Windows
dir
```

### Check CLI Installation

```bash
# Check if CLI in PATH
which claude
which gemini
which opencode

# Windows
where.exe claude
```

---

## Error Code Summary Table

| Code | Category | Severity | Auto-Recover | Exit Code |
|------|----------|----------|--------------|-----------|
| ERR-001 | Filesystem | Medium | No | 0 (partial) |
| ERR-002 | State | High | Yes | 0 |
| ERR-003 | Governance | High | Yes | 0 |
| ERR-004 | Governance | Critical | No | 1 |
| ERR-005 | Detection | Medium | No (manual) | 0 |
| ERR-006 | Filesystem | Critical | No | 1 |
| ERR-007 | Validation | Low | No | 1 |
| WARN-001 | Detection | Low | N/A | 0 |
| WARN-002 | State | Low | N/A | 0 |
| WARN-003 | Sync | Low | N/A | 0 |
| WARN-004 | Detection | Low | N/A | 0 |
| WARN-005 | Validation | Low | N/A | 0 |
| INFO-001 | Init | None | N/A | 0 |
| INFO-002 | Detection | None | N/A | 0 |
| INFO-003 | State | None | N/A | 0 |

---

## References

- **Error Handling**: commands/helpers/error-handling.md
- **Recovery**: commands/helpers/memory-recovery.md, constitution-recovery.md
- **Validation**: commands/helpers/constitution-validator.md, memory-validator.md
- **Troubleshooting**: .context/troubleshooting/foundation-issues.md
