# Reset Rationale: From Python System to Template-Driven Spec-Kit

> **Data:** 2026-02-07
> **Versao:** 2.2.0
> **Branch:** reset/spec-kit-model

---

## Por que o Reset?

### O Problema

O Hefesto v1.x cresceu para um sistema Python complexo:
- **19 arquivos Python** (~2500 linhas de codigo)
- **14 modulos na lib/** (atomic, audit, backup, collision, colors, diff, editor, expansion, human_gate, preview, sanitizer, timeout, wizard)
- **9 comandos** com wrappers .md que chamavam Python
- **Dependencias**: Python 3.8+, PyYAML, e outros

Isso criou uma contradicao fundamental: **um gerador de skills para AI CLIs que dependia de Python para funcionar**. O usuario precisava de Python instalado apenas para gerar arquivos Markdown.

### A Solucao

Resetar para um **spec-kit puro**: templates Markdown que o AI agent interpreta diretamente.

- **0 arquivos Python** - zero dependencias
- **5 comandos core** (create, validate, init, extract, list)
- **~750 linhas de templates** que substituem ~2500 linhas Python
- **Auto-critica** como diferencial vs sistema anterior (sem self-review)

---

## O que Mudou

### Removido

| Componente | Razao |
|-----------|-------|
| `commands/lib/` (14 modulos Python) | Logica movida para templates Markdown |
| `commands/hefesto_*_impl.py` | Substituidos por hefesto.*.md templates |
| `commands/templates/` | Relocado para `templates/` |
| `specs/003-005/` | Historico preservado no git |
| `testes/` | Resultados de teste obsoletos |
| `MEMORY.md` | Filesystem IS the state |
| `.hefesto/` | Temp state desnecessario sem Python |
| 4 comandos (adapt, sync, show, delete, resume) | Funcionalidade absorvida ou desnecessaria |
| `docs/reports/`, `docs/performance/` | Preservados no git history |

### Adicionado

| Componente | Proposito |
|-----------|----------|
| `templates/skill-template.md` | Template canonico para skills |
| `templates/quality-checklist.md` | Checklist de auto-critica 10 itens |
| `templates/cli-compatibility.md` | Regras de adaptacao multi-CLI |
| `hefesto.validate.md` | Novo comando de validacao |
| `hefesto.list.md` | Novo comando de listagem |
| `T0-HEFESTO-12` | Auto-critica obrigatoria |
| `T0-HEFESTO-13` | Template Authority |

### Preservado

| Componente | Status |
|-----------|--------|
| `.claude/skills/` (7+ skills) | Inalteradas |
| `speckit.*.md` (9 comandos) | Inalterados |
| `knowledge/` | Mantido |
| `.context/` (14 arquivos) | Mantido |
| `specs/001-002/` | Mantidos como historico |
| `docs/decisions/` (ADRs) | Mantidos |
| `LICENSE`, `CONTRIBUTING.md` | Mantidos |

---

## Decisoes Tecnicas

### 1. Por que Markdown puro?

O AI agent ja e um processador de linguagem natural. Dar-lhe instrucoes em Markdown e mais eficiente do que fazer ele executar Python. O Python era um intermediario desnecessario.

### 2. Por que 5 comandos (nao 9)?

| Comando Antigo | Destino |
|---------------|---------|
| `/hefesto.create` | Mantido (reescrito) |
| `/hefesto.init` | Mantido (simplificado) |
| `/hefesto.extract` | Mantido (reescrito) |
| `/hefesto.validate` | Novo (antes era fase interna) |
| `/hefesto.list` | Novo (antes era `/hefesto.show` + `/hefesto.list`) |
| `/hefesto.adapt` | Absorvido por `cli-compatibility.md` |
| `/hefesto.sync` | Desnecessario (create ja gera multi-CLI) |
| `/hefesto.show` | Absorvido por `/hefesto.list` |
| `/hefesto.delete` | Usuario pode deletar manualmente |
| `/hefesto.resume` | Sem wizard Python, sem necessidade |
| `/hefesto.detect` | Absorvido por `/hefesto.init` |

### 3. Por que auto-critica?

O sistema anterior nao tinha self-review. O AI gerava a skill e apresentava diretamente. Agora, o checklist de 10 itens forca o AI a revisar seu proprio output, corrigir falhas, e documentar correcoes antes do Human Gate. Isso e uma **melhoria** sobre o sistema anterior.

### 4. Ollama/Llama excluidos

Decisao do usuario: Ollama e modelos locais nao tem diretorio de skills proprio. O foco sao os 7 CLIs que suportam skill directories nativamente.

---

## Metricas de Impacto

| Metrica | v1.x | v2.0 |
|---------|------|------|
| Arquivos Python | 19 | 0 |
| Linhas de codigo Python | ~2500 | 0 |
| Comandos hefesto | 9 | 5 |
| Templates Markdown | ~600 linhas | ~750 linhas |
| Dependencias externas | Python 3.8+, PyYAML | Nenhuma |
| Skills existentes | 7+ | 7+ (inalteradas) |
| Speckit commands | 9 | 9 (inalterados) |
| Auto-critica | Nao | Sim (10 itens) |
| CLIs suportados | 7 | 7 |



