# Implementation Plan: Multi-CLI Automatic Detection and Parallel Skill Generation

**Branch**: `004-multi-cli-generator` | **Date**: 2026-02-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/004-multi-cli-generator/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement automatic detection of 7 supported AI CLIs (Claude, Gemini, Codex, Copilot, OpenCode, Cursor, Qwen) and parallel skill generation across all detected CLIs. System will detect CLIs via PATH scanning and config directory checking, then generate skills simultaneously using CLI-specific adapters for syntax transformations. Detection must complete <500ms, generation must be 3x faster than sequential, and atomic rollback must occur if any CLI fails.

## Technical Context

**Language/Version**: Markdown-based (prompt system) with shell script detection (Bash/PowerShell cross-platform)  
**Primary Dependencies**: None - zero-dependency prompt-based system leveraging existing Hefesto infrastructure  
**Storage**: Filesystem (MEMORY.md for persistence, `.{cli}/skills/` for skill output)  
**Testing**: Manual validation against 7 CLI installations + constitution compliance checks  
**Target Platform**: Cross-platform (Windows/macOS/Linux) via existing CLI infrastructure
**Project Type**: Single project (Hefesto skill generator - command expansion)  
**Performance Goals**: Detection <500ms for 7 CLIs, parallel generation 3x faster than sequential, 100% rollback on failure  
**Constraints**: No external dependencies, must work offline, must maintain Agent Skills spec compliance (ADR-001), filesystem-only operations  
**Scale/Scope**: 7 supported CLIs, detection matrix with 2 methods (PATH + config dirs), parallel execution for up to 7 concurrent generations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### SpecKit Constitution (.specify/memory/constitution.md)
- [x] **Principle I - Spec-First Development**: Complete specification exists and approved (spec.md, 236 lines)
- [x] **Principle II - Human Gate Protocol**: This plan requires approval before Phase 0 research begins
- [x] **Principle III - Test-Driven Implementation**: N/A - no automated tests specified in requirements (manual validation only)
- [x] **Principle IV - Progressive Documentation**: Plan structure follows JIT pattern (plan.md → research.md → data-model.md → contracts/)
- [x] **Principle V - Constitution Compliance**: Checking now and will re-check after Phase 1

### Hefesto Constitution (CONSTITUTION.md)
- [x] **T0-HEFESTO-01 (Agent Skills Standard)**: Generated skills will follow agentskills.io spec (enforced by existing validator)
- [x] **T0-HEFESTO-02 (Human Gate)**: Multi-CLI generation maintains existing Human Gate in `/hefesto.create` workflow
- [x] **T0-HEFESTO-03 (Progressive Disclosure)**: Generated skills maintain <500 line SKILL.md limit (enforced by existing validator)
- [x] **T0-HEFESTO-04 (Multi-CLI Detection)**: PRIMARY FEATURE - implements this rule
- [x] **T0-HEFESTO-05 (Local Storage)**: Uses existing local storage structure (`.{cli}/skills/`)
- [x] **T0-HEFESTO-06 (Validation)**: Applies existing spec validation to all CLI outputs
- [x] **T0-HEFESTO-07 (Nomenclature)**: Uses existing skill naming validator
- [x] **T0-HEFESTO-08 (Idempotence)**: Collision detection applies to all CLIs (check each directory independently)
- [x] **T0-HEFESTO-09 (CLI Compatibility)**: PRIMARY FEATURE - implements full 7-CLI compatibility matrix
- [x] **T0-HEFESTO-10 (Citations)**: Generated skills maintain citation requirements (enforced by existing templates)
- [x] **T0-HEFESTO-11 (Security)**: No new security surface - operates within existing CLI boundaries, no shell execution of user input

**Status**: ✅ ALL GATES PASS - No constitution violations detected

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
# Hefesto is a prompt-based system - "implementation" is Markdown definitions
commands/
├── hefesto.detect.md           # NEW - CLI detection command (can be run independently)
├── hefesto.create.md            # MODIFIED - integrate multi-CLI generation
├── hefesto.extract.md           # MODIFIED - integrate multi-CLI generation
├── hefesto.adapt.md             # MODIFIED - integrate multi-CLI generation
├── helpers/
│   ├── cli-detector.md          # NEW - detection logic (PATH + config dirs)
│   ├── cli-adapter.md           # NEW - CLI-specific transformations
│   ├── parallel-generator.md    # NEW - parallel execution orchestration
│   └── rollback-handler.md      # NEW - atomic rollback on failure
└── templates/
    ├── detection-report.md      # NEW - template for detection output
    └── generation-report.md     # NEW - template for multi-CLI generation output

# Output locations (created during execution)
.claude/skills/{skill-name}/     # Claude Code skills
.gemini/skills/{skill-name}/     # Gemini CLI skills
.codex/skills/{skill-name}/      # OpenAI Codex skills
.github/skills/{skill-name}/     # VS Code/Copilot skills
.opencode/skills/{skill-name}/   # OpenCode skills
.cursor/skills/{skill-name}/     # Cursor skills
.qwen/skills/{skill-name}/       # Qwen Code skills

# State persistence
MEMORY.md                        # MODIFIED - add "detected_clis" section
```

**Structure Decision**: Single project (prompt-based system) - no traditional source code. Implementation consists of Markdown command definitions that leverage existing Hefesto infrastructure (templates, validators, Human Gate). New helpers provide detection, adaptation, and orchestration logic as reusable components callable from modified commands.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations detected** - all constitution checks pass without exceptions.

---

## Phase 0-1 Completion Summary

### Generated Artifacts

✅ **plan.md** - Complete with technical context and structure (this file)  
✅ **research.md** - 13 sections covering detection strategies, parallel execution, adapters, rollback, cross-platform, performance, testing, edge cases, integration, alternatives, open questions  
✅ **data-model.md** - 11 sections with 6 entities (CLI Detection Result, CLI Adapter, Generation Task, Detection Report, Generation Report, MEMORY.md extension)  
✅ **contracts/cli-detector.md** - Interface definition with 5 operations, testing contract, configuration reference  
✅ **contracts/cli-adapter.md** - Interface definition with 4 operations, adapter registry for 7 CLIs, testing contract  
✅ **contracts/parallel-generator.md** - Interface definition with 5 operations, parallel execution strategies, progress tracking, error scenarios  
✅ **quickstart.md** - Developer onboarding with 6-phase implementation workflow, testing checklist, common patterns, troubleshooting

### Constitution Re-Check (Phase 1 Complete)

**SpecKit Constitution**:
- ✅ Principle I: Spec exists and approved (spec.md)
- ✅ Principle II: Human Gate maintained (this plan requires approval)
- ✅ Principle III: N/A (no automated tests in requirements)
- ✅ Principle IV: JIT documentation structure followed (plan → research → data-model → contracts → quickstart)
- ✅ Principle V: Re-checked, all gates pass

**Hefesto Constitution** (T0 Rules):
- ✅ All 11 T0 rules validated against design
- ✅ No new violations introduced by design decisions
- ✅ Feature implements T0-HEFESTO-04 and T0-HEFESTO-09 as primary goal

### Next Command

`/speckit.tasks` - Generate tasks.md for implementation breakdown

---

**Plan Status**: ✅ **COMPLETE** - Ready for Human Gate Approval
