# ADR-003: Frontmatter Leve com Metadados JIT

**Status:** Aceito
**Data:** 2026-02-04
**Autores:** Human + AI Agent

---

## Contexto

O ADR-002 introduziu metadados expandidos (11 campos) para enriquecer skills. Porem, incluir todos no frontmatter do SKILL.md:

1. **Polui o arquivo principal** - Frontmatter muito grande
2. **Viola T0-HEFESTO-03** - Progressive Disclosure exige core leve
3. **Carrega dados desnecessarios** - Agente nem sempre precisa de todos os campos

---

## Decisao

Adotar estrutura de **2 niveis** para metadados:

### Nivel 1: Frontmatter SKILL.md (Obrigatorio, ~100 tokens)

```yaml
---
name: skill-name           # T0-HEFESTO-01: max 64 chars, lowercase
description: |             # T0-HEFESTO-01: max 1024 chars
  Descricao da skill.
  Use quando: [gatilhos de uso]
license: MIT               # Licenca da skill
metadata: ./metadata.yaml  # Ponteiro JIT (opcional)
---
```

| Campo | Obrigatorio | Limite | Fonte |
|-------|-------------|--------|-------|
| `name` | Sim | 64 chars | T0-HEFESTO-01 |
| `description` | Sim | 1024 chars | T0-HEFESTO-01 |
| `license` | Sim | - | ADR-003 |
| `metadata` | Nao | path relativo | ADR-003 |

### Nivel 2: metadata.yaml (JIT, carregado sob demanda)

```yaml
# metadata.yaml - Agente carrega apenas se necessario
author: "Nome <email@exemplo.com>"
version: "1.0.0"
created: 2026-02-04
updated: 2026-02-04

category: development
tags: [tag1, tag2, tag3]
platforms: [claude, gemini, codex, copilot]

dependencies:
  - python>=3.8
  - requests

example_prompt: "Exemplo de como invocar esta skill"

test_cases:
  - name: "Caso basico"
    input: "entrada de teste"
    expected: "saida esperada"

related_skills:
  - testing-strategy
  - documentation

sources:
  - title: "Documentacao Oficial"
    url: "https://exemplo.com/docs"
    accessed: 2026-02-04
```

### Estrutura Final de Skill

```
skill-name/
├── SKILL.md           # Core + frontmatter leve (~100 tokens)
├── metadata.yaml      # Metadados expandidos (JIT)
├── scripts/           # Recursos executaveis (JIT)
├── references/        # Documentacao detalhada (JIT)
└── assets/            # Recursos estaticos (JIT)
```

---

## Fluxo de Carregamento

```
1. Agente detecta skill pelo nome
2. Carrega SKILL.md (frontmatter + corpo)
3. SE precisa de mais info:
   - Verifica campo `metadata:`
   - Carrega metadata.yaml sob demanda
4. SE precisa de recursos:
   - Carrega scripts/, references/, assets/ sob demanda
```

---

## Consequencias

### Positivas

- **Frontmatter leve** - Apenas 4 campos, ~100 tokens
- **JIT real** - Metadados expandidos carregados apenas quando necessarios
- **Consistente com T0-HEFESTO-03** - Progressive Disclosure mantido
- **Flexivel** - metadata.yaml pode crescer sem afetar SKILL.md
- **Retrocompativel** - Skills sem `metadata:` funcionam normalmente

### Negativas

- **Dois arquivos** - Skill completa requer SKILL.md + metadata.yaml
- **Complexidade de validacao** - Validar dois arquivos em vez de um

---

## Alternativas Consideradas

### Alternativa 1: Todos os campos no frontmatter
**Descricao:** Manter todos os 11 campos no SKILL.md
**Por que rejeitada:** Viola T0-HEFESTO-03, frontmatter muito pesado

### Alternativa 2: Inline YAML no corpo do SKILL.md
**Descricao:** Bloco ```yaml no corpo em vez de arquivo separado
**Por que rejeitada:** Ainda polui SKILL.md, nao e JIT real

### Alternativa 3: JSON em vez de YAML
**Descricao:** Usar metadata.json
**Por que rejeitada:** YAML e mais legivel e consistente com frontmatter

---

## Atualizacoes Necessarias

- [x] CARD-002: Atualizar estrutura de templates
- [ ] CONSTITUTION.md: Documentar estrutura de 2 niveis
- [ ] Templates: Criar metadata.yaml template
- [ ] Validador: Validar ambos os arquivos

---

## Referencias

- T0-HEFESTO-01: Agent Skills Standard
- T0-HEFESTO-03: Progressive Disclosure
- ADR-002: Integracao de Pesquisa Academica
- Agent Skills Spec: https://agentskills.io

---

**ADR-003** | Hefesto Skill Generator | Aceito em 2026-02-04
