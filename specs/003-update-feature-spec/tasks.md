# Tasks: Update Feature Spec to v2.2.0

**Input**: Design documents from `specs/003-update-feature-spec/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Note**: This feature implements Hefesto v2.2.0 with 2 new commands (`/hefesto.update`, `/hefesto.agent`), web research integration, and payload synchronization across 7 CLIs. Tasks are organized by implementation step from CARD-003.

## Format: `[ID] [P?] [Step] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Step]**: Which implementation step this task belongs to (S0, S1, S2, S3, S4, S5)
- Include exact file paths in descriptions

## Path Conventions

This is a multi-CLI distributed template system:
- Canonical commands: `.claude/commands/`
- CLI directories: `.gemini/`, `.codex/`, `.github/`, `.opencode/`, `.cursor/`, `.qwen/`
- Templates: `templates/`, `.hefesto/templates/`, `installer/payload/hefesto/templates/`
- Installer payloads: `installer/payload/commands/<cli>/`

---

## Phase 1: Governance & Version (Step 0)

**Purpose**: Update version numbers and constitution before implementation

- [ ] T001 [P] [S0] Add T1-HEFESTO-03 (Web Research) rule to CONSTITUTION.md after line ~248
- [ ] T002 [P] [S0] Add version history entry for 2.1.0 in CONSTITUTION.md
- [ ] T003 [P] [S0] Update .hefesto/version from "2.1.0" to "2.2.0"
- [ ] T004 [P] [S0] Update $HEFESTO_VERSION in installer/install.ps1 to "2.2.0"
- [ ] T005 [P] [S0] Update version variable in installer/install.sh to "2.2.0"

---

## Phase 2: Web Research Integration (Step 1)

**Purpose**: Add conditional web search to create and extract commands

### Step 1A: Update hefesto.create (canonical)

- [ ] T006 [S1] Add web research step 6 to Phase 2 in .claude/commands/hefesto.create.md after "Research the skill's domain"
- [ ] T007 [S1] Renumber existing step 6 ("Plan the skill structure") to step 7 in .claude/commands/hefesto.create.md

### Step 1B: Update hefesto.extract (canonical + drift fix)

- [ ] T008 [S1] Add web research step 5 to Phase 2 in .claude/commands/hefesto.extract.md after "Summarize extraction"
- [ ] T009 [S1] Fix drift: Change "10-point quality checklist" to "13-point" at line 91 in .claude/commands/hefesto.extract.md
- [ ] T010 [S1] Fix drift: Change "<X>/10 PASS" to "<X>/13 PASS" at line 114 in .claude/commands/hefesto.extract.md

---

## Phase 3: Create /hefesto.update Command (Step 2)

**Purpose**: Implement 7-phase workflow to modify existing skill content

### Step 2A: Create canonical command

- [ ] T011 [S2] Create .claude/commands/hefesto.update.md with 7 phases (Selection, Understanding, Change Planning, Apply Changes, Auto-Critique, Human Gate, Persistence)
- [ ] T012 [S2] Add web research step to Phase 3 in .claude/commands/hefesto.update.md
- [ ] T013 [S2] Add 13-point checklist to Phase 5 in .claude/commands/hefesto.update.md
- [ ] T014 [S2] Add Human Gate with diff visualization to Phase 6 in .claude/commands/hefesto.update.md
- [ ] T015 [S2] Add multi-CLI persistence logic to Phase 7 in .claude/commands/hefesto.update.md

### Step 2B: Propagate to 7 CLIs (live repo)

- [ ] T016 [P] [S2] Create .gemini/commands/hefesto.update.toml with TOML wrapper and {{args}} syntax
- [ ] T017 [P] [S2] Create .codex/prompts/hefesto.update.md with $ARGUMENTS syntax
- [ ] T018 [P] [S2] Create .github/agents/hefesto.update.agent.md with full content
- [ ] T019 [P] [S2] Create .github/prompts/hefesto.update.prompt.md with agent reference stub
- [ ] T020 [P] [S2] Create .opencode/command/hefesto.update.md with $ARGUMENTS syntax
- [ ] T021 [P] [S2] Create .cursor/commands/hefesto.update.md with $ARGUMENTS syntax
- [ ] T022 [P] [S2] Create .qwen/commands/hefesto.update.md with {{args}} syntax

### Step 2C: Create installer payloads

- [ ] T023 [P] [S2] Copy .claude/commands/hefesto.update.md to installer/payload/commands/claude/hefesto.update.md
- [ ] T024 [P] [S2] Copy .gemini/commands/hefesto.update.toml to installer/payload/commands/gemini/hefesto.update.toml
- [ ] T025 [P] [S2] Copy .codex/prompts/hefesto.update.md to installer/payload/commands/codex/hefesto.update.md
- [ ] T026 [P] [S2] Copy .github/agents/hefesto.update.agent.md to installer/payload/commands/github/agents/hefesto.update.agent.md
- [ ] T027 [P] [S2] Copy .github/prompts/hefesto.update.prompt.md to installer/payload/commands/github/prompts/hefesto.update.prompt.md
- [ ] T028 [P] [S2] Copy .opencode/command/hefesto.update.md to installer/payload/commands/opencode/hefesto.update.md
- [ ] T029 [P] [S2] Copy .cursor/commands/hefesto.update.md to installer/payload/commands/cursor/hefesto.update.md
- [ ] T030 [P] [S2] Copy .qwen/commands/hefesto.update.md to installer/payload/commands/qwen/hefesto.update.md

---

## Phase 4: Create /hefesto.agent Command & Template (Step 3)

**Purpose**: Implement 6-phase workflow to compose skills into specialized agents

### Step 3A: Create agent template

- [ ] T031 [S3] Create templates/agent-template.md with canonical agent format (frontmatter + persona + skills + workflow + rules)
- [ ] T032 [S3] Add CLI-specific path mapping rules to templates/agent-template.md
- [ ] T033 [S3] Add Copilot dual-file generation note to templates/agent-template.md
- [ ] T034 [P] [S3] Copy templates/agent-template.md to .hefesto/templates/agent-template.md
- [ ] T035 [P] [S3] Copy templates/agent-template.md to installer/payload/hefesto/templates/agent-template.md

### Step 3B: Create canonical command

- [ ] T036 [S3] Create .claude/commands/hefesto.agent.md with 6 phases (Understanding, Skill Discovery, Generation, Auto-Critique, Human Gate, Persistence)
- [ ] T037 [S3] Add skill discovery and validation to Phase 2 in .claude/commands/hefesto.agent.md
- [ ] T038 [S3] Add CLI-aware path generation using cli-compatibility.md to Phase 3 in .claude/commands/hefesto.agent.md
- [ ] T039 [S3] Add 7-point agent checklist to Phase 4 in .claude/commands/hefesto.agent.md
- [ ] T040 [S3] Add Copilot dual-file generation logic to Phase 6 in .claude/commands/hefesto.agent.md

### Step 3C: Propagate to 7 CLIs (live repo)

- [ ] T041 [P] [S3] Create .gemini/commands/hefesto.agent.toml with TOML wrapper and {{args}} syntax
- [ ] T042 [P] [S3] Create .codex/prompts/hefesto.agent.md with $ARGUMENTS syntax
- [ ] T043 [P] [S3] Create .github/agents/hefesto.agent.agent.md with full content
- [ ] T044 [P] [S3] Create .github/prompts/hefesto.agent.prompt.md with agent reference stub
- [ ] T045 [P] [S3] Create .opencode/command/hefesto.agent.md with $ARGUMENTS syntax
- [ ] T046 [P] [S3] Create .cursor/commands/hefesto.agent.md with $ARGUMENTS syntax
- [ ] T047 [P] [S3] Create .qwen/commands/hefesto.agent.md with {{args}} syntax

### Step 3D: Create installer payloads

- [ ] T048 [P] [S3] Copy .claude/commands/hefesto.agent.md to installer/payload/commands/claude/hefesto.agent.md
- [ ] T049 [P] [S3] Copy .gemini/commands/hefesto.agent.toml to installer/payload/commands/gemini/hefesto.agent.toml
- [ ] T050 [P] [S3] Copy .codex/prompts/hefesto.agent.md to installer/payload/commands/codex/hefesto.agent.md
- [ ] T051 [P] [S3] Copy .github/agents/hefesto.agent.agent.md to installer/payload/commands/github/agents/hefesto.agent.agent.md
- [ ] T052 [P] [S3] Copy .github/prompts/hefesto.agent.prompt.md to installer/payload/commands/github/prompts/hefesto.agent.prompt.md
- [ ] T053 [P] [S3] Copy .opencode/command/hefesto.agent.md to installer/payload/commands/opencode/hefesto.agent.md
- [ ] T054 [P] [S3] Copy .cursor/commands/hefesto.agent.md to installer/payload/commands/cursor/hefesto.agent.md
- [ ] T055 [P] [S3] Copy .qwen/commands/hefesto.agent.md to installer/payload/commands/qwen/hefesto.agent.md

---

## Phase 5: Payload Sync - Fix Drift (Step 4)

**Purpose**: Synchronize all 18 drifted files with 13-point checklist and Token Economy

### Step 4A: Overhaul Gemini create command

- [ ] T056 [S4] Add "How to" section calibration step to Phase 2 in .gemini/commands/hefesto.create.toml
- [ ] T057 [S4] Add Token Economy table step to Phase 2 in .gemini/commands/hefesto.create.toml
- [ ] T058 [S4] Replace Phase 3 structure in .gemini/commands/hefesto.create.toml (remove "Instructions/Key Concepts", add "How to" sections)
- [ ] T059 [S4] Add Token Economy table to Phase 3 in .gemini/commands/hefesto.create.toml
- [ ] T060 [S4] Replace 10-point checklist with 13-point checklist in Phase 4 in .gemini/commands/hefesto.create.toml
- [ ] T061 [S4] Change "<X>/10 PASS" to "<X>/13 PASS" in Phase 5 in .gemini/commands/hefesto.create.toml
- [ ] T062 [S4] Copy .gemini/commands/hefesto.create.toml to installer/payload/commands/gemini/hefesto.create.toml

### Step 4B: Fix Gemini extract command

- [ ] T063 [S4] Change "10-point" to "13-point" in .gemini/commands/hefesto.extract.toml
- [ ] T064 [S4] Change "<X>/10 PASS" to "<X>/13 PASS" in .gemini/commands/hefesto.extract.toml
- [ ] T065 [S4] Add web research step to Phase 2 in .gemini/commands/hefesto.extract.toml
- [ ] T066 [S4] Copy .gemini/commands/hefesto.extract.toml to installer/payload/commands/gemini/hefesto.extract.toml

### Step 4C: Propagate create updates to all CLIs (live repo)

- [ ] T067 [P] [S4] Copy updated .claude/commands/hefesto.create.md to .codex/prompts/hefesto.create.md
- [ ] T068 [P] [S4] Copy updated .claude/commands/hefesto.create.md to .opencode/command/hefesto.create.md
- [ ] T069 [P] [S4] Copy updated .claude/commands/hefesto.create.md to .cursor/commands/hefesto.create.md
- [ ] T070 [P] [S4] Adapt .claude/commands/hefesto.create.md to .qwen/commands/hefesto.create.md (change $ARGUMENTS to {{args}})
- [ ] T071 [P] [S4] Copy updated .claude/commands/hefesto.create.md to .github/agents/hefesto.create.agent.md

### Step 4D: Propagate create updates to all payloads

- [ ] T072 [P] [S4] Copy updated .claude/commands/hefesto.create.md to installer/payload/commands/claude/hefesto.create.md
- [ ] T073 [P] [S4] Copy updated .codex/prompts/hefesto.create.md to installer/payload/commands/codex/hefesto.create.md
- [ ] T074 [P] [S4] Copy updated .opencode/command/hefesto.create.md to installer/payload/commands/opencode/hefesto.create.md
- [ ] T075 [P] [S4] Copy updated .cursor/commands/hefesto.create.md to installer/payload/commands/cursor/hefesto.create.md
- [ ] T076 [P] [S4] Copy updated .qwen/commands/hefesto.create.md to installer/payload/commands/qwen/hefesto.create.md
- [ ] T077 [P] [S4] Copy updated .github/agents/hefesto.create.agent.md to installer/payload/commands/github/agents/hefesto.create.agent.md

### Step 4E: Propagate extract updates to all CLIs (live repo)

- [ ] T078 [P] [S4] Copy updated .claude/commands/hefesto.extract.md to .codex/prompts/hefesto.extract.md
- [ ] T079 [P] [S4] Copy updated .claude/commands/hefesto.extract.md to .opencode/command/hefesto.extract.md
- [ ] T080 [P] [S4] Copy updated .claude/commands/hefesto.extract.md to .cursor/commands/hefesto.extract.md
- [ ] T081 [P] [S4] Adapt .claude/commands/hefesto.extract.md to .qwen/commands/hefesto.extract.md (change $ARGUMENTS to {{args}})
- [ ] T082 [P] [S4] Copy updated .claude/commands/hefesto.extract.md to .github/agents/hefesto.extract.agent.md

### Step 4F: Propagate extract updates to all payloads

- [ ] T083 [P] [S4] Copy updated .claude/commands/hefesto.extract.md to installer/payload/commands/claude/hefesto.extract.md
- [ ] T084 [P] [S4] Copy updated .codex/prompts/hefesto.extract.md to installer/payload/commands/codex/hefesto.extract.md
- [ ] T085 [P] [S4] Copy updated .opencode/command/hefesto.extract.md to installer/payload/commands/opencode/hefesto.extract.md
- [ ] T086 [P] [S4] Copy updated .cursor/commands/hefesto.extract.md to installer/payload/commands/cursor/hefesto.extract.md
- [ ] T087 [P] [S4] Copy updated .qwen/commands/hefesto.extract.md to installer/payload/commands/qwen/hefesto.extract.md
- [ ] T088 [P] [S4] Copy updated .github/agents/hefesto.extract.agent.md to installer/payload/commands/github/agents/hefesto.extract.agent.md

### Step 4G: Verify other commands (validate, init, list)

- [ ] T089 [P] [S4] Cross-check .claude/commands/hefesto.validate.md against all 7 CLI live directories for consistency
- [ ] T090 [P] [S4] Cross-check .claude/commands/hefesto.init.md against all 7 CLI live directories for consistency
- [ ] T091 [P] [S4] Cross-check .claude/commands/hefesto.list.md against all 7 CLI live directories for consistency
- [ ] T092 [P] [S4] Cross-check installer/payload/commands/*/hefesto.validate.* against canonical for consistency
- [ ] T093 [P] [S4] Cross-check installer/payload/commands/*/hefesto.init.* against canonical for consistency
- [ ] T094 [P] [S4] Cross-check installer/payload/commands/*/hefesto.list.* against canonical for consistency

---

## Phase 6: Documentation Updates (Step 5)

**Purpose**: Update documentation to reflect v2.2.0 changes

### Step 5A: Update AGENTS.md

- [ ] T095 [S5] Bump version to 2.2.0 in AGENTS.md
- [ ] T096 [S5] Add /hefesto.update to command table in AGENTS.md
- [ ] T097 [S5] Add /hefesto.agent to command table in AGENTS.md
- [ ] T098 [S5] Change "5 comandos" to "7 comandos" in AGENTS.md
- [ ] T099 [S5] Add reference to templates/agent-template.md in AGENTS.md

### Step 5B: Update ARCHITECTURE.md

- [ ] T100 [S5] Bump version to 2.2.0 in docs/ARCHITECTURE.md
- [ ] T101 [S5] Add /hefesto.update 7-phase flow diagram to docs/ARCHITECTURE.md
- [ ] T102 [S5] Add /hefesto.agent 6-phase flow diagram to docs/ARCHITECTURE.md
- [ ] T103 [S5] Update command count from 5 to 7 in docs/ARCHITECTURE.md
- [ ] T104 [S5] Update project structure section to include agent-template.md in docs/ARCHITECTURE.md

### Step 5C: Update cli-compatibility.md

- [ ] T105 [S5] Add "Agent-Specific Notes" section to templates/cli-compatibility.md with CLI directory mappings
- [ ] T106 [S5] Add note about Copilot dual-file format to templates/cli-compatibility.md
- [ ] T107 [P] [S5] Copy updated templates/cli-compatibility.md to .hefesto/templates/cli-compatibility.md
- [ ] T108 [P] [S5] Copy updated templates/cli-compatibility.md to installer/payload/hefesto/templates/cli-compatibility.md

---

## Phase 7: Validation & Testing

**Purpose**: Verify all changes are correct and functional

- [ ] T109 [P] Verify /hefesto.list shows 7 commands (not 5)
- [ ] T110 [P] Verify CONSTITUTION.md contains T1-HEFESTO-03 rule
- [ ] T111 [P] Verify .hefesto/version contains "2.2.0"
- [ ] T112 [P] Verify installer scripts reference version "2.2.0"
- [ ] T113 [P] Verify .claude/commands/hefesto.create.md has web research step
- [ ] T114 [P] Verify .claude/commands/hefesto.extract.md shows "13-point" (not "10-point")
- [ ] T115 [P] Verify .gemini/commands/hefesto.create.toml has Token Economy table
- [ ] T116 [P] Verify .gemini/commands/hefesto.create.toml has 13-point checklist
- [ ] T117 [P] Verify templates/agent-template.md exists in all 3 locations
- [ ] T118 Verify zero drift: Compare .claude/commands/ against each installer/payload/commands/<cli>/ directory
- [ ] T119 Manual test: Run /hefesto.update on test skill (if available)
- [ ] T120 Manual test: Run /hefesto.agent to generate test agent (if available)

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1 (Governance) → Phase 2 (Web Research) → Phase 3 (/hefesto.update)
                                              → Phase 4 (/hefesto.agent)
                                              → Phase 5 (Payload Sync)
                                              → Phase 6 (Documentation)
                                              → Phase 7 (Validation)
```

**Critical Path**:
1. Phase 1 MUST complete first (version numbers govern all other changes)
2. Phase 2 MUST complete before Phase 5 (canonical commands must be updated before sync)
3. Phases 3, 4 can run in parallel after Phase 2
4. Phase 5 depends on Phases 2, 3, 4 completion
5. Phase 6 can run in parallel with Phase 5
6. Phase 7 runs last to validate everything

### Step-Level Dependencies

- **Step 0 (S0)**: All 5 tasks can run in parallel
- **Step 1 (S1)**: Tasks T006-T007 must be sequential; T008-T010 must be sequential; both groups can run in parallel
- **Step 2 (S2)**: T011-T015 must be sequential; after T015, all T016-T030 can run in parallel
- **Step 3 (S3)**: T031-T033 sequential; T034-T035 parallel; T036-T040 sequential; after T040, all T041-T055 can run in parallel
- **Step 4 (S4)**: Within each substep (4A-4G), tasks can be parallel; substeps depend on Step 1 completion
- **Step 5 (S5)**: All 5A tasks sequential; all 5B tasks sequential; 5C tasks have one sequential pair (T105-T106) then parallel (T107-T108)
- **Phase 7**: All tasks can run in parallel except T118-T120 which depend on all previous phases

### Parallel Opportunities

**Maximum Parallelism** (assuming 8 workers):
- Phase 1: 5 tasks → 1 minute
- Phase 2: 2 groups (create + extract) → 2 minutes
- Phase 3 Step 2B: 7 CLI files → 3 minutes
- Phase 3 Step 2C: 8 payload files → 3 minutes
- Phase 4 Step 3C: 7 CLI files → 3 minutes
- Phase 4 Step 3D: 8 payload files → 3 minutes
- Phase 5 Step 4C-4F: ~30 files → 10 minutes
- Phase 6: 3 doc groups → 5 minutes
- Phase 7: 12 verification tasks → 5 minutes

**Total Estimated Time (parallel)**: ~35 minutes

**Total Estimated Time (sequential)**: ~3 hours

---

## Parallel Execution Examples

### Example 1: Phase 1 (Governance)
```bash
# Launch all 5 governance tasks together:
Task: "Add T1-HEFESTO-03 rule to CONSTITUTION.md"
Task: "Add version history to CONSTITUTION.md"
Task: "Update .hefesto/version to 2.2.0"
Task: "Update installer/install.ps1 version"
Task: "Update installer/install.sh version"
```

### Example 2: Step 2B (Update command propagation)
```bash
# Launch all 7 CLI files together:
Task: "Create .gemini/commands/hefesto.update.toml"
Task: "Create .codex/prompts/hefesto.update.md"
Task: "Create .github/agents/hefesto.update.agent.md"
Task: "Create .github/prompts/hefesto.update.prompt.md"
Task: "Create .opencode/command/hefesto.update.md"
Task: "Create .cursor/commands/hefesto.update.md"
Task: "Create .qwen/commands/hefesto.update.md"
```

### Example 3: Step 4C-4F (Payload sync)
```bash
# Launch all propagation tasks together:
Task: "Copy to .codex/prompts/hefesto.create.md"
Task: "Copy to .opencode/command/hefesto.create.md"
Task: "Copy to .cursor/commands/hefesto.create.md"
Task: "Adapt to .qwen/commands/hefesto.create.md"
Task: "Copy to .github/agents/hefesto.create.agent.md"
# ... (continue for all 18+ files)
```

---

## Implementation Strategy

### Recommended Approach: Sequential by Phase

Given the template-driven nature and file dependencies, **sequential execution by phase** is recommended:

1. **Phase 1** (5 tasks) - Complete all governance updates → Checkpoint: Versions updated
2. **Phase 2** (5 tasks) - Update canonical commands → Checkpoint: Web research integrated
3. **Phase 3** (30 tasks) - Create /hefesto.update → Checkpoint: Update command available
4. **Phase 4** (25 tasks) - Create /hefesto.agent → Checkpoint: Agent command available
5. **Phase 5** (39 tasks) - Sync all payloads → Checkpoint: Zero drift achieved
6. **Phase 6** (14 tasks) - Update documentation → Checkpoint: Docs synchronized
7. **Phase 7** (12 tasks) - Validate everything → Checkpoint: v2.2.0 complete

### MVP Milestone: After Phase 3

At this point you have:
- ✅ Governance updated
- ✅ Web research integrated
- ✅ `/hefesto.update` working in all 7 CLIs
- ⏳ `/hefesto.agent` not yet available
- ⏳ Payload drift not yet fixed

**Decision Point**: Can deploy `/hefesto.update` alone if needed urgently.

### Full Release: After Phase 7

All features complete:
- ✅ `/hefesto.update` (modify skills)
- ✅ `/hefesto.agent` (compose skills)
- ✅ Web research integration
- ✅ Zero payload drift
- ✅ Documentation updated
- ✅ All 7 CLIs synchronized

---

## Task Summary

| Phase | Step | Task Count | Parallel Tasks | Estimated Time (parallel) |
|-------|------|------------|----------------|---------------------------|
| Phase 1 | S0 | 5 | 5 | 1 min |
| Phase 2 | S1 | 5 | 0 | 5 min |
| Phase 3 | S2 | 30 | 22 | 10 min |
| Phase 4 | S3 | 25 | 18 | 8 min |
| Phase 5 | S4 | 39 | 33 | 12 min |
| Phase 6 | S5 | 14 | 8 | 5 min |
| Phase 7 | Validation | 12 | 11 | 5 min |
| **TOTAL** | | **130** | **97** | **~35-45 min** |

---

## Notes

- All tasks follow strict `- [ ] [ID] [P?] [Step] Description with path` format
- [P] tasks are parallelizable (different files, no dependencies within step)
- [Step] labels (S0-S5) map to CARD-003 implementation steps
- Canonical source: `.claude/commands/` (all changes start here)
- Syntax adaptation: `$ARGUMENTS` (6 CLIs) vs `{{args}}` (Gemini, Qwen)
- TOML wrapping: Only Gemini uses `description = "..." prompt = """..."""`
- Triple locations: Templates must sync to `templates/`, `.hefesto/templates/`, `installer/payload/hefesto/templates/`
- Human Gate: All new commands include explicit approval workflow
- Constitution: T1-HEFESTO-03 is new in v2.2.0
- Drift fix: 18 files updated from 10-point to 13-point checklist
- Agent template: New in v2.2.0, enables skill composition
- Verification: Phase 7 ensures zero drift between canonical and payloads
