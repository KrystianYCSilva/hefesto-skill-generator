---
description: "Detect and report inconsistencies between MEMORY.md state and filesystem to ensure data integrity"
category: "helper"
type: "synchronization"
used_by: ["/hefesto.list --check-sync", "/hefesto.sync (future)"]
validates: "filesystem consistency"
version: "1.0.0"
---

# Filesystem State Synchronization

**Purpose**: Detect and report inconsistencies between MEMORY.md and filesystem  
**Used by**: `/hefesto.list --check-sync`, potentially `/hefesto.sync` (future)

---

## Overview

State synchronization ensures that MEMORY.md accurately reflects the actual filesystem state. Over time, inconsistencies can occur due to:

- Manual file deletion (skills removed without updating MEMORY.md)
- Manual file addition (skills copied from elsewhere)
- External tools modifying skill directories
- Failed operations (partial success, MEMORY.md not updated)

---

## Synchronization Check Workflow

```markdown
FUNCTION check_filesystem_sync():
  
  1. Parse current state from MEMORY.md
     state = parse_memory_md("MEMORY.md")
     tracked_clis = state.detected_clis
     tracked_skills = state.skill_registry
  
  2. Scan filesystem
     filesystem_clis = scan_cli_directories()
     filesystem_skills = scan_skill_directories()
  
  3. Compare and identify inconsistencies
     inconsistencies = {
       orphaned_clis: [],      # In filesystem, not in MEMORY.md
       missing_clis: [],        # In MEMORY.md, not in filesystem
       orphaned_skills: [],     # In filesystem, not in MEMORY.md
       missing_skills: [],      # In MEMORY.md, not in filesystem
       version_mismatches: []   # CLI version changed
     }
     
     # CLI-level check
     FOR EACH fs_cli IN filesystem_clis:
       IF fs_cli.id NOT IN [cli.id FOR cli IN tracked_clis]:
         inconsistencies.orphaned_clis.append(fs_cli)
     
     FOR EACH tracked_cli IN tracked_clis:
       IF tracked_cli.id NOT IN [cli.id FOR cli IN filesystem_clis]:
         inconsistencies.missing_clis.append(tracked_cli)
       ELSE:
         # Check version mismatch
         fs_cli = filesystem_clis.find(c => c.id == tracked_cli.id)
         IF fs_cli.version != tracked_cli.version:
           inconsistencies.version_mismatches.append({
             cli: tracked_cli.id,
             tracked_version: tracked_cli.version,
             filesystem_version: fs_cli.version
           })
     
     # Skill-level check
     FOR EACH fs_skill IN filesystem_skills:
       tracked_skill = tracked_skills.find(s => s.name == fs_skill.name)
       IF NOT tracked_skill:
         inconsistencies.orphaned_skills.append(fs_skill)
       ELSE:
         # Check if skill exists in all tracked CLIs
         FOR EACH cli IN tracked_skill.clis:
           cli_skill_path = ".{cli}/skills/{fs_skill.name}/"
           IF NOT directory_exists(cli_skill_path):
             inconsistencies.missing_skills.append({
               skill: fs_skill.name,
               cli: cli,
               expected_path: cli_skill_path
             })
     
     FOR EACH tracked_skill IN tracked_skills:
       # Check if skill exists in filesystem for any tracked CLI
       found_in_any_cli = false
       FOR EACH cli IN tracked_skill.clis:
         cli_skill_path = ".{cli}/skills/{tracked_skill.name}/"
         IF directory_exists(cli_skill_path):
           found_in_any_cli = true
           BREAK
       
       IF NOT found_in_any_cli:
         inconsistencies.missing_skills.append({
           skill: tracked_skill.name,
           clis: tracked_skill.clis,
           reason: "not found in any tracked CLI directory"
         })
  
  4. Return sync report
     RETURN {
       synchronized: inconsistencies.is_empty(),
       inconsistencies: inconsistencies
     }
```

---

## Inconsistency Types

### 1. Orphaned CLI Directory

**Definition**: CLI directory exists in filesystem but not tracked in MEMORY.md

**Example**:
```text
Filesystem: .cursor/skills/ exists
MEMORY.md: No entry for "cursor" CLI
```

**Cause**:
- Manual directory creation
- Partial /hefesto.init failure
- MEMORY.md corruption recovery missed the CLI

**Recommended Action**: Add to MEMORY.md (run `/hefesto.detect`)

---

### 2. Missing CLI Directory

**Definition**: CLI tracked in MEMORY.md but directory doesn't exist in filesystem

**Example**:
```text
MEMORY.md: "cursor" CLI with .cursor/skills/
Filesystem: .cursor/skills/ does not exist
```

**Cause**:
- Manual directory deletion
- Filesystem permissions changed
- External tool removed directory

**Recommended Action**: Remove from MEMORY.md or recreate directory

---

### 3. Orphaned Skill

**Definition**: Skill directory exists in filesystem but not tracked in MEMORY.md

**Example**:
```text
Filesystem: .claude/skills/legacy-formatter/ exists
MEMORY.md: No "legacy-formatter" entry in skill registry
```

**Cause**:
- Manual skill directory creation
- Skill copied from another project
- MEMORY.md corruption recovery missed the skill

**Recommended Action**: Add to skill registry (or delete if unwanted)

---

### 4. Missing Skill

**Definition**: Skill tracked in MEMORY.md but directory doesn't exist in filesystem

**Example**:
```text
MEMORY.md: "api-docs" skill for CLIs [claude, cursor]
Filesystem: .cursor/skills/api-docs/ does not exist
```

**Cause**:
- Manual deletion
- Failed skill generation
- Filesystem sync issue

**Recommended Action**: Remove from registry or regenerate skill

---

### 5. Version Mismatch

**Definition**: CLI version in MEMORY.md doesn't match current detected version

**Example**:
```text
MEMORY.md: claude version 1.1.0
Filesystem: claude --version returns 1.2.0
```

**Cause**:
- CLI upgraded after detection
- MEMORY.md not updated after upgrade

**Recommended Action**: Update MEMORY.md version (run `/hefesto.detect --force`)

---

## Sync Report Format

### Report Structure

```markdown
## Filesystem Synchronization Report

**Status**: {Synchronized | Inconsistencies Detected}
**Checked**: {timestamp}
**CLIs Checked**: {count}
**Skills Checked**: {count}

---

{IF synchronized}
✅ Filesystem fully synchronized with MEMORY.md

All CLI directories match tracked state
All skills exist in expected locations
{ELSE}

### Inconsistencies ({count})

{IF orphaned_clis.length > 0}
#### Orphaned CLI Directories ({count})

CLI directories found in filesystem but not tracked:

- **.{cli.id}/skills/** ({cli.display_name})
  - Detected: {cli.detection_method}
  - Version: {cli.version}
  - **Action**: Run `/hefesto.detect` to add to tracking
{END FOR}
{END IF}

{IF missing_clis.length > 0}
#### Missing CLI Directories ({count})

CLI directories tracked but not found in filesystem:

- **.{cli.id}/skills/** ({cli.display_name})
  - Last known version: {cli.version}
  - **Action**: Delete from MEMORY.md or recreate directory
{END FOR}
{END IF}

{IF orphaned_skills.length > 0}
#### Orphaned Skills ({count})

Skills found in filesystem but not tracked:

- **{skill.name}** (in .{cli}/skills/)
  - Last Modified: {skill.last_modified}
  - **Action**: Add to registry or delete if unwanted
{END FOR}
{END IF}

{IF missing_skills.length > 0}
#### Missing Skills ({count})

Skills tracked but not found in expected locations:

- **{skill.name}** (expected in .{cli}/skills/)
  - Tracked for CLIs: {skill.clis.join(", ")}
  - **Action**: Remove from registry or regenerate skill
{END FOR}
{END IF}

{IF version_mismatches.length > 0}
#### Version Mismatches ({count})

CLI versions changed since last detection:

- **{cli.display_name}**
  - Tracked: v{mismatch.tracked_version}
  - Current: v{mismatch.filesystem_version}
  - **Action**: Run `/hefesto.detect --force` to update
{END FOR}
{END IF}

---

### Recommended Actions

1. Run `/hefesto.detect` to add new CLIs and update versions
2. Review orphaned skills and decide: keep (add to registry) or delete
3. For missing skills: regenerate with `/hefesto.create` or remove from registry
4. For missing CLI directories: recreate or remove from tracking

{END IF}
```

---

## Usage Examples

### Example 1: Fully Synchronized

```text
> /hefesto.list --check-sync

...

## Filesystem Synchronization Report

**Status**: Synchronized
**Checked**: 2026-02-04 16:30:00 UTC
**CLIs Checked**: 4
**Skills Checked**: 5

---

✅ Filesystem fully synchronized with MEMORY.md

All CLI directories match tracked state
All skills exist in expected locations
```

### Example 2: Orphaned Skill

```text
> /hefesto.list --check-sync

...

## Filesystem Synchronization Report

**Status**: Inconsistencies Detected
**Checked**: 2026-02-04 16:30:00 UTC
**CLIs Checked**: 4
**Skills Checked**: 6 (5 tracked, 1 untracked)

---

### Inconsistencies (1)

#### Orphaned Skills (1)

Skills found in filesystem but not tracked:

- **legacy-formatter** (in .claude/skills/)
  - Last Modified: 2026-01-15 10:00:00 UTC
  - **Action**: Add to registry or delete if unwanted

---

### Recommended Actions

1. To track: Manually add skill to MEMORY.md or regenerate
2. To remove: `rm -rf .claude/skills/legacy-formatter`
```

### Example 3: Multiple Inconsistencies

```text
> /hefesto.list --check-sync

...

## Filesystem Synchronization Report

**Status**: Inconsistencies Detected
**Checked**: 2026-02-04 16:30:00 UTC
**CLIs Checked**: 5 (4 tracked, 1 untracked)
**Skills Checked**: 6 (5 tracked, 1 missing)

---

### Inconsistencies (3)

#### Orphaned CLI Directories (1)

CLI directories found in filesystem but not tracked:

- **.cursor/skills/** (Cursor)
  - Detected: PATH
  - Version: 1.0.5
  - **Action**: Run `/hefesto.detect` to add to tracking

#### Missing Skills (1)

Skills tracked but not found in expected locations:

- **api-docs** (expected in .cursor/skills/)
  - Tracked for CLIs: claude, cursor
  - **Action**: Remove from registry or regenerate skill

#### Version Mismatches (1)

CLI versions changed since last detection:

- **Claude Code**
  - Tracked: v1.1.0
  - Current: v1.2.0
  - **Action**: Run `/hefesto.detect --force` to update

---

### Recommended Actions

1. Run `/hefesto.detect` to add Cursor and update Claude Code version
2. For api-docs: Check if it exists in .claude/skills/ and regenerate for Cursor
3. Review and clean up any inconsistencies
```

---

## Automatic Sync Check

### When to Run

```markdown
AUTOMATIC sync check triggered:

1. On /hefesto.list --check-sync (explicit)
2. On /hefesto.init (verify initial state)
3. After MEMORY.md recovery (validate rebuilt state)
4. Periodically on long-running sessions (future)

MANUAL sync check:
- User runs `/hefesto.list --check-sync` explicitly
```

### Performance Considerations

```markdown
Sync check is OPTIONAL by default for performance:

- /hefesto.list (default): No sync check (fast, < 100ms)
- /hefesto.list --check-sync: Full sync check (slower, < 200ms)

RATIONALE:
- Most operations don't need sync verification
- Sync check requires filesystem scanning (I/O intensive)
- User can explicitly request when needed
```

---

## Future: /hefesto.sync Command

### Automatic Synchronization (Future Enhancement)

```text
/hefesto.sync [--auto-fix] [--interactive]

Purpose: Fix filesystem inconsistencies automatically

Options:
  --auto-fix      Automatically resolve inconsistencies (dangerous)
  --interactive   Prompt for each inconsistency (safe)
```

**Workflow**:
```markdown
1. Run sync check
   sync_report = check_filesystem_sync()

2. Present inconsistencies to user
   IF --interactive:
     FOR EACH inconsistency:
       PROMPT user: "Fix this inconsistency? [y/n]"
       IF yes: apply_fix(inconsistency)
   ELIF --auto-fix:
     FOR EACH inconsistency:
       apply_fix(inconsistency)
   ELSE:
     DISPLAY sync_report
     DISPLAY: "Use --auto-fix or --interactive to resolve"

3. Update MEMORY.md with fixes
   write_memory_md(updated_state)

4. Display results
   DISPLAY: "Fixed {count} inconsistencies"
```

**Auto-fix Strategy**:
- Orphaned CLIs → Add to MEMORY.md
- Missing CLIs → Remove from MEMORY.md (if directory gone)
- Orphaned skills → Add to skill registry
- Missing skills → Remove from skill registry
- Version mismatches → Update to current version

---

## Testing

### Test Case 1: Orphaned Skill

```bash
# Setup: Manually create skill directory
mkdir -p .claude/skills/test-skill
echo "# Test Skill" > .claude/skills/test-skill/SKILL.md

# Execute
/hefesto.list --check-sync

# Expected Result
- Detects orphaned skill "test-skill"
- Reports in inconsistencies section
- Suggests action (add to registry or delete)
```

### Test Case 2: Missing Skill

```bash
# Setup: Delete skill directory but keep in MEMORY.md
rm -rf .cursor/skills/api-docs

# Execute
/hefesto.list --check-sync

# Expected Result
- Detects missing skill "api-docs" for cursor CLI
- Reports in inconsistencies section
- Suggests regeneration or removal from registry
```

### Test Case 3: Version Mismatch

```bash
# Setup: Upgrade CLI (simulate by editing MEMORY.md)
sed -i 's/claude.*1.1.0/claude | 1.2.0/' MEMORY.md
# Then actually upgrade claude CLI

# Execute
/hefesto.list --check-sync

# Expected Result
- Detects version mismatch
- Reports tracked vs. current version
- Suggests running /hefesto.detect --force
```

---

## Performance

| Operation | Target | Typical |
|-----------|--------|---------|
| Scan filesystem CLIs | < 500ms | 200-400ms |
| Scan filesystem skills | < 200ms | 100-150ms |
| Compare state | < 50ms | 20-30ms |
| Generate report | < 50ms | 20-30ms |
| **Total Sync Check** | **< 800ms** | **350-600ms** |

---

## References

- **Validator**: helpers/memory-validator.md
- **Recovery**: helpers/memory-recovery.md
- **Data Model**: data-model.md (filesystem synchronization)
- **Requirements**: FR-038 (filesystem synchronization check)
- **Command**: hefesto.list.md (--check-sync option)
