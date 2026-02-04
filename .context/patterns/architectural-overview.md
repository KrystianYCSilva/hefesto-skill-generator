# Architectural Overview - Hefesto Skill Generator

> **Tier:** T1 - Normativo
> **Versao:** 1.0.0

---

## 1. Visao Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────────────┐
│                        HEFESTO SKILL GENERATOR                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                      COMMAND LAYER                            │   │
│  │  /hefesto.create │ /hefesto.extract │ /hefesto.validate │...  │   │
│  └───────────────────────────┬──────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    PROCESSING ENGINE                          │   │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐ │   │
│  │  │  Template  │ │  Extract   │ │  Validate  │ │   Adapt    │ │   │
│  │  │  Processor │ │  Analyzer  │ │  Engine    │ │   Engine   │ │   │
│  │  └────────────┘ └────────────┘ └────────────┘ └────────────┘ │   │
│  └───────────────────────────┬──────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                      HUMAN GATE                               │   │
│  │  Preview → Validation Report → [approve|expand|edit|reject]   │   │
│  └───────────────────────────┬──────────────────────────────────┘   │
│                              │                                       │
│         ┌────────────────────┼────────────────────┐                 │
│         ▼                    ▼                    ▼                  │
│  ┌────────────┐       ┌────────────┐       ┌────────────┐           │
│  │  Approve   │       │   Expand   │       │   Reject   │           │
│  └─────┬──────┘       └─────┬──────┘       └────────────┘           │
│        │                    │                                        │
│        │                    ▼                                        │
│        │             ┌────────────┐                                  │
│        │             │   Wizard   │                                  │
│        │             │ Interactive│                                  │
│        │             └─────┬──────┘                                  │
│        │                   │                                         │
│        └───────────────────┘                                         │
│                    │                                                 │
│                    ▼                                                 │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                   MULTI-CLI GENERATOR                         │   │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────┐  │   │
│  │  │ Claude │ │ Gemini │ │ Codex  │ │Copilot │ │   Others   │  │   │
│  │  │Adapter │ │Adapter │ │Adapter │ │Adapter │ │  Adapters  │  │   │
│  │  └────────┘ └────────┘ └────────┘ └────────┘ └────────────┘  │   │
│  └───────────────────────────┬──────────────────────────────────┘   │
│                              │                                       │
│                              ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                      OUTPUT LAYER                             │   │
│  │  .claude/skills/ │ .gemini/skills/ │ .codex/skills/ │ ...    │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 2. Componentes Principais

### 2.1. Command Layer

**Responsabilidade:** Receber comandos do usuario e rotear para processadores.

| Comando | Processador | Descricao |
|---------|-------------|-----------|
| `/hefesto.create` | Template Processor | Criar skill de descricao |
| `/hefesto.extract` | Extract Analyzer | Criar skill de codigo |
| `/hefesto.validate` | Validate Engine | Validar skill existente |
| `/hefesto.adapt` | Adapt Engine | Adaptar para outro CLI |
| `/hefesto.sync` | Multi-CLI Generator | Sincronizar entre CLIs |
| `/hefesto.list` | Output Layer | Listar skills |

### 2.2. Processing Engine

**Responsabilidade:** Processar inputs e gerar skills.

#### Template Processor

```
Input: Descricao natural
Output: SKILL.md preenchido

Fluxo:
1. Carregar skill-template.md
2. Extrair conceitos da descricao
3. Preencher frontmatter (name, description)
4. Gerar instrucoes baseadas na descricao
5. Retornar skill para Human Gate
```

#### Extract Analyzer

```
Input: Arquivo(s) de codigo ou docs
Output: SKILL.md derivado

Fluxo:
1. Ler arquivo(s) especificado(s)
2. Identificar padroes, convencoes, boas praticas
3. Gerar name e description baseados no conteudo
4. Criar instrucoes que capturam os padroes
5. Retornar skill para Human Gate
```

#### Validate Engine

```
Input: SKILL.md existente
Output: Relatorio de validacao

Fluxo:
1. Carregar SKILL.md
2. Validar estrutura (frontmatter, secoes)
3. Validar contra Agent Skills spec
4. Validar qualidade (T1 rules)
5. Retornar relatorio
```

#### Adapt Engine

```
Input: SKILL.md + CLI alvo
Output: SKILL.md adaptado

Fluxo:
1. Carregar SKILL.md original
2. Carregar adapter do CLI alvo
3. Aplicar transformacoes (ex: $ARGUMENTS → {{args}})
4. Retornar skill adaptada para Human Gate
```

### 2.3. Human Gate

**Responsabilidade:** Controle de qualidade humano.

```
Input: Skill gerada/adaptada
Output: Decisao do usuario

Fluxo:
1. Apresentar preview da skill
2. Mostrar resultado da validacao
3. Apresentar opcoes: [approve] [expand] [edit] [reject]
4. Aguardar decisao
5. Rotear para proximo passo
```

### 2.4. Wizard Interactive

**Responsabilidade:** Expansao guiada de skills.

```
Input: Skill basica
Output: Skill expandida

Fluxo:
1. Perguntar sobre scripts necessarios
2. Perguntar sobre referencias
3. Perguntar sobre assets
4. Perguntar sobre CLIs adicionais
5. Expandir skill com base nas respostas
6. Retornar para Human Gate
```

### 2.5. Multi-CLI Generator

**Responsabilidade:** Gerar skill para multiplos CLIs.

```
Input: Skill aprovada
Output: Skills em diretorios de cada CLI

Fluxo:
1. Detectar CLIs instalados
2. Para cada CLI:
   a. Carregar adapter
   b. Aplicar transformacoes
   c. Criar diretorio de skill
   d. Salvar SKILL.md
   e. Salvar recursos JIT
3. Atualizar INDEX.md (se existir)
4. Reportar resultado
```

---

## 3. Fluxo de Dados

### 3.1. /hefesto.create

```
Usuario
   │
   │ "/hefesto.create Uma skill para code review"
   │
   ▼
Command Layer
   │
   │ Roteia para Template Processor
   │
   ▼
Template Processor
   │
   │ Gera SKILL.md
   │
   ▼
Validate Engine
   │
   │ Valida contra spec
   │
   ▼
Human Gate
   │
   │ [approve] selecionado
   │
   ▼
Multi-CLI Generator
   │
   │ Detecta: Claude, Gemini
   │ Gera: .claude/skills/code-review/
   │        .gemini/skills/code-review/
   │
   ▼
Output Layer
   │
   │ Reporta: "Skill criada em 2 CLIs"
   │
   ▼
Usuario
```

### 3.2. /hefesto.extract

```
Usuario
   │
   │ "/hefesto.extract @src/utils/validation.ts"
   │
   ▼
Command Layer
   │
   │ Roteia para Extract Analyzer
   │
   ▼
Extract Analyzer
   │
   │ Le arquivo, identifica padroes
   │ Gera SKILL.md
   │
   ▼
[Continua como /hefesto.create]
```

---

## 4. Estrutura de Diretorios

### 4.1. Projeto Hefesto

```
hefesto-skill-generator/
├── README.md
├── CONSTITUTION.md
├── MEMORY.md
├── AGENTS.md
│
├── .context/              # Para IAs
│
├── docs/                  # Para humanos
│
├── templates/             # Templates de skills
│   ├── skill-template.md
│   └── adapters/
│       ├── claude.adapter.md
│       ├── gemini.adapter.md
│       └── ...
│
├── commands/              # Definicoes de comandos
│   ├── hefesto.create.md
│   ├── hefesto.extract.md
│   └── ...
│
├── knowledge/             # Base de conhecimento
│   ├── agent-skills-spec.md
│   ├── best-practices.md
│   ├── cli-matrix.md
│   └── validation-rules.md
│
└── examples/              # Skills de exemplo
    ├── code-review/
    └── testing-strategy/
```

### 4.2. Skill Gerada

```
skill-name/
├── SKILL.md              # Core (obrigatorio, < 500 linhas)
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

## 5. Adapters

### 5.1. Adapter Base

```markdown
# Adapter: {CLI Name}

## Metadata
- CLI: {name}
- Directory: {.cli/skills/}
- Format: {SKILL.md | TOML}

## Transformations

### Arguments
- From: $ARGUMENTS
- To: {$ARGUMENTS | {{args}}}

### Format
- Primary: SKILL.md
- Alternative: {TOML | None}

## Directory Structure
{diretorio especifico}
```

### 5.2. Adapters Implementados

| CLI | Adapter | Transformacoes |
|-----|---------|----------------|
| Claude | claude.adapter.md | Nenhuma (nativo) |
| Gemini | gemini.adapter.md | `$ARGUMENTS` → `{{args}}` |
| Codex | codex.adapter.md | Nenhuma |
| Copilot | copilot.adapter.md | Nenhuma |
| OpenCode | opencode.adapter.md | Nenhuma |
| Cursor | cursor.adapter.md | Nenhuma |
| Qwen | qwen.adapter.md | `$ARGUMENTS` → `{{args}}` |

---

## 6. Extensibilidade

### 6.1. Adicionar Novo CLI

1. Criar adapter em `templates/adapters/{cli}.adapter.md`
2. Definir transformacoes necessarias
3. Adicionar deteccao em Multi-CLI Generator
4. Testar geracao

### 6.2. Adicionar Novo Comando

1. Criar definicao em `commands/hefesto.{comando}.md`
2. Definir fluxo de processamento
3. Implementar Human Gate se necessario
4. Documentar em README.md

---

**Ultima Atualizacao:** 2026-02-04
