---
description: "Validate CONSTITUTION.md integrity and enforce T0 rule presence for all Hefesto commands"
category: "helper"
type: "validator"
used_by: ["all commands"]
validates: "CONSTITUTION.md"
version: "1.0.0"
---

# CONSTITUTION Validation Logic

**Purpose**: Validate CONSTITUTION.md integrity and T0 rule presence  
**Used by**: All `/hefesto.*` commands (pre-execution check)

---

## Validation Workflow

```markdown
ON every /hefesto.* command execution:
  1. Run existence check
  2. If missing → Auto-restore (ERR-003)
  3. Run structure validation
  4. Run T0 rules validation
  5. If violations → Block operations (ERR-004)
  6. Cache validation result (valid until file modified)
  7. Proceed with command
```

---

## Validation Checks

### 1. File Existence Check

**Purpose**: Ensure CONSTITUTION.md is present at project root

**Implementation**:
```bash
# Unix/macOS/Linux
if [ ! -f "CONSTITUTION.md" ]; then
  trigger_restoration
fi

# Windows (PowerShell)
if (!(Test-Path "CONSTITUTION.md")) {
  Invoke-Restoration
}
```

**Expected Result**: File exists at `./CONSTITUTION.md`

**On Failure**: Execute auto-restoration (see constitution-recovery.md)

**References**: FR-010, ERR-003

---

### 2. YAML Frontmatter Validation

**Purpose**: Verify frontmatter structure and required fields

**Implementation**:
```markdown
PARSE YAML between "---" delimiters

REQUIRED FIELDS:
- version: string (SemVer format)
- status: enum ("ratified" | "draft")
- tier: enum ("T0" | "T1" | "T2")
- last_updated: timestamp (ISO 8601)

VALIDATION RULES:
- version MUST match ^\d+\.\d+\.\d+$
- status MUST be "ratified" (draft not allowed for operational use)
- tier MUST be "T0" (constitutional authority)
- last_updated MUST be valid ISO 8601 timestamp
```

**Example Valid Frontmatter**:
```yaml
---
version: "1.1.0"
status: ratified
tier: T0
last_updated: 2026-02-04T00:00:00Z
---
```

**On Failure**: Restore from bundle (structural corruption)

**References**: CONSTITUTION.md format, ADR-003

---

### 3. T0 Rules Presence Validation

**Purpose**: Ensure all 11 T0 rules are present and intact

**Implementation**:
```markdown
REQUIRED_T0_RULES = [
  "T0-HEFESTO-01",  # Agent Skills Standard
  "T0-HEFESTO-02",  # Human Gate Protocol
  "T0-HEFESTO-03",  # Progressive Disclosure (SKILL.md < 500 linhas)
  "T0-HEFESTO-04",  # Multi-CLI Detection
  "T0-HEFESTO-05",  # Local Storage
  "T0-HEFESTO-06",  # Validation
  "T0-HEFESTO-07",  # Skill Naming
  "T0-HEFESTO-08",  # Idempotency
  "T0-HEFESTO-09",  # Metadata
  "T0-HEFESTO-10",  # Cross-CLI Consistency
  "T0-HEFESTO-11",  # Security
]

FOR EACH rule_id IN REQUIRED_T0_RULES:
  search_pattern = "### " + rule_id + ":"
  
  IF NOT file_contains(search_pattern):
    violations.append(rule_id)

IF violations.length > 0:
  trigger_violation_error(violations)
```

**Expected Result**: All 11 T0 rules found with proper heading format

**On Failure**: Block operations, require manual intervention (ERR-004)

**References**: FR-010, T0 rules in CONSTITUTION.md

---

### 4. Structure Integrity Check

**Purpose**: Verify heading hierarchy and section organization

**Implementation**:
```markdown
EXPECTED STRUCTURE:
1. # (H1): Title
2. ## Tier 0 (T0) - Regras Absolutas (CONSTITUTION)
3. ### T0-HEFESTO-01: ... (T0 rule heading)
   ... (repeat for all 11 rules)
4. ## Tier 1 (T1) - Regras Normativas
5. ## Tier 2 (T2) - Regras Informativas

VALIDATION:
- H1 title present
- T0 section present before T1/T2
- All T0 rules within T0 section
- Heading hierarchy: H1 → H2 → H3 (no skips)
```

**Expected Result**: Logical structure with proper hierarchy

**On Failure**: Warn user, allow operations if T0 rules intact

**References**: CONSTITUTION.md structure

---

### 5. Content Integrity Check

**Purpose**: Verify T0 rules have descriptions (not just headings)

**Implementation**:
```markdown
FOR EACH rule_id IN REQUIRED_T0_RULES:
  section = extract_section(rule_id)
  
  VALIDATE:
  - Section contains "**Regra:**" or "**Rule:**" marker
  - Section has at least 50 characters of content
  - Section ends before next H3 heading or section boundary

IF section too short OR marker missing:
  warnings.append(rule_id + " may be incomplete")
```

**Expected Result**: Each T0 rule has substantive description

**On Failure**: Warn user, allow operations (non-critical)

**References**: CONSTITUTION.md content format

---

## Validation Cache

### Purpose

Avoid repeated file parsing on every command within same session

### Strategy

```markdown
cache = {
  file_path: "CONSTITUTION.md",
  last_modified: filesystem.stat(file_path).mtime,
  validation_result: null,
  validated_at: null
}

FUNCTION validate_constitution():
  current_mtime = filesystem.stat("CONSTITUTION.md").mtime
  
  IF cache.last_modified == current_mtime AND cache.validation_result != null:
    RETURN cache.validation_result  # Cache hit
  
  # Cache miss - run full validation
  result = run_all_checks()
  
  # Update cache
  cache.last_modified = current_mtime
  cache.validation_result = result
  cache.validated_at = current_timestamp()
  
  RETURN result
```

**Performance Impact**:
- First validation: ~500ms (file read + parsing)
- Cached validation: ~5ms (filesystem stat only)

**Cache Invalidation**: Automatic when file modified (mtime change)

---

## Validation Results

### Result Structure

```yaml
valid: boolean
checks:
  existence: "pass" | "restored"
  frontmatter: "pass" | "fail"
  t0_rules: "pass" | "fail"
  structure: "pass" | "warn"
  content: "pass" | "warn"
violations: []  # List of missing T0 rule IDs
warnings: []    # List of structural issues
restored: boolean
```

### Pass Conditions

```markdown
VALIDATION PASSES IF:
- File exists (or was restored successfully)
- Frontmatter valid
- All 11 T0 rules present
- (Structure and content warnings allowed)
```

### Fail Conditions

```markdown
VALIDATION FAILS IF:
- File missing and restoration fails
- Frontmatter invalid or missing required fields
- Any T0 rule missing
```

---

## Integration with Commands

### Pre-Execution Hook

```markdown
FUNCTION execute_hefesto_command(command, args):
  # MANDATORY: Validate before any operation
  validation = validate_constitution()
  
  IF NOT validation.valid:
    display_error(validation.violations)
    abort_with_exit_code(1)
  
  IF validation.warnings.length > 0:
    display_warnings(validation.warnings)
  
  # Proceed with command
  return command.run(args)
```

### Integration Checklist

**Every `/hefesto.*` command MUST**:
- ✅ Call `validate_constitution()` before any operation
- ✅ Block execution if validation fails (exit code 1)
- ✅ Display clear error messages referencing specific T0 violations
- ✅ Auto-restore if CONSTITUTION.md missing (transparent recovery)
- ✅ Display warnings for non-critical issues (allow operation to continue)

**Commands Integrated**:
- ✅ `/hefesto.init` - Validates before bootstrap
- ✅ `/hefesto.detect` - Validates before re-detection  
- ✅ `/hefesto.list` - Validates before listing
- 🔄 `/hefesto.create` - Will validate before skill generation (future)
- 🔄 `/hefesto.extract` - Will validate before skill extraction (future)
- 🔄 `/hefesto.validate` - Will validate before skill validation (future)
- 🔄 `/hefesto.adapt` - Will validate before adaptation (future)
- 🔄 `/hefesto.sync` - Will validate before sync (future)

### Example Integration in /hefesto.init

```markdown
# /hefesto.init Command - Phase 0: Pre-Execution Validation

1. Validate CONSTITUTION (pre-execution hook)
   validation = validate_constitution()
   
   IF validation.restored:
     LOG: "CONSTITUTION.md was missing, restored from bundle"
   
   IF NOT validation.valid:
     DISPLAY:
       ❌ Constitutional Violation: {validation.violations}
       All operations blocked until resolved.
     ABORT with exit code 1
   
   IF validation.warnings.length > 0:
     DISPLAY warnings (non-blocking)

2. Check if already initialized (only after CONSTITUTION valid)
3. Run CLI detection
4. Create directories
5. Generate report
6. Persist state
```

### Example Integration in /hefesto.detect

```markdown
# /hefesto.detect Command - Phase 0: Pre-Execution Validation

1. Validate CONSTITUTION (same as /hefesto.init)

2. Check if Hefesto initialized (only after CONSTITUTION valid)
   IF NOT file_exists("MEMORY.md"):
     DISPLAY: "Run /hefesto.init first"
     ABORT

3. Run CLI re-detection
4. Update MEMORY.md
5. Generate report
```

### Example Integration in /hefesto.list

```markdown
# /hefesto.list Command - Phase 0: Pre-Execution Validation

1. Validate CONSTITUTION (same as above)

2. Check if Hefesto initialized (only after CONSTITUTION valid)
   IF NOT file_exists("MEMORY.md"):
     DISPLAY: "Run /hefesto.init first"
     ABORT

3. Parse MEMORY.md (with corruption recovery)
4. Display CLIs and skills
5. Optionally check filesystem sync
```

---

## T0 Rule Enforcement and Operation Blocking

### Enforcement Principles

**T0 Rules are ABSOLUTE**:
- Cannot be bypassed or disabled
- Violations MUST block all operations
- No "force" or "skip" flags allowed
- Manual intervention required to resolve

### Operation Blocking Mechanism

```markdown
FUNCTION enforce_t0_compliance():
  
  validation = validate_constitution()
  
  IF NOT validation.valid:
    # CRITICAL: Violation detected
    
    1. Display violation details
       FOR EACH violation IN validation.violations:
         DISPLAY: "❌ Missing T0 rule: {violation}"
    
    2. Display resolution options
       DISPLAY:
         **Action Required**:
         1. Review CONSTITUTION.md for unauthorized changes
         2. Restore from backup: git restore CONSTITUTION.md
         3. Or force restore: /hefesto.restore-constitution --force
    
    3. Block operation
       LOG: "Operation blocked due to T0 violation"
       EXIT with code 1
  
  # Validation passed - operation can proceed
  RETURN success
```

### Blocked Operations

**When T0 violations detected, the following operations are BLOCKED**:

| Operation | Reason |
|-----------|--------|
| `/hefesto.init` | Cannot initialize without governance rules |
| `/hefesto.detect` | Cannot detect CLIs without enforcement framework |
| `/hefesto.list` | Cannot list state without validation |
| `/hefesto.create` | Cannot generate skills without Agent Skills spec compliance (T0-HEFESTO-01) |
| `/hefesto.extract` | Same as create |
| `/hefesto.validate` | Cannot validate without validation rules (T0-HEFESTO-06) |
| `/hefesto.adapt` | Cannot adapt without consistency rules (T0-HEFESTO-10) |
| `/hefesto.sync` | Cannot sync without idempotency rules (T0-HEFESTO-08) |

**ONLY ALLOWED operation when T0 violated**:
- `/hefesto.restore-constitution --force` (to fix the violation)

### T0 Rule Mapping to Operations

| T0 Rule | Enforced By | Impact if Violated |
|---------|-------------|-------------------|
| **T0-HEFESTO-01** (Agent Skills Standard) | `/hefesto.create`, `/hefesto.extract` | Blocks skill generation - cannot ensure spec compliance |
| **T0-HEFESTO-02** (Human Gate Protocol) | `/hefesto.create`, `/hefesto.extract` | Blocks skill generation - cannot ensure approval workflow |
| **T0-HEFESTO-03** (Progressive Disclosure) | `/hefesto.create`, `/hefesto.extract` | Blocks skill generation - cannot enforce 500-line limit |
| **T0-HEFESTO-04** (Multi-CLI Detection) | `/hefesto.init`, `/hefesto.detect` | Blocks initialization - cannot ensure automatic detection |
| **T0-HEFESTO-05** (Local Storage) | All operations | Blocks all operations - cannot ensure project-local storage |
| **T0-HEFESTO-06** (Validation) | `/hefesto.validate`, all operations | Blocks validation - no validation rules to enforce |
| **T0-HEFESTO-07** (Skill Naming) | `/hefesto.create`, `/hefesto.extract` | Blocks skill generation - cannot validate skill names |
| **T0-HEFESTO-08** (Idempotency) | All operations | Blocks all operations - cannot ensure safe re-execution |
| **T0-HEFESTO-09** (Metadata) | `/hefesto.create`, `/hefesto.extract` | Blocks skill generation - cannot ensure metadata requirements |
| **T0-HEFESTO-10** (Cross-CLI Consistency) | `/hefesto.adapt`, `/hefesto.sync` | Blocks adaptation - cannot ensure consistency |
| **T0-HEFESTO-11** (Security) | All operations | Blocks all operations - security framework missing |

### Violation Severity Levels

```markdown
SEVERITY_CRITICAL (blocks all operations):
- Any T0 rule missing
- CONSTITUTION.md missing and restoration fails
- Frontmatter invalid or missing required fields

SEVERITY_HIGH (blocks operation, suggests recovery):
- CONSTITUTION.md missing (auto-restores)
- T0 rule content modified (checksum mismatch - future)

SEVERITY_MEDIUM (warns but allows):
- Structure irregularities (heading hierarchy)
- Incomplete T0 rule descriptions

SEVERITY_LOW (logs only):
- Version mismatch warnings
- Formatting inconsistencies
```

### Enforcement Flow Diagram

```markdown
START Command Execution
  |
  v
Validate CONSTITUTION.md
  |
  ├─> File Missing?
  |   ├─> Yes → Auto-Restore
  |   |         ├─> Success → Continue
  |   |         └─> Fail → BLOCK (exit 1)
  |   └─> No → Continue
  |
  v
Parse YAML Frontmatter
  |
  ├─> Invalid?
  |   ├─> Yes → BLOCK (exit 1)
  |   └─> No → Continue
  |
  v
Check All 11 T0 Rules
  |
  ├─> Any Missing?
  |   ├─> Yes → BLOCK (exit 1)
  |   └─> No → Continue
  |
  v
Check Structure & Content
  |
  ├─> Warnings?
  |   ├─> Yes → Display Warnings
  |   └─> No → Continue
  |
  v
✅ CONSTITUTION VALID
  |
  v
Proceed with Command
```

### Bypass Prevention

**NO BYPASS MECHANISMS ALLOWED**:

```markdown
# ❌ FORBIDDEN
/hefesto.init --skip-constitution-check
/hefesto.create --force-without-validation
export HEFESTO_SKIP_T0=true

# ✅ ONLY ALLOWED
/hefesto.restore-constitution --force  # To fix violations
```

**Rationale**: T0 rules are constitutional law. Allowing bypass would:
- Compromise governance framework
- Enable generation of non-compliant skills
- Break security guarantees
- Violate Agent Skills spec requirements

### Manual Override (Emergency Only)

**ONLY in emergency situations** (e.g., CONSTITUTION.md bundle corrupted):

```markdown
1. User must manually create valid CONSTITUTION.md
2. User must manually verify all 11 T0 rules present
3. User must restart command
4. System validates new CONSTITUTION.md
5. If valid → proceed, if invalid → still blocked
```

**No programmatic bypass exists or will be added.**

---

## Error Messages

### ERR-003: Missing CONSTITUTION.md

```markdown
⚠️ Governance Recovery: CONSTITUTION.md missing

Restored from Hefesto bundle (v1.1.0)
All T0 rules intact

**Action**: None required (automatic recovery)
```

### ERR-004: Invalid CONSTITUTION.md

```markdown
❌ Constitutional Violation: T0 rules missing or invalid

Missing rules:
- T0-HEFESTO-01: Agent Skills Standard
- T0-HEFESTO-03: Progressive Disclosure

Modified rules detected:
- T0-HEFESTO-07: Skill Naming (content changed)

**Action Required**:
1. Review CONSTITUTION.md for unauthorized changes
2. Restore from backup: git restore CONSTITUTION.md
3. Or force restore: /hefesto.restore-constitution --force

All operations blocked until resolved.
```

### Warning: Structure Issues

```markdown
⚠️ CONSTITUTION.md Structure Warning

Non-critical issues detected:
- Heading hierarchy irregular (skipped H2)
- T0-HEFESTO-09 description may be incomplete

Operations will continue, but consider reviewing CONSTITUTION.md

**Action**: Review and fix if needed (non-blocking)
```

---

## Testing Validation

### Test Case 1: Valid CONSTITUTION

```bash
# Setup: Use bundled CONSTITUTION.md
cp templates/CONSTITUTION.md.bundle ./CONSTITUTION.md

# Execute
validate_constitution()

# Expected Result
valid: true
all_checks: pass
violations: []
warnings: []
```

### Test Case 2: Missing File

```bash
# Setup: Remove CONSTITUTION.md
rm CONSTITUTION.md

# Execute
validate_constitution()

# Expected Result
valid: true (after restoration)
checks.existence: "restored"
violations: []
```

### Test Case 3: Missing T0 Rule

```bash
# Setup: Remove T0-HEFESTO-01 section
sed -i '/T0-HEFESTO-01/,/T0-HEFESTO-02/d' CONSTITUTION.md

# Execute
validate_constitution()

# Expected Result
valid: false
checks.t0_rules: "fail"
violations: ["T0-HEFESTO-01"]
```

### Test Case 4: Corrupted Frontmatter

```bash
# Setup: Invalid YAML
echo "---\ninvalid: yaml: syntax:\n---" | cat - CONSTITUTION.md.tail > CONSTITUTION.md

# Execute
validate_constitution()

# Expected Result
valid: true (after restoration)
checks.frontmatter: "fail" → restored
```

---

## Performance Benchmarks

| Operation | Target | Strategy |
|-----------|--------|----------|
| First validation (cold) | < 500ms | Full file parse |
| Cached validation (warm) | < 5ms | Filesystem stat only |
| Auto-restoration | < 200ms | Bundle copy + verify |
| T0 rule search (11 rules) | < 100ms | Regex pattern matching |

**Total Impact on Command Execution**: < 10ms (cached) or < 700ms (cold + restore)

---

## References

- Research: CONSTITUTION Management (research.md #4)
- Error Handling: ERR-003, ERR-004 (error-handling.md)
- FR-010: Validate structure and T0 rules on every command
- User Story 4: Enforce Constitutional Governance
- CONSTITUTION.md: Source of T0 rules (project root)
