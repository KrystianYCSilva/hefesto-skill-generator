# Exemplo: Fluxo de Comando /hefesto.create

> **Tier:** T3 - Ilustrativo
> **Proposito:** Demonstrar fluxo completo do comando /hefesto.create (v2.0.0)

---

## 1. Input do Usuario

```
/hefesto.create Uma skill para padronizar commits seguindo conventional commits
```

---

## 2. Processamento (6 fases)

### Phase 1: Understanding

```
Input: "Uma skill para padronizar commits seguindo conventional commits"

Conceitos Extraidos:
- Dominio: Git/Version Control
- Acao: Padronizar commits
- Padrao: Conventional Commits
- Tipo: Workflow
```

### Phase 2: Research

```
Templates carregados:
- templates/skill-template.md
- templates/quality-checklist.md
- templates/cli-compatibility.md
```

### Phase 3: Generation

```yaml
---
name: conventional-commits
description: |
  Padroniza mensagens de commit seguindo a especificacao Conventional Commits.
  Use when: criar commits, revisar historico, gerar changelogs automaticos.
---

# Conventional Commits

Skill para criar mensagens de commit padronizadas e semanticas.

## How to identify change type

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

## How to write a commit message

Formato:

<tipo>(<escopo>): <descricao>

[corpo opcional]

[footer opcional]

Exemplos:

feat(auth): add login with Google OAuth
fix(api): handle null response from external service

## How to validate a commit

Checklist:
- [ ] Tipo correto (feat/fix/docs/etc.)
- [ ] Descricao em imperativo ("add" nao "added")
- [ ] Descricao < 72 caracteres
- [ ] Corpo explica "por que" (se necessario)
```

### Phase 4: Auto-Critica (13 pontos)

```
CRITICAL:
  [PASS] Frontmatter: SOMENTE name + description
  [PASS] Name: "conventional-commits" (20 chars, conforme)
  [PASS] Description: 130 chars, com "Use when:"
  [PASS] Body: 45 linhas (< 500)
  [PASS] Secoes "How to [task]"

WARNING:
  [PASS] Token economy (nao ensina Git basico)
  [PASS] Sem tutorials
  [PASS] Exemplos presentes (non-obvious patterns)
  [PASS] Progressive disclosure (< 200 linhas)
  [PASS] Sem anti-patterns
  [PASS] Sem "When to Use" no body
  [PASS] Sem README/CHANGELOG

INFO:
  [PASS] Sem credenciais, tokens, PII

Resultado: PASS (13/13)
```

### Phase 5: Human Gate

```
## Skill Gerada: conventional-commits

### Preview
[Conteudo do SKILL.md acima]

### Auto-Critica: PASS (13/13)

### CLIs Detectados
- Claude Code (.claude/ encontrado)
- Gemini CLI (gemini no PATH)

### Opcoes
- [approve] - Salvar skill em Claude Code e Gemini CLI
- [edit] - Modificar antes de salvar
- [reject] - Cancelar operacao
```

### Phase 6: Persistence (apos [approve])

```
Salvando em CLIs detectados...

Claude Code:
  .claude/skills/conventional-commits/SKILL.md

Gemini CLI:
  .gemini/skills/conventional-commits/SKILL.md

Skill criada com sucesso em 2 CLIs.
```

---

## 3. Resumo do Fluxo

```
/hefesto.create <descricao>
        |
        v
Phase 1: Understanding  -> Extrair conceitos
Phase 2: Research        -> Ler templates
Phase 3: Generation      -> Gerar SKILL.md
Phase 4: Auto-Critica    -> 13-point checklist
Phase 5: Human Gate      -> [approve] [edit] [reject]
Phase 6: Persistence     -> Escrever em TODOS CLIs
```

---

**Ultima Atualizacao:** 2026-02-07 (v2.0.0)


