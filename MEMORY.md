# MEMORY.md - AI Persistent State

> **Projeto:** Hefesto Skill Generator
> **Versao:** 1.4.0

---

## Last Updated

2026-02-05

---

## Current State

| Campo | Valor |
|-------|-------|
| **Projeto** | Hefesto Skill Generator |
| **Versao** | 1.3.0 |
| **Status** | Em Desenvolvimento |
| **Fase** | Feature 004 Complete - Multi-CLI Automatic Parallel Generation |

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

### 2026-02-04 (Sessao 5-7) - Feature 003: Hefesto Commands

- [x] Gerado spec.md com 4 user stories e 11 functional requirements
- [x] Gerado plan.md com technical context e constitution check
- [x] Gerado research.md com command structure patterns
- [x] Gerado data-model.md com 6 entities (Command, Wizard, Human Gate, etc.)
- [x] Gerado quickstart.md com developer guide
- [x] Gerados 7 contracts em contracts/ directory
- [x] Gerado tasks.md com 74 tarefas organizadas por user story
- [x] Executado /speckit.analyze - 0 critical issues
- [x] Implementados 7 novos comandos em commands/:
  - hefesto.create.md (545 linhas)
  - hefesto.extract.md (599 linhas)
  - hefesto.validate.md (537 linhas)
  - hefesto.adapt.md (592 linhas)
  - hefesto.sync.md (595 linhas)
  - hefesto.show.md (509 linhas)
  - hefesto.delete.md (561 linhas)
- [x] Atualizado hefesto.help.md com todos os 9 comandos
- [x] Atualizado MEMORY.md v1.3.0

---

## Next Steps

### Imediato (Proxima Sessao)

- [x] Feature 004 implementada e testada (9/9 testes ✅)
- [ ] Atualizar README.md com Feature 004
- [ ] Atualizar CONSTITUTION.md (validar T0-HEFESTO-04 e T0-HEFESTO-09)
- [ ] Atualizar AGENTS.md com exemplos de uso
- [ ] Marcar CARDs 001-004 como finalizados
- [ ] Atualizar docs/README.md com Feature 004 section

### Futuro (Por Ordem)

1. ✅ CARD-001: Foundation (COMPLETO)
2. ✅ CARD-002: Templates System (COMPLETO - inclui MCP + metadata.yaml)
3. ✅ CARD-003: Commands /hefesto.* (COMPLETO - 9 comandos)
4. ✅ CARD-004: Multi-CLI Generator (COMPLETO - deteccao + adaptacao paralela + 9 testes)
5. CARD-005: Human Gate + Wizard (patterns definidos, testar execucao)
6. CARD-006: Knowledge Base (adicionar command examples)
7. CARD-007: Examples (criar skills de demonstracao)
8. CARD-008: Shared Skill Pool (.hefesto/skills/ central)
9. Validacao Final e Release v1.4.0

---

## Skills Criadas

### prompt-engineering-basics

| Campo | Valor |
|-------|-------|
| **Nome** | prompt-engineering-basics |
| **Versão** | 1.0.0 |
| **Criada** | 2026-02-05 (Sessão 11) |
| **Categoria** | ai-development |
| **Target CLIs** | OpenCode, Claude (2 CLIs) |
| **Descrição** | Fundamentos de prompt engineering para modelos generativos (ChatGPT, Claude, Gemini) com técnicas core e avançadas |
| **Estrutura** | Progressive Disclosure (SKILL.md 335 linhas + 6 references) |
| **Tamanho** | ~335 linhas (core) + ~2870 linhas (references) |
| **Técnicas Core** | Zero-shot, Few-shot, Chain-of-Thought, Role Prompting, Instruction Prompting |
| **Técnicas Avançadas** | Self-Criticism, Decomposition (Least-to-Most), Ensembling (Self-Consistency), Thought Generation (Tree of Thoughts) |
| **Tags** | prompt-engineering, ai, llm, chatgpt, claude, gemini, best-practices, fundamentals, self-criticism, decomposition, ensembling, thought-generation, chain-of-thought, few-shot |
| **Fontes** | 9 (Learn Prompting x6, OpenAI Guide, Anthropic Guide, Tree of Thoughts paper arXiv) |
| **References** | few-shot-prompting, chain-of-thought, advanced-techniques (novo), prompt-templates, model-specific-tips, evaluation-testing |
| **Adaptações** | Target reduzido de 6 para 2 CLIs conforme solicitação do usuário |
| **Status** | ✅ Validada contra T0 (335 linhas < 500), aprovada pelo Human Gate com edições, sincronizada para 2 CLIs |

### coala-framework

| Campo | Valor |
|-------|-------|
| **Nome** | coala-framework |
| **Versão** | 1.0.0 |
| **Criada** | 2026-02-05 |
| **Categoria** | ai-development |
| **Target CLIs** | Claude, Gemini, Codex, OpenCode, Cursor, Qwen (6 CLIs) |
| **Descrição** | Framework CoALA (Cognitive Architectures for Language Agents) com memórias especializadas e ciclo de decisão |
| **Estrutura** | Progressive Disclosure (SKILL.md 445 linhas + 4 references) |
| **Tamanho** | ~445 linhas (core) + ~2313 linhas (references) |
| **Tags** | coala, cognitive-architecture, language-agents, memory-systems, decision-making, ai-agents, llm-agents, episodic-memory, semantic-memory, procedural-memory, working-memory, long-term-memory, agent-framework, reasoning, planning |
| **Fontes** | 4 (CoALA paper arXiv, Soar docs, ACT-R docs, Awesome Language Agents) |
| **References** | memory-implementation, action-space-patterns, decision-cycle-advanced, integration-examples |
| **Status** | ✅ Validada contra T0+T1, aprovada pelo Human Gate, sincronizada para 6 CLIs |

### markdown-fundamentals

| Campo | Valor |
|-------|-------|
| **Nome** | markdown-fundamentals |
| **Versão** | 1.0.0 |
| **Criada** | 2026-02-05 (Sessão 9) |
| **Categoria** | documentation |
| **Target CLIs** | Claude, Gemini, Codex, OpenCode, Cursor, Qwen (6 CLIs) |
| **Descrição** | Fundamentos Markdown (CommonMark, GFM, compatibilidade entre plataformas) |
| **Estrutura** | Progressive Disclosure (SKILL.md 268 linhas + 6 references) |
| **Tamanho** | ~268 linhas (core) + ~2392 linhas (references) |
| **Tags** | markdown, documentation, commonmark, gfm, writing, best-practices, fundamentals, compatibility |
| **Fontes** | 6 (CommonMark spec, GFM spec, GitHub docs, GitLab docs, Mermaid docs, W3C WCAG) |
| **References** | headings-structure, links-images, code-blocks, tables-lists, advanced-features, compatibility |
| **Status** | ✅ Validada contra T0+T1, aprovada pelo Human Gate, sincronizada para 6 CLIs |

### kotlin-fundamentals

| Campo | Valor |
|-------|-------|
| **Nome** | kotlin-fundamentals |
| **Versão** | 1.0.0 |
| **Criada** | 2026-02-04 (Sessão 9) |
| **Categoria** | development |
| **Target CLIs** | Claude, Gemini, Codex, OpenCode, Cursor, Qwen (6 CLIs) |
| **Descrição** | Fundamentos Kotlin (tipos seguros, funcional, coroutines básicas, Kotlin 1.x–2.x) |
| **Estrutura** | Progressive Disclosure (SKILL.md 290 linhas + 7 references) |
| **Tamanho** | ~290 linhas (core) + ~2500 linhas (references) |
| **Kotlin Versions** | 1.0–2.x (genérico, sem framework específico) |
| **Tags** | kotlin, programming, oop, clean-code, best-practices, fundamentals, coroutines, functional |
| **Fontes** | 5 (kotlinlang.org x3, Kotlin in Action, Effective Kotlin) |
| **References** | types, oop, functions, collections, coroutines, error-handling, kotlin-versions (K2) |
| **Status** | ✅ Validada contra T0, aprovada pelo Human Gate, sincronizada para 6 CLIs |

### fundamentos-do-kotlin-1xx-e-2xx

| Campo | Valor |
|-------|-------|
| **Nome** | fundamentos-do-kotlin-1xx-e-2xx |
| **Versão** | 1.0.0 |
| **Criada** | 2026-02-04 |
| **Categoria** | development |
| **Target CLIs** | qwen (1 CLI) |
| **Status** | ⚠️ Registrada no MEMORY mas NÃO encontrada no disco (.qwen/skills/) — substituída por kotlin-fundamentals |

### java-fundamentals

| Campo | Valor |
|-------|-------|
| **Nome** | java-fundamentals |
| **Versão** | 1.0.0 |
| **Criada** | 2026-02-04 (Sessão 8) |
| **Categoria** | development |
| **Target CLIs** | OpenCode, Claude, Gemini, Codex, Cursor, Qwen (6 CLIs) |
| **Compatível** | Claude, Gemini, Codex, Copilot, OpenCode, Cursor, Qwen |
| **Descrição** | Fundamentos Java (POO, clean code, recursos Java 6-25) |
| **Estrutura** | Progressive Disclosure (SKILL.md + 8 references/*.md) |
| **Tamanho** | 480 linhas (core) + 3200 linhas (references) |
| **Java Versions** | 6-25 (generic, sem frameworks) |
| **Tags** | java, oop, clean-code, best-practices, design-patterns |
| **Fontes** | 5 (Oracle, Effective Java, JLS, Clean Code, GoF) |
| **Status** | ✅ Validada contra T0, persistida, sincronizada |
| **Sincronizada** | 2026-02-04 (Sessão 8) para 6 CLIs |

**Arquivos criados:**
- `.opencode/skills/java-fundamentals/SKILL.md` (425 linhas)
- `.claude/skills/java-fundamentals/SKILL.md` (425 linhas)
- `.gemini/skills/java-fundamentals/SKILL.md` (425 linhas)
- `.codex/skills/java-fundamentals/SKILL.md` (425 linhas)
- `.cursor/skills/java-fundamentals/SKILL.md` (425 linhas)
- `.qwen/skills/java-fundamentals/SKILL.md` (425 linhas)
- `.opencode/skills/java-fundamentals/metadata.yaml` (completo)
- `.opencode/skills/java-fundamentals/references/generics.md` (450 linhas)
- `.opencode/skills/java-fundamentals/references/concurrency.md` (400 linhas)
- `.opencode/skills/java-fundamentals/references/memory.md` (380 linhas)
- `.opencode/skills/java-fundamentals/references/design-patterns.md` (420 linhas)
- `.opencode/skills/java-fundamentals/references/io-nio.md` (380 linhas)
- `.opencode/skills/java-fundamentals/references/serialization.md` (350 linhas)
- `.opencode/skills/java-fundamentals/references/reflection.md` (400 linhas)
- `.opencode/skills/java-fundamentals/references/functional.md` (420 linhas)

---

## CLIs Detectados

| CLI | Método | Status | Versão | Skills Dir | Skills |
|-----|--------|--------|--------|------------|--------|
| **Claude Code** | PATH + Config | ✅ active | 2.1.31 | .claude/skills/ | java-fundamentals, coala-framework, prompt-engineering-basics |
| **Gemini CLI** | PATH + Config | ✅ active | 0.27.0 | .gemini/skills/ | java-fundamentals, coala-framework |
| **Codex** | PATH + Config | ✅ active | (npm) | .codex/skills/ | java-fundamentals, coala-framework |
| **OpenCode** | PATH + Config | ✅ active | 1.1.48 | .opencode/skills/ | java-fundamentals, coala-framework, prompt-engineering-basics |
| **Cursor** | PATH + Config | ✅ active | 2.4.27 | .cursor/skills/ | java-fundamentals, coala-framework |
| **Qwen Code** | PATH + Config | ✅ active | 0.9.0 | .qwen/skills/ | java-fundamentals, coala-framework |
| **Copilot** | config_dir only | ⚠️ warning_no_path | null | .copilot/skills/ | (vazio) |

**Nota:** `code` no PATH aponta para binário do Cursor, não VS Code. Copilot não detectável sem ~/.vscode ou extensão instalada.

**Última detecção**: 2026-02-04 (hefesto.init re-scan)
**Total AI CLIs**: 7 (6 active, 1 warning_no_path)

---

## Metricas

| Metrica | Valor |
|---------|-------|
| **Total de CARDs** | 8 |
| **CARDs Completos** | 4 (Foundation, Templates, Commands, Multi-CLI) |
| **Total de Sub-Tasks** | 69+ (Feature 004: +61 tasks) |
| **Estimativa Total** | 86h+ |
| **Tasks Concluidas Feature 003** | 61/74 (82%) |
| **Tasks Concluidas Feature 004** | 60/61 (98.4%) |
| **Comandos Implementados** | 9/9 (100%) |
| **Helpers Implementados** | 5/5 (100%) - Feature 004 |
| **Progresso Geral** | ~57% (4/7 CARDs) |
| **Regras T0** | 11 |
| **ADRs** | 3 |
| **Skills Criadas** | 5 (java-fundamentals, kotlin-fundamentals, markdown-fundamentals, coala-framework, prompt-engineering-basics) |
| **Skills Sincronizadas** | 2-6 CLIs por skill (média: 5 CLIs) |

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
| 2026-02-04 | 5-7 | Feature 003: Comandos Hefesto (spec, implementação) |
| 2026-02-04 | 8 | /hefesto.create: Primeira skill java-fundamentals ✅ |
| 2026-02-04 | 8 | /hefesto.detect: 5 novos CLIs detectados (Claude, Gemini, Codex, Cursor, Qwen) |
| 2026-02-04 | 8 | /hefesto.sync: java-fundamentals sincronizada para 6 CLIs ✅ |
| 2026-02-04 | 9 | /hefesto.init: re-scan CLIs, 7 detectados (6 active + Copilot warning), inconsistência kotlin skill flagged |
| 2026-02-04 | 9 | /hefesto.create: kotlin-fundamentals criada e sincronizada para 6 CLIs ✅ (7 references incl. K2) |
| 2026-02-05 | 9 | /hefesto.create: markdown-fundamentals criada e sincronizada para 6 CLIs ✅ (6 references, cat. documentation) |
| 2026-02-05 | 9 | Análise arquitetural: "thin SKILL.md cross-CLI" descartado → CARD-008 criado (Shared Skill Pool .hefesto/skills/) |
| 2026-02-05 | 10 | **Feature 004: Multi-CLI Automatic Parallel Generation** ✅ COMPLETA |
| 2026-02-05 | 10 | Criados 5 helpers (cli-detector, cli-adapter, parallel-generator, rollback-handler, multi-cli-integration) |
| 2026-02-05 | 10 | Criados 2 templates (detection-report, generation-report) com 210-211 linhas |
| 2026-02-05 | 10 | Executados 9 testes manuais - 100% aprovação (TESTE-01 a TESTE-09) |
| 2026-02-05 | 10 | Gerados relatórios: test-report (400L), executive-summary (300L), final-checklist (350L), INDEX |
| 2026-02-05 | 10 | Feature 004 Status: 9/9 testes ✅, 10/10 critérios obrigatórios ✅, 3/3 critérios desejáveis ✅, 8/8 T0 rules ✅ |
| 2026-02-05 | 10 | /hefesto.create: coala-framework criada e sincronizada para 6 CLIs ✅ (framework CoALA, 4 references, cat. ai-development) |

---

**MEMORY.md** | Hefesto Skill Generator | Atualizado: 2026-02-04

---

## Reports Generated

### Session 008 Reports (2026-02-04)

| Report | Description | Size | Status |
|--------|-------------|------|--------|
| **session-008-execution-report.md** | Detailed session execution analysis | 269 lines | ✅ Complete |
| **session-008-new-commands-proposal.md** | Proposed new commands (distribute, extend, edit) | ~300 lines | ✅ Complete |

**Location**: `docs/reports/`

**Key Findings**:
- ✅ Successfully created and distributed java-fundamentals skill
- ❌ Identified `/hefesto.sync` semantic confusion (used incorrectly for distribution)
- ❌ Missing `/hefesto.extend` command for incremental skill updates
- ❌ Missing `/hefesto.distribute` command for multi-CLI distribution
- 📋 Proposed 3 new CARDs (008, 009, 010) with 36h total effort

**Next Sprint**: CARD-008 (Shared Skill Pool — .hefesto/skills/ + sync adaptado)

### Session 009 Reports (2026-02-05)

| Report | Description | Size | Status |
|--------|-------------|------|--------|
| **session-009-execution-report.md** | Full session analysis: 2 skills criadas, batch validation, análise arquitetural, CARD-008 | ~250 lines | ✅ Complete |

**Location**: `docs/reports/`

**Key Findings**:
- ✅ kotlin-fundamentals e markdown-fundamentals criadas e sincronizadas (6 CLIs cada)
- ✅ Batch validation: 3/3 skills passaram T0+T1+Structure
- ✅ Análise arquitetural: "thin cross-CLI" descartado → CARD-008 aprovado
- ⚠️ Human Gate bypassado 1x pelo sub-agent (kotlin) — padrão corrigido no seguinte
- ⚠️ Skill "fantasma" no MEMORY detectada e flagged durante init
- 📋 4 recomendações de next steps documentadas no report

