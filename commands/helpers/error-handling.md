---
description: "Consistent error handling patterns, recovery strategies, and reporting formats for all Hefesto commands"
category: "helper"
type: "patterns"
used_by: ["all commands"]
version: "1.0.0"
---

# Error Handling Patterns

**Purpose**: Define consistent error handling, recovery strategies, and reporting formats  
**Used by**: All `/hefesto.*` commands

---

## Error Categories

| Category | Severity | Recovery | User Action |
|----------|----------|----------|-------------|
| **Permission Errors** | Medium | Skip & continue | Fix permissions or manual action |
| **Corrupted State** | High | Auto-recover | Review backup if needed |
| **Missing Files** | Medium | Auto-restore | None (transparent) |
| **Invalid Input** | Low | Reject with guidance | Correct input |
| **System Errors** | High | Abort with details | Report issue |

---

## Error Codes

### ERR-001: Permission Denied

**Scenario**: Cannot create directory or write file due to filesystem permissions

**Detection**:
```bash
mkdir .claude/skills/ 2>&1 | grep -i "permission denied"
```

**Recovery**:
```markdown
1. Log error with specific path and operation
2. Skip the problematic CLI (partial success)
3. Continue with remaining CLIs
4. Include in final error report
```

**User Message**:
```markdown
❌ Permission Error: claude
   Cannot create directory: .claude/skills/
   Reason: Permission denied
   
   Fix: Run one of the following:
   - chmod +w . (Unix/macOS)
   - Run terminal with appropriate permissions
   - Manually create directory: mkdir .claude/skills/
```

**References**: FR-017, Edge case clarification #2

---

### ERR-002: Corrupted MEMORY.md

**Scenario**: MEMORY.md exists but cannot be parsed (invalid YAML, malformed tables)

**Detection**:
```markdown
TRY:
  Parse YAML frontmatter
  Parse Markdown tables
CATCH ParseError:
  → ERR-002
```

**Recovery**:
```markdown
1. Create backup: MEMORY.md → MEMORY.md.backup.{ISO8601_TIMESTAMP}
2. Log recovery action
3. Create fresh MEMORY.md from template
4. Rescan filesystem:
   a. Detect existing CLI directories
   b. Scan skill directories for skill count
   c. Rebuild state from filesystem
5. Continue operation
```

**User Message**:
```markdown
⚠️ State Recovery: MEMORY.md corrupted

Backup created: MEMORY.md.backup.2026-02-04T14-30-00Z
Rebuilt state from filesystem:
- Detected 3 CLI directories
- Found 5 skills

**Action**: Review backup if needed, or delete backup if recovery successful
```

**References**: FR-016, Edge case clarification #1

---

### ERR-003: Missing CONSTITUTION.md

**Scenario**: CONSTITUTION.md not found at project root

**Detection**:
```bash
test -f CONSTITUTION.md || echo "ERR-003"
```

**Recovery**:
```markdown
1. Log warning: "CONSTITUTION.md missing, restoring from bundle"
2. Copy bundled CONSTITUTION.md to project root
3. Validate restored file
4. Continue operation
```

**User Message**:
```markdown
⚠️ Governance Recovery: CONSTITUTION.md missing

Restored from Hefesto bundle (v1.1.0)
All T0 rules intact

**Action**: None required (automatic recovery)
```

**References**: FR-010, Edge case clarification #4

---

### ERR-004: Invalid CONSTITUTION.md

**Scenario**: CONSTITUTION.md exists but T0 rules violated or missing

**Detection**:
```markdown
FOR EACH rule_id IN ["T0-HEFESTO-01", ..., "T0-HEFESTO-11"]:
  IF NOT constitution_contains(rule_id):
    → ERR-004
```

**Recovery**:
```markdown
CRITICAL: Do NOT auto-restore (may overwrite intentional changes)

1. Block all operations
2. Report missing/invalid T0 rules
3. Provide restoration command
4. Abort
```

**User Message**:
```markdown
❌ Constitutional Violation: T0 rules missing or invalid

Missing rules: T0-HEFESTO-01, T0-HEFESTO-03

**Action Required**:
1. Review CONSTITUTION.md for unauthorized changes
2. Restore from backup: git restore CONSTITUTION.md
3. Or force restore: /hefesto.restore-constitution

All operations blocked until resolved.
```

**References**: FR-010, User Story 4

---

### ERR-005: No CLIs Detected

**Scenario**: Auto-detection found zero CLIs (PATH and config)

**Detection**:
```markdown
IF COUNT(detected_clis) = 0 AFTER detection phases:
  → ERR-005
```

**Recovery**:
```markdown
1. Prompt user for manual specification
2. Present list of supported CLIs
3. Create directories for selected CLIs with status="manual"
4. Continue operation
```

**User Message**:
```markdown
⚠️ No AI CLIs detected automatically

**Action Required**: Select which CLI you use

1. Claude Code
2. Gemini CLI
3. OpenAI Codex
4. VS Code/Copilot
5. OpenCode
6. Cursor
7. Qwen Code

Enter numbers (comma-separated) or 'q' to quit: _
```

**References**: FR-013, Edge case from spec.md

---

### ERR-006: Disk Space Insufficient

**Scenario**: Not enough disk space to create directories or write files

**Detection**:
```bash
df -h . | awk 'NR==2 {print $4}' | grep -E '^[0-9]+M$|^[0-9]K$'
```

**Recovery**:
```markdown
NO AUTO-RECOVERY

1. Calculate required space (~100MB for full initialization)
2. Report current available space
3. Abort operation
```

**User Message**:
```markdown
❌ Insufficient Disk Space

Required: ~100MB
Available: 15MB

**Action**: Free up disk space and retry
```

**References**: Assumption "at least 100MB free disk space"

---

### ERR-007: Invalid Skill Name

**Scenario**: Skill name doesn't match Agent Skills spec format

**Detection**:
```markdown
IF NOT skill_name.matches('^[a-z0-9]+(-[a-z0-9]+)*$'):
  → ERR-007
IF skill_name.length > 64:
  → ERR-007
```

**Recovery**:
```markdown
NO AUTO-RECOVERY (user input error)

1. Reject skill creation
2. Explain format requirements
3. Suggest corrected name if possible
```

**User Message**:
```markdown
❌ Invalid Skill Name: "MySkill_v1"

Requirements:
- Lowercase letters and numbers only
- Hyphens allowed (not at start/end)
- Max 64 characters
- Examples: code-review, api-docs, test-generator

Suggestion: "my-skill-v1"
```

**References**: T0-HEFESTO-07, Data Model: Skill Registry Entry validation

---

## General Error Handling Principles

### 1. Fail-Safe Design

```markdown
ALWAYS prefer partial success over total failure

IF operation affects multiple entities:
  FOR EACH entity:
    TRY:
      Process entity
    CATCH error:
      Log error
      Continue to next entity
  
  Report all successes and failures at end
```

**Example**: Creating CLI directories for 7 CLIs
- If 2 fail with permission errors → Create remaining 5
- Report 5 successes, 2 failures with fix instructions

---

### 2. Idempotent Operations

```markdown
ALL operations MUST be safely repeatable

IF entity already exists:
  Verify it matches expected state
  If matches → No-op
  If differs → Log warning, update if safe

NEVER error on repeated operations
```

**Example**: Running `/hefesto.init` twice
- First run: Creates directories
- Second run: Detects existing directories, verifies structure, reports "already initialized"

---

### 3. Transparent Recovery

```markdown
FOR recoverable errors:
  1. Attempt auto-recovery
  2. Log recovery action
  3. Inform user AFTER success
  4. Provide rollback option

FOR non-recoverable errors:
  1. Do NOT attempt changes
  2. Report error with context
  3. Provide fix instructions
  4. Abort gracefully
```

---

### 4. Detailed Error Context

**Every error message MUST include**:
1. **What**: Clear description of error
2. **Where**: Specific file/path/command
3. **Why**: Root cause if known
4. **How to Fix**: Actionable next steps

**Bad Error**:
```markdown
❌ Error: Operation failed
```

**Good Error**:
```markdown
❌ Permission Error: claude
   Cannot create directory: /home/user/project/.claude/skills/
   Reason: Permission denied (parent directory read-only)
   
   Fix:
   - Run: chmod +w /home/user/project
   - Or manually create: mkdir -p .claude/skills && chmod +w .claude/skills
```

---

## Error Reporting Format

### Inline Errors (During Operation)

```markdown
⚠️ Warning: {brief description}
❌ Error: {brief description}
```

### Summary Report (At End)

```markdown
## Operation Summary

✅ Successful: {count}/{total}
⚠️  Warnings: {count}
❌ Errors: {count}

### Successful Operations
- {entity}: {action} → {result}

### Warnings
- {entity}: {warning_message}
  → {impact}

### Errors
- {entity}: {error_message}
  → Fix: {actionable_steps}

**Next Steps**: {recommended_actions}
```

---

## Testing Error Scenarios

### Simulate Permission Error

```bash
# Create read-only directory
mkdir .test-cli
chmod -w .test-cli
# Attempt to create subdirectory → should trigger ERR-001
```

### Simulate Corrupted MEMORY.md

```bash
# Create invalid YAML
echo "---\ninvalid: yaml: syntax:\n---" > MEMORY.md
# Run any command → should trigger ERR-002 recovery
```

### Simulate Missing CONSTITUTION.md

```bash
# Move to backup
mv CONSTITUTION.md CONSTITUTION.md.hidden
# Run any command → should trigger ERR-003 recovery
```

---

## References

- Research: Error Handling and Recovery Patterns (research.md #5)
- FR-016: Corrupted MEMORY.md recovery
- FR-017: Permission error graceful handling
- SC-003: 95%+ success rate (error handling enables partial success)
- Edge cases: All 7 scenarios addressed
