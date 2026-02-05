---
description: "Synchronize existing skills with latest templates and update outdated structures"
command: "/hefesto.sync"
category: "skill-management"
user_story: "US3"
priority: "P2"
version: "1.0.0"
---

# /hefesto.sync - Sync Skills Command

**Command**: `/hefesto.sync`  
**Purpose**: Synchronize skills with latest templates  
**User Story**: US3 - Adaptation & Sync (P2)

---

## Overview

The `/hefesto.sync` command updates existing skills to match latest template versions while preserving user modifications. Features:

1. **Version Detection**: Compare skill vs template versions
2. **Batch Processing**: Sync all outdated skills at once
3. **Merge Strategy**: Preserve custom content, update structure
4. **Human Gate**: Review changes before applying (T0-HEFESTO-02)
5. **Backup**: Auto-backup before modifications
6. **Dry Run**: Preview changes without applying

**Target Performance**: < 5s for 10 skills (excluding Human Gate)

---

## Command Signature

```text
/hefesto.sync [skill_name] [--cli <name>] [--dry-run] [--template-version <version>]

Arguments:
  skill_name              Specific skill to sync (optional)
                          If missing: Sync ALL skills

Options:
  --cli <name>            Sync only in specific CLI directory
  --dry-run               Show changes without applying
  --template-version <v>  Target specific template version (default: latest)
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

3. Load templates with version info
   templates = load_templates_with_versions()
   IF templates IS empty:
     ERROR: "Template system not available"
     ABORT
```

**Performance Target**: < 500ms

---

### Phase 1: Discovery & Analysis

```markdown
1. Determine scope
   IF skill_name IS provided:
     skills_to_check = [find_skill(skill_name, cli_filter)]
     IF NOT found:
       ERROR E-SYNC-001: "Skill not found: {skill_name}"
       ABORT
   ELSE:
     skills_to_check = discover_all_skills(cli_filter)
     IF skills_to_check IS empty:
       INFO: "No skills found to sync"
       EXIT 0

2. Check each skill for updates
   outdated_skills = []
   
   FOR EACH skill IN skills_to_check:
     # Read skill metadata
     metadata_path = dirname(skill.path) + "/metadata.yaml"
     TRY:
       metadata = read_yaml(metadata_path)
       skill_version = metadata.template_version OR "0.0.0"
     CATCH:
       skill_version = "0.0.0"  # Assume very old
     
     # Get template version
     template = get_template_for_skill(skill)
     template_version = template.version
     
     # Compare versions
     IF version_compare(skill_version, template_version) < 0:
       diff = calculate_structural_diff(skill, template)
       outdated_skills.append({
         skill: skill,
         current_version: skill_version,
         target_version: template_version,
         diff: diff
       })

3. Display findings
   IF outdated_skills IS empty:
     DISPLAY: "✅ All skills are up to date"
     EXIT 0
   
   DISPLAY: "Found {count(outdated_skills)} skill(s) to update:"
   FOR EACH outdated IN outdated_skills:
     DISPLAY: "  - {outdated.skill.name}: v{outdated.current_version} → v{outdated.target_version}"
     IF verbose:
       DISPLAY: "    Changes: {summarize(outdated.diff)}"
```

**Performance Target**: < 1s for 10 skills  
**References**: FR-009

---

### Phase 2: Backup Creation

```markdown
1. Create backup directory
   backup_dir = ".hefesto/backups/sync-{timestamp}/"
   create_directory(backup_dir)

2. Backup each skill
   FOR EACH outdated IN outdated_skills:
     skill_dir = dirname(outdated.skill.path)
     backup_name = "{outdated.skill.name}-{outdated.skill.cli}.tar.gz"
     backup_path = "{backup_dir}/{backup_name}"
     
     TRY:
       create_tarball(skill_dir, backup_path)
     CATCH IOError:
       ERROR E-SYNC-006: "Backup creation failed"
       DISPLAY: "Cannot proceed without backup"
       ABORT
   
   DISPLAY: "✅ Backups created: {backup_dir}"
```

**Performance Target**: < 2s for 10 skills  
**References**: T0-HEFESTO-08

---

### Phase 3: Merge Strategy Planning

```markdown
1. Analyze user modifications
   (see: helpers/skill-merger.md)
   
   FOR EACH outdated IN outdated_skills:
     # Identify custom sections
     custom_sections = identify_custom_content(outdated.skill, template)
     
     # Identify structural changes
     structural_changes = outdated.diff.structural
     
     # Detect conflicts
     conflicts = detect_merge_conflicts(custom_sections, structural_changes)
     
     IF conflicts NOT empty:
       outdated.merge_strategy = "manual"
       outdated.conflicts = conflicts
     ELSE:
       outdated.merge_strategy = "auto"

2. Display merge plan
   DISPLAY: ""
   DISPLAY: "Merge Strategy:"
   DISPLAY: "═══════════════════════════════════════════════════"
   
   auto_merge = count(outdated WHERE merge_strategy == "auto")
   manual_review = count(outdated WHERE merge_strategy == "manual")
   
   DISPLAY: "Auto-merge: {auto_merge} skills"
   DISPLAY: "Manual review: {manual_review} skills"
   DISPLAY: ""
   
   IF manual_review > 0:
     DISPLAY: "Skills requiring manual review:"
     FOR EACH skill IN outdated WHERE merge_strategy == "manual":
       DISPLAY: "  - {skill.name}: {count(skill.conflicts)} conflict(s)"
```

**References**: FR-009

---

### Phase 4: Dry Run or Human Gate

```markdown
1. Check dry-run flag
   IF args.has_flag("--dry-run"):
     DISPLAY: ""
     DISPLAY: "DRY RUN - No changes will be applied"
     DISPLAY: "═══════════════════════════════════════════════════"
     
     FOR EACH outdated IN outdated_skills:
       DISPLAY: ""
       DISPLAY: "Skill: {outdated.skill.name}"
       DISPLAY: "Changes:"
       FOR EACH change IN outdated.diff:
         DISPLAY: "  + {change.description}"
     
     DISPLAY: ""
     DISPLAY: "To apply changes, run without --dry-run"
     EXIT 0

2. Human Gate
   (see: helpers/human-gate.md)
   
   DISPLAY:
   ═══════════════════════════════════════════════════
   🔄 Sync {count(outdated_skills)} Skill(s)?
   ═══════════════════════════════════════════════════
   
   Skills to update:
   {FOR EACH outdated IN outdated_skills}
   - {outdated.skill.name}: v{outdated.current_version} → v{outdated.target_version}
     {IF merge_strategy == "manual"}⚠️  Manual review required{ENDIF}
     Changes:
       {FOR EACH change IN outdated.diff.summary}
       • {change}
   
   Backups created: {backup_dir}
   
   ═══════════════════════════════════════════════════

3. Prompt for action
   IF any(outdated WHERE merge_strategy == "manual"):
     PROMPT: "Actions: [approve all] [review each] [cancel]"
   ELSE:
     PROMPT: "Actions: [approve all] [cancel]"
   
   INPUT: action
   
   CASE action:
     "approve all":
       PROCEED to Phase 5 (apply to all)
     
     "review each":
       FOR EACH outdated IN outdated_skills:
         display_detailed_preview(outdated)
         PROMPT: "[approve] [skip] [edit] [cancel all]"
         INPUT: skill_action
         
         CASE skill_action:
           "approve" → Mark for sync
           "skip" → Skip this skill
           "edit" → Allow manual edits
           "cancel all" → ABORT entire operation
       
       PROCEED to Phase 5 (apply to marked skills)
     
     "cancel":
       DISPLAY: "Operation cancelled. No changes made."
       ABORT
     
     timeout (300s):
       ABORT "Operation timed out"
```

**References**: T0-HEFESTO-02, FR-002

---

### Phase 5: Apply Updates

```markdown
1. Apply sync to each approved skill
   synced_count = 0
   failed_count = 0
   
   FOR EACH outdated IN outdated_skills WHERE approved:
     TRY:
       IF outdated.merge_strategy == "auto":
         result = auto_merge_skill(outdated)
       ELSE:
         result = manual_merge_skill(outdated)
       
       IF result.success:
         synced_count += 1
       ELSE:
         failed_count += 1
         DISPLAY: "❌ Failed: {outdated.skill.name} - {result.error}"
     
     CATCH Exception as e:
       failed_count += 1
       DISPLAY: "❌ Error syncing {outdated.skill.name}: {e}"

2. Auto-merge process
   auto_merge_skill(outdated):
     # Load template
     new_template = load_template(outdated.target_version)
     
     # Preserve user content
     preserved = extract_custom_sections(outdated.skill.content)
     
     # Apply new structure
     merged_content = new_template.copy()
     FOR EACH section IN preserved:
       inject_section(merged_content, section)
     
     # Update metadata
     metadata = read_yaml(outdated.skill.metadata_path)
     metadata.template_version = outdated.target_version
     metadata.last_synced = current_timestamp()
     
     # Validate
     validation = validate_skill(merged_content)
     IF validation.errors NOT empty:
       ERROR E-SYNC-005: "Validation failed post-sync"
       ROLLBACK from backup
       RETURN {success: false, error: "Validation failed"}
     
     # Write files
     write_file(outdated.skill.path, merged_content)
     write_yaml(outdated.skill.metadata_path, metadata)
     
     RETURN {success: true}

3. Manual merge process
   manual_merge_skill(outdated):
     # Similar to auto_merge but:
     # - Prompt for each conflict resolution
     # - Allow section-by-section review
     # - Provide conflict markers
     ...

4. Update MEMORY.md
   state = read_memory_md()
   state.last_sync = current_timestamp()
   
   IF NOT state.has("skills_synced"):
     state.skills_synced = []
   
   FOR EACH synced IN synced_skills:
     state.skills_synced.append({
       name: synced.skill.name,
       previous_version: synced.current_version,
       new_version: synced.target_version,
       updated: current_timestamp()
     })
   
   write_memory_md(state)

5. Summary
   DISPLAY: ""
   DISPLAY: "═══════════════════════════════════════════════════"
   DISPLAY: "Sync Complete"
   DISPLAY: "═══════════════════════════════════════════════════"
   DISPLAY: "Synced: {synced_count} ✅"
   DISPLAY: "Failed: {failed_count} ❌"
   DISPLAY: "Backups: {backup_dir}"
   DISPLAY: ""
   DISPLAY: "Next steps:"
   DISPLAY: "- Validate: /hefesto.validate"
   DISPLAY: "- Test updated skills with your AI CLI"
   DISPLAY: "═══════════════════════════════════════════════════"
   
   IF failed_count > 0:
     EXIT 1
   ELSE:
     EXIT 0
```

**Performance Target**: < 2s for 10 skills  
**References**: FR-009, T0-HEFESTO-06

---

## Error Cases

| Code | Condition | Handler |
|------|-----------|---------|
| **E-SYNC-001** | No skills found | Info message + exit gracefully |
| **E-SYNC-002** | Write permission denied | Error + list affected files |
| **E-SYNC-003** | Merge conflict | Manual review Human Gate |
| **E-SYNC-004** | Template version not found | Error + list available |
| **E-SYNC-005** | Validation fails post-sync | Rollback + show errors |
| **E-SYNC-006** | Backup creation fails | Block sync + warning |

---

## Usage Examples

### Example 1: Sync All Skills

```bash
> /hefesto.sync

Checking 5 skills for updates...

Found 2 skill(s) to update:
  - email-validator: v1.0.0 → v1.2.0
  - testing-strategy: v1.1.0 → v1.2.0

✅ Backups created: .hefesto/backups/sync-20260204-103000/

═══════════════════════════════════════════════════
🔄 Sync 2 Skill(s)?
═══════════════════════════════════════════════════

Skills to update:
- email-validator: v1.0.0 → v1.2.0
  Changes:
    • Added metadata.yaml support
    • Updated frontmatter structure

- testing-strategy: v1.1.0 → v1.2.0
  Changes:
    • Added version field

Backups created: .hefesto/backups/sync-20260204-103000/

═══════════════════════════════════════════════════

Actions: [approve all] [cancel]
> approve all

Syncing email-validator... ✅
Syncing testing-strategy... ✅

═══════════════════════════════════════════════════
Sync Complete
═══════════════════════════════════════════════════
Synced: 2 ✅
Failed: 0 ❌
Backups: .hefesto/backups/sync-20260204-103000/
```

### Example 2: Dry Run

```bash
> /hefesto.sync --dry-run

Checking 5 skills...

Found 2 skill(s) to update:
  - email-validator: v1.0.0 → v1.2.0
  - testing-strategy: v1.1.0 → v1.2.0

DRY RUN - No changes will be applied
═══════════════════════════════════════════════════

Skill: email-validator
Changes:
  + Add metadata.yaml support
  + Update frontmatter structure
  + Add version field

Skill: testing-strategy
Changes:
  + Add version field

To apply changes, run without --dry-run
```

### Example 3: Review Each

```bash
> /hefesto.sync

[... discovery ...]

Actions: [approve all] [review each] [cancel]
> review each

═══════════════════════════════════════════════════
Skill: email-validator (1/2)
═══════════════════════════════════════════════════

Current: v1.0.0
Target: v1.2.0

Changes:
  + Add metadata.yaml support
  + Update frontmatter structure

[approve] [skip] [edit] [cancel all]
> approve

═══════════════════════════════════════════════════
Skill: testing-strategy (2/2)
═══════════════════════════════════════════════════

[... repeat ...]
```

### Example 4: Specific Skill

```bash
> /hefesto.sync email-validator

Checking email-validator...

Current version: v1.0.0
Latest version: v1.2.0

Changes:
  + Add metadata.yaml support
  + Update frontmatter structure

[Proceeds with single skill sync...]
```

### Example 5: No Updates Needed

```bash
> /hefesto.sync

Checking 5 skills for updates...

✅ All skills are up to date
```

---

## Merge Policy

**Preserve:**
- User-written content sections
- Custom examples
- Modified descriptions
- Added references

**Update:**
- Template structure
- New required fields
- Updated metadata schema

**Conflict:**
- Structure changes affecting custom content → Manual review required

---

## Success Criteria

- ✅ **SC-001**: Command implemented
- ✅ **SC-003**: Human Gate enforced
- ✅ **US-003 Scenario 2**: Template updates
- ✅ **FR-009**: Outdated template detection

---

## Performance Targets

| Operation | Target | Typical |
|-----------|--------|---------|
| Discovery | < 1s | 500ms |
| Diff calculation | < 500ms per skill | 200ms |
| Backup creation | < 2s (10 skills) | 1s |
| Apply changes | < 2s (10 skills) | 1s |
| Human Gate wait | unbounded | N/A |
| **Total (excl. Human Gate)** | **< 5s** | **~3s** |

---

## Dependencies

**Required Helpers:**
- `helpers/human-gate.md` - Batch approval
- `helpers/template-validator.md` - Post-sync validation
- `helpers/skill-merger.md` - Preserve user changes

**Required Templates:**
- All CLI templates with version metadata

**State Files:**
- `MEMORY.md` - Sync history and skill registry

---

## See Also

- **Related Commands**: `/hefesto.adapt`, `/hefesto.validate`, `/hefesto.create`
- **Specification**: `specs/003-hefesto-commands/contracts/sync.contract.md`
- **T0 Rules**: `CONSTITUTION.md` (T0-HEFESTO-02, 06, 08)
- **User Story**: `specs/003-hefesto-commands/spec.md` US3
