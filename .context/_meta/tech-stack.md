# Tech Stack - Hefesto Skill Generator

> **Tier:** T2 - Informativo
> **Versao:** 2.0.0

---

## 1. Arquitetura

### Tipo de Sistema

**Spec-Kit Template-Driven** - Zero Python, zero dependencias. Toda logica vive em Markdown templates que a IA interpreta diretamente.

### Componentes

```
MARKDOWN TEMPLATES  ->  AI AGENT  ->  SKILLS (output)
                         ^
                    skill-template.md
                    quality-checklist.md
                    cli-compatibility.md
```

---

## 2. Stack Tecnica

### Core

| Componente | Tecnologia | Justificativa |
|------------|------------|---------------|
| Formato | Markdown + YAML frontmatter | Padrao Agent Skills |
| Templates | 3 Markdown (skill, checklist, CLI map) | Fonte de verdade |
| Installer | Bash + PowerShell | Cross-platform bootstrap |
| CI/CD | GitHub Actions | Build + release automatizado |
| Linguagem | Markdown (template-driven) | Zero dependencies |

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
  templates/                    # Templates fonte
    skill-template.md
    quality-checklist.md
    cli-compatibility.md
  installer/                    # Bootstrap distribuivel
    install.sh / install.ps1
    payload/
      hefesto/templates/
      commands/{cli}/
  .<cli>/commands/hefesto.*     # 5 comandos por CLI (7 CLIs)
  .<cli>/skills/                # Skills de demonstracao
  .github/workflows/release.yml
  docs/                         # Documentacao
  .context/                     # Contexto para IAs
```

### Projeto do Usuario (apos install)

```
meu-projeto/
  .hefesto/
    version                    # "2.0.0"
    templates/                 # 3 templates
  .<cli>/
    commands/hefesto.*         # 5 comandos
    skills/                    # Skills geradas
```

---

## 5. Dependencias

### Runtime

| Dependencia | Tipo | Obrigatorio |
|-------------|------|-------------|
| CLI de IA (qualquer 1 dos 7) | Runtime | Sim |
| Filesystem | Sistema | Sim |
| Git | Sistema | Nao (recomendado) |

### Instalacao

| Dependencia | Tipo | Obrigatorio |
|-------------|------|-------------|
| Bash 3.2+ (Unix) ou PowerShell 5.1+ (Windows) | Installer | Sim |

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

**Ultima Atualizacao:** 2026-02-07
