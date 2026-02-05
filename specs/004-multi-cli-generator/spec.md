# Feature Specification: Multi-CLI Automatic Detection and Parallel Skill Generation

**Feature Branch**: `004-multi-cli-generator`  
**Created**: 2026-02-04  
**Status**: Draft  
**Input**: Implement CARD-004 Multi-CLI Generator for automatic detection and parallel skill generation across multiple AI CLIs (Claude, Gemini, Codex, Copilot, OpenCode, Cursor, Qwen) following Agent Skills spec, ADR-001, ADR-002, ADR-003 and T0-HEFESTO-04, T0-HEFESTO-09

---

## User Scenarios & Testing

### User Story 1 - Automatic CLI Detection (Priority: P1)

As a developer using multiple AI CLIs, when I run `/hefesto.create`, the system automatically detects which CLIs I have installed without asking me, so I don't have to manually specify them.

**Why this priority**: Core value proposition - removes friction and manual configuration. Foundation for all multi-CLI operations.

**Independent Test**: Can be fully tested by running `/hefesto.create` on a system with multiple CLIs installed and verifying all are detected automatically without user prompts.

**Acceptance Scenarios**:

1. **Given** I have Claude Code and Gemini CLI installed in PATH, **When** I run `/hefesto.create "code review skill"`, **Then** system detects both CLIs automatically within 500ms
2. **Given** I have OpenCode config directory (`.opencode/`) but no PATH executable, **When** system runs detection, **Then** OpenCode is still detected as available
3. **Given** I have 4 different CLIs installed, **When** system performs detection, **Then** all 4 are identified correctly with their versions
4. **Given** no AI CLIs are installed, **When** system runs detection, **Then** system enters interactive fallback mode asking which CLI to target

---

### User Story 2 - Parallel Skill Generation for All Detected CLIs (Priority: P1)

As a developer, when I create a skill, it is automatically generated for all my installed CLIs simultaneously, so I have consistent access across all tools without manual duplication.

**Why this priority**: Primary feature goal - ensures skill consistency. Without this, multi-CLI support is incomplete.

**Independent Test**: Create one skill and verify it appears correctly in all detected CLI directories (`.claude/skills/`, `.gemini/skills/`, etc.) with proper adaptations.

**Acceptance Scenarios**:

1. **Given** 3 CLIs are detected (Claude, Gemini, OpenCode), **When** I approve a skill creation, **Then** skill is generated in all 3 CLI directories simultaneously
2. **Given** Gemini CLI is detected, **When** skill is generated, **Then** Gemini version uses `{{args}}` syntax instead of `$ARGUMENTS`
3. **Given** VS Code/Copilot is detected, **When** skill is generated, **Then** skill structure follows `.github/skills/` conventions
4. **Given** skill generation fails for one CLI, **When** error occurs, **Then** system rolls back all generated skills and reports which CLI failed

---

### User Story 3 - Selective CLI Targeting (Priority: P2)

As a developer, I can optionally restrict skill generation to specific CLIs using `--cli` flag, so I have control when I don't want skills in all tools.

**Why this priority**: Power user feature - nice to have but not critical for MVP. Default behavior (all CLIs) covers most use cases.

**Independent Test**: Run `/hefesto.create "skill" --cli claude,gemini` and verify skill only appears in those two CLI directories.

**Acceptance Scenarios**:

1. **Given** I run `/hefesto.create "skill" --cli claude`, **When** skill is created, **Then** only `.claude/skills/` contains the new skill
2. **Given** I run `/hefesto.create "skill" --cli claude,gemini,cursor`, **When** skill is created, **Then** exactly those 3 CLI directories contain the skill
3. **Given** I specify an invalid CLI name `--cli invalid`, **When** command executes, **Then** system shows error with list of detected CLIs
4. **Given** I specify a CLI not detected `--cli copilot` but Copilot not installed, **When** command executes, **Then** system warns and asks if user wants to create directory anyway

---

### User Story 4 - Detection Report and Visibility (Priority: P2)

As a developer, when detection completes, I see a report of which CLIs were found and where, so I understand what will happen before skill generation.

**Why this priority**: User confidence and transparency - important for UX but skill generation works without it.

**Independent Test**: Run `/hefesto.detect` and verify output shows all detected CLIs with paths and versions.

**Acceptance Scenarios**:

1. **Given** detection finds 3 CLIs, **When** report is displayed, **Then** each CLI shows: name, version, executable path, and config directory path
2. **Given** a CLI is in PATH but no config directory exists, **When** report is shown, **Then** CLI shows warning status indicating config dir will be created
3. **Given** detection completes, **When** report is displayed, **Then** summary shows "X out of 7 supported CLIs detected"
4. **Given** user runs `/hefesto.list`, **When** output is shown, **Then** CLI detection status is persisted from last detection run

---

### Edge Cases

- **What happens when CLI executable exists but is broken/non-functional?** - Detection marks CLI as "error" status with message, skill generation skips it
- **What happens when two CLIs share the same config directory?** - Detection picks first by priority order (defined in CLI detection matrix)
- **What happens when detection takes longer than 500ms?** - System shows progress indicator, continues detection, logs performance warning
- **What happens when creating directory fails due to permissions?** - System marks that CLI as failed, continues with others, reports permission errors at end
- **What happens when skill already exists in one CLI but not others?** - System handles as collision (idempotence check), prompts user for action per T0-HEFESTO-08
- **What happens when user cancels during parallel generation?** - System stops all in-progress generations, cleans up partial files, reports cancellation
- **What happens during sync when CLIs get out of sync?** - Out of scope for this feature - handled by separate `/hefesto.sync` command

---

## Requirements

### Functional Requirements

**CLI Detection**:

- **FR-001**: System MUST detect AI CLIs by checking for executables in system PATH within 500ms
- **FR-002**: System MUST detect AI CLIs by checking for existing config directories (`.claude/`, `.gemini/`, etc.)
- **FR-003**: System MUST combine results from both detection methods (PATH + config dirs) to determine available CLIs
- **FR-004**: System MUST check all 7 supported CLIs: Claude Code, Gemini CLI, OpenAI Codex, VS Code/Copilot, OpenCode, Cursor, Qwen Code
- **FR-005**: System MUST attempt to extract version information from each detected CLI executable
- **FR-006**: System MUST persist detection results to MEMORY.md for future reference

**Parallel Generation**:

- **FR-007**: System MUST generate skills for all detected CLIs simultaneously (parallel execution)
- **FR-008**: System MUST create CLI-specific directory structure (`.cli-name/skills/skill-name/`) if not exists
- **FR-009**: System MUST apply CLI-specific adaptations during generation (e.g., Gemini `{{args}}`, Copilot `.github/` structure)
- **FR-010**: System MUST validate each generated skill against Agent Skills spec before persistence
- **FR-011**: System MUST implement atomic rollback - if any CLI generation fails, all must be rolled back

**CLI Targeting**:

- **FR-012**: System MUST support `--cli` optional argument to restrict generation to specific CLIs
- **FR-013**: System MUST validate CLI names provided in `--cli` against detected CLIs
- **FR-014**: System MUST support comma-separated CLI names in `--cli` argument (e.g., `--cli claude,gemini`)
- **FR-015**: System MUST default to "all detected CLIs" when `--cli` argument is not provided

**Reporting**:

- **FR-016**: System MUST display detection report showing: CLI name, status (detected/not found), version, executable path, config directory
- **FR-017**: System MUST show generation progress for each CLI during parallel generation
- **FR-018**: System MUST report success/failure status for each CLI after generation completes
- **FR-019**: System MUST provide summary count of successful vs failed generations

**Error Handling**:

- **FR-020**: System MUST gracefully handle when no CLIs are detected (fallback to interactive mode)
- **FR-021**: System MUST handle permission errors when creating directories (mark CLI as failed, continue with others)
- **FR-022**: System MUST handle version extraction failures (mark version as "unknown", continue detection)
- **FR-023**: System MUST detect and report collisions (skill already exists) per T0-HEFESTO-08

**Compliance**:

- **FR-024**: System MUST follow T0-HEFESTO-04 (detect CLIs BEFORE asking user)
- **FR-025**: System MUST follow T0-HEFESTO-09 (ensure compatibility with all supported CLIs)
- **FR-026**: System MUST follow ADR-001 (use Agent Skills as primary format)
- **FR-027**: System MUST follow ADR-003 (use lightweight frontmatter with JIT metadata)
- **FR-028**: System MUST maintain skill semantic equivalence across all CLIs (same functionality, adapted syntax)

### Key Entities

- **CLI Detection Result**: Represents outcome of detecting one AI CLI
  - Name (e.g., "Claude Code")
  - Status (detected, not_found, error)
  - Version (e.g., "2.1.31" or "unknown")
  - Executable Path (e.g., "C:\Users\...\claude.exe")
  - Config Directory (e.g., ".claude/")
  - Detection Method (PATH, config_dir, both)
  - Priority (1-7, for conflict resolution)

- **CLI Adapter**: Defines CLI-specific transformations
  - Target CLI name
  - Variable syntax mapping (e.g., `$ARGUMENTS` → `{{args}}`)
  - Directory structure rules
  - Frontmatter additions/modifications
  - Validation rules

- **Generation Task**: Represents skill generation for one CLI
  - Target CLI
  - Skill name
  - Status (pending, in_progress, success, failed)
  - Error message (if failed)
  - Output paths

---

## Success Criteria

### Measurable Outcomes

- **SC-001**: CLI detection completes in under 500ms for systems with up to 7 CLIs installed
- **SC-002**: System achieves 100% detection accuracy (no false positives - never detects non-existent CLI)
- **SC-003**: Parallel generation completes 3x faster than sequential generation for 3+ CLIs
- **SC-004**: Zero cross-CLI skill inconsistencies - same skill in different CLIs has identical functionality
- **SC-005**: Rollback success rate of 100% - when one CLI fails, no partial files remain in any CLI directory
- **SC-006**: Users can create skills for multiple CLIs without manual configuration in 90% of use cases
- **SC-007**: Detection report provides sufficient information for users to understand CLI availability without consulting documentation

---

## Assumptions

- User has at least one supported AI CLI installed
- User has read/write permissions in project directory
- CLI executables respond to `--version` or `-v` flag for version extraction (fallback to "unknown" if not)
- Config directories follow standard naming convention (`.cli-name/`)
- System PATH is properly configured for installed CLI executables
- Network access not required (all detection is local)
- Detection runs on Windows, macOS, and Linux (cross-platform PATH resolution)
- Maximum supported CLIs: 7 (as defined in T0-HEFESTO-09 matrix)

---

## Scope

**In Scope**:
- Automatic detection of 7 supported AI CLIs
- Parallel skill generation for detected CLIs
- CLI-specific adaptations (syntax, structure)
- Selective targeting via `--cli` flag
- Detection reporting and status visibility
- Atomic rollback on failure
- Collision detection and handling

**Out of Scope**:
- Installation of AI CLIs (assumes pre-installed)
- CLI configuration or setup (assumes properly configured)
- Skill synchronization between CLIs (separate `/hefesto.sync` command)
- Custom CLI support beyond the 7 defined
- CLI version compatibility checks (assumes latest versions compatible)
- Network-based CLI detection or discovery
- CLI health monitoring or continuous detection

---

## Dependencies

**Internal**:
- CARD-001 (Foundation) - Required: directory structure, MEMORY.md persistence
- CARD-002 (Templates) - Required: adapter system, skill templates
- CARD-003 (Commands) - Optional: `/hefesto.create`, `/hefesto.list` integration

**External**:
- T0-HEFESTO-04 (Multi-CLI Detection)
- T0-HEFESTO-05 (Local Storage)
- T0-HEFESTO-09 (CLI Compatibility Matrix)
- ADR-001 (Agent Skills Standard)
- ADR-003 (Lightweight Frontmatter)

**Technical**:
- Cross-platform PATH resolution (Node.js `which` or equivalent)
- Filesystem permissions
- Parallel execution capability
