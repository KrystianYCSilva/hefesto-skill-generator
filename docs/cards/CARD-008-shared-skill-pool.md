# CARD-008: Shared Skill Pool - Fonte Canônica em .hefesto/skills/

## 1. Descricao & User Story

"Como um **desenvolvedor que mantém skills distribuídas em 6+ CLIs**, eu quero que exista uma **fonte canônica única** para cada skill, e que o `hefesto.sync` distribua versões adaptadas para cada CLI automaticamente, para que eu **nunca edite a mesma skill em dois lugares diferentes**."

---

## 2. Contexto e Motivação

Atualmente cada skill é copiada byte-identical para todos os CLIs detectados:

```
.claude/skills/kotlin-fundamentals/   ← cópia 1
.gemini/skills/kotlin-fundamentals/   ← cópia 2
.codex/skills/kotlin-fundamentals/    ← cópia 3
.opencode/skills/kotlin-fundamentals/ ← cópia 4
.cursor/skills/kotlin-fundamentals/   ← cópia 5
.qwen/skills/kotlin-fundamentals/     ← cópia 6
```

**Dados atuais (2026-02-05):**

| Métrica | Valor |
|---------|-------|
| Skills existentes | 3 |
| CLIs ativo | 6 |
| Cópias no disco | 18 diretórios |
| Conteúdo único | 235.471 bytes |
| Total no disco | 1.412.826 bytes (6x) |

Na escala atual (1,35 MB) isso não é problema. Mas quando skills crescerem para 50+, editar uma referência ou corrigir um erro exige abrir a mesma skill em 6 diretórios. O risco de drift silencioso entre copias cresce linearmente com o número de skills.

**Alternativa descartada:** SKILL.md "thin" em cada CLI apontando para a skill completa residente em outro CLI. Não funciona porque:
- Todos os CLIs resolvem `./references/*.md` relativo à posição física do próprio SKILL.md
- Nenhum CLI suporta "seguir ponteiro" para diretório alheio
- Viola T0-HEFESTO-05 (Armazenamento Local)

---

## 3. Regras de Negocio (RN)

* [RN01] DEVE existir um diretório `.hefesto/skills/` como fonte canônica de todas as skills
* [RN02] Cada skill no pool DEVE ter uma versão "clean" sem adaptações CLI-específicas
* [RN03] O `hefesto.sync` DEVE ser o único mecanismo para distribuir skills do pool para os CLIs
* [RN04] Edições DEVEM ser feitas na fonte canônica; as copias nos CLIs são output do sync
* [RN05] O pool DEVE coexistir com as copias existentes nos CLIs (não é breaking change)

---

## 4. Regras Tecnicas (RT)

* [RT01] (T0-HEFESTO-05) Cada CLI mantém sua cópia completa em `.CLI/skills/<name>/` — isolamento preservado
* [RT02] (T0-HEFESTO-09) O sync aplica adaptações por CLI antes de distribuir:
  - Gemini/Qwen: `$ARGUMENTS` → `{{args}}`
  - Futuras adaptações definidas em `metadata.yaml` por skill
* [RT03] Estrutura do pool:
  ```
  .hefesto/
  └── skills/
      ├── kotlin-fundamentals/
      │   ├── SKILL.md
      │   ├── metadata.yaml
      │   └── references/
      ├── markdown-fundamentals/
      │   ├── SKILL.md
      │   ├── metadata.yaml
      │   └── references/
      └── java-fundamentals/
          ├── SKILL.md
          ├── metadata.yaml
          └── references/
  ```
* [RT04] O `hefesto.sync` atualizado DEVE:
  1. Ler a skill da fonte canônica (`.hefesto/skills/<name>/`)
  2. Aplicar adaptações de T0-HEFESTO-09 para cada CLI alvo
  3. Comparar com a cópia existente no CLI (diff)
  4. Atualizar apenas se houver diferença (idempotência — T0-HEFESTO-08)
  5. Reportar: `[unchanged]`, `[updated]`, `[new]` por CLI
* [RT05] O `hefesto.create` atualizado DEVE persistir a skill no pool PRIMEIRO, depois disparar sync
* [RT06] Migração das skills existentes: mover copias de um CLI para o pool, executar sync para recriar nos outros

---

## 5. Requisitos de Qualidade (RQ)

* [RQ01] Sync DEVE ser idempotente — executar duas vezes com mesmo estado produz mesmo resultado
* [RQ02] Diff granular — sync atualiza apenas arquivos que mudaram, não o diretório inteiro
* [RQ03] Report claro do estado pós-sync por CLI (unchanged / updated / new / error)
* [RQ04] Falha em um CLI NAO deve bloquear sync dos outros (fault tolerance)
* [RQ05] Pool DEVE ser incluído no versionamento (git) junto com o resto do projeto

---

## 6. Criterios de Aceite

- [ ] Diretório `.hefesto/skills/` criado e populado com as 3 skills existentes
- [ ] `hefesto.create` persiste no pool antes de distribuir
- [ ] `hefesto.sync` lê do pool e distribui para todos os CLIs detectados
- [ ] Adaptações T0-HEFESTO-09 aplicadas corretamente durante o sync
- [ ] Sync idempotente — segunda execução sem mudanças retorna `[unchanged]` em todos os CLIs
- [ ] Report de status por CLI funcionando
- [ ] Skills nos CLIs funcionam exatamente como antes após migração
- [ ] Documentação do fluxo atualizada no hefesto.help

---

## 7. Tarefas (Sub-Cards)

- [ ] CARD-008.1: Criar estrutura `.hefesto/skills/` e migrar skills existentes
- [ ] CARD-008.2: Atualizar `hefesto.create` para persistir no pool primeiro
- [ ] CARD-008.3: Implementar adaptação T0-HEFESTO-09 no sync (substitution layer)
- [ ] CARD-008.4: Atualizar `hefesto.sync` para ler do pool e distribuir com diff granular
- [ ] CARD-008.5: Implementar report de status pós-sync
- [ ] CARD-008.6: Testes de idempotência e fault tolerance
- [ ] CARD-008.7: Atualizar hefesto.help com documentação do pool

---

## 8. Referencias

- T0-HEFESTO-05: Armazenamento Local (isolamento por CLI preservado)
- T0-HEFESTO-08: Idempotência (sync não deve sobrescrever sem necessidade)
- T0-HEFESTO-09: Compatibilidade CLI (adaptações aplicadas no sync)
- CARD-003: Commands (hefesto.create e hefesto.sync são comandos existentes)
- CARD-004: Multi-CLI Generator (detecção de CLIs usada pelo sync)
- Análise arquitetural: "Thin SKILL.md" descartado — ver sessão 2026-02-05

---

## 9. Metadata

| Campo | Valor |
|-------|-------|
| **Status** | Planned |
| **Prioridade** | Média (não urgente na escala atual) |
| **Estimativa** | 10h |
| **Assignee** | AI Agent |
| **Dependencias** | CARD-003 (comandos), CARD-004 (multi-CLI) |
| **Trigger** | Skills no projeto superarem ~50 unidades, ou drift silencioso entre CLIs ser reportado |

---

**CARD-008** | Hefesto Skill Generator | Shared Skill Pool
