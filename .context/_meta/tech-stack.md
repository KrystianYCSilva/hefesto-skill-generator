# Tech Stack - Hefesto Skill Generator

> **Tier:** T2 - Informativo
> **Versao:** 1.0.0

---

## 1. Arquitetura

### Tipo de Sistema

**Prompt-Based System** - O Hefesto e um sistema baseado em prompts/templates que funciona via comandos em CLIs de IA.

### Componentes

```
┌─────────────────────────────────────────────────────────────┐
│                    Hefesto Skill Generator                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │  Commands   │  │  Templates  │  │  Knowledge Base     │  │
│  │  (/hefesto) │  │  (skill-    │  │  (agent-skills-spec │  │
│  │             │  │   template) │  │   best-practices)   │  │
│  └──────┬──────┘  └──────┬──────┘  └──────────┬──────────┘  │
│         │                │                     │             │
│         └────────────────┼─────────────────────┘             │
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                   Generation Engine                      ││
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────────┐││
│  │  │Template │ │Validator│ │Human    │ │Multi-CLI        │││
│  │  │Parser   │ │         │ │Gate     │ │Generator        │││
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────────────┘││
│  └─────────────────────────────────────────────────────────┘│
│                          │                                   │
│                          ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    Output (Skills)                       ││
│  │  .claude/ │ .gemini/ │ .codex/ │ .github/ │ .cursor/    ││
│  └─────────────────────────────────────────────────────────┘│
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. Stack Tecnica

### Core

| Componente | Tecnologia | Justificativa |
|------------|------------|---------------|
| Formato | Markdown + YAML | Padrao Agent Skills |
| Templates | Markdown com placeholders | Compatibilidade universal |
| Validacao | Regex + Schema | Conformidade com spec |

### Armazenamento

| Local | Uso |
|-------|-----|
| Projeto atual | Skills geradas por padrao |
| `~/.hefesto/` | Configuracoes globais (opcional) |

### Formatos Suportados

| Formato | Uso |
|---------|-----|
| Markdown (SKILL.md) | Formato primario |
| YAML | Frontmatter |
| TOML | Formato alternativo (Gemini/Qwen) |

---

## 3. CLIs Suportados

### Com Suporte Nativo Agent Skills

| CLI | Versao Min | Diretorio | Formato |
|-----|------------|-----------|---------|
| Claude Code | 1.0+ | `.claude/skills/` | SKILL.md |
| Gemini CLI | 0.20+ | `.gemini/skills/` | SKILL.md/TOML |
| OpenAI Codex | 0.90+ | `.codex/skills/` | SKILL.md |
| VS Code/Copilot | 1.100+ | `.github/skills/` | SKILL.md |
| OpenCode | 0.1+ | `.opencode/skills/` | SKILL.md |
| Cursor | 1.0+ | `.cursor/skills/` | SKILL.md |
| Qwen Code | 0.8+ | `.qwen/skills/` | SKILL.md/TOML |

### Adaptacoes Necessarias

| CLI | Adaptacao |
|-----|-----------|
| Gemini/Qwen | `$ARGUMENTS` → `{{args}}` |
| Gemini/Qwen | Suporte a TOML alternativo |

---

## 4. Estrutura de Arquivos

### Projeto Hefesto

```
hefesto-skill-generator/
├── README.md
├── CONSTITUTION.md           # T0 Rules
├── MEMORY.md                 # Estado persistente
├── AGENTS.md                 # Bootstrap para IAs
│
├── .context/                 # Contexto para IAs
│   ├── README.md
│   ├── ai-assistant-guide.md
│   ├── _meta/
│   ├── standards/
│   ├── patterns/
│   ├── examples/
│   ├── workflows/
│   └── troubleshooting/
│
├── docs/                     # Documentacao humana
│   ├── README.md
│   ├── cards/
│   ├── decisions/
│   └── ...
│
├── templates/                # Templates de skills
│   ├── skill-template.md
│   └── adapters/
│
├── commands/                 # Comandos /hefesto.*
│   ├── hefesto.create.md
│   ├── hefesto.extract.md
│   └── ...
│
├── knowledge/                # Base de conhecimento
│   ├── agent-skills-spec.md
│   ├── best-practices.md
│   └── ...
│
└── examples/                 # Skills de exemplo
    └── ...
```

### Skill Gerada

```
skill-name/
├── SKILL.md              # Core (obrigatorio)
├── scripts/              # Executaveis (opcional)
│   ├── validate.py
│   └── execute.sh
├── references/           # Docs detalhadas (opcional)
│   ├── REFERENCE.md
│   └── EXAMPLES.md
└── assets/               # Recursos estaticos (opcional)
    ├── templates/
    └── schemas/
```

---

## 5. Dependencias

### Runtime

| Dependencia | Tipo | Obrigatorio |
|-------------|------|-------------|
| CLI de IA (qualquer) | Runtime | Sim |
| Filesystem | Sistema | Sim |
| Git | Sistema | Nao (recomendado) |

### Desenvolvimento

| Dependencia | Uso |
|-------------|-----|
| Markdown parser | Validacao de templates |
| YAML parser | Validacao de frontmatter |

---

## 6. Integracao

### Com Sistemas Existentes

| Sistema | Integracao |
|---------|-----------|
| spec-kit | Comandos /speckit.* compativeis |
| itzamna-prompt-os | Estrutura .context/ compativel |
| prompts | Templates de skill compativeis |

### APIs Externas

Nenhuma API externa necessaria. Sistema completamente local.

---

**Ultima Atualizacao:** 2026-02-04
