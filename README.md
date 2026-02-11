# Hefesto Skill Generator

> **Hybrid Agent Skill generator for 7 AI CLIs**

[![Version](https://img.shields.io/badge/version-2.2.0-blue)]()
[![Agent Skills](https://img.shields.io/badge/standard-Agent%20Skills-green)](https://agentskills.io)
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## What is Hefesto?

**Hefesto** generates [Agent Skills](https://agentskills.io) for 7 AI CLI tools from natural language descriptions.

**Hybrid architecture:**
- **Python CLI** (`hefesto`): Bootstrap, status, list commands
- **AI Slash Commands** (`/hefesto.*`): Template-driven skill generation by AI agents

Named after the Greek god of the forge, Hefesto crafts specialized tools (skills) that empower AI agents.

---

## Architecture

```
PYTHON CLI (hefesto)  →  Bootstrap + Management
                         ↓
                    .hefesto/templates/
                         ↓
MARKDOWN TEMPLATES  →  AI AGENT  →  SKILLS (output)
                         ↑
                    skill-template.md
                    quality-checklist.md
                    cli-compatibility.md
```

- **Python CLI**: Bootstrap, detection, status (typer + rich)
- **Template-driven AI**: Skill generation via Markdown templates
- **Multi-CLI**: Auto-detects and generates for all 17 CLIs simultaneously
- **Self-reviewing**: Auto-critica 13-point checklist before human approval

---

## Supported CLIs (17 total)

| CLI | Skills Directory | Variable Syntax | Type |
|-----|------------------|-----------------|------|
| GitHub Copilot | `.github/skills/` | `$ARGUMENTS` | IDE |
| Claude Code | `.claude/skills/` | `$ARGUMENTS` | CLI |
| Gemini CLI | `.gemini/skills/` | `{{args}}` | CLI |
| Cursor | `.cursor/skills/` | `$ARGUMENTS` | IDE |
| Qwen Code | `.qwen/skills/` | `{{args}}` | CLI |
| opencode | `.opencode/skills/` | `$ARGUMENTS` | CLI |
| Codex CLI | `.codex/skills/` | `$ARGUMENTS` | CLI |
| Windsurf | `.windsurf/skills/` | `$ARGUMENTS` | IDE |
| Kilo Code | `.kilocode/skills/` | `$ARGUMENTS` | IDE |
| Auggie CLI | `.augment/skills/` | `$ARGUMENTS` | CLI |
| CodeBuddy | `.codebuddy/skills/` | `$ARGUMENTS` | CLI |
| Qoder CLI | `.qoder/skills/` | `$ARGUMENTS` | CLI |
| Roo Code | `.roo/skills/` | `$ARGUMENTS` | IDE |
| Amazon Q CLI | `.amazonq/skills/` | `$ARGUMENTS` | CLI |
| Amp | `.agents/skills/` | `$ARGUMENTS` | CLI |
| SHAI | `.shai/skills/` | `$ARGUMENTS` | CLI |
| IBM Bob | `.bob/skills/` | `$ARGUMENTS` | IDE |

---

## Commands

### Python CLI

| Command | Description |
|---------|-------------|
| `hefesto init` | Bootstrap: detect CLIs, create .hefesto/, install slash commands |
| `hefesto check` | Show status (version, templates, CLIs, skills) |
| `hefesto list` | List all installed skills across CLIs |
| `hefesto version` | Show Hefesto CLI version |

### AI Slash Commands

| Command | Description | Human Gate |
|---------|-------------|------------|
| `/hefesto.create` | Create skill from description | Yes |
| `/hefesto.validate` | Validate & fix skill against spec | Yes (fix-auto) |
| `/hefesto.update` | Update existing skill | Yes |
| `/hefesto.extract` | Extract skill from code/docs | Yes |
| `/hefesto.agent` | Generate specialized agent | Yes |
| `/hefesto.init` | Verify Hefesto installation | No |
| `/hefesto.list` | List installed skills | No (read-only) |

---

## Quick Start

### 1. Install Python CLI

```bash
uv tool install hefesto-cli --from git+https://github.com/KrystianYCSilva/hefesto-skill-generator.git
```

### 2. Initialize in Your Project

```bash
cd your-project/
hefesto init        # Detects CLIs, creates .hefesto/, installs slash commands
hefesto check       # Verify installation
```

### 3. Use Slash Commands (in AI CLI)

```bash
# Create your first skill
/hefesto.create "Validate email addresses using RFC 5322 regex patterns"

# Validate the generated skill
/hefesto.validate validate-email

# List all skills
hefesto list        # Or /hefesto.list in AI CLI

# Extract skill from existing code
/hefesto.extract src/utils/date-formatter.ts
```

---

## How `/hefesto.create` Works

```
Phase 1: Understanding    → Parse description, extract concepts
Phase 2: Research          → Read templates, exemplar skills, official docs
Phase 3: Generation        → Generate SKILL.md following agentskills.io spec
Phase 4: Auto-Critica      → Self-review against 13-point checklist
Phase 5: Human Gate        → Present to user for [approve] [edit] [reject]
Phase 6: Persistence       → Write to all detected CLI directories
```

---

## Installation

### Option 1: Python CLI (Recommended)

```bash
# Install globally with uv
uv tool install hefesto-cli --from git+https://github.com/KrystianYCSilva/hefesto-skill-generator.git

# Or with pipx
pipx install git+https://github.com/KrystianYCSilva/hefesto-skill-generator.git

# Or from local clone
git clone https://github.com/KrystianYCSilva/hefesto-skill-generator.git
cd hefesto-skill-generator
uv tool install .
```

See [INSTALL.md](INSTALL.md) for detailed installation instructions and troubleshooting.

### Option 2: Installer Script (Legacy)

```bash
# Unix/macOS
git clone https://github.com/<org>/hefesto-skill-generator.git
cd my-project
bash hefesto-skill-generator/installer/install.sh
```

```powershell
# Windows PowerShell
git clone https://github.com/<org>/hefesto-skill-generator.git
cd my-project
& hefesto-skill-generator\installer\install.ps1
```

The installer automatically:
- Detects installed AI CLIs (Claude, Gemini, Codex, Copilot, OpenCode, Cursor, Qwen)
- Creates `.hefesto/` with templates and version
- Installs `hefesto.*` commands for each detected CLI
- Creates `skills/` directories

### Option 2: GitHub Release

```bash
# Unix/macOS
curl -fsSL https://github.com/<org>/hefesto-skill-generator/releases/latest/download/hefesto-latest.tar.gz | tar xz
cd installer && bash install.sh
```

```powershell
# Windows
Invoke-WebRequest -Uri "https://github.com/<org>/hefesto-skill-generator/releases/latest/download/hefesto-latest.zip" -OutFile hefesto.zip
Expand-Archive hefesto.zip; cd installer; .\install.ps1
```

### Verify Installation

```bash
/hefesto.init  # Check installation status
```

---

## Skill Structure

```
skill-name/
├── SKILL.md              # Core (required, <500 lines, <5000 tokens)
├── references/           # Deep-dive docs (optional, JIT loaded)
├── scripts/              # Executable helpers (optional)
└── assets/               # Static resources (optional)
```

### Skill Template

```yaml
---
name: skill-id
description: |
  Action verb describing what the skill does.
  Use when: specific trigger condition.
---

# Skill Title

Brief introduction.

## How to <first capability>

Task-oriented instructions.

## How to <second capability>

More task-oriented instructions.
```

**Frontmatter:** ONLY `name` + `description` (no license, metadata, version)

---

## Project Structure

```
hefesto-skill-generator/
├── installer/
│   ├── install.sh               # Bash installer (Unix/macOS)
│   ├── install.ps1              # PowerShell installer (Windows)
│   └── payload/                 # Distributable package
│       ├── hefesto/templates/   # Templates shipped to .hefesto/
│       └── commands/            # Commands per CLI
├── templates/
│   ├── skill-template.md        # Canonical skill structure
│   ├── quality-checklist.md     # 13-point auto-critica checklist
│   └── cli-compatibility.md     # Multi-CLI adaptation rules
├── .claude/commands/             # hefesto + speckit commands
├── .gemini/commands/             # Mirrored for Gemini (TOML)
├── .codex/prompts/               # Mirrored for Codex
├── .github/agents+prompts/       # Mirrored for Copilot
├── .opencode/command/            # Mirrored for OpenCode
├── .cursor/commands/             # Mirrored for Cursor
├── .qwen/commands/               # Mirrored for Qwen
├── .agents/                      # Internal agent skills (skill-creator)
├── .specify/                     # Spec-kit infrastructure (templates, scripts)
├── .context/                     # AI context hub (rules, patterns, examples)
├── knowledge/                    # Best practices and research references
├── specs/                        # Feature specifications (spec-kit artifacts)
└── docs/                         # Documentation, ADRs, guides
```

### User Project (after install)

```
my-project/
├── .hefesto/
│   ├── version                  # 2.2.0")
│   └── templates/               # Skill template, checklist, CLI rules
├── .claude/commands/hefesto.*   # Commands (per detected CLI)
├── .claude/skills/              # Skills directory (per detected CLI)
└── ...
```

---

## Links

| Resource | URL |
|----------|-----|
| Agent Skills Spec | https://agentskills.io |
| Claude Code Skills | https://docs.anthropic.com/en/docs/claude-code/skills |
| Gemini CLI | https://geminicli.com |
| OpenAI Codex | https://developers.openai.com/codex |
| VS Code/Copilot Skills | https://code.visualstudio.com/docs/copilot/customization/agent-skills |

---

## Also in This Repo

- **Spec-kit** (`speckit.*` commands): Feature specification workflow (specify, plan, tasks, implement)
- **Skill Creator** (`.agents/skills/skill-creator/`): Reference implementation for agentskills.io

## Contributing & Governance

- See `CONTRIBUTING.md` for how to contribute
- See `CODE_OF_CONDUCT.md` for community behavior expectations
- See `CONSTITUTION.md` for T0 governance rules (13 rules)
- Licensed under MIT - see `LICENSE`

---

**Hefesto Skill Generator** | Forging tools for AI agents | 2026



