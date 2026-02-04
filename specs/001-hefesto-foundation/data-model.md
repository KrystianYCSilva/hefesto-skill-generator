---
description: "Data model definition with entities, attributes, relationships, and validation rules for Hefesto Foundation"
feature: "001-hefesto-foundation"
type: "data-model"
phase: "1"
status: "complete"
created: "2026-02-04"
version: "1.0.0"
---

# Data Model: Hefesto Foundation Infrastructure

**Feature**: 001-hefesto-foundation  
**Date**: 2026-02-04  
**Phase**: 1 (Design)

## Overview

This document defines the data entities, their attributes, relationships, and validation rules for the Hefesto Foundation Infrastructure. These entities are persisted primarily in MEMORY.md and represent the runtime state of the Hefesto system.

---

## Entity Relationship Diagram

```text
┌─────────────────────────────────────────────────────────────────┐
│                        Project State                             │
│  ─────────────────────────────────────────────────────────────  │
│  hefesto_version: string                                         │
│  initialized: timestamp                                          │
│  last_updated: timestamp                                         │
└─────────────────┬──────────────────────────┬────────────────────┘
                  │                          │
                  │ 1                        │ 1
                  │                          │
                  │ *                        │ *
       ┌──────────▼──────────┐    ┌─────────▼────────────┐
       │ CLI Detection Result│    │  Skill Directory     │
       │  ────────────────── │    │  ──────────────────  │
       │  name: string       │    │  cli_name: string    │
       │  method: enum       │◄───┤  path: string        │
       │  version: string?   │ 1:1│  created: timestamp  │
       │  path: string       │    │  skill_count: int    │
       │  status: enum       │    └──────────────────────┘
       └─────────────────────┘
                  │
                  │ 1
                  │
                  │ *
       ┌──────────▼──────────┐
       │ Skill Registry Entry│
       │  ────────────────── │
       │  name: string       │
       │  clis: string[]     │
       │  created: timestamp │
       │  last_modified: ts  │
       └─────────────────────┘

       ┌─────────────────────┐
       │ Constitutional Rule │ (Read-only reference)
       │  ────────────────── │
       │  rule_id: string    │
       │  description: text  │
       │  level: enum        │
       └─────────────────────┘
```

---

## Entity Definitions

### 1. Project State

**Description**: Root entity representing the overall state of Hefesto in a project.

**Attributes**:

| Attribute | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `hefesto_version` | `string` | Yes | SemVer format (e.g., "1.0.0") | Version of Hefesto that initialized the project |
| `initialized` | `timestamp` | Yes | ISO 8601 format | When Hefesto was first initialized in this project |
| `last_updated` | `timestamp` | Yes | ISO 8601 format, >= initialized | Last time MEMORY.md was modified |
| `detected_clis` | `CLI Detection Result[]` | Yes | Min 0 items | List of detected AI CLIs |
| `skill_registry` | `Skill Registry Entry[]` | Yes | Min 0 items | List of generated skills |

**Relationships**:
- **Has many** CLI Detection Results (1:n)
- **Has many** Skill Registry Entries (1:n)

**Validation Rules**:
- `last_updated` MUST be >= `initialized`
- `hefesto_version` MUST match regex `^\d+\.\d+\.\d+$`
- MUST contain at least one CLI Detection Result after successful bootstrap

**Persistence**: MEMORY.md (Markdown with YAML frontmatter)

**Example**:

```yaml
---
hefesto_version: "1.0.0"
initialized: 2026-02-04T14:30:00Z
last_updated: 2026-02-04T15:45:00Z
---
```

---

### 2. CLI Detection Result

**Description**: Represents a detected AI CLI with metadata about how it was discovered and its current status.

**Attributes**:

| Attribute | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `name` | `string` | Yes | One of: "claude", "gemini", "codex", "copilot", "opencode", "cursor", "qwen" | Canonical CLI identifier |
| `detection_method` | `enum` | Yes | Values: "PATH", "config_directory", "manual" | How the CLI was detected |
| `version` | `string` | No | SemVer format or null | CLI version if detectable |
| `skills_directory_path` | `string` | Yes | Absolute or relative path | Location of skills directory for this CLI |
| `status` | `enum` | Yes | Values: "active", "warning_no_path", "error_permission" | Current CLI status |

**Relationships**:
- **Belongs to** Project State (n:1)
- **Has one** Skill Directory (1:1)

**Validation Rules**:
- `name` MUST be unique within a Project State
- `skills_directory_path` MUST match pattern `\.{name}/skills/?`
- If `detection_method` is "config_directory" and `status` is "active", SHOULD warn (CLI config exists but not in PATH)
- `version` is null if version detection fails (non-blocking)

**State Transitions**:

```text
[Detected via PATH] → status: "active"
[Detected via config only] → status: "warning_no_path"
[Permission error on creation] → status: "error_permission"
```

**Persistence**: MEMORY.md (Markdown table in "Detected CLIs" section)

**Example**:

```markdown
| CLI | Detection Method | Skills Directory | Version | Status |
|-----|------------------|------------------|---------|--------|
| claude | PATH | .claude/skills/ | 1.2.0 | active |
| gemini | config_directory | .gemini/skills/ | null | warning_no_path |
```

---

### 3. Skill Directory

**Description**: Represents a CLI-specific skills storage location on the filesystem.

**Attributes**:

| Attribute | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `cli_name` | `string` | Yes | Must match CLI Detection Result name | CLI this directory belongs to |
| `absolute_path` | `string` | Yes | Absolute filesystem path | Full path to skills directory |
| `created` | `timestamp` | Yes | ISO 8601 format | When directory was created |
| `skill_count` | `integer` | Yes | >= 0 | Number of skills in this directory |

**Relationships**:
- **Belongs to** CLI Detection Result (1:1)

**Validation Rules**:
- Directory MUST exist on filesystem
- Directory MUST be readable and writable by current user
- `absolute_path` MUST end with `/skills/` or `\skills\` (platform-specific)

**Lifecycle**:
- **Created**: During bootstrap when CLI is detected
- **Updated**: When skills are added/removed (skill_count changes)
- **Never deleted**: Directories persist even if CLI uninstalled

**Persistence**: Implicit (filesystem) + metadata in MEMORY.md

**Example** (filesystem):

```text
/home/user/projects/my-app/.claude/skills/
```

---

### 4. Skill Registry Entry

**Description**: Metadata about a generated skill tracked across CLI implementations.

**Attributes**:

| Attribute | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `name` | `string` | Yes | Agent Skills name format (lowercase, hyphens, max 64) | Skill identifier |
| `clis` | `string[]` | Yes | Min 1 item, values from CLI names | CLIs where skill is deployed |
| `created` | `timestamp` | Yes | ISO 8601 format | When skill was first generated |
| `last_modified` | `timestamp` | Yes | ISO 8601 format, >= created | Last time skill was updated |

**Relationships**:
- **Belongs to** Project State (n:1)

**Validation Rules**:
- `name` MUST match Agent Skills spec format: `^[a-z0-9]+(-[a-z0-9]+)*$`
- `name` MUST be <= 64 characters
- `clis` array MUST contain only valid CLI names from detected CLIs
- `last_modified` MUST be >= `created`
- Each `name` MUST be unique within Project State

**Lifecycle**:
- **Created**: When `/hefesto.create` or `/hefesto.extract` completes successfully
- **Updated**: When skill modified via `/hefesto.edit` (future)
- **Deleted**: When skill removed (entry removed from registry, directories cleaned)

**Persistence**: MEMORY.md (Markdown table in "Skill Registry" section)

**Example**:

```markdown
| Skill Name | CLIs | Created | Last Modified |
|------------|------|---------|---------------|
| code-review | claude, gemini, codex | 2026-02-04T10:00:00Z | 2026-02-04T11:30:00Z |
| api-docs | claude, copilot | 2026-02-04T12:00:00Z | 2026-02-04T12:00:00Z |
```

---

### 5. Constitutional Rule (Reference Entity)

**Description**: Read-only reference to governance rules defined in CONSTITUTION.md. Not persisted in MEMORY.md but validated against.

**Attributes**:

| Attribute | Type | Required | Constraints | Description |
|-----------|------|----------|-------------|-------------|
| `rule_id` | `string` | Yes | Format: "T{tier}-HEFESTO-{number}" | Unique rule identifier |
| `description` | `text` | Yes | Max 2048 characters | Rule definition |
| `enforcement_level` | `enum` | Yes | Values: "ABSOLUTE", "NORMATIVE", "INFORMATIVE" | How strictly enforced |

**Relationships**: None (reference only)

**Validation Rules**:
- `rule_id` MUST follow format `T[0-2]-HEFESTO-\d{2}`
- All T0 rules MUST be present in CONSTITUTION.md
- T0 rules are immutable (cannot be changed without Hefesto version upgrade)

**Persistence**: CONSTITUTION.md (source of truth, read-only)

**Example** (from CONSTITUTION.md):

```markdown
### T0-HEFESTO-01: Agent Skills Standard

**Regra:** TODA skill gerada DEVE seguir a especificacao [agentskills.io](https://agentskills.io).
```

---

## Data Integrity Rules

### Referential Integrity

1. **CLI Detection Result → Skill Directory**:
   - Every CLI Detection Result MUST have exactly one Skill Directory
   - Skill Directory MUST exist on filesystem

2. **Skill Registry Entry → CLI Detection Results**:
   - Every CLI name in `Skill Registry Entry.clis[]` MUST match a `CLI Detection Result.name`
   - Skills can only be deployed to detected CLIs

### State Consistency

1. **MEMORY.md Corruption Recovery**:
   - If MEMORY.md cannot be parsed:
     - Backup to `MEMORY.md.backup.{timestamp}`
     - Create fresh MEMORY.md with empty state
     - Rescan filesystem to rebuild CLI Detection Results and Skill Registry

2. **Filesystem Synchronization**:
   - `Skill Directory.skill_count` MUST match actual count of subdirectories in skills directory
   - If mismatch detected, rebuild from filesystem scan

### Versioning

1. **Hefesto Version Compatibility**:
   - If `Project State.hefesto_version` < current Hefesto version → migration check
   - If `Project State.hefesto_version` > current Hefesto version → error, upgrade required

---

## Validation Queries

### Bootstrap Validation

```markdown
CHECK: At least one CLI detected
  → SELECT COUNT(*) FROM cli_detection_results WHERE status IN ('active', 'warning_no_path')
  → MUST BE >= 1

CHECK: All skill directories exist
  → FOR EACH cli_detection_result
      VERIFY filesystem.exists(cli_detection_result.skills_directory_path)
```

### Runtime Validation

```markdown
CHECK: MEMORY.md is parseable
  → PARSE MEMORY.md YAML frontmatter
  → PARSE MEMORY.md Markdown tables

CHECK: All skills have valid CLI references
  → FOR EACH skill_registry_entry
      FOR EACH cli IN skill_registry_entry.clis
        VERIFY EXISTS cli_detection_result WHERE name = cli
```

### Constitution Validation

```markdown
CHECK: CONSTITUTION.md exists
  → VERIFY filesystem.exists("CONSTITUTION.md")

CHECK: All T0 rules present
  → FOR rule_id IN ["T0-HEFESTO-01" ... "T0-HEFESTO-11"]
      VERIFY CONSTITUTION.md CONTAINS rule_id
```

---

## Schema Evolution

### Version 1.0.0 (Current)

- Initial schema as defined above

### Future Considerations

| Version | Potential Changes | Migration Strategy |
|---------|-------------------|-------------------|
| 1.1.0 | Add `skill_tags` to Skill Registry Entry | Backward compatible, nullable |
| 1.2.0 | Add `dependencies` array to Skill Registry Entry | Backward compatible, default empty array |
| 2.0.0 | Change MEMORY.md format to JSON | Breaking change, migration script required |

---

## Appendix: File Format Examples

### Complete MEMORY.md Example

```markdown
---
hefesto_version: "1.0.0"
initialized: 2026-02-04T14:30:00Z
last_updated: 2026-02-04T15:45:00Z
---

# Hefesto Project State

## Detected CLIs

| CLI | Detection Method | Skills Directory | Version | Status |
|-----|------------------|------------------|---------|--------|
| claude | PATH | .claude/skills/ | 1.2.0 | active |
| gemini | config_directory | .gemini/skills/ | null | warning_no_path |
| opencode | PATH | .opencode/skills/ | 0.2.1 | active |

## Skill Registry

| Skill Name | CLIs | Created | Last Modified |
|------------|------|---------|---------------|
| code-review | claude, gemini, opencode | 2026-02-04T10:00:00Z | 2026-02-04T11:30:00Z |

## State Metadata

- **Total Skills**: 1
- **Active CLIs**: 3
- **Last Validation**: 2026-02-04T15:45:00Z
```

---

**Next Steps**: Generate contracts/ (CLI detection schema) and quickstart.md (bootstrap usage guide).
