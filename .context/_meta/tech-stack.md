# Tech Stack - Hefesto Skill Generator

> **Tier:** T2 - Informativo
> **Versao:** 2.2.0
---

## 1. Arquitetura

### Tipo de Sistema

**Hybrid Architecture** - Python CLI para bootstrap + Markdown templates para AI-driven skill generation.

### Componentes

```
PYTHON CLI (hefesto)  ->  Bootstrap + Management
                          ↓
                     .hefesto/templates/
                          ↓
MARKDOWN TEMPLATES  ->  AI AGENT  ->  SKILLS (output)
                          ^
                     skill-template.md
                     quality-checklist.md
                     cli-compatibility.md
```

**Camadas:**
1. **Python CLI** (`hefesto-cli`): init, check, list, version
2. **Templates**: Markdown files que AI agents interpretam
3. **Slash Commands**: `/hefesto.*` para operações guiadas por AI

---

## 2. Stack Tecnica

### Core

| Componente | Tecnologia | Justificativa |
|------------|------------|---------------|
| CLI | Python 3.11+ (Typer + Rich) | User-facing commands |
| Formato | Markdown + YAML frontmatter | Padrao Agent Skills |
| Templates | 4 Markdown (skill, checklist, CLI map, agent) | Fonte de verdade |
| Installer | Python wheel + legacy bash/PowerShell | Cross-platform install |
| Package Manager | uv / pipx / pip | Isolated global install |
| CI/CD | GitHub Actions | Build + release automatizado |

### Python Dependencies

| Dependency | Version | Uso |
|------------|---------|-----|
| typer | >=0.12.0 | CLI framework |
| rich | >=13.0.0 | Terminal UI (tables, panels, trees) |
| hatchling | build-time | Wheel builder |

### Armazenamento

| Local | Uso | Formato |
|-------|-----|---------|
| `.hefesto/` | Namespace Hefesto no projeto usuario | Templates + version |
| `.hefesto/templates/` | Templates distribuidos | Markdown |
| `.<cli>/commands/` | Comandos hefesto.* por CLI | `.md` ou `.toml` |
| `.<cli>/skills/` | Skills geradas | Markdown (SKILL.md) |
| `templates/` | Templates fonte (repo Hefesto) | Markdown |
| `installer/payload/` | Pacote distribuivel | Markdown + scripts |

### Formatos Suportados

| Formato | Uso |
|---------|-----|
| Markdown (SKILL.md) | Formato primario de skills |
| YAML | Frontmatter (name + description) |
| TOML | Formato alternativo (Gemini commands) |

---

## 3. CLIs Suportados

| CLI | Skills Dir | Commands Dir | Formato Cmd | Variable Syntax |
|-----|-----------|-------------|-------------|-----------------|
| Claude Code | `.claude/skills/` | `.claude/commands/` | `.md` | `$ARGUMENTS` |
| Gemini CLI | `.gemini/skills/` | `.gemini/commands/` | `.toml` | `{{args}}` |
| OpenAI Codex | `.codex/skills/` | `.codex/prompts/` | `.md` | `$ARGUMENTS` |
| VS Code/Copilot | `.github/skills/` | `.github/agents/` + `prompts/` | `.md` | `$ARGUMENTS` |
| OpenCode | `.opencode/skills/` | `.opencode/command/` | `.md` | `$ARGUMENTS` |
| Cursor | `.cursor/skills/` | `.cursor/commands/` | `.md` | `$ARGUMENTS` |
| Qwen Code | `.qwen/skills/` | `.qwen/commands/` | `.md` | `{{args}}` |

---

## 4. Estrutura de Arquivos

### Repositorio Hefesto

```
hefesto-skill-generator/
  README.md
  INSTALL.md
  pyproject.toml                # Python package config
  src/hefesto_cli/
    __init__.py                 # CLI principal (~450 linhas)
  templates_hefesto/            # Templates distribuidos via wheel
    skill-template.md
    quality-checklist.md
    cli-compatibility.md
    agent-template.md
    commands/                   # 7 slash commands
      hefesto.create.md
      hefesto.validate.md
      hefesto.update.md
      hefesto.extract.md
      hefesto.agent.md
      hefesto.init.md
      hefesto.list.md
  templates/                    # Templates fonte (legacy, deprecated)
  installer/                    # Installer scripts (legacy)
  .<cli>/commands/hefesto.*     # Comandos por CLI (7 CLIs)
  .<cli>/skills/                # Skills de demonstracao
  .context/                     # Contexto para IAs
  docs/
  specs/
```

### Projeto do Usuario (apos `hefesto init`)

```
meu-projeto/
  .hefesto/
    version                    # "2.2.0"
    templates/                 # 4 templates
      skill-template.md
      quality-checklist.md
      cli-compatibility.md
      agent-template.md
  .<cli>/
    commands/hefesto.*         # 7 comandos
    skills/                    # Skills geradas (vazio inicialmente)
```

---

## 5. Dependencias

### Runtime (Python CLI)

| Dependencia | Versao | Obrigatorio |
|-------------|--------|-------------|
| Python | 3.11+ | Sim |
| typer | >=0.12.0 | Sim (auto-instalado) |
| rich | >=13.0.0 | Sim (auto-instalado) |

### Runtime (Skill Generation)

| Dependencia | Tipo | Obrigatorio |
|-------------|------|-------------|
| CLI de IA (qualquer 1 dos 7) | Runtime | Sim (para usar slash commands) |
| Filesystem | Sistema | Sim |
| Git | Sistema | Nao (recomendado) |

### Instalacao

| Dependencia | Tipo | Recomendado |
|-------------|------|-------------|
| uv | Package manager | Sim |
| pipx | Package manager | Alternativa |
| pip | Package manager | Alternativa |

---

## 6. Integracao

### Com Sistemas Existentes

| Sistema | Integracao |
|---------|-----------|
| spec-kit | Comandos /speckit.* compativeis |
| agentskills.io | Standard de skills seguido |

### APIs Externas

Nenhuma API externa necessaria. Sistema completamente local.

---

**Ultima Atualizacao:** 2026-02-11 (Python CLI v2.2.0)



