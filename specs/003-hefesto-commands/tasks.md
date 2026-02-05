# Tasks: Feature 003 - Hefesto Commands Implementation

## Format Guide
```
- [ ] TXXX [P?] [Story?] Description with file path
  - Story labels: [US1], [US2], [US3], [US4] (only for user story phases)
  - [P] = Parallelizable (different files, no dependencies)
  - Task IDs are sequential (T001, T002, T003...)
  - Exact file paths required in descriptions
```

---

## Phase 1: Setup & Verification

### Infrastructure Verification
- [X] T001 Verify commands/ directory structure exists at `commands/`
- [X] T002 Verify hefesto.list.md exists from Feature 001 at `commands/hefesto.list.md`
- [X] T003 Verify hefesto.help.md exists from Feature 001 at `commands/hefesto.help.md`
- [X] T004 Review Agent Skills spec requirements at `.context/standards/agent-skills-spec.md`

---

## Phase 2: Foundational Updates

### Update Existing Commands
- [X] T005 Update hefesto.help.md to include all 9 commands (7 new + 2 existing) at `commands/hefesto.help.md`
- [X] T006 Verify hefesto.list.md aligns with new command structure at `commands/hefesto.list.md`

---

## Phase 3: User Story 1 - Core Skill Creation & Extraction (P1)

### US1: /hefesto.create - Skill Creation from Description
- [X] T007 [P] [US1] Create hefesto.create.md with Wizard Mode flow at `commands/hefesto.create.md`
- [X] T008 [US1] Add skill name & description prompts to hefesto.create.md
- [X] T009 [US1] Add CLI detection & tool mapping prompts to hefesto.create.md
- [X] T010 [US1] Add parameter definition prompts to hefesto.create.md
- [X] T011 [US1] Add examples & edge cases prompts to hefesto.create.md
- [X] T012 [US1] Add Human Gate preview & approval flow to hefesto.create.md
- [X] T013 [US1] Add auto-storage logic (current project) to hefesto.create.md
- [X] T014 [US1] Add SC-005 embedded documentation to hefesto.create.md

### US1: /hefesto.extract - Skill Extraction from Code
- [X] T015 [P] [US1] Create hefesto.extract.md with Wizard Mode flow at `commands/hefesto.extract.md`
- [X] T016 [US1] Add source code input prompts (file path or paste) to hefesto.extract.md
- [X] T017 [US1] Add CLI auto-detection logic to hefesto.extract.md
- [X] T018 [US1] Add pattern recognition & command extraction to hefesto.extract.md
- [X] T019 [US1] Add skill metadata inference to hefesto.extract.md
- [X] T020 [US1] Add Human Gate preview & approval flow to hefesto.extract.md
- [X] T021 [US1] Add auto-storage logic (current project) to hefesto.extract.md
- [X] T022 [US1] Add SC-005 embedded documentation to hefesto.extract.md

---

## Phase 4: User Story 2 - Validation & Listing (P1)

### US2: /hefesto.validate - Skill Validation
- [X] T023 [US2] Create hefesto.validate.md at `commands/hefesto.validate.md`
- [X] T024 [US2] Add skill file input (path or auto-detect) to hefesto.validate.md
- [X] T025 [US2] Add Agent Skills spec validation checks to hefesto.validate.md
- [X] T026 [US2] Add CONSTITUTION.md T0 rule compliance checks to hefesto.validate.md
- [X] T027 [US2] Add validation report format (pass/fail + suggestions) to hefesto.validate.md
- [X] T028 [US2] Add SC-002 <2s read-only constraint to hefesto.validate.md
- [X] T029 [US2] Add SC-005 embedded documentation to hefesto.validate.md

### US2: /hefesto.list - Verify Existing Implementation
- [X] T030 [US2] Verify hefesto.list.md meets SC-002 <2s constraint at `commands/hefesto.list.md`
- [X] T031 [US2] Verify hefesto.list.md has proper filtering & search at `commands/hefesto.list.md`

---

## Phase 5: User Story 3 - Adaptation & Sync (P2)

### US3: /hefesto.adapt - CLI Adaptation
- [X] T032 [P] [US3] Create hefesto.adapt.md with Wizard Mode flow at `commands/hefesto.adapt.md`
- [X] T033 [US3] Add source skill selection prompt to hefesto.adapt.md
- [X] T034 [US3] Add target CLI detection & mapping to hefesto.adapt.md
- [X] T035 [US3] Add command syntax translation logic to hefesto.adapt.md
- [X] T036 [US3] Add parameter compatibility mapping to hefesto.adapt.md
- [X] T037 [US3] Add Human Gate preview & approval flow to hefesto.adapt.md
- [X] T038 [US3] Add SC-003 write protection to hefesto.adapt.md
- [X] T039 [US3] Add SC-005 embedded documentation to hefesto.adapt.md

### US3: /hefesto.sync - Multi-CLI Sync
- [X] T040 [P] [US3] Create hefesto.sync.md with Wizard Mode flow at `commands/hefesto.sync.md`
- [X] T041 [US3] Add skill selection & target CLI detection to hefesto.sync.md
- [X] T042 [US3] Add sync conflict detection logic to hefesto.sync.md
- [X] T043 [US3] Add merge strategy prompts (overwrite/merge/skip) to hefesto.sync.md
- [X] T044 [US3] Add Human Gate preview for all changes to hefesto.sync.md
- [X] T045 [US3] Add batch approval workflow to hefesto.sync.md
- [X] T046 [US3] Add SC-003 write protection to hefesto.sync.md
- [X] T047 [US3] Add SC-005 embedded documentation to hefesto.sync.md

---

## Phase 6: User Story 4 - Management & Help (P2)

### US4: /hefesto.show - Skill Display
- [X] T048 [P] [US4] Create hefesto.show.md at `commands/hefesto.show.md`
- [X] T049 [US4] Add skill selection prompt (name or path) to hefesto.show.md
- [X] T050 [US4] Add formatted display logic (metadata + examples + usage) to hefesto.show.md
- [X] T051 [US4] Add syntax highlighting hints to hefesto.show.md
- [X] T052 [US4] Add SC-002 <2s read-only constraint to hefesto.show.md
- [X] T053 [US4] Add SC-005 embedded documentation to hefesto.show.md

### US4: /hefesto.delete - Skill Deletion
- [X] T054 [P] [US4] Create hefesto.delete.md at `commands/hefesto.delete.md`
- [X] T055 [US4] Add skill selection prompt (name or path) to hefesto.delete.md
- [X] T056 [US4] Add dependency check (skills using this skill) to hefesto.delete.md
- [X] T057 [US4] Add Human Gate confirmation (DESTRUCTIVE action warning) to hefesto.delete.md
- [X] T058 [US4] Add SC-003 write protection to hefesto.delete.md
- [X] T059 [US4] Add SC-005 embedded documentation to hefesto.delete.md

### US4: /hefesto.help - Verify Existing Implementation
- [X] T060 [US4] Verify hefesto.help.md includes all 9 commands at `commands/hefesto.help.md`
- [X] T061 [US4] Verify hefesto.help.md has usage examples at `commands/hefesto.help.md`

---

## Phase 7: Polish & Documentation

### Cross-Command Integration
- [X] T062 Verify all commands reference Human Gate protocol consistently
- [X] T063 Verify all commands use Wizard Mode for complex flows
- [X] T064 Verify all commands reference CLI auto-detection
- [X] T065 Verify all commands store skills in current project by default

### Documentation Updates
- [X] T066 Update MEMORY.md with Phase 3 completion status at `MEMORY.md`
- [X] T067 Update MEMORY.md with all 9 commands documented at `MEMORY.md`
- [X] T068 Verify AGENTS.md command table is complete at `AGENTS.md`
- [ ] T069 Add implementation notes to `.context/troubleshooting/common-issues.md`

### Success Criteria Verification
- [X] T070 Verify SC-001: 9/9 commands exist (7 new + 2 existing)
- [X] T071 Verify SC-002: All read commands <2s (list, validate, show)
- [X] T072 Verify SC-003: All write commands have Human Gate (create, extract, adapt, sync, delete)
- [X] T073 Verify SC-004: All complex commands use Auto Wizard Mode
- [X] T074 Verify SC-005: All commands have embedded docs

---

## Dependencies

### Sequential Chains
```
T001-T004 → T005-T006 (verify before updating)
T005 → T007-T060 (help.md must be updated before new commands reference it)
T007-T014 → T062 (create.md must exist before cross-command integration)
T015-T022 → T062 (extract.md must exist before cross-command integration)
T062-T065 → T066-T074 (integration complete before documentation)
```

### Parallel Opportunities
```
Phase 3 US1:
- T007 (create.md) || T015 (extract.md) - different files

Phase 5 US3:
- T032 (adapt.md) || T040 (sync.md) - different files

Phase 6 US4:
- T048 (show.md) || T054 (delete.md) - different files
```

---

## Implementation Strategy

### Phase Approach
1. **Phase 1-2 (T001-T006)**: Quick verification & foundation updates (~30min)
2. **Phase 3 (T007-T022)**: P1 User Story 1 - Core creation/extraction MVP (~3-4 hours)
3. **Phase 4 (T023-T031)**: P1 User Story 2 - Validation & listing (~1-2 hours)
4. **Phase 5 (T032-T047)**: P2 User Story 3 - Adaptation & sync (~3-4 hours)
5. **Phase 6 (T048-T061)**: P2 User Story 4 - Management & help (~2-3 hours)
6. **Phase 7 (T062-T074)**: Polish & verification (~1-2 hours)

### Command Template Structure
Each command file should follow:
```markdown
# Command: /hefesto.{command}

## Purpose
[Single line description]

## Wizard Mode Flow
[Step-by-step interactive prompts]

## Parameters
[CLI tools, skill names, paths, etc.]

## Human Gate Protocol
[For write operations only]

## Output Format
[What the user sees]

## Examples
[3-5 usage examples]

## Edge Cases
[Error handling & validation]

## Success Criteria
[SC-XXX references]

## See Also
[Related commands]
```

### CLI Detection Pattern (Reusable)
```
1. Scan package.json for devDependencies/scripts
2. Check for config files (.prettierrc, .eslintrc, etc.)
3. Check for lock files (package-lock.json, yarn.lock, etc.)
4. Present detected CLIs to user for confirmation
```

### Human Gate Pattern (Reusable)
```
1. Generate skill in memory
2. Validate against Agent Skills spec
3. Display formatted preview
4. Prompt: [approve] [expand] [edit] [reject]
5. Only persist on [approve]
```

---

## Success Metrics

| Metric | Target | Verification Task |
|--------|--------|-------------------|
| Commands Created | 7 new + 2 existing = 9 total | T070 |
| Read Performance | <2s for list/validate/show | T071 |
| Write Protection | 100% Human Gate for 5 commands | T072 |
| Wizard Mode | 100% for complex commands | T073 |
| Documentation | 100% embedded docs | T074 |

---

**tasks.md** | Feature 003 - Hefesto Commands | 2026-02-04
