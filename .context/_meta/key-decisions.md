# Key Decisions - Hefesto Skill Generator

> **Tier:** T2 - Informativo
> **Versao:** 1.0.0

---

## ADRs Consolidados

### ADR-001: Agent Skills como Padrao Primario

**Status:** Aceito
**Data:** 2026-02-04

**Contexto:**
Existem multiplos formatos de skills/comandos entre diferentes CLIs de IA. Precisavamos escolher um padrao para o Hefesto.

**Decisao:**
Adotar [agentskills.io](https://agentskills.io) como formato primario.

**Consequencias:**
- Positivas: Padrao aberto, suportado por multiplos CLIs, bem documentado
- Negativas: CLIs que nao suportam nativamente precisam de adapters

---

### ADR-002: Human Gate Obrigatorio

**Status:** Aceito
**Data:** 2026-02-04

**Contexto:**
Skills podem ter impacto significativo no workflow do desenvolvedor. Geracao automatica sem revisao pode criar problemas.

**Decisao:**
Implementar Human Gate obrigatorio para todas as operacoes de escrita.

**Consequencias:**
- Positivas: Controle de qualidade, usuario sempre no controle
- Negativas: Fluxo um pouco mais lento

---

### ADR-003: Template-First com Wizard Expansivel

**Status:** Aceito
**Data:** 2026-02-04

**Contexto:**
Criar skills pode ser simples ou complexo. Precisavamos de uma abordagem que atendesse ambos os casos.

**Decisao:**
Iniciar com template basico, expandir via wizard interativo quando necessario.

**Consequencias:**
- Positivas: Rapido para casos simples, completo para casos complexos
- Negativas: Duas "modes" de operacao para documentar

---

### ADR-004: Deteccao Automatica de CLIs

**Status:** Aceito
**Data:** 2026-02-04

**Contexto:**
Usuario pode ter multiplos CLIs instalados. Perguntar "qual CLI?" a cada vez e tedioso.

**Decisao:**
Detectar CLIs instalados automaticamente e gerar para todos.

**Consequencias:**
- Positivas: Experiencia fluida, menos perguntas
- Negativas: Pode gerar em CLIs que usuario nao usa ativamente

---

### ADR-005: Armazenamento no Projeto por Padrao

**Status:** Aceito
**Data:** 2026-02-04

**Contexto:**
Skills podem ser pessoais (global) ou de projeto (local). Precisavamos definir um padrao.

**Decisao:**
Armazenar no projeto atual por padrao, global apenas se explicitamente solicitado.

**Consequencias:**
- Positivas: Skills versionadas com o projeto, facil compartilhamento via Git
- Negativas: Skills pessoais requerem flag explicita

---

### ADR-006: Extracao de Codigo como Feature

**Status:** Aceito
**Data:** 2026-02-04

**Contexto:**
Desenvolvedores ja tem padroes em seu codigo que poderiam virar skills.

**Decisao:**
Implementar `/hefesto.extract` para criar skills a partir de codigo existente.

**Consequencias:**
- Positivas: Reutilizacao de conhecimento existente
- Negativas: Complexidade adicional de implementacao

---

### ADR-007: Progressive Disclosure para Skills

**Status:** Aceito
**Data:** 2026-02-04

**Contexto:**
Skills podem ter muita informacao. Carregar tudo de uma vez consome contexto desnecessariamente.

**Decisao:**
SKILL.md < 500 linhas, recursos adicionais em scripts/, references/, assets/.

**Consequencias:**
- Positivas: Otimizacao de contexto, carregamento JIT
- Negativas: Estrutura de diretorio mais complexa

---

## Principios Derivados

| Principio | ADR Origem |
|-----------|------------|
| Seguir Agent Skills spec | ADR-001 |
| Nunca persistir sem aprovacao | ADR-002 |
| Simples por padrao, complexo sob demanda | ADR-003 |
| Detectar antes de perguntar | ADR-004 |
| Projeto-first, global-opcional | ADR-005 |
| Reutilizar conhecimento existente | ADR-006 |
| Otimizar uso de contexto | ADR-007 |

---

**Ultima Atualizacao:** 2026-02-04
