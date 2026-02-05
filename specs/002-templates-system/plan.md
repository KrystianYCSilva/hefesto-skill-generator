# Implementation Plan: Templates System

**Branch**: `002-templates-system` | **Date**: 2026-02-04 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/002-templates-system/spec.md`

**Note**: This is a **prompt-based system** where commands are Markdown files executed by AI agents. No traditional programming languages are used.

## Summary

The Templates System provides a base Agent Skills-compliant template, CLI-specific adapters for 7 CLIs + MCP, and a variable substitution system. All templates are stored in `.hefesto/templates/` per project after bootstrap, versioned with Hefesto releases, and validated in-process before persistence. This enables consistent multi-CLI skill generation following T0 constitutional rules.

## Technical Context

**Language/Version**: N/A (Prompt-based Markdown system)  
**Primary Dependencies**: N/A (Self-contained Markdown command definitions)  
**Storage**: Filesystem (`.hefesto/templates/` in user projects)  
**Testing**: Manual validation against Agent Skills spec + idempotency tests  
**Target Platform**: Cross-platform (Windows, macOS, Linux) via AI CLI agents  
**Project Type**: Prompt-based system (Markdown command definitions)  
**Performance Goals**: Variable substitution < 100ms per skill, template validation < 50ms  
**Constraints**: 
- SKILL.md < 500 lines (T0-HEFESTO-03)
- Frontmatter < 100 tokens (ADR-003)
- Templates versioned with Hefesto releases
- No external validator dependencies (in-process validation)
**Scale/Scope**: 9 templates total (1 base + 7 CLI adapters + 1 MCP adapter + 1 metadata template)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### T0 Rules Compliance

| Rule ID | Rule | Status | Justification |
|---------|------|--------|---------------|
| **T0-HEFESTO-01** | Agent Skills Standard | ✅ PASS | Base template validates 100% against agentskills.io spec (FR-001, FR-021) |
| **T0-HEFESTO-02** | Human Gate Obrigatorio | ✅ PASS | Validation failures block persistence, trigger Human Gate (FR-025) |
| **T0-HEFESTO-03** | Progressive Disclosure | ✅ PASS | Base template < 500 lines (FR-003), JIT metadata (FR-006, ADR-003) |
| **T0-HEFESTO-04** | Multi-CLI Deteccao | ✅ PASS | Foundation (CARD-001) provides CLI detection; templates adapt to all detected CLIs |
| **T0-HEFESTO-05** | Armazenamento Local | ✅ PASS | Templates stored in `.hefesto/templates/` per project (FR-020, clarification #6) |
| **T0-HEFESTO-06** | Validacao Spec | ✅ PASS | In-process validation before persistence (FR-012, FR-021, clarification #7) |
| **T0-HEFESTO-07** | Nomenclatura Padrao | ✅ PASS | Variable validation enforces naming rules (FR-013) |
| **T0-HEFESTO-08** | Idempotencia | ✅ PASS | Adapters produce byte-for-byte identical output (FR-015, SC-006) |
| **T0-HEFESTO-09** | Compatibilidade CLI | ✅ PASS | 7 CLI adapters + MCP adapter, CLI-specific syntax transformation (FR-004, FR-005, FR-010) |
| **T0-HEFESTO-10** | Citacao de Fontes | ℹ️ N/A | Templates are structural artifacts, not content requiring citations |
| **T0-HEFESTO-11** | Seguranca por Padrao | ✅ PASS | Variable validation prevents injection (FR-008), escape mechanism provided (FR-016) |

**Overall Status**: ✅ **ALL APPLICABLE T0 RULES PASS**

No constitutional violations. No complexity justification required.

## Project Structure

### Documentation (this feature)

```text
specs/002-templates-system/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/speckit.plan output)
├── research.md          # Phase 0 output (below)
├── data-model.md        # Phase 1 output (below)
├── quickstart.md        # Phase 1 output (below)
├── contracts/           # Phase 1 output (N/A - no API contracts for prompt system)
├── checklists/
│   └── requirements.md  # Requirements validation (completed)
└── tasks.md             # Phase 2 output (/speckit.tasks - NOT created by /speckit.plan)
```

### Source Code (repository root)

**Structure Decision**: This is a **prompt-based system** where commands are Markdown files, not traditional code. The "implementation" consists of creating template files and helper command definitions.

```text
commands/
├── templates/
│   ├── skill-template.md          # Base Agent Skills template
│   ├── metadata-template.yaml     # Expanded metadata template
│   └── adapters/
│       ├── claude.adapter.md      # Claude Code adapter
│       ├── gemini.adapter.md      # Gemini CLI adapter
│       ├── codex.adapter.md       # OpenAI Codex adapter
│       ├── copilot.adapter.md     # VS Code/Copilot adapter
│       ├── opencode.adapter.md    # OpenCode adapter
│       ├── cursor.adapter.md      # Cursor adapter
│       ├── qwen.adapter.md        # Qwen Code adapter
│       └── mcp.adapter.md         # MCP server adapter
│
└── helpers/
    ├── variable-substitution.md   # Variable replacement logic
    ├── template-validator.md      # Agent Skills spec validation
    └── adapter-selector.md        # CLI adapter selection logic
```

**Deployment**: Templates copied to `.hefesto/templates/` in user projects during `/hefesto.init`

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

**No violations** - This section intentionally left empty.

---

## Phase 0: Research & Decision Making

### Research Questions

1. **Agent Skills Specification Deep Dive**
   - What are the exact YAML frontmatter validation rules?
   - What Markdown structures are required/forbidden in skill body?
   - What are the size/token limits for each field?
   - How do different CLIs interpret the same Agent Skills file?

2. **CLI-Specific Syntax Requirements**
   - What argument syntaxes do each of the 7 CLIs use?
   - Which CLIs support `$ARGUMENTS` vs `{{args}}`?
   - Are there CLI-specific extensions beyond Agent Skills spec?
   - What metadata fields does each CLI recognize vs ignore?

3. **MCP Specification 2024-11-05**
   - What is the server structure for MCP 2024-11-05?
   - How are tools/resources exposed in MCP servers?
   - What transport mechanisms are required?
   - How do we map Agent Skills frontmatter to MCP tool metadata?

4. **Variable Substitution Best Practices**
   - What template engines/patterns exist for Markdown?
   - How do we handle escaping of variable-like syntax in documentation?
   - What validation is needed before substitution?
   - How do we ensure idempotent transformations?

5. **Template Versioning Strategy**
   - How do we track template versions in MEMORY.md?
   - What happens during Hefesto version upgrades?
   - How do users safely update templates without breaking existing skills?
   - What migration path exists for breaking template changes?

### Research Findings

*(To be filled during Phase 0 execution - create `research.md`)*

---

## Phase 1: Design

### Data Model

*(To be filled during Phase 1 execution - create `data-model.md`)*

**Key Entities** (from spec.md):

1. **Template**
   - file_path: string (relative to `.hefesto/templates/`)
   - content: string (Markdown with variables)
   - variables: list[Variable]
   - validation_status: boolean
   - format: enum (base | adapter | metadata)
   - version: string (matches Hefesto version)

2. **Variable**
   - name: string (`{{SKILL_NAME}}`, `{{SKILL_DESCRIPTION}}`, etc.)
   - value: string | null
   - required: boolean
   - default_value: string | null
   - validation_rules: regex | enum

3. **Adapter**
   - target_cli: enum (claude | gemini | codex | copilot | opencode | cursor | qwen | mcp)
   - input_template: Template
   - output_format: string
   - transformation_rules: list[Rule]
   - idempotency_hash: string

4. **Metadata Structure**
   - frontmatter_fields: dict (4 required: name, description, license, metadata)
   - metadata_yaml_fields: dict (11 optional from ADR-002)
   - jit_resources: dict (scripts/, references/, assets/ paths)

5. **Validation Result**
   - is_valid: boolean
   - errors: list[ValidationError]
   - warnings: list[string]
   - spec_version: string
   - validation_rules_applied: list[ValidationRule]

6. **Validation Error**
   - rule_id: string (e.g., "T0-HEFESTO-07")
   - field_name: string
   - actual_value: string
   - expected_constraint: string
   - suggestion: string (actionable fix)

7. **Validation Rule**
   - rule_id: string
   - description: string
   - validator_function: predicate
   - error_message_template: string

### API Contracts

**N/A** - This is a prompt-based system with no API endpoints. Interaction model:

1. **User invokes command** (e.g., `/hefesto.create`)
2. **AI agent reads** templates from `.hefesto/templates/`
3. **AI agent substitutes** variables based on user input
4. **AI agent validates** output against Agent Skills spec
5. **AI agent presents** result via Human Gate
6. **User approves/rejects** via CLI interaction
7. **AI agent persists** to appropriate CLI skills directory

### Quickstart Guide

*(To be filled during Phase 1 execution - create `quickstart.md`)*

---

## Phase 2: Task Planning

**OUT OF SCOPE** for `/speckit.plan` - Run `/speckit.tasks` next to generate task breakdown.

---

## Success Metrics (from spec.md)

| ID | Metric | Target | Verification Method |
|----|--------|--------|---------------------|
| SC-001 | Agent Skills validation pass rate | 100% | Validate 20 generated skills against spec |
| SC-002 | CLI adapter validity | 100% for all 7 CLIs | Test each adapter against official CLI docs |
| SC-003 | Variable substitution performance | < 100ms per skill | Benchmark with 100 skills |
| SC-004 | Base template size | < 500 lines | Line count check |
| SC-005 | Frontmatter token count | < 100 tokens | Token counter on generated frontmatter |
| SC-006 | Adapter idempotency | 100 consecutive identical runs | Hash comparison across 100 runs |
| SC-007 | Metadata.yaml skill size | < 500 lines in SKILL.md | Line count with metadata.yaml present |
| SC-008 | MCP server success rate | 100% start + query | Integration test with MCP client |
| SC-009 | Edge case handling | 95%+ without crashes | Test 20 edge cases from spec |
| SC-011 | Validation error quality | 100% include suggestions | Audit 50 validation error messages |
| SC-010 | Documentation completeness | All templates documented | Manual review of usage examples |

---

## Dependencies

**Completed**:
- ✅ CARD-001 (Hefesto Foundation Infrastructure) - Provides CLI detection, state persistence (MEMORY.md), constitutional validation

**Referenced ADRs**:
- ADR-001: Agent Skills Standard - Base format for all templates
- ADR-002: Research Integration - MCP adapter, security rules (T0-HEFESTO-11)
- ADR-003: Lightweight Frontmatter - Two-tier metadata (frontmatter + metadata.yaml)

**External Specifications**:
- Agent Skills Specification (agentskills.io) - Validation rules encoded in-process
- Model Context Protocol 2024-11-05 or higher - MCP adapter target

---

## Next Steps

1. **Run `/speckit.tasks`** to generate detailed task breakdown from this plan
2. **Phase 0**: Create `research.md` answering the 5 research questions above
3. **Phase 1**: Create `data-model.md` expanding the 7 key entities
4. **Phase 1**: Create `quickstart.md` for template usage
5. **Phase 2**: Execute tasks generated by `/speckit.tasks`

---

**Plan Status**: ✅ Complete - Ready for `/speckit.tasks`  
**Constitutional Status**: ✅ All T0 rules pass  
**Technical Risks**: Low (prompt-based system, no code dependencies)
