# MEMORY.md - AI Persistent State

> **Projeto:** Hefesto Skill Generator
> **Versao:** 1.2.0

---

## Last Updated

2026-02-04

---

## Current State

| Campo | Valor |
|-------|-------|
| **Projeto** | Hefesto Skill Generator |
| **Versao** | 1.2.0 |
| **Status** | Em Desenvolvimento |
| **Fase** | Planning Completo + Research + Metadata JIT |

---

## Project Overview

Sistema de geracao de Agent Skills para multiplos CLIs de IA, seguindo o padrao aberto agentskills.io. Fundamentado em literatura academica com estrutura de metadados JIT.

---

## Key Decisions (ADRs)

| ADR | Titulo | Status | Impacto |
|-----|--------|--------|---------|
| ADR-001 | Escolha do Agent Skills Standard | Aceito | Base do projeto |
| ADR-002 | Integracao de Pesquisa Academica | Aceito | +T0-HEFESTO-11, +MCP |
| ADR-003 | Frontmatter Leve com Metadados JIT | Aceito | Estrutura 2 niveis |

---

## Estrutura de Metadados (ADR-003)

### Nivel 1: Frontmatter SKILL.md (~100 tokens)

```yaml
---
name: skill-name           # Obrigatorio
description: |             # Obrigatorio
  Descricao da skill.
  Use quando: [gatilhos]
license: MIT               # Obrigatorio
metadata: ./metadata.yaml  # Opcional - ponteiro JIT
---
```

### Nivel 2: metadata.yaml (JIT)

```yaml
author: "Nome <email>"
version: "1.0.0"
created: 2026-02-04
updated: 2026-02-04
category: development
tags: [tag1, tag2]
platforms: [claude, gemini]
dependencies: []
example_prompt: "..."
test_cases: [...]
sources: [...]
```

### Estrutura de Skill

```
skill-name/
├── SKILL.md           # Core + frontmatter leve
├── metadata.yaml      # Metadados expandidos (JIT)
├── scripts/           # Recursos executaveis (JIT)
├── references/        # Documentacao detalhada (JIT)
└── assets/            # Recursos estaticos (JIT)
```

---

## Completed Actions

### 2026-02-04 (Sessao 1)

- [x] Criado README.md com visao geral do projeto
- [x] Criado CONSTITUTION.md com regras T0 (10 regras)
- [x] Criada estrutura .context/ completa
- [x] Criado AGENTS.md (bootstrap)
- [x] Criado MEMORY.md

### 2026-02-04 (Sessao 2)

- [x] Criada estrutura docs/cards/ e docs/plan/
- [x] Criados todos os CARDs de implementacao (7)
- [x] Criado PLAN-001-hefesto-v1.md
- [x] Atualizado docs/README.md

### 2026-02-04 (Sessao 3) - Integracao de Pesquisa

- [x] Analisada pesquisa `skill-generator-automatizado.md`
- [x] Criado ADR-002: Integracao de Pesquisa Academica
- [x] Atualizado CONSTITUTION.md v1.1.0 (+T0-HEFESTO-11)
- [x] Atualizado CARD-002 (+MCP, +metadados)
- [x] Atualizado CARD-006 (+research/, +security)
- [x] Criada estrutura knowledge/research/
- [x] Movida pesquisa para knowledge/research/

### 2026-02-04 (Sessao 4) - Metadados JIT

- [x] Criado ADR-003: Frontmatter Leve com Metadados JIT
- [x] Definida estrutura de 2 niveis para metadados
- [x] Atualizado CARD-002 com nova estrutura
- [x] Atualizado MEMORY.md

---

## Next Steps

### Imediato (Proxima Sessao)

- [ ] Iniciar CARD-001: Foundation
  - [ ] Implementar detector de CLIs
  - [ ] Criar estrutura de diretorios
  - [ ] Registrar comandos

### Futuro (Por Ordem)

1. CARD-002: Templates System (inclui MCP + metadata.yaml template)
2. CARD-003: Commands /hefesto.*
3. CARD-004: Multi-CLI Generator
4. CARD-005: Human Gate + Wizard
5. CARD-006: Knowledge Base
6. CARD-007: Examples
7. Validacao Final e Release v1.0.0

---

## Skills Criadas

Nenhuma skill criada ainda.

---

## CLIs Detectados

Deteccao pendente (executar apos implementacao CARD-001).

---

## Metricas

| Metrica | Valor |
|---------|-------|
| **Total de CARDs** | 7 |
| **Total de Sub-Tasks** | 62 |
| **Estimativa Total** | 76h |
| **Tasks Concluidas** | 0 |
| **Progresso** | 0% |
| **Regras T0** | 11 |
| **ADRs** | 3 |

---

## T0 Rules Summary

| ID | Regra | Fonte |
|----|-------|-------|
| T0-HEFESTO-01 | Agent Skills Standard | Original |
| T0-HEFESTO-02 | Human Gate Obrigatorio | Original |
| T0-HEFESTO-03 | Progressive Disclosure | Original |
| T0-HEFESTO-04 | Multi-CLI Deteccao | Original |
| T0-HEFESTO-05 | Armazenamento Local | Original |
| T0-HEFESTO-06 | Validacao Spec | Original |
| T0-HEFESTO-07 | Nomenclatura Padrao | Original |
| T0-HEFESTO-08 | Idempotencia | Original |
| T0-HEFESTO-09 | Compatibilidade CLI | Original |
| T0-HEFESTO-10 | Citacao de Fontes | Original |
| T0-HEFESTO-11 | Seguranca por Padrao | ADR-002 |

---

## Notes

- Projeto segue padrao Agent Skills (agentskills.io)
- Human Gate obrigatorio para todas operacoes de escrita
- Skills armazenadas no projeto por padrao
- Deteccao automatica de CLIs
- 7 CLIs suportados: Claude, Gemini, Codex, Copilot, OpenCode, Cursor, Qwen
- **ADR-002:** Suporte a MCP Protocol + Seguranca T0
- **ADR-003:** Frontmatter leve (~100 tokens) + metadata.yaml JIT

---

## Session Log

| Data | Sessao | Acoes |
|------|--------|-------|
| 2026-02-04 | 1 | Planejamento e estrutura base |
| 2026-02-04 | 2 | CARDs (7) e PLAN-001 |
| 2026-02-04 | 3 | Integracao pesquisa (ADR-002) |
| 2026-02-04 | 4 | Metadados JIT (ADR-003) |

---

**MEMORY.md** | Hefesto Skill Generator | Atualizado: 2026-02-04
