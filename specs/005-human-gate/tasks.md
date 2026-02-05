# Tasks: Human Gate + Wizard Mode

**Input**: Design documents from `/specs/005-human-gate/`  
**Prerequisites**: plan.md (complete), spec.md (complete), contracts/ (complete)

**Tests**: Not explicitly requested in spec - focusing on implementation tasks

**Organization**: Tasks grouped by user story priority (P1 → P2 → P3) for independent implementation

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (US1, US2, US3, US4, US5)
- Exact file paths included in descriptions

## Path Conventions

Based on plan.md structure:
- Source: `commands/` and `commands/lib/`
- Tests: `commands/tests/`
- Runtime: `.hefesto/backups/`, `.hefesto/temp/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and library structure

- [X] T001 Create `.hefesto/` directory structure for backups and temp state
- [X] T002 Create `commands/lib/` directory for shared Human Gate modules
- [X] T003 [P] Create `commands/lib/__init__.py` to make lib a Python package
- [X] T004 [P] Create `commands/lib/audit.py` with operation logging infrastructure (FR-033)
- [X] T005 [P] Create `.hefesto/logs/` directory for security and operation logs

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core utilities that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Implement input sanitization in `commands/lib/sanitizer.py` (FR-031, T0-HEFESTO-11)
- [X] T007 [P] Implement ANSI color utility in `commands/lib/colors.py`
- [X] T008 [P] Implement timeout wrapper utility in `commands/lib/timeout.py`
- [X] T009 Add security logging to `commands/lib/audit.py`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Mandatory Approval Before Persistence (Priority: P1) 🎯 MVP

**Goal**: Implement Human Gate that shows preview and requires explicit approval before ANY file writes

**Independent Test**: Run `/hefesto.create "test skill"`, verify preview displays with file contents, choose `[reject]`, confirm no files created

### Implementation for User Story 1

- [ ] T010 [P] [US1] Create `commands/lib/preview.py` for preview generation (FR-003)
- [ ] T011 [P] [US1] Create `commands/lib/atomic.py` for atomic file operations (FR-006)
- [ ] T012 [US1] Implement Human Gate decision flow in `commands/lib/human_gate.py` (FR-001 to FR-007)
- [ ] T013 [US1] Integrate Human Gate into `commands/hefesto_create_impl.py`
- [ ] T014 [US1] Add operation logging to Human Gate in `commands/lib/human_gate.py`

**Checkpoint**: User Story 1 complete - Human Gate prevents unwanted file creation

---

## Phase 4: User Story 2 - Guided Skill Creation via Wizard (Priority: P2)

**Goal**: Step-by-step wizard that guides users through skill creation without memorizing syntax

**Independent Test**: Run `/hefesto.create` (no args), verify wizard prompts for name/description/etc, complete wizard, verify valid skill created

### Implementation for User Story 2

- [ ] T015 [P] [US2] Create `commands/lib/wizard.py` with Wizard State class (FR-010 to FR-014)
- [ ] T016 [US2] Implement wizard step collection in `commands/lib/wizard.py`
- [ ] T017 [US2] Implement wizard final review in `commands/lib/wizard.py` (FR-014)
- [ ] T018 [US2] Implement wizard timeout handling in `commands/lib/wizard.py`
- [ ] T019 [US2] Integrate Wizard Mode into `commands/hefesto_create_impl.py`
- [ ] T020 [US2] Integrate Wizard Mode into `commands/hefesto_extract_impl.py` (FR-009)

**Checkpoint**: User Story 2 complete - Wizard guides first-time users through skill creation

---

## Phase 5: User Story 3 - Expandable JIT Resources (Priority: P2)

**Goal**: Allow users to iteratively add scripts/references/assets during approval process

**Independent Test**: Create basic skill, choose `[expand]` at Human Gate, add script, verify preview shows new structure, approve, confirm script file created

### Implementation for User Story 3

- [ ] T021 [P] [US3] Create `commands/lib/expansion.py` for JIT resource management (FR-015 to FR-019)
- [ ] T022 [US3] Implement `[expand]` handler in `commands/lib/human_gate.py`
- [ ] T023 [US3] Update atomic persistence in `commands/lib/atomic.py`

**Checkpoint**: User Story 3 complete - Users can add optional resources iteratively

---

## Phase 6: User Story 4 - Collision Handling (Priority: P2)

**Goal**: Detect existing skills and offer overwrite (with backup), merge, or cancel options

**Independent Test**: Create skill "test-skill", attempt to create another with same name, verify collision detection, choose `[overwrite]`, verify backup created, confirm new skill replaces old

### Implementation for User Story 4

- [ ] T024 [P] [US4] Create `commands/lib/backup.py` for .tar.gz backup creation (FR-023)
- [ ] T025 [P] [US4] Create `commands/lib/diff.py` for markdown section diffing (FR-024)
- [ ] T026 [US4] Create `commands/lib/collision.py` for collision detection (FR-020 to FR-025)
- [ ] T027 [US4] Implement `[overwrite]` handler in `commands/lib/collision.py`
- [ ] T028 [US4] Implement `[merge]` handler in `commands/lib/collision.py`
- [ ] T029 [US4] Integrate collision detection into `commands/hefesto_create_impl.py`

**Checkpoint**: User Story 4 complete - Existing skills protected with backup/merge options

---

## Phase 7: User Story 5 - Inline Editing (Priority: P3)

**Goal**: Allow users to edit generated skill content before approval

**Independent Test**: Generate skill, choose `[edit]`, modify content in editor, save, verify re-validation runs, confirm changes in updated preview

### Implementation for User Story 5

- [ ] T030 [P] [US5] Create `commands/lib/editor.py` for $EDITOR integration (FR-027 to FR-030)
- [ ] T031 [US5] Implement `[edit]` handler in `commands/lib/human_gate.py`

**Checkpoint**: User Story 5 complete - Advanced users can edit skills inline

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements and documentation

- [ ] T032 [P] Add `/hefesto.resume` command in `commands/hefesto_resume_impl.py`
- [ ] T033 [P] Update `AGENTS.md` with `/hefesto.resume` command documentation
- [ ] T034 [P] Create quickstart examples in `specs/005-human-gate/quickstart.md`
- [ ] T035 Update `commands/hefesto_create_impl.py` final integration
- [ ] T036 [P] Update `MEMORY.md` with Feature 005 completion status
- [ ] T037 Manual testing of all 5 user stories

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - Can start after Phase 2
- **User Story 2 (Phase 4)**: Depends on Foundational + US1 (uses Human Gate) - Can start after US1
- **User Story 3 (Phase 5)**: Depends on US1 (extends Human Gate) - Can start after US1
- **User Story 4 (Phase 6)**: Depends on US1 (integrates with Human Gate) - Can start after US1
- **User Story 5 (Phase 7)**: Depends on US1 (extends Human Gate) - Can start after US1
- **Polish (Phase 8)**: Depends on all user stories

### User Story Dependencies

- **US1 (P1)**: Foundation only - **MVP READY**
- **US2 (P2)**: Requires US1 (proceeds to Human Gate after wizard)
- **US3 (P2)**: Requires US1 (extends `[expand]` option at Human Gate) - Can run parallel with US2/US4
- **US4 (P2)**: Requires US1 (collision before Human Gate) - Can run parallel with US2/US3
- **US5 (P3)**: Requires US1 (extends `[edit]` option at Human Gate) - Can run parallel with US2/US3/US4

### Parallel Opportunities

**Phase 1 (Setup)**: T003, T004, T005 can run in parallel

**Phase 2 (Foundational)**: T007, T008 can run in parallel after T006

**Phase 3 (US1)**: T010, T011 can run in parallel, then T012 → T013 → T014

**Phase 4 (US2)**: T015, T016 can start together

**Phase 5 (US3)**: T021 can run independently once US1 complete

**Phase 6 (US4)**: T024, T025, T026 can run in parallel

**Phase 7 (US5)**: T030 can run independently once US1 complete

**Phase 8 (Polish)**: T032, T033, T034, T036 can run in parallel

---

## Implementation Strategy

### MVP First (US1 Only) - Recommended

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T009) ← CRITICAL BLOCKER
3. Complete Phase 3: US1 (T010-T014)
4. **STOP and VALIDATE**: Test Human Gate independently
5. Deploy/demo MVP with core safety mechanism

### Incremental Delivery

1. **MVP (US1)**: Human Gate safety mechanism - **Delivers T0-HEFESTO-02 compliance**
2. **+US2**: Add Wizard Mode - **Makes tool accessible to beginners**
3. **+US3**: Add JIT expansion - **Supports Progressive Disclosure**
4. **+US4**: Add collision handling - **Prevents data loss in production**
5. **+US5**: Add inline editing - **Power user feature**

---

## Total Task Count

- **Phase 1 (Setup)**: 5 tasks
- **Phase 2 (Foundational)**: 4 tasks ← CRITICAL PATH
- **Phase 3 (US1 - P1)**: 5 tasks ← MVP
- **Phase 4 (US2 - P2)**: 6 tasks
- **Phase 5 (US3 - P2)**: 3 tasks
- **Phase 6 (US4 - P2)**: 6 tasks
- **Phase 7 (US5 - P3)**: 2 tasks
- **Phase 8 (Polish)**: 6 tasks

**Total**: 37 implementation tasks

**MVP Scope (Recommended)**: T001-T014 (14 tasks) delivers core Human Gate safety

**Parallel Opportunities**: 15 tasks marked [P] can run concurrently

---

**End of Tasks Document**
