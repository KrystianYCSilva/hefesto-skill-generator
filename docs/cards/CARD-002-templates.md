# CARD-002: Templates System - Sistema de Templates

## 1. Descricao & User Story

"Como um **gerador de skills**, eu quero ter **templates padronizados** para cada tipo de skill e CLI, para que eu possa **gerar skills consistentes e validas** automaticamente."

---

## 2. Regras de Negocio (RN)

* [RN01] Template base DEVE seguir Agent Skills spec (agentskills.io)
* [RN02] Cada CLI DEVE ter um adapter que converte template base
* [RN03] Templates DEVEM suportar variaveis de substituicao
* [RN04] Template principal (SKILL.md) DEVE ser < 500 linhas
* [RN05] Recursos adicionais DEVEM usar estrutura JIT (scripts/, references/, assets/)
* [RN06] Templates DEVEM suportar metadados expandidos (ADR-002)
* [RN07] Adapter MCP DEVE ser fornecido como formato alternativo de saida

---

## 3. Regras Tecnicas (RT)

* [RT01] (T0-HEFESTO-01) Frontmatter YAML obrigatorio com `name` e `description`
* [RT02] (T0-HEFESTO-03) Progressive Disclosure: core < 500 linhas
* [RT03] (T0-HEFESTO-07) Nomenclatura: lowercase, hyphens, max 64 chars
* [RT04] (T0-HEFESTO-09) Adapters por CLI:
  ```
  templates/
  ├── skill-template.md        # Template base Agent Skills
  └── adapters/
      ├── claude.adapter.md    # $ARGUMENTS
      ├── gemini.adapter.md    # {{args}}
      ├── codex.adapter.md     # $ARGUMENTS
      ├── copilot.adapter.md   # $ARGUMENTS
      ├── opencode.adapter.md  # $ARGUMENTS
      ├── cursor.adapter.md    # $ARGUMENTS
      └── qwen.adapter.md      # {{args}}
  ```
* [RT05] Variaveis de substituicao:
  - `{{SKILL_NAME}}` - Nome da skill
  - `{{SKILL_DESCRIPTION}}` - Descricao
  - `{{SKILL_BODY}}` - Corpo da skill
  - `{{CREATED_DATE}}` - Data de criacao
  - `{{VERSION}}` - Versao da skill
  - `{{ARGUMENTS}}` - Placeholder para argumentos (CLI-specific)
* [RT06] (ADR-003) Frontmatter leve com metadados JIT:
  ```yaml
  # SKILL.md - Frontmatter LEVE (~100 tokens)
  ---
  name: skill-name           # Obrigatorio (T0-HEFESTO-01)
  description: |             # Obrigatorio (T0-HEFESTO-01)
    Descricao detalhada.
    Use quando: [gatilhos]
  license: MIT               # Obrigatorio (ADR-003)
  metadata: ./metadata.yaml  # Opcional - ponteiro JIT
  ---
  ```
  ```yaml
  # metadata.yaml - Carregado JIT pelo agente
  author: "Nome <email>"
  version: "1.0.0"
  created: 2026-02-04
  category: "development"
  tags: [tag1, tag2]
  platforms: ["claude", "gemini"]
  dependencies: ["dep1"]
  example_prompt: "Exemplo de uso"
  test_cases: [...]
  ```
* [RT08] Estrutura final de skill:
  ```
  skill-name/
  ├── SKILL.md           # Core + frontmatter leve
  ├── metadata.yaml      # Metadados expandidos (JIT)
  ├── scripts/           # Recursos executaveis (JIT)
  ├── references/        # Documentacao detalhada (JIT)
  └── assets/            # Recursos estaticos (JIT)
  ```
* [RT07] (ADR-002) Adapter MCP para interoperabilidade:
  ```
  templates/
  └── adapters/
      └── mcp.adapter.md      # MCP Server template
  ```
  - Gera servidor MCP standalone
  - Compativel com Gemini CLI, Codex, Copilot, Cursor
  - Expoe skill via protocolo padronizado

---

## 4. Requisitos de Qualidade (RQ)

* [RQ01] 100% das skills geradas DEVEM passar validacao Agent Skills spec
* [RQ02] Templates DEVEM ser testados contra todos os CLIs
* [RQ03] Adapters DEVEM ser idempotentes (mesma entrada = mesma saida)
* [RQ04] Tempo de geracao < 100ms por skill

---

## 5. Criterios de Aceite

- [ ] Template base (skill-template.md) criado e validado
- [ ] Adapters para todos os 7 CLIs implementados
- [ ] Sistema de variaveis funcionando
- [ ] Validacao automatica de output
- [ ] Skills geradas passam em todos os CLIs testados
- [ ] Documentacao de cada adapter

---

## 6. Tarefas (Sub-Cards)

- [ ] CARD-002.1: Criar skill-template.md base
- [ ] CARD-002.2: Implementar sistema de variaveis
- [ ] CARD-002.3: Criar adapter Claude Code
- [ ] CARD-002.4: Criar adapter Gemini CLI
- [ ] CARD-002.5: Criar adapter OpenAI Codex
- [ ] CARD-002.6: Criar adapter VS Code/Copilot
- [ ] CARD-002.7: Criar adapter OpenCode
- [ ] CARD-002.8: Criar adapter Cursor
- [ ] CARD-002.9: Criar adapter Qwen Code
- [ ] CARD-002.10: Validador de templates
- [ ] CARD-002.11: Criar adapter MCP (ADR-002)
- [ ] CARD-002.12: Criar metadata.yaml template (ADR-003)
- [ ] CARD-002.13: Implementar carregamento JIT de metadados

---

## 7. Referencias

- T0-HEFESTO-01: Agent Skills Standard
- T0-HEFESTO-03: Progressive Disclosure
- T0-HEFESTO-07: Nomenclatura Padrao
- T0-HEFESTO-09: Compatibilidade CLI
- T0-HEFESTO-11: Seguranca por Padrao
- ADR-002: Integracao de Pesquisa Academica
- ADR-003: Frontmatter Leve com Metadados JIT
- Agent Skills Spec: https://agentskills.io
- MCP Spec: Model Context Protocol (Anthropic)

---

## 8. Metadata

| Campo | Valor |
|-------|-------|
| **Status** | Planned |
| **Prioridade** | Alta |
| **Estimativa** | 10h |
| **Assignee** | AI Agent |
| **Dependencias** | CARD-001 (Foundation) |

---

**CARD-002** | Hefesto Skill Generator | Templates System
