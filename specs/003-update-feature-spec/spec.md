# Feature Specification: Hefesto v2.2.0 - Update, Web Research, Sub-Agents, Payload Sync

**Feature Branch**: `003-update-feature-spec`  
**Created**: 2026-02-08  
**Status**: Draft  
**Input**: User description: "com base no card @docs/cards/CARD-003-v2.2.0-features.md"  
**Release Target**: v2.2.0  
**Prerequisites**: v2.0.0 delivered (CARD-001, CARD-002 COMPLETED)

## Context

V2.0.0 was tested with Gemini CLI and revealed 4 needs:
- **Update**: No way to modify content of existing skills (only create or validate)
- **Web Research**: Agents hallucinate URLs when they cannot verify via web search
- **Sub-Agents**: No way to compose skills into specialized agents
- **Payload Drift**: Gemini commands are outdated (10 vs 13-point checklist, no Token Economy table)

**Philosophy**: Maintain template-driven/zero-code architecture (T0-HEFESTO-13). Everything in Markdown.

---

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

  NOTE: US1-US3 from v2.0.0 (create, extract, validate) are BASELINE functionality already implemented.
  This release (v2.2.0) adds NEW user stories US4-US6 below.
-->

### User Story 4 - Update Skill Content (Priority: P1)

As a developer, I want to modify the content of an existing skill (add, remove, or change sections), so that I can evolve my skills without recreating them from scratch.

**Why this priority**: Critical gap discovered in v2.0.0 - users cannot edit existing skill content.

**Independent Test**: Execute `/hefesto.update my-skill "Add examples section with 3 code samples"` and verify the skill is updated with new content while preserving structure.

**Acceptance Scenarios**:

1. **Given** an existing skill, **When** running `/hefesto.update <skill-name> <change-description>`, **Then** apply changes to SKILL.md in all CLI directories with Human Gate approval.
2. **Given** an update request with web research needed, **When** the command includes URLs or references, **Then** verify URLs exist via web search before including them.
3. **Given** an updated skill, **When** presenting for approval, **Then** show before/after diff and complete updated skill content.

---

### User Story 5 - Generate Specialized Agent (Priority: P2)

As a developer, I want to compose multiple existing skills into a specialized agent with a persona and workflow, so that I can create domain-specific assistants.

**Why this priority**: Enables reusability and composition of skills into higher-level capabilities.

**Independent Test**: Execute `/hefesto.agent "Java code reviewer that checks SOLID principles"` and verify a new agent command is created that references relevant skills.

**Acceptance Scenarios**:

1. **Given** existing skills in the repository, **When** running `/hefesto.agent <description>`, **Then** discover relevant skills and generate an agent command that composes them.
2. **Given** a generated agent, **When** validating with 7-point agent checklist, **Then** ensure all referenced skills exist and workflow is sequential.
3. **Given** an approved agent, **When** persisting, **Then** create agent as a command file (not a skill) in all detected CLI directories.

---

### User Story 6 - Verify URLs Before Publishing (Priority: P3)

As a developer, I want the system to verify URLs via web search before including them in skills, so that I avoid hallucinated or broken links.

**Why this priority**: Quality improvement discovered in v2.0.0 testing - agents frequently invent URLs.

**Independent Test**: Run `/hefesto.create "PostgreSQL optimization guide"` and verify that all URLs in generated skill exist (or receive explicit "not verified" notice).

**Acceptance Scenarios**:

1. **Given** a skill generation with URL references, **When** web search is available, **Then** verify each URL exists before including it.
2. **Given** web search is unavailable, **When** generating a skill with potential URLs, **Then** include notice "References not verified via web search".

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement `/hefesto.update` command with 7-phase workflow (Selection, Understanding, Change Planning, Apply Changes, Auto-Critique, Human Gate, Persistence).
- **FR-002**: System MUST add conditional web research step to Phase 2 of `/hefesto.create` command.
- **FR-003**: System MUST add conditional web research step to Phase 2 of `/hefesto.extract` command.
- **FR-004**: System MUST implement `/hefesto.agent` command with 6-phase workflow (Understanding, Skill Discovery, Generation, Auto-Critique, Human Gate, Persistence).
- **FR-005**: System MUST implement 7-point agent-specific quality checklist (skill existence, frontmatter, persona, workflow, CLI paths, conciseness, security).
- **FR-006**: System MUST persist agents as command files (not skills) in all detected CLI directories.
- **FR-007**: System MUST add T1-HEFESTO-03 (Web Research) rule to CONSTITUTION.md.
- **FR-008**: System MUST fix payload drift in 18 files (10→13 point checklist, Token Economy table, section naming).
- **FR-009**: System MUST show before/after diff in Human Gate for `/hefesto.update` command.
- **FR-010**: System MUST bump version to 2.2.0 in `.hefesto/version` and installer scripts.

### Non-Functional Requirements

- **NFR-001**: All changes MUST maintain template-driven/zero-code architecture (T0-HEFESTO-13).
- **NFR-002**: Web research integration MUST be conditional (work when unavailable without blocking).
- **NFR-003**: Agent generation MUST reuse existing skills (no duplication of skill content).
- **NFR-004**: Payload sync MUST be idempotent (safe to run multiple times).

### Key Entities *(include if feature involves data)*

- **Skill**: Represents an Agent Skill with `name`, `description`, `body` (existing entity from v2.0.0).
- **Agent**: NEW entity - represents a composed command with `name`, `persona`, `skill_refs[]`, `workflow[]`.
- **UpdateChange**: NEW entity - represents a modification request with `skill_name`, `change_description`, `diff_before_after`.
- **CLI**: Represents a target AI CLI (Claude, Gemini, etc.) with specific paths and syntax (existing entity from v2.0.0).
- **Template**: Markdown file used as a blueprint for generation (existing entity from v2.0.0).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can update an existing skill with content changes in under 2 minutes (includes Human Gate approval).
- **SC-002**: Users can generate a specialized agent from description in under 1.5 minutes.
- **SC-003**: `/hefesto.update` correctly applies changes while preserving agentskills.io structure in 100% of test cases.
- **SC-004**: `/hefesto.agent` validates all 7 agent checklist points and only persists agents with 0 CRITICAL issues.
- **SC-005**: Web research integration verifies at least 90% of included URLs when web search is available.
- **SC-006**: Payload sync fixes all 18 identified drift issues and passes validation.
- **SC-007**: All generated agents successfully compose existing skills without duplicating skill content.