---
description: "Validate existing skill against Agent Skills specification and T0 rules"
command: "/hefesto.validate"
category: "skill-management"
user_story: "US2"
priority: "P1"
version: "1.0.0"
---

# /hefesto.validate - Validate Skill Command

**Command**: `/hefesto.validate`  
**Purpose**: Validate skill against Agent Skills spec and T0 rules (read-only)  
**User Story**: US2 - Validation & Listing (P1)

---

## Overview

The `/hefesto.validate` command checks existing skills for compliance with agentskills.io specification and T0 rules without modification. Features:

1. **Read-Only**: No filesystem modifications
2. **T0 Compliance**: Mandatory checks (T0-HEFESTO-01 through T0-HEFESTO-11)
3. **T1/T2 Checks**: Optional with `--strict` flag
4. **Batch Validation**: Validate all skills when no name specified
5. **Detailed Reporting**: Line numbers, remediation suggestions

**Target Performance**: < 2s for typical use (SC-002)

---

## Command Signature

```text
/hefesto.validate [skill_name] [--cli <name>] [--strict]

Arguments:
  skill_name     Name of skill to validate (optional)
                 If missing: Validate ALL skills

Options:
  --cli <name>   Validate only in specific CLI directory
  --strict       Enable T1/T2 checks (normative/informative rules)
```

---

## Execution Workflow

### Phase 0: Pre-Execution Validation

```markdown
1. Validate CONSTITUTION
   (see: helpers/constitution-validator.md)
   IF invalid → ABORT

2. Check Hefesto initialization
   IF NOT file_exists("MEMORY.md"):
     DISPLAY: "❌ Hefesto not initialized. Run /hefesto.init first."
     ABORT (exit code 1)

3. Load CLI detection
   clis = read_memory_md().detected_clis
   IF clis IS empty:
     WARN: "No CLIs detected. Run /hefesto.detect"
     ABORT
```

**Performance Target**: < 100ms

---

### Phase 1: Skill Discovery

```markdown
1. Determine scope
   IF skill_name IS provided:
     skills_to_validate = discover_skill(skill_name, cli_filter)
     IF NOT found:
       ERROR E-VALIDATE-001: "Skill not found: {skill_name}"
       
       # Fuzzy search for suggestions
       similar = fuzzy_search(skill_name, all_skills)
       IF similar NOT empty:
         DISPLAY: "Did you mean:"
         FOR EACH suggestion IN similar:
           DISPLAY: "  - {suggestion}"
       
       ABORT (exit code 1)
   
   ELSE:
     # Validate all skills
     skills_to_validate = discover_all_skills(cli_filter)
     IF skills_to_validate IS empty:
       INFO: "No skills found to validate"
       EXIT (exit code 0)

2. Build skill list
   FOR EACH skill IN skills_to_validate:
     skill_info = {
       name: skill.name,
       path: skill.path,
       cli: skill.cli,
       size: file_size(skill.path)
     }
```

**Performance Target**: < 500ms for 10 skills  
**References**: FR-004

---

### Phase 2: Validation Execution

```markdown
1. Initialize validation results
   results = []

2. Validate each skill
   FOR EACH skill IN skills_to_validate:
     DISPLAY: "Validating {skill.name}..."
     
     validation = validate_single_skill(skill, strict_mode)
     results.append(validation)

3. Single skill validation
   (see: helpers/template-validator.md)
   
   validate_single_skill(skill, strict):
     errors = []
     warnings = []
     
     # Load skill content
     TRY:
       content = read_file(skill.path)
       metadata_path = dirname(skill.path) + "/metadata.yaml"
       metadata = read_file(metadata_path) IF exists
     CATCH IOError:
       ERROR E-VALIDATE-002: "Cannot read skill file"
       RETURN {status: "error", errors: [parse_error]}
     
     # Parse frontmatter
     TRY:
       frontmatter = parse_yaml_frontmatter(content)
     CATCH YAMLError:
       ERROR E-VALIDATE-003: "Missing or invalid frontmatter"
       errors.append({
         code: "E-VALIDATE-003",
         severity: "error",
         message: "Invalid YAML frontmatter",
         line: 1,
         fix: "Add valid YAML frontmatter (---\\nname: ...\\n---)"
       })
       RETURN {status: "fail", errors: errors}
     
     # T0 RULE CHECKS (MANDATORY)
     
     # T0-HEFESTO-01: Agent Skills Standard
     IF NOT frontmatter.has("name"):
       errors.append({
         code: "T0-HEFESTO-01",
         message: "Missing required field: name",
         line: frontmatter_start,
         fix: "Add 'name: skill-name' to frontmatter"
       })
     
     IF NOT frontmatter.has("description"):
       errors.append({
         code: "T0-HEFESTO-01",
         message: "Missing required field: description",
         line: frontmatter_start,
         fix: "Add 'description: ...' to frontmatter"
       })
     
     IF frontmatter.description IS empty:
       errors.append({
         code: "T0-HEFESTO-01",
         message: "Description cannot be empty",
         line: description_line,
         fix: "Provide meaningful description"
       })
     
     # T0-HEFESTO-03: Progressive Disclosure
     line_count = count_lines(content)
     IF line_count > 500:
       errors.append({
         code: "T0-HEFESTO-03",
         message: "SKILL.md exceeds 500 lines (current: {line_count})",
         line: null,
         fix: "Move detailed content to references/ or scripts/"
       })
     
     # T0-HEFESTO-07: Nomenclatura Padrao
     name = frontmatter.name
     IF NOT matches_pattern(name, "^[a-z0-9]+(-[a-z0-9]+)*$"):
       errors.append({
         code: "T0-HEFESTO-07",
         message: "Invalid name format: {name}",
         line: name_line,
         fix: "Use lowercase, hyphens only: {sanitize_name(name)}"
       })
     
     IF length(name) > 64:
       errors.append({
         code: "T0-HEFESTO-07",
         message: "Name exceeds 64 characters",
         line: name_line,
         fix: "Shorten to: {truncate(name, 64)}"
       })
     
     IF length(frontmatter.description) > 1024:
       errors.append({
         code: "T0-HEFESTO-01",
         message: "Description exceeds 1024 characters",
         line: description_line,
         fix: "Shorten description"
       })
     
     # T0-HEFESTO-11: Seguranca por Padrao
     (see: helpers/secret-detector.md)
     secrets = detect_secrets(content)
     IF secrets NOT empty:
       FOR EACH secret IN secrets:
         errors.append({
           code: "T0-HEFESTO-11",
           severity: "critical",
           message: "Potential secret detected: {secret.type}",
           line: secret.line,
           fix: "Remove secret, use environment variable"
         })
     
     # T1 CHECKS (--strict mode only)
     IF strict:
       # T1-HEFESTO-01: Descricao Acionavel
       IF NOT contains(description, ["Use when", "Use for", "Use this"]):
         warnings.append({
           code: "T1-HEFESTO-01",
           severity: "warning",
           message: "Description should include 'Use when:' clause",
           line: description_line,
           fix: "Add usage context: 'Use when: ...'"
         })
       
       # T1-HEFESTO-02: Exemplos em Skills Complexas
       IF is_complex_skill(content) AND NOT has_examples(content):
         warnings.append({
           code: "T1-HEFESTO-02",
           message: "Complex skill should include examples",
           line: null,
           fix: "Add ## Examples section"
         })
       
       # T1-HEFESTO-03: Versionamento
       IF NOT frontmatter.has("version") AND NOT metadata.has("version"):
         warnings.append({
           code: "T1-HEFESTO-03",
           message: "Missing version metadata",
           line: frontmatter_start,
           fix: "Add 'version: 1.0.0' to frontmatter"
         })
     
     # FILE STRUCTURE CHECKS
     IF metadata_path referenced IN frontmatter BUT NOT exists:
       errors.append({
         code: "E-VALIDATE-006",
         message: "Referenced metadata.yaml not found",
         line: null,
         fix: "Create {metadata_path} or remove reference"
       })
     
     scripts_dir = dirname(skill.path) + "/scripts"
     IF directory_exists(scripts_dir):
       FOR EACH script IN list_files(scripts_dir):
         IF should_be_executable(script) AND NOT is_executable(script):
           warnings.append({
             code: "W-VALIDATE-001",
             severity: "warning",
             message: "Script not executable: {script}",
             line: null,
             fix: "chmod +x {script}"
           })
     
     RETURN {
       status: "pass" IF errors empty ELSE "fail",
       errors: errors,
       warnings: warnings,
       line_count: line_count,
       checks_run: count_checks
     }
```

**Performance Target**: < 500ms per skill  
**References**: T0-HEFESTO-06, FR-004

---

### Phase 3: Results Display

```markdown
1. Display validation results
   
   FOR EACH result IN results:
     skill_name = result.skill.name
     
     IF result.status == "pass":
       DISPLAY: "✅ {skill_name} - VALID"
       
       IF result.warnings NOT empty AND verbose:
         FOR EACH warning IN result.warnings:
           DISPLAY: "  ⚠️  [{warning.code}] {warning.message}"
     
     ELSE:
       DISPLAY: "❌ {skill_name} - INVALID"
       
       FOR EACH error IN result.errors:
         DISPLAY: ""
         DISPLAY: "  ERROR [{error.code}]: {error.message}"
         IF error.line:
           DISPLAY: "    Location: {result.skill.path}:{error.line}"
         DISPLAY: "    Fix: {error.fix}"

2. Summary
   total = count(results)
   passed = count(results WHERE status == "pass")
   failed = count(results WHERE status == "fail")
   
   DISPLAY: ""
   DISPLAY: "═══════════════════════════════════════════════════"
   DISPLAY: "Validation Summary"
   DISPLAY: "═══════════════════════════════════════════════════"
   DISPLAY: "Total skills: {total}"
   DISPLAY: "Passed: {passed} ✅"
   DISPLAY: "Failed: {failed} ❌"
   DISPLAY: "Success rate: {passed/total * 100}%"
   DISPLAY: "═══════════════════════════════════════════════════"

3. Exit code
   IF all passed:
     EXIT 0
   ELSE:
     EXIT 1
```

**References**: spec.md L80-86, US-002

---

## Error Cases

| Code | Condition | Handler |
|------|-----------|---------|
| **E-VALIDATE-001** | Skill not found | Error + fuzzy search suggestions |
| **E-VALIDATE-002** | Cannot read file | IO error with path |
| **E-VALIDATE-003** | Missing frontmatter | T0-HEFESTO-01 violation |
| **E-VALIDATE-004** | Invalid name format | T0-HEFESTO-07 violation + auto-fix suggestion |
| **E-VALIDATE-005** | SKILL.md exceeds 500 lines | T0-HEFESTO-03 violation + refactor suggestion |
| **E-VALIDATE-006** | Missing required metadata | List missing fields |

---

## Usage Examples

### Example 1: Single Skill Validation

```bash
> /hefesto.validate email-validator

Validating email-validator...

✅ email-validator - VALID

Checks run: 8 T0 rules, 0 warnings

═══════════════════════════════════════════════════
Validation Summary
═══════════════════════════════════════════════════
Total skills: 1
Passed: 1 ✅
Failed: 0 ❌
Success rate: 100%
═══════════════════════════════════════════════════
```

### Example 2: Failed Validation

```bash
> /hefesto.validate Code-Review

Validating Code-Review...

❌ Code-Review - INVALID

  ERROR [T0-HEFESTO-07]: Invalid name format: Code-Review
    Location: .claude/skills/Code-Review/SKILL.md:2
    Fix: Use lowercase, hyphens only: code-review

  ERROR [T0-HEFESTO-03]: SKILL.md exceeds 500 lines (current: 612)
    Location: .claude/skills/Code-Review/SKILL.md
    Fix: Move detailed content to references/ or scripts/

═══════════════════════════════════════════════════
Validation Summary
═══════════════════════════════════════════════════
Total skills: 1
Passed: 0 ✅
Failed: 1 ❌
Success rate: 0%
═══════════════════════════════════════════════════
```

### Example 3: Validate All Skills

```bash
> /hefesto.validate

Validating 5 skills...

✅ email-validator - VALID
❌ Code-Review - INVALID (name format)
✅ testing-strategy - VALID
✅ deploy-aws - VALID
❌ api-wrapper - INVALID (exceeds 500 lines)

═══════════════════════════════════════════════════
Validation Summary
═══════════════════════════════════════════════════
Total skills: 5
Passed: 3 ✅
Failed: 2 ❌
Success rate: 60%
═══════════════════════════════════════════════════
```

### Example 4: Strict Mode

```bash
> /hefesto.validate email-validator --strict

Validating email-validator...

✅ email-validator - VALID

  ⚠️  [T1-HEFESTO-01] Description should include 'Use when:' clause
    Fix: Add usage context: 'Use when: ...'

  ⚠️  [T1-HEFESTO-03] Missing version metadata
    Fix: Add 'version: 1.0.0' to frontmatter

Checks run: 8 T0 rules + 3 T1 rules, 2 warnings

═══════════════════════════════════════════════════
```

### Example 5: Specific CLI

```bash
> /hefesto.validate --cli gemini

Validating skills in .gemini/skills/...

✅ testing-strategy - VALID
✅ email-validator - VALID

═══════════════════════════════════════════════════
Validation Summary
═══════════════════════════════════════════════════
Total skills: 2
Passed: 2 ✅
Failed: 0 ❌
Success rate: 100%
═══════════════════════════════════════════════════
```

---

## Validation Checklist

### T0 Rules (Mandatory)

- [ ] **T0-HEFESTO-01**: Valid frontmatter (name, description)
- [ ] **T0-HEFESTO-03**: SKILL.md < 500 lines
- [ ] **T0-HEFESTO-07**: Name lowercase, hyphens only, < 64 chars
- [ ] **T0-HEFESTO-11**: No secrets or credentials

### T1 Rules (--strict flag)

- [ ] **T1-HEFESTO-01**: "Use when:" in description
- [ ] **T1-HEFESTO-02**: Examples for complex skills
- [ ] **T1-HEFESTO-03**: Version metadata present

### File Structure

- [ ] SKILL.md exists and readable
- [ ] metadata.yaml exists if referenced
- [ ] scripts/ files have correct permissions
- [ ] references/ are valid markdown

---

## Success Criteria

- ✅ **SC-001**: Command implemented
- ✅ **SC-002**: Executes in < 2s
- ✅ **SC-005**: Help documentation embedded
- ✅ **US-002 Scenario 2**: Error reporting with remediation

---

## Performance Targets

| Operation | Target | Typical |
|-----------|--------|---------|
| Skill discovery | < 100ms | 50ms |
| Single validation | < 500ms | 200ms |
| All skills (10) | < 2s | 1s |
| **Total** | **< 2s** | **~1s** |

---

## Dependencies

**Required Helpers:**
- `helpers/template-validator.md` - Core validation logic
- `helpers/cli-detector.md` - Skill discovery
- `helpers/secret-detector.md` - Security checks

**State Files:**
- `MEMORY.md` - CLI detection results (read-only)

---

## See Also

- **Related Commands**: `/hefesto.create`, `/hefesto.show`, `/hefesto.sync`
- **Specification**: `specs/003-hefesto-commands/contracts/validate.contract.md`
- **T0 Rules**: `CONSTITUTION.md` (all T0-HEFESTO rules)
- **User Story**: `specs/003-hefesto-commands/spec.md` US2
