# CARD-005: Human Gate + Wizard - Controle Humano

## 1. Descricao & User Story

"Como um **usuario consciente de seguranca**, eu quero que o Hefesto **sempre me mostre** o que sera criado e **aguarde minha aprovacao**, para que eu tenha **controle total** sobre o que e persistido no meu projeto."

---

## 2. Regras de Negocio (RN)

* [RN01] TODA operacao de escrita DEVE passar por Human Gate
* [RN02] Preview DEVE mostrar EXATAMENTE o que sera criado
* [RN03] Usuario DEVE ter opcoes: `[approve]`, `[expand]`, `[edit]`, `[reject]`
* [RN04] Wizard DEVE guiar usuario passo-a-passo quando necessario
* [RN05] Expansao DEVE permitir adicionar recursos JIT iterativamente

---

## 3. Regras Tecnicas (RT)

* [RT01] (T0-HEFESTO-02) NUNCA persistir sem aprovacao explicita
* [RT02] Fluxo Human Gate:
  ```
  1. Gerar skill em memoria (nao persistir)
  2. Validar contra Agent Skills spec
  3. Apresentar preview formatado ao usuario
  4. Aguardar resposta:
     - [approve] -> Persistir
     - [expand]  -> Adicionar recursos JIT
     - [edit]    -> Permitir edicao inline
     - [reject]  -> Descartar e informar
  5. SO APOS aprovacao, persistir
  6. Confirmar persistencia ao usuario
  ```
* [RT03] Formato do Preview:
  ```markdown
  ## Preview: Skill "{{name}}"
  
  ### Arquivos a serem criados:
  - .claude/skills/{{name}}/SKILL.md ({{lines}} linhas)
  - .gemini/skills/{{name}}/SKILL.md ({{lines}} linhas)
  
  ### Conteudo SKILL.md:
  ```yaml
  ---
  name: {{name}}
  description: {{description}}
  ---
  ```
  [corpo truncado se > 50 linhas]
  
  ### Acoes:
  [approve] [expand] [edit] [reject]
  ```
* [RT04] Wizard Mode (para /hefesto.create):
  ```
  Passo 1: Nome da skill (validar T0-HEFESTO-07)
  Passo 2: Descricao (validar max 1024 chars)
  Passo 3: Corpo principal (instrucoes)
  Passo 4: Recursos JIT? (scripts, references, assets)
  Passo 5: Review e Human Gate
  ```
* [RT05] (T0-HEFESTO-08) Se skill existe: `[overwrite]`, `[merge]`, `[cancel]`

---

## 4. Requisitos de Qualidade (RQ)

* [RQ01] Preview DEVE ser legivel em terminal 80 colunas
* [RQ02] Wizard DEVE permitir voltar passos (`back`)
* [RQ03] Timeout de Human Gate: 5 minutos (cancelar automatico)
* [RQ04] Mensagens DEVEM ser claras sobre consequencias

---

## 5. Criterios de Aceite

- [ ] Human Gate funcional para todos comandos de escrita
- [ ] Preview mostra conteudo exato a ser criado
- [ ] Opcoes [approve], [expand], [edit], [reject] funcionando
- [ ] Wizard mode implementado para /hefesto.create
- [ ] Wizard mode implementado para /hefesto.extract
- [ ] Expansao JIT iterativa funcionando
- [ ] Tratamento de skill existente ([overwrite], [merge], [cancel])
- [ ] Timeout implementado
- [ ] Mensagens de confirmacao apos persistencia

---

## 6. Tarefas (Sub-Cards)

- [ ] CARD-005.1: Implementar geracao em memoria (sem persistencia)
- [ ] CARD-005.2: Implementar validacao pre-persistencia
- [ ] CARD-005.3: Implementar formatador de preview
- [ ] CARD-005.4: Implementar handler de aprovacao
- [ ] CARD-005.5: Implementar handler de expansao
- [ ] CARD-005.6: Implementar handler de edicao inline
- [ ] CARD-005.7: Implementar handler de rejeicao
- [ ] CARD-005.8: Implementar wizard /hefesto.create
- [ ] CARD-005.9: Implementar wizard /hefesto.extract
- [ ] CARD-005.10: Implementar tratamento skill existente
- [ ] CARD-005.11: Implementar timeout

---

## 7. Referencias

- T0-HEFESTO-02: Human Gate Obrigatorio
- T0-HEFESTO-06: Validacao Spec
- T0-HEFESTO-08: Idempotencia
- .context/examples/command-example.md: Exemplo de fluxo

---

## 8. Metadata

| Campo | Valor |
|-------|-------|
| **Status** | Planned |
| **Prioridade** | Alta |
| **Estimativa** | 10h |
| **Assignee** | AI Agent |
| **Dependencias** | CARD-001, CARD-002, CARD-003 |

---

**CARD-005** | Hefesto Skill Generator | Human Gate + Wizard
