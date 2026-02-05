# Implementation Plan: Hefesto Commands

**Branch**: `003-hefesto-commands` | **Date**: 2026-02-04 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/003-hefesto-commands/spec.md`

---

## Summary

Implement 8 Hefesto command definitions as Markdown-based prompts following Agent Skills standard. All write operations enforce Human Gate (T0-HEFESTO-02). Commands support positional arguments and interactive Wizard Mode. Extends completed Feature 002 (Templates System).

---

## Technical Context

**Language/Version**: N/A (Prompt-based Markdown system)  
**Primary Dependencies**: Feature 002 (Templates System) - COMPLETE  
**Storage**: Filesystem (MEMORY.md, skill directories per CLI)  
**Testing**: Manual validation against spec + Agent Skills compliance  
**Target Platform**: AI Agent execution (Claude, Gemini, OpenCode, etc.)  
**Project Type**: Prompt-based command system (Markdown definitions)  
**Performance Goals**: <2s reads (list, show, validate, help), <10s writes (create, extract, adapt, sync, delete)  
**Constraints**: <500 lines per command (T0-HEFESTO-03), 100% Human Gate writes (T0-HEFESTO-02)  
**Scale/Scope**: 8 commands, ~40-100 lines each, integration with helpers/templates

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### T0 Rules Compliance

| Rule | Requirement | Status | Notes |
|------|-------------|--------|-------|
| **T0-HEFESTO-01** | Agent Skills Standard | ✅ PASS | Commands generate skills per agentskills.io |
| **T0-HEFESTO-02** | Human Gate Mandatory | ✅ PASS | All writes enforce helpers/human-gate.md |
| **T0-HEFESTO-03** | Progressive Disclosure | ✅ PASS | Each command <500 lines, references helpers |
| **T0-HEFESTO-04** | Multi-CLI Detection | ✅ PASS | Commands use MEMORY.md CLI registry |
| **T0-HEFESTO-05** | Local Storage | ✅ PASS | Persist to CLI-specific directories |
| **T0-HEFESTO-06** | Validation Pre-Persist | ✅ PASS | Use helpers/template-validator.md |
| **T0-HEFESTO-07** | Nomenclatura Padrao | ✅ PASS | Enforce lowercase, hyphen-separated names |
| **T0-HEFESTO-08** | Idempotencia | ✅ PASS | Detect collisions, prompt overwrite/rename |
| **T0-HEFESTO-09** | Compatibilidade CLI | ✅ PASS | Use templates/adapters/ |
| **T0-HEFESTO-10** | Citacao de Fontes | ✅ PASS | Prompt for sources in Wizard Mode |
| **T0-HEFESTO-11** | Seguranca | ✅ PASS | Validate inputs, sanitize file paths |

**Result**: ✅ **ALL T0 RULES SATISFIED** - Proceed to implementation

---

## Project Structure

### Documentation (this feature)

```text
specs/003-hefesto-commands/
├── plan.md              # This file
├── research.md          # Phase 0: Command patterns, Wizard, args
├── data-model.md        # Phase 1: Command, Wizard, Human Gate entities
├── quickstart.md        # Phase 1: Developer guide
├── contracts/           # Phase 1: Command contracts
├── checklists/
│   └── requirements.md  # ✅ COMPLETE
└── spec.md              # ✅ COMPLETE
```

### Source Code (repository root)

```text
commands/
├── hefesto.create.md          # ⏳ CREATE
├── hefesto.extract.md         # ⏳ CREATE
├── hefesto.validate.md        # ⏳ CREATE
├── hefesto.adapt.md           # ⏳ CREATE
├── hefesto.sync.md            # ⏳ CREATE
├── hefesto.show.md            # ⏳ CREATE
├── hefesto.delete.md          # ⏳ CREATE
├── hefesto.list.md            # ✅ EXISTS
├── hefesto.help.md            # ✅ EXISTS
│
├── templates/                  # ✅ COMPLETE (Feature 002)
│   ├── skill-template.md
│   ├── metadata-template.yaml
│   └── adapters/              # 8 CLI/MCP adapters
│
└── helpers/                    # ✅ COMPLETE (Features 001-002)
    ├── human-gate.md
    ├── template-validator.md
    ├── adapter-selector.md
    ├── variable-substitution.md
    └── (others)
```

**Structure Decision**: Prompt-based Markdown command definitions executed by AI agents. Foundation and Templates complete, provide all helper infrastructure.

---

## Complexity Tracking

> **No T0 violations** - All requirements comply with T0 rules.

---

## Phase 0: Research (Immediate)

### Objectives

Resolve technical unknowns:
1. Command Definition Patterns - Markdown structure best practices
2. Wizard Mode Implementation - Interactive input gathering
3. Argument Parsing - Positional args + flags strategies
4. Command Integration - Coordination with shared helpers

### Research Questions

| ID | Question | Priority |
|----|----------|----------|
| R-001 | Optimal Markdown command structure? | P1 |
| R-002 | Wizard Mode trigger and management? | P1 |
| R-003 | Argument parsing patterns in prompts? | P1 |
| R-004 | Helper invocation patterns? | P2 |
| R-005 | Command header/frontmatter content? | P2 |
| R-006 | Error handling strategies? | P2 |

### Deliverable

`research.md` with:
- Analysis of existing commands (help, list)
- Command structure recommendations
- Wizard Mode flow diagrams
- Argument parsing patterns
- Helper integration examples
- Error handling strategies

**Time**: 1-2 hours

---

## Phase 1: Design (Post-Research)

### Deliverables

#### 1. Data Model (`data-model.md`)

Define entities:
- Command: name, signature, wizard config, helpers
- Wizard: questions, validation, defaults
- Human Gate: trigger, preview, actions
- Skill: (already defined in Feature 002)

#### 2. Quickstart Guide (`quickstart.md`)

Developer guide:
- Command definition structure
- Wizard Mode implementation
- Human Gate integration
- Helper invocation
- Testing commands
- Common pitfalls

#### 3. Command Contracts (`contracts/`)

Individual contract files for each command:
- Input: args, flags, assumptions
- Output: messages, file ops, MEMORY updates
- Side Effects: filesystem, state
- Error Cases: failures, handling
- Performance: target timing
- Dependencies: helpers, templates, state

**Time**: 2-3 hours

---

## Phase 2: Task Breakdown (Subsequent)

*Use `/speckit.tasks` command - not created by `/speckit.plan`*

---

## Implementation Order

### Priority P1 (Core)

1. `/hefesto.create` - Create from description
2. `/hefesto.extract` - Extract from code
3. `/hefesto.validate` - Validate spec compliance

### Priority P2 (Extended)

4. `/hefesto.adapt` - Adapt for different CLI
5. `/hefesto.sync` - Sync to latest templates
6. `/hefesto.show` - Show specific skill
7. `/hefesto.delete` - Delete with confirmation

### Existing

- `/hefesto.list` - Already implemented
- `/hefesto.help` - Already implemented

---

## Dependencies

### Completed

- ✅ Feature 001: CLI detection, MEMORY.md, helpers (human-gate, error-handling, platform-detection)
- ✅ Feature 002: Templates, adapters, validators

### Required Assumptions

- MEMORY.md has `clis_detected` section
- CLI directories exist
- CONSTITUTION.md valid
- T0 rules enforced at execution

---

## Success Criteria Mapping

| ID | Criterion | Strategy | Validation |
|----|-----------|----------|------------|
| SC-001 | 8/8 commands | Create 7 new + verify 2 existing | Checklist: all .md exist |
| SC-002 | <2s reads | Optimize I/O, minimize reads | Manual timing |
| SC-003 | 100% Human Gate | All writes call human-gate.md | Code review |
| SC-004 | Auto Wizard | Detect missing args, enter interactive | Manual test without args |
| SC-005 | Embedded docs | Usage, examples, troubleshooting | Code review |

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Wizard UX confusion | Medium | Medium | Clear prompts, examples |
| Human Gate bypass | Low | High | Strict template-validator |
| Definition inconsistency | Medium | Medium | Consistent structure template |
| Performance >2s | Low | Medium | Minimize I/O, cache MEMORY.md |
| Name collision edge cases | Medium | Low | Robust prompts (yes/no/rename) |

---

## Open Questions (Resolve in Research)

1. Wizard question formatting?
2. Error message verbosity?
3. Command chaining support?
4. Undo/rollback for deletes?
5. Batch operations support?

---

## Next Steps

### Immediate (This Session)

1. ✅ Generate plan.md
2. ⏳ Create research.md (Phase 0)
3. ⏳ Create data-model.md (Phase 1)
4. ⏳ Create quickstart.md (Phase 1)
5. ⏳ Create contracts/ (Phase 1)

### Subsequent

6. `/speckit.tasks` for task breakdown
7. Implement P1 commands
8. Implement P2 commands
9. Validate against success criteria
10. Update MEMORY.md
11. Update AGENTS.md

---

## Estimated Timeline

| Phase | Deliverable | Time |
|-------|-------------|------|
| Phase 0 | research.md | 1-2h |
| Phase 1 | data-model, quickstart, contracts | 2-3h |
| Phase 2 | Task breakdown | 1h |
| Impl P1 | create, extract, validate | 4-6h |
| Impl P2 | adapt, sync, show, delete | 4-6h |
| Testing | Manual validation | 2-3h |
| **Total** | **Complete** | **14-21h** |

---

## References

- Specification: [spec.md](./spec.md)
- Requirements: [checklists/requirements.md](./checklists/requirements.md)
- Constitution: [CONSTITUTION.md](../../CONSTITUTION.md)
- Templates: [commands/templates/](../../commands/templates/)
- Helpers: [commands/helpers/](../../commands/helpers/)
