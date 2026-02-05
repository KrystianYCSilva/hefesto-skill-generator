---
description: "Validate MEMORY.md structure and detect corruption in project state files"
category: "helper"
type: "validator"
used_by: ["/hefesto.list", "/hefesto.detect", "state-reading operations"]
validates: "MEMORY.md"
version: "1.0.0"
---

# MEMORY.md Validator

**Purpose**: Validate MEMORY.md structure and detect corruption  
**Used by**: `/hefesto.list`, `/hefesto.detect`, all state-reading operations

---

## Validation Workflow

```markdown
ON state read operation:
  1. Run file existence check
  2. Run YAML frontmatter validation
  3. Run Markdown table structure validation
  4. Run data integrity validation
  5. If any check fails → Trigger recovery (ERR-002)
  6. Return parsed state
```

---

## Validation Checks

### 1. File Existence Check

**Purpose**: Ensure MEMORY.md is present

**Implementation**:
```markdown
IF NOT file_exists("MEMORY.md"):
  RETURN error({
    code: "MEMORY_MISSING",
    message: "MEMORY.md not found. Run /hefesto.init first.",
    recoverable: false
  })
```

**On Failure**: Cannot recover - user must run `/hefesto.init`

---

### 2. YAML Frontmatter Validation

**Purpose**: Verify frontmatter structure and required fields

**Implementation**:
```markdown
FUNCTION validate_frontmatter(content):
  
  1. Extract frontmatter section
     frontmatter_match = regex_match(content, /^---\n(.*?)\n---/s)
     IF NOT frontmatter_match:
       RETURN error("YAML_MISSING", "No YAML frontmatter found")
  
  2. Parse YAML
     yaml_content = frontmatter_match.group(1)
     TRY:
       frontmatter = parse_yaml(yaml_content)
     CATCH YAMLError as e:
       RETURN error("YAML_INVALID", "Invalid YAML syntax: {e}")
  
  3. Validate required fields
     REQUIRED_FIELDS = {
       "hefesto_version": string,
       "initialized": timestamp,
       "last_updated": timestamp
     }
     
     FOR EACH field, type IN REQUIRED_FIELDS:
       IF field NOT IN frontmatter:
         RETURN error("YAML_MISSING_FIELD", "Missing field: {field}")
       IF NOT isinstance(frontmatter[field], type):
         RETURN error("YAML_INVALID_TYPE", "Field {field} has wrong type")
  
  4. Validate field constraints
     IF NOT regex_match(frontmatter.hefesto_version, /^\d+\.\d+\.\d+$/):
       RETURN error("YAML_INVALID_VERSION", "Invalid version format")
     
     IF frontmatter.last_updated < frontmatter.initialized:
       RETURN error("YAML_INVALID_TIMESTAMP", "last_updated < initialized")
  
  RETURN success(frontmatter)
```

**On Failure**: Trigger recovery (corrupted frontmatter)

**References**: memory-template.md, data-model.md (Project State)

---

### 3. Markdown Table Structure Validation

**Purpose**: Verify CLI and skill tables are present and well-formed

**Implementation**:
```markdown
FUNCTION validate_tables(content):
  
  1. Check for required sections
     REQUIRED_SECTIONS = [
       "## Detected CLIs",
       "## Skill Registry",
       "## State Metadata"
     ]
     
     FOR EACH section IN REQUIRED_SECTIONS:
       IF section NOT IN content:
         RETURN error("TABLE_MISSING_SECTION", "Missing section: {section}")
  
  2. Validate CLI table structure
     cli_table = extract_section(content, "## Detected CLIs")
     
     # Check for table header
     IF NOT cli_table.contains("| CLI | Detection Method | Skills Directory | Version | Status |"):
       RETURN error("TABLE_INVALID_CLI_HEADER", "CLI table header malformed")
     
     # Parse table rows
     cli_rows = parse_table_rows(cli_table)
     FOR EACH row IN cli_rows:
       IF row.cells.length < 5:
         RETURN error("TABLE_INVALID_CLI_ROW", "CLI row has too few columns")
  
  3. Validate skill table structure
     skill_table = extract_section(content, "## Skill Registry")
     
     # Check for table header
     IF NOT skill_table.contains("| Skill Name | CLIs | Created | Last Modified |"):
       RETURN error("TABLE_INVALID_SKILL_HEADER", "Skill table header malformed")
     
     # Parse table rows (may be empty - no skills yet)
     skill_rows = parse_table_rows(skill_table)
     FOR EACH row IN skill_rows:
       IF row.cells.length < 4:
         RETURN error("TABLE_INVALID_SKILL_ROW", "Skill row has too few columns")
  
  RETURN success({cli_rows, skill_rows})
```

**On Failure**: Trigger recovery (corrupted tables)

**References**: memory-template.md

---

### 4. Data Integrity Validation

**Purpose**: Verify data values are valid and consistent

**Implementation**:
```markdown
FUNCTION validate_data_integrity(cli_rows, skill_rows):
  
  1. Validate CLI data
     FOR EACH cli IN cli_rows:
       # Validate CLI name
       IF cli.name NOT IN ["claude", "gemini", "codex", "copilot", "opencode", "cursor", "qwen"]:
         WARN("Unknown CLI: {cli.name}")
       
       # Validate detection method
       IF cli.detection_method NOT IN ["PATH", "config_directory", "manual"]:
         RETURN error("DATA_INVALID_METHOD", "Invalid detection method: {cli.detection_method}")
       
       # Validate status
       IF cli.status NOT IN ["active", "warning_no_path", "error_permission", "manual"]:
         RETURN error("DATA_INVALID_STATUS", "Invalid status: {cli.status}")
       
       # Validate version format (if not null)
       IF cli.version != "null" AND NOT regex_match(cli.version, /^\d+\.\d+\.\d+$/):
         WARN("Invalid version format for {cli.name}: {cli.version}")
  
  2. Validate skill data
     FOR EACH skill IN skill_rows:
       # Validate skill name format (Agent Skills spec)
       IF NOT regex_match(skill.name, /^[a-z0-9]+(-[a-z0-9]+)*$/):
         RETURN error("DATA_INVALID_SKILL_NAME", "Invalid skill name: {skill.name}")
       
       IF skill.name.length > 64:
         RETURN error("DATA_INVALID_SKILL_NAME", "Skill name too long: {skill.name}")
       
       # Validate CLIs reference
       skill_clis = skill.clis.split(",").trim()
       FOR EACH cli_ref IN skill_clis:
         IF cli_ref NOT IN [row.name FOR row IN cli_rows]:
           RETURN error("DATA_INVALID_CLI_REF", "Skill {skill.name} references unknown CLI: {cli_ref}")
       
       # Validate timestamps
       IF NOT is_iso8601(skill.created):
         RETURN error("DATA_INVALID_TIMESTAMP", "Invalid created timestamp: {skill.created}")
       IF NOT is_iso8601(skill.last_modified):
         RETURN error("DATA_INVALID_TIMESTAMP", "Invalid last_modified timestamp: {skill.last_modified}")
       IF skill.last_modified < skill.created:
         RETURN error("DATA_INVALID_TIMESTAMP", "Skill {skill.name}: last_modified < created")
  
  3. Check for duplicates
     cli_names = [cli.name FOR cli IN cli_rows]
     IF has_duplicates(cli_names):
       RETURN error("DATA_DUPLICATE_CLI", "Duplicate CLI entries found")
     
     skill_names = [skill.name FOR skill IN skill_rows]
     IF has_duplicates(skill_names):
       RETURN error("DATA_DUPLICATE_SKILL", "Duplicate skill entries found")
  
  RETURN success()
```

**On Failure**: Trigger recovery if critical errors, warn if minor issues

**References**: data-model.md (validation rules)

---

## Validation Results

### Result Structure

```yaml
valid: boolean
errors: []      # List of validation errors (blocking)
warnings: []    # List of validation warnings (non-blocking)
parsed_state:   # Parsed state if validation passed
  frontmatter: {...}
  detected_clis: [...]
  skill_registry: [...]
```

### Pass Conditions

```markdown
VALIDATION PASSES IF:
- File exists
- YAML frontmatter valid
- All required fields present
- Tables structurally valid
- No critical data integrity errors
- (Warnings allowed)
```

### Fail Conditions

```markdown
VALIDATION FAILS IF:
- File missing
- YAML frontmatter missing or invalid
- Required fields missing
- Table structure malformed
- Critical data integrity errors (invalid formats, broken references)
```

---

## Integration with Commands

### Example: /hefesto.list

```markdown
FUNCTION execute_list_command():
  
  1. Validate MEMORY.md
     validation = validate_memory_md("MEMORY.md")
     
     IF NOT validation.valid:
       # Trigger recovery
       recovery = recover_corrupted_memory()
       IF recovery.failed:
         DISPLAY: "❌ Cannot read MEMORY.md (recovery failed)"
         ABORT
       ELSE:
         DISPLAY: "⚠️ MEMORY.md was corrupted, recovered from filesystem"
         state = recovery.rebuilt_state
     ELSE:
       state = validation.parsed_state
  
  2. Display warnings (if any)
     FOR EACH warning IN validation.warnings:
       DISPLAY: "⚠️ {warning.message}"
  
  3. Continue with list display
     display_clis(state.detected_clis)
     display_skills(state.skill_registry)
```

---

## Testing Validation

### Test Case 1: Valid MEMORY.md

```bash
# Setup: Use valid MEMORY.md
/hefesto.init

# Execute
/hefesto.list

# Expected Result
- Validation passes
- State displayed correctly
- No warnings or errors
```

### Test Case 2: Missing YAML Frontmatter

```bash
# Setup: Remove frontmatter
tail -n +4 MEMORY.md > MEMORY.md.tmp && mv MEMORY.md.tmp MEMORY.md

# Execute
/hefesto.list

# Expected Result
- Validation fails: YAML_MISSING
- Recovery triggered
- State rebuilt from filesystem
```

### Test Case 3: Invalid YAML Syntax

```bash
# Setup: Corrupt YAML
sed -i '2s/hefesto_version/hefesto version/' MEMORY.md

# Execute
/hefesto.list

# Expected Result
- Validation fails: YAML_INVALID
- Recovery triggered
- Backup created
```

### Test Case 4: Missing Required Field

```bash
# Setup: Remove initialized field
sed -i '/^initialized:/d' MEMORY.md

# Execute
/hefesto.list

# Expected Result
- Validation fails: YAML_MISSING_FIELD
- Recovery triggered
```

### Test Case 5: Invalid Skill Name

```bash
# Setup: Add invalid skill name
echo "| Invalid_Skill | claude | 2026-02-04 | 2026-02-04 |" >> MEMORY.md

# Execute
/hefesto.list

# Expected Result
- Validation fails: DATA_INVALID_SKILL_NAME
- Recovery triggered
```

---

## Performance

| Operation | Target | Typical |
|-----------|--------|---------|
| File existence check | < 1ms | < 1ms |
| YAML parsing | < 10ms | 5-8ms |
| Table parsing | < 20ms | 10-15ms |
| Data validation | < 10ms | 5-8ms |
| **Total Validation** | **< 50ms** | **20-30ms** |

---

## References

- **Template**: templates/memory-template.md
- **Data Model**: data-model.md (Project State, CLI Detection Result, Skill Registry Entry)
- **Error Handling**: error-handling.md (ERR-002)
- **Recovery**: helpers/memory-recovery.md
- **Requirements**: FR-016 (corrupted MEMORY.md handling)
