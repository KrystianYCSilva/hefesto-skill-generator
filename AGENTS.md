# AGENTS.md - Hefesto Skill Generator

> **Bootstrap para AI Agents**
> **Versao:** 2.2.0
> **Arquitetura:** Template-Driven (zero codigo, 100% Markdown)

---

## Quick Start

```
1. Ler este arquivo
2. Carregar templates/ (skill-template, quality-checklist, cli-compatibility)
3. Verificar .hefesto/version para estado da instalacao
```

---

## Arquitetura

Hefesto e um **spec-kit**: templates Markdown que o AI agent interpreta e executa.
Nao ha codigo Python, Node.js ou qualquer dependencia externa.

```
MARKDOWN TEMPLATES  ->  AI AGENT  ->  SKILLS (output)
      ^                                    |
  templates/                          .<cli>/skills/
  skill-template.md                   (7 CLIs)
  quality-checklist.md
  cli-compatibility.md
```

---

## Comandos Hefesto

| Comando | Descricao | Human Gate |
|---------|-----------|------------|
| `/hefesto.create` | Criar skill de descricao natural (6 fases + auto-critica) | Sim |
| `/hefesto.update` | Modificar conteudo de skills existentes (7 fases + diff) | Sim |
| `/hefesto.extract` | Extrair skill de codigo/docs existente | Sim |
| `/hefesto.agent` | Gerar agent especializado compondo skills (6 fases) | Sim |
| `/hefesto.validate` | Validar + corrigir skill contra spec (fix-auto) | Sim |
| `/hefesto.init` | Bootstrap: detectar CLIs, verificar instalacao | Nao |
| `/hefesto.list` | Listar todas as skills instaladas | Nao (read-only) |

---

## Human Gate Protocol

```
SEMPRE antes de persistir skills:
1. Gerar skill em memoria
2. Auto-Critica: checklist 13 itens (5 CRITICAL + 7 WARNING + 1 INFO)
3. Corrigir FAILs automaticamente
4. Apresentar preview ao usuario
5. Aguardar: [approve], [edit], [reject]
6. SO APOS aprovacao, persistir em todos CLIs detectados
```

---

## Quick Rules (T0)

| ID | Regra |
|----|-------|
| T0-HEFESTO-01 | TODA skill DEVE seguir Agent Skills spec (agentskills.io) |
| T0-HEFESTO-02 | NUNCA persistir sem Human Gate aprovado |
| T0-HEFESTO-03 | SKILL.md < 500 linhas, recursos JIT em sub-arquivos |
| T0-HEFESTO-04 | SEMPRE detectar CLIs antes de perguntar ao usuario |
| T0-HEFESTO-05 | Armazenar skills no projeto atual por padrao |
| T0-HEFESTO-12 | Auto-critica 13 pontos OBRIGATORIA antes de Human Gate |
| T0-HEFESTO-13 | Logica em Markdown, NUNCA em codigo executavel |

---

## References

| Preciso de... | Arquivo |
|---------------|---------|
| Template de skill | `templates/skill-template.md` |
| Template de agent | `templates/agent-template.md` |
| Checklist de qualidade | `templates/quality-checklist.md` |
| Regras multi-CLI | `templates/cli-compatibility.md` |
| Regras T0 completas | `CONSTITUTION.md` |
| Contexto do projeto | `.context/` |

---

**AGENTS.md** | Hefesto Skill Generator v2.0.0 | 2026-02-07
