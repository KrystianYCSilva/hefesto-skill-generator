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

| Card | Titulo | Estimativa | Status |
|------|--------|------------|--------|
| [CARD-001](./cards/CARD-001-foundation.md) | Foundation | 4h | ✅ COMPLETED |
| [CARD-002](./cards/CARD-002-templates.md) | Templates System | 8h | ✅ COMPLETED |
| [CARD-003](./cards/CARD-003-commands.md) | Commands /hefesto.* | 12h | ✅ COMPLETED |
| [CARD-004](./cards/CARD-004-multi-cli.md) | Multi-CLI Generator (Feature 004) | 8h | ✅ COMPLETED |
| [CARD-005](./cards/CARD-005-human-gate.md) | Human Gate + Wizard | 10h | Planned |

### Media Prioridade

| Card | Titulo | Estimativa | Dependencias |
|------|--------|------------|--------------|
| [CARD-006](./cards/CARD-006-knowledge-base.md) | Knowledge Base | 16h | CARD-001 |
| [CARD-007](./cards/CARD-007-examples.md) | Examples | 12h | CARD-002, CARD-004 |

---

## Progresso por Fase

| Fase | Card | Status | Progresso |
|------|------|--------|-----------|
| 1. Foundation | CARD-001 | ✅ COMPLETED | 6/6 |
| 2. Templates | CARD-002 | ✅ COMPLETED | 13/13 |
| 3. Commands | CARD-003 | ✅ COMPLETED | 9/9 |
| 4. Multi-CLI | CARD-004 | ✅ COMPLETED (Feature 004) | 8/8 |
| 5. Human Gate | CARD-005 | Planned | 0/8 |
| 6. Knowledge | CARD-006 | Planned | 0/5 |
| 7. Examples | CARD-007 | Planned | 0/6 |
| 8. Validacao | - | Planned | 0/5 |
| **TOTAL** | | | **36/56** (64% ✅) |

**Estimativa Total Restante:** ~36h (de 74h total)

---

## Feature 004: Multi-CLI Automatic Parallel Generation

✅ **Status: COMPLETED (2026-02-05)**

Feature 004 enables automatic detection and parallel skill generation across all 7 supported CLIs (Claude, Gemini, Codex, OpenCode, Cursor, Qwen, Copilot) with 3x performance improvement over sequential generation.

### Quick Facts

- **Detection Time**: <500ms for all 7 CLIs
- **Parallel Speedup**: 3x faster than sequential (2s vs 6s)
- **CLI Adapters**: 7 adapters with auto-transformations (e.g., Gemini `$ARGUMENTS` → `{{args}}`)
- **Atomic Rollback**: Guaranteed all-or-nothing on multi-CLI generation
- **Test Coverage**: 9/9 manual tests passed ✅
- **Compliance**: 10/10 mandatory criteria + 3/3 desirable criteria + 8/8 T0 rules ✅

### Key Deliverables

| Component | Type | Location | Status |
|-----------|------|----------|--------|
| CLI Detector | Helper | `commands/helpers/cli-detector.md` | ✅ Complete |
| CLI Adapter | Helper | `commands/helpers/cli-adapter.md` | ✅ Complete |
| Parallel Generator | Helper | `commands/helpers/parallel-generator.md` | ✅ Complete |
| Rollback Handler | Helper | `commands/helpers/rollback-handler.md` | ✅ Complete |
| Multi-CLI Integration Guide | Helper | `commands/helpers/multi-cli-integration.md` | ✅ Complete |
| Detection Report Template | Template | `commands/templates/detection-report.md` | ✅ Complete |
| Generation Report Template | Template | `commands/templates/generation-report.md` | ✅ Complete |

### Reports & Documentation

Feature 004 includes comprehensive test reports and analysis:

| Report | Lines | Location | Key Finding |
|--------|-------|----------|-------------|
| Test Report | 400 | `docs/reports/feature-004-test-report.md` | 9/9 tests passed |
| Executive Summary | 300 | `docs/reports/feature-004-executive-summary.md` | 100% compliance |
| Final Checklist | 350 | `docs/reports/feature-004-final-checklist.md` | All checks passed |
| Test Manifest | 10 | `testes/RESUMO-TESTES.txt` | TESTE-01 through TESTE-09 |

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

**Ultima Atualizacao:** 2026-02-05 (Feature 004 Complete)
