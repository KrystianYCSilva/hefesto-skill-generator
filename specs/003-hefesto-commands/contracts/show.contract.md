# Contract: /hefesto.show

## Command Purpose
Display full content and metadata of a specific skill (read-only).

## Input Specification

**Args:**
- `skill_name` (positional, required): Name of skill to display

**Flags:**
- `--cli <name>` (optional): Show from specific CLI directory (if multiple exist)
- `--metadata-only` (optional): Show only metadata.yaml
- `--body-only` (optional): Show only SKILL.md body (skip metadata)

**Environment:**
- Requires: Skill exists in at least one CLI directory
- No write permissions needed (read-only)

## Output Specification

**User Messages:**
1. Header: "Skill: <name> (<cli>)"
2. Metadata section (formatted YAML)
3. Content divider
4. SKILL.md body (markdown)
5. Footer: "Location: <path>"

**File Operations:**
- None (read-only)

**MEMORY.md Updates:**
- None

## Side Effects

**Filesystem Changes:**
- None (read-only)

**State Mutations:**
- None

## Error Cases

| Error | Condition | Handler |
|-------|-----------|---------|
| `E-SHOW-001` | Skill not found | Error + suggest similar names |
| `E-SHOW-002` | Skill exists in multiple CLIs | Require explicit `--cli` flag |
| `E-SHOW-003` | File not readable | Permission error |
| `E-SHOW-004` | Invalid SKILL.md format | Show raw content + warning |
| `E-SHOW-005` | metadata.yaml referenced but missing | Warning + show SKILL.md only |

## Performance Targets

- File discovery: < 100ms
- File read: < 50ms
- Formatting: < 50ms
- **Total: < 200ms (SC-002: < 2s)**

## Dependencies

**Required Helpers:**
- `helpers/cli-detector.md` - Skill location

**State Files:**
- `MEMORY.md` - CLI detection results (read-only)

## Success Criteria Mapping

- **SC-001**: Command implemented
- **SC-002**: Executes in < 2s
- **SC-005**: Help documentation embedded
- **US-004 Scenario 1**: Content display
- **FR-011**: Skill name + full content display

## Output Format

```markdown
═══════════════════════════════════════════════════
Skill: email-validator (claude)
═══════════════════════════════════════════════════

METADATA
--------
name: email-validator
description: Validates email addresses using regex patterns
version: 1.0.0
created: 2026-02-04
category: validation
tags: [email, regex, validation]

CONTENT
-------
# Email Validator Skill

[... full SKILL.md body ...]

═══════════════════════════════════════════════════
Location: .claude/skills/email-validator/SKILL.md
Size: 2.3 KB
Last modified: 2026-02-04 10:30:00
═══════════════════════════════════════════════════
```

## Example Invocations

```bash
# Show full skill
/hefesto.show email-validator

# Show from specific CLI
/hefesto.show testing-strategy --cli gemini

# Metadata only
/hefesto.show email-validator --metadata-only
# Output:
# name: email-validator
# version: 1.0.0
# ...

# Body only (skip metadata)
/hefesto.show email-validator --body-only
```

## Mapped Requirements

- **FR-011**: Accept skill name + display full content
- **US-004 Scenario 1**: Content display functionality
- **SC-002**: Performance < 2s
