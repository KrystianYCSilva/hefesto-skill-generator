# PLAN-001: Hefesto Skill Generator v1.0

**Versao Alvo:** v1.0.0
**Status:** Em Planejamento
**Data Criacao:** 2026-02-04

---

## Objetivo

Implementar a versao 1.0 do Hefesto Skill Generator, um sistema completo para geracao de Agent Skills padronizadas para multiplos CLIs de IA (Claude Code, Gemini CLI, Codex, Copilot, OpenCode, Cursor, Qwen Code).

---

## Visao Geral

```
                    ┌─────────────────────────────────────────┐
                    │         Hefesto Skill Generator         │
                    │              v1.0.0                      │
                    └─────────────────────────────────────────┘
                                      │
           ┌──────────────────────────┼──────────────────────────┐
           │                          │                          │
    ┌──────▼──────┐           ┌───────▼───────┐          ┌───────▼───────┐
    │  Commands   │           │   Templates   │          │  Knowledge    │
    │  /hefesto.* │           │   + Adapters  │          │     Base      │
    └──────┬──────┘           └───────┬───────┘          └───────┬───────┘
           │                          │                          │
           └──────────────────────────┼──────────────────────────┘
                                      │
                              ┌───────▼───────┐
                              │  Multi-CLI    │
                              │  Generator    │
                              └───────┬───────┘
                                      │
                              ┌───────▼───────┐
                              │  Human Gate   │
                              │  + Wizard     │
                              └───────┬───────┘
                                      │
           ┌──────────────────────────┼──────────────────────────┐
           │           │              │              │           │
    ┌──────▼──────┐ ┌──▼───┐ ┌───────▼───────┐ ┌───▼────┐ ┌─────▼────┐
    │   Claude    │ │Gemini│ │    Codex      │ │Copilot │ │  Outros  │
    │    Code     │ │ CLI  │ │               │ │        │ │          │
    └─────────────┘ └──────┘ └───────────────┘ └────────┘ └──────────┘
```

---

## Checklist

### Fase 1: Foundation (CARD-001)
**Estimativa:** 4h | **Dependencias:** Nenhuma

- [ ] 1.1 Implementar detector de CLIs (PATH)
- [ ] 1.2 Implementar detector de config dirs
- [ ] 1.3 Criar estrutura de diretorios por CLI
- [ ] 1.4 Copiar CONSTITUTION.md para projeto
- [ ] 1.5 Inicializar MEMORY.md
- [ ] 1.6 Registrar comandos /hefesto.*

**Entregavel:** Estrutura base funcionando, CLIs detectados

---

### Fase 2: Templates (CARD-002)
**Estimativa:** 8h | **Dependencias:** Fase 1

- [ ] 2.1 Criar skill-template.md base
- [ ] 2.2 Implementar sistema de variaveis
- [ ] 2.3 Criar adapter Claude Code
- [ ] 2.4 Criar adapter Gemini CLI
- [ ] 2.5 Criar adapter OpenAI Codex
- [ ] 2.6 Criar adapter VS Code/Copilot
- [ ] 2.7 Criar adapter OpenCode
- [ ] 2.8 Criar adapter Cursor
- [ ] 2.9 Criar adapter Qwen Code
- [ ] 2.10 Implementar validador de templates

**Entregavel:** Templates gerando skills validas para todos CLIs

---

### Fase 3: Commands (CARD-003)
**Estimativa:** 12h | **Dependencias:** Fase 2

- [ ] 3.1 Implementar /hefesto.create
- [ ] 3.2 Implementar /hefesto.extract
- [ ] 3.3 Implementar /hefesto.validate
- [ ] 3.4 Implementar /hefesto.adapt
- [ ] 3.5 Implementar /hefesto.sync
- [ ] 3.6 Implementar /hefesto.list
- [ ] 3.7 Implementar /hefesto.show
- [ ] 3.8 Implementar /hefesto.delete
- [ ] 3.9 Implementar /hefesto.help
- [ ] 3.10 Integrar Human Gate

**Entregavel:** Todos os comandos funcionais

---

### Fase 4: Multi-CLI (CARD-004)
**Estimativa:** 8h | **Dependencias:** Fase 2

- [ ] 4.1 Unificar deteccao PATH + config
- [ ] 4.2 Implementar geracao paralela
- [ ] 4.3 Implementar argumento --cli
- [ ] 4.4 Implementar report de deteccao
- [ ] 4.5 Implementar fallback interativo
- [ ] 4.6 Testes de integracao por CLI

**Entregavel:** Geracao simultanea para multiplos CLIs

---

### Fase 5: Human Gate (CARD-005)
**Estimativa:** 10h | **Dependencias:** Fase 3

- [ ] 5.1 Implementar geracao em memoria
- [ ] 5.2 Implementar validacao pre-persistencia
- [ ] 5.3 Implementar formatador de preview
- [ ] 5.4 Implementar handlers (approve/expand/edit/reject)
- [ ] 5.5 Implementar wizard /hefesto.create
- [ ] 5.6 Implementar wizard /hefesto.extract
- [ ] 5.7 Implementar tratamento skill existente
- [ ] 5.8 Implementar timeout

**Entregavel:** Controle humano completo

---

### Fase 6: Knowledge Base (CARD-006)
**Estimativa:** 16h | **Dependencias:** Fase 1

- [ ] 6.1 Documentar Agent Skills spec
- [ ] 6.2 Criar best-practices (4 docs)
- [ ] 6.3 Documentar CLI specifics (7 docs)
- [ ] 6.4 Criar patterns (4 docs)
- [ ] 6.5 Gerar INDEX.md

**Entregavel:** Base de conhecimento completa

---

### Fase 7: Examples (CARD-007)
**Estimativa:** 12h | **Dependencias:** Fase 2, Fase 4

- [ ] 7.1 Criar exemplos simples (2)
- [ ] 7.2 Criar exemplos intermediarios (2)
- [ ] 7.3 Criar exemplos avancados (2)
- [ ] 7.4 Adaptar para todos CLIs
- [ ] 7.5 Testar em CLIs reais
- [ ] 7.6 Documentar uso

**Entregavel:** 6+ exemplos funcionais testados

---

### Fase 8: Validacao Final
**Estimativa:** 4h | **Dependencias:** Todas

- [ ] 8.1 Testes end-to-end
- [ ] 8.2 Validacao contra Agent Skills spec
- [ ] 8.3 Teste em todos CLIs
- [ ] 8.4 Documentacao final
- [ ] 8.5 Release v1.0.0

**Entregavel:** v1.0.0 pronta para uso

---

## Progresso

| Fase | Status | Progresso | Estimativa |
|------|--------|-----------|------------|
| Fase 1: Foundation | Pendente | 0/6 | 4h |
| Fase 2: Templates | Pendente | 0/10 | 8h |
| Fase 3: Commands | Pendente | 0/10 | 12h |
| Fase 4: Multi-CLI | Pendente | 0/6 | 8h |
| Fase 5: Human Gate | Pendente | 0/8 | 10h |
| Fase 6: Knowledge | Pendente | 0/5 | 16h |
| Fase 7: Examples | Pendente | 0/6 | 12h |
| Fase 8: Validacao | Pendente | 0/5 | 4h |
| **TOTAL** | | **0/56** | **74h** |

---

## Dependencias entre Fases

```
Fase 1 (Foundation)
    │
    ├──► Fase 2 (Templates)
    │        │
    │        ├──► Fase 3 (Commands)
    │        │        │
    │        │        └──► Fase 5 (Human Gate)
    │        │
    │        └──► Fase 4 (Multi-CLI)
    │                 │
    │                 └──► Fase 7 (Examples)
    │
    └──► Fase 6 (Knowledge)

Todas ──► Fase 8 (Validacao Final)
```

---

## Riscos e Mitigacoes

| Risco | Probabilidade | Impacto | Mitigacao |
|-------|---------------|---------|-----------|
| CLI nao detectado corretamente | Media | Alto | Fallback para pergunta ao usuario |
| Spec Agent Skills muda | Baixa | Alto | Versionar spec localmente |
| Incompatibilidade entre CLIs | Media | Medio | Testes extensivos por CLI |
| Timeout em operacoes | Baixa | Baixo | Implementar feedback de progresso |
| Skill muito grande | Media | Medio | Validacao de tamanho pre-persistencia |

---

## Marcos (Milestones)

| Marco | Descricao | Data Alvo | Status |
|-------|-----------|-----------|--------|
| M1 | Foundation + Templates | +1 semana | Pendente |
| M2 | Commands + Multi-CLI | +2 semanas | Pendente |
| M3 | Human Gate completo | +3 semanas | Pendente |
| M4 | Knowledge + Examples | +4 semanas | Pendente |
| M5 | v1.0.0 Release | +5 semanas | Pendente |

---

## Metricas de Sucesso

| Metrica | Meta | Como Medir |
|---------|------|------------|
| Skills validas | 100% | Validacao Agent Skills spec |
| CLIs suportados | 7/7 | Testes de geracao |
| Tempo de geracao | < 2s | Benchmark |
| Cobertura knowledge | 100% spec | Checklist |
| Exemplos funcionais | 6+ | Testes manuais |

---

## Referencias

- CARD-001 a CARD-007: Detalhes de implementacao
- CONSTITUTION.md: Regras T0
- ADR-001: Escolha Agent Skills standard
- Agent Skills Spec: https://agentskills.io

---

*Ultima atualizacao: 2026-02-04*

**PLAN-001** | Hefesto Skill Generator | v1.0.0
