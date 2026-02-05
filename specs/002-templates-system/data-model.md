# Data Model: Templates System

**Feature**: 002-templates-system  
**Date**: 2026-02-04  
**Phase**: 1 (Design)

## Overview

This document defines the conceptual data model for the Templates System. Since this is a **prompt-based system** (Markdown command definitions, not traditional code), these are logical entities that guide template structure and validation logic.

---

## Entity Definitions

### 1. Template

**Purpose**: Represents a reusable skill structure with variables

**Attributes**:
- `file_path`: string - Relative path from `.hefesto/templates/` (e.g., `skill-template.md`, `adapters/claude.adapter.md`)
- `content`: string - Full Markdown content including frontmatter and body with variable placeholders
- `variables`: list[Variable] - All variables found in template (extracted via regex `{{[A-Z_]+}}`)
- `validation_status`: boolean - Whether template itself is valid (checked on load)
- `format`: enum - Template type
  - `base`: Main skill template (skill-template.md)
  - `adapter`: CLI-specific transformation (adapters/*.adapter.md)
  - `metadata`: Metadata template (metadata-template.yaml)
- `version`: string - Matches Hefesto version (e.g., "1.0.0")

**Lifecycle**:
1. **Bootstrap**: Copied from Hefesto source to `.hefesto/templates/` during `/hefesto.init`
2. **Load**: Read into memory when skill generation command invoked
3. **Validate**: Check format enum, variable syntax, version match
4. **Update**: Re-copied when user runs `/hefesto.init` after Hefesto upgrade

**Validation Rules**:
- File must exist at `file_path`
- Content must be valid Markdown with YAML frontmatter (for skill templates)
- Version must match Hefesto version (warn if mismatch)
- Variables must use `{{VAR}}` syntax

---

### 2. Variable

**Purpose**: Represents a substitution placeholder in templates

**Attributes**:
- `name`: string - Variable identifier (e.g., "SKILL_NAME", "SKILL_DESCRIPTION", "ARGUMENTS")
- `value`: string | null - Actual value to substitute (null before substitution)
- `required`: boolean - Whether variable must be provided by user
- `default_value`: string | null - Fallback if not provided (e.g., current date for CREATED_DATE)
- `validation_rules`: regex | enum - Constraints on value
  - `SKILL_NAME`: `/^[a-z0-9]+(-[a-z0-9]+)*$/` (T0-HEFESTO-07)
  - `SKILL_DESCRIPTION`: Non-empty, ≤1024 chars
  - `CREATED_DATE`: ISO 8601 format

**Official Variable List** (FR-007):
| Variable | Required | Default | Validation |
|----------|----------|---------|------------|
| `{{SKILL_NAME}}` | Yes | (none) | T0-HEFESTO-07 naming rules |
| `{{SKILL_DESCRIPTION}}` | Yes | (none) | ≤1024 chars, non-empty |
| `{{SKILL_BODY}}` | Yes | (none) | Any Markdown |
| `{{CREATED_DATE}}` | No | Current ISO 8601 | ISO 8601 format |
| `{{VERSION}}` | No | "1.0.0" | SemVer format |
| `{{ARGUMENTS}}` | No | (empty) | CLI-specific transformation |

**Substitution Process**:
1. **Extract**: Find all `{{...}}` in template
2. **Validate**: Check against official list (FR-008)
3. **Escape**: Process `{{{{VAR}}}}` → `{{VAR}}` (research.md Q4)
4. **Replace**: Substitute values (single pass, deterministic order)
5. **Verify**: Ensure no remaining unescaped `{{...}}`

---

### 3. Adapter

**Purpose**: Represents CLI-specific transformation rules

**Attributes**:
- `target_cli`: enum - Target CLI identifier
  - `claude` | `gemini` | `codex` | `copilot` | `opencode` | `cursor` | `qwen` | `mcp`
- `input_template`: Template - Base template to transform (usually skill-template.md)
- `output_format`: string - Expected output structure
- `transformation_rules`: list[Rule] - Ordered list of transformations
  - Example: `{"from": "{{ARGUMENTS}}", "to": "$ARGUMENTS"}` (for Claude)
  - Example: `{"from": "{{ARGUMENTS}}", "to": "{{args}}"}` (for Gemini)
- `idempotency_hash`: string - SHA-256 of (input + transformations) to verify determinism

**CLI-Specific Transformations** (from research.md Q2):

| Adapter File | Target CLI | Key Transformation |
|--------------|------------|-------------------|
| claude.adapter.md | Claude Code | `{{ARGUMENTS}}` → `$ARGUMENTS` |
| gemini.adapter.md | Gemini CLI | `{{ARGUMENTS}}` → `{{args}}` |
| codex.adapter.md | OpenAI Codex | `{{ARGUMENTS}}` → `$ARGUMENTS` |
| copilot.adapter.md | VS Code/Copilot | `{{ARGUMENTS}}` → `$ARGUMENTS` |
| opencode.adapter.md | OpenCode | `{{ARGUMENTS}}` → `$ARGUMENTS` |
| cursor.adapter.md | Cursor | `{{ARGUMENTS}}` → `$ARGUMENTS` |
| qwen.adapter.md | Qwen Code | `{{ARGUMENTS}}` → `{{args}}` |
| mcp.adapter.md | MCP Server | Generate full MCP 2024-11-05 server structure |

**Idempotency Guarantee** (FR-015, SC-006):
- Given same input template + same variable values
- Apply adapter transformations
- Output must be byte-for-byte identical across 100 consecutive runs
- Verified via SHA-256 hash comparison

---

### 4. Metadata Structure

**Purpose**: Represents two-tier metadata design (ADR-003)

**Attributes**:
- `frontmatter_fields`: dict - Lightweight fields in SKILL.md frontmatter
  - Required: `name`, `description`, `license`
  - Optional: `metadata` (pointer to metadata.yaml)
  - Target: ~100 tokens total
- `metadata_yaml_fields`: dict - Expanded fields in metadata.yaml (JIT load)
  - 11 optional fields from ADR-002:
    - `author`, `version`, `created`, `updated`
    - `category`, `tags`, `platforms`
    - `dependencies`, `example_prompt`, `test_cases`, `related_skills`, `sources`
- `jit_resources`: dict - Additional resource paths
  - `scripts/`: Executable resources
  - `references/`: Detailed documentation
  - `assets/`: Static resources (images, etc.)

**Structure Example**:
```yaml
# SKILL.md frontmatter (Tier 1)
---
name: code-review
description: |
  Padroniza code reviews seguindo boas praticas.
  Use quando: revisar PRs, avaliar codigo, aplicar padroes.
license: MIT
metadata: ./metadata.yaml
---
```

```yaml
# metadata.yaml (Tier 2 - JIT)
author: "Hefesto Team <team@example.com>"
version: "1.0.0"
created: 2026-02-04
updated: 2026-02-04
category: development
tags: [code-review, quality, standards]
platforms: [claude, gemini, codex, copilot, opencode, cursor, qwen]
example_prompt: "Review the changes in src/app.js"
```

**Loading Behavior**:
1. Agent always loads SKILL.md (frontmatter + body)
2. Agent loads metadata.yaml only if:
   - `metadata` field present in frontmatter
   - Agent needs expanded metadata (e.g., version info, test cases)
3. Agent loads scripts/references/assets only if:
   - Referenced in skill body
   - Agent needs execution or documentation

---

### 5. Validation Result

**Purpose**: Represents outcome of Agent Skills spec validation

**Attributes**:
- `is_valid`: boolean - Overall validation status
- `errors`: list[ValidationError] - All validation failures (blocks persistence if any)
- `warnings`: list[string] - Non-blocking issues (e.g., missing optional field)
- `spec_version`: string - Agent Skills spec version validated against (e.g., "1.0.0")
- `validation_rules_applied`: list[ValidationRule] - All rules checked

**Validation Flow** (FR-012, FR-025):
1. **Pre-substitution**: Validate variable names against official list
2. **Post-substitution**: Validate generated SKILL.md
3. **Frontmatter check**: name, description fields + constraints
4. **Size check**: < 500 lines (T0-HEFESTO-03), < 100 tokens frontmatter (FR-011)
5. **Security check**: No secrets, sanitized paths (T0-HEFESTO-11)
6. **Result**: If `is_valid = false`, block persistence + trigger Human Gate

**Validation Example**:
```json
{
  "is_valid": false,
  "errors": [
    {
      "rule_id": "T0-HEFESTO-07",
      "field_name": "name",
      "actual_value": "Code-Review",
      "expected_constraint": "lowercase, hyphens only",
      "suggestion": "Use 'code-review'"
    }
  ],
  "warnings": [],
  "spec_version": "1.0.0",
  "validation_rules_applied": ["T0-HEFESTO-01", "T0-HEFESTO-07", "FR-011"]
}
```

---

### 6. Validation Error

**Purpose**: Represents a specific validation failure with actionable suggestion

**Attributes**:
- `rule_id`: string - Constitutional or functional rule violated (e.g., "T0-HEFESTO-07", "FR-011")
- `field_name`: string - Field that failed validation (e.g., "name", "description", "frontmatter")
- `actual_value`: string - What was provided
- `expected_constraint`: string - What rule requires
- `suggestion`: string - Actionable fix (SC-011: 100% of errors have suggestions)

**Error Presentation** (clarification #9):
```
❌ Validation Failed (2 errors):

1. [T0-HEFESTO-07] name: "Code-Review"
   Expected: lowercase, hyphens only
   Suggestion: Use "code-review"

2. [FR-011] Frontmatter: 142 tokens
   Expected: < 100 tokens
   Suggestion: Move metadata to metadata.yaml
```

**User Actions**:
- `[fix]`: Re-run generation with corrected input
- `[cancel]`: Abort generation
- `[ignore]`: NOT available for T0 violations (absolute rules)

---

### 7. Validation Rule

**Purpose**: Represents an Agent Skills specification constraint encoded in-process

**Attributes**:
- `rule_id`: string - Unique identifier (e.g., "agent-skills-name-format")
- `description`: string - Human-readable rule explanation
- `validator_function`: predicate - Logic to check constraint (conceptual - actual implementation in commands)
- `error_message_template`: string - Template for generating ValidationError.suggestion

**Example Rules** (FR-021):

| Rule ID | Description | Validator Logic | Error Template |
|---------|-------------|-----------------|----------------|
| `agent-skills-name-format` | Name must be lowercase, hyphens, max 64 chars | Regex: `^[a-z0-9]+(-[a-z0-9]+)*$` | "Use lowercase with hyphens (e.g., '{suggested_name}')" |
| `agent-skills-description-length` | Description ≤1024 chars, non-empty | `len(desc) > 0 && len(desc) <= 1024` | "Shorten description to {max_length} characters" |
| `hefesto-progressive-disclosure` | SKILL.md < 500 lines | `line_count < 500` | "Move content to references/ directory" |
| `hefesto-frontmatter-tokens` | Frontmatter < 100 tokens | `token_count < 100` | "Move metadata to metadata.yaml" |

**No External Dependencies** (clarification #7):
- All validation rules encoded directly in Hefesto commands
- No npm packages, Python libraries, or external validators
- Enables offline operation (FR-007 assumption)

---

## Relationships

```
Template (1) ──contains──> (*) Variable
   │
   │ is_transformed_by
   ↓
Adapter (1) ──produces──> (1) Template (output)
   │
   │ validated_by
   ↓
ValidationResult (1) ──contains──> (*) ValidationError
   │                      │
   │                      └──references──> (1) ValidationRule
   │
   └──validates──> (1) Template

MetadataStructure (1) ──embedded_in──> (1) Template (frontmatter + pointer)
```

---

## State Transitions

### Template Lifecycle

```
[Hefesto Source] 
     │
     │ /hefesto.init
     ↓
[.hefesto/templates/] ──┐
     │                  │
     │ skill generation │ version mismatch
     ↓                  │
[Loaded in Memory]     │
     │                  │
     │ substitution     │
     ↓                  │
[Generated Skill]      │
     │                  │
     │ validation       │
     ↓                  ↓
[Validated] ───────> [Outdated Warning]
     │                  │
     │ Human Gate       │ user action
     ↓                  ↓
[Persisted]       [Re-init with Backup]
```

---

## Constraints & Invariants

### Mandatory Constraints

1. **T0-HEFESTO-01**: Template frontmatter MUST have `name` + `description`
2. **T0-HEFESTO-03**: Template SKILL.md MUST be < 500 lines
3. **T0-HEFESTO-07**: Variable `{{SKILL_NAME}}` value MUST match `/^[a-z0-9]+(-[a-z0-9]+)*$/`
4. **FR-015**: Adapter transformations MUST be idempotent

### Invariants

1. **Version consistency**: Template.version ALWAYS equals MEMORY.md hefesto.templates.version after init
2. **Variable completeness**: Template NEVER contains variables outside official list (FR-007)
3. **Escape precedence**: `{{{{VAR}}}}` ALWAYS processed before `{{VAR}}` substitution
4. **Validation before persistence**: Template NEVER persisted if ValidationResult.is_valid = false

---

## Performance Characteristics

**Target Performance** (from plan.md):
- Variable substitution: < 100ms per skill
- Template validation: < 50ms per skill
- Adapter transformation: < 75ms per skill

**Optimization Strategies** (from research.md):
- Preload templates into memory (avoid disk I/O)
- Cache compiled validation rules
- Single-pass string replacement
- Use exact string matching over regex where possible

---

## Security Considerations

**T0-HEFESTO-11 Compliance**:
- **Input validation**: Sanitize `{{SKILL_NAME}}` against path traversal (`../`, `./`)
- **Output sanitization**: Strip executable code, ANSI escapes
- **Least privilege**: Templates never require elevated permissions
- **Secret detection**: Block if secrets/tokens found in template content

---

## Next Steps

1. Create `quickstart.md` with template usage examples
2. Run `/speckit.tasks` to generate implementation tasks
3. Implement templates following this data model
4. Validate against Agent Skills spec and constitutional rules

---

**Data Model Status**: ✅ Complete  
**Next**: Create quickstart.md (Phase 1)
