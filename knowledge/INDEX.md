# Hefesto Knowledge Base - Índice

**Versão**: 1.0.0  
**Última Atualização**: 2026-02-05  
**Propósito**: Base de conhecimento consolidada para geração de Agent Skills

---

## 📚 Estrutura

```
knowledge/
├── INDEX.md (este arquivo)
├── agent-skills-spec.md
├── mcp-protocol.md
├── best-practices/
│   ├── naming.md
│   ├── structure.md
│   ├── descriptions.md
│   ├── jit-resources.md
│   └── security.md
├── cli-specifics/
│   ├── claude-code.md
│   ├── gemini-cli.md
│   ├── codex.md
│   ├── copilot.md
│   ├── opencode.md
│   ├── cursor.md
│   └── qwen-code.md
├── patterns/
│   ├── code-review-skill.md
│   ├── testing-skill.md
│   ├── documentation-skill.md
│   └── refactoring-skill.md
└── research/
    ├── INDEX.md
    ├── ai-instruments.md
    ├── prompt-injection.md
    └── skill-generator-automatizado.md (completo)
```

---

## 🎯 Guias Rápidos

### Para Criar uma Skill
1. Consultar [agent-skills-spec.md](agent-skills-spec.md)
2. Seguir [best-practices/structure.md](best-practices/structure.md)
3. Verificar [best-practices/naming.md](best-practices/naming.md)
4. Aplicar [best-practices/security.md](best-practices/security.md)

### Para Adaptar para CLI Específico
1. Consultar CLI correspondente em `cli-specifics/`
2. Verificar [mcp-protocol.md](mcp-protocol.md) se aplicável
3. Seguir estrutura de [patterns/](patterns/)

### Para Pesquisa Acadêmica
1. Ver [research/INDEX.md](research/INDEX.md)
2. Papers citados em [research/skill-generator-automatizado.md](research/skill-generator-automatizado.md)

---

## 📖 Documentos Principais

### 1. Agent Skills Spec
**Arquivo**: [agent-skills-spec.md](agent-skills-spec.md)  
**Fonte**: https://agentskills.io  
**Conteúdo**: Especificação completa do padrão Agent Skills

### 2. Model Context Protocol (MCP)
**Arquivo**: [mcp-protocol.md](mcp-protocol.md)  
**Fonte**: https://modelcontextprotocol.io  
**Conteúdo**: Protocolo MCP para interoperabilidade

### 3. Research: Skill Generator Automatizado
**Arquivo**: [research/skill-generator-automatizado.md](research/skill-generator-automatizado.md)  
**Fontes**: 87 papers acadêmicos (IEEE, ACM, arXiv)  
**Conteúdo**: Pesquisa completa sobre geração automatizada de skills

---

## 🏷️ Best Practices (5 documentos)

| Arquivo | Tópico | Regras T0 |
|---------|--------|-----------|
| [naming.md](best-practices/naming.md) | Nomenclatura padronizada | T0-HEFESTO-07 |
| [structure.md](best-practices/structure.md) | Estrutura de skills | T0-HEFESTO-01 |
| [descriptions.md](best-practices/descriptions.md) | Descrições eficazes | T0-HEFESTO-01 |
| [jit-resources.md](best-practices/jit-resources.md) | Recursos JIT | T0-HEFESTO-03 |
| [security.md](best-practices/security.md) | Segurança | T0-HEFESTO-11 |

---

## 🔧 CLI Specifics (7 CLIs)

| CLI | Arquivo | Status | Versão |
|-----|---------|--------|--------|
| **Claude Code** | [claude-code.md](cli-specifics/claude-code.md) | ✅ Documentado | 2.1.31 |
| **Gemini CLI** | [gemini-cli.md](cli-specifics/gemini-cli.md) | ✅ Documentado | 0.27.0 |
| **Codex** | [codex.md](cli-specifics/codex.md) | ✅ Documentado | npm |
| **GitHub Copilot** | [copilot.md](cli-specifics/copilot.md) | ✅ Documentado | - |
| **OpenCode** | [opencode.md](cli-specifics/opencode.md) | ✅ Documentado | 1.1.48 |
| **Cursor** | [cursor.md](cli-specifics/cursor.md) | ✅ Documentado | 2.4.27 |
| **Qwen Code** | [qwen-code.md](cli-specifics/qwen-code.md) | ✅ Documentado | 0.9.0 |

---

## 🎨 Patterns (4 padrões comuns)

| Pattern | Arquivo | Caso de Uso |
|---------|---------|-------------|
| **Code Review** | [code-review-skill.md](patterns/code-review-skill.md) | Review automatizado de código |
| **Testing** | [testing-skill.md](patterns/testing-skill.md) | Geração de testes |
| **Documentation** | [documentation-skill.md](patterns/documentation-skill.md) | Geração de docs |
| **Refactoring** | [refactoring-skill.md](patterns/refactoring-skill.md) | Refatoração de código |

---

## 📚 Research Papers (87 citações)

Ver [research/INDEX.md](research/INDEX.md) para lista completa.

### Principais Papers
1. **AI-Instruments** (ACM DL) - Reificação da intenção
2. **Prompt Injection Attacks** (arXiv) - Segurança de agentes
3. **Multi-Agent Framework** (MDPI) - Frameworks multi-agente
4. **Trustworthy AI** (IEEE) - Auditabilidade e confiança

---

## 🔗 Links Úteis

### Documentação Oficial
- Agent Skills: https://agentskills.io
- Claude Code: https://code.claude.com/docs
- Gemini CLI: https://geminicli.com/docs
- MCP Protocol: https://modelcontextprotocol.io
- Qwen Code: https://qwenlm.github.io/qwen-code-docs/

### Frameworks & SDKs
- LangChain: https://docs.langchain.com/
- AutoGen: https://microsoft.github.io/autogen/
- CrewAI: https://docs.crewai.com
- Pydantic AI: https://ai.pydantic.dev

### Ferramentas de Pesquisa
- Perplexity: https://www.perplexity.ai
- Tavily: https://www.tavily.com/
- Learn Prompting: https://learnprompting.org/

---

## 📊 Estatísticas

| Métrica | Valor |
|---------|-------|
| **Total de Arquivos** | 20 |
| **Papers Citados** | 87 |
| **CLIs Documentados** | 7 |
| **Best Practices** | 5 |
| **Patterns** | 4 |
| **Linhas de Pesquisa** | ~3767 |

---

## 🔄 Atualização

Esta knowledge base é atualizada continuamente conforme:
- Novos CLIs surgem
- Especificações são atualizadas
- Novas pesquisas são publicadas
- Feedback da comunidade

**Última Revisão**: 2026-02-05  
**Próxima Revisão**: Trimestral

---

**Knowledge Base** | Hefesto Skill Generator | v1.0.0
