# Feature Specification: Update Feature Spec to v2.2.0

**Feature Branch**: `003-update-feature-spec`  
**Created**: 2026-02-08  
**Status**: Draft  
**Input**: User description: "com base no card @docs/cards/CARD-003-v2.2.0-features.md"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - Create Skill (Priority: P1)

As a developer, I want to create a new Agent Skill from a description, so that I can extend my AI assistant's capabilities.

**Why this priority**: Core functionality of the tool.

**Independent Test**: Execute `/hefesto.create "Validate email addresses"` and verify a new skill directory is created with `SKILL.md`.

**Acceptance Scenarios**:

1. **Given** no existing skill named "validate-email", **When** running `/hefesto.create "Validate email addresses"`, **Then** generate a skill structure in all detected CLI directories.
2. **Given** an existing skill, **When** running `/hefesto.create` with the same name, **Then** prompt for overwrite/rename/skip.

---

### User Story 2 - Extract Skill (Priority: P2)

As a developer, I want to extract a skill from existing code or documentation, so that I can reuse knowledge without manual rewriting.

**Why this priority**: Key differentiator for leveraging existing assets.

**Independent Test**: Execute `/hefesto.extract src/utils.ts` and verify a skill is generated reflecting the code's logic.

**Acceptance Scenarios**:

1. **Given** a valid source file, **When** running `/hefesto.extract`, **Then** analyze content and generate a compliant `SKILL.md`.
2. **Given** a directory, **When** running `/hefesto.extract`, **Then** synthesize patterns from multiple files.

---

### User Story 3 - Validate Skill (Priority: P3)

As a developer, I want to validate and fix my skills, so that they comply with the Agent Skills specification.

**Why this priority**: Quality assurance and maintenance.

**Independent Test**: Run `/hefesto.validate my-skill` on a non-compliant skill and see fix suggestions.

**Acceptance Scenarios**:

1. **Given** a skill with errors, **When** running `/hefesto.validate`, **Then** report errors and offer `[fix-auto]`.
2. **Given** a valid skill, **When** running `/hefesto.validate`, **Then** report `PASS`.

---

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST implement `/hefesto.create` command handling natural language descriptions.
- **FR-002**: System MUST implement `/hefesto.extract` command supporting file and directory inputs.  
- **FR-003**: System MUST implement `/hefesto.validate` command with 13-point quality checklist.
- **FR-004**: System MUST implement `/hefesto.adapt` command for converting skills between CLIs.
- **FR-005**: System MUST implement `/hefesto.list` command to show installed skills.
- **FR-006**: System MUST implement `/hefesto.init` for bootstrapping the environment.
- **FR-007**: System MUST support Human Gate workflow (approve/reject) for all write operations.

### Key Entities *(include if feature involves data)*

- **Skill**: Represents an Agent Skill with `name`, `description`, and `body`.
- **CLI**: Represents a target AI CLI (Claude, Gemini, etc.) with specific paths and syntax.
- **Template**: Markdown file used as a blueprint for generation.

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: Users can generate a valid skill from description in under 1 minute.
- **SC-002**: `/hefesto.validate` correctly identifies all 13 types of violations in test cases.
- **SC-003**: 100% of generated skills pass the `agentskills.io` specification validation.
- **SC-004**: System successfully detects and writes to all 7 supported CLIs (if installed).