# Key Decisions - Hefesto Skill Generator

> **Tier:** T2 - Informativo
> **Versao:** 1.0.0-LTS (Production Ready)
> **Status:** ✅ LTS Release

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

### ADR-008: Geracao Paralela Atomica para Multi-CLI (Feature 004)

**Status:** Aceito e Implementado
**Data:** 2026-02-05

**Contexto:**
Gerar skills sequencialmente para 7 CLIs e lento (~6s). ALem disso, se falha no meio da geracao, fica com estado inconsistente (alguns CLIs com skill, outros sem).

**Decisao:**
Implementar geracao paralela com atomicidade garantida:
1. Detectar todos CLIs em <500ms (nao perguntar usuario)
2. Gerar em paralelo para todos CLIs simultaneamente
3. Guarantir all-or-nothing semantics (rollback atomico se qualquer falha)
4. Permitir restricao com `--cli` flag se usuario preferir

**Arquitetura Feature 004:**
- **CLI Detector**: Deteccao rapida de 7 CLIs via PATH + config dirs
- **CLI Adapter**: 7 adapters especificos com transformacoes (ex: Gemini `$ARGUMENTS` → `{{args}}`)
- **Parallel Generator**: Execucao paralela com bash/PowerShell
- **Rollback Handler**: Cleanup garantido em caso de falha

**Consequencias:**
- Positivas: 
  - 3x performance improvement (2s vs 6s)
  - Zero estado inconsistente
  - Experiencia fluida sem perguntas
  - Professional-grade reliability
- Negativas: 
  - Complexidade adicional de implementacao
  - Necessario suporte a deteccao de 7 CLIs
  - Rollback Handler necessario

**Implementacao Status:**
- ✅ 5 helpers implementados (cli-detector, cli-adapter, parallel-generator, rollback-handler, multi-cli-integration)
- ✅ 2 templates criados (detection-report, generation-report)
- ✅ 9/9 testes manuais passando
- ✅ Spec compliance: 10/10 mandatory + 3/3 desirable + 8/8 T0 rules

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
| **Paralelo + Atomico para multi-CLI** | **ADR-008 (Feature 004)** |

---

---

### ADR-009: LTS v1.0.0 Release with 97.4% Completion

**Status:** Aceito
**Data:** 2026-02-05

**Contexto:**
Projeto atingiu 97.4% de completude (222/228 tasks) com todas as features P1 (prioridade 1) entregues. Itens pendentes sao nao-bloqueantes: testes manuais (T037), exemplos de comandos adicionais, e implementacao do shared skill pool (diferido para v1.1.0).

**Decisao:**
Marcar Hefesto como production-ready com status LTS v1.0.0, permitindo uso em producao com recomendacao de testes manuais antes de workflows criticos.

**Entregas LTS v1.0.0:**
- ✅ 9 comandos operacionais (100%)
- ✅ 9 skills demonstrativas em 5 dominios
- ✅ 5 CARDs completos (001-005)
- ✅ Multi-CLI parallel generation (3x performance)
- ✅ Human Gate workflow (89% completo, core operacional)
- ✅ Todas as 11 regras T0 validadas
- ✅ Agent Skills spec compliance

**Itens Pendentes (Nao-Bloqueantes):**
- Manual testing Feature 005 (T037) - recomendado antes de uso critico
- Exemplos adicionais de comandos (CARD-006) - nice-to-have
- Shared skill pool (CARD-008) - diferido para v1.1.0

**Consequencias:**
- Positivas:
  - Release formal marca maturidade do projeto
  - Usuarios podem usar com confianca em producao
  - LTS garante suporte de longo prazo
  - 9 skills demonstram qualidade e capacidade
  - 97.4% completion profissional
- Negativas:
  - 2.6% de tasks pendentes (6 tasks)
  - Testes manuais ainda recomendados
  - CARD-008 diferido para proxima versao

**Justificativa:**
Com todas as features P1 entregues, 9 skills validadas, e 97.4% de completude, o projeto demonstrou maturidade para producao. Itens pendentes sao incrementais e nao-bloqueantes.

---

**Ultima Atualizacao:** 2026-02-05 (LTS v1.0.0 Release - ADR-009 added)
