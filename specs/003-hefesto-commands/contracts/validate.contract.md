# Contract: /hefesto.validate

## Command Purpose
Validate existing skill against Agent Skills specification and T0 rules without modification.

## Input Specification

**Args:**
- `skill_name` (positional, optional): Name of skill to validate
  - If missing: Validate ALL skills

**Flags:**
- `--cli <name>` (optional): Validate only in specific CLI directory
- `--strict` (optional): Enable additional T1/T2 checks

**Environment:**
- Requires: Skills exist in detected CLI directories
- Requires: Template validator helper
- No write permissions needed (read-only)

## Output Specification

**User Messages:**
1. "Validating <skill-name>..."
2. For each violation:
   - "ERROR [T0-HEFESTO-XX]: <description>"
   - "  Location: <file>:<line>"
   - "  Fix: <remediation>"
3. Summary: "X errors, Y warnings"
4. Exit status: 0 (valid) or 1 (invalid)

**File Operations:**
- None (read-only operation)

**MEMORY.md Updates:**
- None (validation does not mutate state)

## Side Effects

**Filesystem Changes:**
- None (read-only)

**State Mutations:**
- None

## Error Cases

| Error | Condition | Handler |
|-------|-----------|---------|
| `E-VALIDATE-001` | Skill not found | Error with similar suggestions |
| `E-VALIDATE-002` | Invalid SKILL.md structure | Parse error with line number |
| `E-VALIDATE-003` | Missing frontmatter | T0-HEFESTO-01 violation |
| `E-VALIDATE-004` | Invalid name format | T0-HEFESTO-07 violation + auto-fix suggestion |
| `E-VALIDATE-005` | SKILL.md exceeds 500 lines | T0-HEFESTO-03 violation + refactor suggestion |
| `E-VALIDATE-006` | Missing required metadata | List missing fields |

## Performance Targets

- Single skill validation: < 500ms (SC-002)
- All skills validation: < 2s for 10 skills (SC-002)
- File I/O: < 100ms per skill
- **Target: < 2s total for typical use**

## Dependencies

**Required Helpers:**
- `helpers/template-validator.md` - Core validation logic
- `helpers/cli-detector.md` - Skill discovery

**State Files:**
- `MEMORY.md` - CLI detection results (read-only)

## Success Criteria Mapping

- **SC-001**: Command implemented
- **SC-002**: Executes in < 2s
- **SC-005**: Help documentation embedded
- **US-002 Scenario 2**: Error reporting for invalid skills
- **FR-004**: Validates against spec + T0 rules

## Validation Checklist

**T0 Rules (Mandatory):**
- [ ] T0-HEFESTO-01: Valid frontmatter (name, description)
- [ ] T0-HEFESTO-03: SKILL.md < 500 lines
- [ ] T0-HEFESTO-07: Name lowercase, hyphens only, < 64 chars
- [ ] T0-HEFESTO-11: No secrets or credentials

**T1 Rules (--strict flag):**
- [ ] T1-HEFESTO-01: "Use when:" in description
- [ ] T1-HEFESTO-02: Examples for complex skills
- [ ] T1-HEFESTO-03: Version metadata present

**File Structure:**
- [ ] SKILL.md exists
- [ ] metadata.yaml (if referenced in frontmatter)
- [ ] scripts/ permissions are executable
- [ ] references/ are valid markdown

## Example Invocations

```bash
# Validate single skill
/hefesto.validate email-validator
# Output:
# ✓ Valid frontmatter
# ✓ Name format correct
# ✗ ERROR [T0-HEFESTO-03]: SKILL.md exceeds 500 lines (current: 612)
#   Location: .claude/skills/email-validator/SKILL.md
#   Fix: Move detailed examples to references/examples.md

# Validate all skills
/hefesto.validate
# Output:
# Validating 5 skills...
# ✓ email-validator
# ✗ Code-Review (name uppercase)
# ✓ testing-strategy
# Summary: 4/5 valid

# Strict mode
/hefesto.validate --strict email-validator
# (includes T1 checks)

# Specific CLI
/hefesto.validate --cli gemini
```

## Mapped Requirements

- **FR-004**: Template-validator integration
- **US-002 Scenario 2**: Specific error messages with remediation
- **SC-002**: Performance < 2s
- **T0-HEFESTO-06**: Validation spec enforcement
