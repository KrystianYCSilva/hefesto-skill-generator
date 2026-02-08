# Testing Strategy - T1 (Normativo)

> **Tier:** T1 - NORMATIVO
> **Estrategia de validacao para skills geradas.**
> **Versao:** 2.0.0

---

## 1. Niveis de Validacao

### 1.1. Validacao de Estrutura (Automatica)

**Quando:** Sempre, antes de Human Gate

**Checklist:**
- [ ] Arquivo SKILL.md existe
- [ ] Frontmatter YAML valido
- [ ] Campo `name` presente e valido
- [ ] Campo `description` presente e nao vazio
- [ ] Frontmatter contem SOMENTE `name` + `description`
- [ ] SKILL.md < 500 linhas
- [ ] Diretorios JIT corretos (scripts/, references/, assets/)

### 1.2. Validacao de Spec (Automatica)

**Quando:** Apos validacao de estrutura

**Checklist Agent Skills:**
- [ ] `name`: max 64 chars
- [ ] `name`: apenas lowercase, numeros, hyphens
- [ ] `name`: nao comeca/termina com hyphen
- [ ] `name`: sem hyphens consecutivos
- [ ] `description`: max 1024 chars
- [ ] `description`: nao vazio, com "Use when:" trigger

### 1.3. Validacao de Qualidade (13 pontos)

**Quando:** Apos validacoes automaticas, antes de Human Gate

| Nivel | Qtd | Criterios |
|-------|-----|-----------|
| CRITICAL | 5 | Frontmatter valido, name format, description format, body < 500 linhas, "How to" sections |
| WARNING | 7 | Token economy, no tutorials, examples, progressive disclosure, anti-patterns, no body "When to Use", no README/CHANGELOG |
| INFO | 1 | Security (sem credenciais, tokens, PII) |

### 1.4. Human Gate

**Quando:** Apos auto-critica

**Apresentar ao usuario:**
- Preview completo da skill
- Resultado da auto-critica (13 pontos)
- Opcoes: [approve] [edit] [reject]

---

## 2. Criterios de Aprovacao

| Criterio | Obrigatorio |
|----------|-------------|
| Frontmatter valido (SOMENTE name + description) | Sim |
| Name conforme spec | Sim |
| Description acionavel com "Use when:" | Sim |
| Body com secoes "How to [task]" | Sim |
| < 500 linhas | Sim |
| Auto-critica 13 pontos PASS ou PARTIAL | Sim |
| Human Gate aprovado | Sim |

---

## 3. Validacao via /hefesto.validate

O comando `/hefesto.validate` roda validacao completa com capacidade de correcao:

```
1. Ler SKILL.md da skill alvo
2. Rodar checklist 13 pontos
3. Classificar: PASS | PARTIAL (warnings) | FAIL (criticals)
4. Se FAIL ou PARTIAL:
   - Diagnostico detalhado com sugestoes
   - Opcoes: [fix-auto] [fix-manual] [skip]
   - fix-auto: gerar versao corrigida -> Human Gate -> persistir
5. Se PASS: reportar sucesso
```

---

## 4. Validacao por CLI

### 4.1. Universal (todos os CLIs)

```yaml
---
name: valid-name
description: |
  Descricao valida. Use when: trigger.
---

# Skill Title

## How to <capability>
...
```

### 4.2. Especifica

**Gemini/Qwen:** Verificar conversao `$ARGUMENTS` -> `{{args}}`
**Copilot:** Verificar diretorio `.github/skills/`

---

## 5. Erros de Validacao

### 5.1. Erros Criticos (Bloqueantes)

| Erro | Causa | Acao |
|------|-------|------|
| `INVALID_NAME` | Name fora do padrao | Bloquear, sugerir correcao |
| `EMPTY_DESCRIPTION` | Description vazio | Bloquear, solicitar preenchimento |
| `INVALID_YAML` | Frontmatter malformado | Bloquear, mostrar erro |
| `FILE_TOO_LARGE` | > 500 linhas | Bloquear, sugerir split |
| `FORBIDDEN_FIELDS` | Frontmatter com campos alem de name/description | Bloquear, remover campos |

### 5.2. Warnings (Nao Bloqueantes)

| Warning | Causa | Acao |
|---------|-------|------|
| `STEP_PATTERN` | Usa "Step N" ao inves de "How to" | Avisar, sugerir refatoracao |
| `BODY_WHEN_TO_USE` | "When to Use" no body | Avisar, mover para description |
| `TUTORIAL_CONTENT` | Ensina conceitos basicos | Avisar, sugerir remocao |
| `ANTI_PATTERN` | Tabelas compatibilidade, footers | Avisar, sugerir remocao |

---

## 6. Formato de Reporte

### Sucesso

```
## Validacao: PASS

- [x] Frontmatter: SOMENTE name + description
- [x] Name: `code-review` (11 chars, conforme)
- [x] Description: 142 chars, com "Use when:"
- [x] Body: 87 linhas, secoes "How to"
- [x] Auto-critica: 13/13 PASS
```

### Falha

```
## Validacao: FAIL

### CRITICAL (bloqueantes)
- FORBIDDEN_FIELDS: Frontmatter contem `license`, `metadata`
  -> Remover campos extras, manter SOMENTE name + description

### WARNING
- STEP_PATTERN: Usa "Step 1:", "Step 2:" ao inves de "How to"
  -> Refatorar para secoes "How to [task]"

### Opcoes
- [fix-auto] Aplicar correcoes automaticamente
- [fix-manual] Corrigir manualmente
- [skip] Ignorar
```

---

**Ultima Atualizacao:** 2026-02-07 (v2.0.0)
