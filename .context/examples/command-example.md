# Exemplo: Fluxo de Comando /hefesto.create

> **Tier:** T3 - Ilustrativo
> **Proposito:** Demonstrar fluxo completo do comando /hefesto.create

---

## 1. Input do Usuario

```
/hefesto.create Uma skill para padronizar commits seguindo conventional commits
```

---

## 2. Processamento (Template Processor)

### 2.1. Extracao de Conceitos

```
Input: "Uma skill para padronizar commits seguindo conventional commits"

Conceitos Extraidos:
- Dominio: Git/Version Control
- Acao: Padronizar commits
- Padrao: Conventional Commits
- Tipo: Workflow/Automation
```

### 2.2. Geracao de Name

```
Regras aplicadas:
- Lowercase
- Hyphens para espacos
- Max 64 chars
- Sem caracteres especiais

Resultado: "conventional-commits"
```

### 2.3. Geracao de Description

```yaml
description: |
  Padroniza mensagens de commit seguindo a especificacao Conventional Commits.
  Use quando: criar commits, revisar historico, gerar changelogs automaticos.
```

### 2.4. SKILL.md Gerado

```yaml
---
name: conventional-commits
description: |
  Padroniza mensagens de commit seguindo a especificacao Conventional Commits.
  Use quando: criar commits, revisar historico, gerar changelogs automaticos.
license: MIT
compatibility: Claude Code, Gemini CLI, Codex, OpenCode, Cursor, Qwen Code, VS Code/Copilot
metadata:
  author: user
  version: "1.0.0"
  created: 2026-02-04
  category: development
  tags: [git, commits, conventional-commits, version-control, changelog]
---

# Conventional Commits

> Padroniza mensagens de commit seguindo a especificacao Conventional Commits.

## When to Use

- ✅ Criar novos commits
- ✅ Revisar mensagens de commit existentes
- ✅ Gerar changelogs automaticos
- ✅ Padronizar commits de um time
- ❌ Historico de commits ja existente (refatorar pode quebrar referencias)

## Instructions

### Step 1: Identificar Tipo de Mudanca

Determine o tipo da mudanca:

| Tipo | Uso |
|------|-----|
| `feat` | Nova funcionalidade |
| `fix` | Correcao de bug |
| `docs` | Documentacao |
| `style` | Formatacao (sem mudanca de codigo) |
| `refactor` | Refatoracao |
| `test` | Testes |
| `chore` | Manutencao |

### Step 2: Identificar Escopo (Opcional)

Escopo indica area afetada:
- `feat(auth)`: Feature na area de autenticacao
- `fix(api)`: Fix na API
- `docs(readme)`: Documentacao do README

### Step 3: Escrever Mensagem

Formato:
```
<tipo>(<escopo>): <descricao>

[corpo opcional]

[footer opcional]
```

### Step 4: Validar

Checklist:
- [ ] Tipo correto
- [ ] Descricao em imperativo ("add" nao "added")
- [ ] Descricao < 72 caracteres
- [ ] Corpo explica "por que" (se necessario)

## Examples

### Exemplo 1: Feature Simples

```
feat(auth): add login with Google OAuth

Allows users to authenticate using their Google account.
Closes #123
```

### Exemplo 2: Bug Fix

```
fix(api): handle null response from external service

- Add null check before processing
- Return empty array instead of error
```

### Exemplo 3: Breaking Change

```
feat(api)!: change response format to JSON:API

BREAKING CHANGE: All endpoints now return JSON:API format.
Migration guide: docs/migration-v2.md
```

## References

- [Conventional Commits Spec](https://www.conventionalcommits.org/) - Especificacao oficial
- [commitlint](https://commitlint.js.org/) - Ferramenta de validacao

---

**Gerado por:** Hefesto Skill Generator v1.0.0
```

---

## 3. Validacao (Validate Engine)

### 3.1. Validacao de Estrutura

```
Checklist:
✅ Arquivo SKILL.md presente
✅ Frontmatter YAML valido
✅ Campo 'name' presente: "conventional-commits"
✅ Campo 'description' presente: 156 chars
✅ SKILL.md: 98 linhas (< 500)
✅ Sem diretorios JIT (skill simples)
```

### 3.2. Validacao de Spec

```
Agent Skills Spec:
✅ name: 20 chars (max 64)
✅ name: apenas lowercase e hyphens
✅ name: nao comeca/termina com hyphen
✅ name: sem hyphens consecutivos
✅ description: 156 chars (max 1024)
✅ description: nao vazio
```

### 3.3. Validacao de Qualidade

```
T1 Rules:
✅ Markdown bem formatado
✅ YAML frontmatter valido
✅ Description acionavel (tem "Use quando:")
✅ Instrucoes claras e sequenciais
✅ Exemplos presentes
✅ Referencias documentadas
⚠️ Warning: Considerar adicionar scripts/ para validacao automatica
```

---

## 4. Human Gate

### 4.1. Apresentacao ao Usuario

```markdown
## Skill Gerada: conventional-commits

### Preview

[Conteudo do SKILL.md acima]

### Validacao

✅ **Estrutura:** Valida
✅ **Agent Skills Spec:** Conforme
✅ **Qualidade:** Aprovada

### Warnings

⚠️ Considerar adicionar `scripts/validate-commit.sh` para validacao automatica

### CLIs Detectados

- ✅ Claude Code (.claude/ encontrado)
- ✅ Gemini CLI (gemini no PATH)

### Opcoes

- **[approve]** - Salvar skill em Claude Code e Gemini CLI
- **[expand]** - Adicionar scripts, referencias, assets
- **[edit]** - Modificar antes de salvar
- **[reject]** - Cancelar operacao

Sua escolha:
```

### 4.2. Usuario Seleciona [approve]

---

## 5. Multi-CLI Generator

### 5.1. Deteccao de CLIs

```
Verificando CLIs instalados...

✅ Claude Code
   - Comando: claude --version → v1.2.0
   - Diretorio: .claude/ existe

✅ Gemini CLI
   - Comando: gemini --version → v0.25.0
   - Diretorio: .gemini/ nao existe (sera criado)

❌ OpenAI Codex
   - Comando: codex --version → nao encontrado

❌ VS Code/Copilot
   - Diretorio: .github/ nao existe

Total: 2 CLIs detectados
```

### 5.2. Geracao para Claude Code

```
Criando: .claude/skills/conventional-commits/

Arquivos:
- .claude/skills/conventional-commits/SKILL.md ✅

Nenhuma adaptacao necessaria (formato nativo).
```

### 5.3. Geracao para Gemini CLI

```
Criando: .gemini/skills/conventional-commits/

Adaptacoes aplicadas:
- Nenhuma (skill nao usa $ARGUMENTS)

Arquivos:
- .gemini/skills/conventional-commits/SKILL.md ✅
```

---

## 6. Output Final

```markdown
## Skill Criada com Sucesso ✅

### conventional-commits

**Descrição:** Padroniza mensagens de commit seguindo Conventional Commits.

### Locais

| CLI | Caminho |
|-----|---------|
| Claude Code | `.claude/skills/conventional-commits/SKILL.md` |
| Gemini CLI | `.gemini/skills/conventional-commits/SKILL.md` |

### Uso

```
# Claude Code
/conventional-commits

# Gemini CLI
/conventional-commits
```

### Proximos Passos

1. Teste a skill com `/conventional-commits`
2. Considere adicionar scripts de validacao (`/hefesto.expand conventional-commits`)
3. Sincronize com outros CLIs se necessario (`/hefesto.sync conventional-commits`)
```

---

## 7. Resumo do Fluxo

```
/hefesto.create <descricao>
        │
        ▼
┌───────────────────┐
│ Template Processor│ → Extrai conceitos, gera SKILL.md
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Validate Engine   │ → Valida estrutura, spec, qualidade
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Human Gate        │ → Apresenta preview, aguarda decisao
└─────────┬─────────┘
          │ [approve]
          ▼
┌───────────────────┐
│ Multi-CLI Gen     │ → Detecta CLIs, adapta, salva
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Output            │ → Reporta resultado
└───────────────────┘
```

---

**Ultima Atualizacao:** 2026-02-04
