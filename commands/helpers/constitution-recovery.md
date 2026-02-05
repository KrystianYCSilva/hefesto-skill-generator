---
description: "Auto-restore CONSTITUTION.md when missing or corrupted to maintain governance integrity"
category: "helper"
type: "recovery"
used_by: ["constitution-validator.md", "all commands"]
recovers: "CONSTITUTION.md"
version: "1.0.0"
---

# CONSTITUTION Recovery

**Purpose**: Auto-restore CONSTITUTION.md when missing or corrupted  
**Used by**: `constitution-validator.md`, all `/hefesto.*` commands

---

## Recovery Scenarios

### Scenario 1: File Missing (ERR-003)

**Trigger**: `CONSTITUTION.md` not found at project root

**Recovery**:
```markdown
1. Log: "CONSTITUTION.md missing, restoring from bundle"
2. Locate bundled CONSTITUTION.md
   - Path: {hefesto_root}/templates/CONSTITUTION.md.bundle
   - Or embedded in Hefesto distribution
3. Copy bundle to project root
   copy_file(bundle_path, "CONSTITUTION.md")
4. Verify restored file
   validation = validate_constitution()
   IF NOT validation.valid:
     ABORT with error (bundle itself corrupted - critical failure)
5. Log: "CONSTITUTION.md restored successfully"
6. RETURN success
```

**User Message**:
```markdown
⚠️ Governance Recovery: CONSTITUTION.md missing

Restored from Hefesto bundle (v1.1.0)
All T0 rules intact

**Action**: None required (automatic recovery)
```

**References**: FR-010, ERR-003

---

### Scenario 2: File Corrupted (ERR-004)

**Trigger**: `CONSTITUTION.md` exists but T0 rules violated or missing

**Recovery**:
```markdown
CRITICAL: Do NOT auto-restore (may overwrite intentional changes)

1. Identify violations
   missing_rules = validate_t0_rules()
   
2. Create backup (if not already backed up)
   timestamp = get_timestamp()
   copy_file("CONSTITUTION.md", "CONSTITUTION.md.backup.{timestamp}")

3. Report violations
   DISPLAY:
     ❌ Constitutional Violation: T0 rules missing or invalid
     Missing rules: {missing_rules}
     Backup created: CONSTITUTION.md.backup.{timestamp}

4. Provide restoration options
   DISPLAY:
     **Action Required**:
     1. Review CONSTITUTION.md for unauthorized changes
     2. Restore from backup: git restore CONSTITUTION.md
     3. Or force restore from bundle: /hefesto.restore-constitution --force

5. Block all operations
   ABORT with exit code 1
```

**User Message**:
```markdown
❌ Constitutional Violation: T0 rules missing or invalid

Missing rules:
- T0-HEFESTO-01: Agent Skills Standard
- T0-HEFESTO-03: Progressive Disclosure

Backup created: CONSTITUTION.md.backup.2026-02-04T14-30-00Z

**Action Required**:
1. Review CONSTITUTION.md for unauthorized changes
2. Restore from backup: git restore CONSTITUTION.md
3. Or force restore: /hefesto.restore-constitution --force

All operations blocked until resolved.
```

**References**: FR-010, ERR-004

---

## Bundle Location

### Bundled CONSTITUTION.md

**Expected Location** (one of):
1. `{hefesto_root}/templates/CONSTITUTION.md.bundle`
2. `{hefesto_root}/.context/governance/CONSTITUTION.md.bundle`
3. Embedded in Hefesto distribution (base64 or similar)

**Verification**:
```markdown
FUNCTION locate_constitution_bundle():
  search_paths = [
    "{hefesto_root}/templates/CONSTITUTION.md.bundle",
    "{hefesto_root}/.context/governance/CONSTITUTION.md.bundle",
    "{hefesto_install_dir}/share/CONSTITUTION.md.bundle"
  ]
  
  FOR EACH path IN search_paths:
    IF file_exists(path):
      RETURN path
  
  ABORT with error: "CRITICAL: Cannot locate CONSTITUTION.md bundle"
```

---

## Manual Restoration Command

### /hefesto.restore-constitution

**Purpose**: Manually restore CONSTITUTION.md from bundle (force option)

**Signature**:
```text
/hefesto.restore-constitution [--force] [--backup]

Options:
  --force    Overwrite existing CONSTITUTION.md without confirmation
  --backup   Create backup before restoration (default: true)
```

**Workflow**:
```markdown
1. Check if CONSTITUTION.md exists
   IF exists AND NOT --force:
     PROMPT: "CONSTITUTION.md exists. Overwrite? (y/n)"
     IF user != "y":
       ABORT

2. Create backup (if --backup)
   IF file_exists("CONSTITUTION.md") AND --backup:
     timestamp = get_timestamp()
     copy_file("CONSTITUTION.md", "CONSTITUTION.md.backup.{timestamp}")
     DISPLAY: "Backup created: CONSTITUTION.md.backup.{timestamp}"

3. Locate bundle
   bundle_path = locate_constitution_bundle()

4. Copy bundle to project root
   copy_file(bundle_path, "CONSTITUTION.md")

5. Validate restored file
   validation = validate_constitution()
   IF NOT validation.valid:
     DISPLAY: "❌ Restoration failed: Bundle is invalid"
     ABORT

6. Display success
   DISPLAY: "✅ CONSTITUTION.md restored from bundle (v{version})"
```

**Example Usage**:
```text
> /hefesto.restore-constitution --force

Backup created: CONSTITUTION.md.backup.2026-02-04T14-30-00Z
✅ CONSTITUTION.md restored from bundle (v1.1.0)
All T0 rules intact
```

---

## Recovery Testing

### Test Case 1: Missing File

```bash
# Setup
rm CONSTITUTION.md

# Trigger
/hefesto.init

# Expected Result
- File restored from bundle
- Bootstrap continues successfully
- No user intervention required
```

### Test Case 2: Corrupted File

```bash
# Setup: Remove T0-HEFESTO-01
sed -i '/T0-HEFESTO-01/,/T0-HEFESTO-02/d' CONSTITUTION.md

# Trigger
/hefesto.init

# Expected Result
- Validation detects missing T0 rule
- Backup created
- Operations blocked
- User prompted for action
```

### Test Case 3: Manual Restoration

```bash
# Setup: Corrupt CONSTITUTION.md
echo "invalid content" > CONSTITUTION.md

# Execute
/hefesto.restore-constitution --force

# Expected Result
- Backup created
- File restored from bundle
- Validation passes
- Success message displayed
```

---

## Error Handling

### Bundle Not Found

```markdown
IF cannot_locate_bundle():
  DISPLAY:
    ❌ CRITICAL: Cannot locate CONSTITUTION.md bundle
    
    Hefesto installation may be corrupted.
    
    **Action**:
    1. Reinstall Hefesto
    2. Or manually download CONSTITUTION.md from:
       https://github.com/your-org/hefesto/blob/main/CONSTITUTION.md
    3. Place at project root
  
  ABORT with exit code 2
```

### Bundle Invalid

```markdown
IF restored_file_invalid():
  DISPLAY:
    ❌ CRITICAL: CONSTITUTION.md bundle is corrupted
    
    Hefesto installation is compromised.
    
    **Action**:
    1. Reinstall Hefesto
    2. Report issue: https://github.com/your-org/hefesto/issues
  
  ABORT with exit code 2
```

---

## Versioning

### Version Compatibility

```markdown
FUNCTION check_constitution_version():
  current_hefesto_version = "1.0.0"  # From Hefesto
  constitution_version = extract_version("CONSTITUTION.md")
  
  IF constitution_version > current_hefesto_version:
    WARN:
      ⚠️ CONSTITUTION.md version ({constitution_version}) 
         is newer than Hefesto version ({current_hefesto_version})
      
      This may cause compatibility issues.
      Consider upgrading Hefesto.
  
  IF constitution_version < current_hefesto_version:
    INFO:
      ℹ️  CONSTITUTION.md version ({constitution_version})
         is older than Hefesto version ({current_hefesto_version})
      
      Consider updating: /hefesto.restore-constitution --force
```

---

## Security Considerations

### Bundle Integrity

**Recommendation**: Sign bundled CONSTITUTION.md to prevent tampering

```markdown
FUTURE ENHANCEMENT:

1. Generate checksum of bundled CONSTITUTION.md
   checksum = sha256(bundle_content)

2. Store checksum in Hefesto distribution
   CONSTITUTION_BUNDLE_SHA256 = "abc123..."

3. Verify checksum before restoration
   IF sha256(bundle_file) != CONSTITUTION_BUNDLE_SHA256:
     ABORT: "Bundle integrity check failed (tampered or corrupted)"
```

### Backup Security

- Backups stored in project directory (not version-controlled by default)
- Timestamp-based naming prevents conflicts
- Original file preserved for forensic analysis if needed

---

## References

- **Validation**: helpers/constitution-validator.md
- **Error Handling**: helpers/error-handling.md (ERR-003, ERR-004)
- **Platform**: helpers/platform-detection.md (file operations)
- **Requirements**: FR-010 (validate and restore CONSTITUTION.md)
- **User Story**: User Story 4 (Constitutional Governance)
