# Hefesto Skill Generator - Documentation

> Human-readable documentation for understanding, maintaining, and extending Hefesto.

---

## Documentation Index

### Core Documentation

- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - System architecture, components, data flow, and design decisions
- **[decisions/](./decisions/)** - Architectural Decision Records (ADRs) documenting key decisions

---

## What is Hefesto?

Hefesto Skill Generator is a template-driven system that generates [Agent Skills](https://agentskills.io) for 17 AI CLI tools from natural language descriptions.

### Key Objectives

1. **Zero-code skill generation**: Generate skills from descriptions without writing code
2. **Multi-CLI support**: Single source generates for all detected AI CLIs
3. **Quality assurance**: Auto-critique with 13-point checklist + human gate approval
4. **Standard compliance**: Follow [agentskills.io](https://agentskills.io) specification
5. **Developer experience**: Simple install, intuitive commands, clear workflows

---

## What Does Hefesto Do?

### For Users

- **Create skills** from natural language descriptions (`/hefesto.create`)
- **Validate skills** against agentskills.io spec with auto-fix (`/hefesto.validate`)
- **Update skills** to modify existing skills (`/hefesto.update`)
- **Extract skills** from existing code/docs (`/hefesto.extract`)
- **Generate agents** by composing skills (`/hefesto.agent`)
- **List skills** installed in project (`/hefesto.list`)

### For Projects

- **Bootstrap** AI development with `hefesto init`
- **Auto-detect** installed AI CLIs (17 supported)
- **Install commands** for each detected CLI
- **Maintain consistency** across multi-CLI projects

---

## Architecture Overview

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

### Components

1. **Python CLI** - Bootstrap, detection, status (typer + rich)
2. **Templates** - Skill structure, quality checklist, CLI compatibility rules
3. **AI Commands** - 7 slash commands per CLI (`/hefesto.*`)
4. **Human Gate** - Approval workflow for all write operations
5. **Multi-CLI Output** - Simultaneous generation for all detected CLIs

See [ARCHITECTURE.md](./ARCHITECTURE.md) for detailed architecture documentation.

---

## Requirements

### For Users

- **At least 1 AI CLI** installed (Claude Code, Gemini CLI, Codex, Copilot, OpenCode, Cursor, Qwen, etc.)
- **Python 3.11+** for CLI installation
- **uv** or **pipx** recommended for installation

### For Skills

- Follow [agentskills.io](https://agentskills.io) specification
- SKILL.md < 500 lines, < ~5000 tokens
- Frontmatter: ONLY `name` + `description`
- Task-oriented sections ("How to [task]")

---

## Key Design Decisions

See [decisions/](./decisions/) for detailed ADRs:

- **[ADR-001](./decisions/ADR-001-agent-skills-standard.md)** - Why Agent Skills as primary standard
- **[ADR-002](./decisions/ADR-002-research-integration.md)** - Research integration strategy
- **[ADR-003](./decisions/ADR-003-lightweight-frontmatter.md)** - Lightweight frontmatter approach

---

## How to Extend Hefesto

### Add Support for New CLI

1. Add CLI rules to `templates/cli-compatibility.md`
2. Create 7 commands in CLI format (create, validate, update, extract, agent, init, list)
3. Update CLI detection in Python CLI
4. Test installation with `hefesto init`

### Add New Command

1. Create `hefesto.{cmd}.md` for Claude (canonical)
2. Adapt for other 16 CLIs
3. Update templates if needed
4. Document in README

---

## Links

| Resource | URL |
|----------|-----|
| Agent Skills Spec | https://agentskills.io |
| Main README | [../README.md](../README.md) |
| Contributing | [../CONTRIBUTING.md](../CONTRIBUTING.md) |
| Constitution (T0 Rules) | [../CONSTITUTION.md](../CONSTITUTION.md) |

---

**Hefesto Documentation** | v2.2.0 | 2026
