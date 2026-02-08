# AGENTS.md - Hefesto Skill Generator

> **Bootstrap para AI Agents**
> **Versao:** 2.0.0
> **Arquitetura:** Template-Driven (zero codigo, 100% Markdown)

---

## Quick Start

```
1. Ler este arquivo
2. Carregar CONSTITUTION.md (T0 - regras absolutas)
3. Templates em templates/ (skill-template, quality-checklist, cli-compatibility)
```

---

## Arquitetura

Hefesto e um **spec-kit**: templates Markdown que o AI agent interpreta e executa.
Nao ha codigo Python, Node.js ou qualquer dependencia externa.

```
COMANDOS (Markdown)  →  AI AGENT (interpreta)  →  SKILLS (output)
      ↑                       ↑                        ↓
  templates/              CONSTITUTION.md        .<cli>/skills/
  quality-checklist       (regras T0)            (7 CLIs)
  cli-compatibility
```

---

## Comandos Hefesto

| Comando | Descricao | Human Gate |
|---------|-----------|------------|
| `/hefesto.create` | Criar skill de descricao natural (6 fases + auto-critica) | Sim |
| `/hefesto.validate` | Validar skill contra Agent Skills spec | Nao (read-only) |
| `/hefesto.extract` | Extrair skill de codigo/docs existente | Sim |
| `/hefesto.init` | Bootstrap: detectar CLIs, criar diretorios | Nao |
| `/hefesto.list` | Listar todas as skills instaladas | Nao (read-only) |

### Comandos Spec-Kit (inalterados)

| Comando | Descricao |
|---------|-----------|
| `/speckit.specify` | Criar spec de feature |
| `/speckit.clarify` | Clarificar spec com perguntas |
| `/speckit.plan` | Gerar plano de implementacao |
| `/speckit.tasks` | Gerar tasks de implementacao |
| `/speckit.implement` | Executar tasks |
| `/speckit.analyze` | Analisar consistencia |
| `/speckit.checklist` | Gerar checklist |
| `/speckit.constitution` | Gerenciar constituicao |
| `/speckit.taskstoissues` | Converter tasks em GitHub issues |

---

## Human Gate Protocol

```
SEMPRE antes de persistir skills:
1. Gerar skill em memoria
2. Auto-Critica: checklist 10 itens (T0-HEFESTO-12)
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
| T0-HEFESTO-12 | Auto-critica OBRIGATORIA antes de Human Gate |
| T0-HEFESTO-13 | Logica em Markdown, NUNCA em codigo executavel |

---

## References

| Preciso de... | Arquivo |
|---------------|---------|
| Regras T0 completas | `CONSTITUTION.md` |
| Template de skill | `templates/skill-template.md` |
| Checklist de qualidade | `templates/quality-checklist.md` |
| Regras multi-CLI | `templates/cli-compatibility.md` |
| Knowledge base | `knowledge/` |
| Contexto do projeto | `.context/` |

---

**AGENTS.md** | Hefesto Skill Generator | 2026-02-07
