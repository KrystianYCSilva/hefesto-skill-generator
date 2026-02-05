# Contract: CLI Adapter

**Feature**: 004-multi-cli-generator  
**Component**: CLI-Specific Transformation System  
**Type**: Interface Definition

---

## Purpose

CLI Adapters transform generic skill content into CLI-specific formats, applying syntax conversions, directory structure adjustments, and validation rules unique to each AI CLI.

---

## Interface

### Input

```yaml
skill_content:
  skill_name: string            # Name of skill (lowercase-hyphenated)
  skill_md: string              # Core SKILL.md content
  references: map               # Optional reference files (filename → content)
  scripts: map                  # Optional scripts (filename → content)
  assets: map                   # Optional assets (filename → content)
  metadata: map                 # Skill metadata from frontmatter
```

### Output

```yaml
adapted_skill:
  skill_name: string            # Unchanged from input
  skill_md: string              # Transformed SKILL.md content
  references: map               # Transformed reference files
  scripts: map                  # Transformed scripts
  assets: map                   # Unchanged assets
  metadata: map                 # Modified metadata with CLI-specific additions
  target_directory: string      # Full path for skill output
  validation_result: ValidationResult  # Self-validation result
```

---

## Operations

### `adapt(skill_content: SkillContent, cli_name: string) -> AdaptedSkill`

**Description**: Transforms skill content for target CLI.

**Algorithm**:
```
1. Load adapter for cli_name from adapter registry
2. Apply variable transformations (transform_variables)
3. Apply directory structure rules (transform_structure)
4. Add CLI-specific frontmatter (add_frontmatter)
5. Validate adapted content (validate)
6. Return AdaptedSkill with all transformations applied
```

**Error Handling**: Returns AdaptedSkill with validation_result.valid=false if transformation fails

---

### `transform_variables(content: string, cli_name: string) -> string`

**Description**: Replaces generic variable syntax with CLI-specific syntax.

**Transformation Rules**:

| Source | Claude | Gemini | Codex | Copilot | OpenCode | Cursor | Qwen |
|--------|--------|--------|-------|---------|----------|--------|------|
| `$ARGUMENTS` | `$ARGUMENTS` | `{{args}}` | `$ARGUMENTS` | `$ARGUMENTS` | `$ARGUMENTS` | `$ARGUMENTS` | `{{args}}` |

**Algorithm**:
```
1. Load variable_syntax map for cli_name from adapter
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

**Description**: Determines output directory structure for CLI.

**Algorithm**:
```
1. Load directory_structure rules for cli_name
2. Construct base path: {skills_base}/{skill_name}/
3. If use_skill_name_dir=false: base path = {skills_base}/
4. For each file in skill (SKILL.md, references, scripts, assets):
   a. Apply path adjustments from adapter rules
   b. Add to output directory structure
5. Return DirectoryStructure with all file paths
```

**Directory Structure Map**:

| CLI | skills_base | use_skill_name_dir | Special Rules |
|-----|-------------|-------------------|---------------|
| Claude | `.claude/skills` | true | None |
| Gemini | `.gemini/skills` | true | None |
| Codex | `.codex/skills` | true | None |
| Copilot | `.github/skills` | true | GitHub-specific metadata |
| OpenCode | `.opencode/skills` | true | None |
| Cursor | `.cursor/skills` | true | None |
| Qwen | `.qwen/skills` | true | Optional TOML generation |

**Example Output**:
```yaml
# Claude
.claude/skills/code-review/SKILL.md
.claude/skills/code-review/references/EXAMPLES.md
.claude/skills/code-review/scripts/validate.sh

# Copilot
.github/skills/code-review/SKILL.md
.github/skills/code-review/references/EXAMPLES.md
.github/skills/code-review/scripts/validate.sh
```

---

### `add_frontmatter(metadata: map, cli_name: string) -> map`

**Description**: Adds CLI-specific frontmatter fields.

**Algorithm**:
```
1. Load frontmatter_additions for cli_name
2. Merge additions into existing metadata
3. Preserve existing fields (no overwriting)
4. Return enhanced metadata
```

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

**Description**: Validates adapted skill against CLI-specific rules.

**Algorithm**:
```
1. Run Agent Skills spec validation (common to all CLIs)
2. For each validation_rule in CLI adapter:
   a. Execute rule check
   b. If check fails, add error to result
3. Return ValidationResult with all errors collected
```

**Validation Rules by CLI**:

**All CLIs**:
- ✅ Agent Skills spec compliance (name, description, SKILL.md format)
- ✅ SKILL.md under 500 lines (T0-HEFESTO-03)
- ✅ No secrets or credentials (T0-HEFESTO-11)
- ✅ Name follows lowercase-hyphen convention (T0-HEFESTO-07)

**Gemini**:
- ✅ No `$ARGUMENTS` in content (must use `{{args}}`)
- ✅ Valid TOML if TOML generation enabled

**Qwen**:
- ✅ No `$ARGUMENTS` in content (must use `{{args}}`)
- ✅ Valid TOML if TOML generation enabled

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

## Adapter Registry

### Location

Defined in: `commands/helpers/cli-adapter.md`

### Registry Schema

```yaml
adapters:
  claude:
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
  
  gemini:
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
  
  codex:
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
  
  copilot:
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
  
  opencode:
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
  
  cursor:
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
  
  qwen:
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

## Testing Contract

### Manual Test Cases

1. **Claude Adapter (No Transformations)**
   - **Input**: Generic skill with `$ARGUMENTS`
   - **Expected**: Unchanged content, `.claude/skills/{name}/SKILL.md`

2. **Gemini Adapter (Variable Transformation)**
   - **Input**: Generic skill with `$ARGUMENTS`
   - **Expected**: All `$ARGUMENTS` → `{{args}}`, `.gemini/skills/{name}/SKILL.md`

3. **Copilot Adapter (Frontmatter Addition)**
   - **Input**: Generic skill with standard frontmatter
   - **Expected**: `github_integration: true` added, `.github/skills/{name}/SKILL.md`

4. **Qwen Adapter (Variable + Validation)**
   - **Input**: Generic skill with `$ARGUMENTS`
   - **Expected**: All `$ARGUMENTS` → `{{args}}`, validation checks for residual `$ARGUMENTS`

5. **Validation Failure Detection**
   - **Input**: Gemini skill with `$ARGUMENTS` still present
   - **Expected**: valid=false, error="$ARGUMENTS found in Gemini skill"

6. **Multiple File Transformation**
   - **Input**: Skill with SKILL.md + 2 references + 1 script
   - **Expected**: All files transformed, correct directory structure

---

## Integration Points

### With CLI Detector

**Dependency**: Adapter selection based on CLI Detection Result.

**Usage**:
```
detection_result = cli_detector.detect_all_clis()
for cli in detection_result.clis where status=detected:
  adapter = load_adapter(cli.name)
  adapted_skill = adapter.adapt(skill_content, cli.name)
```

---

### With Parallel Generator

**Dependency**: Parallel Generator invokes adapter for each target CLI.

**Usage**:
```
tasks = []
for cli in target_clis:
  task = GenerationTask(
    target_cli=cli,
    adapter=load_adapter(cli),
    skill_content=skill_content
  )
  tasks.append(task)
parallel_generator.execute(tasks)
```

---

## Performance Considerations

- **Transformation Speed**: <50ms per skill per CLI (primarily string operations)
- **Validation Speed**: <100ms per skill (existing validator reuse)
- **Memory Usage**: One adapter instance per CLI (7 total, negligible overhead)
- **Caching**: Adapters are stateless, can be loaded once and reused

---

## Related Contracts

- [CLI Detector](./cli-detector.md) - Provides CLI list for adapter selection
- [Parallel Generator](./parallel-generator.md) - Consumes adapters for multi-CLI generation
- [Rollback Handler](./rollback-handler.md) - Uses validation results to determine rollback

---

**Contract Version**: 1.0.0 | **Status**: Draft | **Date**: 2026-02-04
