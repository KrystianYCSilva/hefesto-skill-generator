---
description: "Delete skill from filesystem with Human Gate confirmation (destructive)"
command: "/hefesto.delete"
category: "skill-management"
user_story: "US4"
priority: "P2"
version: "1.0.0"
---

# /hefesto.delete - Delete Skill Command

**Command**: `/hefesto.delete`  
**Purpose**: Delete skill with Human Gate confirmation (destructive)  
**User Story**: US4 - Management & Help (P2)

---

## Overview

The `/hefesto.delete` command safely removes skills from the filesystem with mandatory confirmation. Features:

1. **Human Gate**: Requires explicit confirmation by typing skill name (T0-HEFESTO-02)
2. **Backup**: Auto-create backup before deletion (default)
3. **Multi-CLI**: Delete from specific CLI or all CLIs
4. **Safe**: Rollback on partial failure
5. **Audit Trail**: Log deletions in MEMORY.md

**Target Performance**: < 2s (excluding Human Gate wait)

---

## Command Signature

```text
/hefesto.delete <skill_name> [--cli <name>] [--force] [--backup]

Arguments:
  skill_name      Name of skill to delete (required)

Options:
  --cli <name>    Delete from specific CLI only (default: all)
  --force         Skip Human Gate (DANGEROUS - requires explicit confirmation)
  --backup        Create backup before deletion (default: true)
```

---

## Execution Workflow

### Phase 0: Pre-Execution Validation

```markdown
1. Validate CONSTITUTION
   (see: helpers/constitution-validator.md)
   IF invalid → ABORT

2. Check Hefesto initialization
   IF NOT file_exists("MEMORY.md"):
     DISPLAY: "❌ Hefesto not initialized. Run /hefesto.init first."
     ABORT (exit code 1)

3. Parse arguments
   skill_name = args.positional[0] OR null
   
   IF skill_name IS null:
     ERROR: "Missing required argument: skill_name"
     SUGGEST: "Usage: /hefesto.delete <skill_name>"
     ABORT
   
   cli_filter = args.flags.get("cli") OR null
   force = args.flags.has("force")
   create_backup = args.flags.get("backup", default=true)
```

**Performance Target**: < 100ms

---

### Phase 1: Skill Discovery

```markdown
1. Find skill locations
   detected_clis = read_memory_md().detected_clis
   found_locations = []
   
   IF cli_filter IS provided:
     skill_path = ".{cli_filter}/skills/{skill_name}/"
     IF directory_exists(skill_path):
       found_locations.append({
         cli: cli_filter,
         path: skill_path
       })
   
   ELSE:
     # Search in all CLIs
     FOR EACH cli IN detected_clis:
       skill_path = ".{cli}/skills/{skill_name}/"
       IF directory_exists(skill_path):
         found_locations.append({
           cli: cli,
           path: skill_path
         })

2. Handle not found
   IF found_locations IS empty:
     ERROR E-DELETE-001: "Skill not found: {skill_name}"
     
     # List available skills
     available = list_all_skills()
     IF available NOT empty:
       DISPLAY: "Available skills:"
       FOR EACH skill IN available[:10]:  # Show max 10
         DISPLAY: "  - {skill.name}"
     
     ABORT (exit code 1)

3. Gather deletion info
   total_size = 0
   total_files = 0
   file_list = []
   
   FOR EACH location IN found_locations:
     files = list_all_files_recursive(location.path)
     size = sum(file_sizes(files))
     
     total_files += count(files)
     total_size += size
     file_list.extend(files)
```

**Performance Target**: < 100ms

---

### Phase 2: Backup Creation

```markdown
1. Check backup flag
   IF create_backup == false:
     WARN: "⚠️  Backup disabled - deletion will be permanent"

2. Create backup if enabled
   IF create_backup:
     backup_name = "{skill_name}-{timestamp}.tar.gz"
     backup_dir = ".hefesto/backups/"
     backup_path = "{backup_dir}/{backup_name}"
     
     # Create backup directory if needed
     IF NOT directory_exists(backup_dir):
       create_directory(backup_dir)
     
     # Create tarball
     TRY:
       FOR EACH location IN found_locations:
         add_to_tarball(backup_path, location.path, prefix=location.cli)
     
     CATCH IOError:
       ERROR E-DELETE-003: "Backup creation failed"
       DISPLAY: "Cannot proceed without backup"
       ABORT
     
     backup_info = {
       path: backup_path,
       size: get_file_size_kb(backup_path)
     }
     
     DISPLAY: "✅ Backup created: {backup_path} ({backup_info.size} KB)"
```

**Performance Target**: < 1s  
**References**: T0-HEFESTO-08

---

### Phase 3: Human Gate

```markdown
1. Check force flag warning
   IF force:
     WARN: "⚠️  Force flag enabled"
     WARN: "Human Gate will still require typing skill name"

2. Display confirmation prompt
   (see: helpers/human-gate.md)
   
   DISPLAY:
   ═══════════════════════════════════════════════════
   ⚠️  WARNING: DESTRUCTIVE OPERATION
   ═══════════════════════════════════════════════════
   Skill: {skill_name}
   
   Locations:
     {FOR EACH location IN found_locations}
     - .{location.cli}/skills/{skill_name}/
   
   Files to delete:
     {FOR EACH file IN file_list[:10]}  # Show first 10
     - {relative_path(file)}
     {IF count(file_list) > 10}
     ... and {count(file_list) - 10} more files
   
   Total: {total_files} files, {format_size(total_size)}
   
   {IF create_backup}
   Backup created at:
     {backup_path}
   {ELSE}
   ⚠️  NO BACKUP - Deletion is permanent!
   {ENDIF}
   
   ═══════════════════════════════════════════════════
   
   This action CANNOT be undone without backup.
   
   To confirm deletion, type the skill name: _

3. Prompt for confirmation
   PROMPT: skill_name_input
   
   IF skill_name_input != skill_name:
     ERROR E-DELETE-004: "Skill name mismatch"
     DISPLAY: "Deletion cancelled. No changes made."
     ABORT
   
   DISPLAY: ""
   DISPLAY: "Final confirmation: DELETE {skill_name}? [yes/NO]"
   PROMPT: final_confirm
   
   IF final_confirm.lower() NOT IN ["yes", "y"]:
     DISPLAY: "Deletion cancelled. No changes made."
     ABORT

4. Timeout
   IF no_response_after(120_seconds):
     DISPLAY: "Operation timed out. No changes made."
     ABORT
```

**References**: T0-HEFESTO-02, FR-002

---

### Phase 4: Deletion

```markdown
1. Initialize deletion tracking
   deleted_locations = []
   failed_locations = []

2. Delete each location
   FOR EACH location IN found_locations:
     TRY:
       # Check write permissions first
       IF NOT has_write_permission(location.path):
         ERROR E-DELETE-002: "Write permission denied: {location.path}"
         failed_locations.append({
           location: location,
           error: "Permission denied"
         })
         CONTINUE
       
       # Perform deletion
       delete_directory_recursive(location.path)
       deleted_locations.append(location)
       
       DISPLAY: "✅ Deleted: .{location.cli}/skills/{skill_name}/"
     
     CATCH Exception as e:
       failed_locations.append({
         location: location,
         error: str(e)
       })
       DISPLAY: "❌ Failed: .{location.cli}/skills/{skill_name}/ - {e}"

3. Handle partial failure
   IF failed_locations NOT empty AND deleted_locations NOT empty:
     ERROR E-DELETE-005: "Partial deletion occurred"
     
     DISPLAY: ""
     DISPLAY: "⚠️  WARNING: Partial deletion"
     DISPLAY: "Deleted from: {list(deleted_locations)}"
     DISPLAY: "Failed: {list(failed_locations)}"
     
     IF create_backup:
       DISPLAY: ""
       DISPLAY: "Restore from backup:"
       DISPLAY: "  tar -xzf {backup_path} -C ."
     
     # Do NOT rollback - some deletions succeeded
     # User can restore from backup if needed

4. Handle total failure
   IF count(deleted_locations) == 0:
     ERROR: "All deletions failed"
     
     FOR EACH failed IN failed_locations:
       DISPLAY: "❌ {failed.location.cli}: {failed.error}"
     
     ABORT (exit code 1)
```

**Performance Target**: < 500ms  
**References**: T0-HEFESTO-08

---

### Phase 5: State Update

```markdown
1. Update MEMORY.md
   state = read_memory_md()
   
   # Initialize deleted skills log if needed
   IF NOT state.has("skills_deleted"):
     state.skills_deleted = []
   
   # Log deletion
   state.skills_deleted.append({
     name: skill_name,
     deleted: current_timestamp(),
     backup: backup_path IF create_backup ELSE null,
     clis: [loc.cli FOR loc IN deleted_locations]
   })
   
   # Remove from active skills registry
   state.skills_created = [
     s FOR s IN state.skills_created 
     IF s.name != skill_name
   ]
   
   TRY:
     write_memory_md(state)
   CATCH IOError:
     WARN E-DELETE-006: "MEMORY.md update failed"
     DISPLAY: "Deletion completed but state not updated"
     # Continue - deletion already succeeded

2. Success message
   DISPLAY: ""
   DISPLAY: "═══════════════════════════════════════════════════"
   DISPLAY: "Deletion Complete"
   DISPLAY: "═══════════════════════════════════════════════════"
   DISPLAY: "Skill: {skill_name}"
   DISPLAY: "Deleted from: {count(deleted_locations)} CLI(s)"
   FOR EACH location IN deleted_locations:
     DISPLAY: "  ✅ {location.cli}"
   
   IF create_backup:
     DISPLAY: ""
     DISPLAY: "Backup: {backup_path}"
     DISPLAY: ""
     DISPLAY: "To restore:"
     DISPLAY: "  tar -xzf {backup_path} -C ."
   
   DISPLAY: "═══════════════════════════════════════════════════"
   
   EXIT 0
```

**Performance Target**: < 500ms

---

## Error Cases

| Code | Condition | Handler |
|------|-----------|---------|
| **E-DELETE-001** | Skill not found | Error + list available |
| **E-DELETE-002** | Write permission denied | Error + path details |
| **E-DELETE-003** | Backup creation fails | Block deletion + error |
| **E-DELETE-004** | User cancels Human Gate | Info + exit gracefully |
| **E-DELETE-005** | Partial deletion | Warning + backup info |
| **E-DELETE-006** | MEMORY.md update fails | Complete deletion but warn |

---

## Usage Examples

### Example 1: Basic Deletion

```bash
> /hefesto.delete email-validator

Found email-validator in:
  - .claude/skills/email-validator/
  - .gemini/skills/email-validator/

✅ Backup created: .hefesto/backups/email-validator-20260204-103000.tar.gz (12 KB)

═══════════════════════════════════════════════════
⚠️  WARNING: DESTRUCTIVE OPERATION
═══════════════════════════════════════════════════
Skill: email-validator

Locations:
  - .claude/skills/email-validator/
  - .gemini/skills/email-validator/

Files to delete:
  - SKILL.md
  - metadata.yaml
  - scripts/validator.py

Total: 3 files, 12 KB

Backup created at:
  .hefesto/backups/email-validator-20260204-103000.tar.gz

═══════════════════════════════════════════════════

This action CANNOT be undone without backup.

To confirm deletion, type the skill name: email-validator

Final confirmation: DELETE email-validator? [yes/NO] yes

✅ Deleted: .claude/skills/email-validator/
✅ Deleted: .gemini/skills/email-validator/

═══════════════════════════════════════════════════
Deletion Complete
═══════════════════════════════════════════════════
Skill: email-validator
Deleted from: 2 CLI(s)
  ✅ claude
  ✅ gemini

Backup: .hefesto/backups/email-validator-20260204-103000.tar.gz

To restore:
  tar -xzf .hefesto/backups/email-validator-20260204-103000.tar.gz -C .

═══════════════════════════════════════════════════
```

### Example 2: Specific CLI

```bash
> /hefesto.delete testing-strategy --cli gemini

Found testing-strategy in:
  - .gemini/skills/testing-strategy/

[... proceeds with single CLI deletion ...]
```

### Example 3: No Backup (Dangerous)

```bash
> /hefesto.delete temp-skill --backup=false

⚠️  Backup disabled - deletion will be permanent

═══════════════════════════════════════════════════
⚠️  WARNING: DESTRUCTIVE OPERATION
═══════════════════════════════════════════════════

[... no backup section ...]

⚠️  NO BACKUP - Deletion is permanent!

[... requires confirmation ...]
```

### Example 4: Cancelled

```bash
> /hefesto.delete important-skill

[... shows confirmation ...]

To confirm deletion, type the skill name: no-wait-cancel

❌ ERROR [E-DELETE-004]: Skill name mismatch

Deletion cancelled. No changes made.
```

### Example 5: Permission Error

```bash
> /hefesto.delete protected-skill

[... shows confirmation ...]

To confirm deletion, type the skill name: protected-skill

Final confirmation: DELETE protected-skill? [yes/NO] yes

❌ ERROR [E-DELETE-002]: Write permission denied: .claude/skills/protected-skill/

Suggestion: Check permissions
Usage: /hefesto.delete <skill_name>
```

---

## Human Gate Specification

### Confirmation Requirements

**Level 1 (Type skill name):**
```
To confirm deletion, type the skill name: _
```
User must type exact skill name (case-sensitive).

**Level 2 (Yes/No):**
```
Final confirmation: DELETE {skill_name}? [yes/NO]
```
User must type "yes" or "y" (case-insensitive).

### Timeout

- **120 seconds** of no response triggers automatic cancellation
- All partial state is discarded
- No filesystem changes made

---

## Success Criteria

- ✅ **SC-001**: Command implemented
- ✅ **SC-003**: Human Gate enforced 100%
- ✅ **US-004 Scenario 2**: Deletion with confirmation
- ✅ **FR-002**: Human Gate requirement
- ✅ **T0-HEFESTO-02**: Human Gate protocol

---

## Performance Targets

| Operation | Target | Typical |
|-----------|--------|---------|
| Discovery | < 100ms | 50ms |
| Backup creation | < 1s | 500ms |
| Human Gate wait | unbounded | N/A |
| Deletion | < 500ms | 200ms |
| State update | < 500ms | 200ms |
| **Total (excl. Human Gate)** | **< 2s** | **~1s** |

---

## Dependencies

**Required Helpers:**
- `helpers/human-gate.md` - Destructive operation confirmation
- `helpers/cli-detector.md` - Skill locations

**State Files:**
- `MEMORY.md` - Skill registry and deletion log

---

## See Also

- **Related Commands**: `/hefesto.show`, `/hefesto.list`, `/hefesto.create`
- **Specification**: `specs/003-hefesto-commands/contracts/delete.contract.md`
- **T0 Rules**: `CONSTITUTION.md` (T0-HEFESTO-02, 08)
- **User Story**: `specs/003-hefesto-commands/spec.md` US4
