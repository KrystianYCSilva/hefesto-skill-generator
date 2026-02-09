# hefesto-skill-generator Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-08

## Active Technologies

- Markdown templates, PowerShell scripts (v5.1+) (003-update-feature-spec)
- Template-driven, zero-code architecture (T0-HEFESTO-13)
- Multi-CLI agent skill generator (7 CLIs: Claude, Gemini, Codex, Copilot, OpenCode, Cursor, Qwen)

## Project Structure

```text
.<cli>/                      # CLI-specific directories (7 total)
├── commands/                # Command files (.md or .toml)
├── skills/                  # Skill directories
└── .../

templates/                   # Canonical templates
.hefesto/                   # Installed configuration
installer/                  # Distribution payloads
specs/                      # Feature specifications
```

## Commands

```powershell
# List all Hefesto commands
/hefesto.list

# Create new skill
/hefesto.create "<description>"

# Update existing skill
/hefesto.update <skill-name> "<change-description>"

# Generate agent from skills
/hefesto.agent "<agent description>"

# Validate skill
/hefesto.validate <skill-name>
```

## Code Style

**Markdown**: Follow agentskills.io specification
**PowerShell**: Follow standard conventions
**TOML**: Use `"""..."""` raw strings for complex content

## Recent Changes

- **v2.2.0** (003-update-feature-spec): Added `/hefesto.update`, `/hefesto.agent`, Web Research Integration, Payload Sync (10→13 point checklist)

## Feature-specific Context: v2.2.0

**New Commands**:
- `/hefesto.update` - 7-phase workflow to modify existing skill content
- `/hefesto.agent` - 6-phase workflow to compose skills into specialized agents

**New Concepts**:
- **Web Research Integration**: Conditional web search in create/extract/update commands for URL verification
- **Agent Composition**: Agents reference skills via file paths, creating specialized workflows
- **Payload Sync**: Fixed drift between canonical commands and installer payloads

**Quality Checklists**:
- Skills: 13-point checklist (CRITICAL/WARNING/INFO severity)
- Agents: 7-point checklist (focus on skill composition integrity)

**File Patterns**:
- Skills: `.<cli>/skills/<name>/SKILL.md`
- Agents: `.<cli>/commands/<name>.md` (except Copilot: `.github/agents/<name>.agent.md`)
- Templates: 3 locations (source, installed, payload)

**Constitution Rules** (all passing):
- T0-HEFESTO-01 to T0-HEFESTO-13
- T1-HEFESTO-03 (Web Research) - NEW in v2.2.0

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
