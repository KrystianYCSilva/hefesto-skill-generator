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
                    CONSTITUTION.md
                    (T0 governance rules)
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
| `/hefesto.validate` | Validate skill against spec | No (read-only) |
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
Phase 4: Auto-Critica      → Self-review against 10-point checklist
Phase 5: Human Gate        → Present to user for [approve] [edit] [reject]
Phase 6: Persistence       → Write to all detected CLI directories
```

---

## Installation

### Option 1: Clone (Recommended)

```bash
git clone https://github.com/<org>/hefesto-skill-generator.git
cd my-project

# Copy commands to your project
cp -r hefesto-skill-generator/.claude/commands/hefesto.*.md .claude/commands/
cp -r hefesto-skill-generator/templates/ templates/
cp hefesto-skill-generator/CONSTITUTION.md .

# Initialize
/hefesto.init
```

### Option 2: Use directly in repo

```bash
git clone https://github.com/<org>/hefesto-skill-generator.git
cd hefesto-skill-generator
/hefesto.init
/hefesto.create "My first skill"
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

# skill-id

Brief introduction.

## Instructions

1. Step-by-step workflow

## Examples

### Example 1: Title

**Input:** realistic input
**Output:** expected output

## References

- [Official Docs](https://...)
- [Standard](https://...)
```

---

## Project Structure

```
hefesto-skill-generator/
├── CONSTITUTION.md              # T0 governance rules (13 rules)
├── AGENTS.md                    # AI agent bootstrap
├── templates/
│   ├── skill-template.md        # Canonical skill structure
│   ├── quality-checklist.md     # 10-point auto-critica checklist
│   └── cli-compatibility.md     # Multi-CLI adaptation rules
├── .claude/commands/             # 5 hefesto + 9 speckit commands
├── .gemini/commands/             # Mirrored for Gemini
├── .codex/prompts/               # Mirrored for Codex
├── .opencode/command/            # Mirrored for OpenCode
├── .cursor/commands/             # Mirrored for Cursor
├── .claude/skills/               # Generated skills
├── knowledge/                    # Best practices, research
├── .context/                     # Project context files
└── docs/                         # Documentation, decisions
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
