# ARCHITECTURE.md - Hefesto Skill Generator

> **Visao Arquitetural do Sistema**
> **Versao:** 2.0.0

---

## 1. Visao Geral

Hefesto Skill Generator e um spec-kit template-driven que gera Agent Skills para 7 CLIs de IA. Zero Python, zero dependencias - toda logica vive em Markdown templates que a IA interpreta.

```
                           USUARIO
                              |
                /hefesto.create  /hefesto.validate  /hefesto.extract
                              |
                              v
                    MARKDOWN TEMPLATES
                              |
            skill-template.md | quality-checklist.md | cli-compatibility.md
                              |
                              v
                        AI ENGINE
                  (interpreta templates)
                              |
                              v
                        HUMAN GATE
                 [approve] [edit] [reject]
                              |
                              v
                    MULTI-CLI OUTPUT
        .claude/  .gemini/  .codex/  .github/  .opencode/  .cursor/  .qwen/
```

---

## 2. Componentes

### 2.1. Command Layer

7 comandos disponibilizados para cada CLI detectado:

| Comando | Descricao | Human Gate |
|---------|-----------|------------|
| `/hefesto.create` | Criar skill de descricao natural | Sim |
| `/hefesto.validate` | Validar + corrigir skill contra spec | Sim (fix-auto) |
| `/hefesto.extract` | Extrair skill de codigo/docs | Sim |
| `/hefesto.init` | Bootstrap: detectar CLIs, verificar instalacao | Nao |
| `/hefesto.list` | Listar skills instaladas | Nao (read-only) |

### 2.2. Template System

Templates sao a fonte de verdade para geracao e validacao:

| Template | Responsabilidade |
|----------|-----------------|
| `skill-template.md` | Estrutura canonica de skills |
| `quality-checklist.md` | Auto-critica de 13 pontos (5 CRITICAL + 7 WARNING + 1 INFO) |
| `cli-compatibility.md` | Mapa de CLIs, diretorios e adaptacoes |

### 2.3. Human Gate

Controle de qualidade humano em todas as operacoes de escrita.

```
Skill gerada/corrigida
    |
    v
Preview + Auto-Critica (13 pontos)
    |
    v
[approve] [edit] [reject]
    |
    v
Persistencia em TODOS os CLIs detectados
```

### 2.4. Installer

Scripts de bootstrap que instalam Hefesto em qualquer projeto:

```
installer/
  install.sh        # Bash (Unix/macOS/Git Bash)
  install.ps1       # PowerShell (Windows)
  payload/
    hefesto/templates/    # -> .hefesto/templates/
    commands/{cli}/       # -> .<cli>/commands/ (ou prompts/)
```

O installer:
1. Detecta CLIs instalados (PATH + diretorios)
2. Cria `.hefesto/` com templates e versao
3. Copia comandos `hefesto.*` (7 comandos) para cada CLI detectado
4. Cria diretorios `skills/` para cada CLI

---

## 3. Fluxo de Dados

### /hefesto.create (6 fases)

```
Phase 1: Understanding    -> Parsear descricao, extrair conceitos
Phase 2: Research         -> Ler templates, skills exemplares, docs oficiais
Phase 3: Generation       -> Gerar SKILL.md seguindo agentskills.io spec
Phase 4: Auto-Critica     -> Self-review contra checklist de 13 pontos
Phase 5: Human Gate       -> Apresentar para [approve] [edit] [reject]
Phase 6: Persistence      -> Escrever em todos os CLIs detectados
```

### /hefesto.validate (com fix-auto)

```
1. Ler SKILL.md da skill alvo
2. Rodar checklist de 13 pontos
3. Classificar: PASS | PARTIAL (warnings) | FAIL (criticals)
4. Se FAIL ou PARTIAL:
   a. Diagnostico detalhado com sugestoes
   b. Perguntar: [fix-auto] [fix-manual] [skip]
   c. Se fix-auto: gerar versao corrigida + Human Gate
   d. Se aprovada: persistir em todos os CLIs
5. Se PASS: reportar sucesso
```

---

## 4. Estrutura de Dados

### Skill (Agent Skills Format)

```yaml
---
name: lowercase-hyphen (max 64 chars, regex: ^[a-z0-9]+(-[a-z0-9]+)*$)
description: |
  Action verb describing what the skill does.
  Use when: specific trigger condition.
---

# Skill Title

Brief introduction.

## How to <first capability>

Task-oriented instructions.

## How to <second capability>

More instructions.
```

**Frontmatter:** SOMENTE `name` + `description` (sem license, metadata, version)
**Body:** Secoes "How to [task]" (nao "Instructions > Step N")
**Limites:** < 500 linhas, < ~5000 tokens

### Checklist de Qualidade (13 pontos)

| Nivel | Qtd | Criterios |
|-------|-----|-----------|
| CRITICAL | 5 | Frontmatter, name format, description, body size, "How to" pattern |
| WARNING | 7 | Token economy, no tutorials, examples, progressive disclosure, anti-patterns, no body "When to Use", no README/CHANGELOG |
| INFO | 1 | Security (sem credenciais, tokens, PII) |

---

## 5. CLIs Suportados

| CLI | Skills Dir | Commands Dir | Formato | Variable Syntax |
|-----|-----------|-------------|---------|-----------------|
| Claude Code | `.claude/skills/` | `.claude/commands/` | `.md` | `$ARGUMENTS` |
| Gemini CLI | `.gemini/skills/` | `.gemini/commands/` | `.toml` | `{{args}}` |
| OpenAI Codex | `.codex/skills/` | `.codex/prompts/` | `.md` | `$ARGUMENTS` |
| VS Code/Copilot | `.github/skills/` | `.github/agents/` + `.github/prompts/` | `.md` | `$ARGUMENTS` |
| OpenCode | `.opencode/skills/` | `.opencode/command/` | `.md` | `$ARGUMENTS` |
| Cursor | `.cursor/skills/` | `.cursor/commands/` | `.md` | `$ARGUMENTS` |
| Qwen Code | `.qwen/skills/` | `.qwen/commands/` | `.md` | `{{args}}` |

---

## 6. Estrutura do Projeto

### Repositorio Hefesto

```
hefesto-skill-generator/
  README.md
  templates/                    # Templates fonte (fonte de verdade)
    skill-template.md
    quality-checklist.md
    cli-compatibility.md
  installer/                    # Pacote distribuivel
    install.sh
    install.ps1
    payload/
      hefesto/templates/        # Copia dos templates
      commands/{cli}/           # Comandos por CLI
  .claude/commands/hefesto.*    # Comandos Claude (canonicos)
  .gemini/commands/hefesto.*    # Comandos Gemini (TOML)
  .codex/prompts/hefesto.*     # Comandos Codex
  .github/agents/ + prompts/   # Comandos Copilot
  .opencode/command/hefesto.*  # Comandos OpenCode
  .cursor/commands/hefesto.*   # Comandos Cursor
  .qwen/commands/hefesto.*     # Comandos Qwen
  .agents/                      # Agent skills internos (skill-creator)
  .specify/                     # Spec-kit infrastructure
  .context/                     # AI context hub (regras, padroes, exemplos)
  knowledge/                    # Best practices e research references
  specs/                        # Feature specifications (spec-kit artifacts)
  docs/                         # Documentacao, ADRs, guias
  .github/workflows/release.yml # CI/CD build + release
```

### Projeto do Usuario (apos install)

```
meu-projeto/
  .hefesto/
    version                    # "2.0.0"
    templates/
      skill-template.md
      quality-checklist.md
      cli-compatibility.md
  .claude/
    commands/hefesto.*.md      # 7 comandos (create, update, extract, agent, validate, init, list)
    skills/                    # Skills geradas
  .gemini/
    commands/hefesto.*.toml    # 7 comandos (create, update, extract, agent, validate, init, list)
    skills/
  ...                          # Idem para cada CLI detectado
```

---

## 7. Decisoes Arquiteturais

| Decisao | Justificativa |
|---------|---------------|
| Template-driven (zero Python) | Zero dependencias, portabilidade universal |
| Agent Skills Standard | Padrao aberto agentskills.io |
| Human Gate obrigatorio | Controle de qualidade, usuario no controle |
| Deteccao automatica CLIs | UX fluida, menos perguntas |
| `.hefesto/` como namespace | Isolamento do Hefesto no projeto do usuario |
| Installer scripts | Bootstrap portatil (bash + PowerShell) |
| Frontmatter minimo (name + description) | Token economy, sem ruido |

Ver `docs/decisions/` para ADRs detalhados.

---

## 8. Extensibilidade

### Adicionar Novo CLI

1. Adicionar regras em `templates/cli-compatibility.md`
2. Criar comandos no formato do CLI (7 comandos: create, update, extract, agent, validate, init, list)
3. Atualizar `installer/` (scripts + payload)

### Adicionar Novo Comando

1. Criar `hefesto.{cmd}.md` para Claude (canonico)
2. Propagar para os 6 CLIs restantes
3. Atualizar `installer/payload/commands/`

---

**Ultima Atualizacao:** 2026-02-07 (v2.0.0)
