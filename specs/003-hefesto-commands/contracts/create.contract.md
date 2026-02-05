# Contract: /hefesto.create

## Command Purpose
Generate new Agent Skill from natural language description with Human Gate approval.

## Input Specification

**Args:**
- `description` (positional, optional): Natural language description of the skill to create
  - If missing: Enter Wizard Mode (FR-003)
  - Max length: 2000 chars (T0-HEFESTO-11)

**Flags:**
- `--target <cli>` (optional): Target specific CLI (default: all detected)
- `--template <name>` (optional): Use specific template variant

**Environment:**
- Requires: Detected CLIs in MEMORY.md
- Requires: Template system available (CARD-002)
- Requires: Write permissions to project skill directories

## Output Specification

**User Messages:**
1. "Generating skill from description..."
2. Preview of generated skill with metadata
3. Human Gate prompt: `[approve]`, `[expand]`, `[edit]`, `[reject]`
4. On approval: "Skill created: <path>"
5. On rejection: "Operation cancelled"

**File Operations:**
- Create `.<cli>/skills/<name>/SKILL.md`
- Create `.<cli>/skills/<name>/metadata.yaml` (if extended metadata needed)
- Update MEMORY.md with new skill entry

**MEMORY.md Updates:**
```yaml
skills_created:
  - name: <skill-name>
    created: 2026-02-04
    clis: [claude, gemini]
    status: active
```

## Side Effects

**Filesystem Changes:**
- New directory: `.<cli>/skills/<name>/`
- New files: SKILL.md, metadata.yaml
- Modified: MEMORY.md

**State Mutations:**
- Increment skill counter in MEMORY.md
- Add to skill registry

## Error Cases

| Error | Condition | Handler |
|-------|-----------|---------|
| `E-CREATE-001` | Description exceeds 2000 chars | Truncate + warn |
| `E-CREATE-002` | Invalid skill name generated | Auto-sanitize per T0-HEFESTO-07 |
| `E-CREATE-003` | Skill already exists | Trigger collision Human Gate (FR-008) |
| `E-CREATE-004` | No CLIs detected | Error + suggest `/hefesto.detect` |
| `E-CREATE-005` | Template validation fails | Show errors + block persist |
| `E-CREATE-006` | Write permission denied | Error with path details |

## Performance Targets

- Template loading: < 500ms (SC-002)
- Skill generation: < 5s (model dependent)
- Human Gate wait: unbounded (user input)
- Persistence: < 1s
- **Total (excluding Human Gate):** < 7s

## Dependencies

**Required Helpers:**
- `helpers/human-gate.md` - Approval workflow
- `helpers/template-validator.md` - T0 compliance check
- `helpers/cli-detector.md` - Available CLIs

**Required Templates:**
- `templates/base/SKILL.md.template`
- `templates/base/metadata.yaml.template`

**State Files:**
- `MEMORY.md` - Skill registry and CLI detection

## Success Criteria Mapping

- **SC-001**: Command is implemented and executable
- **SC-003**: Human Gate triggered 100% before persist
- **SC-004**: Wizard mode activates when description missing
- **SC-005**: Documentation embedded in help

## Wizard Mode Specification

**Activation:** When `description` argument missing

**Questions (strictly necessary only):**
1. "What should this skill do?" → `description`
2. "Skill name (auto-generated: <suggestion>):" → `name` (optional override)
3. "Target CLIs (detected: claude, gemini) [all]:" → `targets`

**Behavior:**
- Provide smart defaults (e.g., auto-generate name from description)
- Allow Enter to accept defaults
- Validate inputs inline before proceeding

## Example Invocations

```bash
# With argument
/hefesto.create "Validate email addresses using regex patterns"

# Wizard mode
/hefesto.create
# → What should this skill do?
# → [User input...]

# Specific target
/hefesto.create "Run Jest tests" --target claude

# Custom template
/hefesto.create "Deploy to AWS" --template deployment
```

## Mapped Requirements

- **FR-002**: Human Gate enforcement
- **FR-003**: Wizard Mode support
- **FR-008**: Collision detection
- **US-001 Scenario 1**: Description-based creation
- **US-001 Scenario 3**: Wizard Mode entry
- **T0-HEFESTO-02**: Human Gate protocol
- **T0-HEFESTO-06**: Pre-persist validation
- **T0-HEFESTO-08**: Idempotent collision handling
