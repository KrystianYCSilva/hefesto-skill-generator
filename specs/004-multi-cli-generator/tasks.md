# Tasks: Multi-CLI Automatic Detection and Parallel Skill Generation

**Input**: Design documents from `/specs/004-multi-cli-generator/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Manual validation only (no automated tests requested in specification)

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

Hefesto is a prompt-based system - implementation consists of Markdown command definitions in `commands/` directory at repository root.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure (no changes needed - Hefesto infrastructure exists)

- [ ] T001 Verify existing Hefesto infrastructure (commands/, templates/, MEMORY.md, CONSTITUTION.md)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core helpers and templates that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T002 [P] Create cli-detector.md helper in commands/helpers/cli-detector.md
- [ ] T003 [P] Create cli-adapter.md registry in commands/helpers/cli-adapter.md
- [ ] T004 [P] Create parallel-generator.md orchestrator in commands/helpers/parallel-generator.md
- [ ] T005 [P] Create rollback-handler.md cleanup logic in commands/helpers/rollback-handler.md
- [ ] T006 [P] Create detection-report.md template in commands/templates/detection-report.md
- [ ] T007 [P] Create generation-report.md template in commands/templates/generation-report.md
- [ ] T008 Extend MEMORY.md schema with detected_clis section in MEMORY.md

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Automatic CLI Detection (Priority: P1) 🎯 MVP

**Goal**: Automatically detect installed AI CLIs without asking user

**Independent Test**: Run `/hefesto.create` on system with multiple CLIs and verify all detected automatically within 500ms

### Implementation for User Story 1

- [ ] T009 [US1] Implement PATH scanning logic in commands/helpers/cli-detector.md (Unix: which, Windows: where.exe)
- [ ] T010 [US1] Implement config directory checking logic in commands/helpers/cli-detector.md (check .claude/, .gemini/, etc.)
- [ ] T011 [US1] Implement result merging with priority-based conflict resolution in commands/helpers/cli-detector.md
- [ ] T012 [US1] Implement version extraction with 200ms timeout in commands/helpers/cli-detector.md
- [ ] T013 [US1] Implement detection report generation using commands/templates/detection-report.md
- [ ] T014 [US1] Implement MEMORY.md persistence for detection results in commands/helpers/cli-detector.md
- [ ] T015 [US1] Create /hefesto.detect command in commands/hefesto.detect.md (call cli-detector, display report, persist to MEMORY.md)
- [ ] T016 [US1] Add fallback mode for zero CLIs detected in commands/hefesto.detect.md

**Checkpoint**: CLI detection fully functional - can detect 0-7 CLIs in <500ms and persist results

---

## Phase 4: User Story 2 - Parallel Skill Generation (Priority: P1) 🎯 MVP

**Goal**: Generate skills for all detected CLIs simultaneously with atomic rollback

**Independent Test**: Create skill and verify appears in all detected CLI directories with proper adaptations

### Implementation for User Story 2

- [ ] T017 [P] [US2] Define Claude adapter (no transformations) in commands/helpers/cli-adapter.md
- [ ] T018 [P] [US2] Define Gemini adapter ($ARGUMENTS to {{args}}) in commands/helpers/cli-adapter.md
- [ ] T019 [P] [US2] Define Codex adapter (no transformations) in commands/helpers/cli-adapter.md
- [ ] T020 [P] [US2] Define Copilot adapter (github_integration field) in commands/helpers/cli-adapter.md
- [ ] T021 [P] [US2] Define OpenCode adapter (no transformations) in commands/helpers/cli-adapter.md
- [ ] T022 [P] [US2] Define Cursor adapter (no transformations) in commands/helpers/cli-adapter.md
- [ ] T023 [P] [US2] Define Qwen adapter ($ARGUMENTS to {{args}}) in commands/helpers/cli-adapter.md
- [ ] T024 [US2] Implement transform_variables() logic in commands/helpers/cli-adapter.md
- [ ] T025 [US2] Implement transform_structure() directory construction in commands/helpers/cli-adapter.md
- [ ] T026 [US2] Implement add_frontmatter() CLI-specific fields in commands/helpers/cli-adapter.md
- [ ] T027 [US2] Implement validate() with CLI-specific rules in commands/helpers/cli-adapter.md
- [ ] T028 [US2] Implement generate_all() main orchestration in commands/helpers/parallel-generator.md
- [ ] T029 [US2] Implement generate_single_cli() per-CLI generation in commands/helpers/parallel-generator.md
- [ ] T030 [US2] Implement temp directory staging (create, use, cleanup) in commands/helpers/parallel-generator.md
- [ ] T031 [US2] Implement parallel execution (bash background jobs for Unix) in commands/helpers/parallel-generator.md
- [ ] T032 [US2] Implement parallel execution (PowerShell jobs for Windows) in commands/helpers/parallel-generator.md
- [ ] T033 [US2] Implement validate_all_generated() parallel validation in commands/helpers/parallel-generator.md
- [ ] T034 [US2] Implement commit_to_targets() atomic move operation in commands/helpers/parallel-generator.md
- [ ] T035 [US2] Implement rollback_all() cleanup logic in commands/helpers/rollback-handler.md
- [ ] T036 [US2] Implement generation report using commands/templates/generation-report.md
- [ ] T037 [US2] Modify /hefesto.create to call cli-detector before generation in commands/hefesto.create.md
- [ ] T038 [US2] Modify /hefesto.create to call parallel-generator instead of single generation in commands/hefesto.create.md
- [ ] T039 [US2] Extend idempotence check for multi-CLI collision detection in commands/hefesto.create.md
- [ ] T040 [US2] Add progress indicators (detection, generation, validation, commit) in commands/hefesto.create.md

**Checkpoint**: Parallel generation fully functional - skills generated for all CLIs with 3x speedup and atomic rollback

---

## Phase 5: User Story 3 - Selective CLI Targeting (Priority: P2)

**Goal**: Allow users to restrict generation to specific CLIs via --cli flag

**Independent Test**: Run `/hefesto.create "skill" --cli claude,gemini` and verify only those two directories contain skill

### Implementation for User Story 3

- [ ] T041 [US3] Add --cli flag parsing to /hefesto.create in commands/hefesto.create.md
- [ ] T042 [US3] Implement comma-separated CLI name parsing in commands/hefesto.create.md
- [ ] T043 [US3] Implement CLI name validation against detected CLIs in commands/hefesto.create.md
- [ ] T044 [US3] Implement CLI filtering logic (apply --cli filter to detected list) in commands/hefesto.create.md
- [ ] T045 [US3] Add error handling for invalid CLI names with helpful message in commands/hefesto.create.md
- [ ] T046 [US3] Add warning for non-detected CLI with prompt to create anyway in commands/hefesto.create.md
- [ ] T047 [US3] Modify /hefesto.extract to support --cli flag in commands/hefesto.extract.md
- [ ] T048 [US3] Modify /hefesto.adapt to support --cli flag in commands/hefesto.adapt.md

**Checkpoint**: CLI targeting fully functional - users can restrict generation to specific CLIs

---

## Phase 6: User Story 4 - Detection Report and Visibility (Priority: P2)

**Goal**: Display clear detection report showing which CLIs found and where

**Independent Test**: Run `/hefesto.detect` and verify shows all detected CLIs with paths and versions

### Implementation for User Story 4

- [ ] T049 [US4] Enhance detection report template with formatted CLI list in commands/templates/detection-report.md
- [ ] T050 [US4] Add summary line "X out of 7 supported CLIs detected" in commands/templates/detection-report.md
- [ ] T051 [US4] Add status indicators (detected, config_only, not_found, error) in commands/temp
