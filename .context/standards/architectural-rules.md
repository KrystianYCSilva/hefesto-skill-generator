# Architectural Rules - T0 (Enforcement)

> **Tier:** T0 - ABSOLUTO
> **SEMPRE seguir estas regras. Sem excecoes.**

---

## T0-HEFESTO-01: Agent Skills Standard

**Regra:** TODA skill gerada DEVE seguir a especificacao [agentskills.io](https://agentskills.io).

```yaml
# CORRETO
---
name: code-review
description: |
  Padroniza code reviews seguindo boas praticas.
  Use quando: revisar PRs, avaliar codigo.
---

# PROIBIDO
---
Name: Code-Review    # uppercase
description: ""      # vazio
---
```

---

## T0-HEFESTO-02: Human Gate Obrigatorio

**Regra:** NUNCA persistir skill sem aprovacao humana explicita.

```
# CORRETO
1. Gerar skill em memoria
2. Apresentar preview ao usuario
3. Aguardar [approve], [expand], [edit], [reject]
4. SO APOS aprovacao, persistir

# PROIBIDO
1. Gerar skill
2. Salvar automaticamente  # NUNCA
```

---

## T0-HEFESTO-03: Progressive Disclosure

**Regra:** SKILL.md DEVE ter menos de 500 linhas e 5000 tokens.

```
# CORRETO
skill/
├── SKILL.md       # < 500 linhas (core)
├── references/    # Docs extensas aqui
└── scripts/       # Codigo executavel aqui

# PROIBIDO
skill/
└── SKILL.md       # > 500 linhas (tudo junto)
```

---

## T0-HEFESTO-04: Nomenclatura Padrao

**Regra:** Campo `name` DEVE seguir formato especifico.

```
# CORRETO
name: code-review
name: testing-strategy
name: api-docs-v2

# PROIBIDO
name: Code-Review        # uppercase
name: -testing           # comeca com hyphen
name: api--docs          # hyphens consecutivos
name: a                  # muito curto sem contexto
```

**Validacao:**
- Apenas lowercase (a-z)
- Apenas numeros (0-9)
- Apenas hyphens (-)
- Nao comecar/terminar com hyphen
- Sem hyphens consecutivos
- Max 64 caracteres

---

## T0-HEFESTO-05: Description Obrigatoria

**Regra:** Campo `description` DEVE ser preenchido e incluir "Use when:" ou similar.

```yaml
# CORRETO
description: |
  Padroniza code reviews seguindo boas praticas.
  Use quando: revisar PRs, avaliar codigo de terceiros.

# PROIBIDO
description: ""          # vazio
description: "skill"     # muito generico
```

---

## T0-HEFESTO-06: Deteccao Antes de Perguntar

**Regra:** SEMPRE detectar CLIs instalados ANTES de perguntar ao usuario.

```
# CORRETO
1. Verificar CLIs no PATH
2. Verificar diretorios de config
3. Gerar para TODOS detectados
4. SO SE nenhum detectado, perguntar

# PROIBIDO
1. Perguntar "Qual CLI voce usa?"  # NUNCA primeiro
```

---

## T0-HEFESTO-07: Validacao Pre-Persistencia

**Regra:** TODA skill DEVE ser validada contra spec ANTES de persistir.

**Checklist:**
- [ ] Frontmatter valido (name, description)
- [ ] Name conforme spec (lowercase, hyphens, max 64)
- [ ] Description nao vazia (max 1024 chars)
- [ ] SKILL.md < 500 linhas
- [ ] Sem informacoes sensiveis
- [ ] Recursos JIT em diretorios corretos

---

## T0-HEFESTO-08: Idempotencia

**Regra:** Operacoes DEVEM ser idempotentes.

```
# CORRETO (skill ja existe)
1. Detectar skill existente
2. Perguntar: [overwrite], [merge], [cancel]
3. Aguardar resposta
4. Executar acao escolhida

# PROIBIDO
1. Sobrescrever silenciosamente  # NUNCA
```

---

## T0-HEFESTO-09: Armazenamento Local

**Regra:** Skills DEVEM ser armazenadas no projeto atual por padrao.

```
# CORRETO (projeto atual)
./projeto/.claude/skills/code-review/SKILL.md
./projeto/.gemini/skills/code-review/SKILL.md

# GLOBAL (apenas se solicitado explicitamente)
~/.claude/skills/code-review/SKILL.md
```

---

## T0-HEFESTO-10: Citacao de Fontes

**Regra:** Skills tecnicas DEVEM citar fontes.

```yaml
# CORRETO
## References

- [Official Docs](https://...) - Acessado em 2026-02-04
- [Academic Paper](https://...) - Autor, Ano

# PROIBIDO
# Sem referencias para skill tecnica
```

---

## Logica de Resolucao

```
IF T0 conflita com qualquer tier → T0 VENCE SEMPRE
ALWAYS cite a regra especifica (ID) na resposta
ALWAYS validar ANTES de persistir
NEVER persistir sem Human Gate
```

---

**Ultima Atualizacao:** 2026-02-04
