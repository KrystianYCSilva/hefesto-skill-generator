---
description: "Tasks for feature 002-templates-system"
---

# Tasks: Templates System

**Input**: Design documents from `/specs/002-templates-system/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create templates directory structure in commands/templates/
- [x] T002 [P] Create helpers directory in commands/helpers/
- [x] T003 [P] Create subdirectories for adapters in commands/templates/adapters/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T004 Create official variable list documentation in commands/helpers/variables.md
- [x] T005 [P] Create variable validation logic in commands/helpers/variable-validator.md
- [x] T006 [P] Create template validation logic in commands/helpers/template-validator.md (Agent Skills spec)
- [x] T007 Create variable substitution logic with escape support in commands/helpers/variable-substitution.md (refer to research.md Q4 for implementation details)
- [x] T008 Create Human Gate blocking logic in commands/helpers/human-gate.md (FR-025, T0-HEFESTO-02)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Base Agent Skills Template (Priority: P1) 🎯 MVP

**Goal**: Provide a base skill template that follows Agent Skills specification and T0 rules

**Independent Test**: Generate a skill from base template with sample data, validate against agentskills.io spec

### Implementation for User Story 1

- [x] T009 [US1] Create base skill template in commands/templates/skill-template.md
- [x] T010 [US1] Implement T0-HEFESTO-03 check (500 lines) in commands/helpers/template-validator.md
- [x] T011 [US1] Implement T0-HEFESTO-01 check (frontmatter) in commands/helpers/template-validator.md
- [x] T012 [US1] Verify base template passes validation with sample data
- [x] T013 [US1] Verify handling of invalid input and edge cases for base template (SC-009)

**Checkpoint**: Base template is ready and validates correctly

---

## Phase 4: User Story 2 - CLI Adapters (Priority: P1)

**Goal**: Transform base template for specific CLIs (7 supported CLIs)

**Independent Test**: Apply adapter to base template, verify output matches CLI documentation syntax

### Implementation for User Story 2

- [x] T014 [P] [US2] Create Claude Code adapter in commands/templates/adapters/claude.adapter.md
- [x] T015 [P] [US2] Create Gemini CLI adapter in commands/templates/adapters/gemini.adapter.md
- [x] T016 [P] [US2] Create OpenAI Codex adapter in commands/templates/adapters/codex.adapter.md
- [x] T017 [P] [US2] Create VS Code/Copilot adapter in commands/templates/adapters/copilot.adapter.md
- [x] T018 [P] [US2] Create OpenCode adapter in commands/templates/adapters/opencode.adapter.md
- [x] T019 [P] [US2] Create Cursor adapter in commands/templates/adapters/cursor.adapter.md
- [x] T020 [P] [US2] Create Qwen Code adapter in commands/templates/adapters/qwen.adapter.md
- [x] T021 [US2] Create adapter selector logic in commands/helpers/adapter-selector.md
- [x] T022 [US2] Implement relative path adjustment logic for adapters (FR-019)
- [x] T023 [US2] Verify adapter idempotency (SC-006) and syntax compliance for all 7 CLIs

**Checkpoint**: All 7 CLI adapters exist and produce correct output syntax

---

## Phase 5: User Story 3 - Variable Substitution (Priority: P1)

**Goal**: Replace placeholders with actual skill data

**Independent Test**: Provide variables map to substitution command, verify output has no remaining placeholders

### Implementation for User Story 3

- [x] T024 [P] [US3] Implement {{SKILL_NAME}} substitution with T0-HEFESTO-07 validation
- [x] T025 [P] [US3] Implement {{SKILL_DESCRIPTION}} substitution
- [x] T026 [P] [US3] Implement {{CREATED_DATE}} auto-population (ISO 8601)
- [x] T027 [P] [US3] Implement {{VERSION}} substitution (default 1.0.0)
- [x] T028 [P] [US3] Implement {{ARGUMENTS}} substitution
- [x] T029 [US3] Verify escape mechanism {{{{VAR}}}} works as intended
- [x] T030 [US3] Verify injection prevention and T0-HEFESTO-11 security rules

**Checkpoint**: Variable substitution works for all official variables and escapes

---

## Phase 6: User Story 4 - JIT Metadata Structure (Priority: P2)

**Goal**: Support expanded metadata via metadata.yaml (ADR-003)

**Independent Test**: Generate skill with expanded metadata, verify SKILL.md has pointer and metadata.yaml exists

### Implementation for User Story 4

- [x] T031 [US4] Create metadata template in commands/templates/metadata-template.yaml
- [x] T032 [US4] Update base template to support optional metadata pointer
- [x] T033 [US4] Implement metadata.yaml validation rules in commands/helpers/template-validator.md
- [x] T034 [US4] Update substitution logic to handle metadata fields
- [x] T035 [US4] Verify metadata edge cases (missing optional fields, invalid YAML)

**Checkpoint**: Skills can be generated with rich metadata without polluting SKILL.md

---

## Phase 7: User Story 5 - MCP Adapter (Priority: P3)

**Goal**: Export skills as Model Context Protocol servers

**Independent Test**: Generate MCP server from skill, verify valid JSON-RPC 2.0 response

### Implementation for User Story 5

- [x] T036 [US5] Create MCP adapter in commands/templates/adapters/mcp.adapter.md (spec 2024-11-05)
- [x] T037 [US5] Implement argument schema extraction logic for MCP (map entities per data-model.md)
- [x] T038 [US5] Verify MCP adapter output structure against spec
- [x] T039 [US5] Verify MCP server startup and error handling edge cases

**Checkpoint**: Skills can be exported as standalone MCP servers

---

## Phase 8: Polish & Integration

**Purpose**: Finalize and integrate with system

- [x] T040 Update MEMORY.md template to track template version
- [x] T041 [P] Document template usage in docs/guides/templates.md
- [x] T042 [P] Add template update logic to /hefesto.init command
- [x] T043 Final system audit: Run full regression test on all template types

---

## Dependencies & Execution Order

1. **Setup & Foundational** (T001-T008): Must be done first
2. **User Story 1** (T009-T013): Depends on Foundational
3. **User Story 2 & 3** (T014-T030): Depend on US1, can run in parallel
4. **User Story 4** (T031-T035): Depends on US1
5. **User Story 5** (T036-T039): Depends on US1
6. **Polish** (T040-T043): Done last
