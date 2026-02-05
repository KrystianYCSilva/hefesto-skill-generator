# .context/ - AI Context Hub

> **Projeto:** Hefesto Skill Generator
> **Versao:** 1.0.0
> **Tier System:** Ativo

---

## Quick Start

1. Leia este arquivo
2. Carregue `standards/architectural-rules.md` (T0)
3. Verifique `_meta/tech-stack.md` para especificidades do projeto
4. Consulte `ai-assistant-guide.md` para protocolo completo

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
│   ├── architectural-rules.md   # T0: ABSOLUTO
│   ├── code-quality.md          # T1: Qualidade
│   └── testing-strategy.md      # T1: Testes
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
    └── common-issues.md
```

---

## Tier System

| Tier | Tipo | Autoridade | Diretorio |
|------|------|------------|-----------|
| **T0** | Enforcement | ABSOLUTA | `standards/architectural-rules.md` |
| **T1** | Standards | NORMATIVA | `standards/`, `patterns/` |
| **T2** | Context | INFORMATIVA | `_meta/` |
| **T3** | Examples | ILUSTRATIVA | `examples/` |

### Logica de Resolucao

```
IF T0 conflita com qualquer tier → T0 VENCE
IF T1 conflita com T2 ou T3 → T1 VENCE
IF T2 conflita com T3 → T2 VENCE
ALWAYS cite a regra especifica (ID) na resposta
```

---

## Links Rapidos

| Preciso de... | Arquivo |
|---------------|---------|
| Regras absolutas | `standards/architectural-rules.md` |
| Visao do projeto | `_meta/project-overview.md` |
| Stack tecnica | `_meta/tech-stack.md` |
| Decisoes arquiteturais | `_meta/key-decisions.md` |
| Padroes de codigo | `standards/code-quality.md` |
| Estrategia de testes | `standards/testing-strategy.md` |
| Arquitetura | `patterns/architectural-overview.md` |
| Exemplos | `examples/` |

---

## Para IAs

**IMPORTANTE:** Antes de gerar codigo ou skills:

1. Carregar `standards/architectural-rules.md` (T0)
2. Verificar CONSTITUTION.md na raiz do projeto
3. Respeitar Human Gate para todas as operacoes de escrita
4. Validar contra Agent Skills spec antes de persistir

---

**Ultima Atualizacao:** 2026-02-04
