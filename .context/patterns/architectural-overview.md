# Architectural Overview - Hefesto Skill Generator

> **Tier:** T1 - Normativo
> **Versao:** 2.2.0
---

## 1. Visao Geral da Arquitetura

```
MARKDOWN TEMPLATES  ->  AI AGENT  ->  SKILLS (output)
                         ^
                    skill-template.md
                    quality-checklist.md
                    cli-compatibility.md
```

Hefesto e um **spec-kit template-driven**: zero Python, toda logica em Markdown templates que a IA interpreta diretamente.

---

## 2. Componentes Principais

### 2.1. Command Layer

5 comandos disponibilizados para cada CLI detectado:

| Comando | Descricao | Human Gate |
|---------|-----------|------------|
| `/hefesto.create` | Criar skill de descricao natural | Sim |
| `/hefesto.validate` | Validar + corrigir skill contra spec | Sim (fix-auto) |
| `/hefesto.extract` | Extrair skill de codigo/docs | Sim |
| `/hefesto.init` | Bootstrap: detectar CLIs, verificar instalacao | Nao |
| `/hefesto.list` | Listar skills instaladas | Nao (read-only) |

### 2.2. Template System

Templates sao a fonte de verdade:

| Template | Responsabilidade |
|----------|-----------------|
| `skill-template.md` | Estrutura canonica de skill (frontmatter + body) |
| `quality-checklist.md` | Auto-critica 13 pontos (5 CRITICAL + 7 WARNING + 1 INFO) |
| `cli-compatibility.md` | Mapa de CLIs, diretorios e adaptacoes |

### 2.3. Human Gate

Todas as operacoes de escrita passam pelo Human Gate:

```
Skill gerada/corrigida -> Preview + Auto-Critica -> [approve|edit|reject] -> Persistencia multi-CLI
```

### 2.4. Installer

Bootstrap portatil para qualquer projeto:

- `install.sh` (Bash 3.2+ - macOS/Linux/Git Bash)
- `install.ps1` (PowerShell 5.1+ - Windows)

O installer detecta CLIs, cria `.hefesto/`, copia comandos, cria skills dirs.

### 2.5. Multi-CLI Generator

Gera skill em todos os CLIs detectados simultaneamente, com adaptacoes automaticas de formato e syntax.

---

## 3. Fluxo de Dados

### 3.1. /hefesto.create (6 fases)

```
Usuario -> Descricao natural
    |
Phase 1: Understanding    -> Parse, extrair conceitos
Phase 2: Research         -> Ler templates, exemplars
Phase 3: Generation       -> Gerar SKILL.md (agentskills.io spec)
Phase 4: Auto-Critica     -> Checklist 13 pontos
Phase 5: Human Gate       -> [approve] [edit] [reject]
Phase 6: Persistence      -> Escrever em TODOS os CLIs detectados
```

### 3.2. /hefesto.validate (com fix-auto)

```
Usuario -> /hefesto.validate skill-name
    |
1. Ler SKILL.md
2. Rodar checklist 13 pontos
3. Classificar: PASS | PARTIAL | FAIL
4. Se problemas: [fix-auto] [fix-manual] [skip]
5. fix-auto -> gerar correcao -> Human Gate -> persistir
```

### 3.3. /hefesto.extract

```
Usuario -> @arquivo(s)
    |
Analisar padroes -> Gerar SKILL.md -> [continua como create]
```

---

## 4. Estrutura de Diretorios

### 4.1. Repositorio Hefesto

```
hefesto-skill-generator/
  README.md
  templates/                    # Templates fonte (fonte de verdade)
    skill-template.md
    quality-checklist.md
    cli-compatibility.md
  installer/                    # Pacote distribuivel
    install.sh / install.ps1
    payload/
      hefesto/templates/        # -> .hefesto/templates/
      commands/{cli}/           # -> .<cli>/commands/
  .claude/commands/hefesto.*    # 5 comandos (canonicos)
  .gemini/commands/hefesto.*    # 5 comandos (TOML)
  .codex/prompts/hefesto.*     # 5 comandos
  .github/agents/ + prompts/   # 5 comandos (Copilot)
  .opencode/command/hefesto.*  # 5 comandos
  .cursor/commands/hefesto.*   # 5 comandos
  .qwen/commands/hefesto.*     # 5 comandos
  .github/workflows/release.yml
```

### 4.2. Projeto do Usuario (apos install)

```
meu-projeto/
  .hefesto/
    version                    # "2.0.0"
    templates/                 # 3 templates
  .<cli>/
    commands/hefesto.*         # 5 comandos por CLI
    skills/                    # Skills geradas aqui
```

### 4.3. Skill Gerada

```
skill-name/
  SKILL.md              # Core (obrigatorio, < 500 linhas)
  references/           # Docs detalhadas (opcional, JIT loaded)
  scripts/              # Executaveis (opcional)
  assets/               # Recursos estaticos (opcional)
```

---

## 5. Adapters (via cli-compatibility.md)

| CLI | Adaptacoes |
|-----|-----------|
| Claude/Codex/OpenCode/Cursor | Nenhuma (nativo `$ARGUMENTS`, `.md`) |
| Gemini | `.toml` format, `{{args}}` syntax |
| Qwen | `{{args}}` syntax |
| Copilot | `.github/` namespace, agents + prompts |

---

## 6. Extensibilidade

### Adicionar Novo CLI

1. Adicionar regras em `templates/cli-compatibility.md`
2. Criar 5 comandos no formato do CLI
3. Atualizar `installer/` (scripts + payload)

### Adicionar Novo Comando

1. Criar `hefesto.{cmd}.md` para Claude (canonico)
2. Propagar para os 6 CLIs restantes
3. Atualizar `installer/payload/commands/`

---

**Ultima Atualizacao:** 2026-02-07



