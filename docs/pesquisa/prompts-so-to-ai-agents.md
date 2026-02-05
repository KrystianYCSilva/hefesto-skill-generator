**1 INTRODUÇÃO**

O conceito de "Sistema Operacional de Prompts para Agentes de IA" (ou *Prompt Operating System*, abreviado como PromptOS) não é um termo formalizado em literatura acadêmica tradicional, mas sim uma metáfora arquitetônica emergente que descreve a infraestrutura organizacional e técnica necessária para gerenciar, orquestrar e executar prompts, habilidades (*skills*), personas e contextos de forma sistemática — especialmente em ambientes de programação paralela humano-agente, conforme documentado nas duas pesquisas fornecidas.

**2 O QUE É UM SISTEMA OPERACIONAL DE PROMPTS?**

Um Sistema Operacional de Prompts é uma camada de abstração que organiza os artefatos de comportamento de agentes de IA da mesma forma que um sistema operacional tradicional gerencia processos, memória e dispositivos. Ele fornece:

* Gerenciamento de contexto dinâmico  
* Orquestração de habilidades (*skills*)  
* Versionamento e isolamento de personas  
* Controle de acesso e segurança  
* Interface padronizada com múltiplos modelos (GPT, Claude, Qwen, etc.)

Esse “sistema operacional” permite que desenvolvedores tratem prompts como código, aplicando práticas de engenharia de software modernas: versionamento com Git, testes automatizados, CI/CD, revisão por pares e governança.**Fundamento teórico**: A ideia está alinhada com o paradigma de Desenvolvimento Dirigido por Especificação (SDD) descrito na primeira pesquisa, onde prompts, regras e habilidades são artefatos de software mantidos no repositório do projeto — funcionando como “manuais de IA” explícitos e versionáveis.

**3 COMO CRIAR E CONFIGURAR UM SISTEMA OPERACIONAL DE PROMPTS?**

Com base nas tendências de 2025–2026, um PromptOS eficaz pode ser construído usando os seguintes componentes-chave:

**3.1 ESTRUTURA DE ARQUIVOS PADRÃO**

Organize seu projeto com diretórios dedicados:

(Obs.: Em um trabalho ABNT, blocos de código ou longas citações devem ter fonte menor (ex: 10pt), espaçamento simples e recuo de 4cm da margem esquerda.)  
/projeto/  
├── .promptos/  
│   ├── personas/  
│   │   └── senior\_dev.yaml  
│   ├── skills/  
│   │   └── extract\_emails\_from\_excel.json  
│   ├── contexts/  
│   │   └── architectural-guidelines.md  
│   └── config.yaml          \# Configuração global do PromptOS  
├── src/  
└── tests/  
**3.2 ARQUIVO DE PERSONA (**personas/\*.yaml**)**

Define o comportamento persistente do agente:

(Obs.: Aplicar formatação de bloco de código/citação longa, conforme nota anterior.)  
name: "Senior Backend Engineer"  
description: "Specializes in Python, FastAPI, and PostgreSQL."  
rules:  
  \- "Always write type hints."  
  \- "Never modify files outside the current task scope."  
  \- "Prefer simplicity over cleverness."  
skills:  
  \- "refactor\_fastapi\_routes"  
  \- "generate\_pytest\_cases"  
context\_files:  
  \- ".promptos/contexts/backend\_standards.md"  
**3.3 ARQUIVO DE SKILL (**skills/\*.json**)**

Encapsula lógica reutilizável com interface bem definida:

(Obs.: Aplicar formatação de bloco de código/citação longa, conforme nota anterior.)  
{  
  "name": "refactor\_fastapi\_routes",  
  "description": "Refactor FastAPI route handlers to follow project conventions.",  
  "input\_schema": {  
    "type": "object",  
    "properties": { "file\_path": { "type": "string" } },  
    "required": \["file\_path"\]  
  },  
  "output\_schema": {  
    "type": "object",  
    "properties": {  
      "modified\_lines": { "type": "array", "items": { "type": "string" } }  
    }  
  },  
  "implementation": "./scripts/refactor\_fastapi.py"  
}  
**3.4 CONTEXTO DINÂMICO VIA RAG OU MCP**

Use Retrieval-Augmented Generation (RAG) ou o Model Context Protocol (MCP) para injetar contexto relevante em tempo real:

* Ferramentas como GitHub Copilot Agent, Claude Code, e Cursor já suportam MCP.  
* Exemplo: @docs/architecture.md ou \#selection (no Copilot) automaticamente injetam contexto no prompt.

**3.5 EXECUÇÃO ORQUESTRADA**

Utilize CLIs ou frameworks que atuam como “kernel” do PromptOS:

* GitHub Spec Kit: Workflow de 4 fases (Especificar → Planejar → Tarefas → Revisar).  
* Claude Code CLI: Permite comandos personalizados (/fix, /test) baseados em prompts armazenados.  
* AgentForge / LangGraph / Microsoft ADK: Frameworks para orquestrar fluxos multi-habilidade.

**4 PRINCIPAIS GUIAS, FUNDAMENTOS E FONTES**

**Tabela 1** – Fontes Acadêmicas e Técnicas.

| Fonte | Contribuição |
| ----- | ----- |
| \[Da Engenharia de Prompt à Especificação de Comportamento (2026)\] | Introduz o SDD (Specification-Driven Development) como evolução da engenharia de prompts; trata prompts como código versionável. |
| \[Da Instrução ao Agente Autônomo (2025–2026)\] | Define Engenharia de Contexto e Arquiteturas Cognitivas (ex: UMM, CCA) como base para sistemas robustos. |
| LLMOrbit: A Circular Taxonomy of LLMs (arXiv:2601.14053) | Classifica agentes por camadas cognitivas e operacionais. |
| Context Engineering for AI Agents in OSS (arXiv:2510.21413) | Mostra como projetos open-source usam arquivos .md para guiar agentes. |

**4.1 FERRAMENTAS E PLATAFORMAS REAIS (2025–2026)**

* GitHub Copilot Agent Mode: Usa Custom Instructions e suporte a MCP.  
* Cursor IDE: .cursorrules \+ modo Composer \= PromptOS nativo.  
* Anthropic Claude Code: Habilidades registráveis via API (/v1/skills) e comandos slash personalizáveis.  
* Alibaba Qwen \+ Model Studio: Ecossistema com Tools e workflows visuais.  
* Microsoft ADK \+ MCP: Permite criar agentes declarativos com TypeSpec.

**4.2 BLOGS E COMUNIDADES TÉCNICAS**

* Anthropic Docs: [Best Practices for Claude 4.x](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)  
* OpenAI Community: Discussões sobre developer vs instructions roles (GPT-5.2).  
* Dev.to / LinkedIn: Artigos como "Policy-Bound Personas via YAML & Markdown" (ai\_collab\_platform).  
* DigitalOcean / MarkTechPost: Comparativos entre Copilot, Cursor e Windsurf.

**5 PRINCÍPIOS FUNDAMENTAIS DE UM PROMPOS**

1. **Prompts são código** → Versione com Git.  
2. **Habilidades são funções** → Defina interfaces claras (input/output schemas).  
3. **Personas são perfis persistentes** → Não dependem de prompts ad-hoc.  
4. **Contexto é gerenciado, não colado** → Use RAG, MCP ou variáveis de ambiente (\#file, \#selection).  
5. **Teste tudo** → Automatize validação de saída com JSON Schema e testes de regressão.  
6. **Segurança por design** → Evite injeção de prompt; use camadas de colaboração antes da execução.

**6 PRÓXIMOS PASSOS PARA IMPLEMENTAÇÃO**

1. Crie um diretório .promptos no seu repositório.  
2. Defina uma persona base em YAML.  
3. Implemente 1–2 skills com esquemas JSON.  
4. Use o GitHub Spec Kit ou Claude Code para orquestrar tarefas.  
5. Integre testes automatizados no CI/CD (ex: validar se a saída do agente passa em um schema).  
6. Adote MCP para conectar ferramentas externas (bancos de dados, APIs, etc.).

**7 CONCLUSÃO**

O Sistema Operacional de Prompts não é um produto único, mas sim um paradigma arquitetural que emerge naturalmente quando equipes tratam a colaboração com IA como um sistema de software completo — com módulos, interfaces, estado e governança. Em 2026, essa abordagem é essencial para evitar o “caos de software” gerado por agentes não supervisionados e para escalar a programação paralela de forma segura, reprodutível e sustentável.  
