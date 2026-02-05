# ARCHITECTURE.md - Hefesto Skill Generator

> **Visao Arquitetural do Sistema**
> **Versao:** 1.4.0 (Feature 004: Multi-CLI Parallel Generation)

---

## 1. Visao Geral

Hefesto Skill Generator e um sistema prompt-based que gera Agent Skills padronizadas para multiplos CLIs de IA.

```
┌─────────────────────────────────────────────────────────────────────┐
│                              USUARIO                                 │
│                                                                      │
│    /hefesto.create    /hefesto.extract    /hefesto.validate         │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         HEFESTO ENGINE                               │
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌────────────┐ │
│  │  Template   │  │   Extract   │  │  Validate   │  │   Adapt    │ │
│  │  Processor  │  │   Analyzer  │  │   Engine    │  │   Engine   │ │
│  └─────────────┘  └─────────────┘  └─────────────┘  └────────────┘ │
│                                                                      │
│                        ┌─────────────┐                               │
│                        │ Human Gate  │                               │
│                        └─────────────┘                               │
│                                                                      │
│                   ┌───────────────────────┐                          │
│                   │  Multi-CLI Generator  │                          │
│                   └───────────────────────┘                          │
└───────────────────────────────┬─────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         OUTPUT (Skills)                              │
│                                                                      │
│   .claude/skills/    .gemini/skills/    .codex/skills/    ...       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Componentes

### 2.1. Command Layer

Recebe comandos do usuario e roteia para processadores apropriados.

**Comandos:**
- `/hefesto.create` → Template Processor
- `/hefesto.extract` → Extract Analyzer
- `/hefesto.validate` → Validate Engine
- `/hefesto.adapt` → Adapt Engine
- `/hefesto.sync` → Multi-CLI Generator
- `/hefesto.list` → Output Layer

### 2.2. Processing Engine

#### Template Processor

Gera skills a partir de descricao natural.

```
Input: Descricao em linguagem natural
Output: SKILL.md preenchido
```

#### Extract Analyzer

Extrai skills a partir de codigo/documentacao existente.

```
Input: Arquivo(s) de codigo ou docs
Output: SKILL.md derivado dos padroes encontrados
```

#### Validate Engine

Valida skills contra Agent Skills spec.

```
Input: SKILL.md existente
Output: Relatorio de validacao
```

#### Adapt Engine

Adapta skills para CLIs especificos.

```
Input: SKILL.md + CLI alvo
Output: SKILL.md adaptado
```

### 2.3. Human Gate

Controle de qualidade humano. Todas as operacoes de escrita passam por aqui.

```
Input: Skill gerada/adaptada
Output: Decisao do usuario [approve|expand|edit|reject]
```

### 2.4. Multi-CLI Generator (Feature 004)

Detecta CLIs instalados automaticamente e gera skills em paralelo para todos os CLIs detectados.

**Componentes (Feature 004):**

1. **CLI Detector** (`cli-detector.md`)
   - Deteccao via PATH do sistema
   - Deteccao via diretorios de configuracao
   - Suporta 7 CLIs: Claude, Gemini, Codex, OpenCode, Cursor, Qwen, Copilot
   - Performance: <500ms para deteccao completa

2. **CLI Adapter** (`cli-adapter.md`)
   - 7 adapters para transformacoes CLI-especificas
   - Ex: Gemini/Qwen `$ARGUMENTS` → `{{args}}`
   - Garante compatibilidade em todos CLIs

3. **Parallel Generator** (`parallel-generator.md`)
   - Execucao paralela com bash/PowerShell
   - 3x speedup vs sequencial (2s vs 6s)
   - Orquestra geracao simultanea

4. **Rollback Handler** (`rollback-handler.md`)
   - Atomic all-or-nothing semantics
   - Cleanup garantido se falha em qualquer CLI
   - Sem dados parciais deixados

```
Input: Skill aprovada + CLIs detectados (ou --cli flag)
Process: 
  1. Detectar CLIs instalados (<500ms)
  2. Selecionar adapters apropriados
  3. Gerar em paralelo para todos CLIs
  4. Rollback atomico se qualquer falha
Output: Skills em .claude/, .gemini/, .codex/, etc. (simultaneamente)
```

---

## 3. Fluxo de Dados

### /hefesto.create

```
Usuario → Descricao (+ opcional: --cli flag)
    ↓
Template Processor → SKILL.md (draft)
    ↓
Validate Engine → Validacao contra Agent Skills spec
    ↓
Human Gate → [approve|expand|edit|reject]
    ↓
CLI Detector (Feature 004) → Detecta 7 CLIs instalados (<500ms)
    ↓
Parallel Generator (Feature 004) → Gera em paralelo para CLIs detectados
    │
    ├─→ CLI Adapter 1 (Claude) → .claude/skills/{name}/
    ├─→ CLI Adapter 2 (Gemini) → .gemini/skills/{name}/ (com transformacoes)
    ├─→ CLI Adapter 3 (Codex) → .codex/skills/{name}/
    ├─→ CLI Adapter 4 (OpenCode) → .opencode/skills/{name}/
    ├─→ CLI Adapter 5 (Cursor) → .cursor/skills/{name}/
    ├─→ CLI Adapter 6 (Qwen) → .qwen/skills/{name}/ (com transformacoes)
    └─→ CLI Adapter 7 (Copilot) → .github/skills/{name}/
    ↓
Rollback Handler (Feature 004) → All-or-nothing garantido
    ↓
Usuario ← Resultado (3x mais rapido que sequencial)
```

**Feature 004 Performance:**
- Sequential: ~6s
- Parallel (Feature 004): ~2s (3x faster)
- Detection overhead: <500ms

### /hefesto.extract

```
Usuario → @arquivo
    ↓
Extract Analyzer → Padroes identificados
    ↓
Template Processor → SKILL.md (draft)
    ↓
[Continua como /hefesto.create]
```

---

## 4. Estrutura de Dados

### Skill (Agent Skills Format)

```yaml
---
name: string (max 64, lowercase, hyphens)
description: string (max 1024, nao vazio)
license: string (opcional)
compatibility: string (opcional)
metadata:
  author: string
  version: string
  category: string
  tags: [string]
---

# Titulo

## When to Use
...

## Instructions
...

## References
...
```

### Validation Result

```yaml
valid: boolean
errors: [string]  # Bloqueantes
warnings: [string]  # Informativos
checklist:
  structure: boolean
  spec: boolean
  quality: boolean
```

---

## 5. CLIs Suportados (Feature 004)

| CLI | Diretorio | Adapter | Deteccao | Status |
|-----|-----------|---------|----------|--------|
| Claude Code | `.claude/skills/` | Nativo (passthrough) | PATH + config | ✅ Active |
| Gemini CLI | `.gemini/skills/` | Transform: `$ARGUMENTS` → `{{args}}` | PATH + config | ✅ Active |
| OpenAI Codex | `.codex/skills/` | Nativo (npm compatible) | PATH | ✅ Active |
| VS Code/Copilot | `.github/skills/` | Nativo (estrutura VS Code) | config dir only | ⚠️ Warning |
| OpenCode | `.opencode/skills/` | Nativo (passthrough) | PATH + config | ✅ Active |
| Cursor | `.cursor/skills/` | Nativo (passthrough) | PATH + config | ✅ Active |
| Qwen Code | `.qwen/skills/` | Transform: `$ARGUMENTS` → `{{args}}` | PATH + config | ✅ Active |

**Feature 004 Detection Strategy:**
1. Check PATH for executables (priority order: claude > gemini > cursor > codex > qwen > opencode)
2. Check config directories (~/.claude, ~/.gemini, ~/.qwen, ~/.cursor, etc.)
3. Return union of all detected CLIs
4. Report non-detected CLIs for user awareness

---

## 6. Decisoes Arquiteturais

| Decisao | Justificativa |
|---------|---------------|
| Agent Skills Standard | Padrao aberto, suportado por multiplos CLIs |
| Human Gate obrigatorio | Controle de qualidade, usuario no controle |
| Deteccao automatica CLIs | UX fluida, menos perguntas |
| Projeto-first storage | Skills versionadas com codigo |
| Progressive Disclosure | Otimizacao de contexto |

Ver `docs/decisions/` para ADRs detalhados.

---

## 7. Extensibilidade

### Adicionar Novo CLI

1. Criar adapter em `templates/adapters/{cli}.adapter.md`
2. Definir transformacoes
3. Adicionar deteccao no Multi-CLI Generator

### Adicionar Novo Comando

1. Criar definicao em `commands/hefesto.{cmd}.md`
2. Definir fluxo
3. Implementar Human Gate se necessario

---

## 8. Feature 004: Multi-CLI Automatic Parallel Generation

**Status:** ✅ COMPLETED (2026-02-05)

Feature 004 brings significant architectural improvements:

- **Automatic Detection**: 7 CLIs detected in <500ms without user prompts
- **Parallel Execution**: 3x performance improvement (2s vs 6s sequential)
- **Atomic Guarantees**: All-or-nothing semantics on multi-CLI generation
- **CLI Adapters**: 7 specialized adapters with auto-transformations
- **Rollback Safety**: Guaranteed cleanup on partial failures

**Implementation:**
- 5 helpers: cli-detector, cli-adapter, parallel-generator, rollback-handler, multi-cli-integration
- 2 templates: detection-report, generation-report
- 9 manual tests: 100% pass rate
- Spec compliance: 10/10 mandatory criteria + 3/3 desirable + 8/8 T0 rules

**Reports:**
- Feature 004 Test Report: `docs/reports/feature-004-test-report.md`
- Feature 004 Executive Summary: `docs/reports/feature-004-executive-summary.md`
- Feature 004 Final Checklist: `docs/reports/feature-004-final-checklist.md`

---

**Ultima Atualizacao:** 2026-02-05 (Feature 004 Complete)
