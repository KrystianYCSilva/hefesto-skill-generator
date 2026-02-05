# Data Model: Multi-CLI Detection and Generation

**Feature**: 004-multi-cli-generator  
**Phase**: 1 (Design)  
**Date**: 2026-02-04

---

## 1. CLI Detection Result

**Purpose**: Represents the outcome of detecting a single AI CLI.

### Schema

```yaml
name: string              # CLI name (e.g., "claude", "gemini", "codex")
status: enum              # detected | detected_config_only | not_found | error
version: string | null    # Version string (e.g., "2.1.31") or null if unknown
executable_path: string | null  # Full path to CLI executable (e.g., "/usr/local/bin/claude")
config_directory: string  # Relative path to config directory (e.g., ".claude")
detection_method: enum    # path | config_dir | both
priority: integer         # 1-7, used for conflict resolution
error_message: string | null  # Error description if status=error
```

### Status Values

| Status | Meaning | Executable | Config Dir |
|--------|---------|------------|------------|
| `detected` | Fully detected | ✅ Found | ✅ Exists |
| `detected_config_only` | Config found, no executable | ❌ Not found | ✅ Exists |
| `not_found` | Not detected | ❌ Not found | ❌ Not exists |
| `error` | Detection error | ❓ Error | ❓ Error |

### Detection Method Values

| Method | Meaning |
|--------|---------|
| `path` | Detected via PATH scanning only |
| `config_dir` | Detected via config directory check only |
| `both` | Detected via both methods |

### Example Instances

**Fully Detected CLI (Claude)**:
```yaml
name: claude
status: detected
version: 2.1.31
executable_path: C:\Users\kryst\AppData\Local\Claude\claude.exe
config_directory: .claude
detection_method: both
priority: 1
error_message: null
```

**Config-Only Detection (Gemini)**:
```yaml
name: gemini
status: detected_config_only
version: null
executable_path: null
config_directory: .gemini
detection_method: config_dir
priority: 2
error_message: null
```

**Not Found (Cursor)**:
```yaml
name: cursor
status: not_found
version: null
executable_path: null
config_directory: .cursor
detection_method: null
priority: 6
error_message: null
```

**Error State (Codex)**:
```yaml
name: codex
status: error
version: null
executable_path: /usr/local/bin/codex
config_directory: .codex
detection_method: path
priority: 3
error_message: "Permission denied when executing version check"
```

---

## 2. CLI Adapter

**Purpose**: Defines CLI-specific transformations for skill generation.

### Schema

```yaml
cli_name: string          # Target CLI name (must match CLI Detection Result.name)
variable_syntax: map      # Variable transformation rules
directory_structure: map  # Directory path adjustments
frontmatter_additions: map  # Additional frontmatter fields
validation_rules: list    # CLI-specific validation requirements
```

### Variable Syntax Map

```yaml
variable_syntax:
  ARGUMENTS: string       # Replacement for $ARGUMENTS variable
  # Future: additional variables as needed
```

### Directory Structure Map

```yaml
directory_structure:
  skills_base: string     # Base directory for skills (e.g., ".claude/skills")
  use_skill_name_dir: boolean  # Whether skill has own directory
  additional_paths: list  # Additional directories to create
```

### Frontmatter Additions Map

```yaml
frontmatter_additions:
  field_name: string      # Additional YAML fields to inject
  # Example: "cli_version: minimum"
```

### Validation Rules List

```yaml
validation_rules:
  - rule_id: string       # Unique identifier for rule
    description: string   # Human-readable description
    check: string         # Validation logic (prompt-based)
```

### Example Instances

**Claude Adapter (Reference)**:
```yaml
cli_name: claude
variable_syntax:
  ARGUMENTS: "$ARGUMENTS"
directory_structure:
  skills_base: ".claude/skills"
  use_skill_name_dir: true
  additional_paths: []
frontmatter_additions: {}
validation_rules:
  - rule_id: agent-skills-compliance
    description: "Validate against agentskills.io spec"
    check: "Run existing validator from /hefesto.validate"
```

**Gemini Adapter**:
```yaml
cli_name: gemini
variable_syntax:
  ARGUMENTS: "{{args}}"
directory_structure:
  skills_base: ".gemini/skills"
  use_skill_name_dir: true
  additional_paths: []
frontmatter_additions: {}
validation_rules:
  - rule_id: agent-skills-compliance
    description: "Validate against agentskills.io spec"
    check: "Run existing validator from /hefesto.validate"
  - rule_id: gemini-variable-syntax
    description: "Ensure {{args}} syntax used instead of $ARGUMENTS"
    check: "Search SKILL.md for $ARGUMENTS, fail if found"
```

**Copilot Adapter**:
```yaml
cli_name: copilot
variable_syntax:
  ARGUMENTS: "$ARGUMENTS"
directory_structure:
  skills_base: ".github/skills"
  use_skill_name_dir: true
  additional_paths: []
frontmatter_additions:
  github_integration: true
validation_rules:
  - rule_id: agent-skills-compliance
    description: "Validate against agentskills.io spec"
    check: "Run existing validator from /hefesto.validate"
```

**Qwen Adapter**:
```yaml
cli_name: qwen
variable_syntax:
  ARGUMENTS: "{{args}}"
directory_structure:
  skills_base: ".qwen/skills"
  use_skill_name_dir: true
  additional_paths: []
frontmatter_additions: {}
validation_rules:
  - rule_id: agent-skills-compliance
    description: "Validate against agentskills.io spec"
    check: "Run existing validator from /hefesto.validate"
  - rule_id: qwen-variable-syntax
    description: "Ensure {{args}} syntax used instead of $ARGUMENTS"
    check: "Search SKILL.md for $ARGUMENTS, fail if found"
```

---

## 3. Generation Task

**Purpose**: Represents a single skill generation operation for one CLI.

### Schema

```yaml
task_id: string           # Unique identifier (e.g., "gen-claude-20260204-103000")
target_cli: string        # CLI name from CLI Detection Result
skill_name: string        # Skill name (lowercase-hyphenated)
status: enum              # pending | in_progress | success | failed | rolled_back
start_time: datetime | null  # ISO 8601 timestamp
end_time: datetime | null    # ISO 8601 timestamp
output_paths: list        # List of created file paths
error_message: string | null  # Error description if failed
```

### Status Values

| Status | Meaning | Terminal |
|--------|---------|----------|
| `pending` | Task queued, not started | No |
| `in_progress` | Generation executing | No |
| `success` | Generation completed successfully | Yes |
| `failed` | Generation failed | Yes |
| `rolled_back` | Successfully cleaned up after failure | Yes |

### Example Instances

**Successful Task (Claude)**:
```yaml
task_id: gen-claude-20260204-103000
target_cli: claude
skill_name: code-review
status: success
start_time: 2026-02-04T10:30:00Z
end_time: 2026-02-04T10:30:02Z
output_paths:
  - .claude/skills/code-review/SKILL.md
  - .claude/skills/code-review/references/EXAMPLES.md
error_message: null
```

**Failed Task (Gemini)**:
```yaml
task_id: gen-gemini-20260204-103000
target_cli: gemini
skill_name: code-review
status: failed
start_time: 2026-02-04T10:30:00Z
end_time: 2026-02-04T10:30:03Z
output_paths: []
error_message: "Validation failed: SKILL.md contains $ARGUMENTS instead of {{args}}"
```

**Rolled Back Task (Codex)**:
```yaml
task_id: gen-codex-20260204-103000
target_cli: codex
skill_name: code-review
status: rolled_back
start_time: 2026-02-04T10:30:00Z
end_time: 2026-02-04T10:30:03Z
output_paths:
  - .codex/skills/code-review/SKILL.md  # Deleted during rollback
error_message: "Rolled back due to sibling task failure (gen-gemini-20260204-103000)"
```

---

## 4. Detection Report

**Purpose**: Aggregates CLI Detection Results for display to user.

### Schema

```yaml
detection_timestamp: datetime  # When detection ran
total_supported: integer       # Total CLIs checked (always 7)
total_detected: integer        # Number of CLIs with status=detected
total_config_only: integer     # Number with status=detected_config_only
clis: list                     # List of CLI Detection Results
```

### Example Instance

```yaml
detection_timestamp: 2026-02-04T10:30:00Z
total_supported: 7
total_detected: 3
total_config_only: 1
clis:
  - name: claude
    status: detected
    version: 2.1.31
    executable_path: /usr/local/bin/claude
    config_directory: .claude
    detection_method: both
    priority: 1
    error_message: null
  
  - name: gemini
    status: detected_config_only
    version: null
    executable_path: null
    config_directory: .gemini
    detection_method: config_dir
    priority: 2
    error_message: null
  
  - name: codex
    status: detected
    version: 0.91.2
    executable_path: /usr/local/bin/codex
    config_directory: .codex
    detection_method: both
    priority: 3
    error_message: null
  
  - name: copilot
    status: not_found
    version: null
    executable_path: null
    config_directory: .github
    priority: 4
    error_message: null
  
  - name: opencode
    status: detected
    version: 0.2.1
    executable_path: /usr/local/bin/opencode
    config_directory: .opencode
    detection_method: both
    priority: 5
    error_message: null
  
  - name: cursor
    status: not_found
    version: null
    executable_path: null
    config_directory: .cursor
    priority: 6
    error_message: null
  
  - name: qwen
    status: not_found
    version: null
    executable_path: null
    config_directory: .qwen
    priority: 7
    error_message: null
```

---

## 5. Generation Report

**Purpose**: Aggregates Generation Tasks for display to user.

### Schema

```yaml
generation_timestamp: datetime  # When generation started
skill_name: string              # Name of skill being generated
total_tasks: integer            # Number of CLIs targeted
successful: integer             # Number of successful tasks
failed: integer                 # Number of failed tasks
rollback_occurred: boolean      # Whether rollback was triggered
tasks: list                     # List of Generation Tasks
summary_message: string         # Human-readable summary
```

### Example Instance (Success)

```yaml
generation_timestamp: 2026-02-04T10:30:00Z
skill_name: code-review
total_tasks: 3
successful: 3
failed: 0
rollback_occurred: false
tasks:
  - task_id: gen-claude-20260204-103000
    target_cli: claude
    status: success
    output_paths: [.claude/skills/code-review/SKILL.md]
  - task_id: gen-gemini-20260204-103000
    target_cli: gemini
    status: success
    output_paths: [.gemini/skills/code-review/SKILL.md]
  - task_id: gen-opencode-20260204-103000
    target_cli: opencode
    status: success
    output_paths: [.opencode/skills/code-review/SKILL.md]
summary_message: "Successfully generated skill 'code-review' for 3 CLIs: claude, gemini, opencode"
```

### Example Instance (Failure with Rollback)

```yaml
generation_timestamp: 2026-02-04T10:30:00Z
skill_name: code-review
total_tasks: 3
successful: 0
failed: 1
rollback_occurred: true
tasks:
  - task_id: gen-claude-20260204-103000
    target_cli: claude
    status: rolled_back
    error_message: "Rolled back due to sibling failure"
  - task_id: gen-gemini-20260204-103000
    target_cli: gemini
    status: failed
    error_message: "Validation failed: $ARGUMENTS found instead of {{args}}"
  - task_id: gen-opencode-20260204-103000
    target_cli: opencode
    status: rolled_back
    error_message: "Rolled back due to sibling failure"
summary_message: "Generation failed for gemini. All changes rolled back."
```

---

## 6. MEMORY.md Extension Schema

**Purpose**: Persistent storage for detection results.

### New Section: `detected_clis`

```yaml
detected_clis:
  last_detection: datetime      # ISO 8601 timestamp
  clis: list                    # List of CLI Detection Results (only detected ones)
```

### Example MEMORY.md Entry

```yaml
# ... existing MEMORY.md content ...

## Detected CLIs

last_detection: 2026-02-04T10:30:00Z

clis:
  - name: claude
    status: detected
    version: 2.1.31
    path: /usr/local/bin/claude
    config_dir: .claude
    method: both
  
  - name: gemini
    status: detected_config_only
    version: unknown
    path: null
    config_dir: .gemini
    method: config_dir
  
  - name: opencode
    status: detected
    version: 0.2.1
    path: /usr/local/bin/opencode
    config_dir: .opencode
    method: both
```

---

## 7. CLI Priority Matrix

**Purpose**: Defines conflict resolution order when multiple CLIs match.

### Priority Table

| Priority | CLI Name | Rationale |
|----------|----------|-----------|
| 1 | Claude Code | Reference implementation, highest Agent Skills adoption |
| 2 | Gemini CLI | Google-backed, strong documentation |
| 3 | OpenAI Codex | OpenAI official tooling |
| 4 | VS Code/Copilot | GitHub/Microsoft integration, widespread adoption |
| 5 | OpenCode | Current CLI in use, local development focus |
| 6 | Cursor | Emerging AI-native editor |
| 7 | Qwen Code | Alibaba Cloud, growing adoption |

**Usage**: When conflict occurs (e.g., both `.claude/` and `.codex/` exist but only one CLI executable found), select lower priority number.

---

## 8. Entity Relationships

```
Detection Report (1) ─────> (N) CLI Detection Result
                                    │
                                    │ (referenced by)
                                    │
Generation Task (N) ────────────────┘
                                    │
                                    │ (uses)
                                    │
CLI Adapter (1) ────────────────────┘

Generation Report (1) ─────> (N) Generation Task
```

### Cardinality Notes

- One Detection Report contains multiple CLI Detection Results (1:N)
- Each Generation Task references one CLI Detection Result (N:1)
- Each Generation Task uses one CLI Adapter (N:1)
- One Generation Report aggregates multiple Generation Tasks (1:N)
- CLI Adapter is stateless (shared across all Generation Tasks for that CLI)

---

## 9. State Transitions

### CLI Detection Result Status

```
[initial] ─┬─> pending detection
           │
           ├─> detected (path + config found)
           ├─> detected_config_only (config only)
           ├─> not_found (neither found)
           └─> error (detection failed)
```

Terminal states: `detected`, `detected_config_only`, `not_found`, `error`

### Generation Task Status

```
[initial] ──> pending
              │
              └──> in_progress
                   │
                   ├──> success (terminal)
                   │
                   └──> failed
                        │
                        └──> rolled_back (terminal)
```

Terminal states: `success`, `rolled_back`

**Rollback Trigger**: When ANY task in Generation Report reaches `failed` status, ALL sibling tasks transition to `rolled_back`.

---

## 10. Validation Rules

### CLI Detection Result

- `name` MUST match one of 7 supported CLIs
- `priority` MUST be 1-7 and unique per CLI
- If `status=detected`, `executable_path` MUST NOT be null
- If `status=error`, `error_message` MUST NOT be null
- `config_directory` MUST start with `.` and match CLI name

### CLI Adapter

- `cli_name` MUST match a CLI Detection Result name
- `variable_syntax.ARGUMENTS` MUST NOT be empty
- `directory_structure.skills_base` MUST start with `.`
- All `validation_rules` MUST have unique `rule_id`

### Generation Task

- `task_id` MUST be unique across all tasks in Generation Report
- `target_cli` MUST exist in Detection Report
- If `status=success`, `output_paths` MUST NOT be empty
- If `status=failed`, `error_message` MUST NOT be null
- `end_time` MUST be >= `start_time` (if both present)

---

## 11. Data Model Summary

| Entity | Purpose | Persistence | Mutability |
|--------|---------|-------------|------------|
| CLI Detection Result | Detection outcome | MEMORY.md | Immutable after detection |
| CLI Adapter | Transformation rules | Hardcoded in helper | Immutable |
| Generation Task | Single CLI generation | In-memory (reported) | Mutable (status transitions) |
| Detection Report | Detection summary | MEMORY.md | Immutable after detection |
| Generation Report | Generation summary | In-memory (reported) | Immutable after generation |

---

**Data Model Complete** | Ready for Human Gate Approval → Contracts Phase
