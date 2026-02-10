# Key Decisions - Hefesto Skill Generator

> **Tier:** T2 - Informativo
> **Versao:** 2.2.0
---

## ADRs Consolidados

### ADR-001: Agent Skills como Padrao Primario

**Status:** Aceito
**Data:** 2026-02-04

**Decisao:** Adotar [agentskills.io](https://agentskills.io) como formato primario de skills.

**Consequencias:**
- Positivas: Padrao aberto, suportado por multiplos CLIs, bem documentado
- Negativas: CLIs que nao suportam nativamente precisam de adapters

---

### ADR-002: Human Gate Obrigatorio

**Status:** Aceito
**Data:** 2026-02-04

**Decisao:** Implementar Human Gate obrigatorio para todas as operacoes de escrita.

**Consequencias:**
- Positivas: Controle de qualidade, usuario sempre no controle
- Negativas: Fluxo um pouco mais lento

---

### ADR-003: Deteccao Automatica de CLIs

**Status:** Aceito
**Data:** 2026-02-04

**Decisao:** Detectar CLIs instalados automaticamente e gerar para todos.

**Consequencias:**
- Positivas: Experiencia fluida, menos perguntas
- Negativas: Pode gerar em CLIs que usuario nao usa ativamente

---

### ADR-004: Armazenamento no Projeto por Padrao

**Status:** Aceito
**Data:** 2026-02-04

**Decisao:** Armazenar no projeto atual por padrao, global apenas se explicitamente solicitado.

**Consequencias:**
- Positivas: Skills versionadas com o projeto, facil compartilhamento via Git
- Negativas: Skills pessoais requerem flag explicita

---

### ADR-005: Progressive Disclosure para Skills

**Status:** Aceito
**Data:** 2026-02-04

**Decisao:** SKILL.md < 500 linhas, recursos adicionais em scripts/, references/, assets/.

**Consequencias:**
- Positivas: Otimizacao de contexto, carregamento JIT
- Negativas: Estrutura de diretorio mais complexa

---

### ADR-006: Extracao de Codigo como Feature

**Status:** Aceito
**Data:** 2026-02-04

**Decisao:** Implementar `/hefesto.extract` para criar skills a partir de codigo existente.

**Consequencias:**
- Positivas: Reutilizacao de conhecimento existente
- Negativas: Complexidade adicional de implementacao

---

### ADR-007: Template-Driven (Zero Dependencies)

**Status:** Aceito
**Data:** 2026-02-07

**Decisao:** Toda logica do Hefesto vive em Markdown templates que o AI agent interpreta. Zero Python, zero Node.js, zero dependencias externas.

**Consequencias:**
- Positivas: Portabilidade universal, zero setup, funciona com qualquer AI CLI
- Negativas: Sem automacao "tradicional" (scripts, CLI executavel)

---

### ADR-008: Frontmatter Minimo (ONLY name + description)

**Status:** Aceito
**Data:** 2026-02-07

**Decisao:** Frontmatter de skills deve conter SOMENTE `name` e `description`. Nenhum outro campo (license, metadata, version, tags, compatibility).

**Justificativa:** Token economy - campos extras nao agregam valor para o AI agent e consomem contexto. Toda informacao de trigger/discovery fica na description.

**Consequencias:**
- Positivas: Skills mais leves, menos ruido, focadas no essencial
- Negativas: Perde metadados como tags e versao (trade-off aceito)

---

### ADR-009: Body Pattern "How to [task]"

**Status:** Aceito
**Data:** 2026-02-07

**Decisao:** O body de skills deve usar secoes "How to [task]" ao inves de "Instructions > Step N".

**Justificativa:** Padrao mais natural, orientado a tarefas. Cada secao e auto-contida e pode ser carregada JIT.

**Consequencias:**
- Positivas: Skills mais intuitivas, faceis de navegar
- Negativas: Requer refatoracao de skills existentes com padrao antigo

---

### ADR-010: Installer Portatil (Bash + PowerShell)

**Status:** Aceito
**Data:** 2026-02-07

**Decisao:** Criar scripts de bootstrap portaveis (`install.sh` para Unix, `install.ps1` para Windows) que instalam Hefesto em qualquer projeto.

**O que o installer faz:**
1. Detecta CLIs instalados (PATH + diretorios)
2. Cria `.hefesto/` com templates e versao
3. Copia comandos `hefesto.*` para cada CLI detectado
4. Cria diretorios `skills/`

**Consequencias:**
- Positivas: Instalacao facil, cross-platform, idempotente
- Negativas: Dois scripts para manter (bash + PowerShell)

---

### ADR-011: Auto-Critica 13 Pontos

**Status:** Aceito
**Data:** 2026-02-07

**Decisao:** Toda skill gerada deve passar por auto-critica de 13 pontos (5 CRITICAL + 7 WARNING + 1 INFO) antes de ser apresentada ao usuario.

**Consequencias:**
- Positivas: Qualidade consistente, menos erros chegam ao Human Gate
- Negativas: Geracao ligeiramente mais lenta

---

## Principios Derivados

| Principio | ADR Origem |
|-----------|------------|
| Seguir Agent Skills spec | ADR-001 |
| Nunca persistir sem aprovacao | ADR-002 |
| Detectar antes de perguntar | ADR-003 |
| Projeto-first, global-opcional | ADR-004 |
| Otimizar uso de contexto | ADR-005 |
| Reutilizar conhecimento existente | ADR-006 |
| Template-driven, zero dependencies | ADR-007 |
| Frontmatter minimo | ADR-008 |
| Secoes "How to [task]" | ADR-009 |
| Installer portatil | ADR-010 |
| Auto-critica obrigatoria | ADR-011 |

---

**Ultima Atualizacao:** 2026-02-07 (v2.0.0)


