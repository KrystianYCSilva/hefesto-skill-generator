# Exemplo: Estrutura de Skill - Code Review

> **Tier:** T3 - Ilustrativo
> **Proposito:** Demonstrar estrutura correta de uma skill Agent Skills (v2.0.0)

---

## 1. Estrutura de Diretorios

```
code-review/
├── SKILL.md              # Core (< 500 linhas)
├── scripts/
│   └── analyze.sh        # Script auxiliar
└── references/
    └── checklist.md       # Docs detalhadas (JIT loaded)
```

---

## 2. SKILL.md (Core)

```yaml
---
name: code-review
description: |
  Padroniza code reviews seguindo boas praticas SOLID e Clean Code.
  Use when: revisar PRs, avaliar codigo de terceiros, onboarding de novos devs.
---

# Code Review

Skill para conduzir code reviews estruturados e consistentes.

## How to review a Pull Request

Leia o codigo alvo e identifique:
- Linguagem e framework utilizados
- Padrao arquitetural (MVC, Clean, Hexagonal, etc.)
- Presenca de testes existentes
- Convencoes de codigo do projeto

## How to apply SOLID checklist

Verifique cada principio:

- **S**ingle Responsibility: Cada classe/funcao tem uma unica responsabilidade?
- **O**pen/Closed: Codigo aberto para extensao, fechado para modificacao?
- **L**iskov Substitution: Subtipos substituiveis por tipos base?
- **I**nterface Segregation: Interfaces especificas ao inves de genericas?
- **D**ependency Inversion: Depende de abstracoes, nao implementacoes?

## How to check Clean Code

Checklist de qualidade:
- [ ] Nomes descritivos e pronunciaveis
- [ ] Funcoes pequenas (idealmente < 20 linhas)
- [ ] Sem comentarios obvios (codigo auto-documentado)
- [ ] Sem codigo duplicado (DRY)
- [ ] Tratamento de erros adequado
- [ ] Formatacao consistente

## How to evaluate tests

Se testes existem:
- [ ] Cobertura adequada (>= 80%)
- [ ] Testes unitarios isolados
- [ ] Nomes descritivos nos testes
- [ ] Arrange-Act-Assert pattern

Se testes NAO existem:
- Sugerir criacao de testes prioritarios
- Identificar codigo mais critico para testar

## How to generate review report

Formato recomendado:

### Resumo
[Avaliacao geral em 2-3 linhas]

### Pontos Positivos
- [Item 1]
- [Item 2]

### Melhorias Sugeridas
| Prioridade | Item | Justificativa |
|------------|------|---------------|
| Alta | [Item] | [Por que] |
| Media | [Item] | [Por que] |
```

---

## 3. Pontos-Chave do Exemplo (v2.0.0)

| Aspecto | Implementacao |
|---------|---------------|
| Frontmatter | SOMENTE `name` + `description` |
| Description | Acionavel com "Use when:" |
| Body pattern | Secoes "How to [task]" (NAO "Instructions > Step N") |
| SKILL.md | < 500 linhas (core) |
| Progressive Disclosure | Docs detalhadas em references/ |
| No "When to Use" | Trigger info vive no description |
| No tutorials | Nao ensina SOLID/Clean Code (AI ja sabe) |
| No license/metadata | Sem campos extras no frontmatter |

---

## 4. Anti-Patterns (NAO fazer)

```yaml
# PROIBIDO no v2.0.0

---
name: code-review
description: |
  ...
license: MIT                    # NAO
compatibility: Claude Code      # NAO
metadata:
  version: "1.0.0"             # NAO
  tags: [code-review]          # NAO
---

# Code Review

## When to Use               <-- NAO (trigger fica no description)

## Instructions               <-- NAO (usar "How to [task]")
### Step 1: ...               <-- NAO
### Step 2: ...               <-- NAO

## References                 <-- NAO (URLs well-known sao desnecessarias)
- [Clean Code](https://...)

---
**Gerado por:** Hefesto v1.0.0  <-- NAO (sem footers)
```

---

**Ultima Atualizacao:** 2026-02-07 (v2.0.0)
