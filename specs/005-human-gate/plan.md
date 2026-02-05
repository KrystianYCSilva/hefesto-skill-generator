# Implementation Plan: Human Gate + Wizard Mode

**Branch**: `005-human-gate` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-human-gate/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement mandatory Human Gate approval workflow with wizard-guided skill creation for the Hefesto Skill Generator. This feature ensures 100% of file write operations require explicit user approval (`[approve]`, `[expand]`, `[edit]`, `[reject]`) before persistence, while providing step-by-step guidance for users creating skills without memorizing Agent Skills spec syntax. Supports collision detection with backup/merge/cancel options, JIT resource expansion, inline editing, and wizard state recovery after timeout.

**Primary Requirement**: Zero bypass mechanism for file writes (T0-HEFESTO-02 enforcement)
**Technical Approach**: Terminal-based interactive CLI with state machine for wizard flows, in-memory skill generation with atomic multi-file persistence

## Technical Context

**Language/Version**: Python 3.13  
**Primary Dependencies**: [RESEARCH IN PROGRESS - wizard library, ANSI library, markdown parser]  
**Storage**: Filesystem only (`.hefesto/backups/`, `.hefesto/temp/`, `.claude/skills/`, etc.)  
**Testing**: pytest (existing test suite pattern in `commands/tests/`)  
**Target Platform**: Cross-platform (Windows PowerShell, macOS/Linux Bash)
**Project Type**: Single project (terminal CLI tool)  
**Performance Goals**: Wizard step response <500ms, preview display <2s for 500-line skills, CLI detection <500ms (existing Feature 004)  
**Constraints**: Terminal-only UI (no GUI), 5-minute timeout for Human Gate, atomic all-or-nothing file operations  
**Scale/Scope**: 34 functional requirements, 5 user stories (P1/P2/P3 prioritized), 7 CLIs supported

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### SpecKit Constitution (v1.0.0) Compliance

- [ ] **I. Spec-First Development**: ✅ PASS - Feature spec complete and approved (spec.md with 16/16 validation checks passed)
- [ ] **II. Human Gate Protocol**: ✅ PASS - This plan will be presented for approval before Phase 0 execution
- [ ] **III. Test-Driven Implementation**: ⚠️ CONDITIONAL - User stories specify acceptance scenarios; tasks.md phase will enforce test-first where applicable
- [ ] **IV. Progressive Documentation**: ✅ PASS - Plan references research.md (Phase 0), data-model.md (Phase 1), contracts/ (Phase 1), tasks.md (Phase 2 separate command)
- [ ] **V. Constitution Compliance**: ✅ PASS - This section validates compliance; will re-check after Phase 1

### Hefesto Project Constitution (T0 Rules) Compliance

- [ ] **T0-HEFESTO-01 (Agent Skills Standard)**: ✅ N/A - This feature validates OTHER skills against standard, not itself a skill
- [ ] **T0-HEFESTO-02 (Human Gate)**: ✅ PASS - FR-001 through FR-007 enforce Human Gate for all writes; this feature IS the implementation of T0-02
- [ ] **T0-HEFESTO-03 (Progressive Disclosure)**: ✅ N/A - Not generating skills, implementing skill generator
- [ ] **T0-HEFESTO-04 (Multi-CLI Detection)**: ✅ PASS - FR-020 collision detection checks "any target CLI directory" (depends on existing Feature 004)
- [ ] **T0-HEFESTO-05 (Local Storage)**: ✅ PASS - FR-023 backups to `.hefesto/backups/`, wizard state to `.hefesto/temp/`
- [ ] **T0-HEFESTO-06 (Validation)**: ✅ PASS - FR-002 validates against Agent Skills spec BEFORE Human Gate
- [ ] **T0-HEFESTO-07 (Nomenclature)**: ✅ PASS - FR-013 auto-sanitizes skill names to T0-HEFESTO-07 format
- [ ] **T0-HEFESTO-08 (Idempotence)**: ✅ PASS - FR-020 through FR-025 implement collision detection and idempotent operations
- [ ] **T0-HEFESTO-09 (CLI Compatibility)**: ✅ PASS - Uses existing Feature 004 multi-CLI generation (FR-003 shows "target CLI directories")
- [ ] **T0-HEFESTO-10 (Citations)**: ✅ N/A - Not generating technical skills, implementing generator
- [ ] **T0-HEFESTO-11 (Security)**: ✅ PASS - FR-031 sanitizes all user inputs, FR-034 never executes user scripts during validation

**Overall Gate Status**: ✅ READY FOR PHASE 0 (11/11 T0 checks pass or N/A, 5/5 SpecKit checks pass)

**Violations**: None

## Project Structure

### Documentation (this feature)

```text
specs/005-human-gate/
├── spec.md              # Feature specification (COMPLETE)
├── checklists/
│   └── requirements.md  # Quality validation (16/16 PASS)
├── plan.md              # This file (/speckit.plan Phase 0-1 output)
├── research.md          # Phase 0 output (IN PROGRESS)
├── data-model.md        # Phase 1 output (PENDING)
├── quickstart.md        # Phase 1 output (PENDING)
├── contracts/           # Phase 1 output (PENDING)
│   ├── human-gate.md    # Human Gate decision flow contract
│   ├── wizard.md        # Wizard state machine contract
│   └── preview.md       # Preview object contract
└── tasks.md             # Phase 2 output (separate /speckit.tasks command)
```

### Source Code (repository root)

```text
# Existing structure (Feature 001-004 complete)
commands/
├── hefesto_create_impl.py       # [MODIFY] Add Human Gate + Wizard integration points
├── hefesto_extract_impl.py      # [MODIFY] Add Wizard Mode for missing args
├── hefesto_init_impl.py         # [NO CHANGE] CLI detection already complete
├── lib/                          # [NEW] Shared library modules
│   ├── __init__.py
│   ├── human_gate.py            # Human Gate decision flow (FR-001 to FR-007)
│   ├── wizard.py                # Wizard Mode state machine (FR-008 to FR-014)
│   ├── preview.py               # Preview generation + formatting (FR-003)
│   ├── collision.py             # Collision detection + resolution (FR-020 to FR-025)
│   ├── expansion.py             # JIT resource expansion (FR-015 to FR-019)
│   ├── editing.py               # Inline editing integration (FR-026 to FR-030)
│   ├── sanitizer.py             # Input sanitization (FR-031, T0-HEFESTO-11)
│   └── audit.py                 # Operation logging (FR-033)
└── tests/
    ├── test_human_gate.py       # [NEW] Human Gate tests (SC-001, SC-007)
    ├── test_wizard.py           # [NEW] Wizard Mode tests (SC-002, SC-006, SC-009)
    ├── test_collision.py        # [NEW] Collision tests (SC-004, SC-005, SC-010)
    ├── test_preview.py          # [NEW] Preview tests (SC-003)
    └── test_sanitizer.py        # [NEW] Security tests (FR-031, T0-11)

.hefesto/                        # [NEW] Hefesto runtime directory
├── backups/                     # [NEW] Backup storage (FR-023)
│   └── {skill-name}-{timestamp}.tar.gz
└── temp/                        # [NEW] Temporary state (wizard timeout)
    └── wizard-state-{timestamp}.json
```

**Structure Decision**: Single project structure maintained (existing pattern). New `commands/lib/` directory centralizes Human Gate logic for reuse across `/hefesto.create`, `/hefesto.extract`, and future commands. Test structure mirrors lib/ modules for clarity. `.hefesto/` directory for runtime artifacts (backups, wizard state) follows T0-HEFESTO-05 local storage principle.

## Complexity Tracking

> **No constitutional violations detected. This section intentionally left empty.**

## Dependencies

### External (CARDs - Must Be Complete)

- ✅ **CARD-001 (Foundation)**: CLI detection complete (Feature 004 implemented)
- ✅ **CARD-002 (Templates)**: Skill generation complete (used by preview generation in FR-001)
- ✅ **CARD-003 (Commands)**: `/hefesto.create` and `/hefesto.extract` exist (will be modified with Human Gate integration)

### Internal (ADRs - Governance)

- ✅ **ADR-001 (Agent Skills Standard)**: Validation rules for FR-002
- ✅ **ADR-002 (Research Integration)**: Security validation patterns for FR-031 (T0-HEFESTO-11)
- ✅ **ADR-003 (Lightweight Frontmatter)**: JIT resource structure for FR-015 to FR-019 (scripts/, references/, assets/)

### Technical (Research - PENDING Phase 0)

- ⏳ **Terminal Input Library**: Wizard step-by-step input, timeout handling, "back" command support (FR-010, FR-012, FR-005)
- ⏳ **ANSI Formatting Library**: Cross-platform color preview display with fallback (FR-003, Assumption #1)
- ⏳ **Markdown Parsing**: Section-by-section diff for merge conflicts (FR-024 clarification: Option C)
- ⏳ **Editor Integration**: Launch $EDITOR cross-platform (FR-027)
- ⏳ **Input Sanitization**: Shell/prompt injection prevention (FR-031)
- ⏳ **Atomic File Operations**: All-or-nothing multi-file writes with rollback (FR-006, Edge Case #4)

## Constraints & Assumptions

### Technical Constraints (from spec)

1. **Terminal-Based UI**: All interactions via text terminal (no GUI)
2. **Cross-Platform**: Windows PowerShell + macOS/Linux Bash without modification
3. **Atomic Operations**: Multi-file writes (multi-CLI generation) must be atomic (all succeed or all fail with rollback)
4. **No Implementation Bypass**: Spec intentionally avoids HOW (libraries, frameworks) - design phase determines these

### Assumptions (from spec - validated)

1. **Terminal Capabilities**: ANSI color codes supported (fallback to plain text) - CONFIRMED Windows PowerShell + Linux/macOS terminals
2. **Editor Availability**: $EDITOR set or system default (vim/nano/notepad) - STANDARD assumption for CLI tools
3. **Filesystem Permissions**: Write access to project directory + `.hefesto/` - STANDARD for tool operation
4. **Session Persistence**: Terminal stays active during wizard (timeout handles interruptions) - MITIGATED by wizard state save (FR-097 edge case)
5. **CLI Detection**: At least one CLI detected before Human Gate - VALIDATED by existing Feature 004

### Performance Targets (from Success Criteria)

- **SC-002**: Wizard completion <5 minutes for simple skills (3 steps: name, description, approve)
- **SC-003**: Preview display <2 seconds for skills up to 500 lines (T0-HEFESTO-03 limit)
- **SC-007**: Timeout triggers correctly at 5 minutes (100% accuracy)
- Implicit: CLI detection <500ms (inherited from Feature 004)

## Integration Points

### Existing Code Modifications

1. **`commands/hefesto_create_impl.py`**:
   - **Current**: Generates skill, writes directly to filesystem
   - **Change**: Insert Human Gate BEFORE filesystem write (call `lib/human_gate.py`)
   - **Change**: If description missing, activate Wizard Mode (call `lib/wizard.py`)
   - **Risk**: Low - insertion point is clear (after generation, before write)

2. **`commands/hefesto_extract_impl.py`**:
   - **Current**: Extracts skill from file, writes directly
   - **Change**: Insert Human Gate BEFORE write
   - **Change**: If file path missing, activate Wizard Mode (prompt for path)
   - **Risk**: Low - similar pattern to hefesto_create

3. **Multi-CLI Generation (Feature 004)**:
   - **Current**: Generates for all detected CLIs in parallel
   - **Change**: Human Gate shows preview for ALL target CLIs before ANY write
   - **Change**: Atomic rollback if ANY CLI write fails (Edge Case #4)
   - **Risk**: Medium - requires coordination with existing parallel generation logic

### New Command Required

- **`/hefesto.resume`** (FR-097 edge case clarification: Option B):
  - **Purpose**: Resume wizard from saved state after timeout/interrupt
  - **Args**: `{path}` to wizard state JSON (`.hefesto/temp/wizard-state-{timestamp}.json`)
  - **Implementation**: Load JSON, restore Wizard State, resume at `current_step`
  - **Priority**: P2 (required for wizard timeout edge case)

## Phase 0: Research (Next Step)

**Status**: ⏳ IN PROGRESS (research agent dispatched)

**Research Tasks**:
1. Interactive terminal input library (wizard, timeout, back command)
2. ANSI formatting library (cross-platform, fallback)
3. Markdown parsing for section-by-section diff
4. Editor integration ($EDITOR launch, cross-platform)
5. Input sanitization (shell/prompt injection prevention)
6. Atomic file operations (rollback on failure)

**Output**: `research.md` with decisions, rationales, alternatives considered

**Next Gate**: Present research.md for Human Gate approval before Phase 1

---

## Phase 1: Design (PENDING)

**Prerequisites**: research.md approved

**Deliverables**:
1. `data-model.md`: Entities (Preview Object, Wizard State, Collision Info, etc.)
2. `contracts/`: API contracts (human-gate.md, wizard.md, preview.md)
3. `quickstart.md`: Setup instructions, usage examples
4. Agent context update (technology choices from research)

**Next Gate**: Present Phase 1 artifacts + re-validate Constitution Check

---

## Phase 2: Task Breakdown (PENDING)

**Command**: `/speckit.tasks` (separate command, not part of `/speckit.plan`)

**Deliverables**:
1. `tasks.md`: Granular implementation tasks organized by user story priority (P1 → P2 → P3)

---

**Plan Status**: Phase 0 in progress | Awaiting research.md completion and Human Gate approval
