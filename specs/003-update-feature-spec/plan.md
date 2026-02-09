# Implementation Plan: Update Feature Spec to v2.2.0

**Branch**: `003-update-feature-spec` | **Date**: 2026-02-08 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/003-update-feature-spec/spec.md`, referenced card [CARD-003-v2.2.0-features.md](../../docs/cards/CARD-003-v2.2.0-features.md)

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement four major features for Hefesto v2.2.0:
1. **`/hefesto.update`** - New command to modify existing skill content (7-phase workflow)
2. **Web Research Integration** - Add conditional web search to create/extract/update commands
3. **`/hefesto.agent`** - New command to compose skills into specialized sub-agents (6-phase workflow)
4. **Payload Sync** - Fix drift between canonical commands and installer payloads (13-point checklist, Token Economy)

This is a template-driven, zero-code enhancement maintaining T0-HEFESTO-13 compliance.

## Technical Context

**Language/Version**: Markdown templates, PowerShell scripts (v5.1+)  
**Primary Dependencies**: None (template-driven, zero-code architecture per T0-HEFESTO-13)  
**Storage**: Local filesystem (`.claude/`, `.gemini/`, `.codex/`, `.github/`, `.opencode/`, `.cursor/`, `.qwen/`, `installer/payload/`)  
**Testing**: Manual validation via command execution in each CLI environment  
**Target Platform**: Windows/Linux/macOS with PowerShell, supporting 7 AI CLIs (Claude, Gemini, Codex, Copilot, OpenCode, Cursor, Qwen)  
**Project Type**: Multi-CLI agent skill generator (distributed template system)  
**Performance Goals**: Skill generation < 1 minute per command (SC-001)  
**Constraints**: 
- SKILL.md < 500 lines, ~5000 tokens (T0-HEFESTO-03)
- No external dependencies
- Human Gate required for all persistence (T0-HEFESTO-02)
- Must support all 7 CLIs with syntax adaptation  
**Scale/Scope**: 
- ~65 files modified/created
- 2 new commands (update, agent)
- 1 new template (agent-template.md)
- 7 target CLI directories to sync
- 100% payload/canonical consistency

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### T0 Rules (Absolute - Must Pass)

| Rule | Status | Notes |
|------|--------|-------|
| **T0-HEFESTO-01**: Agent Skills Standard | ✅ PASS | All generated skills follow agentskills.io spec with valid frontmatter |
| **T0-HEFESTO-02**: Human Gate Protocol | ✅ PASS | All commands include explicit Human Gate phase with [approve]/[edit]/[reject] |
| **T0-HEFESTO-03**: Progressive Disclosure | ✅ PASS | SKILL.md < 500 lines, agent commands < 200 lines |
| **T0-HEFESTO-04**: Multi-CLI Detection | ✅ PASS | Commands detect all 7 CLIs automatically via PATH/config dirs |
| **T0-HEFESTO-05**: Local Storage | ✅ PASS | All artifacts persist to project-local directories by default |
| **T0-HEFESTO-06**: Auto-Critique | ✅ PASS | Update uses 13-point checklist, agent uses 7-point checklist |
| **T0-HEFESTO-07**: Name Validation | ✅ PASS | Skill naming enforced via regex `^[a-z0-9]+(-[a-z0-9]+)*$` |
| **T0-HEFESTO-09**: CLI Compatibility | ✅ PASS | Syntax adaptation `$ARGUMENTS` ↔ `{{args}}` per CLI |
| **T0-HEFESTO-11**: Security | ✅ PASS | Auto-critique includes "No credentials/secrets/PII" as CRITICAL check |
| **T0-HEFESTO-12**: Quality Assurance | ✅ PASS | Generate → Auto-Critique → Fix → Human Gate workflow enforced |
| **T0-HEFESTO-13**: Template Authority | ✅ PASS | Zero Python/Node.js code; all logic in Markdown templates |

### T1 Rules (Strong Guidelines)

| Rule | Status | Notes |
|------|--------|-------|
| **T1-HEFESTO-03**: Web Research | 🆕 NEW | Being added in this feature; conditional web search for URL verification |

### Violations Requiring Justification

None. All T0 rules satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
hefesto-skill-generator/
├── .claude/commands/           # Claude CLI canonical commands
│   ├── hefesto.create.md       # ✏️ Modified (add web research step)
│   ├── hefesto.extract.md      # ✏️ Modified (add web research, fix 10→13 drift)
│   ├── hefesto.update.md       # 🆕 New (7-phase update workflow)
│   └── hefesto.agent.md        # 🆕 New (6-phase agent generation)
├── .gemini/commands/           # Gemini CLI TOML wrappers
│   ├── hefesto.create.toml     # ✏️ Modified (overhaul: 13-pt, Token Economy, "How to")
│   ├── hefesto.extract.toml    # ✏️ Modified (13-pt, web research)
│   ├── hefesto.update.toml     # 🆕 New
│   └── hefesto.agent.toml      # 🆕 New
├── .codex/prompts/             # OpenAI Codex CLI
│   ├── hefesto.update.md       # 🆕 New
│   └── hefesto.agent.md        # 🆕 New
├── .github/
│   ├── agents/                 # Copilot native agent format
│   │   ├── hefesto.update.agent.md    # 🆕 New
│   │   └── hefesto.agent.agent.md     # 🆕 New
│   └── prompts/                # Copilot prompt stubs
│       ├── hefesto.update.prompt.md   # 🆕 New
│       └── hefesto.agent.prompt.md    # 🆕 New
├── .opencode/command/          # OpenCode CLI
├── .cursor/commands/           # Cursor CLI
├── .qwen/commands/             # Qwen CLI (uses {{args}})
├── templates/                  # Shared templates
│   ├── agent-template.md       # 🆕 New (agent command blueprint)
│   └── cli-compatibility.md    # ✏️ Modified (add agent-specific notes)
├── .hefesto/
│   ├── version                 # ✏️ Modified (2.1.0 → 2.2.0)
│   └── templates/              # Installed templates (copies from /templates)
│       └── agent-template.md   # 🆕 New
├── installer/
│   ├── install.ps1             # ✏️ Modified (version bump)
│   ├── install.sh              # ✏️ Modified (version bump)
│   └── payload/                # Distribution payloads (mirror of .<cli>/ structure)
│       ├── commands/claude/    # 🆕 2 new, ✏️ 2 modified
│       ├── commands/gemini/    # 🆕 2 new, ✏️ 2 modified (fix drift)
│       ├── commands/codex/     # 🆕 2 new, ✏️ 2 modified
│       ├── commands/github/    # 🆕 4 new (agents + prompts)
│       ├── commands/opencode/  # 🆕 2 new
│       ├── commands/cursor/    # 🆕 2 new
│       ├── commands/qwen/      # 🆕 2 new
│       └── hefesto/templates/
│           └── agent-template.md  # 🆕 New
├── CONSTITUTION.md             # ✏️ Modified (add T1-HEFESTO-03, bump 2.0.0 → 2.1.0)
├── AGENTS.md                   # ✏️ Modified (add update/agent, bump version)
└── docs/
    └── ARCHITECTURE.md         # ✏️ Modified (add update/agent flows, bump version)
```

**Structure Decision**: Multi-CLI distributed template system. No traditional `src/` or `tests/` directories. All logic lives in Markdown command files distributed across 7 CLI-specific directories plus installer payloads. This feature modifies existing commands and adds 2 new commands across all directories.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. All T0 rules satisfied.

## Phase 0: Research & Clarifications

**Status**: NEEDS EXECUTION

### Research Tasks

1. **Web Search Tool Availability**
   - **Question**: Which CLIs support web search natively?
   - **Why**: Need to know if conditional web research is universally available or requires CLI-specific handling
   - **Expected Finding**: Document which CLIs have `web_search` tool and which don't

2. **Agent Command Placement**
   - **Question**: For non-Copilot CLIs, do agent commands go in `/commands/` or separate `/agents/` directory?
   - **Why**: Copilot has dual structure (.github/agents + .github/prompts); need to confirm pattern for others
   - **Expected Finding**: Confirm that non-Copilot CLIs use single `/commands/` directory

3. **TOML Multi-line String Best Practices**
   - **Question**: What's the safest escaping strategy for Gemini TOML files with complex Markdown?
   - **Why**: Need to ensure 13-point table with pipes doesn't break TOML parsing
   - **Expected Finding**: Confirm `"""..."""` raw string literal is sufficient; identify any edge cases

4. **Existing Drift Audit**
   - **Question**: Are there other commands beyond create/extract with drift?
   - **Why**: CARD-003 mentions validate, init, list need verification
   - **Expected Finding**: Complete list of files with version/checklist inconsistencies

5. **Agent Naming Convention**
   - **Question**: Should generated agents follow skill naming rules (lowercase-hyphen)?
   - **Why**: Agents are commands, not skills; may need different validation
   - **Expected Finding**: Confirm agents follow same `^[a-z0-9]+(-[a-z0-9]+)*$` pattern

### Outputs

All findings will be documented in `research.md` with:
- Decision: [what was chosen]
- Rationale: [why chosen]
- Alternatives considered: [what else evaluated]

## Phase 1: Design Artifacts

**Status**: PENDING (blocked on Phase 0)

### 1.1 Data Model (`data-model.md`)

**Key Entities**:

```markdown
### Skill (existing)
- name: string (lowercase-hyphen, max 64 chars)
- description: string (max 1024 chars, "Use when:" required)
- body: markdown content
- metadata: frontmatter YAML

### Agent (new)
- name: string (same rules as skill)
- description: string (max 1024 chars)
- persona: string (required, specific role description)
- skills: list[skill_reference] (paths to composed skills)
- workflow: ordered_list[step] (sequential execution steps)
- rules: list[constraint] (behavioral constraints)
- target_cli: enum[claude, gemini, codex, github, opencode, cursor, qwen]

### CLI (existing)
- name: string
- config_dir: path
- command_dir: path (e.g., ".claude/commands/", ".gemini/commands/")
- agent_dir: optional[path] (only GitHub Copilot has ".github/agents/")
- syntax_variant: enum["$ARGUMENTS", "{{args}}"]

### Template (existing)
- name: string
- path: path
- type: enum[skill, agent, command]
- locations: list[path] (templates/, .hefesto/templates/, installer/payload/hefesto/templates/)

### UpdateChange (new)
- skill_name: string
- change_description: string
- sections_to_modify: list[string]
- web_research_needed: boolean
```

**Relationships**:
- Agent COMPOSES 1+ Skill (read-only references)
- CLI HAS_MANY Command
- Template IS_COPIED_TO 3 locations (source in templates/, installed in .hefesto/templates/, payload in installer/)

### 1.2 API Contracts (`contracts/`)

Not applicable - this is a command-based system, not API-driven.

### 1.3 Quickstart Guide (`quickstart.md`)

**Status**: To be generated in Phase 1

Will include:
- How to run `/hefesto.update <skill-name> <change-description>`
- How to run `/hefesto.agent "<agent description>"`
- How web research is triggered (conditional, automatic)
- Expected Human Gate prompts
- How to verify payload sync

## Phase 2: Task Generation

**Status**: NOT STARTED (handled by `/speckit.tasks` command after plan approval)

Tasks will be generated based on Step 0-5 in CARD-003:
- Step 0: Governance (version bumps, CONSTITUTION)
- Step 1: Web Research Integration (modify create/extract)
- Step 2: `/hefesto.update` command (create + propagate)
- Step 3: `/hefesto.agent` command + template (create + propagate)
- Step 4: Payload Sync (fix Gemini drift, propagate all)
- Step 5: Documentation (AGENTS.md, ARCHITECTURE.md, cli-compatibility.md)

Estimated: 120-130 tasks with dependencies (actual: 130 tasks generated in tasks.md).

## Next Steps

1. **Human approval**: Review this plan for accuracy and completeness
2. **Phase 0 execution**: Run research tasks, create `research.md`
3. **Phase 1 execution**: Generate `data-model.md`, `quickstart.md`
4. **Constitution re-check**: Verify design doesn't violate T0 rules
5. **Phase 2 planning**: Generate `tasks.md` with `/speckit.tasks` command
