# ADR-002: Integracao de Pesquisa Academica e Tecnica

**Status:** Aceito
**Data:** 2026-02-04
**Autores:** AI Agent + Human Review

---

## Contexto

Durante o planejamento do Hefesto Skill Generator, foi conduzida uma pesquisa academica abrangente documentada em `skill-generator-automatizado.md`. Esta pesquisa analisou:

- Literatura academica (IEEE, ACM) sobre agentes agênticos
- Documentacao oficial de 7 CLIs de IA
- Protocolos emergentes (MCP - Model Context Protocol)
- Melhores praticas de seguranca e verificabilidade

A pesquisa identificou gaps entre as melhores praticas academicas/industriais e o plano inicial do Hefesto.

---

## Decisao

Integrar os insights da pesquisa ao plano do Hefesto atraves de:

### 1. Nova Regra T0: Seguranca Intrinseca

**T0-HEFESTO-11: Seguranca por Padrao**

Skills DEVEM ser projetadas com seguranca intrinseca:
- Validacao de entradas contra injecao de prompts
- Principio do menor privilegio para acesso a recursos
- Sanitizacao de outputs antes de execucao

**Fonte:** "Prompt Injection Attacks on Agentic Coding Assistants" [28]

### 2. Suporte a MCP (Model Context Protocol)

O MCP e um protocolo emergente usado por:
- Gemini CLI
- OpenAI Codex
- GitHub Copilot (via GitHub MCP Server)
- Cursor (como cliente)

**Decisao:** Adicionar adapter MCP como formato de saida alternativo, permitindo que skills sejam expostas como MCP Servers.

**Fonte:** MCP Deep Dive [25], MCP Explained [69]

### 3. Metadados Expandidos

Alem dos campos obrigatorios Agent Skills (`name`, `description`), adicionar campos recomendados:

| Campo | Obrigatorio | Descricao |
|-------|-------------|-----------|
| `name` | Sim (T0) | Nome unico da skill |
| `description` | Sim (T0) | Descricao detalhada |
| `author` | Recomendado | Autor/organizacao |
| `version` | Recomendado | Versao SemVer |
| `license` | Recomendado | Licenca (MIT, Apache-2.0) |
| `category` | Recomendado | Categoria principal |
| `tags` | Recomendado | Tags para descoberta |
| `dependencies` | Recomendado | Dependencias externas |
| `platforms` | Recomendado | CLIs suportados |
| `example_prompt` | Recomendado | Exemplo de invocacao |

**Fonte:** Teorias de Interacao Generativa [8], AI-Instruments [2]

### 4. Arquitetura Motor + Drivers

Formalizar a arquitetura do Hefesto:

```
┌─────────────────────────────────────────┐
│         Motor de Geracao Central        │
│  (Processa schema abstrato da skill)    │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
    v             v             v
┌────────┐  ┌──────────┐  ┌─────────┐
│ Driver │  │  Driver  │  │ Driver  │
│ Claude │  │  Gemini  │  │   MCP   │
└────────┘  └──────────┘  └─────────┘
    │             │             │
    v             v             v
┌────────┐  ┌──────────┐  ┌─────────┐
│manifest│  │{{args}}  │  │MCP      │
│.json   │  │ syntax   │  │Server   │
└────────┘  └──────────┘  └─────────┘
```

### 5. Referencias Academicas na Knowledge Base

Incluir na knowledge base referencias a:
- AI-Instruments (ACM DL) - Reificacao da intencao
- Prompt Injection Attacks - Seguranca
- Multi-Agent Frameworks - Arquitetura
- Trustworthy AI - Auditabilidade

---

## Consequencias

### Positivas

- **Fundamentacao solida:** Plano baseado em literatura academica revisada
- **Seguranca proativa:** Regra T0 previne vulnerabilidades desde o design
- **Interoperabilidade:** Suporte MCP amplia compatibilidade futura
- **Descoberta:** Metadados expandidos facilitam busca e selecao de skills

### Negativas

- **Complexidade:** Mais campos de metadados para preencher
- **Escopo:** Adapter MCP adiciona trabalho ao CARD-002
- **Dependencia:** MCP ainda e protocolo em evolucao

---

## Alternativas Consideradas

### Alternativa 1: Ignorar pesquisa
**Descricao:** Manter plano original sem integrar insights.
**Por que rejeitada:** Perderia oportunidade de fundamentacao academica e gaps de seguranca.

### Alternativa 2: Criar projeto separado para MCP
**Descricao:** Hefesto focaria apenas em Agent Skills, MCP seria outro projeto.
**Por que rejeitada:** Fragmentaria esforcos e duplicaria trabalho de templates.

### Alternativa 3: Integrar tudo como obrigatorio
**Descricao:** Todos os 11 campos de metadados como T0.
**Por que rejeitada:** Aumentaria atrito para criacao de skills simples.

---

## Referencias

### Literatura Academica

| Ref | Titulo | Fonte |
|-----|--------|-------|
| [2] | AI-Instruments: Embodying Prompts | ACM DL |
| [8] | Generative Theories of Interaction | ACM DL |
| [28] | Prompt Injection Attacks on Agentic Coding Assistants | arXiv |
| [29] | Trustworthy and Explainable AI | IEEE |

### Documentacao Tecnica

| Ref | Recurso | URL |
|-----|---------|-----|
| [23] | GitHub MCP Server | docs.github.com |
| [25] | MCP Deep Dive | blog.csdn.net |
| [69] | MCP Explained | 53ai.com |

### Documentos Internos

- CONSTITUTION.md - Regras T0
- CARD-002-templates.md - Sistema de templates
- CARD-006-knowledge-base.md - Base de conhecimento
- skill-generator-automatizado.md - Pesquisa completa

---

**ADR-002** | Hefesto Skill Generator | Aceito em 2026-02-04
