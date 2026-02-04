# AGENTS.md - Hefesto Skill Generator

> **Bootstrap para AI Agents**
> **Versao:** 1.0.0
> **Tier System:** Ativo

---

## Quick Start

**CRITICAL:** Antes de gerar codigo ou skills, carregar contexto de `/.context/`

```
1. Ler este arquivo
2. Carregar CONSTITUTION.md (T0)
3. Carregar .context/standards/architectural-rules.md (T0)
4. Verificar MEMORY.md para estado atual
```

---

## Tier System

| Tier | Arquivo | Autoridade |
|------|---------|------------|
| **T0** | `CONSTITUTION.md` | ABSOLUTA |
| **T0** | `/.context/standards/architectural-rules.md` | ABSOLUTA |
| **T1** | `/.context/standards/code-quality.md` | NORMATIVA |
| **T1** | `/.context/patterns/` | NORMATIVA |
| **T2** | `/.context/_meta/` | INFORMATIVA |
| **T3** | `/.context/examples/` | ILUSTRATIVA |

---

## Quick Rules (T0)

| ID | Regra |
|----|-------|
| T0-HEFESTO-01 | TODA skill DEVE seguir Agent Skills spec (agentskills.io) |
| T0-HEFESTO-02 | NUNCA persistir sem Human Gate aprovado |
| T0-HEFESTO-03 | SKILL.md < 500 linhas, recursos JIT em sub-arquivos |
| T0-HEFESTO-04 | SEMPRE detectar CLIs antes de perguntar ao usuario |
| T0-HEFESTO-05 | Armazenar skills no projeto atual por padrao |

---

## Comandos Disponiveis

| Comando | Descricao | Human Gate |
|---------|-----------|------------|
| `/hefesto.create` | Criar skill de descricao | Sim |
| `/hefesto.extract` | Extrair skill de codigo | Sim |
| `/hefesto.validate` | Validar skill existente | Nao |
| `/hefesto.adapt` | Adaptar para outro CLI | Sim |
| `/hefesto.sync` | Sincronizar entre CLIs | Sim |
| `/hefesto.list` | Listar skills | Nao |

---

## Human Gate Protocol

```
SEMPRE antes de persistir:
1. Gerar skill em memoria
2. Validar contra Agent Skills spec
3. Apresentar preview ao usuario
4. Aguardar: [approve], [expand], [edit], [reject]
5. SO APOS aprovacao, persistir
```

---

## State

Ler `MEMORY.md` para estado atual.

---

## References

| Preciso de... | Arquivo |
|---------------|---------|
| Regras T0 completas | `CONSTITUTION.md` |
| Guia para IAs | `.context/ai-assistant-guide.md` |
| Tech stack | `.context/_meta/tech-stack.md` |
| Exemplos | `.context/examples/` |
| Troubleshooting | `.context/troubleshooting/common-issues.md` |

---

**AGENTS.md** | Hefesto Skill Generator | 2026-02-04
