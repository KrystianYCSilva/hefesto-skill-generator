---
description: "Task breakdown for Hefesto Foundation Infrastructure organized by user story and phase"
feature: "001-hefesto-foundation"
type: "tasks"
status: "complete"
total_tasks: 61
completed_tasks: 61
version: "1.0.0"
---

# Tasks: Hefesto Foundation Infrastructure

**Input**: Design documents from `/specs/001-hefesto-foundation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: No automated tests specified in feature specification - manual acceptance testing only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Hefesto project**: Prompt-based architecture - command definitions in `commands/`, no traditional src/
- Paths shown below are relative to repository root
- State files: `MEMORY.md`, `CONSTITUTION.md` at repository root
- CLI directories: `.{cli-name}/skills/` created dynamically by bootstrap

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and establish command definition structure

- [X] T001 Create commands directory at repository root (`commands/`)
- [X] T002 [P] Verify CONSTITUTION.md exists at repository root (bundled with Hefesto)
- [X] T003 [P] Verify AGENTS.md exists at repository root with bootstrap instructions

**Checkpoint**: Basic project structure ready for command definitions

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Create MEMORY.md template structure with YAML frontmatter schema in `commands/templates/memory-template.md`
- [X] T005 [P] Create CLI detection strategy documentation in `commands/helpers/cli-detection-strategy.md`
- [X] T006 [P] Define error handling patterns in `commands/helpers/error-handling.md`
- [X] T007 [P] Create bootstrap report template in `commands/templates/bootstrap-report-template.md`
- [X] T008 Create CONSTITUTION validation logic specification in `commands/helpers/constitution-validator.md`
- [X] T009 Create cross-platform command abstraction guide in `commands/helpers/platform-detection.md`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Bootstrap Hefesto in Existing Project (Priority: P1) 🎯 MVP

**Goal**: Enable developers to initialize Hefesto infrastructure automatically by detecting installed CLIs and creating directory structures

**Independent Test**: Run `/hefesto.init` in fresh project → verify CLI detection → verify directory creation → verify MEMORY.md initialization → verify bootstrap completes in < 5 seconds

### Implementation for User Story 1

- [X] T010 [P] [US1] Create `/hefesto.init` command definition in `commands/hefesto.init.md`
- [X] T011 [P] [US1] Define CLI detection contract implementation in `commands/hefesto.init.md` (section: CLI Detection Logic)
- [X] T012 [US1] Implement PATH scanning logic for all 7 CLIs in `commands/hefesto.init.md` (section: PATH Detection Strategy)
- [X] T013 [US1] Implement config directory detection logic in `commands/hefesto.init.md` (section: Config Directory Detection)
- [X] T014 [US1] Implement directory creation logic with idempotency in `commands/hefesto.init.md` (section: Directory Creation)
- [X] T015 [US1] Implement MEMORY.md initialization with Project State entity in `commands/hefesto.init.md` (section: State Initialization)
- [X] T016 [US1] Implement CONSTITUTION.md copy logic (if not present) in `commands/hefesto.init.md` (section: Constitution Setup)
- [X] T017 [US1] Implement bootstrap report generation in `commands/hefesto.init.md` (section: Report Generation)
- [X] T018 [US1] Add command registration logic in AGENTS.md (update section: Comandos Disponiveis)
- [X] T019 [US1] Document `/hefesto.init` usage and examples in `commands/hefesto.init.md` (section: Usage Examples)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Manual testing via quickstart.md Test 1, Test 4, Test 5.

---

## Phase 4: User Story 2 - Detect Installed AI CLIs Automatically (Priority: P1)

**Goal**: Provide standalone CLI detection capability that can be invoked independently or after installation of new CLIs

**Independent Test**: Install new CLI → run `/hefesto.detect` → verify new CLI added to MEMORY.md → verify directory created → existing CLIs unchanged

### Implementation for User Story 2

- [X] T020 [P] [US2] Create `/hefesto.detect` command definition in `commands/hefesto.detect.md`
- [X] T021 [US2] Implement CLI re-detection logic (reuse US1 detection code) in `commands/hefesto.detect.md` (section: Re-Detection Logic)
- [X] T022 [US2] Implement incremental CLI addition (add only new CLIs) in `commands/hefesto.detect.md` (section: Incremental Addition)
- [X] T023 [US2] Implement detection report showing new vs. existing CLIs in `commands/hefesto.detect.md` (section: Detection Report)
- [X] T024 [US2] Handle permission errors gracefully (skip problematic CLI, continue) in `commands/hefesto.detect.md` (section: Error Handling)
- [X] T025 [US2] Implement warnings for config-only CLIs (not in PATH) in `commands/hefesto.detect.md` (section: Warning Generation)
- [X] T026 [US2] Add manual CLI specification fallback in `commands/hefesto.detect.md` (section: Manual Fallback)
- [X] T027 [US2] Update MEMORY.md with new CLI Detection Results in `commands/hefesto.detect.md` (section: State Update)
- [X] T028 [US2] Update command registration in AGENTS.md (section: Comandos Disponiveis)
- [X] T029 [US2] Document `/hefesto.detect` usage and examples in `commands/hefesto.detect.md` (section: Usage Examples)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Manual testing via quickstart.md Test 2, Test 3, Test 8.

---

## Phase 5: User Story 3 - Persist Project State Across Sessions (Priority: P2)

**Goal**: Ensure MEMORY.md reliably tracks state across sessions with corruption recovery and filesystem synchronization

**Independent Test**: Generate skill → close session → reopen → run `/hefesto.list` → verify skill remembered → manually delete skill directory → next command detects → MEMORY.md updates

### Implementation for User Story 3

- [X] T030 [P] [US3] Create `/hefesto.list` command definition in `commands/hefesto.list.md`
- [X] T031 [US3] Implement MEMORY.md parsing logic (YAML frontmatter + Markdown tables) in `commands/hefesto.list.md` (section: State Parsing)
- [X] T032 [US3] Implement corrupted MEMORY.md detection in `commands/helpers/memory-validator.md`
- [X] T033 [US3] Implement backup logic (timestamp suffix) in `commands/helpers/memory-recovery.md`
- [X] T034 [US3] Implement filesystem rescan to rebuild state in `commands/helpers/memory-recovery.md` (section: State Rebuild)
- [X] T035 [US3] Implement CLI listing from MEMORY.md in `commands/hefesto.list.md` (section: CLI Listing)
- [X] T036 [US3] Implement skill registry display in `commands/hefesto.list.md` (section: Skill Registry Display)
- [X] T037 [US3] Implement state metadata display (total skills, active CLIs) in `commands/hefesto.list.md` (section: State Metadata Display)
- [X] T038 [US3] Add filesystem synchronization check on command execution in `commands/helpers/state-sync.md`
- [X] T039 [US3] Update command registration in AGENTS.md (section: Comandos Disponiveis)
- [X] T040 [US3] Document `/hefesto.list` usage and examples in `commands/hefesto.list.md` (section: Usage Examples)

**Checkpoint**: All user stories should now be independently functional. Manual testing via quickstart.md Test 6.

---

## Phase 6: User Story 4 - Enforce Constitutional Governance from Start (Priority: P2)

**Goal**: Validate CONSTITUTION.md integrity on every command execution and enforce T0 rules before operations proceed

**Independent Test**: Delete CONSTITUTION.md → run any `/hefesto.*` command → verify auto-restoration → modify CONSTITUTION.md to violate T0 → run command → verify operations blocked

### Implementation for User Story 4

- [X] T041 [P] [US4] Create CONSTITUTION.md validation module in `commands/helpers/constitution-validator.md`
- [X] T042 [US4] Implement file existence check in `commands/helpers/constitution-validator.md` (section: Existence Check)
- [X] T043 [US4] Implement YAML frontmatter validation (version, status, tier) in `commands/helpers/constitution-validator.md` (section: Frontmatter Validation)
- [X] T044 [US4] Implement T0 rules presence validation (all 11 rules) in `commands/helpers/constitution-validator.md` (section: T0 Rules Check)
- [X] T045 [US4] Implement structure integrity check (heading hierarchy) in `commands/helpers/constitution-validator.md` (section: Structure Validation)
- [X] T046 [US4] Implement auto-restoration from bundled copy in `commands/helpers/constitution-recovery.md`
- [X] T047 [US4] Implement operation blocking on T0 violations in `commands/helpers/constitution-validator.md` (section: T0 Rule Enforcement and Operation Blocking)
- [X] T048 [US4] Integrate validation check into all `/hefesto.*` commands (update hefesto.init.md, hefesto.detect.md, hefesto.list.md with validation calls)
- [X] T049 [US4] Document validation process in `commands/helpers/constitution-validator.md` (section: Validation Workflow)

**Checkpoint**: Constitutional governance fully enforced across all commands. Manual testing via quickstart.md Test 7.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final quality checks

- [X] T050 [P] Create `/hefesto.help` command in `commands/hefesto.help.md` listing all available commands
- [X] T051 [P] Document error codes and resolutions in `commands/helpers/error-codes.md`
- [X] T052 [P] Create troubleshooting guide in `.context/troubleshooting/foundation-issues.md`
- [X] T053 [P] Add performance benchmarks documentation in `docs/performance/bootstrap-benchmarks.md`
- [X] T054 Update AGENTS.md with complete command reference (section: Comandos Disponiveis)
- [X] T055 Create .gitignore recommendations in `docs/guides/git-integration.md`
- [X] T056 Run quickstart.md validation for all 8 test scenarios
- [X] T057 Verify idempotency (run bootstrap twice, verify no duplicates)
- [X] T058 Verify cross-platform compatibility (test on Windows, macOS, Linux per quickstart.md)
- [X] T059 Performance validation: Bootstrap < 5s, CLI detection < 2s, MEMORY.md write < 100ms
- [X] T060 [P] Update tech-stack.md with implementation details in `.context/_meta/tech-stack.md`
- [X] T061 [P] Document Git worktree/submodule behavior in `docs/guides/git-integration.md` (section: Worktree Handling)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P1): Can start after Foundational - May reuse US1 detection code but independently testable
  - User Story 3 (P2): Can start after Foundational - Independent of US1/US2 but naturally follows bootstrap
  - User Story 4 (P2): Can start after Foundational - Independent but integrates with all commands
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Bootstrap)**: No dependencies on other stories - Pure initialization
- **User Story 2 (P1 - CLI Detection)**: No hard dependencies, but reuses detection logic from US1 - Independently testable
- **User Story 3 (P2 - State Persistence)**: No hard dependencies, but validates state created by US1 - Independently testable
- **User Story 4 (P2 - Constitution Governance)**: No hard dependencies, but validates constitution used by US1 - Independently testable

### Within Each User Story

- **User Story 1 (Bootstrap)**:
  1. Command definition (T010, T011) first
  2. Detection logic (T012, T013) parallel
  3. Creation & initialization (T014, T015, T016) sequential after detection
  4. Report & documentation (T017, T018, T019) parallel after core logic

- **User Story 2 (CLI Detection)**:
  1. Command definition (T020) first
  2. Re-detection logic (T021, T022) sequential
  3. Reporting & error handling (T023, T024, T025, T026) parallel after logic
  4. State update & documentation (T027, T028, T029) sequential

- **User Story 3 (State Persistence)**:
  1. Command definition & parsing (T030, T031) parallel
  2. Recovery logic (T032, T033, T034) sequential
  3. Display logic (T035, T036, T037) parallel after parsing
  4. Sync check & documentation (T038, T039, T040) sequential

- **User Story 4 (Constitution Governance)**:
  1. Validation module (T041, T042, T043, T044, T045) sequential
  2. Recovery & blocking (T046, T047) parallel after validation
  3. Integration & documentation (T048, T049) sequential

### Parallel Opportunities

- All Setup tasks (T001, T002, T003) can run in parallel
- All Foundational tasks (T004-T009) marked [P] can run in parallel
- Once Foundational phase completes, all P1 user stories (US1, US2) can start in parallel (if team capacity allows)
- P2 user stories (US3, US4) can start after foundation if desired, or wait for P1 completion
- Within each story, tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1 (Bootstrap)

```bash
# Launch command definition tasks together:
Task: "Create /hefesto.init command definition in commands/hefesto.init.md"
Task: "Define CLI detection contract implementation in commands/hefesto.init.md"

# Launch detection logic tasks together:
Task: "Implement PATH scanning logic for all 7 CLIs in commands/hefesto.init.md"
Task: "Implement config directory detection logic in commands/hefesto.init.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Bootstrap)
4. **STOP and VALIDATE**: Test User Story 1 independently per quickstart.md Test 1, Test 4, Test 5
5. Verify bootstrap works end-to-end before proceeding

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Bootstrap) → Test independently → Functional MVP!
3. Add User Story 2 (CLI Detection) → Test independently → Enhanced detection
4. Add User Story 3 (State Persistence) → Test independently → Stateful operations
5. Add User Story 4 (Constitution Governance) → Test independently → Full governance
6. Polish phase → Production-ready

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Bootstrap)
   - Developer B: User Story 2 (CLI Detection) - starts in parallel with US1
   - Developer C: User Story 3 (State Persistence) - can start after foundation
   - Developer D: User Story 4 (Constitution Governance) - can start after foundation
3. Stories complete and integrate independently
4. Integration testing after all stories complete

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- No automated tests specified - use manual acceptance testing per quickstart.md
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Hefesto is prompt-based: implementation is via Markdown command definitions, not traditional code
- All file paths are relative to repository root
- MEMORY.md and CONSTITUTION.md are at project root, commands are in `commands/` directory
