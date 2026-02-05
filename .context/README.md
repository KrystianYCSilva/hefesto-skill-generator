# .context/ - AI Context Hub

> **Projeto:** Hefesto Skill Generator
> **Versao:** 1.0.0-LTS (Production Ready)
> **Status:** ✅ LTS Release
> **Tier System:** Ativo

---

## Quick Start

**Production Ready:** Hefesto v1.0.0-LTS is ready for production use with 9 demonstration skills across 5 domains.

1. Leia este arquivo
2. Carregue `standards/architectural-rules.md` (T0)
3. Verifique `_meta/tech-stack.md` para especificidades do projeto
4. Consulte `ai-assistant-guide.md` para protocolo completo
5. Explore 9 available skills in `.opencode/skills/`, `.claude/skills/`, etc.

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

## Feature 004: Multi-CLI Automatic Parallel Generation

**Status:** ✅ COMPLETED (2026-02-05)

Feature 004 brings major architectural improvements:

**Key Changes:**
- ADR-008 added: Parallel + Atomic multi-CLI generation
- T0-HEFESTO-06 enhanced: Parallel detection in <500ms
- 5 new helpers: cli-detector, cli-adapter, parallel-generator, rollback-handler, multi-cli-integration
- 2 new templates: detection-report, generation-report

**Performance:**
- 3x faster skill generation (2s vs 6s sequential)
- Atomic all-or-nothing semantics
- <500ms CLI detection

**Test Results:**
- 9/9 manual tests passed ✅
- 10/10 mandatory criteria met ✅
- 3/3 desirable criteria met ✅
- 8/8 T0 rules validated ✅

**Documentation Updates:**
- Updated: architectural-rules.md (T0-HEFESTO-06, added T0-HEFESTO-11)
- Updated: key-decisions.md (added ADR-008)
- Updated: project-overview.md (Feature 004 info)

---

---

## LTS v1.0.0 Release

**Status:** ✅ PRODUCTION READY (2026-02-05)

- **Release:** Long-Term Support v1.0.0
- **Completion:** 97.4% (222/228 tasks)
- **Skills:** 9 demonstration skills across 5 domains
- **Commands:** 9/9 operational (100%)
- **T0 Compliance:** All 11 constitutional rules validated
- **Production Ready:** Safe for production use

**Available Skills:**
1. java-fundamentals (6 CLIs)
2. kotlin-fundamentals (6 CLIs)
3. markdown-fundamentals (6 CLIs)
4. coala-framework (6 CLIs)
5. prompt-engineering-basics (2 CLIs)
6. zk-framework (1 CLI)
7. programming-fundamentals (1 CLI)
8. context-engineering-basics (1 CLI)
9. chain-of-thought (1 CLI)

---

**Ultima Atualizacao:** 2026-02-05 (LTS v1.0.0 Release)
