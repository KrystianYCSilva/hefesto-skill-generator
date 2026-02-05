# Testing Strategy - T1 (Normativo)

> **Tier:** T1 - NORMATIVO
> **Estrategia de validacao para skills geradas.**

---

## 1. Niveis de Validacao

### 1.1. Validacao de Estrutura (Automatica)

**Quando:** Sempre, antes de Human Gate

**Checklist:**
- [ ] Arquivo SKILL.md existe
- [ ] Frontmatter YAML valido
- [ ] Campo `name` presente e valido
- [ ] Campo `description` presente e nao vazio
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
- [ ] `description`: nao vazio

### 1.3. Validacao de Qualidade (Human Gate)

**Quando:** Apos validacoes automaticas

**Apresentar ao usuario:**
- Preview da skill
- Resultado das validacoes automaticas
- Opcoes: [approve], [expand], [edit], [reject]

---

## 2. Criterios de Aprovacao

### 2.1. Skill Basica

| Criterio | Obrigatorio |
|----------|-------------|
| Frontmatter valido | Sim |
| Name conforme spec | Sim |
| Description acionavel | Sim |
| Instrucoes presentes | Sim |
| < 500 linhas | Sim |

### 2.2. Skill Complexa

| Criterio | Obrigatorio |
|----------|-------------|
| Todos de skill basica | Sim |
| Exemplos presentes | Sim |
| Referencias documentadas | Sim |
| Recursos JIT organizados | Sim |

---

## 3. Validacao por CLI

### 3.1. Validacao Universal

Aplicavel a TODOS os CLIs:

```yaml
---
name: valid-name
description: |
  Descricao valida.
---

# Instructions

...
```

### 3.2. Validacao Especifica

**Gemini/Qwen:**
- Verificar conversao `$ARGUMENTS` → `{{args}}`
- Verificar formato TOML se aplicavel

**Copilot:**
- Verificar diretorio `.github/skills/`
- Verificar compatibilidade com VS Code

---

## 4. Testes de Regressao

### 4.1. Skill Existente (Overwrite)

**Fluxo:**
1. Detectar skill existente
2. Comparar com versao nova
3. Mostrar diff ao usuario
4. Aguardar: [overwrite], [merge], [cancel]

### 4.2. Sincronizacao Multi-CLI

**Fluxo:**
1. Identificar CLIs com skill
2. Comparar versoes
3. Mostrar diferencas
4. Sincronizar apos aprovacao

---

## 5. Metricas de Qualidade

| Metrica | Alvo | Critico |
|---------|------|---------|
| Skills validas geradas | 100% | < 95% |
| Taxa aprovacao 1a tentativa | >= 80% | < 60% |
| Erros de validacao | 0 | > 5% |
| Skills sincronizadas | 100% | < 90% |

---

## 6. Erros de Validacao

### 6.1. Erros Criticos (Bloqueantes)

| Erro | Causa | Acao |
|------|-------|------|
| `INVALID_NAME` | Name fora do padrao | Bloquear, sugerir correcao |
| `EMPTY_DESCRIPTION` | Description vazio | Bloquear, solicitar preenchimento |
| `INVALID_YAML` | Frontmatter malformado | Bloquear, mostrar erro |
| `FILE_TOO_LARGE` | > 500 linhas | Bloquear, sugerir split |

### 6.2. Warnings (Nao Bloqueantes)

| Warning | Causa | Acao |
|---------|-------|------|
| `MISSING_EXAMPLES` | Skill complexa sem exemplos | Avisar, permitir continuar |
| `MISSING_REFERENCES` | Skill tecnica sem fontes | Avisar, permitir continuar |
| `GENERIC_DESCRIPTION` | Description muito vago | Avisar, sugerir melhoria |

---

## 7. Formato de Reporte

### 7.1. Validacao Bem Sucedida

```markdown
## Validacao: APROVADA ✅

### Checklist
- [x] Frontmatter valido
- [x] Name conforme spec: `code-review`
- [x] Description presente (142 chars)
- [x] SKILL.md: 87 linhas

### Warnings
Nenhum

### Proximo Passo
Human Gate: [approve] [expand] [edit] [reject]
```

### 7.2. Validacao com Erros

```markdown
## Validacao: FALHOU ❌

### Erros (Bloqueantes)
- `INVALID_NAME`: "Code-Review" contem uppercase
  - Sugestao: `code-review`

### Warnings
- `MISSING_EXAMPLES`: Skill parece complexa (4 passos)
  - Sugestao: Adicionar secao Examples

### Acao Necessaria
Corrigir erros antes de prosseguir.
```

---

## 8. Validacao Continua

### 8.1. Pre-Commit (Recomendado)

Se usuario usar Git, sugerir hook:

```bash
# .git/hooks/pre-commit
for skill in .*/skills/*/SKILL.md; do
  hefesto validate "$skill" || exit 1
done
```

### 8.2. CI/CD (Opcional)

Workflow para validacao automatica:

```yaml
# .github/workflows/validate-skills.yml
on: [push, pull_request]
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: |
          for skill in .*/skills/*/SKILL.md; do
            # Validar cada skill
          done
```

---

**Ultima Atualizacao:** 2026-02-04
