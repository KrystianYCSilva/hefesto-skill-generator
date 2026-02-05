# CARD-007: Examples - Skills de Exemplo

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

- [ ] 2+ exemplos simples implementados
- [ ] 2+ exemplos intermediarios implementados
- [ ] 2+ exemplos avancados implementados
- [ ] Todos passam validacao Agent Skills
- [ ] Todos tem README explicativo
- [ ] Testados em Claude Code e Gemini CLI
- [ ] INDEX.md com navegacao
- [ ] Documentacao de como usar exemplos

---

## 6. Tarefas (Sub-Cards)

- [ ] CARD-007.1: Criar exemplo hello-world (simples)
- [ ] CARD-007.2: Criar exemplo commit-message (simples)
- [ ] CARD-007.3: Criar exemplo code-review (intermediario)
- [ ] CARD-007.4: Criar exemplo testing-strategy (intermediario)
- [ ] CARD-007.5: Criar exemplo architecture-review (avancado)
- [ ] CARD-007.6: Criar exemplo full-stack-feature (avancado)
- [ ] CARD-007.7: Adaptar exemplos para todos CLIs
- [ ] CARD-007.8: Testar em CLIs reais
- [ ] CARD-007.9: Criar README.md principal
- [ ] CARD-007.10: Documentar uso dos exemplos

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
| **Status** | Planned |
| **Prioridade** | Media |
| **Estimativa** | 12h |
| **Assignee** | AI Agent |
| **Dependencias** | CARD-002, CARD-004 |

---

**CARD-007** | Hefesto Skill Generator | Examples
