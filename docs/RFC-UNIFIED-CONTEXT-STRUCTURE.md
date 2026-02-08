# RFC: Estrutura Unificada .context/ para AI-Assisted Development

> **Versao:** 1.0.0
> **Data:** 2026-01-16
> **Status:** APROVADA
> **Baseado em:** RFC-001, RFC-002, RFC-CONTEXT-ENGINEERING

---

## 1. Resumo Executivo

Esta RFC define a estrutura padronizada da pasta `.context/` para projetos que utilizam AI-Assisted Development. A estrutura suporta dois niveis de conformidade:

- **Nivel Basico:** Para projetos internos e menos criticos
- **Nivel Completo:** Para projetos de clientes ou alta criticidade

---

## 2. Estrutura de Diretorios

### 2.1. Nivel Basico (Minimo Obrigatorio)

```
project-root/
├── AGENTS.md                    # Bootstrap (kernel)
├── MEMORY.md                    # Estado persistente
│
└── .context/                    # Contexto para IAs
    ├── README.md               # Hub de navegacao
    ├── _meta/
    │   └── tech-stack.md       # Stack tecnica
    └── standards/
        └── architectural-rules.md  # Regras T0
```

### 2.2. Nivel Completo (Projetos Criticos)

```
project-root/
├── AGENTS.md                    # Bootstrap GitHub Copilot
├── CLAUDE.md                    # Bootstrap Claude
├── .cursorrules                 # Bootstrap Cursor IDE
├── MEMORY.md                    # Estado persistente (longo prazo)
├── MEMORIA.md                   # Estado sessao (curto prazo) [OPCIONAL]
│
└── .context/
    ├── README.md               # Hub de navegacao
    ├── ai-assistant-guide.md   # Protocolo completo para IAs
    │
    ├── _meta/                  # T2: Contexto e Decisoes
    │   ├── project-overview.md
    │   ├── tech-stack.md
    │   └── key-decisions.md    # ADRs consolidados
    │
    ├── standards/              # T0-T1: Regras e Padroes
    │   ├── architectural-rules.md  # T0: ABSOLUTO
    │   ├── code-quality.md         # T1: SOLID, Clean Code
    │   └── testing-strategy.md     # T1: TDD, cobertura
    │
    ├── patterns/               # T1: Blueprints
    │   └── architectural-overview.md
    │
    ├── examples/               # T3: Exemplos de codigo
    │   └── clean-architecture-structure.md
    │
    ├── workflows/              # Fluxos de trabalho
    │   └── development-workflows.md
    │
    └── troubleshooting/        # Erros comuns
        └── common-issues.md
```

---

## 3. Tier System (Hierarquia de Precedencia)

O Tier System e OBRIGATORIO em ambos os niveis:

| Tier | Tipo | Autoridade | Prevalece Sobre | Diretorio |
|------|------|------------|-----------------|-----------|
| **T0** | Enforcement | ABSOLUTA | Todos | `standards/architectural-rules.md` |
| **T1** | Standards | NORMATIVA | T2, T3 | `standards/`, `patterns/` |
| **T2** | Context | INFORMATIVA | T3 | `_meta/` |
| **T3** | Examples | ILUSTRATIVA | Nenhum | `examples/` |

### Logica de Resolucao de Conflitos

```
IF T0 conflita com qualquer tier → T0 VENCE
IF T1 conflita com T2 ou T3 → T1 VENCE
IF T2 conflita com T3 → T2 VENCE
ALWAYS cite a regra especifica (ID) na resposta
```

---

## 4. Conteudo dos Arquivos

### 4.1. AGENTS.md (Bootstrap - OBRIGATORIO)

```markdown
# AI Development Kernel

**CRITICAL**: Before generating code, load context from `/.context/`

## Tier System
| Tier | File | Authority |
|------|------|-----------|
| T0 | `/.context/standards/architectural-rules.md` | ABSOLUTE |
| T1 | `/.context/standards/code-quality.md` | NORMATIVE |
| T2 | `/.context/_meta/` | INFORMATIVE |

## Quick Rules (T0)
[Liste 3-5 regras T0 criticas aqui]

## State
Read `MEMORY.md` for current state.
```

### 4.2. MEMORY.md (Estado - OBRIGATORIO)

```markdown
# MEMORY.md - AI Persistent State

## Last Updated
[DATA]

## Current State
**Project:** [NOME]
**Status:** [STATUS]

## Recent Actions
[Ultimas acoes realizadas]

## Next Steps
[Proximos passos]
```

### 4.3. .context/README.md (Hub - OBRIGATORIO)

```markdown
# .context/ - AI Context Hub

## Quick Start
1. Read this file
2. Load `standards/architectural-rules.md` (T0)
3. Check `_meta/tech-stack.md` for project specifics

## Structure
- `_meta/` → Project context (T2)
- `standards/` → Rules and patterns (T0-T1)
- `patterns/` → Blueprints (T1)
- `examples/` → Code samples (T3)

## Tier System
[Tabela do Tier System]
```

### 4.4. standards/architectural-rules.md (T0 - OBRIGATORIO)

```markdown
# Architectural Rules - T0 (Enforcement)

> **Tier**: T0 - ABSOLUTO. SEMPRE seguir estas regras.

---

## [CATEGORIA]-[ID]: Nome da Regra

**Regra**: Descricao clara.

```java
// CORRETO
[codigo correto]

// PROIBIDO
[codigo proibido]
```

---


### 4.5. ai-assistant-guide.md (Nivel Completo)

**Conteudo obrigatorio:**
- Bootstrap Sequence (3 passos)
- Request Classification (tabela tipo → arquivos)
- Tier System com logica
- Definition of Done
- Metodologia de Pesquisa
- Available Agents

---

## 5. Bootstrap Multi-IA (Nivel Completo)

### 5.1. CLAUDE.md

```markdown
# Claude AI - Context Engineering Setup

**CRITICAL**: Load `/.context/ai-assistant-guide.md` first.

## Essential Pointers
| Tier | File |
|------|------|
| T0 | `/.context/standards/architectural-rules.md` |
| T1 | `/.context/standards/code-quality.md` |
| T2 | `/.context/_meta/key-decisions.md` |
```

### 5.2. .cursorrules

```markdown
# Cursor IDE Rules

Load `/.context/ai-assistant-guide.md` before generating code.

## Mandatory Rules (T0)
[Lista de regras T0]

## Testing
- Line coverage >= 90%
- Branch coverage >= 80%
```

---

## 6. Metodologia de Pesquisa (Nivel Completo)

### Hierarquia de Fontes

| Tier | Tipo | Exemplos | Uso |
|------|------|----------|-----|
| **1** | Oficiais | gov.br, docs oficiais | SEMPRE primeiro |
| **2** | Academicas | Capes, SciELO | Artigos cientificos |
| **3** | Consolidados | Baeldung, StackOverflow | Suplementar |
| **4** | Forums | Reddit | ULTIMO RECURSO |
| **X** | **PROIBIDO** | Blogs pessoais, redes sociais | NUNCA |

### Regras

```
SEMPRE trazer referencia (URL + data)
SEMPRE validar com fonte oficial
SEMPRE documentar em docs/pesquisa-previa/
NUNCA usar fontes nao-verificaveis
```

---

## 7. Definition of Done (Nivel Completo)

| Metrica | Minimo |
|---------|--------|
| **Line Coverage** | >= 90% |
| **Branch Coverage** | >= 80% |
| **Convencao 1:1** | 1 classe teste : 1 classe impl |
| **Documentacao** | Atualizada |

---

## 8. Checklist de Conformidade

### Nivel Basico

- [ ] AGENTS.md criado
- [ ] MEMORY.md criado
- [ ] .context/README.md criado
- [ ] .context/_meta/tech-stack.md criado
- [ ] .context/standards/architectural-rules.md criado (minimo 5 regras T0)

### Nivel Completo (adicional)

- [ ] CLAUDE.md criado
- [ ] .cursorrules criado
- [ ] .context/ai-assistant-guide.md criado
- [ ] .context/_meta/project-overview.md criado
- [ ] .context/_meta/key-decisions.md criado
- [ ] .context/standards/code-quality.md criado
- [ ] .context/standards/testing-strategy.md criado
- [ ] .context/patterns/ populado
- [ ] .context/examples/ populado
- [ ] .context/workflows/ populado
- [ ] .context/troubleshooting/ populado
- [ ] Metodologia de pesquisa documentada
- [ ] Definition of Done definido

---

## 9. Migracao de Projetos Existentes

Ver: `docs/templates/BROWNFIELD-MIGRATION-GUIDE.md`

---

## 10. Referencias

- RFC-001: AI-Assisted Software Development Lifecycle
- RFC-002: Standardized Documentation Structure
- RFC-CONTEXT-ENGINEERING: Context Engineering para IAs

---

**Versao:** 1.0.0
**Ultima Atualizacao:** 2026-01-16
