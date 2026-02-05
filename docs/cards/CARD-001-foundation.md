# CARD-001: Foundation - Estrutura Base

## 1. Descricao & User Story

"Como um **desenvolvedor usando CLIs de IA**, eu quero ter uma **estrutura base do Hefesto** instalada no meu projeto, para que eu possa **gerar Agent Skills padronizadas** para qualquer CLI suportado."

---

## 2. Regras de Negocio (RN)

* [RN01] O projeto DEVE ter estrutura de diretorios para skills de cada CLI suportado
* [RN02] A CONSTITUTION.md DEVE estar presente e ser imutavel (T0)
* [RN03] O MEMORY.md DEVE rastrear estado persistente entre sessoes
* [RN04] Os comandos /hefesto.* DEVEM estar disponiveis apos bootstrap

---

## 3. Regras Tecnicas (RT)

* [RT01] (T0-HEFESTO-01) Toda skill DEVE seguir Agent Skills spec
* [RT02] (T0-HEFESTO-05) Skills armazenadas no projeto por padrao
* [RT03] Estrutura de diretorios:
  ```
  projeto/
  ├── .claude/skills/      # Claude Code
  ├── .gemini/skills/      # Gemini CLI  
  ├── .codex/skills/       # OpenAI Codex
  ├── .github/skills/      # VS Code/Copilot
  ├── .opencode/skills/    # OpenCode
  ├── .cursor/skills/      # Cursor
  └── .qwen/skills/        # Qwen Code
  ```
* [RT04] Apenas diretorios de CLIs detectados sao criados
* [RT05] Arquivos de configuracao base:
  - CONSTITUTION.md (T0)
  - MEMORY.md (state)
  - commands/*.md (comandos)

---

## 4. Requisitos de Qualidade (RQ)

* [RQ01] Bootstrap completo em < 5 segundos
* [RQ02] Zero dependencias externas para estrutura base
* [RQ03] Compativel com Git (arquivos < 100KB cada)
* [RQ04] Funciona offline apos bootstrap inicial

---

## 5. Criterios de Aceite

- [x] Estrutura de diretorios criada para CLIs detectados
- [x] CONSTITUTION.md presente e carregavel
- [x] MEMORY.md inicializado com estado vazio
- [x] Comandos /hefesto.* funcionais
- [x] Deteccao automatica de CLIs instalados
- [x] Human Gate funcional para operacoes de escrita

---

## 6. Tarefas (Sub-Cards)

- [ ] CARD-001.1: Criar detector de CLIs (PATH + config dirs)
- [ ] CARD-001.2: Implementar criacao de estrutura de diretorios
- [ ] CARD-001.3: Copiar CONSTITUTION.md para projeto
- [ ] CARD-001.4: Inicializar MEMORY.md
- [ ] CARD-001.5: Registrar comandos /hefesto.*

---

## 7. Referencias

- T0-HEFESTO-01: Agent Skills Standard
- T0-HEFESTO-04: Multi-CLI Deteccao
- T0-HEFESTO-05: Armazenamento Local
- ADR-001: Escolha do padrao Agent Skills

---

## 8. Metadata

| Campo | Valor |
|-------|-------|
| **Status** | ✅ COMPLETED (2026-02-05) |
| **Prioridade** | Alta |
| **Estimativa** | 4h |
| **Assignee** | AI Agent |
| **Dependencias** | Nenhuma (primeiro card) |

---

**CARD-001** | Hefesto Skill Generator | Foundation
