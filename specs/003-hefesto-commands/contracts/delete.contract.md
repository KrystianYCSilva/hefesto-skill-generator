# Contract: /hefesto.delete

## Command Purpose
Delete skill from filesystem with Human Gate confirmation (destructive operation).

## Input Specification

**Args:**
- `skill_name` (positional, required): Name of skill to delete

**Flags:**
- `--cli <name>` (optional): Delete from specific CLI only (default: all)
- `--force` (optional): Skip Human Gate (DANGEROUS - requires explicit confirmation)
- `--backup` (optional): Create backup before deletion (default: true)

**Environment:**
- Requires: Skill exists in at least one CLI directory
- Requires: Write permissions to skill directories
- Requires: Write permissions to MEMORY.md

## Output Specification

**User Messages:**
1. "Found <skill-name> in: <cli-list>"
2. Preview of files to be deleted
3. Human Gate prompt: "DELETE <skill-name>? This cannot be undone. [yes/no]"
4. On confirmation: "Creating backup..."
5. "Deleted <skill-name> from <N> CLI(s)"

**File Operations:**
- Backup: `.hefesto/backups/<skill>-<timestamp>.tar.gz`
- Delete: `.<cli>/skills/<name>/` (entire directory)
- Update MEMORY.md

**MEMORY.md Updates:**
```yaml
skills_deleted:
  - name: <skill-name>
    deleted: 2026-02-04
    backup: .hefesto/backups/<file>
    clis: [claude, gemini]
```

## Side Effects

**Filesystem Changes:**
- Deleted: `.<cli>/skills/<name>/` directory
- Created: Backup archive (if --backup=true)
- Modified: MEMORY.md

**State Mutations:**
- Remove from skill registry
- Add to deleted skills log
- Record backup location

## Error Cases

| Error | Condition | Handler |
|-------|-----------|---------|
| `E-DELETE-001` | Skill not found | Error + list available |
| `E-DELETE-002` | Write permission denied | Error + path details |
| `E-DELETE-003` | Backup creation fails | Block deletion + error |
| `E-DELETE-004` | User cancels Human Gate | Info: "Deletion cancelled" + exit |
| `E-DELETE-005` | Partial deletion (multi-CLI) | Rollback + error |
| `E-DELETE-006` | MEMORY.md update fails | Complete deletion but warn |

## Performance Targets

- Discovery: < 100ms
- Backup creation: < 1s per skill
- Human Gate wait: unbounded
- Deletion: < 500ms
- **Total (excluding Human Gate):** < 2s

## Dependencies

**Required Helpers:**
- `helpers/human-gate.md` - Destructive operation confirmation
- `helpers/cli-detector.md` - Skill locations

**State Files:**
- `MEMORY.md` - Skill registry and deletion log

## Success Criteria Mapping

- **SC-001**: Command implemented
- **SC-003**: Human Gate enforced 100%
- **US-004 Scenario 2**: Deletion with confirmation
- **FR-002**: Human Gate requirement
- **T0-HEFESTO-02**: Human Gate protocol

## Human Gate Specification

**Confirmation Text:**
```
═══════════════════════════════════════════════════
WARNING: DESTRUCTIVE OPERATION
═══════════════════════════════════════════════════
Skill: <skill-name>
Locations:
  - .claude/skills/<skill-name>/
  - .gemini/skills/<skill-name>/

Files to delete:
  - SKILL.md
  - metadata.yaml
  - scripts/validator.py
  (4 files, 12 KB total)

Backup will be created at:
  .hefesto/backups/<skill-name>-2026-02-04-103000.tar.gz

Type the skill name to confirm deletion: _
```

**Confirmation:** User must type exact skill name (not just "yes")

## Example Invocations

```bash
# Delete with confirmation
/hefesto.delete email-validator
# → Type skill name to confirm: email-validator
# → Deleted email-validator from 2 CLI(s)

# Delete from specific CLI
/hefesto.delete testing-strategy --cli gemini

# Force delete (skip Human Gate - DANGEROUS)
/hefesto.delete old-skill --force
# Still requires typing skill name

# Delete without backup
/hefesto.delete temp-skill --backup=false
```

## Mapped Requirements

- **FR-002**: Human Gate enforcement
- **US-004 Scenario 2**: Deletion with Human Gate
- **T0-HEFESTO-02**: Human Gate protocol
- **T0-HEFESTO-08**: Safe operations (backup before delete)
