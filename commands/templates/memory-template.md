---
description: "Template structure for MEMORY.md with YAML frontmatter schema and Markdown table format"
category: "template"
type: "state"
used_by: ["/hefesto.init", "/hefesto.detect", "recovery processes"]
format: "YAML + Markdown"
version: "1.0.0"
---

# MEMORY.md Template

**Purpose**: Template structure for MEMORY.md with YAML frontmatter schema  
**Used by**: `/hefesto.init`, `/hefesto.detect`, recovery processes

---

## Template Structure

```markdown
---
hefesto_version: "{VERSION}"
initialized: "{ISO8601_TIMESTAMP}"
last_updated: "{ISO8601_TIMESTAMP}"
---

# Hefesto Project State

## Detected CLIs

| CLI | Detection Method | Skills Directory | Version | Status |
|-----|------------------|------------------|---------|--------|
{CLI_DETECTION_ROWS}

## Skill Registry

| Skill Name | CLIs | Created | Last Modified |
|------------|------|---------|---------------|
{SKILL_REGISTRY_ROWS}

## State Metadata

- **Total Skills**: {SKILL_COUNT}
- **Active CLIs**: {CLI_COUNT}
- **Last Validation**: {ISO8601_TIMESTAMP}
```

---

## Frontmatter Schema

| Field | Type | Required | Format | Description |
|-------|------|----------|--------|-------------|
| `hefesto_version` | string | Yes | SemVer (x.y.z) | Hefesto version that initialized project |
| `initialized` | timestamp | Yes | ISO 8601 | When Hefesto was first initialized |
| `last_updated` | timestamp | Yes | ISO 8601 | Last time MEMORY.md was modified |

**Validation Rules**:
- `hefesto_version` MUST match regex `^\d+\.\d+\.\d+$`
- `last_updated` MUST be >= `initialized`
- All timestamps in UTC

---

## CLI Detection Row Schema

**Format**: Markdown table row

**Fields**:
- `CLI`: Canonical name (claude, gemini, codex, copilot, opencode, cursor, qwen)
- `Detection Method`: PATH | config_directory | manual
- `Skills Directory`: Relative path to skills directory (e.g., `.claude/skills/`)
- `Version`: SemVer or "null" if undetectable
- `Status`: active | warning_no_path | error_permission

**Example**:
```markdown
| claude | PATH | .claude/skills/ | 1.2.0 | active |
| gemini | config_directory | .gemini/skills/ | null | warning_no_path |
```

---

## Skill Registry Row Schema

**Format**: Markdown table row

**Fields**:
- `Skill Name`: Agent Skills format (lowercase, hyphens, max 64 chars)
- `CLIs`: Comma-separated list of CLI names
- `Created`: ISO 8601 timestamp
- `Last Modified`: ISO 8601 timestamp

**Example**:
```markdown
| code-review | claude, gemini, opencode | 2026-02-04T10:00:00Z | 2026-02-04T11:30:00Z |
```

---

## State Metadata

**Computed Fields** (derived from tables, not authoritative):
- `Total Skills`: COUNT(Skill Registry rows)
- `Active CLIs`: COUNT(CLI Detection rows WHERE status = 'active')
- `Last Validation`: Timestamp of last validation check

---

## Usage

### Creating New MEMORY.md

```markdown
1. Copy template structure
2. Replace {VERSION} with current Hefesto version
3. Replace {ISO8601_TIMESTAMP} with current UTC timestamp
4. Initialize empty tables (headers only, no data rows)
5. Set Total Skills = 0, Active CLIs = 0
```

### Updating Existing MEMORY.md

```markdown
1. Parse frontmatter YAML
2. Update `last_updated` timestamp
3. Add/update rows in appropriate table
4. Recalculate State Metadata
5. Preserve all existing data
```

### Validation

```markdown
CHECK: Frontmatter is valid YAML
CHECK: All required frontmatter fields present
CHECK: Timestamps in ISO 8601 format
CHECK: Tables have required columns
CHECK: No duplicate CLI names
CHECK: No duplicate skill names
```

---

## Error Recovery

### Corrupted MEMORY.md

```markdown
1. Attempt to parse YAML frontmatter
2. If parse fails:
   a. Backup to MEMORY.md.backup.{timestamp}
   b. Create fresh MEMORY.md from this template
   c. Rescan filesystem to rebuild CLI and skill data
   d. Log recovery action
```

### Missing Fields

```markdown
IF frontmatter missing fields:
  - Add missing fields with default values
  - Set initialized = last_updated = current timestamp
  - Set hefesto_version = current version
  - Log repair action
```

---

## References

- Data Model: Project State entity (data-model.md)
- Data Model: CLI Detection Result entity (data-model.md)
- Data Model: Skill Registry Entry entity (data-model.md)
- FR-004: Initialize MEMORY.md with empty state structure
- FR-011: Track detected CLIs, skill names, timestamp, version
- FR-016: Handle corrupted MEMORY.md recovery
