# ARCHITECTURE.md - Hefesto Skill Generator

> **Visao Arquitetural do Sistema**
> **Versao:** 1.0.0

---

## 1. Visao Geral

Hefesto Skill Generator e um sistema prompt-based que gera Agent Skills padronizadas para multiplos CLIs de IA.

```
┌─────────────────────────────────────────────────────────────────────┐
│                              USUARIO                                 │
│                                                                      │
│    /hefesto.create    /hefesto.extract    /hefesto.validate         │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         HEFESTO ENGINE                               │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │  Template   │  │   Extract   │  │  Validate   │  │   Adapt    │ │
│  │  Processor  │  │   Analyzer  │  │   Engine    │  │   Engine   │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │
│                                                                      │
│                        ┌─────────────┐                               │
│                        │ Human Gate  │                               │
│                        └─────────────┘                               │
│                                                                      │
│                   ┌───────────────────────┐                          │
│                   │  Multi-CLI Generator  │                          │
│                   └───────────────────────┘                          │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         OUTPUT (Skills)                              │
│                                                                      │
│   .claude/skills/    .gemini/skills/    .codex/skills/    ...       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Componentes

### 2.1. Command Layer

Recebe comandos do usuario e roteia para processadores apropriados.

**Comandos:**
- `/hefesto.create` → Template Processor
- `/hefesto.extract` → Extract Analyzer
- `/hefesto.validate` → Validate Engine
- `/hefesto.adapt` → Adapt Engine
- `/hefesto.sync` → Multi-CLI Generator
- `/hefesto.list` → Output Layer

### 2.2. Processing Engine

#### Template Processor

Gera skills a partir de descricao natural.

```
Input: Descricao em linguagem natural
Output: SKILL.md preenchido
```

#### Extract Analyzer

Extrai skills a partir de codigo/documentacao existente.

```
Input: Arquivo(s) de codigo ou docs
Output: SKILL.md derivado dos padroes encontrados
```

#### Validate Engine

Valida skills contra Agent Skills spec.

```
Input: SKILL.md existente
Output: Relatorio de validacao
```

#### Adapt Engine

Adapta skills para CLIs especificos.

```
Input: SKILL.md + CLI alvo
Output: SKILL.md adaptado
```

### 2.3. Human Gate

Controle de qualidade humano. Todas as operacoes de escrita passam por aqui.

```
Input: Skill gerada/adaptada
Output: Decisao do usuario [approve|expand|edit|reject]
```

### 2.4. Multi-CLI Generator

Detecta CLIs instalados e gera skills para todos.

```
Input: Skill aprovada
Output: Skills em diretorios de cada CLI
```

---

## 3. Fluxo de Dados

### /hefesto.create

```
Usuario → Descricao
    ↓
Template Processor → SKILL.md (draft)
    ↓
Validate Engine → Validacao
    ↓
Human Gate → [approve|expand|edit|reject]
    ↓
Multi-CLI Generator → .claude/, .gemini/, ...
    ↓
Usuario ← Resultado
```

### /hefesto.extract

```
Usuario → @arquivo
    ↓
Extract Analyzer → Padroes identificados
    ↓
Template Processor → SKILL.md (draft)
    ↓
[Continua como /hefesto.create]
```

---

## 4. Estrutura de Dados

### Skill (Agent Skills Format)

```yaml
---
name: string (max 64, lowercase, hyphens)
description: string (max 1024, nao vazio)
license: string (opcional)
compatibility: string (opcional)
metadata:
  author: string
  version: string
  category: string
  tags: [string]
---

# Titulo

## When to Use
...

## Instructions
...

## References
...
```

### Validation Result

```yaml
valid: boolean
errors: [string]  # Bloqueantes
warnings: [string]  # Informativos
checklist:
  structure: boolean
  spec: boolean
  quality: boolean
```

---

## 5. CLIs Suportados

| CLI | Diretorio | Adapter |
|-----|-----------|---------|
| Claude Code | `.claude/skills/` | Nativo |
| Gemini CLI | `.gemini/skills/` | $ARGUMENTS → {{args}} |
| OpenAI Codex | `.codex/skills/` | Nativo |
| VS Code/Copilot | `.github/skills/` | Nativo |
| OpenCode | `.opencode/skills/` | Nativo |
| Cursor | `.cursor/skills/` | Nativo |
| Qwen Code | `.qwen/skills/` | $ARGUMENTS → {{args}} |

---

## 6. Decisoes Arquiteturais

| Decisao | Justificativa |
|---------|---------------|
| Agent Skills Standard | Padrao aberto, suportado por multiplos CLIs |
| Human Gate obrigatorio | Controle de qualidade, usuario no controle |
| Deteccao automatica CLIs | UX fluida, menos perguntas |
| Projeto-first storage | Skills versionadas com codigo |
| Progressive Disclosure | Otimizacao de contexto |

Ver `docs/decisions/` para ADRs detalhados.

---

## 7. Extensibilidade

### Adicionar Novo CLI

1. Criar adapter em `templates/adapters/{cli}.adapter.md`
2. Definir transformacoes
3. Adicionar deteccao no Multi-CLI Generator

### Adicionar Novo Comando

1. Criar definicao em `commands/hefesto.{cmd}.md`
2. Definir fluxo
3. Implementar Human Gate se necessario

---

**Ultima Atualizacao:** 2026-02-04
