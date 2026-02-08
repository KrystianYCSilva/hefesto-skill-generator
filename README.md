# Hefesto Skill Generator

> **Template-driven Agent Skill generator for 7 AI CLIs**

[![Version](https://img.shields.io/badge/version-2.0.0-blue)]()
[![Agent Skills](https://img.shields.io/badge/standard-Agent%20Skills-green)](https://agentskills.io)
[![License](https://img.shields.io/badge/license-MIT-green)]()
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen)]()

---

## What is Hefesto?

**Hefesto** generates [Agent Skills](https://agentskills.io) for 7 AI CLI tools from natural language descriptions. It's a **spec-kit**: Markdown templates that the AI interprets - zero Python, zero dependencies.

Named after the Greek god of the forge, Hefesto crafts specialized tools (skills) that empower AI agents.

---

## Architecture

```
MARKDOWN TEMPLATES  →  AI AGENT  →  SKILLS (output)
                         ↑
                    skill-template.md
                    quality-checklist.md
                    cli-compatibility.md
```

- **No code**: All logic lives in Markdown templates
- **No dependencies**: No Python, Node.js, pip, or npm
- **Multi-CLI**: Generates for all detected CLIs simultaneously
- **Self-reviewing**: Auto-critica checklist before human approval

---

## Supported CLIs

| CLI | Skills Directory | Variable Syntax |
|-----|------------------|-----------------|
| Claude Code | `.claude/skills/` | `$ARGUMENTS` |
| Gemini CLI | `.gemini/skills/` | `{{args}}` |
| OpenAI Codex | `.codex/skills/` | `$ARGUMENTS` |
| VS Code/Copilot | `.github/skills/` | `$ARGUMENTS` |
| OpenCode | `.opencode/skills/` | `$ARGUMENTS` |
| Cursor | `.cursor/skills/` | `$ARGUMENTS` |
| Qwen Code | `.qwen/skills/` | `{{args}}` |

---

## Commands

| Command | Description | Human Gate |
|---------|-------------|------------|
| `/hefesto.create` | Create skill from description | Yes |
| `/hefesto.validate` | Validate & fix skill against spec | Yes (fix-auto) |
| `/hefesto.extract` | Extract skill from code/docs | Yes |
| `/hefesto.init` | Bootstrap: detect CLIs, create dirs | No |
| `/hefesto.list` | List installed skills | No (read-only) |

---

## Quick Start

```bash
# 1. Initialize (detects CLIs, creates directories)
/hefesto.init

# 2. Create your first skill
/hefesto.create "Validate email addresses using RFC 5322 regex patterns"

# 3. Validate the generated skill
/hefesto.validate validate-email

# 4. List all skills
/hefesto.list

# 5. Extract skill from existing code
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

### Option 1: Installer Script (Recommended)

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
├── .claude/commands/             # 5 hefesto + speckit commands
├── .gemini/commands/             # Mirrored for Gemini (TOML)
├── .codex/prompts/               # Mirrored for Codex
├── .github/agents+prompts/       # Mirrored for Copilot
├── .opencode/command/            # Mirrored for OpenCode
├── .cursor/commands/             # Mirrored for Cursor
├── .qwen/commands/               # Mirrored for Qwen
├── .context/                     # Project context files
└── docs/                         # Documentation, decisions
```

### User Project (after install)

```
my-project/
├── .hefesto/
│   ├── version                  # Installed version ("2.0.0")
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

## Contributing & Governance

- See `CONTRIBUTING.md` for how to contribute
- See `CODE_OF_CONDUCT.md` for community behavior expectations
- See `CONSTITUTION.md` for T0 governance rules
- Licensed under MIT - see `LICENSE`

---

**Hefesto Skill Generator** | Forging tools for AI agents | 2026
