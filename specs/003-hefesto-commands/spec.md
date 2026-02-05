# Feature Specification: Hefesto Commands

**Feature Branch**: `003-hefesto-commands`
**Created**: 2026-02-04
**Status**: Draft
**Input**: User description: "CARD-003-commands.md implementation based on PLAN-001 and research"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Core Skill Creation & Extraction (Priority: P1)

As a skill developer, I want to create new skills from descriptions or extract them from existing code using `/hefesto.create` and `/hefesto.extract`, so that I can rapidly build my skill library.

**Why this priority**: These are the primary generative capabilities of the system. Without them, users cannot create content.

**Independent Test**:
1. Run `/hefesto.create` with a description argument. Verify a valid skill template is generated and persisted after approval.
2. Run `/hefesto.extract` pointing to a code file. Verify a skill is generated wrapping that code.

**Acceptance Scenarios**:

1. **Given** a user input `/hefesto.create "Validate email regex"`, **When** the command executes, **Then** the agent generates a skill based on the template, triggers the Human Gate for approval, and persists it to the correct CLI directory.
2. **Given** a user input `/hefesto.extract ./utils/validator.py`, **When** the command executes, **Then** the agent analyzes the code, generates a wrapper skill, triggers the Human Gate, and persists it.
3. **Given** `/hefesto.create` without arguments, **When** executed, **Then** it enters "Wizard Mode" asking strictly necessary questions interactively.

---

### User Story 2 - Validation & Listing (Priority: P1)

As a skill developer, I want to list available skills and validate their integrity using `/hefesto.list` and `/hefesto.validate`, so that I can manage my library and ensure compliance.

**Why this priority**: Users need visibility into what they have created and confidence that it works.

**Independent Test**:
1. Create an invalid skill (manually). Run `/hefesto.validate`. Verify error reporting.
2. Run `/hefesto.list`. Verify it displays all detected skills across CLIs.

**Acceptance Scenarios**:

1. **Given** a set of skills in `.claude/skills` and `.gemini/skills`, **When** `/hefesto.list` is run, **Then** a formatted table of all skills, versions, and target CLIs is displayed.
2. **Given** a skill violating T0 rules (e.g., uppercase name), **When** `/hefesto.validate <skill>` is run, **Then** specific error messages with remediation suggestions are shown.

---

### User Story 3 - Adaptation & Sync (Priority: P2)

As a user of multiple AI tools, I want to adapt skills from one CLI to another and keep them synchronized using `/hefesto.adapt` and `/hefesto.sync`.

**Why this priority**: Enables the "Write Once, Run Anywhere" value proposition.

**Independent Test**:
1. Create a skill for Claude. Run `/hefesto.adapt <skill> --target gemini`. Verify a Gemini-compatible version is created.

**Acceptance Scenarios**:

1. **Given** a valid Claude skill, **When** `/hefesto.adapt skill-name --target gemini` is run, **Then** the system uses the Gemini adapter to create a compliant copy in the Gemini skills directory.
2. **Given** updated templates, **When** `/hefesto.sync` is run, **Then** all skills are checked against their templates and updates are proposed via Human Gate.

---

### User Story 4 - Management & Help (Priority: P2)

As a user, I want to view details of specific skills, delete unwanted ones, and access help documentation using `/hefesto.show`, `/hefesto.delete`, and `/hefesto.help`.

**Why this priority**: Essential CRUD and usability features.

**Independent Test**:
1. Run `/hefesto.show <skill>`. Verify content display.
2. Run `/hefesto.delete <skill>`. Verify Human Gate confirmation and file removal.

**Acceptance Scenarios**:

1. **Given** a skill exists, **When** `/hefesto.delete skill-name` is invoked, **Then** a confirmation prompt (Human Gate) appears before deletion.
2. **Given** any context, **When** `/hefesto.help` is called, **Then** a list of all available commands and their usage examples is displayed.

---

### Edge Cases

- **Invalid Arguments**: Commands must handle missing or malformed arguments gracefully with standardized error format:
  ```
  ERROR [E-{COMMAND}-{CODE}]: {Description}
  Suggestion: {Remediation action}
  Usage: /hefesto.{command} {syntax}
  ```
  Example: `ERROR [E-CREATE-001]: Description exceeds 2000 characters. Suggestion: Shorten description and try again. Usage: /hefesto.create "description"`
- **Permission Denied**: If the agent cannot write to a directory, clear error messages must be shown.
- **Interruption**: If a Wizard mode session is interrupted (user cancels, timeout, or error), the system MUST:
  1. Discard all in-memory state immediately
  2. NOT persist any partial artifacts to filesystem
  3. NOT modify MEMORY.md
  4. Display: "Operation cancelled. No changes made."
  
  Wizard timeout: 300 seconds (5 minutes) of inactivity triggers automatic cleanup.
- **Name Collisions**: Creating a skill that already exists should prompt for overwrite (Human Gate).

## Clarifications

### Session 2026-02-04

- Q: How should the system handle name collisions when creating or extracting a skill that already exists? → A: Prompt for overwrite via Human Gate (yes/no/rename)
- Q: How should users update existing skills when the underlying templates change? → A: Use `sync` command to update existing skills to latest template version
- Q: What should happen when `/hefesto.extract` is run without any arguments? → A: Enter interactive mode
- Q: How should command arguments be parsed? → A: Positional arguments for primary inputs, flags for options
- Q: What is the exact scope of `/hefesto.show`? → A: Show content of one specific skill

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement 9 distinct commands: create, extract, validate, adapt, sync, list, show, delete, help. Note: list and help already exist from Feature 001; 7 new commands required.
- **FR-002**: All "write" commands (create, extract, adapt, sync, delete) MUST enforce Human Gate (T0-HEFESTO-02) before filesystem changes. Standard Human Gate options: [approve], [reject]. For name collision scenarios (see FR-008), add [rename] option.
- **FR-003**: `/hefesto.create` and `/hefesto.extract` MUST support both argument-based execution and interactive "Wizard Mode" if arguments are missing (entering interactive mode automatically).
- **FR-004**: `/hefesto.validate` MUST check skills against the Agent Skills specification and T0 rules using the `template-validator` helper.
- **FR-005**: `/hefesto.list` MUST aggregate skills from all detected CLI directories defined in MEMORY.md.
- **FR-006**: `/hefesto.help` MUST be always available and context-aware (showing help for specific subcommands if requested).
- **FR-008**: System MUST detect name collisions during creation/extraction and trigger Human Gate (FR-002) with extended options: [approve] (overwrite), [rename], [cancel]. Collision detection occurs before validation to prevent wasted processing.
- **FR-009**: `/hefesto.sync` MUST identify skills using outdated templates and propose updates to bring them to the latest version.
- **FR-010**: Command parsing MUST support positional arguments for primary inputs (e.g., skill name) and flags for options (e.g., `--target`), falling back to Wizard Mode if required positionals are missing.
- **FR-011**: `/hefesto.show` MUST accept a skill name as a positional argument and display the full content of that specific skill (metadata + body).

### Key Entities

- **Command**: A Markdown definition file in `commands/` that defines the prompt and logic for an operation.
- **Wizard**: An interactive prompt flow defined within the command to gather missing information.
- **Human Gate**: A blocking verification step (implemented in `helpers/human-gate.md`) required for side-effects.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of the 8 specified commands are implemented and executable.
- **SC-002**: Read commands (`list`, `show`, `validate`, `help`) execute in under 2 seconds.
- **SC-003**: Human Gate is triggered 100% of the time for write operations (`create`, `extract`, `adapt`, `sync`, `delete`).
- **SC-004**: Wizard mode activates automatically (entering interactive mode) when required arguments are missing for `create` and `extract`.
- **SC-005**: All commands have embedded documentation accessible via `/hefesto.help`.

