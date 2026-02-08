# Code Quality Standards - T1 (Normativo)

> **Tier:** T1 - NORMATIVO
> **Seguir estas regras como padrao.**
> **Versao:** 2.0.0

---

## T1-QUALITY-01: Markdown Bem Formatado

**Regra:** Todo Markdown DEVE ser bem formatado.

- Headers hierarquicos (H1 > H2 > H3)
- Listas consistentes
- Blocos de codigo com linguagem especificada
- Tabelas alinhadas
- Links funcionais

---

## T1-QUALITY-02: Frontmatter Minimo

**Regra:** Frontmatter DEVE conter SOMENTE `name` + `description`.

```yaml
# CORRETO (v2.0.0)
---
name: code-review
description: |
  Padroniza code reviews seguindo boas praticas SOLID.
  Use when: revisar PRs, avaliar codigo.
---

# PROIBIDO
---
name: code-review
description: "..."
license: MIT                    # NAO permitido
compatibility: Claude Code      # NAO permitido
metadata:
  version: "1.0.0"             # NAO permitido
  tags: [code-review]          # NAO permitido
---
```

---

## T1-QUALITY-03: Descricoes Acionaveis

**Regra:** Description DEVE ser acionavel com "Use when:" ou trigger equivalente.

```yaml
# CORRETO
description: |
  Padroniza code reviews seguindo boas praticas SOLID.
  Use when: revisar PRs, avaliar codigo de terceiros, onboarding.

# PROIBIDO
description: Uma skill para code review.  # Nao acionavel
```

---

## T1-QUALITY-04: Body Pattern "How to [task]"

**Regra:** O body DEVE usar secoes "How to [task]", NAO "Instructions > Step N".

```markdown
# CORRETO (v2.0.0)

## How to review a Pull Request

Leia o codigo alvo e identifique:
- Linguagem e framework
- Padrao arquitetural
- Presenca de testes

## How to apply SOLID checklist

Verifique cada principio...

# PROIBIDO

## Instructions

### Step 1: Analisar Contexto
### Step 2: Aplicar Checklist
```

---

## T1-QUALITY-05: Token Economy

**Regra:** Calibrar profundidade pelo nivel de conceito.

| Nivel | Tratamento |
|-------|------------|
| Basico (AI ja sabe) | 1 frase |
| Intermediario | 1 paragrafo + exemplo |
| Avancado/project-specific | Secao completa + references/ |

**PROIBIDO:** Ensinar conceitos que o AI agent ja conhece (polimorfismo, Streams, try-catch).

---

## T1-QUALITY-06: Estrutura de Secoes

**Regra:** Skills DEVEM seguir estrutura consistente.

```markdown
---
name: skill-id
description: |
  Action verb. Use when: trigger.
---

# Skill Title

Brief introduction (1-2 frases).

## How to <first capability>

Task-oriented instructions.

## How to <second capability>

More instructions.
```

**PROIBIDO no body:**
- Secao "When to Use" (trigger info fica no description)
- Secao "References" com URLs well-known
- Tabelas de compatibilidade
- Version/license footers
- README.md ou CHANGELOG.md dentro da skill

---

## T1-QUALITY-07: Recursos JIT Organizados

**Regra:** Recursos adicionais DEVEM estar em diretorios padrao.

```
skill/
├── SKILL.md          # Core (< 500 linhas)
├── references/       # Docs extensas (JIT loaded)
├── scripts/          # Executaveis
└── assets/           # Recursos estaticos
```

---

## T1-QUALITY-08: Exemplos Quando Nao-Obvios

**Regra:** Exemplos SAO necessarios apenas para padroes nao-obvios ou project-specific. Nao e obrigatorio para conceitos universais.

---

## T1-QUALITY-09: Progressive Disclosure

**Regra:** Se SKILL.md ultrapassa ~200 linhas, mover conteudo detalhado para `references/`.

---

## T1-QUALITY-10: Anti-Patterns

**Regra:** Skills NAO devem conter:

- Tabelas de compatibilidade entre CLIs
- Footers de versao ou license
- Secao "References" com URLs well-known (MDN, Oracle, etc.)
- Secao "When to Use" no body (trigger fica no description)
- README.md, CHANGELOG.md dentro da skill

---

**Ultima Atualizacao:** 2026-02-07 (v2.0.0)
