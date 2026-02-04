# Feature Specification: Hefesto Foundation Infrastructure

**Feature Branch**: `001-hefesto-foundation`  
**Created**: 2026-02-04  
**Status**: Draft  
**Input**: User description: "@docs\cards\CARD-001-foundation.md para implementação do @docs\plan\PLAN-001-hefesto-v1.md e seguindo as adrs @docs\decisions/"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Bootstrap Hefesto in Existing Project (Priority: P1)

As a developer using AI CLI tools, I want to initialize the Hefesto Skill Generator infrastructure in my existing project so that I can immediately start generating standardized Agent Skills for any supported CLI without manual setup.

**Why this priority**: This is the foundational capability that enables all other Hefesto features. Without initialization, no skill generation can occur.

**Independent Test**: Can be fully tested by running the initialization command in a fresh project directory and verifying the directory structure, configuration files, and command availability without requiring any skill generation.

**Acceptance Scenarios**:

1. **Given** a project directory without Hefesto, **When** I run the bootstrap command, **Then** all CLI detection occurs automatically and directory structures are created only for detected CLIs
2. **Given** multiple AI CLIs installed on my system, **When** initialization completes, **Then** I see a report showing which CLIs were detected and where skills will be stored
3. **Given** Hefesto is initialized, **When** I invoke any `/hefesto.*` command, **Then** the command executes successfully and references the local CONSTITUTION.md

---

### User Story 2 - Detect Installed AI CLIs Automatically (Priority: P1)

As a developer, I want Hefesto to automatically detect which AI CLIs are installed on my system so that I don't have to manually configure which tools I'm using or create directory structures I don't need.

**Why this priority**: Prevents user friction and ensures skills are generated only for tools the user actually has, avoiding clutter and confusion.

**Independent Test**: Can be tested by installing/uninstalling different CLIs and running detection, verifying correct identification without requiring full initialization or skill generation.

**Acceptance Scenarios**:

1. **Given** Claude Code is installed, **When** detection runs, **Then** the system identifies it via PATH check and creates `.claude/skills/` directory
2. **Given** no AI CLIs are installed, **When** detection runs, **Then** the system prompts the user to specify at least one CLI manually
3. **Given** Gemini CLI has a `.gemini/` config directory but is not in PATH, **When** detection runs, **Then** the system still identifies it and prepares appropriate structure

---

### User Story 3 - Persist Project State Across Sessions (Priority: P2)

As a developer working across multiple coding sessions, I want Hefesto to remember the state of my skills and configuration so that I don't lose context between sessions and can track what skills exist in my project.

**Why this priority**: Enables stateful operation and prevents regeneration or conflicts, but the system can function for single-session use without this.

**Independent Test**: Can be tested by initializing Hefesto, generating a skill, closing the session, reopening, and verifying the system still knows about the skill without re-scanning the filesystem.

**Acceptance Scenarios**:

1. **Given** I have generated 3 skills in a previous session, **When** I start a new session and run `/hefesto.list`, **Then** all 3 skills are displayed without filesystem scanning
2. **Given** MEMORY.md tracks skill state, **When** I manually delete a skill directory, **Then** the next command execution detects the inconsistency and updates MEMORY.md
3. **Given** the project is cloned to a new machine, **When** Hefesto initializes, **Then** MEMORY.md is recognized and state is restored

---

### User Story 4 - Enforce Constitutional Governance from Start (Priority: P2)

As a project stakeholder, I want the CONSTITUTION.md to be immutable and enforced from the moment Hefesto is initialized so that all skill generation operations adhere to established T0 rules without requiring manual verification.

**Why this priority**: Ensures governance and quality from day one, but the foundation can technically function without deep constitutional enforcement until skills are generated.

**Independent Test**: Can be tested by attempting to modify CONSTITUTION.md or generate a non-compliant skill structure immediately after initialization and verifying the system blocks or warns appropriately.

**Acceptance Scenarios**:

1. **Given** Hefesto is initialized with CONSTITUTION.md, **When** I attempt to generate a skill with an invalid name (uppercase, special chars), **Then** the operation is rejected with a reference to T0-HEFESTO-04
2. **Given** CONSTITUTION.md exists, **When** any `/hefesto.*` command loads, **Then** the system validates against T0 rules before proceeding
3. **Given** a skill violates T0-HEFESTO-03 (>500 lines), **When** I attempt to persist it, **Then** the Human Gate blocks persistence and suggests moving content to references/

---

### Edge Cases

- When a CLI is detected via PATH but its config directory doesn't exist yet, the system creates the skills directory structure normally, as the executable presence is sufficient for skill generation
- When a CLI config directory exists but the CLI is not in PATH, the system creates the directory structure anyway (indicating prior user activity) but includes a warning in the detection report that the CLI executable was not found in PATH
- When permission errors occur creating skill directories (e.g., read-only filesystem), the system skips the problematic CLI, logs the error with specific path and permission details, continues initializing other CLIs, and presents a summary report of all failures at completion
- When MEMORY.md is corrupted or contains invalid state data, the system backs up the corrupted file with timestamp suffix (e.g., MEMORY.md.backup.2026-02-04T14-30-00), creates a fresh MEMORY.md, and rescans the filesystem to rebuild state from existing skill directories
- When CLIs are installed after Hefesto initialization, they are not automatically detected; users must manually trigger re-detection using a command (e.g., `/hefesto.detect` or `/hefesto.init --detect`) to add newly installed CLIs and create their directory structures
- When CONSTITUTION.md is manually deleted or modified outside Hefesto, the system detects this on every command execution: if missing, it automatically restores from the bundled copy; if modified externally, it validates the structure and blocks all operations if T0 rules are violated or missing
- How does the system handle projects with multiple Git worktrees or submodules?

## Clarifications

### Session 2026-02-04

- Q: When MEMORY.md is corrupted or contains invalid state data, what recovery strategy should the system use? → A: Back up corrupted MEMORY.md with timestamp suffix, create fresh MEMORY.md, and rescan filesystem to rebuild state
- Q: When the system encounters permission errors creating skill directories, what should it do? → A: Skip the problematic CLI, log the error with the specific path and permission issue, continue with other CLIs, and report all failures at the end
- Q: When CLIs are installed after Hefesto initialization, how should the system detect them? → A: Require manual re-detection via a command like `/hefesto.init --detect` or `/hefesto.detect` to add new CLIs
- Q: When CONSTITUTION.md is manually deleted or modified outside Hefesto, how should the system respond? → A: Detect on every command execution; if missing, restore from bundled copy; if modified externally, validate structure and block operations if T0 rules are violated or missing
- Q: When a CLI is detected via config directory but not in PATH, what should the system do? → A: Create the directory structure anyway (user has config, indicating prior use) but warn that CLI executable not found in PATH

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST automatically detect AI CLIs via PATH environment variable and config directory existence checks
- **FR-002**: System MUST create directory structures only for detected CLIs following the pattern `.<cli-name>/skills/`
- **FR-003**: System MUST copy CONSTITUTION.md to the project root if not already present
- **FR-004**: System MUST initialize MEMORY.md with an empty state structure if not already present
- **FR-005**: System MUST register all `/hefesto.*` commands and make them available to the AI agent
- **FR-006**: Detection MUST check for the following CLIs in order: Claude Code, Gemini CLI, OpenAI Codex, VS Code/Copilot, OpenCode, Cursor, Qwen Code
- **FR-007**: System MUST support offline operation after initial bootstrap (no network calls required for structure creation)
- **FR-008**: System MUST complete bootstrap process in under 5 seconds for typical projects
- **FR-009**: System MUST be idempotent - running bootstrap multiple times on the same project should not create duplicate structures or corrupt state
- **FR-010**: System MUST validate CONSTITUTION.md structure and T0 rules on every command execution; if missing, restore from bundled copy; if modified externally, validate and block operations if T0 rules are violated or missing
- **FR-011**: MEMORY.md MUST track: list of detected CLIs, created skill names, last update timestamp, Hefesto version
- **FR-012**: System MUST provide a detection report showing which CLIs were found and via what method (PATH vs config directory), including warnings for CLIs detected via config directory but not found in PATH
- **FR-013**: System MUST handle the case where no CLIs are detected by prompting for manual specification with a list of supported options
- **FR-014**: System MUST create skill directories with appropriate permissions (readable/writable by current user)
- **FR-015**: System MUST be compatible with Git repositories (all created files under 100KB, appropriate .gitignore suggestions)
- **FR-016**: System MUST handle corrupted MEMORY.md by backing it up with timestamp suffix, creating fresh MEMORY.md, and rescanning filesystem to rebuild state
- **FR-017**: System MUST handle permission errors gracefully by skipping the problematic CLI, logging the error with path and permission details, continuing with remaining CLIs, and reporting all failures in the final summary
- **FR-018**: System MUST provide a manual re-detection command (e.g., `/hefesto.detect`) to detect and initialize newly installed CLIs after initial bootstrap
- **FR-019**: System MUST create directory structures for CLIs detected via config directory even when not in PATH, treating config presence as indication of prior use

### Key Entities *(include if feature involves data)*

- **CLI Detection Result**: Represents a detected AI CLI with attributes: name (string), detection method (PATH | config_directory | manual), version (string | null), skills directory path (string)
- **Project State**: Represents persistent state in MEMORY.md with attributes: detected CLIs (list), initialized timestamp (ISO 8601), Hefesto version (semver), skill registry (list of skill names)
- **Constitutional Rule**: Represents a T0 governance rule with attributes: rule ID (e.g., T0-HEFESTO-01), description (string), enforcement level (ABSOLUTE | NORMATIVE | INFORMATIVE)
- **Skill Directory**: Represents a CLI-specific skills location with attributes: CLI name, absolute path, created timestamp, skill count

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developers can bootstrap Hefesto in a new project in under 10 seconds from command invocation to completion message
- **SC-002**: CLI detection accurately identifies 100% of installed supported CLIs without false negatives
- **SC-003**: Bootstrap process completes successfully in 95%+ of standard project environments (Windows, macOS, Linux) without manual intervention
- **SC-004**: Generated directory structures are recognized by all 7 supported AI CLIs without configuration changes
- **SC-005**: MEMORY.md state remains consistent across 100+ command executions without corruption
- **SC-006**: Constitutional violations are caught and blocked in 100% of test cases before filesystem persistence
- **SC-007**: Bootstrap operation uses less than 50MB of disk space for all configuration files and structures combined
- **SC-008**: All bootstrap operations complete offline after initial Hefesto installation (0 network requests)
- **SC-009**: Repeated bootstrap operations on the same project are idempotent with 0 duplicate directories or state corruption

### Assumptions

- Users have at least read/write permissions in the project directory where Hefesto is being initialized
- At least one supported AI CLI is either installed in PATH or has created a config directory in standard locations
- The project uses Git or another version control system (for .gitignore compatibility)
- Users are running on Windows, macOS, or Linux operating systems
- Project directory has at least 100MB free disk space for skill storage growth
- Standard shell environment variables (PATH, HOME, etc.) are correctly configured

## References

- **CARD-001**: Foundation - Estrutura Base (source specification)
- **PLAN-001**: Hefesto Skill Generator v1.0 implementation plan
- **ADR-001**: Agent Skills Standard adoption decision
- **ADR-002**: Security integration (T0-HEFESTO-11) and research foundation
- **ADR-003**: Lightweight frontmatter with JIT metadata loading
- **T0-HEFESTO-01**: Agent Skills spec compliance requirement
- **T0-HEFESTO-04**: Multi-CLI automatic detection requirement
- **T0-HEFESTO-05**: Local project storage requirement
- **Agent Skills Specification**: https://agentskills.io
