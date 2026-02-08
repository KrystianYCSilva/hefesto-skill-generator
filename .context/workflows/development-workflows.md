# Development Workflows - Hefesto Skill Generator

> **Tier:** T2 - Informativo
> **Proposito:** Fluxos de trabalho para uso do Hefesto

---

## 1. Workflow: Criar Nova Skill

### 1.1. Via Descricao Natural

```
/hefesto.create "Validate email addresses using RFC 5322 regex patterns"
```

**Fases:**

```
Phase 1: Understanding    -> Parse descricao, extrair conceitos
Phase 2: Research         -> Ler templates, exemplars, docs oficiais
Phase 3: Generation       -> Gerar SKILL.md (agentskills.io spec)
Phase 4: Auto-Critica     -> Self-review contra checklist 13 pontos
Phase 5: Human Gate       -> Preview -> [approve] [edit] [reject]
Phase 6: Persistence      -> Escrever em TODOS os CLIs detectados
```

### 1.2. Via Extracao de Codigo

```
/hefesto.extract src/utils/validation.ts
```

**Fases:** Analise automatica -> gera SKILL.md -> continua como create (fases 4-6).

---

## 2. Workflow: Validar Skill Existente

```
/hefesto.validate validate-email
```

**Fluxo:**

```
1. Ler SKILL.md da skill alvo
2. Rodar checklist 13 pontos (5 CRITICAL + 7 WARNING + 1 INFO)
3. Classificar: PASS | PARTIAL (warnings) | FAIL (criticals)
4. Se FAIL ou PARTIAL:
   - Diagnostico detalhado com sugestoes
   - Opcoes: [fix-auto] [fix-manual] [skip]
   - fix-auto: gerar versao corrigida -> Human Gate -> persistir
5. Se PASS: reportar sucesso
```

---

## 3. Workflow: Listar Skills

```
/hefesto.list
```

Lista todas as skills instaladas no projeto, agrupadas por CLI.

---

## 4. Workflow: Verificar Instalacao

```
/hefesto.init
```

**Modo Verificacao** (se `.hefesto/version` existe):
- Mostra versao instalada
- Verifica templates (3 requeridos)
- Detecta CLIs e compara com comandos instalados
- Reporta status: `[OK]` ou `[NEEDS UPDATE]`

**Modo Bootstrap** (se `.hefesto/version` NAO existe):
- Informa para rodar installer primeiro (`install.sh` ou `install.ps1`)
- Oferece criar diretorios basicos como fallback

---

## 5. Comandos Rapidos

| Acao | Comando |
|------|---------|
| Criar skill | `/hefesto.create "descricao"` |
| Extrair de codigo | `/hefesto.extract arquivo` |
| Validar skill | `/hefesto.validate skill-name` |
| Verificar instalacao | `/hefesto.init` |
| Listar skills | `/hefesto.list` |

---

**Ultima Atualizacao:** 2026-02-07
