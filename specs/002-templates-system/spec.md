---
description: "Feature specification for Templates System with base skill template, CLI adapters, and variable substitution"
feature: "002-templates-system"
type: "specification"
status: "draft"
created: "2026-02-04"
version: "1.0.0"
---

# Feature Specification: Templates System

**Feature Branch**: `002-templates-system`  
**Created**: 2026-02-04  
**Status**: Draft  
**Input**: User description: "CARD-002-templates.md para implementação do PLAN-001-hefesto-v1.md e seguindo as adrs"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate Agent Skills Compliant Template (Priority: P1)

As a skill generator system, I want to provide a base skill template that follows the Agent Skills specification so that all generated skills are valid, standardized, and compatible with the ecosystem regardless of target CLI.

**Why this priority**: This is the foundation of the entire templates system. Without a valid base template, no CLI adapter can function correctly, and skills cannot be generated.

**Independent Test**: Can be fully tested by generating a skill from the base template with sample data and validating it against the official Agent Skills specification validator without requiring CLI adapters or variable substitution.

**Acceptance Scenarios**:

1. **Given** the base skill template with placeholder variables, **When** I substitute valid values for name and description, **Then** the output passes 100% of Agent Skills spec validation rules
2. **Given** a skill body that exceeds 500 lines, **When** I use the base template, **Then** the template structure automatically suggests moving content to references/ directory following T0-HEFESTO-03
3. **Given** the base template with lightweight frontmatter, **When** I generate a skill, **Then** the frontmatter contains only 4 fields (name, description, license, metadata pointer) and is under 100 tokens per ADR-003

---

### User Story 2 - Transform Base Template for Specific CLI (Priority: P1)

As a skill generator, I want CLI-specific adapters that transform the base template into the exact format required by each target CLI so that generated skills work immediately without manual adjustments.

**Why this priority**: Enables multi-CLI support which is a core value proposition. Each adapter can be independently tested and deployed.

**Independent Test**: Can be tested by taking a valid base template, applying a single CLI adapter (e.g., Claude adapter), and verifying the output matches the official Claude Code skill format without requiring other adapters.

**Acceptance Scenarios**:

1. **Given** the base template with `{{ARGUMENTS}}` placeholder, **When** I apply the Claude adapter, **Then** the output uses `$ARGUMENTS` syntax per Claude Code documentation
2. **Given** the base template with `{{ARGUMENTS}}` placeholder, **When** I apply the Gemini adapter, **Then** the output uses `{{args}}` syntax per Gemini CLI documentation
3. **Given** a base template, **When** I apply any CLI adapter twice with the same input, **Then** both outputs are byte-for-byte identical (idempotent per RQ03)

---

### User Story 3 - Substitute Variables in Templates (Priority: P1)

As a skill generator, I want a variable substitution system that replaces placeholders with actual skill data so that templates can be reused with different content while maintaining structure.

**Why this priority**: Without variable substitution, templates are static and unusable. This is the mechanism that makes templates functional.

**Independent Test**: Can be tested by creating a template with all supported variables, providing test values, and verifying correct substitution in the output without requiring template validation or CLI adapters.

**Acceptance Scenarios**:

1. **Given** a template containing `{{SKILL_NAME}}`, **When** I substitute with "data-validator", **Then** the output contains "data-validator" in all locations where the variable appeared
2. **Given** a template with `{{CREATED_DATE}}`, **When** I substitute without providing a date, **Then** the system automatically uses the current date in ISO 8601 format
3. **Given** a template with undefined variable `{{UNKNOWN}}`, **When** I attempt substitution, **Then** the system raises a validation error listing the undefined variable before persistence

---

### User Story 4 - Generate Skills with JIT Metadata Structure (Priority: P2)

As a skill generator, I want to create skills with a two-tier metadata structure (lightweight frontmatter + JIT metadata.yaml) so that skills remain under 500 lines while supporting rich metadata per ADR-003.

**Why this priority**: Enables advanced metadata without violating T0-HEFESTO-03. The system can function with basic frontmatter only, but this enables discovery and documentation.

**Independent Test**: Can be tested by generating a skill with expanded metadata, verifying SKILL.md remains under the line limit while metadata.yaml contains complete information, and confirming an agent can load metadata only when needed.

**Acceptance Scenarios**:

1. **Given** a skill with 15 metadata fields, **When** I generate using the two-tier structure, **Then** SKILL.md frontmatter contains only 4 fields while metadata.yaml contains all 15
2. **Given** a skill without the `metadata:` field in frontmatter, **When** an agent loads it, **Then** the skill functions normally without attempting to load metadata.yaml
3. **Given** a skill with `metadata: ./metadata.yaml` field, **When** an agent needs version information, **Then** the system loads metadata.yaml on-demand without loading scripts/ or references/

---

### User Story 5 - Export Skills as MCP Servers (Priority: P3)

As a skill generator, I want to provide an MCP adapter that converts Agent Skills into Model Context Protocol servers so that skills can be exposed to any MCP-compatible client (Gemini CLI, Codex, Copilot, Cursor) per ADR-002.

**Why this priority**: Enables future interoperability and research integration, but the system provides full value through direct CLI skills without MCP.

**Independent Test**: Can be tested by converting a skill using the MCP adapter, starting the resulting MCP server, connecting an MCP client, and verifying the skill is discoverable and invocable without requiring other adapters.

**Acceptance Scenarios**:

1. **Given** a valid Agent Skills SKILL.md, **When** I apply the MCP adapter, **Then** the output is a valid MCP server following the Model Context Protocol specification
2. **Given** an MCP-adapted skill, **When** I start the server and query available tools, **Then** the skill appears with its name and description from the original frontmatter
3. **Given** multiple skills adapted to MCP, **When** I deploy them, **Then** each runs as an independent server without shared state or conflicts

---

### Edge Cases

- When a template contains a variable that is not in the official variable list (e.g., `{{CUSTOM_VAR}}`), the system raises a validation error during generation listing all unrecognized variables and suggesting the official list from RT05
- When a CLI adapter is applied to a template missing required variables for that CLI (e.g., Claude adapter but no `{{ARGUMENTS}}`), the adapter inserts a sensible default value and logs a warning about the missing variable
- When substituting `{{SKILL_NAME}}` with a value containing invalid characters (uppercase, spaces, special chars), the system rejects the value before any substitution occurs with reference to T0-HEFESTO-07 naming rules
- When a skill body contains literal text that looks like a variable (e.g., documentation showing `{{EXAMPLE}}`), the system provides an escape mechanism (double braces: `{{{{EXAMPLE}}}}` renders as `{{EXAMPLE}}`) to prevent unwanted substitution
- When generating a skill with metadata.yaml but the target CLI doesn't support custom metadata files, the adapter flattens relevant metadata fields into the main SKILL.md as comments to preserve information without breaking compatibility
- When applying multiple adapters sequentially (e.g., base → Claude → MCP), the system validates that each transformation preserves the Agent Skills structure and warns if adapter ordering creates conflicts
- When a template references external resources via relative paths (e.g., `./scripts/helper.sh`) but the target directory structure doesn't match, the adapter adjusts paths or fails with clear instructions about expected structure

## Clarifications

### Session 2026-02-04

- Q: When a template contains unrecognized variables, should the system fail immediately or attempt substitution? → A: Fail immediately with validation error listing all unrecognized variables and suggest the official variable list
- Q: When a CLI adapter is missing required variables, what default behavior should occur? → A: Insert sensible default value specific to that CLI and log a warning about the missing variable
- Q: When skill bodies contain literal text resembling variables, how can users escape them? → A: Provide double-brace escape mechanism where `{{{{VAR}}}}` renders as `{{VAR}}`
- Q: When CLIs don't support metadata.yaml, how should adapters handle expanded metadata? → A: Flatten relevant metadata into main SKILL.md as comments to preserve information
- Q: When applying adapters sequentially, what validation should occur? → A: Validate each transformation preserves Agent Skills structure and warn about adapter ordering conflicts

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a base skill template (skill-template.md) that validates against the Agent Skills specification without any modifications
- **FR-002**: Base template MUST include YAML frontmatter with exactly 4 fields: name, description, license, metadata (per ADR-003)
- **FR-003**: Base template MUST support Progressive Disclosure with core content under 500 lines (T0-HEFESTO-03)
- **FR-004**: System MUST provide 7 CLI adapters: claude.adapter.md, gemini.adapter.md, codex.adapter.md, copilot.adapter.md, opencode.adapter.md, cursor.adapter.md, qwen.adapter.md
- **FR-005**: System MUST provide 1 MCP adapter: mcp.adapter.md for Model Context Protocol server generation
- **FR-006**: System MUST provide a metadata.yaml template with all 15 expanded metadata fields documented in ADR-002
- **FR-007**: Variable substitution system MUST support exactly these variables: `{{SKILL_NAME}}`, `{{SKILL_DESCRIPTION}}`, `{{SKILL_BODY}}`, `{{CREATED_DATE}}`, `{{VERSION}}`, `{{ARGUMENTS}}`
- **FR-008**: System MUST validate variable names against the official list (RT05) before substitution occurs
- **FR-009**: System MUST automatically populate `{{CREATED_DATE}}` with current ISO 8601 timestamp if not provided
- **FR-010**: CLI adapters MUST transform `{{ARGUMENTS}}` to CLI-specific syntax: `$ARGUMENTS` for Claude/Codex/Copilot/OpenCode/Cursor, `{{args}}` for Gemini/Qwen
- **FR-011**: System MUST validate that generated SKILL.md frontmatter is under 100 tokens (ADR-003)
- **FR-012**: System MUST validate generated skills against Agent Skills specification before persistence
- **FR-013**: System MUST enforce naming rules (T0-HEFESTO-07): lowercase, hyphens, max 64 chars for `{{SKILL_NAME}}` substitution
- **FR-014**: System MUST create directory structure for JIT resources: scripts/, references/, assets/ when requested
- **FR-015**: Adapters MUST be idempotent - same input produces byte-for-byte identical output (RQ03)
- **FR-016**: System MUST provide escape mechanism for literal variable syntax in skill bodies (double braces)
- **FR-017**: System MUST handle missing adapter variables by inserting CLI-specific defaults and logging warnings
- **FR-018**: System MUST validate adapter transformations preserve Agent Skills structure when chaining adapters
- **FR-019**: System MUST adjust relative paths in templates when target directory structure differs

### Key Entities *(include if feature involves data)*

- **Template**: Represents a reusable skill structure with attributes: file path, content (string), variables (list), validation status (boolean), format (base | adapter | metadata)
- **Variable**: Represents a substitution placeholder with attributes: name (string), value (string | null), required (boolean), default value (string | null), validation rules (regex | enum)
- **Adapter**: Represents a CLI-specific transformation with attributes: target CLI (enum), input template (Template), output format (string), transformation rules (list), idempotency hash (string)
- **Metadata Structure**: Represents JIT metadata with attributes: frontmatter fields (4 required), metadata.yaml fields (11 optional per ADR-002), JIT resources (scripts/references/assets paths)
- **Validation Result**: Represents template validation outcome with attributes: is valid (boolean), errors (list of strings), warnings (list of strings), spec version (string)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of skills generated from base template pass Agent Skills specification validation without modifications
- **SC-002**: CLI adapters generate valid skills for all 7 supported CLIs without manual adjustments in 100% of test cases
- **SC-003**: Variable substitution completes in under 100ms per skill (RQ04)
- **SC-004**: Base template SKILL.md is under 500 lines (T0-HEFESTO-03)
- **SC-005**: Frontmatter in generated skills is under 100 tokens (ADR-003)
- **SC-006**: Adapters produce identical output when given identical input in 100 consecutive runs (idempotency)
- **SC-007**: Skills with metadata.yaml remain under 500 lines in SKILL.md while supporting 15+ metadata fields
- **SC-008**: MCP adapter generates servers that successfully start and respond to tool queries in 100% of integration tests
- **SC-009**: Template generation handles 95%+ of edge cases (undefined variables, escape sequences, missing defaults) without crashes
- **SC-010**: All templates and adapters are documented with usage examples and integrate with `/hefesto.create` command

### Assumptions

- Users generate skills using commands that invoke templates (templates are not manually edited by users)
- CLI adapters are maintained as the respective CLI documentation evolves
- The Agent Skills specification remains stable during development or changes are backward compatible
- The Model Context Protocol (MCP) specification is sufficiently stable for adapter implementation
- Users have at least one of the 7 supported CLIs installed when generating skills
- Skills generated for a specific CLI are deployed to that CLI's designated skills directory (e.g., .claude/skills/)
- Variable values provided by users or commands are pre-sanitized for basic security (no injection attacks via templates)
- JIT metadata loading is supported by the AI agents consuming the skills (or gracefully ignored if not)
- Template files themselves are stored in the Hefesto repository, not in individual user projects
- The foundation infrastructure (CARD-001) is complete and provides CLI detection, state persistence, and constitutional validation

---

**Status**: Draft - Ready for `/speckit.plan`  
**Dependencies**: CARD-001 (Hefesto Foundation Infrastructure - Complete)  
**ADRs Referenced**: ADR-001 (Agent Skills Standard), ADR-002 (Research Integration), ADR-003 (Lightweight Frontmatter)
