# docs/ - Documentacao do Projeto

> **AVISO PARA IAs**: Esta pasta e "arquivo morto" para humanos.
> Para contexto ativo, consulte `/.context/` primeiro.

---

## Estrutura

| Pasta | Conteudo |
|-------|----------|
| `cards/` | Unidades de trabalho (tarefas de implementacao) |
| `decisions/` | ADRs (decisoes arquiteturais) |
| `plan/` | Planos de implementacao |

---

## Links Rapidos

- [ARCHITECTURE.md](./ARCHITECTURE.md) - Visao geral do sistema
- [Cards Ativos](./cards/) - Trabalho em andamento
- [Decisoes](./decisions/) - Historico de ADRs
- [Plano de Implementacao](./plan/PLAN-001-hefesto-v1.md) - Roadmap v1.0

---

## Convencoes de Nomenclatura

| Tipo | Formato | Exemplo |
|------|---------|---------|
| Card | `CARD-XXX-descricao.md` | CARD-001-foundation.md |
| ADR | `ADR-XXX-descricao.md` | ADR-001-agent-skills-standard.md |
| Plano | `PLAN-XXX-descricao.md` | PLAN-001-hefesto-v1.md |

---

## Cards Disponiveis

### Alta Prioridade

| Card | Titulo | Estimativa | Dependencias |
|------|--------|------------|--------------|
| [CARD-001](./cards/CARD-001-foundation.md) | Foundation | 4h | - |
| [CARD-002](./cards/CARD-002-templates.md) | Templates System | 8h | CARD-001 |
| [CARD-003](./cards/CARD-003-commands.md) | Commands /hefesto.* | 12h | CARD-001, CARD-002 |
| [CARD-004](./cards/CARD-004-multi-cli.md) | Multi-CLI Generator | 8h | CARD-001, CARD-002 |
| [CARD-005](./cards/CARD-005-human-gate.md) | Human Gate + Wizard | 10h | CARD-001, CARD-002, CARD-003 |

### Media Prioridade

| Card | Titulo | Estimativa | Dependencias |
|------|--------|------------|--------------|
| [CARD-006](./cards/CARD-006-knowledge-base.md) | Knowledge Base | 16h | CARD-001 |
| [CARD-007](./cards/CARD-007-examples.md) | Examples | 12h | CARD-002, CARD-004 |

---

## Progresso por Fase

| Fase | Card | Status | Progresso |
|------|------|--------|-----------|
| 1. Foundation | CARD-001 | Planned | 0/6 |
| 2. Templates | CARD-002 | Planned | 0/10 |
| 3. Commands | CARD-003 | Planned | 0/10 |
| 4. Multi-CLI | CARD-004 | Planned | 0/6 |
| 5. Human Gate | CARD-005 | Planned | 0/8 |
| 6. Knowledge | CARD-006 | Planned | 0/5 |
| 7. Examples | CARD-007 | Planned | 0/6 |
| 8. Validacao | - | Planned | 0/5 |
| **TOTAL** | | | **0/56** |

**Estimativa Total:** 74h

---

## ADRs

| ADR | Titulo | Status |
|-----|--------|--------|
| [ADR-001](./decisions/ADR-001-agent-skills-standard.md) | Escolha do Agent Skills Standard | Aceito |

---

## Planos

| Plano | Titulo | Status |
|-------|--------|--------|
| [PLAN-001](./plan/PLAN-001-hefesto-v1.md) | Hefesto v1.0.0 | Em Planejamento |

---

**Ultima Atualizacao:** 2026-02-04
