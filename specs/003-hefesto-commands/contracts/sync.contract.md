# Contract: /hefesto.sync

## Command Purpose
Synchronize existing skills with latest templates and update outdated structures.

## Input Specification

**Args:**
- `skill_name` (positional, optional): Specific skill to sync
  - If missing: Sync ALL skills

**Flags:**
- `--cli <name>` (optional): Sync only in specific CLI directory
- `--dry-run` (optional): Show changes without applying
- `--template-version <version>` (optional): Target specific template version

**Environment:**
- Requires: Skills exist in CLI directories
- Requires: Template system with version tracking
- Requires: Write permissions (unless --dry-run)

## Output Specification

**User Messages:**
1. "Checking <N> skills for updates..."
2. For each outdated skill:
   - "<skill-name>: v1.0.0 → v1.2.0"
   - "Changes: <list of updates>"
3. Human Gate prompt (batch): `[approve all]`, `[review each]`, `[cancel]`
4. On approval: "Synced X skills"

**File Operations:**
- Update `.<cli>/skills/<name>/SKILL.md` (structure changes)
- Update/create `metadata.yaml` (new fields)
- Preserve custom content (user modifications)
- Update MEMORY.md

**MEMORY.md Updates:**
```yaml
last_sync: 2026-02-04
skills_synced:
  - name: <skill-name>
    previous_version: "1.0.0"
    new_version: "1.2.0"
    updated: 2026-02-04
```

## Side Effects

**Filesystem Changes:**
- Modified: Multiple SKILL.md files
- Modified: metadata.yaml files
- Modified: MEMORY.md
- Created: Backups in `.hefesto/backups/`

**State Mutations:**
- Update skill versions in registry
- Record sync timestamp

## Error Cases

| Error | Condition | Handler |
|-------|-----------|---------|
| `E-SYNC-001` | No skills found | Info message + exit gracefully |
| `E-SYNC-002` | Write permission denied | Error + list affected files |
| `E-SYNC-003` | Merge conflict (user changes) | Manual review Human Gate |
| `E-SYNC-004` | Template version not found | Error + list available versions |
| `E-SYNC-005` | Validation fails post-sync | Rollback + show errors |
| `E-SYNC-006` | Backup creation fails | Block sync + warning |

## Performance Targets

- Discovery: < 1s for 10 skills
- Diff calculation: < 500ms per skill
- Human Gate wait: unbounded
- Apply changes: < 2s for 10 skills
- **Total (excluding Human Gate):** < 5s for typical library

## Dependencies

**Required Helpers:**
- `helpers/human-gate.md` - Batch approval
- `helpers/template-validator.md` - Post-sync validation
- `helpers/skill-merger.md` - Preserve user changes

**Required Templates:**
- All CLI templates with version metadata

**State Files:**
- `MEMORY.md` - Sync history and skill registry

## Success Criteria Mapping

- **SC-001**: Command implemented
- **SC-003**: Human Gate enforced
- **US-003 Scenario 2**: Template updates
- **FR-002**: Human Gate requirement
- **FR-009**: Outdated template detection

## Sync Strategy

**Detection:**
1. Read `metadata.yaml:template_version` from each skill
2. Compare with current template version
3. Calculate diff of structural changes

**Merge Policy:**
- Preserve: User-written content sections
- Update: Template structure, new fields
- Conflict: Require manual review

**Backup:**
- Create `.hefesto/backups/<skill>-<timestamp>.tar.gz` before changes

## Example Invocations

```bash
# Sync all skills
/hefesto.sync
# Output:
# Checking 5 skills...
# email-validator: v1.0.0 → v1.2.0 (added metadata.yaml)
# testing-strategy: Up to date
# [approve all] or [review each]?

# Dry run
/hefesto.sync --dry-run
# Shows changes without applying

# Specific skill
/hefesto.sync email-validator

# Specific CLI
/hefesto.sync --cli gemini

# Target version
/hefesto.sync --template-version 1.1.0
```

## Mapped Requirements

- **FR-002**: Human Gate enforcement
- **FR-009**: Outdated template detection + updates
- **US-003 Scenario 2**: Template synchronization
- **T0-HEFESTO-02**: Human Gate protocol
- **T0-HEFESTO-08**: Safe, idempotent operations
