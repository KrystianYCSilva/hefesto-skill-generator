# Contract: /hefesto.adapt

## Command Purpose
Adapt existing skill from one CLI to another with syntax/format transformations.

## Input Specification

**Args:**
- `skill_name` (positional, required): Name of skill to adapt
- `--target <cli>` (flag, required): Target CLI (claude, gemini, codex, copilot, opencode, cursor, qwen)

**Flags:**
- `--source <cli>` (optional): Source CLI (auto-detected if only one exists)
- `--force` (optional): Skip Human Gate (DANGEROUS - not recommended)

**Environment:**
- Requires: Source skill exists
- Requires: Target CLI detected in MEMORY.md
- Requires: Adapter for target CLI available

## Output Specification

**User Messages:**
1. "Adapting <skill-name> from <source> to <target>..."
2. "Applying transformations: <list>"
3. Preview of adapted skill with diff
4. Human Gate prompt: `[approve]`, `[edit]`, `[reject]`
5. On approval: "Skill adapted: <path>"

**File Operations:**
- Create `.<target-cli>/skills/<name>/SKILL.md`
- Create `.<target-cli>/skills/<name>/metadata.yaml`
- Copy/transform scripts if needed
- Update MEMORY.md

**MEMORY.md Updates:**
```yaml
skills_created:
  - name: <skill-name>
    created: 2026-02-04
    adapted_from: <source-cli>
    clis: [<target-cli>]
```

## Side Effects

**Filesystem Changes:**
- New directory: `.<target-cli>/skills/<name>/`
- New files: SKILL.md, metadata.yaml, scripts/
- Modified: MEMORY.md

**State Mutations:**
- Add adapted skill to registry
- Preserve source skill untouched

## Error Cases

| Error | Condition | Handler |
|-------|-----------|---------|
| `E-ADAPT-001` | Source skill not found | Error + list available |
| `E-ADAPT-002` | Target CLI not detected | Error + suggest `/hefesto.detect` |
| `E-ADAPT-003` | Adapter not available | Error + list supported targets |
| `E-ADAPT-004` | Target skill already exists | Collision Human Gate (FR-008) |
| `E-ADAPT-005` | Transformation fails validation | Show errors + block persist |
| `E-ADAPT-006` | Source in multiple CLIs | Require explicit `--source` |

## Performance Targets

- Source skill load: < 200ms
- Transformation: < 2s
- Validation: < 500ms
- Human Gate wait: unbounded
- Persistence: < 1s
- **Total (excluding Human Gate):** < 4s

## Dependencies

**Required Helpers:**
- `helpers/human-gate.md` - Approval workflow
- `helpers/template-validator.md` - Post-adapt validation
- `helpers/cli-adapters/<target>.md` - Transformation rules

**Required Templates:**
- Target CLI templates

**State Files:**
- `MEMORY.md` - CLI detection and skill registry

## Success Criteria Mapping

- **SC-001**: Command implemented
- **SC-003**: Human Gate enforced
- **US-003 Scenario 1**: CLI adaptation
- **FR-002**: Human Gate requirement
- **T0-HEFESTO-09**: Multi-CLI compatibility

## Adaptation Rules (by CLI)

**Gemini/Qwen:**
- Transform `$ARGUMENTS` → `{{args}}`
- Generate TOML variant if supported

**Codex:**
- Preserve `$ARGUMENTS` syntax
- Adjust context window hints

**Copilot:**
- Add GitHub-specific metadata
- Transform to `.github/skills/` structure

## Example Invocations

```bash
# Adapt Claude skill to Gemini
/hefesto.adapt email-validator --target gemini

# Explicit source
/hefesto.adapt testing-strategy --source claude --target copilot

# Force without Human Gate (NOT RECOMMENDED)
/hefesto.adapt deploy-aws --target cursor --force
```

## Mapped Requirements

- **FR-002**: Human Gate enforcement
- **US-003 Scenario 1**: Cross-CLI adaptation
- **T0-HEFESTO-02**: Human Gate protocol
- **T0-HEFESTO-08**: Idempotent collision handling
- **T0-HEFESTO-09**: CLI compatibility matrix
