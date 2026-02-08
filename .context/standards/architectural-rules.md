# Architectural Rules - T0 (Enforcement)

> **Tier:** T0 - ABSOLUTO
> **SEMPRE seguir estas regras. Sem excecoes.**
> **Versao:** 2.0.0
> **Fonte de verdade:** `CONSTITUTION.md` (raiz do projeto)

---

## T0-HEFESTO-01: Agent Skills Standard

**Regra:** TODA skill gerada DEVE seguir a especificacao [agentskills.io](https://agentskills.io).

**Frontmatter:** SOMENTE `name` + `description` (sem license, metadata, version, tags).

```yaml
# CORRETO
---
name: code-review
description: |
  Padroniza code reviews seguindo boas praticas.
  Use when: revisar PRs, avaliar codigo.
---

# PROIBIDO
---
name: Code-Review        # uppercase
description: ""          # vazio
license: MIT             # campo proibido
metadata:
  version: "1.0.0"       # campo proibido
---
```

---

## T0-HEFESTO-02: Human Gate Obrigatorio

**Regra:** NUNCA persistir skill sem aprovacao humana explicita.

```
1. Gerar skill em memoria
2. Auto-Critica: checklist 13 itens
3. Corrigir FAILs automaticamente
4. Apresentar preview ao usuario
5. Aguardar: [approve] [edit] [reject]
6. SO APOS aprovacao, persistir em TODOS CLIs detectados
```

---

## T0-HEFESTO-03: Progressive Disclosure

**Regra:** SKILL.md DEVE ter menos de 500 linhas e ~5000 tokens.

```
# CORRETO
skill/
├── SKILL.md       # < 500 linhas (core)
├── references/    # Docs extensas (JIT loaded)
└── scripts/       # Codigo executavel

# PROIBIDO
skill/
└── SKILL.md       # > 500 linhas (tudo junto)
```

---

## T0-HEFESTO-04: Nomenclatura Padrao

**Regra:** Campo `name` DEVE seguir formato especifico.

- Apenas lowercase (a-z), numeros (0-9), hyphens (-)
- Nao comecar/terminar com hyphen
- Sem hyphens consecutivos
- Max 64 caracteres
- Pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`

---

## T0-HEFESTO-05: Description Obrigatoria

**Regra:** Campo `description` DEVE ser preenchido (max 1024 chars) e incluir "Use when:" ou trigger equivalente.

```yaml
# CORRETO
description: |
  Padroniza code reviews seguindo boas praticas.
  Use when: revisar PRs, avaliar codigo.

# PROIBIDO
description: ""          # vazio
description: "skill"     # muito generico
```

---

## T0-HEFESTO-06: Deteccao Antes de Perguntar

**Regra:** SEMPRE detectar CLIs instalados ANTES de perguntar ao usuario.

1. Verificar CLIs no PATH (claude, gemini, codex, cursor, qwen, opencode)
2. Verificar diretorios de config existentes (.claude/, .gemini/, etc.)
3. Gerar para TODOS os CLIs detectados
4. SO SE nenhum detectado, perguntar

---

## T0-HEFESTO-07: Validacao Pre-Persistencia

**Regra:** TODA skill DEVE ser validada contra spec ANTES de persistir.

**Checklist 13 pontos:**

| Nivel | Qtd | Criterios |
|-------|-----|-----------|
| CRITICAL | 5 | Frontmatter valido, name format, description format, body < 500 linhas, "How to" sections |
| WARNING | 7 | Token economy, no tutorials, examples, progressive disclosure, anti-patterns, no body "When to Use", no README/CHANGELOG |
| INFO | 1 | Security (sem credenciais, tokens, PII) |

---

## T0-HEFESTO-08: Idempotencia

**Regra:** Operacoes DEVEM ser idempotentes.

- Se skill ja existe: perguntar [overwrite] [rename] [skip]
- Nunca sobrescrever silenciosamente

---

## T0-HEFESTO-09: Armazenamento Local

**Regra:** Skills DEVEM ser armazenadas no projeto atual por padrao.

```
# Diretorios por CLI
.claude/skills/<name>/SKILL.md
.gemini/skills/<name>/SKILL.md
.codex/skills/<name>/SKILL.md
.github/skills/<name>/SKILL.md
.opencode/skills/<name>/SKILL.md
.cursor/skills/<name>/SKILL.md
.qwen/skills/<name>/SKILL.md
```

---

## T0-HEFESTO-10: Citacao de Fontes

**Regra:** Skills tecnicas PODEM citar fontes quando relevante.

- Citar docs oficiais quando referenciadas diretamente
- Nao incluir URLs well-known obvias (MDN, Oracle docs)
- Fontes extensas em references/, nao no SKILL.md principal

---

## T0-HEFESTO-11: Seguranca por Padrao

**Regra:** Skills DEVEM ser projetadas com seguranca intrinseca.

**PROIBIDO:** Credenciais, tokens, secrets, PII, URLs internas/privadas.

---

## T0-HEFESTO-12: Auto-Critica Obrigatoria

**Regra:** O AI agent DEVE revisar seu proprio output antes de apresentar ao usuario.

1. Gerar skill
2. Rodar checklist de 13 itens (ver `templates/quality-checklist.md`)
3. Corrigir FAILs automaticamente
4. Documentar correcoes
5. SO ENTAO apresentar ao usuario no Human Gate

---

## T0-HEFESTO-13: Template Authority

**Regra:** Toda logica do Hefesto vive em templates Markdown. NUNCA em codigo executavel.

Os comandos em `.<cli>/commands/hefesto.*.md` (e equivalentes) sao a UNICA fonte de verdade para o comportamento do sistema.

**PROIBIDO:** Scripts Python/Node.js para logica do Hefesto, dependencias externas.

---

## Logica de Resolucao

```
IF T0 conflita com qualquer tier -> T0 VENCE SEMPRE
ALWAYS cite a regra especifica (ID) na resposta
ALWAYS validar ANTES de persistir
NEVER persistir sem Human Gate
```

---

**Ultima Atualizacao:** 2026-02-07 (v2.0.0 - 13 regras T0)
