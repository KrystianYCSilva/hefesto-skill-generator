# Code Quality Standards - T1 (Normativo)

> **Tier:** T1 - NORMATIVO
> **Seguir estas regras como padrao.**

---

## T1-QUALITY-01: Markdown Bem Formatado

**Regra:** Todo Markdown DEVE ser bem formatado.

**Requisitos:**
- Headers hierarquicos (H1 > H2 > H3)
- Listas consistentes (- ou *)
- Blocos de codigo com linguagem especificada
- Tabelas alinhadas
- Links funcionais

```markdown
# CORRETO

## Section Header

- Item 1
- Item 2

```yaml
code: here
```

# PROIBIDO

Section Header  # Sem #

* Item 1
- Item 2  # Misturado

```
code without language
```
```

---

## T1-QUALITY-02: YAML Frontmatter Valido

**Regra:** Frontmatter DEVE ser YAML valido e bem formatado.

```yaml
# CORRETO
---
name: skill-name
description: |
  Descricao multiline.
  Segunda linha.
metadata:
  version: "1.0.0"
---

# PROIBIDO
---
name: skill-name
description: Descricao com "aspas" sem escape
metadata:
  version: 1.0.0  # String sem aspas em YAML
---
```

---

## T1-QUALITY-03: Descricoes Acionaveis

**Regra:** Descricoes DEVEM ser acionaveis com "Use when:" ou similar.

```yaml
# CORRETO
description: |
  Padroniza code reviews seguindo boas praticas SOLID.
  Use quando: revisar PRs, avaliar codigo de terceiros, onboarding.

# ACEITAVEL
description: |
  Analisa complexidade ciclomatica e sugere refatoracoes.
  Ideal para: reducao de divida tecnica, melhoria de maintainability.

# PROIBIDO
description: Uma skill para code review.  # Nao acionavel
```

---

## T1-QUALITY-04: Instrucoes Claras

**Regra:** Instrucoes DEVEM ser claras e sequenciais.

```markdown
# CORRETO

## Instructions

### Step 1: Analisar Contexto

Leia o codigo/PR alvo e identifique:
- Linguagem/framework
- Padrao arquitetural
- Testes existentes

### Step 2: Aplicar Checklist

Verifique cada item:
- [ ] Nomes descritivos
- [ ] Funcoes pequenas (< 20 linhas)
- [ ] Sem codigo duplicado

# PROIBIDO

## Instructions

Faca code review do codigo seguindo boas praticas e reporte os problemas encontrados.
# Muito vago, sem passos claros
```

---

## T1-QUALITY-05: Exemplos Quando Necessario

**Regra:** Skills complexas DEVEM incluir exemplos.

**Criterio de complexidade:**
- Mais de 3 passos
- Requer conhecimento de dominio
- Multiplos casos de uso

```markdown
# CORRETO (skill complexa)

## Examples

### Example 1: PR de Feature Nova

**Input:** PR com 5 arquivos, nova feature de login

**Output Esperado:**
```
## Code Review Summary

### Positivo
- Boa separacao de responsabilidades
- Testes unitarios presentes

### Melhorias Sugeridas
- Extrair validacao para classe separada
- Adicionar teste de integracao
```

# PROIBIDO (skill complexa)

## Instructions

[Instrucoes sem exemplos]  # Falta exemplo para skill complexa
```

---

## T1-QUALITY-06: Estrutura Consistente

**Regra:** Skills DEVEM seguir estrutura consistente.

**Ordem de Secoes:**
1. Frontmatter (YAML)
2. Titulo (H1)
3. When to Use
4. Instructions
5. Examples (se aplicavel)
6. References (se aplicavel)
7. Footer (opcional)

---

## T1-QUALITY-07: Recursos JIT Organizados

**Regra:** Recursos adicionais DEVEM estar em diretorios padrao.

```
# CORRETO
skill/
├── SKILL.md
├── scripts/
│   └── validate.py
├── references/
│   └── REFERENCE.md
└── assets/
    └── schema.json

# PROIBIDO
skill/
├── SKILL.md
├── validate.py      # Solto na raiz
├── REFERENCE.md     # Solto na raiz
└── schema.json      # Solto na raiz
```

---

## T1-QUALITY-08: Versionamento

**Regra:** Skills DEVEM ter versao no metadata.

```yaml
# CORRETO
metadata:
  version: "1.0.0"
  created: 2026-02-04
  updated: 2026-02-04

# PROIBIDO
metadata:
  author: nome  # Sem versao
```

---

## T1-QUALITY-09: Tags para Descoberta

**Regra:** Skills DEVEM ter 3-8 tags relevantes.

```yaml
# CORRETO
metadata:
  tags: [code-review, quality, solid, clean-code, best-practices]

# PROIBIDO
metadata:
  tags: []  # Vazio
  tags: [skill]  # Muito generico
```

---

## T1-QUALITY-10: Compatibilidade Documentada

**Regra:** Compatibilidade de CLI DEVE ser documentada.

```yaml
# CORRETO
compatibility: Claude Code, Gemini CLI, Codex, OpenCode, Cursor, Qwen Code, VS Code/Copilot

# OU
compatibility: |
  Requer acesso a filesystem e execucao de scripts Python.
  Testado em: Claude Code 1.0+, Gemini CLI 0.20+
```

---

**Ultima Atualizacao:** 2026-02-04
