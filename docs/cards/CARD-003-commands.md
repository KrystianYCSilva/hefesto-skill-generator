# CARD-003: Commands - Comandos /hefesto.*

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

- [ ] Todos os 8 comandos implementados
- [ ] Human Gate funcionando para comandos de escrita
- [ ] Modo wizard implementado para /hefesto.create
- [ ] Modo wizard implementado para /hefesto.extract
- [ ] Validacao de argumentos
- [ ] Mensagens de erro claras
- [ ] Help contextual para cada comando
- [ ] Documentacao de cada comando

---

## 6. Tarefas (Sub-Cards)

- [ ] CARD-003.1: Implementar /hefesto.create
- [ ] CARD-003.2: Implementar /hefesto.extract
- [ ] CARD-003.3: Implementar /hefesto.validate
- [ ] CARD-003.4: Implementar /hefesto.adapt
- [ ] CARD-003.5: Implementar /hefesto.sync
- [ ] CARD-003.6: Implementar /hefesto.list
- [ ] CARD-003.7: Implementar /hefesto.show
- [ ] CARD-003.8: Implementar /hefesto.delete
- [ ] CARD-003.9: Implementar /hefesto.help
- [ ] CARD-003.10: Integrar Human Gate em comandos de escrita

---

## 7. Referencias

- T0-HEFESTO-02: Human Gate Obrigatorio
- AGENTS.md: Lista de comandos disponiveis
- .context/examples/command-example.md: Exemplo de fluxo

---

## 8. Metadata

| Campo | Valor |
|-------|-------|
| **Status** | Planned |
| **Prioridade** | Alta |
| **Estimativa** | 12h |
| **Assignee** | AI Agent |
| **Dependencias** | CARD-001, CARD-002 |

---

**CARD-003** | Hefesto Skill Generator | Commands
