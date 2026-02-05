# CARD-006: Knowledge Base - Base de Conhecimento

## Status: 🚧 PARTIAL (2026-02-05)

**Release:** LTS v1.0.0  
**Completion Date:** 2026-02-05 (Partial)

### Completion Notes

Knowledge structure exists but needs command examples:
- ✅ `.context/` directory structure in place
- ✅ CONSTITUTION.md (T0 rules)
- ✅ architectural-rules.md (T0 standards)
- ✅ code-quality.md (T1 normative)
- ✅ tech-stack.md (T2 informative)
- ⚠️ Command examples needed in `.context/examples/`
- ⚠️ CLI-specific documentation incomplete

### Next Steps

- Add command usage examples to `.context/examples/`
- Complete CLI-specific documentation in `.context/cli-specifics/`
- Generate INDEX.md for navigation

---

## 1. Descricao & User Story

"Como um **gerador de skills**, eu quero ter acesso a uma **base de conhecimento** sobre Agent Skills spec, melhores praticas e padroes de cada CLI, para que eu possa **gerar skills de alta qualidade** consistentemente."

---

## 2. Regras de Negocio (RN)

* [RN01] Knowledge base DEVE conter spec completa do Agent Skills
* [RN02] Best practices DEVEM ser categorizadas por dominio
* [RN03] Peculiaridades de cada CLI DEVEM estar documentadas
* [RN04] Knowledge DEVE ser consultavel por skills em runtime
* [RN05] Atualizacoes de spec DEVEM ser rastreadas
* [RN06] (ADR-002) Referencias academicas DEVEM fundamentar melhores praticas
* [RN07] (ADR-002) Documentacao sobre seguranca de agentes DEVE ser incluida

---

## 3. Regras Tecnicas (RT)

* [RT01] (T0-HEFESTO-01) Spec Agent Skills como fonte primaria
* [RT02] (T0-HEFESTO-10) Citacao de fontes obrigatoria
* [RT03] Estrutura da knowledge base:
  ```
  knowledge/
  ├── INDEX.md                    # Indice navegavel
  ├── agent-skills-spec.md        # Spec completa
  ├── mcp-protocol.md             # MCP Protocol spec (ADR-002)
  ├── best-practices/
  │   ├── naming.md               # Nomenclatura
  │   ├── structure.md            # Estrutura de skills
  │   ├── descriptions.md         # Boas descricoes
  │   ├── jit-resources.md        # Recursos JIT
  │   └── security.md             # Seguranca de skills (T0-HEFESTO-11)
  ├── cli-specifics/
  │   ├── claude-code.md          # Peculiaridades Claude
  │   ├── gemini-cli.md           # Peculiaridades Gemini
  │   ├── codex.md                # Peculiaridades Codex
  │   ├── copilot.md              # Peculiaridades Copilot
  │   ├── opencode.md             # Peculiaridades OpenCode
  │   ├── cursor.md               # Peculiaridades Cursor
  │   └── qwen-code.md            # Peculiaridades Qwen
  ├── patterns/
  │   ├── code-review-skill.md    # Padrao: code review
  │   ├── testing-skill.md        # Padrao: testes
  │   ├── documentation-skill.md  # Padrao: docs
  │   └── refactoring-skill.md    # Padrao: refatoracao
  └── research/                   # Literatura academica (ADR-002)
      ├── INDEX.md                # Indice de pesquisas
      ├── ai-instruments.md       # Reificacao da intencao
      ├── prompt-injection.md     # Seguranca de agentes
      └── skill-generator-automatizado.md  # Pesquisa completa
  ```
* [RT04] Formato de cada documento knowledge:
  ```markdown
  # [Titulo]
  
  ## Fonte
  [Link oficial] | Acessado: YYYY-MM-DD
  
  ## Resumo
  [3-5 linhas]
  
  ## Detalhes
  [Conteudo completo]
  
  ## Exemplos
  [Exemplos praticos]
  
  ## Relacionados
  [Links para outros docs]
  ```
* [RT05] INDEX.md DEVE ser gerado automaticamente

---

## 4. Requisitos de Qualidade (RQ)

* [RQ01] 100% da spec Agent Skills documentada
* [RQ02] Todas as fontes DEVEM ser oficiais ou consolidadas
* [RQ03] Exemplos DEVEM ser testados e funcionais
* [RQ04] Busca por keyword em < 100ms

---

## 5. Criterios de Aceite

- [x] agent-skills-spec.md completo e validado (in CONSTITUTION.md)
- [x] Best practices documentadas (4+ documentos) (in .context/)
- [ ] CLI specifics para todos os 7 CLIs (partial)
- [ ] Patterns para casos de uso comuns (4+ patterns)
- [ ] INDEX.md gerado com navegacao
- [x] Fontes citadas em todos os documentos (T0-HEFESTO-10)
- [ ] Exemplos funcionais em cada documento (needs command examples)

---

## 6. Tarefas (Sub-Cards)

- [ ] CARD-006.1: Documentar Agent Skills spec completa
- [ ] CARD-006.2: Criar best-practices/naming.md
- [ ] CARD-006.3: Criar best-practices/structure.md
- [ ] CARD-006.4: Criar best-practices/descriptions.md
- [ ] CARD-006.5: Criar best-practices/jit-resources.md
- [ ] CARD-006.6: Criar best-practices/security.md (T0-HEFESTO-11)
- [ ] CARD-006.7: Documentar cli-specifics para cada CLI
- [ ] CARD-006.8: Criar pattern code-review-skill.md
- [ ] CARD-006.9: Criar pattern testing-skill.md
- [ ] CARD-006.10: Criar pattern documentation-skill.md
- [ ] CARD-006.11: Criar pattern refactoring-skill.md
- [ ] CARD-006.12: Documentar MCP Protocol (ADR-002)
- [ ] CARD-006.13: Organizar research/ com literatura academica
- [ ] CARD-006.14: Gerar INDEX.md

---

## 7. Referencias

### Regras T0
- T0-HEFESTO-01: Agent Skills Standard
- T0-HEFESTO-10: Citacao de Fontes
- T0-HEFESTO-11: Seguranca por Padrao

### ADRs
- ADR-002: Integracao de Pesquisa Academica

### Documentacao Oficial
- Agent Skills Spec: https://agentskills.io
- Claude Code Docs: https://docs.anthropic.com/en/docs/claude-code/skills
- Gemini CLI: https://geminicli.com
- Qwen Code: https://github.com/QwenLM/qwen-code
- MCP Protocol: https://modelcontextprotocol.io

### Literatura Academica (ADR-002)
- AI-Instruments (ACM DL) - Reificacao da intencao do usuario
- Prompt Injection Attacks (arXiv) - Seguranca de agentes de codigo
- Generative Theories of Interaction (ACM DL) - Design de interacao
- Trustworthy and Explainable AI (IEEE) - Auditabilidade

---

## 8. Metadata

| Campo | Valor |
|-------|-------|
| **Status** | 🚧 PARTIAL (2026-02-05) |
| **Prioridade** | Media |
| **Estimativa** | 20h |
| **Assignee** | AI Agent |
| **Dependencias** | CARD-001 |
| **Remaining Work** | Command examples, CLI specifics, INDEX.md |

---

**CARD-006** | Hefesto Skill Generator | Knowledge Base
