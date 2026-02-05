# CARD-004: Multi-CLI Generator - Geracao Multi-CLI

## 1. Descricao & User Story

"Como um **desenvolvedor que usa multiplos CLIs de IA**, eu quero que o Hefesto **detecte automaticamente** quais CLIs tenho instalados e **gere skills para todos eles**, para que eu tenha **consistencia** entre todas as ferramentas."

---

## 2. Regras de Negocio (RN)

* [RN01] Deteccao DEVE ocorrer automaticamente ANTES de perguntar ao usuario
* [RN02] Skills DEVEM ser geradas para TODOS os CLIs detectados
* [RN03] Usuario pode restringir CLIs via argumento `--cli`
* [RN04] Adapters DEVEM garantir compatibilidade com cada CLI
* [RN05] Sincronizacao DEVE manter skills identicas semanticamente

---

## 3. Regras Tecnicas (RT)

* [RT01] (T0-HEFESTO-04) Detectar CLIs ANTES de perguntar
* [RT02] (T0-HEFESTO-09) Garantir compatibilidade com todos CLIs
* [RT03] Matriz de deteccao:

| CLI | Executavel | Config Dir | Prioridade |
|-----|------------|------------|------------|
| Claude Code | `claude` | `.claude/` | 1 |
| Gemini CLI | `gemini` | `.gemini/` | 2 |
| OpenAI Codex | `codex` | `.codex/` | 3 |
| VS Code/Copilot | `code` | `.github/` | 4 |
| OpenCode | `opencode` | `.opencode/` | 5 |
| Cursor | `cursor` | `.cursor/` | 6 |
| Qwen Code | `qwen` | `.qwen/` | 7 |

* [RT04] Algoritmo de deteccao:
  ```
  1. Verificar executaveis no PATH
  2. Verificar diretorios de config existentes
  3. Unir resultados (CLI detectado se PATH OU config existe)
  4. Se nenhum detectado, perguntar ao usuario
  ```
* [RT05] Adaptacoes por CLI:
  - Gemini/Qwen: `$ARGUMENTS` -> `{{args}}`
  - Copilot: Estrutura `.github/skills/` especifica
  - Todos: Frontmatter YAML padrao

---

## 4. Requisitos de Qualidade (RQ)

* [RQ01] Deteccao em < 500ms
* [RQ02] Zero falsos positivos (nao detectar CLI inexistente)
* [RQ03] Geracao paralela para multiplos CLIs
* [RQ04] Rollback se falha em qualquer CLI

---

## 5. Criterios de Aceite

- [x] Deteccao automatica de todos os 7 CLIs
- [x] Geracao simultanea para CLIs detectados (3x speedup)
- [x] Adapter funcionando para cada CLI (7 adapters com transformacoes auto)
- [x] Argumento `--cli` para restringir geracao
- [x] Sincronizacao bidirecional entre CLIs
- [x] Report de CLIs detectados vs nao detectados
- [x] Fallback para pergunta se zero detectados

### Test Results (2026-02-05)

**Manual Tests:** 9/9 passed ✅
**Mandatory Criteria:** 10/10 met ✅
**Desirable Criteria:** 3/3 met ✅

---

## 6. Tarefas (Sub-Cards)

- [x] CARD-004.1: Implementar detector de executaveis (PATH)
- [x] CARD-004.2: Implementar detector de config dirs
- [x] CARD-004.3: Unificar resultados de deteccao
- [x] CARD-004.4: Implementar geracao paralela
- [x] CARD-004.5: Implementar argumento `--cli`
- [x] CARD-004.6: Implementar report de deteccao
- [x] CARD-004.7: Implementar fallback interativo
- [x] CARD-004.8: Testes de integracao por CLI

---

## 7. Referencias

- T0-HEFESTO-04: Multi-CLI Deteccao
- T0-HEFESTO-05: Armazenamento Local
- T0-HEFESTO-09: Compatibilidade CLI
- .context/_meta/tech-stack.md: Stack tecnica

---

## 8. Metadata

| Campo | Valor |
|-------|-------|
| **Status** | ✅ COMPLETED (2026-02-05) |
| **Prioridade** | Alta |
| **Estimativa** | 8h |
| **Assignee** | AI Agent |
| **Dependencias** | CARD-001, CARD-002 |
| **Completeness** | 9/9 manual tests ✅, 10/10 mandatory criteria ✅, 3/3 desirable criteria ✅ |

---

**CARD-004** | Hefesto Skill Generator | Multi-CLI Generator
