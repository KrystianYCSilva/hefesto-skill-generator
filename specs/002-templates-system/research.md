# Research: Templates System

**Feature**: 002-templates-system  
**Date**: 2026-02-04  
**Phase**: 0 (Research & Decision Making)

## Purpose

This document resolves all technical unknowns identified in `plan.md` to enable informed design decisions in Phase 1.

---

## Research Question 1: Agent Skills Specification Deep Dive

**Question**: What are the exact YAML frontmatter validation rules, Markdown structures, size/token limits, and CLI interpretation differences?

### Findings

**YAML Frontmatter Rules** (from T0-HEFESTO-01 + ADR-001):
- **Mandatory fields**: `name`, `description`
- **`name` validation**:
  - Max 64 characters
  - Lowercase only
  - Alphanumeric + hyphens
  - Cannot start/end with hyphen
  - No consecutive hyphens
  - Regex: `^[a-z0-9]+(-[a-z0-9]+)*$`
- **`description` validation**:
  - Max 1024 characters
  - Must not be empty
  - Should include "Use when:" trigger (T1-HEFESTO-01)
- **Optional fields**: `license`, `metadata` (pointer to metadata.yaml)

**Markdown Body**:
- Standard CommonMark syntax
- No specific structural requirements from Agent Skills spec
- T0-HEFESTO-03 limit: < 500 lines total (including frontmatter)

**Token Limits** (from ADR-003):
- Frontmatter target: ~100 tokens (4 fields only)
- Full SKILL.md: < 5000 tokens

**CLI Interpretation Differences**:
| CLI | Frontmatter | Body | Custom Extensions |
|-----|-------------|------|-------------------|
| Claude Code | YAML | Markdown | context:fork directive |
| Gemini CLI | YAML or TOML | Markdown | {{args}} syntax |
| OpenAI Codex | YAML | Markdown | Standard |
| VS Code/Copilot | YAML | Markdown | GitHub-specific metadata |
| OpenCode | YAML | Markdown | $ARGUMENTS syntax |
| Cursor | YAML | Markdown | Standard |
| Qwen Code | YAML | Markdown | {{args}} syntax |

**Decision**: Use YAML frontmatter with 4 fields max (T0-compliant). Ignore CLI-specific extensions in base template; handle in adapters.

---

## Research Question 2: CLI-Specific Syntax Requirements

**Question**: What argument syntaxes, metadata support, and CLI-specific extensions exist across 7 CLIs?

### Findings

**Argument Syntax Mapping** (from T0-HEFESTO-09):

| CLI | Argument Syntax | Example |
|-----|-----------------|---------|
| Claude Code | `$ARGUMENTS` | `Review code in $ARGUMENTS` |
| Gemini CLI | `{{args}}` | `Review code in {{args}}` |
| OpenAI Codex | `$ARGUMENTS` | `Review code in $ARGUMENTS` |
| VS Code/Copilot | `$ARGUMENTS` | `Review code in $ARGUMENTS` |
| OpenCode | `$ARGUMENTS` | `Review code in $ARGUMENTS` |
| Cursor | `$ARGUMENTS` | `Review code in $ARGUMENTS` |
| Qwen Code | `{{args}}` | `Review code in {{args}}` |

**Metadata Field Support**:
- **All CLIs**: Support `name`, `description` (Agent Skills spec)
- **Most CLIs**: Recognize `license`, `version`, `author` but don't enforce
- **Claude Code**: Uses `context:fork` for skill composition
- **Gemini CLI**: Supports TOML as alternative format
- **VS Code/Copilot**: Recognizes GitHub-specific fields (team, repo)

**CLI-Specific Extensions**:
- **NOT included in base template** (violates portability)
- **Handled via adapters** where beneficial

**Decision**: 
- Base template uses `{{ARGUMENTS}}` placeholder
- Adapters transform to `$ARGUMENTS` (Claude, Codex, Copilot, OpenCode, Cursor) or `{{args}}` (Gemini, Qwen)
- No CLI-specific extensions in base template

---

## Research Question 3: MCP Specification 2024-11-05

**Question**: What is the MCP 2024-11-05 server structure, tool exposure mechanism, and mapping from Agent Skills?

### Findings

**MCP Server Structure** (Model Context Protocol 2024-11-05):

```typescript
// MCP Server Interface
interface MCPServer {
  protocol_version: "2024-11-05" | "2024-11-05.1";
  server_info: ServerInfo;
  capabilities: ServerCapabilities;
  tools: Tool[];
  resources?: Resource[];
}

interface Tool {
  name: string;           // Maps to Agent Skills `name`
  description: string;    // Maps to Agent Skills `description`
  input_schema: JSONSchema;  // Generated from skill parameters
}
```

**Tool Exposure**:
- Tools exposed via JSON-RPC 2.0 protocol
- Supported transports: stdio, HTTP, SSE
- Each skill becomes one MCP tool

**Agent Skills → MCP Mapping**:

| Agent Skills Field | MCP Field | Transformation |
|--------------------|-----------|----------------|
| `name` | `tool.name` | Direct copy |
| `description` | `tool.description` | Direct copy |
| `{{ARGUMENTS}}` | `input_schema.properties.args` | Extract parameter schema |
| Body content | Tool implementation | Embedded as prompt template |
| `license` | `server_info.license` | Direct copy |

**MCP Adapter Output Structure**:
```javascript
// mcp-server-{skill-name}.js
{
  "protocol_version": "2024-11-05",
  "server_info": {
    "name": "skill-name-server",
    "version": "1.0.0"
  },
  "tools": [{
    "name": "skill-name",
    "description": "...",
    "input_schema": {
      "type": "object",
      "properties": {
        "args": {"type": "string", "description": "Arguments for skill"}
      }
    }
  }]
}
```

**Decision**: 
- MCP adapter generates standalone Node.js server file
- One skill = one MCP tool
- Use stdio transport (simplest, most compatible)
- Target MCP spec 2024-11-05 (clarification #10)

---

## Research Question 4: Variable Substitution Best Practices

**Question**: What patterns exist for Markdown template engines, escape mechanisms, validation needs, and idempotency guarantees?

### Findings

**Template Engine Patterns**:
- **Mustache**: `{{VAR}}` syntax, widely supported, no logic
- **Handlebars**: `{{VAR}}` with helpers, adds complexity
- **Jinja2**: `{{ VAR }}` (spaces), Python-specific
- **Custom**: Double brace `{{VAR}}` format, minimal dependencies

**Escape Mechanism** (from clarification #3):
- Problem: Documentation showing `{{EXAMPLE}}` gets substituted
- Solution: Double-double braces: `{{{{VAR}}}}` → `{{VAR}}`
- Precedence: Process escapes before substitutions

**Validation Requirements** (from FR-008, clarification #1):
1. **Before substitution**:
   - Check all variables in template are in official list (FR-007)
   - Fail immediately with error listing unknowns
2. **Variable values**:
   - `{{SKILL_NAME}}`: Apply T0-HEFESTO-07 naming rules
   - `{{SKILL_DESCRIPTION}}`: Max 1024 chars, non-empty
   - `{{CREATED_DATE}}`: Auto-populate if missing (ISO 8601)
3. **After substitution**:
   - Validate against Agent Skills spec (FR-012)
   - Check SKILL.md < 500 lines (FR-003)
   - Check frontmatter < 100 tokens (FR-011)

**Idempotency Guarantees** (FR-015, SC-006):
- Same input → same output (byte-for-byte)
- No timestamps unless provided
- No random IDs
- Deterministic ordering (sort keys alphabetically)
- Hash verification: SHA-256 of output

**Decision**:
- Use `{{VAR}}` syntax (Mustache-like, no dependencies)
- Implement `{{{{VAR}}}}` escape (process first)
- Validate variables before substitution
- Validate output after substitution
- Compute SHA-256 hash for idempotency tests

---

## Research Question 5: Template Versioning Strategy

**Question**: How do we track versions in MEMORY.md, handle upgrades, enable safe updates, and provide migration paths?

### Findings

**Version Tracking in MEMORY.md** (from FR-022, FR-024):
```yaml
# MEMORY.md
hefesto:
  version: "1.0.0"
  templates:
    version: "1.0.0"          # Matches Hefesto version
    last_updated: "2026-02-04T10:30:00Z"
    location: ".hefesto/templates/"
```

**Upgrade Scenarios**:

| Scenario | Hefesto Version | Template Version | Action |
|----------|-----------------|------------------|--------|
| Fresh init | 1.0.0 | (none) | Copy templates v1.0.0 |
| Re-init same version | 1.0.0 | 1.0.0 | Skip copy (idempotent) |
| Hefesto upgraded | 1.1.0 | 1.0.0 | Warn user to run `/hefesto.init` |
| Re-init after upgrade | 1.1.0 | 1.0.0 | Backup old, copy new templates |

**Safe Update Process** (from FR-023, clarification #8):
1. Detect version mismatch (MEMORY.md templates.version < Hefesto version)
2. Warn user: "Templates outdated. Run `/hefesto.init` to update."
3. On `/hefesto.init`:
   - Backup `.hefesto/templates/` to `.hefesto/templates.backup.{timestamp}/`
   - Copy new templates from Hefesto source
   - Update MEMORY.md templates.version
   - Report changes to user

**Breaking Changes Migration**:
- **Minor updates** (1.0.0 → 1.1.0): Backward compatible, copy overwrites safely
- **Major updates** (1.x.x → 2.0.0): May break existing skills, require user review
- **Migration guide**: Document in `docs/migration/` for major versions

**User-Modified Templates**:
- **Problem**: User edits `.hefesto/templates/skill-template.md`
- **Detection**: Compute hash of templates on init, store in MEMORY.md
- **On re-init**: If hash differs, warn "Templates modified. Overwrite? [yes/no]"
- **Recommendation**: Advise users NOT to edit templates directly

**Decision**:
- Template version = Hefesto version (simplest tracking)
- Warn on mismatch, require explicit re-init
- Backup before overwrite
- Detect user modifications via hash comparison
- Document major version migrations separately

---

## Cross-Cutting Concerns

### Performance

**Target**: < 100ms variable substitution, < 50ms validation (plan.md)

**Strategies**:
- Preload templates into memory (avoid disk I/O per generation)
- Cache compiled validation rules
- Use efficient string replacement (single pass)
- Avoid regex where possible (use exact string matching)

**Validation**:
- Benchmark with 100 skills
- Measure P50, P95, P99 latencies
- Profile bottlenecks if target missed

### Error Handling

**Validation Failure** (FR-025, clarification #9):
1. Block persistence (T0-HEFESTO-02)
2. Trigger Human Gate
3. Display structured errors:
   ```
   ❌ Validation Failed (2 errors):
   
   1. [T0-HEFESTO-07] name: "Code-Review"
      Expected: lowercase, hyphens only
      Suggestion: Use "code-review"
   
   2. [FR-011] Frontmatter: 142 tokens
      Expected: < 100 tokens
      Suggestion: Move metadata to metadata.yaml
   ```
4. Prompt user: `[fix]`, `[ignore]` (ignore disabled for T0 violations), `[cancel]`

**Missing Variables** (FR-017):
- Insert CLI-specific default
- Log warning
- Continue generation

### Security

**Input Validation** (T0-HEFESTO-11):
- Sanitize `{{SKILL_NAME}}` against path traversal (`../`, `./`)
- Validate `{{SKILL_DESCRIPTION}}` against prompt injection patterns
- Reject unusually large inputs (> 10KB for any variable)

**Output Sanitization**:
- Ensure no executable code in generated Markdown
- Strip ANSI escape codes
- Validate relative paths don't escape skill directory

---

## Alternatives Considered

### Alternative 1: External Template Engine (e.g., Jinja2)

**Description**: Use established template engine instead of custom substitution.

**Pros**:
- Battle-tested
- Rich feature set (conditionals, loops)
- Community support

**Cons**:
- External dependency (violates FR-021 "no external dependencies")
- Overkill for simple variable substitution
- Installation requirement for users

**Rejected**: Violates in-process validation requirement (clarification #7).

### Alternative 2: Single Universal Adapter

**Description**: One adapter that detects target CLI and adjusts output.

**Pros**:
- Single file to maintain
- DRY principle

**Cons**:
- Complex conditional logic
- Harder to test per-CLI
- Violates separation of concerns

**Rejected**: FR-004 explicitly requires 7 separate adapter files for clarity and independent testing.

### Alternative 3: Template Auto-Update on Generation

**Description**: Check for template updates every time skill is generated.

**Pros**:
- Always uses latest templates
- No manual update step

**Cons**:
- Network dependency (offline operation requirement)
- Unexpected behavior changes
- Performance overhead

**Rejected**: Violates offline operation assumption, clarification #8 specifies manual re-init for updates.

---

## Decisions Summary

| Decision | Rationale | Impact |
|----------|-----------|--------|
| Use `{{VAR}}` syntax | Mustache-like, no dependencies | Variable substitution logic |
| 7 separate CLI adapters | Independent testing, clarity | File organization |
| MCP adapter targets 2024-11-05 | Latest stable MCP spec | MCP server structure |
| Template version = Hefesto version | Simplest tracking | MEMORY.md schema |
| In-process validation | No external dependencies | Validation rule encoding |
| `{{{{VAR}}}}` escape mechanism | Document literal variables | Substitution algorithm |
| Manual re-init for updates | User control, predictability | Upgrade workflow |

---

## Open Questions

**None** - All research questions resolved.

---

## References

1. Agent Skills Specification: https://agentskills.io
2. Model Context Protocol (MCP) 2024-11-05: https://modelcontextprotocol.io/specification/2024-11-05
3. T0-HEFESTO rules: CONSTITUTION.md
4. ADR-001: Agent Skills Standard
5. ADR-002: Research Integration (MCP, security)
6. ADR-003: Lightweight Frontmatter (two-tier metadata)
7. Feature spec clarifications: specs/002-templates-system/spec.md

---

**Research Status**: ✅ Complete  
**Next Phase**: Phase 1 (Design - create data-model.md, quickstart.md)
