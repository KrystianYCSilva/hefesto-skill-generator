# Development Workflows - Hefesto Skill Generator

> **Tier:** T2 - Informativo
> **Proposito:** Fluxos de trabalho para desenvolvimento e uso do Hefesto

---

## 1. Workflow: Criar Nova Skill

### 1.1. Via Descricao Natural

```
┌─────────────────────────────────────────────────────────────┐
│ INICIO: Usuario quer criar skill                            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 1: Descrever a skill                                  │
│                                                              │
│ /hefesto.create Uma skill para [descricao do que faz]        │
│                                                              │
│ Dicas:                                                       │
│ - Seja especifico sobre o proposito                          │
│ - Mencione padroes/frameworks se relevante                   │
│ - Inclua casos de uso principais                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 2: Revisar preview (Human Gate)                       │
│                                                              │
│ - Verificar name gerado                                      │
│ - Verificar description                                      │
│ - Verificar instrucoes                                       │
│                                                              │
│ Opcoes: [approve] [expand] [edit] [reject]                  │
└─────────────────────────────────────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          ▼                   ▼                   ▼
    [approve]            [expand]            [reject]
          │                   │                   │
          │                   ▼                   │
          │     ┌─────────────────────────────┐   │
          │     │ PASSO 2b: Wizard            │   │
          │     │ - Adicionar scripts?        │   │
          │     │ - Adicionar referencias?    │   │
          │     │ - Adicionar assets?         │   │
          │     └─────────────────────────────┘   │
          │                   │                   │
          └───────────────────┘                   │
                              │                   │
                              ▼                   │
┌─────────────────────────────────────────────────────────────┐
│ PASSO 3: Skill persistida                                   │
│                                                              │
│ CLIs detectados: Claude, Gemini                              │
│ Locais:                                                      │
│ - .claude/skills/{name}/SKILL.md                             │
│ - .gemini/skills/{name}/SKILL.md                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 4: Testar skill                                       │
│                                                              │
│ /{name}                                                      │
│ /{name} [argumentos se aplicavel]                            │
└─────────────────────────────────────────────────────────────┘
```

### 1.2. Via Extracao de Codigo

```
┌─────────────────────────────────────────────────────────────┐
│ INICIO: Usuario tem codigo com padroes uteis                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 1: Identificar arquivo(s) fonte                       │
│                                                              │
│ /hefesto.extract @src/utils/validation.ts                    │
│ /hefesto.extract @docs/coding-standards.md                   │
│ /hefesto.extract @src/components/ --pattern "*.tsx"          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 2: Analise automatica                                 │
│                                                              │
│ Hefesto analisa:                                             │
│ - Padroes de codigo                                          │
│ - Convencoes                                                 │
│ - Boas praticas                                              │
│ - Comentarios/documentacao                                   │
│                                                              │
│ Gera SKILL.md com instrucoes derivadas                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 3: Human Gate (como workflow anterior)                │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Workflow: Validar Skill Existente

```
┌─────────────────────────────────────────────────────────────┐
│ INICIO: Usuario quer validar skill                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 1: Executar validacao                                 │
│                                                              │
│ /hefesto.validate code-review                                │
│ /hefesto.validate .claude/skills/code-review/SKILL.md        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 2: Revisar relatorio                                  │
│                                                              │
│ ## Validacao: code-review                                    │
│                                                              │
│ ### Estrutura                                                │
│ ✅ SKILL.md presente                                         │
│ ✅ Frontmatter valido                                        │
│ ✅ 87 linhas (< 500)                                         │
│                                                              │
│ ### Agent Skills Spec                                        │
│ ✅ name conforme                                             │
│ ✅ description conforme                                      │
│                                                              │
│ ### Qualidade                                                │
│ ✅ Description acionavel                                     │
│ ✅ Instrucoes claras                                         │
│ ⚠️ Warning: Considerar adicionar mais exemplos               │
│                                                              │
│ **Resultado:** APROVADA ✅                                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 3 (se erros): Corrigir                                │
│                                                              │
│ /hefesto.edit code-review                                    │
│ [Corrigir problemas apontados]                               │
│ /hefesto.validate code-review                                │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Workflow: Sincronizar Entre CLIs

```
┌─────────────────────────────────────────────────────────────┐
│ INICIO: Skill existe em um CLI, precisa em outros           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 1: Executar sincronizacao                             │
│                                                              │
│ /hefesto.sync code-review                                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 2: Revisar status                                     │
│                                                              │
│ ## Sincronizacao: code-review                                │
│                                                              │
│ | CLI | Status | Acao |                                      │
│ |-----|--------|------|                                      │
│ | Claude | ✅ Existe | Origem |                              │
│ | Gemini | ❌ Nao existe | Criar |                           │
│ | Codex | ❌ Nao existe | Criar |                            │
│                                                              │
│ Criar skill em 2 CLIs?                                       │
│ [yes] [no] [select]                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 3: Confirmar e executar                               │
│                                                              │
│ [yes] selecionado                                            │
│                                                              │
│ Criando em Gemini CLI... ✅                                  │
│ Criando em Codex... ✅                                       │
│                                                              │
│ Sincronizacao concluida!                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Workflow: Adaptar para CLI Especifico

```
┌─────────────────────────────────────────────────────────────┐
│ INICIO: Skill precisa de adaptacao para CLI especifico      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 1: Identificar skill e CLI alvo                       │
│                                                              │
│ /hefesto.adapt code-review --target gemini                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 2: Revisar adaptacoes                                 │
│                                                              │
│ ## Adaptacao: code-review → Gemini CLI                       │
│                                                              │
│ ### Transformacoes Aplicadas                                 │
│ - $ARGUMENTS → {{args}}                                      │
│                                                              │
│ ### Preview                                                  │
│ [Skill adaptada]                                             │
│                                                              │
│ [approve] [edit] [reject]                                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│ PASSO 3: Persistir                                          │
│                                                              │
│ Skill adaptada salva em:                                     │
│ .gemini/skills/code-review/SKILL.md                          │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Workflow: Listar Skills

```
/hefesto.list

## Skills do Projeto

| Skill | CLIs | Versao | Ultima Atualizacao |
|-------|------|--------|-------------------|
| code-review | Claude, Gemini | 1.0.0 | 2026-02-04 |
| conventional-commits | Claude | 1.0.0 | 2026-02-04 |
| testing-strategy | Claude, Gemini, Codex | 1.2.0 | 2026-02-03 |

### Detalhes

- **Total:** 3 skills
- **CLIs cobertos:** Claude (3), Gemini (2), Codex (1)

### Comandos

- `/hefesto.validate <skill>` - Validar skill
- `/hefesto.sync <skill>` - Sincronizar entre CLIs
- `/hefesto.edit <skill>` - Editar skill
```

---

## 6. Comandos Rapidos

| Acao | Comando |
|------|---------|
| Criar skill | `/hefesto.create <descricao>` |
| Extrair de codigo | `/hefesto.extract @arquivo` |
| Validar skill | `/hefesto.validate <name>` |
| Sincronizar CLIs | `/hefesto.sync <name>` |
| Adaptar para CLI | `/hefesto.adapt <name> --target <cli>` |
| Listar skills | `/hefesto.list` |
| Ajuda | `/hefesto.help` |

---

**Ultima Atualizacao:** 2026-02-04
