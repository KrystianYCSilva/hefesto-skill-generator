---
description: "Recover corrupted MEMORY.md by rebuilding project state from filesystem scanning"
category: "helper"
type: "recovery"
used_by: ["memory-validator.md", "state-reading commands"]
recovers: "MEMORY.md"
version: "1.0.0"
---

# MEMORY.md Recovery

**Purpose**: Recover corrupted MEMORY.md by rebuilding state from filesystem  
**Used by**: `memory-validator.md`, all state-reading commands

---

## Recovery Scenarios

### Scenario 1: Corrupted YAML Frontmatter

**Trigger**: YAML parsing fails (invalid syntax, missing fields)

**Recovery Strategy**:
```markdown
1. Create backup
   timestamp = get_timestamp()
   copy_file("MEMORY.md", "MEMORY.md.backup.{timestamp}")
   LOG: "Backup created: MEMORY.md.backup.{timestamp}"

2. Create fresh frontmatter
   frontmatter = {
     hefesto_version: current_hefesto_version,
     initialized: current_timestamp,  # Original lost
     last_updated: current_timestamp
   }

3. Rebuild CLI detection results from filesystem
   detected_clis = scan_cli_directories()

4. Rebuild skill registry from filesystem
   skill_registry = scan_skill_directories()

5. Generate new MEMORY.md
   write_memory_md(frontmatter, detected_clis, skill_registry)

6. Validate recovered file
   validation = validate_memory_md("MEMORY.md")
   IF NOT validation.valid:
     ABORT: "Recovery failed - unable to rebuild valid state"

7. Return recovered state
   RETURN {
     recovered: true,
     backup_path: "MEMORY.md.backup.{timestamp}",
     state: parse_memory_md("MEMORY.md")
   }
```

**User Message**:
```markdown
⚠️ State Recovery: MEMORY.md corrupted

Backup created: MEMORY.md.backup.2026-02-04T16-00-00Z
Rebuilt state from filesystem:
- Detected 3 CLI directories
- Found 5 skills

✅ State recovered successfully

Note: Original initialization timestamp lost (using current time)
Review backup if needed: MEMORY.md.backup.2026-02-04T16-00-00Z
```

**References**: FR-016, ERR-002

---

### Scenario 2: Corrupted Markdown Tables

**Trigger**: Table structure invalid (missing headers, malformed rows)

**Recovery Strategy**:
```markdown
1. Create backup (as above)

2. Extract valid frontmatter
   IF frontmatter_valid:
     keep_frontmatter = parse_frontmatter("MEMORY.md")
   ELSE:
     keep_frontmatter = create_default_frontmatter()

3. Rebuild tables from filesystem
   detected_clis = scan_cli_directories()
   skill_registry = scan_skill_directories()

4. Generate new MEMORY.md with recovered frontmatter
   write_memory_md(keep_frontmatter, detected_clis, skill_registry)

5. Return recovered state
```

**User Message**:
```markdown
⚠️ State Recovery: MEMORY.md tables corrupted

Backup created: MEMORY.md.backup.2026-02-04T16-00-00Z
Frontmatter preserved (timestamps intact)
Rebuilt tables from filesystem:
- Detected 3 CLI directories
- Found 5 skills

✅ State recovered successfully
```

---

### Scenario 3: Invalid Data Values

**Trigger**: Data validation fails (invalid CLI names, broken references)

**Recovery Strategy**:
```markdown
1. Create backup

2. Attempt to preserve valid entries
   valid_clis = []
   FOR EACH cli IN parsed_clis:
     IF validate_cli_entry(cli):
       valid_clis.append(cli)
     ELSE:
       LOG: "Discarding invalid CLI entry: {cli}"

3. Scan filesystem for missing CLIs
   filesystem_clis = scan_cli_directories()
   
   FOR EACH fs_cli IN filesystem_clis:
     IF fs_cli NOT IN valid_clis:
       valid_clis.append(fs_cli)

4. Rebuild skill registry (similar approach)

5. Generate corrected MEMORY.md
```

**User Message**:
```markdown
⚠️ State Recovery: Invalid data detected

Backup created: MEMORY.md.backup.2026-02-04T16-00-00Z
Removed 1 invalid CLI entry
Preserved 3 valid entries
Rescanned filesystem and added 1 missing CLI

✅ State corrected
```

---

## Filesystem Scanning

### Scan CLI Directories

```markdown
FUNCTION scan_cli_directories():
  
  detected_clis = []
  supported_cli_ids = ["claude", "gemini", "codex", "copilot", "opencode", "cursor", "qwen"]
  
  FOR EACH cli_id IN supported_cli_ids:
    skills_dir = ".{cli_id}/skills/"
    
    IF directory_exists(skills_dir):
      # CLI directory exists - attempt to determine how it was detected
      
      # Check if CLI is in PATH
      IF command_exists(cli_id):
        detection_method = "PATH"
        executable_path = get_command_path(cli_id)
        version = try_get_version(cli_id)
        status = "active"
      ELSE:
        # Check for config directory
        config_path = get_config_path(cli_id)
        IF directory_exists(config_path):
          detection_method = "config_directory"
          executable_path = null
          version = null
          status = "warning_no_path"
        ELSE:
          # Must have been manual
          detection_method = "manual"
          executable_path = null
          version = null
          status = "manual"
      
      detected_clis.append({
        id: cli_id,
        name: get_cli_display_name(cli_id),
        detection_method: detection_method,
        executable_path: executable_path,
        version: version,
        skills_directory_path: skills_dir,
        status: status
      })
  
  RETURN detected_clis
```

**Performance**: < 500ms (sequential directory checks + parallel CLI detection)

---

### Scan Skill Directories

```markdown
FUNCTION scan_skill_directories():
  
  skill_registry = []
  
  # Get all CLI directories
  detected_clis = scan_cli_directories()
  
  FOR EACH cli IN detected_clis:
    skills_dir = cli.skills_directory_path
    
    IF directory_exists(skills_dir):
      # List subdirectories (each is a skill)
      skill_dirs = list_directories(skills_dir)
      
      FOR EACH skill_dir IN skill_dirs:
        skill_name = basename(skill_dir)
        
        # Check if skill already in registry (from other CLI)
        existing_skill = skill_registry.find(s => s.name == skill_name)
        
        IF existing_skill:
          # Skill exists for another CLI - add this CLI to list
          IF cli.id NOT IN existing_skill.clis:
            existing_skill.clis.append(cli.id)
        ELSE:
          # New skill - get metadata from filesystem
          skill_metadata = get_skill_metadata(skill_dir)
          
          skill_registry.append({
            name: skill_name,
            clis: [cli.id],
            created: skill_metadata.created OR current_timestamp,
            last_modified: skill_metadata.last_modified OR current_timestamp
          })
  
  RETURN skill_registry
```

**Performance**: < 200ms (directory scanning)

---

### Get Skill Metadata

```markdown
FUNCTION get_skill_metadata(skill_dir):
  
  # Attempt to read SKILL.md for metadata
  skill_md_path = "{skill_dir}/SKILL.md"
  
  IF file_exists(skill_md_path):
    TRY:
      content = read_file(skill_md_path)
      frontmatter = parse_yaml_frontmatter(content)
      
      RETURN {
        created: frontmatter.created OR file_creation_time(skill_md_path),
        last_modified: file_modification_time(skill_md_path)
      }
    CATCH:
      # Fallback to filesystem timestamps
      RETURN {
        created: file_creation_time(skill_dir),
        last_modified: file_modification_time(skill_dir)
      }
  ELSE:
    # No SKILL.md - use directory timestamps
    RETURN {
      created: file_creation_time(skill_dir),
      last_modified: file_modification_time(skill_dir)
    }
```

**Note**: Timestamps are best-effort. Original creation time may be lost if SKILL.md doesn't have frontmatter.

---

## Backup Management

### Backup Naming

```markdown
FUNCTION create_backup(source_file):
  
  timestamp = get_timestamp()  # ISO 8601 format
  # Replace colons and timezone for filesystem compatibility
  timestamp_safe = timestamp.replace(":", "-").replace("+", "").replace("Z", "")
  
  backup_path = "{source_file}.backup.{timestamp_safe}"
  
  copy_file(source_file, backup_path)
  
  RETURN backup_path

EXAMPLE:
  Source: MEMORY.md
  Timestamp: 2026-02-04T16:30:00Z
  Backup: MEMORY.md.backup.2026-02-04T16-30-00Z
```

### Backup Retention

```markdown
RECOMMENDATION (not enforced by foundation):

- Keep last 5 backups
- Auto-delete backups older than 30 days
- User can manually delete backups

FUTURE ENHANCEMENT:

FUNCTION cleanup_old_backups(max_backups=5):
  backups = glob("MEMORY.md.backup.*")
  backups.sort(by=timestamp, desc=true)
  
  IF backups.length > max_backups:
    to_delete = backups[max_backups:]
    FOR EACH backup IN to_delete:
      delete_file(backup)
      LOG: "Deleted old backup: {backup}"
```

---

## Recovery Validation

### Post-Recovery Checks

```markdown
AFTER recovery completes:

1. Validate recovered MEMORY.md
   validation = validate_memory_md("MEMORY.md")
   IF NOT validation.valid:
     ABORT: "Recovery failed - generated invalid MEMORY.md"

2. Check CLI count
   IF detected_clis.length == 0:
     WARN: "No CLI directories found during recovery. Was Hefesto initialized?"

3. Check skill count
   LOG: "Recovered {skill_registry.length} skill(s)"

4. Verify filesystem consistency
   FOR EACH cli IN detected_clis:
     IF NOT directory_exists(cli.skills_directory_path):
       ERROR: "CLI directory disappeared during recovery: {cli.skills_directory_path}"
```

---

## Manual Recovery Command

### /hefesto.recover (Future Enhancement)

**Purpose**: Manually trigger MEMORY.md recovery

**Signature**:
```text
/hefesto.recover [--force] [--no-backup]

Options:
  --force      Force recovery even if MEMORY.md is valid
  --no-backup  Skip creating backup (dangerous)
```

**Workflow**:
```markdown
1. Check if recovery needed
   IF --force NOT provided:
     validation = validate_memory_md("MEMORY.md")
     IF validation.valid:
       DISPLAY: "MEMORY.md is valid. Use --force to force recovery."
       ABORT

2. Create backup (unless --no-backup)
   IF NOT --no-backup:
     backup_path = create_backup("MEMORY.md")
     DISPLAY: "Backup created: {backup_path}"

3. Run recovery
   recovery = recover_corrupted_memory()

4. Display results
   DISPLAY recovery report
```

---

## Error Handling

### Recovery Failure

```markdown
IF recovery fails (cannot rebuild valid state):
  
  DISPLAY:
    ❌ MEMORY.md recovery failed
    
    Backup preserved: MEMORY.md.backup.{timestamp}
    
    Possible causes:
    - No CLI directories found (Hefesto may not be initialized)
    - Filesystem permissions prevent directory scanning
    - Critical corruption in both MEMORY.md and filesystem
    
    **Action**:
    1. Review backup: MEMORY.md.backup.{timestamp}
    2. Manually fix MEMORY.md or delete and re-run: /hefesto.init
    3. Check filesystem permissions
  
  ABORT with exit code 1
```

### Partial Recovery

```markdown
IF recovery partial (some data lost):
  
  DISPLAY:
    ⚠️ Partial recovery successful
    
    Recovered:
    - {cli_count} CLI directories
    - {skill_count} skills
    
    Lost data:
    - Original initialization timestamp (using current time)
    - CLI version information (will be re-detected on next /hefesto.detect)
    - Exact skill creation timestamps (using filesystem times)
    
    **Action**: Review backup if original data needed
  
  CONTINUE with recovered state
```

---

## Testing Recovery

### Test Case 1: Corrupted YAML

```bash
# Setup
echo "---\ninvalid: yaml: syntax:\n---" | cat - <(tail -n +4 MEMORY.md) > MEMORY.md.tmp
mv MEMORY.md.tmp MEMORY.md

# Execute
/hefesto.list

# Expected Result
- Validation detects YAML corruption
- Backup created
- State rebuilt from filesystem
- New MEMORY.md generated
- List command proceeds successfully
```

### Test Case 2: Missing Tables

```bash
# Setup: Remove table sections
head -n 3 MEMORY.md > MEMORY.md.tmp
mv MEMORY.md.tmp MEMORY.md

# Execute
/hefesto.list

# Expected Result
- Validation detects missing tables
- Backup created
- Frontmatter preserved
- Tables rebuilt from filesystem
```

### Test Case 3: Recovery from Empty File

```bash
# Setup
echo "" > MEMORY.md

# Execute
/hefesto.list

# Expected Result
- Complete recovery triggered
- All data rebuilt from filesystem
- New timestamps generated
```

---

## Performance

| Operation | Target | Typical |
|-----------|--------|---------|
| Create backup | < 50ms | 20-30ms |
| Scan CLI directories | < 500ms | 200-400ms |
| Scan skill directories | < 200ms | 100-150ms |
| Generate new MEMORY.md | < 100ms | 50-80ms |
| Validate recovered file | < 50ms | 20-30ms |
| **Total Recovery** | **< 1s** | **400-700ms** |

---

## References

- **Validation**: helpers/memory-validator.md
- **Template**: templates/memory-template.md
- **Data Model**: data-model.md (Project State)
- **Error Handling**: error-handling.md (ERR-002)
- **Platform**: helpers/platform-detection.md (filesystem operations)
- **Requirements**: FR-016 (corrupted MEMORY.md recovery)
- **Edge Case**: Clarification #1 (backup with timestamp, rebuild from filesystem)
