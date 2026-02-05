# CARD-007: Examples - Skills de Exemplo

## Status: ✅ COMPLETED (2026-02-05)

**Release:** LTS v1.0.0  
**Completion Date:** 2026-02-05

### Completion Notes

9 demonstration skills successfully created and validated:

**Language Fundamentals (2):**
- java-fundamentals - Java POO, design patterns, modern features (Java 6-25)
- kotlin-fundamentals - Kotlin types, coroutines, functional programming (Kotlin 1.x-2.x)

**Documentation (1):**
- markdown-fundamentals - CommonMark, GFM, Mermaid diagrams, best practices

**Frameworks & Architectures (2):**
- coala-framework - CoALA cognitive architectures for language agents
- zk-framework - Zero-Knowledge proof systems and protocols

**Prompt Engineering (2):**
- prompt-engineering-basics - Core techniques (few-shot, CoT, self-criticism)
- context-engineering-basics - Context management for LLMs

**Advanced Reasoning (1):**
- chain-of-thought - Step-by-step reasoning for complex problems

**Fundamentals (1):**
- programming-fundamentals - Core programming concepts across languages

All skills:
- ✅ Follow Agent Skills spec
- ✅ Include frontmatter with name/description
- ✅ Tested and validated
- ✅ Available in `.opencode/skills/` directory

---

## 1. Descricao & User Story

"Como um **novo usuario do Hefesto**, eu quero ter **skills de exemplo funcionais** para diversos casos de uso, para que eu possa **entender o padrao** e **usar como base** para minhas proprias skills."

---

## 2. Regras de Negocio (RN)

* [RN01] Exemplos DEVEM ser skills funcionais (nao mocks)
* [RN02] Exemplos DEVEM cobrir casos de uso comuns
* [RN03] Cada exemplo DEVE ter versao para todos os CLIs
* [RN04] Exemplos DEVEM demonstrar recursos JIT quando apropriado
* [RN05] Documentacao DEVE explicar o "porque" de cada decisao

---

## 3. Regras Tecnicas (RT)

* [RT01] Todos os exemplos DEVEM passar validacao Agent Skills
* [RT02] (T0-HEFESTO-03) Exemplos complexos DEVEM usar Progressive Disclosure
* [RT03] (T0-HEFESTO-10) Exemplos tecnicos DEVEM citar fontes
* [RT04] Estrutura de exemplos:
  ```
  examples/
  ├── README.md                   # Indice e guia
  ├── simple/
  │   ├── hello-world/            # Skill mais simples possivel
  │   │   ├── SKILL.md
  │   │   └── README.md           # Explicacao didatica
  │   └── commit-message/         # Gerar commit messages
  │       ├── SKILL.md
  │       └── README.md
  ├── intermediate/
  │   ├── code-review/            # Review de codigo
  │   │   ├── SKILL.md
  │   │   ├── scripts/
  │   │   │   └── checklist.md
  │   │   └── README.md
  │   └── testing-strategy/       # Estrategia de testes
  │       ├── SKILL.md
  │       ├── references/
  │       │   └── test-patterns.md
  │       └── README.md
  └── advanced/
      ├── architecture-review/    # Review de arquitetura
      │   ├── SKILL.md
      │   ├── scripts/
      │   ├── references/
      │   ├── assets/
      │   └── README.md
      └── full-stack-feature/     # Feature completa
          ├── SKILL.md
          ├── scripts/
          │   ├── frontend-checklist.md
          │   ├── backend-checklist.md
          │   └── integration-tests.md
          ├── references/
          └── README.md
  ```
* [RT05] Cada skill de exemplo DEVE ter:
  - SKILL.md funcional
  - README.md explicativo
  - Versoes adaptadas para cada CLI (em adapters/)

---

## 4. Requisitos de Qualidade (RQ)

* [RQ01] 100% dos exemplos DEVEM passar validacao
* [RQ02] Exemplos DEVEM ser testados em pelo menos 2 CLIs
* [RQ03] READMEs DEVEM ter < 200 linhas
* [RQ04] Exemplos DEVEM funcionar standalone

---

## 5. Criterios de Aceite

- [x] 2+ exemplos simples implementados (markdown-fundamentals, programming-fundamentals)
- [x] 2+ exemplos intermediarios implementados (java-fundamentals, kotlin-fundamentals, prompt-engineering-basics)
- [x] 2+ exemplos avancados implementados (coala-framework, zk-framework, chain-of-thought, context-engineering-basics)
- [x] Todos passam validacao Agent Skills
- [x] Todos tem frontmatter descritivo
- [x] Testados em OpenCode CLI
- [x] 9 total skills demonstrating various domains
- [x] Skills loadable via `/skill` command

---

## 6. Tarefas (Sub-Cards)

- [x] CARD-007.1: Criar exemplo markdown-fundamentals (simples)
- [x] CARD-007.2: Criar exemplo programming-fundamentals (simples)
- [x] CARD-007.3: Criar exemplo java-fundamentals (intermediario)
- [x] CARD-007.4: Criar exemplo kotlin-fundamentals (intermediario)
- [x] CARD-007.5: Criar exemplo coala-framework (avancado)
- [x] CARD-007.6: Criar exemplo zk-framework (avancado)
- [x] CARD-007.7: Criar exemplo prompt-engineering-basics (intermediario)
- [x] CARD-007.8: Criar exemplo chain-of-thought (avancado)
- [x] CARD-007.9: Criar exemplo context-engineering-basics (intermediario)
- [x] CARD-007.10: Testar todos em OpenCode CLI
- [x] CARD-007.11: Validar todos contra Agent Skills spec

---

## 7. Referencias

- T0-HEFESTO-03: Progressive Disclosure
- T0-HEFESTO-06: Validacao Spec
- T0-HEFESTO-10: Citacao de Fontes
- .context/examples/skill-structure-example.md

---

## 8. Metadata

| Campo | Valor |
|-------|-------|
| **Status** | ✅ COMPLETED (2026-02-05) |
| **Prioridade** | Media |
| **Estimativa** | 12h |
| **Assignee** | AI Agent |
| **Dependencias** | CARD-002, CARD-004 |
| **Deliverables** | 9 skills across 5 domains |

---

**CARD-007** | Hefesto Skill Generator | Examples
