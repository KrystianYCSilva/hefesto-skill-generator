# decisions/ - Architecture Decision Records

> **ADRs do Hefesto Skill Generator**

---

## Indice de ADRs

| ADR | Titulo | Status | Data |
|-----|--------|--------|------|
| ADR-001 | Agent Skills como Padrao Primario | Aceito | 2026-02-04 |
| ADR-002 | Human Gate Obrigatorio | Aceito | 2026-02-04 |
| ADR-003 | Template-First com Wizard Expansivel | Aceito | 2026-02-04 |
| ADR-004 | Deteccao Automatica de CLIs | Aceito | 2026-02-04 |
| ADR-005 | Armazenamento no Projeto por Padrao | Aceito | 2026-02-04 |
| ADR-006 | Extracao de Codigo como Feature | Aceito | 2026-02-04 |
| ADR-007 | Progressive Disclosure para Skills | Aceito | 2026-02-04 |

---

## Resumo das Decisoes

### ADR-001: Agent Skills Standard

**Decisao:** Adotar agentskills.io como formato primario.

**Consequencias:** Padrao aberto, suportado por multiplos CLIs.

---

### ADR-002: Human Gate

**Decisao:** Implementar aprovacao humana obrigatoria para escrita.

**Consequencias:** Controle de qualidade garantido.

---

### ADR-003: Template-First + Wizard

**Decisao:** Template basico por padrao, wizard para expansao.

**Consequencias:** Rapido para casos simples, completo para complexos.

---

### ADR-004: Deteccao Automatica

**Decisao:** Detectar CLIs instalados automaticamente.

**Consequencias:** UX fluida, menos perguntas.

---

### ADR-005: Projeto-First Storage

**Decisao:** Armazenar skills no projeto atual por padrao.

**Consequencias:** Skills versionadas com Git.

---

### ADR-006: Extract Feature

**Decisao:** Implementar /hefesto.extract para criar skills de codigo.

**Consequencias:** Reutilizacao de conhecimento existente.

---

### ADR-007: Progressive Disclosure

**Decisao:** SKILL.md < 500 linhas, recursos em sub-arquivos.

**Consequencias:** Otimizacao de contexto.

---

**Ultima Atualizacao:** 2026-02-04
