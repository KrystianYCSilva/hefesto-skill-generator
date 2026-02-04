# Hefesto Skill Generator

> **Sistema de geracao de Agent Skills para multiplos CLIs de IA**

[![Version](https://img.shields.io/badge/version-1.0.0-blue)]()
[![Agent Skills](https://img.shields.io/badge/standard-Agent%20Skills-green)](https://agentskills.io)
[![License](https://img.shields.io/badge/license-MIT-green)]()

---

## O que e o Hefesto?

**Hefesto** e um gerador de skills que cria **Agent Skills** padronizadas para multiplos CLIs de IA, seguindo o padrao aberto [agentskills.io](https://agentskills.io) e as melhores praticas academicamente consolidadas.

### Por que Hefesto?

Na mitologia grega, **Hefesto** era o deus ferreiro que forjava ferramentas divinas. Assim como ele, este projeto forja "ferramentas" (skills) que empoderam agentes de IA a realizar tarefas especializadas.

---

## Funcionalidades

- **Padrao Agent Skills**: Segue a especificacao aberta agentskills.io
- **Multi-CLI**: Gera skills para Claude Code, Gemini CLI, Codex, OpenCode, Cursor, Qwen Code, VS Code/Copilot
- **Deteccao Automatica**: Identifica CLIs instalados e gera para todos
- **Template-First**: Inicia com templates, expande sob demanda
- **Human Gate**: Validacao humana antes de persistir
- **Wizard Interativo**: Expansao guiada para skills complexas
- **Extracao de Codigo**: Cria skills a partir de codigo/docs existentes
- **JIT Loading**: Recursos adicionais em sub-arquivos para otimizacao de contexto

---

## CLIs Suportados

| CLI | Suporte Nativo | Diretorio |
|-----|----------------|-----------|
| Claude Code | ✅ | `.claude/skills/<name>/` |
| Gemini CLI | ✅ | `.gemini/skills/<name>/` |
| OpenAI Codex | ✅ | `.codex/skills/<name>/` |
| VS Code/Copilot | ✅ | `.github/skills/<name>/` |
| OpenCode | ✅ | `.opencode/skills/<name>/` |
| Cursor | ✅ | `.cursor/skills/<name>/` |
| Qwen Code | ✅ | `.qwen/skills/<name>/` |

---

## Comandos

| Comando | Descricao |
|---------|-----------|
| `/hefesto.create` | Cria skill a partir de descricao natural |
| `/hefesto.extract` | Extrai skill de codigo/docs existente |
| `/hefesto.validate` | Valida skill contra Agent Skills spec |
| `/hefesto.adapt` | Adapta skill para outro CLI |
| `/hefesto.sync` | Sincroniza skill entre CLIs |
| `/hefesto.list` | Lista skills do projeto |

### Uso Basico

```bash
# Criar nova skill via descricao
/hefesto.create Uma skill para padronizar code reviews seguindo boas praticas

# Extrair skill de codigo existente
/hefesto.extract @src/utils/validation.ts

# Validar skill existente
/hefesto.validate code-review

# Listar skills do projeto
/hefesto.list
```

---

## Estrutura de uma Skill Gerada

```
skill-name/
├── SKILL.md              # Core (<500 linhas, <5000 tokens)
├── scripts/              # Codigo executavel
│   ├── validate.py
│   └── execute.sh
├── references/           # Documentacao detalhada
│   ├── REFERENCE.md
│   └── EXAMPLES.md
└── assets/               # Recursos estaticos
    ├── templates/
    └── schemas/
```

---

## Template de Skill (Agent Skills Standard)

```yaml
---
name: skill-id
description: |
  Descricao de 1-3 linhas sobre o que a skill faz.
  Use quando: casos de uso especificos.
license: MIT
compatibility: Claude Code, Gemini CLI, Codex, OpenCode, Cursor, Qwen Code, VS Code/Copilot
metadata:
  author: seu-nome
  version: "1.0.0"
  category: development
  tags: [tag1, tag2]
---

# Skill Name

> One-liner description

## When to Use

- ✅ Cenario 1
- ✅ Cenario 2
- ❌ Quando NAO usar

## Instructions

[Instrucoes detalhadas...]

## References

- [Detailed Reference](references/REFERENCE.md)
- [Examples](references/EXAMPLES.md)
```

---

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                    /hefesto.create <descricao>                   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 1: TEMPLATE-FIRST                                         │
│  ├── Carregar skill-template.md                                 │
│  ├── Extrair conceitos-chave da descricao                       │
│  └── Gerar SKILL.md inicial                                     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 2: HUMAN GATE (Validacao)                                 │
│  ├── Apresentar skill gerada                                    │
│  ├── Validar contra Agent Skills spec                           │
│  └── Opcoes: [approve] [expand] [edit] [reject]                 │
└─────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼─────────────────┐
            ▼                 ▼                 ▼
      [approve]          [expand]           [reject]
            │                 │                 │
            │                 ▼                 │
            │  ┌──────────────────────────────┐ │
            │  │ FASE 3: WIZARD INTERATIVO   │ │
            │  │ ├── Perguntar sobre scripts │ │
            │  │ ├── Perguntar sobre refs    │ │
            │  │ └── Perguntar sobre CLIs    │ │
            │  └──────────────────────────────┘ │
            │                 │                 │
            ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────┐
│  FASE 4: GERACAO MULTI-CLI                                      │
│  ├── Detectar CLIs instalados                                   │
│  ├── Gerar estrutura para cada CLI                              │
│  └── Criar sub-arquivos JIT                                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Documentacao

| Documento | Descricao |
|-----------|-----------|
| [CONSTITUTION.md](./CONSTITUTION.md) | Regras invioaveis do sistema |
| [.context/](./. context/) | Contexto para IAs |
| [docs/](./docs/) | Documentacao para humanos |
| [docs/cards/](./docs/cards/) | CARDs de implementacao |

---

## Links Uteis

### Documentacao dos CLIs

| CLI | Documentacao |
|-----|--------------|
| Agent Skills Spec | https://agentskills.io |
| Claude Code | https://docs.anthropic.com/en/docs/claude-code/skills |
| Gemini CLI | https://geminicli.com |
| OpenAI Codex | https://developers.openai.com/codex |
| VS Code/Copilot | https://code.visualstudio.com/docs/copilot/customization/agent-skills |
| OpenCode | https://opencode.ai |
| Cursor | https://docs.cursor.com |
| Qwen Code | https://github.com/QwenLM/qwen-code |

---

## Contribuindo

1. Leia o [CONSTITUTION.md](./CONSTITUTION.md)
2. Siga as regras T0 em `.context/standards/architectural-rules.md`
3. Crie um CARD em `docs/cards/` antes de implementar
4. Valide contra a spec Agent Skills

---

## Licenca

MIT License - veja [LICENSE](./LICENSE) para detalhes.

---

**Hefesto Skill Generator** | Forjando ferramentas para agentes de IA | 2026
