# Data Model: Human Gate + Wizard Mode

**Feature**: 005-human-gate  
**Date**: 2026-02-05  
**Phase**: 1 (Design)  
**Source**: [spec.md](./spec.md) - Key Entities section

---

## Entity Overview

```
┌─────────────────┐         ┌─────────────────┐
│  Wizard State   │────────▶│  Preview Object │
└─────────────────┘         └─────────────────┘
                                     │
                                     ▼
                            ┌─────────────────┐
                            │  Human Gate     │
                            │  Decision       │
                            └─────────────────┘
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
            ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
            │  Collision  │  │  Expansion  │  │  Audit Log  │
            │  Info       │  │  Request    │  │  Entry      │
            └─────────────┘  └─────────────┘  └─────────────┘
```

---

## 1. Preview Object

**Purpose**: Represents in-memory skill before persistence (FR-001)

### Attributes

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `skill_name` | str | Yes | Sanitized skill name (T0-HEFESTO-07 format) |
| `skill_content` | str | Yes | Full SKILL.md markdown content |
| `metadata` | dict | Yes | YAML frontmatter parsed as dict |
| `target_clis` | list[str] | Yes | CLIs to generate for (from Feature 004 detection) |
| `validation_status` | str | Yes | 'valid' \| 'invalid' |
| `validation_errors` | list[str] | No | Empty if valid, error messages if invalid |
| `timestamp` | datetime | Yes | When preview was generated |
| `file_paths` | dict[str, Path] | Yes | {cli_name: path} mapping |
| `file_sizes` | dict[str, int] | Yes | {cli_name: bytes} mapping |
| `resources` | list[ExpansionRequest] | No | JIT resources added via [expand] |

### Validation Rules

- `skill_name`: Must match `^[a-z0-9]+(-[a-z0-9]+)*$`, max 64 chars (FR-013, T0-HEFESTO-07)
- `skill_content`: Must have valid YAML frontmatter + markdown body (FR-002, T0-HEFESTO-01)
- `validation_status`: Set to 'valid' only if passes all T0 checks (FR-002)
- `target_clis`: Must be non-empty (at least one CLI detected) (Assumption #5)

### State Transitions

```
[Created] → [Validated] → [Presented to User] → [Approved/Rejected/Edited]
```

### Example

```python
preview = Preview Object(
    skill_name="code-review",
    skill_content="---\nname: code-review\n...",
    metadata={'name': 'code-review', 'description': '...'},
    target_clis=['claude', 'gemini', 'opencode'],
    validation_status='valid',
    validation_errors=[],
    timestamp=datetime(2026, 2, 5, 14, 30),
    file_paths={
        'claude': Path('.claude/skills/code-review'),
        'gemini': Path('.gemini/skills/code-review'),
        'opencode': Path('.opencode/skills/code-review')
    },
    file_sizes={'claude': 1234, 'gemini': 1234, 'opencode': 1234},
    resources=[]
)
```

---

## 2. Wizard State

**Purpose**: Maintains wizard progress across steps (FR-010, FR-012)

### Attributes

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `current_step` | int | Yes | Current wizard step (1-4) |
| `collected_inputs` | dict | Yes | {step_name: user_input} mapping |
| `visited_steps` | list[int] | Yes | Steps already completed (for 'back' command) |
| `start_timestamp` | datetime | Yes | When wizard started |
| `timeout_at` | datetime | Yes | When wizard will timeout (start + 5 minutes) |
| `state_file_path` | Path | No | Where state is saved on timeout |

### Steps

1. **Step 1**: Skill name (FR-010)
2. **Step 2**: Description (FR-010)
3. **Step 3**: Main instructions (FR-010)
4. **Step 4**: Optional JIT resources (FR-010)

### State Transitions

```
[Start] → [Step 1] ⇄ [Step 2] ⇄ [Step 3] ⇄ [Step 4] → [Complete]
                                    │
                                    ▼
                            [Timeout/Interrupt]
                                    │
                                    ▼
                            [Saved to .hefesto/temp/]
```

### Persistence Format (JSON)

```json
{
  "current_step": 2,
  "collected_inputs": {
    "skill_name": "code-review",
    "description": "Standardize code reviews..."
  },
  "visited_steps": [1],
  "start_timestamp": "2026-02-05T14:30:00",
  "timeout_at": "2026-02-05T14:35:00"
}
```

### Validation Rules

- `current_step`: Must be 1-4
- `timeout_at`: Must be `start_timestamp + 300 seconds` (5 minutes - FR-005)
- `collected_inputs`: Each value must pass sanitization (FR-031)

---

## 3. Human Gate Decision

**Purpose**: Records user choice at approval gate (FR-004)

### Attributes

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `decision` | str | Yes | 'approve' \| 'expand' \| 'edit' \| 'reject' |
| `timestamp` | datetime | Yes | When decision was made |
| `response_time` | float | Yes | Seconds from preview to decision |
| `preview_id` | str | Yes | UUID of associated Preview Object |
| `user` | str | No | Username (from $USER env var) |

### State Machine

```
[Preview Displayed]
        │
        ▼
    [Await Decision] (timeout: 5 minutes)
        │
        ├─[approve]─→ [Persist Files]
        ├─[expand]──→ [Expansion Mode] → [Updated Preview] → [Await Decision]
        ├─[edit]────→ [Launch Editor] → [Re-Validate] → [Updated Preview] → [Await Decision]
        ├─[reject]──→ [Abort]
        └─[timeout]─→ [Auto-Cancel]
```

### Validation Rules

- `decision`: Must be one of the 4 valid options (FR-004)
- `response_time`: If > 300 seconds, decision must be 'timeout' (FR-005, SC-007)

---

## 4. Collision Info

**Purpose**: Metadata about existing skill when collision detected (FR-020)

### Attributes

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `existing_skill_name` | str | Yes | Name of colliding skill |
| `created_date` | datetime | Yes | From file metadata (ctime) |
| `modified_date` | datetime | Yes | From file metadata (mtime) |
| `author` | str | No | From git blame or metadata |
| `version` | str | No | From metadata.version field |
| `file_paths` | list[Path] | Yes | All locations where skill exists |
| `backup_path` | Path | No | Set if [overwrite] chosen (FR-023) |

### Validation Rules

- `file_paths`: Must be non-empty (at least one collision detected)
- `backup_path`: Required if decision is 'overwrite', must end in `.tar.gz` (FR-023)

### Example

```python
collision = CollisionInfo(
    existing_skill_name="code-review",
    created_date=datetime(2026, 1, 15, 10, 0),
    modified_date=datetime(2026, 2, 1, 14, 30),
    author="john.doe",
    version="1.0.0",
    file_paths=[
        Path('.claude/skills/code-review'),
        Path('.gemini/skills/code-review')
    ],
    backup_path=None  # Not yet backed up
)
```

---

## 5. Expansion Request

**Purpose**: Tracks JIT resources being added (FR-015 to FR-019)

### Attributes

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `resource_type` | str | Yes | 'scripts' \| 'references' \| 'assets' |
| `filename` | str | Yes | Name of resource file |
| `content` | str | No | File content (for scripts/references) |
| `path` | Path | No | Source path (for assets) |
| `created_at` | datetime | Yes | When resource was added |

### Validation Rules

- `resource_type`: Must be one of 3 valid types (FR-016)
- `filename`: Must not contain path traversal (../, ..\\) (T0-HEFESTO-11)
- `content` XOR `path`: Exactly one must be set (not both)

### Example

```python
expansion = ExpansionRequest(
    resource_type="scripts",
    filename="validate.sh",
    content="#!/bin/bash\n# Validation script\n...",
    path=None,
    created_at=datetime(2026, 2, 5, 14, 35)
)
```

---

## 6. Audit Log Entry

**Purpose**: Operation log for audit trail (FR-033)

### Attributes

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `operation` | str | Yes | 'create' \| 'extract' \| 'overwrite' \| 'merge' \| 'reject' |
| `skill_name` | str | Yes | Name of skill involved |
| `user` | str | Yes | Username (from $USER) |
| `timestamp` | datetime | Yes | When operation occurred |
| `decision` | str | Yes | Human Gate decision made |
| `target_clis` | list[str] | Yes | CLIs skill was generated for |
| `response_time_seconds` | float | Yes | Time from preview to decision |
| `success` | bool | Yes | Whether operation completed successfully |
| `error_message` | str | No | If success=False, the error |

### Persistence Format (JSON Lines)

```jsonl
{"operation":"create","skill_name":"code-review","user":"john.doe","timestamp":"2026-02-05T14:35:00","decision":"approve","target_clis":["claude","gemini"],"response_time_seconds":45.2,"success":true}
{"operation":"overwrite","skill_name":"code-review","user":"jane.smith","timestamp":"2026-02-05T15:00:00","decision":"approve","target_clis":["claude"],"response_time_seconds":120.5,"success":true}
```

### Storage Location

`.hefesto/logs/audit.jsonl` (append-only)

---

## Relationships

### Wizard → Preview
- Wizard collects inputs → generates Preview Object → passes to Human Gate

### Preview → Decision
- Preview displayed → user makes Decision → Decision triggers action

### Decision → Collision
- If Decision is 'approve' and skill exists → detect Collision → present options

### Decision → Expansion
- If Decision is 'expand' → collect Expansion Requests → update Preview

### All Operations → Audit Log
- Every Human Gate decision creates Audit Log Entry

---

## Database Schema (N/A)

This feature uses filesystem only. No database required.

**Runtime Storage**:
- `.hefesto/backups/` - Skill backups (`.tar.gz`)
- `.hefesto/temp/` - Wizard state (JSON)
- `.hefesto/logs/audit.jsonl` - Audit trail (JSON Lines)

---

**Data Model Status**: ✅ COMPLETE  
**Next**: Contracts (API/interface definitions)
