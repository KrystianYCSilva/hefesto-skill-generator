# .context/ - AI Context Hub

> **Projeto:** Hefesto Skill Generator
> **Versao:** 2.2.0
> **Arquitetura:** Template-Driven (zero dependencies)

---

## Quick Start

1. Leia este arquivo (hub de navegacao)
2. Carregue `ai-assistant-guide.md` para protocolo completo
3. Consulte `standards/architectural-rules.md` para regras T0
4. Verifique `_meta/tech-stack.md` para stack tecnica

---

## Estrutura

```
.context/
├── README.md                    # Este arquivo (Hub)
├── ai-assistant-guide.md        # Protocolo completo para IAs
│
├── _meta/                       # T2: Contexto e Decisoes
│   ├── project-overview.md      # Visao geral do projeto
│   ├── tech-stack.md            # Stack tecnica
│   └── key-decisions.md         # ADRs consolidados
│
├── standards/                   # T0-T1: Regras e Padroes
│   ├── architectural-rules.md   # T0: Regras absolutas (espelho de CONSTITUTION.md)
│   ├── code-quality.md          # T1: Qualidade de skills
│   └── testing-strategy.md      # T1: Validacao e testes
│
├── patterns/                    # T1: Blueprints
│   └── architectural-overview.md
│
├── examples/                    # T3: Exemplos
│   ├── skill-structure-example.md
│   └── command-example.md
│
├── workflows/                   # Fluxos de trabalho
│   └── development-workflows.md
│
└── troubleshooting/             # Erros comuns
    ├── common-issues.md
    └── foundation-issues.md
```

---

## Tier System

| Tier | Tipo | Autoridade | Diretorio |
|------|------|------------|-----------|
| **T0** | Enforcement | ABSOLUTA | `CONSTITUTION.md` (raiz) |
| **T1** | Standards | NORMATIVA | `standards/`, `patterns/` |
| **T2** | Context | INFORMATIVA | `_meta/` |
| **T3** | Examples | ILUSTRATIVA | `examples/` |

### Logica de Resolucao

```
IF T0 conflita com qualquer tier -> T0 VENCE
IF T1 conflita com T2 ou T3 -> T1 VENCE
IF T2 conflita com T3 -> T2 VENCE
ALWAYS cite a regra especifica (ID) na resposta
```

---

## Links Rapidos

| Preciso de... | Arquivo |
|---------------|---------|
| Regras absolutas (T0) | `CONSTITUTION.md` (raiz do projeto) |
| Protocolo para IAs | `ai-assistant-guide.md` |
| Visao do projeto | `_meta/project-overview.md` |
| Stack tecnica | `_meta/tech-stack.md` |
| Decisoes arquiteturais | `_meta/key-decisions.md` |
| Qualidade de skills | `standards/code-quality.md` |
| Validacao | `standards/testing-strategy.md` |
| Arquitetura | `patterns/architectural-overview.md` |
| Exemplos | `examples/` |
| Troubleshooting | `troubleshooting/` |

---

## Para IAs

**IMPORTANTE:** Antes de gerar skills:

1. Carregar `templates/` (skill-template, quality-checklist, cli-compatibility)
2. Verificar `.hefesto/version` para estado da instalacao
3. Respeitar Human Gate para todas as operacoes de escrita
4. Validar contra Agent Skills spec (13-point checklist) antes de persistir
5. Frontmatter: SOMENTE `name` + `description`
6. Body: secoes "How to [task]" (NAO "Instructions > Step N")

---

**Ultima Atualizacao:** 2026-02-07 (v2.0.0)


