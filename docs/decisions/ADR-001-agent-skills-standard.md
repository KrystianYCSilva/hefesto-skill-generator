# ADR-001: Agent Skills como Padrao Primario

**Status:** Aceito
**Data:** 2026-02-04
**Autores:** Hefesto Team

---

## Contexto

Existem multiplos formatos de skills/comandos entre diferentes CLIs de IA:

- Claude Code: SKILL.md com frontmatter YAML
- Gemini CLI: SKILL.md ou TOML
- OpenAI Codex: SKILL.md
- VS Code/Copilot: SKILL.md (Agent Skills)
- Cada CLI tem suas particularidades

Precisavamos escolher um padrao para o Hefesto que:
1. Seja bem documentado
2. Suporte multiplos CLIs
3. Seja extensivel
4. Tenha comunidade ativa

---

## Decisao

Adotar [agentskills.io](https://agentskills.io) como formato primario para todas as skills geradas pelo Hefesto.

---

## Consequencias

### Positivas

- **Padrao aberto:** Especificacao publica e bem documentada
- **Multi-CLI:** Suportado por Claude Code, Gemini CLI, Codex, VS Code/Copilot, OpenCode, Cursor, Qwen Code
- **Comunidade:** Adotado por grandes players (Anthropic, Google, OpenAI, Microsoft)
- **Validacao:** Biblioteca de referencia disponivel para validacao
- **Extensibilidade:** Permite metadados customizados

### Negativas

- **Adaptacoes:** CLIs que nao suportam nativamente precisam de adapters
- **Limitacoes:** Algumas features CLI-especificas nao estao na spec (ex: context:fork do Claude)
- **Dependencia:** Mudancas na spec podem afetar Hefesto

---

## Alternativas Consideradas

### Alternativa 1: Formato Proprietario

**Descricao:** Criar formato proprio do Hefesto.

**Por que rejeitada:** 
- Reinventar a roda
- Nao aproveitaria suporte nativo dos CLIs
- Mais trabalho de manutencao

### Alternativa 2: Multiplos Formatos Nativos

**Descricao:** Gerar em formato nativo de cada CLI.

**Por que rejeitada:**
- Complexidade de manter multiplos formatos
- Dificuldade de sincronizacao
- Agent Skills ja e suportado pela maioria

---

## Referencias

- [Agent Skills Specification](https://agentskills.io/specification)
- [Claude Code Skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [GitHub Agent Skills](https://github.com/agentskills/agentskills)

---

**Ultima Atualizacao:** 2026-02-04
