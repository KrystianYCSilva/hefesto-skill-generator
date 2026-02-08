# CARD-003: Hefesto v2.2.0 - Update, Web Research, Sub-Agents, Payload Sync

## Status: PENDING

**Release Target:** v2.2.0
**Branch:** main
**Pre-requisitos:** V2.0.0 entregue (CARD-001, CARD-002 COMPLETED)

---

## 1. Descricao & Contexto

A V2.0.0 foi testada com Gemini CLI e revelou 4 necessidades:
- **Update**: Nao ha como modificar conteudo de skills existentes (so criar ou validar)
- **Web Research**: Agents alucinam URLs quando nao podem verificar via web search
- **Sub-Agents**: Nao ha como compor skills em agentes especializados
- **Payload Drift**: Comandos Gemini estao desatualizados (checklist 10 vs 13 pts, sem Token Economy)

**Filosofia**: Manter template-driven/zero-code (T0-HEFESTO-13). Tudo em Markdown.

---

## 2. Features

### Feature A: `/hefesto.update` (Novo Comando)

**Objetivo**: Modificar CONTEUDO de skills existentes. Diferente de `/hefesto.validate` que so corrige conformidade com a spec.

**7 Fases**:
1. **Selection** - Localizar skill existente nos CLIs
2. **Understanding** - Ler SKILL.md + references/ atuais + CONSTITUTION + templates
3. **Change Planning** - Parsear mudancas + web research condicional
4. **Apply Changes** - Gerar SKILL.md atualizado preservando estrutura agentskills.io
5. **Auto-Critica** - Checklist 13 pontos (mesmo do create)
6. **Human Gate** - Mostrar diff before/after + skill completa. [approve] [edit] [reject]
7. **Persistence** - Atualizar em TODOS CLIs detectados

**Input**: `$ARGUMENTS` como `<skill-name> <change-description>` ou so `<skill-name>`

---

### Feature B: Web Research Integration

**Objetivo**: Instruir agents a buscar na web sob demanda para verificar URLs e encontrar referencias autoritativas.

**Mudancas**:
- Adicionar step "Web Research (conditional)" na Phase 2 do `/hefesto.create`
- Adicionar step "Web Research (conditional)" na Phase 2 do `/hefesto.extract`
- Incluir mesma instrucao na Phase 3 do `/hefesto.update`

**Texto da instrucao**:
```markdown
**Web Research** (conditional):
- When you need to cite URLs, verify claims, or find authoritative references: USE web search
- NEVER invent or hallucinate URLs -- if you include a link, verify it exists
- If web search is unavailable, explicitly state: "References not verified via web search"
- Prefer official documentation URLs (language docs, RFC, MDN, etc.)
```

**Nova regra na CONSTITUTION**: T1-HEFESTO-03: Web Research

---

### Feature C: `/hefesto.agent` (Novo Comando + Template)

**Objetivo**: Gerar sub-agents compondo skills existentes em comandos com persona e workflow.

**Conceito-chave**: Agent = Comando Markdown que carrega Skills e segue um Workflow.

**6 Fases**:
1. **Understanding** - Parsear descricao do agent
2. **Skill Discovery** - Listar skills disponiveis, match com capabilities solicitadas
3. **Generation** - Gerar comando com persona + skill refs + workflow + rules
4. **Auto-Critica** - 7 checks especificos de agent
5. **Human Gate** - Apresentar agent completo
6. **Persistence** - Persistir como COMANDO em todos CLIs (nao como skill)

**Checklist Auto-Critica do Agent (7 pontos)**:

| # | Check | Severity |
|---|-------|----------|
| 1 | All referenced skills exist? | CRITICAL |
| 2 | Frontmatter has description? | CRITICAL |
| 3 | Persona is specific (not generic)? | WARNING |
| 4 | Workflow has sequential steps? | CRITICAL |
| 5 | Skill paths use correct CLI pattern? | CRITICAL |
| 6 | Agent is concise (< 200 lines)? | WARNING |
| 7 | No credentials, secrets, or PII? | CRITICAL |

**Formato do Agent gerado**:
```markdown
---
description: "<Purpose>. Composes skills: <skill-1>, <skill-2>."
---

# <Agent Name>

You are <persona>. You specialize in <domain>.

## Skills

Load these skills for context:
- Read `.<cli>/skills/<skill-1>/SKILL.md` for <capability-1>
- Read `.<cli>/skills/<skill-2>/SKILL.md` for <capability-2>

## Workflow

1. <Step 1>
2. <Step 2>

## Rules

- <Rule 1>
- <Rule 2>
```

**CLI-especifico**: Para GitHub Copilot, gerar TAMBEM `.github/agents/<name>.md` (formato nativo).

**IMPORTANTE**: O agent gerado NAO tem prefixo `hefesto.`. Ex: se o agent se chama `code-reviewer`, o comando fica `/<code-reviewer>`, nao `/hefesto.code-reviewer`.

---

### Feature D: Payload Sync (Fix Drift)

**Objetivo**: Sincronizar todos os payloads do installer com as versoes canonicas.

**Drift identificado**:

| Arquivo | Problema |
|---------|----------|
| `installer/payload/commands/gemini/hefesto.create.toml` | Checklist 10 pts (deve ser 13), sem Token Economy, usa `## Instructions/Key Concepts` ao inves de `## How to` |
| `installer/payload/commands/gemini/hefesto.extract.toml` | "10-point" (deve ser "13-point"), `<X>/10` (deve ser `<X>/13`) |
| `.claude/commands/hefesto.extract.md` | Linha 91: "10-point" (deve ser "13-point"), Linha 114: `<X>/10` (deve ser `<X>/13`) |
| `.gemini/commands/hefesto.create.toml` | Identico ao payload Gemini (mesmo drift) |
| `.gemini/commands/hefesto.extract.toml` | Identico ao payload Gemini (mesmo drift) |

---

## 3. Implementacao Step-by-Step

### Step 0: Governanca e Versao

**Arquivos a modificar**:

#### 0A. `CONSTITUTION.md`
- Bumpar versao do documento para 2.1.0
- Adicionar apos T1-HEFESTO-02 (linha ~248):

```markdown
### T1-HEFESTO-03: Web Research

**Regra:** Skills DEVEM usar web search para verificar URLs e encontrar referencias autoritativas quando disponivel.

**Diretrizes:**
- Ao citar URLs, SEMPRE verificar via web search antes de incluir
- NUNCA inventar URLs ou links
- Se web search indisponivel, declarar que referencias nao foram verificadas
```

- Adicionar na tabela de historico:

```markdown
| 2.1.0 | 2026-02-08 | Adicionado T1-HEFESTO-03 (Web Research), comandos update e agent |
```

#### 0B. `.hefesto/version`
- Alterar conteudo de `2.1.0` para `2.2.0`

#### 0C. `installer/install.ps1`
- Alterar `$HEFESTO_VERSION = "2.0.0"` para `$HEFESTO_VERSION = "2.2.0"` (linha ~17)

#### 0D. `installer/install.sh`
- Alterar variavel de versao para `"2.2.0"`

---

### Step 1: Web Research Integration

#### 1A. `.claude/commands/hefesto.create.md`
- Na Phase 2 (Research & Planning), APOS step 5 ("Research the skill's domain:"), adicionar novo step 6:

```markdown
6. **Web Research** (conditional):
   - When you need to cite URLs, verify claims, or find authoritative references: USE web search
   - NEVER invent or hallucinate URLs -- if you include a link, verify it exists
   - If web search is unavailable, explicitly state: "References not verified via web search"
   - Prefer official documentation URLs (language docs, RFC, MDN, etc.)
```

- Renumerar o step 6 existente ("Plan the skill structure") para step 7

#### 1B. `.claude/commands/hefesto.extract.md`
- Na Phase 2 (Analysis & Extraction), APOS step 4 ("Summarize extraction:"), adicionar step 5:

```markdown
5. **Web Research** (conditional):
   - When the source material references URLs, external docs, or third-party resources: USE web search to verify they exist
   - NEVER invent or hallucinate URLs -- if you include a link, verify it exists
   - If web search is unavailable, explicitly state: "References not verified via web search"
```

- **FIX DRIFT**: Linha 91: alterar "10-point quality checklist" para "13-point quality checklist"
- **FIX DRIFT**: Linha 114: alterar `<X>/10 PASS` para `<X>/13 PASS`

---

### Step 2: `/hefesto.update` - Criar Comando

#### 2A. Criar `.claude/commands/hefesto.update.md` (CANONICAL)

**Conteudo completo do comando** (seguir padrao de `hefesto.create.md`):

```
---
description: "Modify content of existing Agent Skills - add, remove, or change sections while preserving agentskills.io structure"
---

# /hefesto.update - Update Agent Skill

[7 fases conforme descrito na Feature A acima]
[Usar mesma estrutura de hefesto.create.md como referencia]
[Incluir web research na Phase 3]
[Incluir checklist 13 pontos na Phase 5]
[Human Gate na Phase 6 com diff before/after]
[Persistence na Phase 7 para todos CLIs]

## Rules
- NEVER persist changes without completing Phase 6 (Human Gate)
- NEVER skip Phase 5 (Auto-Critica)
- ALWAYS show before/after comparison to the user
- ALWAYS update ALL CLI directories, not just one
```

#### 2B. Propagar para 7 CLIs no repo

| Arquivo a criar | Formato | Variavel | Notas |
|-----------------|---------|----------|-------|
| `.gemini/commands/hefesto.update.toml` | TOML | `{{args}}` | Wrapper `description = "..." prompt = """..."""` |
| `.codex/prompts/hefesto.update.md` | MD + YAML | `$ARGUMENTS` | |
| `.github/agents/hefesto.update.agent.md` | MD + YAML | `$ARGUMENTS` | Conteudo completo |
| `.github/prompts/hefesto.update.prompt.md` | MD + YAML | - | Stub: `agent: hefesto.update` |
| `.opencode/command/hefesto.update.md` | MD + YAML | `$ARGUMENTS` | |
| `.cursor/commands/hefesto.update.md` | MD + YAML | `$ARGUMENTS` | |
| `.qwen/commands/hefesto.update.md` | MD + YAML | `{{args}}` | |

**Regras de adaptacao**:
- Corpo identico em todos CLIs
- `$ARGUMENTS` -> `{{args}}` para Gemini e Qwen
- Referencia de exemplar skill dir: `.claude/skills/` -> `.<cli>/skills/`
- Gemini: wrappear em TOML

#### 2C. Criar payload no installer

Mesmos 8 arquivos em `installer/payload/commands/`:
- `installer/payload/commands/claude/hefesto.update.md`
- `installer/payload/commands/gemini/hefesto.update.toml`
- `installer/payload/commands/codex/hefesto.update.md`
- `installer/payload/commands/github/agents/hefesto.update.agent.md`
- `installer/payload/commands/github/prompts/hefesto.update.prompt.md`
- `installer/payload/commands/opencode/hefesto.update.md`
- `installer/payload/commands/cursor/hefesto.update.md`
- `installer/payload/commands/qwen/hefesto.update.md`

---

### Step 3: `/hefesto.agent` - Criar Comando + Template

#### 3A. Criar `templates/agent-template.md`

Conteudo:
- Formato canonico de um agent command (frontmatter + persona + skills + workflow + rules)
- Regras: skills devem existir, paths CLI-aware, persona obrigatoria, workflow obrigatorio
- Mapeamento de onde persistir por CLI (commands dir)
- Nota especial: GitHub Copilot gera TAMBEM formato nativo em `.github/agents/<name>.md`

**Copiar para**:
- `.hefesto/templates/agent-template.md`
- `installer/payload/hefesto/templates/agent-template.md`

#### 3B. Criar `.claude/commands/hefesto.agent.md` (CANONICAL)

Conteudo completo do comando com 6 fases (conforme Feature C acima).

**Pontos criticos**:
- Phase 2 (Skill Discovery): DEVE listar skills e verificar que existem
- Phase 3: Gerar com paths corretos por CLI usando `templates/cli-compatibility.md`
- Phase 4: Checklist de 7 pontos especifico para agents
- Phase 6: Para Copilot, gerar TAMBEM `.github/agents/<name>.md`
- Agent gerado NAO tem prefixo `hefesto.`

#### 3C. Propagar para 7 CLIs + payload

Mesma tabela do Step 2B/2C mas para `hefesto.agent.*`

---

### Step 4: Payload Sync (Fix Drift)

#### 4A. Overhaul `hefesto.create.toml` do Gemini

**Arquivos**:
- `.gemini/commands/hefesto.create.toml`
- `installer/payload/commands/gemini/hefesto.create.toml`

**Mudancas necessarias** (comparar com `.claude/commands/hefesto.create.md` canonical):

1. **Phase 2**: Adicionar step de calibracao com "How to" e Token Economy + web research
2. **Phase 3**: SUBSTITUIR bloco inteiro da estrutura:
   - REMOVER: `## Instructions`, `## Key Concepts`, `## Examples`, `## References`
   - ADICIONAR: `## How to <first capability>`, `## How to <second capability>`, etc.
   - ADICIONAR: Token Economy table (Basic/Intermediate/Advanced/Project-specific)
   - ADICIONAR: Todas constraints do canonical (frontmatter strict, no "When to Use", etc.)
3. **Phase 4**: SUBSTITUIR checklist 10-point pelo 13-point com coluna Severity:

| # | Check | Severity | Result |
|---|-------|----------|--------|
| 1 | Frontmatter valid? | CRITICAL | ? |
| 2 | Frontmatter strict? (ONLY name + description) | CRITICAL | ? |
| 3 | Size limits? (< 500 lines, < ~5000 tokens) | CRITICAL | ? |
| 4 | Description quality? (action verb, "Use when:", specific) | CRITICAL | ? |
| 5 | No "When to Use" section in body? | WARNING | ? |
| 6 | Task-oriented sections? ("How to [task]") | WARNING | ? |
| 7 | Token Economy applied? | WARNING | ? |
| 8 | Concise? (no filler) | WARNING | ? |
| 9 | Examples only for non-obvious patterns? | WARNING | ? |
| 10 | Terminology consistent? | WARNING | ? |
| 11 | Degrees of freedom appropriate? | INFO | ? |
| 12 | Progressive disclosure? (references/ if > 200 lines) | WARNING | ? |
| 13 | No credentials, secrets, or PII? | CRITICAL | ? |

4. **Phase 5**: `<X>/10 PASS` -> `<X>/13 PASS`

#### 4B. Fix `hefesto.extract.toml` do Gemini

**Arquivos**:
- `.gemini/commands/hefesto.extract.toml`
- `installer/payload/commands/gemini/hefesto.extract.toml`

**Mudancas**:
- "10-point" -> "13-point"
- `<X>/10 PASS` -> `<X>/13 PASS`
- Adicionar web research step

#### 4C. Propagar create atualizado para TODOS os payload CLIs

Apos atualizar canonical `.claude/commands/hefesto.create.md` (Step 1A), propagar para:
- `installer/payload/commands/claude/hefesto.create.md` (copiar canonical)
- `installer/payload/commands/codex/hefesto.create.md` (adaptar se necessario)
- `installer/payload/commands/opencode/hefesto.create.md`
- `installer/payload/commands/cursor/hefesto.create.md`
- `installer/payload/commands/qwen/hefesto.create.md` (trocar $ARGUMENTS por {{args}})
- `installer/payload/commands/github/agents/hefesto.create.agent.md`

E para os CLIs live no repo:
- `.codex/prompts/hefesto.create.md`
- `.opencode/command/hefesto.create.md`
- `.cursor/commands/hefesto.create.md`
- `.qwen/commands/hefesto.create.md`
- `.github/agents/hefesto.create.agent.md`

#### 4D. Propagar extract atualizado para TODOS os payload CLIs

Mesmo processo do 4C mas para hefesto.extract.*

#### 4E. Verificar validate, init e list

Fazer cross-check rapido que validate, init e list estao consistentes em todos payloads. Se houver drift, corrigir.

---

### Step 5: Documentacao

#### 5A. `AGENTS.md`
- Bumpar versao para 2.2.0
- Adicionar `/hefesto.update` e `/hefesto.agent` na tabela de comandos
- "5 comandos" -> "7 comandos"
- Adicionar referencia a `templates/agent-template.md`

#### 5B. `docs/ARCHITECTURE.md`
- Bumpar versao para 2.2.0
- Adicionar fluxos de update (7 fases) e agent (6 fases)
- Atualizar tabela de comandos (5 -> 7)
- Atualizar estrutura do projeto

#### 5C. `templates/cli-compatibility.md`
- Adicionar secao "Agent-Specific Notes" com mapeamento de diretorios por CLI
- Nota: Copilot e o unico com formato nativo de agent
- Copiar atualizado para `.hefesto/templates/` e `installer/payload/hefesto/templates/`

---

## 4. Ordem de Execucao e Dependencias

```
Step 0: Governanca (CONSTITUTION, version)
  |
  v
Step 1: Web Research (modificar create + extract canonical)
  |
  v
Step 2: /hefesto.update (criar canonical + propagar)
  |
  v
Step 3: /hefesto.agent + template (criar + propagar)
  |
  v
Step 4: Payload Sync (fix Gemini + propagar tudo)
  |
  v
Step 5: Documentacao (AGENTS.md, ARCHITECTURE.md, cli-compatibility.md)
```

---

## 5. Verificacao

| Teste | Como Verificar |
|-------|---------------|
| Comandos visiveis | `/hefesto.list` deve mostrar 7 comandos na descricao |
| Drift zero | Comparar `.claude/commands/` com cada `installer/payload/commands/<cli>/` |
| Agent funcional | Executar `/hefesto.agent "code reviewer que compoe code-reviewer e testing-expert"` |
| Update funcional | Executar `/hefesto.update java-101 "adicionar secao sobre Java 21 virtual threads"` |
| Web research | Executar `/hefesto.create "mcp-server-development"` e verificar URLs validas |
| Gemini sync | Abrir `.gemini/commands/hefesto.create.toml` e verificar 13-point + Token Economy |

---

## 6. Riscos e Mitigacoes

| Risco | Impacto | Mitigacao |
|-------|---------|----------|
| TOML escaping no Gemini | Comando quebrado | Usar `"""..."""`, testar manualmente |
| GitHub dual-file confusion | Agent nao funciona | Gerar SEMPRE agent + prompt, documentar diferenca |
| Template em 3 locais | Desync | Copiar atomicamente para `.hefesto/templates/` e `installer/payload/` |
| Volume de arquivos (~50+) | Erro humano | Commitar por step, verificar a cada step |
| Agent referencia skill inexistente | Runtime error | Auto-critica CRITICAL check #1 |

---

## 7. Estimativa de Arquivos

| Categoria | Quantidade |
|-----------|-----------|
| Novos comandos (canonical) | 2 |
| Novos templates | 1 (+2 copias) |
| Propagacao CLI (repo) | 14 (7 por comando) |
| Propagacao payload (installer) | 16 (8 por comando) |
| Modificacoes em canonicals | 2 (create + extract) |
| Fix drift Gemini | 4 |
| Sync payload (create + extract) | ~20 |
| Documentacao | 3 |
| Governanca/versao | 3-4 |
| **TOTAL** | **~65 arquivos** |

---

## 8. Criterios de Aceite

- [ ] `/hefesto.update` operacional com 7 fases + Human Gate
- [ ] `/hefesto.agent` operacional com 6 fases + composicao de skills
- [ ] Web research integrado em create/extract/update
- [ ] ZERO drift entre canonical e payload
- [ ] Gemini com 13-point checklist + Token Economy + "How to" sections
- [ ] CONSTITUTION.md com T1-HEFESTO-03
- [ ] Versao 2.2.0 em todos os pontos
- [ ] Documentacao atualizada (AGENTS.md, ARCHITECTURE.md, cli-compatibility.md)
- [ ] `templates/agent-template.md` criado e copiado para 3 locais
