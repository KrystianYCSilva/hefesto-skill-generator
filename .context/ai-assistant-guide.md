# AI Assistant Guide - Hefesto Skill Generator

> **Versao:** 2.2.0
> **Para:** Todas as IAs (Claude, Copilot, Gemini, Cursor, etc.)

---

## 1. Bootstrap Sequence

```
STEP 1: Carregar este arquivo
STEP 2: Carregar templates/ (skill-template, quality-checklist, cli-compatibility)
STEP 3: Verificar .hefesto/version para instalacao
STEP 4: Carregar contexto adicional conforme necessidade (JIT)
```

---

## 2. Request Classification

| Tipo de Request | Arquivos para Carregar | Acao |
|-----------------|------------------------|------|
| `/hefesto.create` | templates/, skills exemplares | Gerar skill + Human Gate |
| `/hefesto.extract` | templates/, codigo alvo | Analisar + Gerar + Human Gate |
| `/hefesto.validate` | templates/quality-checklist.md | Validar + corrigir (fix-auto) |
| `/hefesto.init` | .hefesto/version | Verificar/bootstrap instalacao |
| `/hefesto.list` | .<cli>/skills/ | Listar skills |

---

## 3. Human Gate Protocol

**REGRA:** NUNCA persistir sem aprovacao humana.

### Fluxo

```
1. Gerar conteudo em memoria
2. Apresentar ao usuario com preview
3. Mostrar opcoes: [approve] [edit] [reject]
4. Aguardar resposta explicita
5. SO APOS aprovacao, persistir em TODOS os CLIs detectados
```

---

## 4. Agent Skills Spec (Referencia Rapida)

### Frontmatter

```yaml
---
name: skill-id          # max 64 chars, lowercase, hyphens, regex: ^[a-z0-9]+(-[a-z0-9]+)*$
description: |          # max 1024 chars, nao vazio
  Action verb describing what the skill does.
  Use when: specific trigger condition.
---
```

**SOMENTE `name` + `description`** - sem license, metadata, version, tags.

### Body Pattern

```markdown
# Skill Title

Brief introduction.

## How to <first capability>

Task-oriented instructions.

## How to <second capability>

More instructions.
```

**Secoes "How to [task]"** - nao "Instructions > Step N" ou "When to Use".

### Quality Rules

- **Frontmatter strict**: ONLY name + description
- **Token Economy**: basic concepts = 1 sentence; advanced = full section
- **No tutorials**: don't teach what the AI already knows
- **No body "When to Use"**: trigger info lives in description only
- **Progressive Disclosure**: references/ if SKILL.md > 200 lines
- **Anti-patterns**: compatibility tables, version footers, license footers
- **Size limit**: < 500 lines, < ~5000 tokens

---

## 5. Deteccao de CLIs

### Diretorios por CLI

| CLI | Skills Dir | Commands Dir | Variable Syntax |
|-----|-----------|-------------|-----------------|
| Claude Code | `.claude/skills/` | `.claude/commands/` | `$ARGUMENTS` |
| Gemini CLI | `.gemini/skills/` | `.gemini/commands/` | `{{args}}` |
| OpenAI Codex | `.codex/skills/` | `.codex/prompts/` | `$ARGUMENTS` |
| VS Code/Copilot | `.github/skills/` | `.github/agents/` + `prompts/` | `$ARGUMENTS` |
| OpenCode | `.opencode/skills/` | `.opencode/command/` | `$ARGUMENTS` |
| Cursor | `.cursor/skills/` | `.cursor/commands/` | `$ARGUMENTS` |
| Qwen Code | `.qwen/skills/` | `.qwen/commands/` | `{{args}}` |

### Deteccao `.github/` (Copilot)

So tratar como Copilot se:
- `github-copilot` no PATH, OU
- `.github/copilot-instructions.md` existir, OU
- `.github/agents/` existir

---

## 6. Checklist de Qualidade (13 pontos)

| Nivel | Criterios |
|-------|-----------|
| **CRITICAL** (5) | Frontmatter valido, name format, description format, body < 500 lines, "How to" sections |
| **WARNING** (7) | Token economy, no tutorials, examples, progressive disclosure, anti-patterns, no body "When to Use", no README/CHANGELOG |
| **INFO** (1) | Security (sem credenciais, tokens, PII) |

---

## 7. Definition of Done

### Para Skills Geradas

- [ ] Frontmatter: SOMENTE name + description
- [ ] SKILL.md < 500 linhas
- [ ] Secoes "How to [task]"
- [ ] Auto-critica 13 pontos PASS
- [ ] Human Gate aprovado
- [ ] Persistido em TODOS os CLIs detectados

---

## 8. Comandos Disponiveis

| Comando | Descricao | Human Gate |
|---------|-----------|------------|
| `/hefesto.create "desc"` | Criar skill de descricao | Sim |
| `/hefesto.extract arquivo` | Extrair skill de codigo | Sim |
| `/hefesto.validate skill-name` | Validar + corrigir skill | Sim (fix-auto) |
| `/hefesto.init` | Bootstrap/verificar instalacao | Nao |
| `/hefesto.list` | Listar skills | Nao |

---

## 9. Erros Comuns

| Erro | Causa | Solucao |
|------|-------|---------|
| "Invalid skill name" | Uppercase ou caracteres invalidos | Usar lowercase e hyphens |
| "Description too long" | Mais de 1024 chars | Resumir descricao |
| "SKILL.md too large" | Mais de 500 linhas | Mover para references/ |
| "No CLI detected" | Nenhum CLI instalado | Perguntar ao usuario |

---

**AI Assistant Guide** | Hefesto Skill Generator v2.0.0 | 2026-02-07



