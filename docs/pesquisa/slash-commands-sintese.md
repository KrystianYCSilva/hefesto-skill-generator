# Síntese da Pesquisa: Comandos Slash em CLIs de IA para Programação

## Visão Geral

Comandos slash (`/`) em CLIs de IA para código funcionam como:
- **roteadores semânticos**
- **atalhos de prompt estruturado**
- **gatilhos de pipelines internos**
- **interfaces de extensão (quando suportado)**

Arquiteturalmente, quase todas seguem este fluxo:
```
Input do usuário
└── Parser de linha
└── Detector de prefixo "/"
└── Command Registry
├── Handler interno
├── Prompt Template
├── Tool / Agent
└── Output Renderer
```

Importante: **nem toda CLI permite adicionar slash commands customizados**. Na maioria dos casos, apenas **desenvolvedores da ferramenta** podem.

## Análise por Plataforma

### Claude Code / Claude CLI (Anthropic)

**Funcionamento:**
- Slash commands são **mapeamentos internos para prompts especializados**
- Ex: `/explain`, `/fix`, `/tests`, `/doc`
- Cada comando ativa:
  - um **prompt template**
  - um **context loader**
  - ferramentas internas (code analysis, diff, etc.)

**Extensibilidade:**
- **Híbrido: Skills e Comandos via Markdown**
- Arquivos Markdown em diretórios `.claude/commands/` agora aparecem como comandos slash personalizados
- O nome do arquivo determina o nome do comando invocado (ex: `commit.md` torna-se `/commit`)
- Configuração via metadados em YAML (frontmatter)
- Suporte a "Hooks" para automação de workflows

**Campos de metadados:**
- `description`: Resumo exibido no menu /help
- `argument-hint`: Guia de argumentos exibido no autocompletar
- `model`: Identificador do modelo para execução específica
- `allowed-tools`: Lista de ferramentas que o comando tem permissão para usar
- `disable-model-invocation`: Impede que o agente invoque o comando autonomamente

### Qwen Code CLI (Alibaba)

**Funcionalidades:**
- Sistema de extensibilidade mais explícito e modular
- Arquivos Markdown em `.qwen/commands/*.md` criam comandos personalizados
- Sistema de gerenciamento de extensões via comando `/extensions`
- Suporte à "recarga em tempo real" (hot reload)
- Integração com servidores Model Context Protocol (MCP)
- Capacidade de converter plugins de outros ecossistemas

**Características:**
- Extensibilidade baseada em plugins e arquivos
- Suporte a agentes secundários personalizados
- Resolução de conflitos de nomes automática
- Recursos avançados de integração via MCP

### Cursor IDE / Cursor CLI

**Abordagem:**
- **IDE-first**, não CLI-first
- Personalização via "User Rules" (Regras de Usuário)
- Comandos slash são "gatilhos" que expandem para instruções completas
- Configuração através da interface de configurações do editor

**Funcionalidades:**
- Criação de "Team Commands" via painel administrativo
- Mapeamento de atalhos para ferramentas de agente
- Tipos de regras: Always Apply, Apply Intelligently, Globs Pattern, Manual

### GitHub Copilot CLI

**Estratégia:**
- Foco em interoperabilidade via Model Context Protocol (MCP)
- Extensibilidade baseada em "Custom Instructions" e contexto
- Menos foco em comandos slash personalizados, mais em enriquecimento de contexto

**Níveis de customização:**
- Repositório (Global): `.github/copilot-instructions.md`
- Específica de Caminho: `.github/instructions/*.instructions.md`
- Agente Local: `AGENTS.md`
- Personalizada: `/memory add`

### Gemini CLI (Google)

**Arquitetura:**
- Baseado em arquivos TOML para definição de comandos slash
- Criação de namespaces através de subdiretórios
- Mecanismo de substituição de variáveis robusto com `{{args}}`
- Integração multimodal em comandos slash
- Sistema de gestão de memória via comandos como `/memory`

**Placeholder dinâmicos:**
- `{{args}}`: Injeta o texto digitado após o comando
- `!{shell_command}`: Executa comandos locais e integra a saída
- `@{file_path}`: Lê conteúdo de arquivos ou listas de diretórios
- `@{image_path}`: Injeta dados binários como entrada multimodal

### OpenCode e OpenAI Codex

**OpenCode:**
- Mais extensível do grupo
- Comandos definidos como comandos declarativos
- Podem ser scripts, prompts ou pipelines
- Suporte a configuração via arquivos YAML/JSON

**Codex:**
- Funciona como aliases semânticos
- Traduzidos para prompts estruturados
- Extensibilidade não documentada oficialmente

## Comparação de Extensibilidade

| Ferramenta | Extensível | Plugins | Config Declarativa | Método de Extensão |
|------------|------------|---------|-------------------|-------------------|
| Claude Code | Sim | Parcial | Sim | Arquivos Markdown + YAML |
| Qwen Code | Sim | Sim | Sim | Sistema de extensões + Markdown |
| Cursor | Não (interno) | Não | Não | User Rules (interface) |
| Copilot | Não (usuário) | Não | Não | MCP + contexto |
| Gemini | Incerto | Incerto | Incerto | Possivelmente TOML |
| OpenCode | Sim | Parcial | Sim | YAML/JSON |
| Codex | Não | Não | Não | Não documentado |

## Recomendações para Desenvolvedores

1. **Para extensibilidade avançada:** Qwen Code e Claude Code oferecem os caminhos mais robustos com suporte a arquivos Markdown e configurações YAML.

2. **Para simplicidade:** Cursor IDE oferece uma abordagem integrada via User Rules, mas com menor portabilidade.

3. **Para integração corporativa:** GitHub Copilot com MCP permite conectar o assistente a sistemas e dados internos da empresa.

4. **Para experimentação:** OpenCode oferece uma abordagem declarativa mais simples para criar comandos personalizados.

## Considerações de Segurança

A maioria das CLIs modernas implementa um modelo de permissões baseado em confiança:
- Confirmação de pasta obrigatória
- Execução de shell com prompts de confirmação
- Acesso externo bloqueado por padrão
- Auditoria com logs de ferramentas explícitos

## Conclusão

A extensibilidade de comandos slash varia significativamente entre as diferentes plataformas de CLIs de IA. Qwen Code e Claude Code lideram em termos de flexibilidade e recursos de extensibilidade, permitindo que desenvolvedores criem comandos personalizados de forma relativamente acessível. Cursor oferece uma abordagem mais integrada, mas menos portável. GitHub Copilot foca em integração via MCP em vez de comandos personalizados. Outras plataformas como Gemini CLI, OpenCode e Codex têm níveis variáveis de suporte e documentação.

A tendência geral é clara: as interfaces de linha de comando de IA estão evoluindo rapidamente de ferramentas fechadas para plataformas abertas e extensíveis, e a capacidade de personalizar comandos slash tornou-se um diferencial competitivo fundamental.