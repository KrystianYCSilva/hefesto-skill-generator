# CARD-003: Commands - Comandos /hefesto.*

## Status: ✅ COMPLETED (2026-02-05)

**Release:** LTS v1.0.0  
**Completion Date:** 2026-02-05

### Completion Notes

All 9 commands fully implemented and operational:
1. `/hefesto.init` - Bootstrap Hefesto in project
2. `/hefesto.create` - Create skill from description (Wizard Mode)
3. `/hefesto.extract` - Extract skill from existing code
4. `/hefesto.validate` - Validate skill against Agent Skills spec
5. `/hefesto.adapt` - Adapt skill to different CLI
6. `/hefesto.sync` - Synchronize skills across CLIs
7. `/hefesto.show` - Display specific skill content
8. `/hefesto.delete` - Delete skill with confirmation
9. `/hefesto.help` - Display help and documentation

All write commands integrated with Human Gate protocol. Wizard mode operational for create/extract with state persistence and `/hefesto.resume` support.

---

## 1. Descricao & User Story

"Como um **usuario de CLI de IA**, eu quero ter **comandos intuitivos** como `/hefesto.create` e `/hefesto.extract`, para que eu possa **criar e gerenciar skills** de forma simples e padronizada."

---

## 2. Regras de Negocio (RN)

* [RN01] Comandos DEVEM seguir padrao `/hefesto.<acao>`
* [RN02] Todos os comandos de escrita DEVEM passar por Human Gate
* [RN03] Comandos de leitura NAO requerem Human Gate
* [RN04] Comandos DEVEM suportar modo wizard (interativo) e direto (argumentos)
* [RN05] Feedback DEVE ser claro sobre sucesso/falha

---

## 3. Regras Tecnicas (RT)

* [RT01] (T0-HEFESTO-02) Human Gate obrigatorio para escrita
* [RT02] Comandos disponiveis:

| Comando | Descricao | Human Gate | Tipo |
|---------|-----------|------------|------|
| `/hefesto.create` | Criar skill de descricao | Sim | Escrita |
| `/hefesto.extract` | Extrair skill de codigo | Sim | Escrita |
| `/hefesto.validate` | Validar skill existente | Nao | Leitura |
| `/hefesto.adapt` | Adaptar para outro CLI | Sim | Escrita |
| `/hefesto.sync` | Sincronizar entre CLIs | Sim | Escrita |
| `/hefesto.list` | Listar skills | Nao | Leitura |
| `/hefesto.show` | Exibir skill especifica | Nao | Leitura |
| `/hefesto.delete` | Remover skill | Sim | Escrita |

* [RT03] Estrutura de comando:
  ```
  commands/
  ├── hefesto.create.md
  ├── hefesto.extract.md
  ├── hefesto.validate.md
  ├── hefesto.adapt.md
  ├── hefesto.sync.md
  ├── hefesto.list.md
  ├── hefesto.show.md
  └── hefesto.delete.md
  ```
* [RT04] Cada comando DEVE ter:
  - Descricao clara
  - Sintaxe de uso
  - Argumentos aceitos
  - Exemplos de uso
  - Fluxo de execucao

---

## 4. Requisitos de Qualidade (RQ)

* [RQ01] Tempo de resposta < 2s para comandos de leitura
* [RQ02] Mensagens de erro DEVEM ser acionaveis
* [RQ03] Help (`/hefesto.help`) DEVE estar sempre disponivel
* [RQ04] Comandos DEVEM ser auto-documentados

---

## 5. Criterios de Aceite

- [x] Todos os 9 comandos implementados (incluindo /hefesto.show e /hefesto.delete)
- [x] Human Gate funcionando para comandos de escrita
- [x] Modo wizard implementado para /hefesto.create
- [x] Modo wizard implementado para /hefesto.extract
- [x] Validacao de argumentos
- [x] Mensagens de erro claras
- [x] Help contextual para cada comando
- [x] Documentacao de cada comando

---

## 6. Tarefas (Sub-Cards)

- [x] CARD-003.1: Implementar /hefesto.create
- [x] CARD-003.2: Implementar /hefesto.extract
- [x] CARD-003.3: Implementar /hefesto.validate
- [x] CARD-003.4: Implementar /hefesto.adapt
- [x] CARD-003.5: Implementar /hefesto.sync
- [x] CARD-003.6: Implementar /hefesto.list
- [x] CARD-003.7: Implementar /hefesto.show
- [x] CARD-003.8: Implementar /hefesto.delete
- [x] CARD-003.9: Implementar /hefesto.help
- [x] CARD-003.10: Integrar Human Gate em comandos de escrita

---

## 7. Referencias

- T0-HEFESTO-02: Human Gate Obrigatorio
- AGENTS.md: Lista de comandos disponiveis
- .context/examples/command-example.md: Exemplo de fluxo

---

## 8. Metadata

| Campo | Valor |
|-------|-------|
| **Status** | ✅ COMPLETED (2026-02-05) |
| **Prioridade** | Alta |
| **Estimativa** | 12h |
| **Assignee** | AI Agent |
| **Dependencias** | CARD-001, CARD-002 |

---

**CARD-003** | Hefesto Skill Generator | Commands
