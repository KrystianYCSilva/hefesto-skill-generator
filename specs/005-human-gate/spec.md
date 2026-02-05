# Feature Specification: Human Gate + Wizard Mode

**Feature Branch**: `005-human-gate`  
**Created**: 2026-02-05  
**Status**: Draft  
**Input**: User description: "Implement CARD-005: Human Gate + Wizard - Interactive approval workflow with wizard mode for skill creation and extraction, following ADRs 001-003 and PLAN-001"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Mandatory Approval Before Persistence (Priority: P1)

As a **security-conscious developer**, I want the system to **always show me exactly what will be created and wait for my explicit approval** before writing any files, so that I have **complete control** over what gets persisted to my project.

**Why this priority**: This is the core safety mechanism (T0-HEFESTO-02) that prevents unwanted changes. Without this, the entire feature is unusable for production.

**Independent Test**: Can be fully tested by running `/hefesto.create "test skill"`, verifying the preview appears with file contents, and confirming nothing is written until approval is given. Delivers immediate value by preventing accidental file creation.

**Acceptance Scenarios**:

1. **Given** I run `/hefesto.create "validate email addresses"`, **When** skill is generated, **Then** I see a formatted preview showing exact file paths, exact file contents (with intelligent truncation after 50 lines), file sizes, target CLI directories
2. **Given** preview is displayed, **When** I choose `[reject]`, **Then** no files are created and I receive confirmation
3. **Given** preview is displayed, **When** I choose `[approve]`, **Then** files are created exactly as shown in preview
4. **Given** preview is displayed, **When** I wait 5 minutes without responding, **Then** operation is automatically cancelled with timeout message

---

### User Story 2 - Guided Skill Creation via Wizard (Priority: P2)

As a **first-time user**, I want a **step-by-step wizard** that guides me through creating a skill when I don't provide all required information, so that I can **create valid skills without memorizing syntax**.

**Why this priority**: Essential for user onboarding and reducing friction. Users shouldn't need to know the entire Agent Skills spec to create their first skill.

**Independent Test**: Can be tested by running `/hefesto.create` (without description). Wizard activates, walks user through all steps, and produces valid skill. Delivers value by making skill creation accessible to beginners.

**Acceptance Scenarios**:

1. **Given** I run `/hefesto.create` without description, **When** wizard starts, **Then** I am prompted step-by-step for: skill name, description, main instructions, optional JIT resources
2. **Given** I'm in wizard step 2, **When** I type `back`, **Then** I return to step 1 with previous input preserved
3. **Given** I provide invalid skill name (uppercase), **When** wizard validates, **Then** name is auto-sanitized to lowercase-hyphenated format (T0-HEFESTO-07)
4. **Given** I complete all wizard steps, **When** final review displays, **Then** I see complete preview and same approval options as manual creation

---

### User Story 3 - Expandable JIT Resources (Priority: P2)

As a **power user**, I want to **iteratively add optional resources** (scripts, references, assets) to my skill during the approval process, so that I can **start simple and expand as needed** without recreating the skill.

**Why this priority**: Supports Progressive Disclosure (T0-HEFESTO-03). Users can create minimal skills quickly and expand later.

**Independent Test**: Create basic skill, choose `[expand]` at Human Gate, add script resource, verify it appears in final skill structure. Delivers value by allowing incremental complexity.

**Acceptance Scenarios**:

1. **Given** skill preview is shown, **When** I choose `[expand]`, **Then** I'm prompted: "Add optional resources? [scripts] [references] [assets] [done]"
2. **Given** I choose `[scripts]`, **When** prompted, **Then** I can specify script filenames and content
3. **Given** resources are added, **When** I choose `[done]`, **Then** updated preview shows new directory structure with added resources
4. **Given** expanded preview is shown, **When** I choose `[approve]`, **Then** all resources are created atomically

---

### User Story 4 - Collision Handling (Priority: P2)

As a **developer improving existing skills**, I want to be **prompted when a skill name already exists** with options to overwrite (with backup), merge, or cancel, so that I don't **accidentally lose work**.

**Why this priority**: Prevents data loss and supports iterative improvement. Critical for production use where skills are updated over time.

**Independent Test**: Create skill "test-skill", then attempt to create another with same name. Verify collision detection triggers with clear options. Delivers value by protecting existing work.

**Acceptance Scenarios**:

1. **Given** skill "validate-email" exists, **When** I create new skill with same name, **Then** system detects collision and shows: `[overwrite]` `[merge]` `[cancel]`
2. **Given** collision detected, **When** I choose `[overwrite]`, **Then** existing skill is backed up to `.hefesto/backups/{name}-{timestamp}.tar.gz` before replacement
3. **Given** collision detected, **When** I choose `[merge]`, **Then** I'm shown diff and can selectively merge changes
4. **Given** collision detected, **When** I choose `[cancel]`, **Then** operation aborts with confirmation message

---

### User Story 5 - Inline Editing (Priority: P3)

As an **advanced user**, I want to **edit the generated skill inline** before approval, so that I can **make quick adjustments without restarting** the creation process.

**Why this priority**: Nice-to-have for power users. Most users will use wizard or approve as-is. Lower priority than core safety and wizard features.

**Independent Test**: Generate skill, choose `[edit]`, modify content, verify changes appear in re-validation and final preview. Delivers value by reducing iteration time.

**Acceptance Scenarios**:

1. **Given** skill preview is shown, **When** I choose `[edit]`, **Then** skill content opens in interactive editor
2. **Given** I edit skill content, **When** I save and close editor, **Then** modified content is re-validated against Agent Skills spec
3. **Given** edited content passes validation, **When** I confirm, **Then** updated preview shows my changes
4. **Given** edited content fails validation, **When** validation runs, **Then** I see specific error messages with option to retry edit

---

### Edge Cases

- **What happens when timeout occurs during wizard?** → Wizard saves current progress to temporary file with path displayed, allowing user to resume or reference later.
- **What happens when user provides empty description in wizard?** → System prompts again with error message (max 3 attempts), then aborts with helpful guidance.
- **What happens when skill validation fails after Human Gate approval?** → This should never occur (validation happens before Human Gate), but if it does, operation aborts and files are not created (defensive programming).
- **What happens when multiple CLIs are targeted and one fails to write?** → Atomic rollback: all created files across all CLIs are removed, backup is restored if overwrite was chosen.
- **What happens when backup creation fails during overwrite?** → Overwrite is aborted with error message, original skill remains intact.
- **What happens when user's input contains shell injection characters during wizard?** → Input is sanitized and validated (T0-HEFESTO-11) before any processing. Malicious patterns are rejected with security warning.

## Requirements *(mandatory)*

### Functional Requirements

#### Core Human Gate (P1)

- **FR-001**: System MUST generate all skill content in memory before displaying to user (no filesystem writes until approval)
- **FR-002**: System MUST validate generated skill against Agent Skills spec (T0-HEFESTO-06) before showing Human Gate
- **FR-003**: System MUST display formatted preview showing: exact file paths, exact file contents (with intelligent truncation after 50 lines), file sizes, target CLI directories
- **FR-004**: System MUST offer exactly four options at Human Gate: `[approve]` `[expand]` `[edit]` `[reject]`
- **FR-005**: System MUST implement 5-minute timeout for Human Gate response, automatically cancelling operation if exceeded
- **FR-006**: System MUST persist files atomically only after `[approve]` confirmation (all files succeed or all fail)
- **FR-007**: System MUST display confirmation message after successful persistence showing all created file paths

#### Wizard Mode (P2)

- **FR-008**: System MUST activate Wizard Mode when `/hefesto.create` is invoked without description argument
- **FR-009**: System MUST activate Wizard Mode when `/hefesto.extract` is invoked without file path argument
- **FR-010**: Wizard MUST collect inputs step-by-step: (1) skill name, (2) description, (3) main instructions, (4) optional JIT resources
- **FR-011**: Wizard MUST validate each input against T0 rules before proceeding to next step (T0-HEFESTO-07 for name, max 1024 chars for description)
- **FR-012**: Wizard MUST support `back` command to return to previous step with inputs preserved
- **FR-013**: Wizard MUST auto-sanitize skill names to conform to T0-HEFESTO-07 (lowercase, hyphens, max 64 chars)
- **FR-014**: Wizard MUST display final review showing all collected inputs before proceeding to Human Gate

#### JIT Resource Expansion (P2)

- **FR-015**: System MUST support `[expand]` option at Human Gate to iteratively add optional resources
- **FR-016**: Expansion mode MUST offer resource types: `[scripts]` `[references]` `[assets]` `[done]`
- **FR-017**: For each resource type, system MUST prompt for filename and content/path
- **FR-018**: System MUST update preview after each resource addition showing new directory structure
- **FR-019**: System MUST allow multiple resources of same type (e.g., multiple scripts)

#### Collision Detection (P2)

- **FR-020**: System MUST detect if skill with same name already exists in any target CLI directory before Human Gate
- **FR-021**: If collision detected, system MUST display existing skill metadata: created date, last modified, author, version
- **FR-022**: System MUST offer collision resolution options: `[overwrite]` `[merge]` `[cancel]`
- **FR-023**: For `[overwrite]`, system MUST create backup at `.hefesto/backups/{skill-name}-{ISO8601-timestamp}.tar.gz` before deletion
- **FR-024**: For `[merge]`, system MUST display unified diff and allow selective merge of sections
- **FR-025**: For `[cancel]`, system MUST abort operation and preserve existing skill intact

#### Inline Editing (P3)

- **FR-026**: System MUST support `[edit]` option at Human Gate to modify generated content
- **FR-027**: Edit mode MUST open skill content in user's default editor (from $EDITOR environment variable)
- **FR-028**: After edit, system MUST re-validate modified content against Agent Skills spec
- **FR-029**: If validation fails, system MUST display errors and offer: `[retry-edit]` `[discard-changes]` `[abort]`
- **FR-030**: If validation passes, system MUST display updated preview with edited content

#### Security & Safety

- **FR-031**: System MUST sanitize all user inputs against injection patterns (shell, prompt, SQL) per T0-HEFESTO-11
- **FR-032**: System MUST enforce idempotence (T0-HEFESTO-08): same inputs produce same outputs
- **FR-033**: System MUST maintain operation log for audit trail (creation timestamp, user, choices made)
- **FR-034**: System MUST never execute user-provided scripts during validation or preview

### Key Entities

- **Preview Object**: Represents in-memory skill before persistence
  - Attributes: skill_name, skill_content, metadata, target_clis, validation_status, timestamp
  - Relationships: Contains validation_errors (if any), references target file paths

- **Wizard State**: Maintains wizard progress across steps
  - Attributes: current_step, collected_inputs, visited_steps, start_timestamp
  - Relationships: Can be serialized to temporary file on timeout/interrupt

- **Collision Info**: Metadata about existing skill when collision detected
  - Attributes: existing_skill_name, created_date, modified_date, author, version, file_paths
  - Relationships: References backup_path if overwrite chosen

- **Expansion Request**: Tracks JIT resources being added
  - Attributes: resource_type (scripts/references/assets), filename, content/path
  - Relationships: Belongs to Preview Object

- **Human Gate Decision**: Records user choice at approval gate
  - Attributes: decision (approve/expand/edit/reject), timestamp, response_time, preview_id
  - Relationships: Triggers corresponding action handler

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of write operations (file creation, modification, deletion) require Human Gate approval with no bypass mechanism
- **SC-002**: Users can complete wizard-guided skill creation in under 5 minutes for simple skills (3 steps: name, description, approve)
- **SC-003**: Preview displays complete in under 2 seconds for skills up to 500 lines (T0-HEFESTO-03 limit)
- **SC-004**: Collision detection identifies 100% of existing skills before Human Gate presentation
- **SC-005**: Backup creation succeeds in 100% of overwrite scenarios, or overwrite is aborted
- **SC-006**: Validation rejection rate (skills failing T0 rules) decreases to below 5% when using Wizard Mode (compared to manual creation)
- **SC-007**: Human Gate timeout (5 minutes) triggers correctly in 100% of cases when user is unresponsive
- **SC-008**: Users successfully recover from timeout/interrupt in 100% of cases via temporary file persistence
- **SC-009**: 95% of users successfully complete their first skill creation using Wizard Mode without external help
- **SC-010**: Zero data loss events: existing skills are never overwritten without confirmed backup creation

### Qualitative Outcomes

- **SC-011**: Users report feeling "in control" of what Hefesto creates (measured via feedback survey)
- **SC-012**: Support tickets related to "unwanted file creation" reduce to zero
- **SC-013**: New users successfully create first skill within first session (no abandonment)

## Assumptions *(mandatory)*

1. **Terminal Capabilities**: User's terminal supports ANSI color codes for formatted preview display (fallback to plain text if not)
2. **Editor Availability**: For inline editing, user has $EDITOR environment variable set or system default editor (vim/nano on Linux, notepad on Windows)
3. **Filesystem Permissions**: User has write permissions to project directory and backup directory
4. **Session Persistence**: Terminal session remains active during wizard and Human Gate operations (timeout handles interruptions)
5. **CLI Detection**: At least one AI CLI is detected in system before Human Gate is reached (validation in Phase 0 of `/hefesto.create`)

## Out of Scope

- **Diff Visualization for Merge**: While merge option is specified (FR-024), full visual diff with syntax highlighting is deferred to future release (v1.1). Initial implementation shows unified diff text only.
- **Collaborative Approval**: Multi-user approval workflows (e.g., skill creation requires team lead approval) not included in v1.0
- **Approval History UI**: While audit log is created (FR-033), no dashboard or search UI for viewing historical approvals in v1.0
- **Custom Timeout Configuration**: 5-minute timeout is hardcoded. User-configurable timeout deferred to v1.1
- **Resumable Wizard from Backup**: Wizard saves progress on timeout, but automatic resume from backup requires manual command (not auto-suggested in v1.0)

## Dependencies

- **CARD-001** (Foundation): Must be complete for CLI detection and directory structure
- **CARD-002** (Templates): Must be complete for skill generation and validation
- **CARD-003** (Commands): Must be complete for `/hefesto.create` and `/hefesto.extract` integration points
- **ADR-001** (Agent Skills Standard): Validation rules derived from this standard
- **ADR-002** (Research Integration): Security validation (T0-HEFESTO-11) requirements
- **ADR-003** (Lightweight Frontmatter): JIT resource structure (scripts/, references/, assets/)

## Technical Constraints

- **No Implementation Details**: This spec intentionally avoids specifying HOW to implement (e.g., "use readline library" or "implement with Python") - only WHAT the system must do
- **Terminal-Based UI**: All interactions must work in text-based terminal (no GUI requirements)
- **Cross-Platform**: Must work on Windows (PowerShell), macOS/Linux (Bash) without modification
- **Atomic Operations**: All multi-file operations (multi-CLI generation) must be atomic (all succeed or all fail with rollback)

## Open Questions

[NEEDS CLARIFICATION: Merge Strategy for Conflicting Sections]

**Context**: FR-024 requires merge capability when skill collision occurs. Current spec says "display unified diff and allow selective merge of sections."

**What we need to know**: Should the merge be:

| Option | Answer | Implications |
| ------ | ------ | ------------ |
| A | Manual text selection (user edits combined file) | Simpler implementation, requires user to resolve conflicts manually like git merge |
| B | Three-way merge with conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) | Familiar to developers, automated conflict detection, but complex for non-technical users |
| C | Section-by-section approval (show each changed section, ask keep/replace) | User-friendly for non-developers, but potentially many prompts for large skills |

**Your choice**: _Option C is recommended for v1.0 (aligns with wizard UX pattern), with Option B as enhancement in v1.1_

---

[NEEDS CLARIFICATION: Preview Truncation Strategy]

**Context**: FR-003 specifies "intelligent truncation after 50 lines" for preview display.

**What we need to know**: For skills exceeding 50 lines, what should truncation show?

| Option | Answer | Implications |
| ------ | ------ | ------------ |
| A | First 50 lines only (with "... truncated" note) | Simple, predictable, but user doesn't see end of file |
| B | First 25 lines + last 25 lines (with "... [X lines hidden] ..." in middle) | Shows both beginning and end, but might miss important middle sections |
| C | Smart truncation (frontmatter + section headers + first few lines of each section) | Most informative, but requires markdown parsing and more complex logic |

**Your choice**: _Option B is recommended for v1.0 (balance of simplicity and usefulness), with Option C as v1.1 enhancement_

---

[NEEDS CLARIFICATION: Wizard Interrupt Recovery]

**Context**: Edge case specifies wizard saves progress on timeout/interrupt.

**What we need to know**: When user returns after interrupt, how should recovery work?

| Option | Answer | Implications |
| ------ | ------ | ------------ |
| A | Auto-detect interrupted session on next command and prompt to resume | Seamless UX, but requires session tracking and auto-detection logic |
| B | Explicit resume command: `/hefesto.resume` with saved state path | User must remember to resume, but simpler implementation |
| C | Save to named temp file, show path in timeout message, user manually copies content | No special resume logic needed, but manual and error-prone |

**Your choice**: _Option B is recommended for v1.0 (clear and simple), with Option A as v1.1 enhancement for better UX_

---

**End of Specification**
