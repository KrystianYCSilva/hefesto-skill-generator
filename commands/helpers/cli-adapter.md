# CLI Adapter Registry

**Purpose**: Transform generic skill content into CLI-specific formats  
**Contract**: [cli-adapter.md](../../specs/004-multi-cli-generator/contracts/cli-adapter.md)  
**Feature**: 004-multi-cli-generator

---

## Overview

CLI Adapters apply CLI-specific transformations:
- **Variable Syntax**: Convert `$ARGUMENTS` to CLI-specific format
- **Directory Structure**: Construct CLI-specific paths
- **Frontmatter**: Add CLI-specific metadata fields
- **Validation**: Apply CLI-specific rules

---

## Adapter Registry

### Claude Code (Priority 1)

```yaml
cli_name: claude
priority: 1
config_directory: .claude
variable_syntax:
  ARGUMENTS: "$ARGUMENTS"
directory_structure:
  skills_base: ".claude/skills"
  use_skill_name_dir: true
frontmatter_additions: {}
validation_rules:
  - agent-skills-compliance
```

**Transformations**: None (reference implementation)

---

### Gemini CLI (Priority 2)

```yaml
cli_name: gemini
priority: 2
config_directory: .gemini
variable_syntax:
  ARGUMENTS: "{{args}}"
directory_structure:
  skills_base: ".gemini/skills"
  use_skill_name_dir: true
frontmatter_additions: {}
validation_rules:
  - agent-skills-compliance
  - gemini-variable-syntax
```

**Transformations**:
- `$ARGUMENTS` → `{{args}}`

**Validation**:
- Fail if `$ARGUMENTS` found in content (must use `{{args}}`)

---

### OpenAI Codex (Priority 3)

```yaml
cli_name: codex
priority: 3
config_directory: .codex
variable_syntax:
  ARGUMENTS: "$ARGUMENTS"
directory_structure:
  skills_base: ".codex/skills"
  use_skill_name_dir: true
frontmatter_additions: {}
validation_rules:
  - agent-skills-compliance
```

**Transformations**: None

---

### VS Code/Copilot (Priority 4)

```yaml
cli_name: copilot
priority: 4
config_directory: .github
variable_syntax:
  ARGUMENTS: "$ARGUMENTS"
directory_structure:
  skills_base: ".github/skills"
  use_skill_name_dir: true
frontmatter_additions:
  github_integration: true
validation_rules:
  - agent-skills-compliance
  - copilot-github-integration
```

**Transformations**:
- Add `github_integration: true` to frontmatter

**Validation**:
- Check `github_integration` field present in frontmatter
- Verify directory under `.github/skills/`

---

### OpenCode (Priority 5)

```yaml
cli_name: opencode
priority: 5
config_directory: .opencode
variable_syntax:
  ARGUMENTS: "$ARGUMENTS"
directory_structure:
  skills_base: ".opencode/skills"
  use_skill_name_dir: true
frontmatter_additions: {}
validation_rules:
  - agent-skills-compliance
```

**Transformations**: None

---

### Cursor (Priority 6)

```yaml
cli_name: cursor
priority: 6
config_directory: .cursor
variable_syntax:
  ARGUMENTS: "$ARGUMENTS"
directory_structure:
  skills_base: ".cursor/skills"
  use_skill_name_dir: true
frontmatter_additions: {}
validation_rules:
  - agent-skills-compliance
```

**Transformations**: None

---

### Qwen Code (Priority 7)

```yaml
cli_name: qwen
priority: 7
config_directory: .qwen
variable_syntax:
  ARGUMENTS: "{{args}}"
directory_structure:
  skills_base: ".qwen/skills"
  use_skill_name_dir: true
frontmatter_additions: {}
validation_rules:
  - agent-skills-compliance
  - qwen-variable-syntax
```

**Transformations**:
- `$ARGUMENTS` → `{{args}}`

**Validation**:
- Fail if `$ARGUMENTS` found in content (must use `{{args}}`)

---

## Operations

### `adapt(skill_content: SkillContent, cli_name: string) -> AdaptedSkill`

**Description**: Transform skill content for target CLI.

**Algorithm**:
```
1. Load adapter for cli_name from registry
2. Apply variable transformations (transform_variables)
3. Apply directory structure rules (transform_structure)
4. Add CLI-specific frontmatter (add_frontmatter)
5. Validate adapted content (validate)
6. Return AdaptedSkill with all transformations applied
```

**Error Handling**: Returns AdaptedSkill with validation_result.valid=false if transformation fails

---

### `transform_variables(content: string, cli_name: string) -> string`

**Description**: Replace generic variable syntax with CLI-specific syntax.

**Transformation Rules**:

| CLI | `$ARGUMENTS` → |
|-----|----------------|
| Claude | `$ARGUMENTS` (no change) |
| Gemini | `{{args}}` |
| Codex | `$ARGUMENTS` (no change) |
| Copilot | `$ARGUMENTS` (no change) |
| OpenCode | `$ARGUMENTS` (no change) |
| Cursor | `$ARGUMENTS` (no change) |
| Qwen | `{{args}}` |

**Algorithm**:
```
1. Load variable_syntax map for cli_name
2. For each mapping (source → target):
   a. Search content for source pattern
   b. Replace all occurrences with target pattern
3. Return transformed content
```

**Example**:
```markdown
# Input (generic)
Execute: `npm test $ARGUMENTS`

# Output (Gemini)
Execute: `npm test {{args}}`

# Output (Claude)
Execute: `npm test $ARGUMENTS`
```

---

### `transform_structure(skill: SkillContent, cli_name: string) -> DirectoryStructure`

**Description**: Determine output directory structure for CLI.

**Directory Structure Map**:

| CLI | skills_base | use_skill_name_dir |
|-----|-------------|-------------------|
| Claude | `.claude/skills` | true |
| Gemini | `.gemini/skills` | true |
| Codex | `.codex/skills` | true |
| Copilot | `.github/skills` | true |
| OpenCode | `.opencode/skills` | true |
| Cursor | `.cursor/skills` | true |
| Qwen | `.qwen/skills` | true |

**Example Output**:
```
# Claude
.claude/skills/code-review/SKILL.md
.claude/skills/code-review/references/EXAMPLES.md

# Copilot
.github/skills/code-review/SKILL.md
.github/skills/code-review/references/EXAMPLES.md
```

---

### `add_frontmatter(metadata: map, cli_name: string) -> map`

**Description**: Add CLI-specific frontmatter fields.

**Frontmatter Additions**:

| CLI | Additional Fields |
|-----|-------------------|
| Claude | None |
| Gemini | None |
| Codex | None |
| Copilot | `github_integration: true` |
| OpenCode | None |
| Cursor | None |
| Qwen | None |

**Example**:
```yaml
# Input (generic)
name: code-review
description: Standardized code review process

# Output (Copilot)
name: code-review
description: Standardized code review process
github_integration: true
```

---

### `validate(adapted_skill: AdaptedSkill) -> ValidationResult`

**Description**: Validate adapted skill against CLI-specific rules.

**Common Validation Rules (All CLIs)**:
- ✅ Agent Skills spec compliance
- ✅ SKILL.md under 500 lines (T0-HEFESTO-03)
- ✅ No secrets or credentials (T0-HEFESTO-11)
- ✅ Name follows lowercase-hyphen convention (T0-HEFESTO-07)

**CLI-Specific Validation Rules**:

**Gemini**:
- ✅ No `$ARGUMENTS` in content (must use `{{args}}`)

**Qwen**:
- ✅ No `$ARGUMENTS` in content (must use `{{args}}`)

**Copilot**:
- ✅ `github_integration` field present in frontmatter
- ✅ Directory under `.github/skills/`

**Return Type**:
```yaml
validation_result:
  valid: boolean
  errors: list[string]        # Error messages
  warnings: list[string]      # Non-blocking warnings
  cli_name: string
```

---

## Helper Functions

### `load_adapter(cli_name: string) -> CLIAdapter`

**Description**: Load adapter configuration from registry.

**Algorithm**:
```
1. Look up cli_name in adapter registry
2. If not found: return error
3. Return adapter configuration object
```

---

### `get_cli_priority(cli_name: string) -> integer`

**Description**: Get priority order for conflict resolution.

**Priority Order**:
1. Claude Code
2. Gemini CLI
3. OpenAI Codex
4. VS Code/Copilot
5. OpenCode
6. Cursor
7. Qwen Code

---

## Error Scenarios

| Scenario | Response | Validation Result |
|----------|----------|-------------------|
| Unknown CLI name | Return error | valid=false, error="Unknown CLI" |
| Variable syntax not found | No transformation | valid=true (no-op) |
| Validation rule fails | Continue, collect error | valid=false, errors list populated |
| Frontmatter merge conflict | Keep original value | valid=true, warning added |
| Directory structure invalid | Return error | valid=false, error="Invalid path" |

---

## Performance

- **Transformation Speed**: <50ms per skill per CLI (primarily string operations)
- **Validation Speed**: <100ms per skill (existing validator reuse)
- **Memory Usage**: One adapter instance per CLI (7 total, negligible overhead)
- **Caching**: Adapters are stateless, can be loaded once and reused

---

## Usage Example

```markdown
# Load adapter
adapter = load_adapter("gemini")

# Transform skill
adapted_skill = adapt(skill_content, "gemini")

# Check validation
if adapted_skill.validation_result.valid:
  write_skill_to_disk(adapted_skill)
else:
  display_errors(adapted_skill.validation_result.errors)
```

---

## Related Files

- **Contract**: [cli-adapter.md](../../specs/004-multi-cli-generator/contracts/cli-adapter.md)
- **Data Model**: [data-model.md](../../specs/004-multi-cli-generator/data-model.md) §2
- **Helpers**: `cli-detector.md`, `parallel-generator.md`
- **Commands**: `hefesto.create.md`, `hefesto.extract.md`, `hefesto.adapt.md`

---

**Version**: 1.0.0 | **Date**: 2026-02-05 | **Feature**: 004-multi-cli-generator
