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

- [X] T001 Verify existing Hefesto infrastructure (commands/, templates/, MEMORY.md, CONSTITUTION.md)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core helpers and templates that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 [P] Create cli-detector.md helper in commands/helpers/cli-detector.md
- [X] T003 [P] Create cli-adapter.md registry in commands/helpers/cli-adapter.md
- [X] T004 [P] Create parallel-generator.md orchestrator in commands/helpers/parallel-generator.md
- [X] T005 [P] Create rollback-handler.md cleanup logic in commands/helpers/rollback-handler.md
- [X] T006 [P] Create detection-report.md template in commands/templates/detection-report.md
- [X] T007 [P] Create generation-report.md template in commands/templates/generation-report.md
- [X] T008 Extend MEMORY.md schema with detected_clis section in MEMORY.md

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
- [ ] T051 [US4] Add status indicators (detected, config_only, not_found, error) in commands/templates/detection-report.md
- [ ] T052 [US4] Add warning indicators for config_only status in commands/templates/detection-report.md
- [ ] T053 [US4] Implement cached detection display in /hefesto.list command in commands/hefesto.list.md
- [ ] T054 [US4] Add detection timestamp display in report in commands/templates/detection-report.md

**Checkpoint**: Detection visibility complete - users see clear reports of CLI availability

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements affecting multiple user stories

- [ ] T055 [P] Add performance logging (measure detection time, generation time) in commands/helpers/cli-detector.md and parallel-generator.md
- [ ] T056 [P] Add error message standardization across all commands in commands/helpers/
- [ ] T057 [P] Update project README.md with multi-CLI examples in README.md
- [ ] T058 [P] Update AGENTS.md with multi-CLI command documentation in AGENTS.md
- [ ] T059 Validate against constitution (T0-HEFESTO-04, T0-HEFESTO-09) using CONSTITUTION.md
- [ ] T060 Run manual testing checklist from quickstart.md (40+ test cases)
- [ ] T061 Update MEMORY.md with initial empty detected_clis section if not exists

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately (verification only)
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 (Detection) can start after Foundational
  - US2 (Generation) depends on US1 detection logic
  - US3 (Targeting) depends on US2 generation integration
  - US4 (Visibility) can start after US1 (independent of US2/US3)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies
- **User Story 2 (P1)**: Depends on US1 detection logic - Uses cli-detector.md from US1
- **User Story 3 (P2)**: Depends on US2 generation integration - Modifies /hefesto.create from US2
- **User Story 4 (P2)**: Can start after US1 - Independent of US2/US3 (only enhances display)

### Within Each User Story

- **US1**: Tasks T009-T016 must run sequentially (building cli-detector.md incrementally)
- **US2**: T017-T023 can run parallel (different adapter definitions), then T024-T040 sequential
- **US3**: Tasks T041-T048 sequential (modifying same commands)
- **US4**: Tasks T049-T054 can run parallel (different templates/commands)

### Parallel Opportunities

- **Foundational Phase**: All tasks T002-T007 can run in parallel (different files)
- **US2 Adapters**: Tasks T017-T023 can run in parallel (7 independent adapter definitions)
- **US4 Visibility**: Tasks T049-T054 can run in parallel (different files)
- **Polish Phase**: Tasks T055-T058 can run in parallel (different files)

---

## Parallel Example: User Story 2 Adapters

```bash
# Launch all adapter definitions together:
Task T017: "Define Claude adapter in commands/helpers/cli-adapter.md"
Task T018: "Define Gemini adapter in commands/helpers/cli-adapter.md"
Task T019: "Define Codex adapter in commands/helpers/cli-adapter.md"
Task T020: "Define Copilot adapter in commands/helpers/cli-adapter.md"
Task T021: "Define OpenCode adapter in commands/helpers/cli-adapter.md"
Task T022: "Define Cursor adapter in commands/helpers/cli-adapter.md"
Task T023: "Define Qwen adapter in commands/helpers/cli-adapter.md"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational (T002-T008) - CRITICAL
3. Complete Phase 3: User Story 1 (T009-T016) - Detection
4. Complete Phase 4: User Story 2 (T017-T040) - Parallel Generation
5. **STOP and VALIDATE**: Test detection and generation independently
6. Deploy/demo if ready

**MVP Delivers**: Automatic CLI detection + parallel skill generation for all detected CLIs

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (Detection) → Test independently
3. Add US2 (Generation) → Test independently → **MVP COMPLETE**
4. Add US3 (Targeting) → Test independently
5. Add US4 (Visibility) → Test independently
6. Polish → Final release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T008)
2. Once Foundational done:
   - Developer A: User Story 1 (T009-T016)
   - Developer B: Start User Story 4 visibility templates (T049-T054)
3. After US1 complete:
   - Developer A: User Story 2 (T017-T040)
   - Developer B: Continue US4 (T053-T054)
4. After US2 complete:
   - Developer A or B: User Story 3 (T041-T048)
5. Polish together (T055-T061)

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] label**: Maps task to specific user story (US1-US4)
- **Prompt-based system**: Implementation is Markdown definitions, not traditional code
- **No automated tests**: Manual validation only (per specification Principle III N/A)
- **Commit strategy**: Commit after each helper/command file is complete
- **Checkpoint validation**: Test each user story independently before moving forward
- **Avoid**: Same-file conflicts when parallelizing (US2 adapters write to same cli-adapter.md in sequence)

---

## Task Summary

- **Total Tasks**: 61
- **Setup Phase**: 1 task
- **Foundational Phase**: 7 tasks (all parallelizable)
- **User Story 1 (P1 - Detection)**: 8 tasks (MVP)
- **User Story 2 (P1 - Generation)**: 24 tasks (MVP)
- **User Story 3 (P2 - Targeting)**: 8 tasks
- **User Story 4 (P2 - Visibility)**: 6 tasks
- **Polish Phase**: 7 tasks (5 parallelizable)

**MVP Scope**: Phases 1-4 (40 tasks) = Detection + Parallel Generation
**Full Feature**: All 61 tasks = Detection + Generation + Targeting + Visibility + Polish

**Parallel Opportunities Identified**: 21 tasks marked [P]

**Format Validation**: ✅ All tasks follow checklist format (checkbox, ID, labels, file paths)