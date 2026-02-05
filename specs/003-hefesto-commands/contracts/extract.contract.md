# Contract: /hefesto.extract

## Command Purpose
Extract Agent Skill from existing code file by wrapping it with skill metadata and documentation.

## Input Specification

**Args:**
- `file_path` (positional, optional): Path to code file to extract
  - If missing: Enter Wizard Mode (FR-003)
  - Must exist and be readable
  - Supports: .py, .js, .ts, .sh, .java, etc.

**Flags:**
- `--target <cli>` (optional): Target specific CLI (default: all detected)
- `--name <skill-name>` (optional): Override auto-generated skill name

**Environment:**
- Requires: Detected CLIs in MEMORY.md
- Requires: Template system available
- Requires: Read access to source file
- Requires: Write permissions to skill directories

## Output Specification

**User Messages:**
1. "Analyzing code from <file_path>..."
2. "Detected: <language>, <framework>, <purpose>"
3. Preview of generated SKILL.md wrapper
4. Human Gate prompt: `[approve]`, `[expand]`, `[edit]`, `[reject]`
5. On approval: "Skill extracted: <path>"

**File Operations:**
- Create `.<cli>/skills/<name>/SKILL.md`
- Create `.<cli>/skills/<name>/scripts/<original-file>` (copy)
- Create `.<cli>/skills/<name>/metadata.yaml`
- Update MEMORY.md

**MEMORY.md Updates:**
```yaml
skills_created:
  - name: <skill-name>
    created: 2026-02-04
    source: <file_path>
    type: extracted
    clis: [...]
```

## Side Effects

**Filesystem Changes:**
- New directory: `.<cli>/skills/<name>/`
- New files: SKILL.md, metadata.yaml
- Copied file: `scripts/<original-file>`
- Modified: MEMORY.md

**State Mutations:**
- Add extracted skill to registry
- Preserve original file untouched

## Error Cases

| Error | Condition | Handler |
|-------|-----------|---------|
| `E-EXTRACT-001` | File not found | Error with path + suggest alternatives |
| `E-EXTRACT-002` | File not readable | Permission error + suggest chmod |
| `E-EXTRACT-003` | Unsupported file type | Warning + generic wrapper |
| `E-EXTRACT-004` | Skill name collision | Trigger collision Human Gate (FR-008) |
| `E-EXTRACT-005` | Code contains secrets | Reject + security warning (T0-HEFESTO-11) |
| `E-EXTRACT-006` | File too large (>100KB) | Warning + confirmation |

## Performance Targets

- File read: < 100ms (typical)
- Code analysis: < 3s
- Template generation: < 2s
- Human Gate wait: unbounded
- Persistence: < 1s
- **Total (excluding Human Gate):** < 7s

## Dependencies

**Required Helpers:**
- `helpers/human-gate.md` - Approval workflow
- `helpers/template-validator.md` - T0 compliance
- `helpers/code-analyzer.md` - Language/framework detection
- `helpers/secret-detector.md` - Security scan (T0-HEFESTO-11)

**Required Templates:**
- `templates/extract/SKILL.md.template`
- `templates/base/metadata.yaml.template`

**State Files:**
- `MEMORY.md` - Skill registry

## Success Criteria Mapping

- **SC-001**: Command implemented
- **SC-003**: Human Gate enforced
- **SC-004**: Wizard mode for missing file_path
- **US-001 Scenario 2**: Code extraction

## Wizard Mode Specification

**Activation:** When `file_path` missing

**Questions:**
1. "Path to code file:" → `file_path`
2. "Skill name (auto-generated: <suggestion>):" → `name` (optional)
3. "Target CLIs [all detected]:" → `targets`

**Smart Defaults:**
- Auto-generate name from file basename (e.g., `validator.py` → `validator`)
- Detect language from extension
- Suggest description based on code structure

## Example Invocations

```bash
# Extract from file
/hefesto.extract ./utils/email-validator.py

# Wizard mode
/hefesto.extract
# → Path to code file: _

# Custom name
/hefesto.extract ./legacy-code.js --name modernized-validator

# Specific target
/hefesto.extract ./deploy.sh --target gemini
```

## Mapped Requirements

- **FR-002**: Human Gate enforcement
- **FR-003**: Wizard Mode support
- **FR-008**: Collision detection
- **US-001 Scenario 2**: Code-based extraction
- **T0-HEFESTO-02**: Human Gate protocol
- **T0-HEFESTO-06**: Validation before persist
- **T0-HEFESTO-11**: Security scanning
