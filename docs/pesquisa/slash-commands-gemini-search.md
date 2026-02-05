# **Arquitetura e Extensibilidade de Comandos Slash em Interfaces de Linha de Comando de Inteligência Artificial**

A evolução das interfaces de linha de comando (CLIs) voltadas para o desenvolvimento de software e assistência de inteligência artificial marcou uma transição fundamental de simples wrappers de chat para agentes autônomos integrados ao sistema operacional e ao ecossistema de desenvolvimento. No cerne desta transformação reside a implementação de comandos slash ("slash commands"), que funcionam como primitivas estruturadas projetadas para mitigar a variabilidade das respostas de modelos de linguagem (LLMs) e fornecer aos desenvolvedores um controle determinístico sobre o contexto, as ferramentas e a lógica de execução.1 Ao contrário de prompts de linguagem natural puros, os comandos slash em CLIs como Claude Code, Gemini CLI, Qwen Code e Cursor IDE oferecem uma sintaxe previsível que permite a padronização de fluxos de trabalho repetitivos, a automação de auditorias de segurança e a orquestração de ferramentas complexas sem a necessidade de redigir instruções extensas em cada interação.2

## **A Gênese e o Mecanismo dos Comandos Slash em Agentes de Terminal**

O conceito de comandos slash em CLIs de IA fundamenta-se na necessidade de separar a instrução operacional da consulta de dados. Enquanto um prompt tradicional busca uma resposta criativa ou analítica, um comando slash (prefixado por /) sinaliza ao agente uma mudança de estado, uma alteração de configuração ou a execução de um macro pré-definido.1 Esses comandos são carregados dinamicamente de arquivos Markdown, TOML ou JSONC, permitindo uma arquitetura de extensibilidade onde o desenvolvedor pode "ensinar" novas habilidades ao agente simplesmente adicionando arquivos a diretórios específicos de usuário ou projeto.5

### **Claude Code: Integração de Habilidades e Automação de Ciclo de Vida**

O Claude Code e o CLI Auggie da Augment representam o estado da arte na fusão de comandos slash com o que agora é denominado "Habilidades" (Skills). Nesta arquitetura, os comandos slash deixaram de ser meros atalhos de texto para se tornarem ferramentas que o próprio agente pode decidir invocar de forma autônoma durante o seu processo de raciocínio.8

A implementação do Claude Code utiliza arquivos Markdown para definir comandos customizados. O nome do arquivo determina o nome do comando invocado (por exemplo, commit.md torna-se /commit). A precedência de carregamento é crucial para garantir que as configurações específicas do projeto se sobreponham às preferências globais do usuário.4

| Escopo do Comando | Localização do Diretório | Função Primária |
| :---- | :---- | :---- |
| Comandos de Usuário (Global) | \~/.augment/commands/ ou \~/.claude/commands/ | Utilitários universais disponíveis em todos os projetos do sistema. |
| Comandos de Workspace (Projeto) | ./.augment/commands/ | Fluxos de trabalho específicos do projeto, compartilhados via controle de versão. |
| Compatibilidade Legada | ./.claude/commands/ | Suporte para configurações existentes de Claude Code. |
| Skills Contextuais | ./.claude/skills/ | Comandos com capacidades avançadas e suporte a arquivos auxiliares. |

4

A configuração destes comandos é gerida através de metadados em YAML (frontmatter). Esta abordagem permite definir não apenas o prompt, mas também o modelo a ser utilizado e as restrições de ferramentas para aquela tarefa específica. Por exemplo, ao definir um comando /lint, um desenvolvedor pode especificar o uso de um modelo mais rápido e econômico, como o Claude Haiku, em vez do Sonnet, para otimizar custos e tempo de resposta.4

| Campo de Metadados | Descrição Técnica | Comportamento Padrão |
| :---- | :---- | :---- |
| description | Resumo exibido no menu /help e utilizado pelo agente para descoberta automática. | Primeira linha do prompt. |
| argument-hint | Guia de argumentos exibido no autocompletar do terminal. | Nenhuma dica. |
| model | Identificador do modelo (ex: sonnet, haiku) para execução específica. | Modelo padrão da sessão. |
| allowed-tools | Lista de ferramentas (Bash, Edit, Read) que o comando tem permissão para usar. | Herda da sessão ativa. |
| disable-model-invocation | Impede que o agente invoque o comando autonomamente como uma ferramenta. | Falso (permitido). |

4

Um diferencial tecnológico do Claude Code é a capacidade de executar comandos shell diretamente dentro do arquivo de definição de comando utilizando o prefixo \!. Quando um comando como /status é invocado, o CLI primeiro executa \! git status, captura a saída e a injeta no prompt antes de enviá-lo para processamento. Isso garante que o agente sempre opere com o estado mais atualizado do ambiente de desenvolvimento.5

### **Gemini CLI: Estruturação via TOML e Injeção Multimodal**

O Gemini CLI, desenvolvido pelo Google, optou por uma abordagem baseada em arquivos TOML para a definição de comandos slash customizados. Esta escolha reflete uma preferência por dados estruturados, facilitando a validação e a manipulação de argumentos complexos.6 A arquitetura do Gemini permite a criação de namespaces através de subdiretórios, onde um arquivo em .gemini/commands/git/commit.toml é mapeado automaticamente para o comando /git:commit.6

O mecanismo de substituição de variáveis do Gemini é robusto, utilizando chaves duplas {{args}} para capturar a entrada do usuário. Além da injeção de texto, o Gemini CLI destaca-se pela integração multimodal em seus comandos slash.6

| Placeholder Dinâmico | Mecanismo de Execução | Implicações de Segurança |
| :---- | :---- | :---- |
| {{args}} | Injeta o texto digitado pelo usuário após o comando. | Escape automático se usado em blocos de shell. |
| \!{shell\_command} | Executa comandos locais e integra a saída ao contexto. | Requer confirmação explícita do usuário (YOLO mode off). |
| @{file\_path} | Lê o conteúdo de arquivos ou listas de diretórios. | Respeita filtros do .gitignore. |
| @{image\_path} | Injeta dados binários (imagens, PDFs) como entrada multimodal. | Suporte nativo para análise de wireframes/screenshots. |

6

A gestão de memória no Gemini CLI também é estendida via comandos slash como /memory, que permite adicionar instruções hierárquicas através de arquivos GEMINI.md. Diferente de um comando slash tradicional que executa uma tarefa, a gestão de memória modifica o sistema de prompts (system prompt) de forma persistente para toda a sessão, garantindo que convenções de código (como "sempre usar TypeScript") sejam respeitadas sem a necessidade de repetição manual.12

## **Qwen Code e a Portabilidade de Ecossistemas de Extensão**

O Qwen Code apresenta uma arquitetura única focada em "Runtime Extension Management". Diferente de outros CLIs que limitam o usuário a definições locais, o Qwen foi projetado para ser compatível com extensões de outros ecossistemas, incluindo a capacidade de converter plugins do Claude Code e da galeria do Gemini CLI para o seu próprio formato.14

### **O Manifesto de Extensão e a Resolução de Conflitos**

A base de qualquer comando slash customizado no Qwen Code é o arquivo qwen-extension.json. Este manifesto define como o CLI deve interagir com servidores MCP (Model Context Protocol), quais comandos devem ser registrados e quais configurações de ambiente são necessárias.14

| Propriedade do Manifesto | Função no Registro de Comandos |
| :---- | :---- |
| name | Identificador único utilizado para prefixar comandos em caso de conflito. |
| mcpServers | Define binários e argumentos para ferramentas externas. |
| commands | Aponta para o diretório contendo arquivos Markdown de definição de prompts. |
| settings | Define variáveis de ambiente necessárias (ex: chaves de API). |

14

Um aspecto sofisticado do Qwen Code é a sua estratégia de resolução de nomes. Se um desenvolvedor instala uma extensão que contém um comando /deploy, mas já existe um comando de projeto com o mesmo nome, o Qwen renomeia automaticamente o comando da extensão para /nome\_da\_extensao.deploy. Isso preserva a funcionalidade global enquanto garante que os comandos específicos do projeto mantenham a precedência natural.14 Além disso, o Qwen suporta o "hot-reloading" de comandos; qualquer alteração em um arquivo Markdown dentro do diretório de extensões é refletida instantaneamente na sessão interativa do terminal.14

## **Cursor IDE e a Automação Baseada em Regras (MDC)**

O Cursor, embora seja primariamente um editor de código (IDE), possui uma integração profunda com o terminal através do Cursor Agent e de seu sistema de regras. Os comandos slash no Cursor são definidos principalmente através do formato .mdc (Markdown Cursor Rules), que permite uma granularidade sem precedentes na aplicação de contexto.16

### **Mapeamento de Atalhos para Ferramentas de Agente**

No Cursor, a criação de um comando slash customizado é frequentemente utilizada para abstrair sequências complexas de ferramentas. Por exemplo, um desenvolvedor pode definir uma regra onde /s \<termo\> instrui o agente a utilizar especificamente a ferramenta codebase\_search com determinados parâmetros.19 Isso é tecnicamente vantajoso pois reduz o "ruído" no contexto do modelo, fornecendo instruções explícitas sobre qual ferramenta deve ser ativada, economizando tokens e tempo de processamento.19

| Tipo de Regra Cursor | Gatilho de Ativação | Uso Recomendado para Comandos Slash |
| :---- | :---- | :---- |
| Always Apply | Automático em cada chat. | Padrões globais de formatação e segurança. |
| Apply Intelligently | Decisão do Agente via descrição. | Comandos que auxiliam na descoberta de código. |
| Globs Pattern | Correspondência de arquivos (ex: \*.ts). | Regras específicas para frameworks (React, Python). |
| Manual (@ mention) | Menção explícita do usuário. | Playbooks de refatoração ou auditoria de segurança. |

16

A implementação de comandos no Cursor também permite a criação de "Team Commands" através de um painel de controle administrativo, onde administradores de equipes podem definir comandos que são propagados automaticamente para todos os membros da organização, garantindo que playbooks de implantação ou regras de estilo sejam unificados.18

## **OpenCode e OpenAI Codex: Paradigmas de Templates de Prompt**

Os sistemas OpenCode e OpenAI Codex CLI utilizam abordagens baseadas em templates para a criação de comandos customizados, priorizando a simplicidade e a portabilidade entre diferentes versões de modelos. O OpenCode, em particular, permite definir comandos tanto em arquivos Markdown quanto diretamente no arquivo de configuração opencode.jsonc.7

### **Isolamento de Subtarefas e Argumentos Posicionais**

Uma inovação técnica presente no OpenCode é o conceito de subtask. Ao definir um comando slash, o desenvolvedor pode forçar sua execução em um subagente isolado (subtask: true). Isso garante que a execução do comando não polua o histórico principal da conversa, mantendo o contexto "limpo" para o raciocínio principal do desenvolvedor.7

No OpenAI Codex, o sistema de argumentos baseia-se em placeholders posicionais ($1, $2,..., $ARGUMENTS). Esta abordagem, similar aos scripts bash tradicionais, facilita a criação de utilitários rápidos para manipulação de arquivos ou geração de testes.20

| Elemento de Sintaxe | OpenCode / Codex | Função Técnica |
| :---- | :---- | :---- |
| Placeholder Total | $ARGUMENTS | Captura toda a string após o comando slash. |
| Placeholder Indexado | $1, $2 | Captura argumentos específicos separados por espaço. |
| Agent Specification | agent: "plan" | Define qual persona de IA deve processar o comando. |
| Shell Output | \! git diff | Injeta a diferença do repositório no prompt. |
| File Reference | @filename | Anexa automaticamente o conteúdo do arquivo mencionado. |

7

O Codex CLI também introduziu o uso do arquivo AGENTS.md para capturar instruções persistentes. Embora não seja um comando slash no sentido estrito de execução, o comando /init nestes sistemas gera automaticamente um scaffold desse arquivo, que serve como a "âncora de comportamento" para todos os comandos subsequentes executados naquele repositório.21

## **GitHub Copilot CLI: Instruções de Repositório e o Futuro dos Plugins**

O GitHub Copilot CLI evoluiu de um assistente de sugestões de comandos shell para um agente de codificação autônomo. Sua arquitetura de extensibilidade foca em "Custom Instructions" e, mais recentemente, em um sistema de plugins baseado em SDK que permite interceptar eventos do ciclo de vida da conversa.1

### **Níveis de Customização no Copilot**

A personalização do Copilot CLI ocorre em múltiplos níveis, permitindo que as instruções sejam tão granulares quanto o caminho de um arquivo específico ou tão abrangentes quanto uma organização inteira.23

| Tipo de Instrução | Arquivo de Configuração | Escopo de Aplicação |
| :---- | :---- | :---- |
| Repositório (Global) | .github/copilot-instructions.md | Todas as requisições dentro do repositório. |
| Específica de Caminho | .github/instructions/\*.instructions.md | Arquivos que coincidem com padrões glob (ex: src/\*\*/\*.py). |
| Agente Local | AGENTS.md | Instruções locais para o agente de codificação. |
| Personalizada | /memory add | Preferências de codificação do usuário individual. |

23

O ecossistema de plugins do Copilot (atualmente em desenvolvimento e visível via SDK PR \#42) promete levar os comandos slash a um novo nível de integração. Através de hooks como onBeforeSend e onSessionCreated, os desenvolvedores podem criar comandos slash que não apenas expandem prompts, mas modificam dinamicamente a estrutura da conversa ou aplicam filtros de segurança em tempo real.24 Comandos como /plugins install permitem que o usuário carregue habilidades como "anti-compaction" (para preservar histórico de conversa) ou integradores com ferramentas de terceiros como Jira e Linear.24

## **Análise Comparativa de Segurança e Governança**

A capacidade de adicionar comandos slash que executam código shell traz implicações significativas de segurança. A maioria das CLIs modernas implementa um modelo de permissões baseado em confiança. O Claude Code, por exemplo, exige que o usuário confirme explicitamente a validade do diretório antes de permitir qualquer modificação de arquivo.25

| Mecanismo de Segurança | Claude Code | Gemini CLI | Codex CLI |
| :---- | :---- | :---- | :---- |
| **Confirmação de Pasta** | Obrigatória no início da sessão. | Baseada em contexto Git. | Manual via .agent config. |
| **Execução de Shell** | Prompt individual ou allow-all. | Prompt individual ou YOLO mode. | Modos: Suggest, Auto-Edit, Full-Auto. |
| **Acesso Externo** | Bloqueado por padrão; requer /allow-all. | Via MCP tools configuradas. | Permissões granulares via MCP. |
| **Auditoria** | Log de ferramentas explícito. | Registro de histórico de checkpoints. | Git checkpoints automáticos. |

10

O Codex CLI oferece três modos de aprovação distintos que servem como referência para a indústria: o modo Suggest, onde a IA propõe e o humano aprova; o modo Auto-Edit, onde a IA edita arquivos locais mas pede permissão para comandos externos; e o modo Full Auto, para tarefas em ambientes controlados e confiáveis.22

## **Conclusão e Perspectivas Futuras**

A investigação das documentações oficiais revela uma convergência tecnológica em direção ao "Prompt Engineering as Code". A transição de arquivos de configuração estáticos para sistemas de habilidades (Skills) dinâmicos e extensíveis permite que o terminal se torne um ambiente de desenvolvimento verdadeiramente colaborativo. O uso de Markdown como o padrão *de facto* para a definição de comandos slash sublinha uma filosofia de design onde a documentação do projeto e as instruções da IA são a mesma entidade.

No futuro, espera-se que a distinção entre comandos slash e habilidades autônomas desapareça completamente. Como observado nas atualizações recentes do Claude Code, o agente não apenas executa o que o usuário pede através de um comando slash, mas entende a biblioteca de comandos slash disponíveis no repositório como um conjunto de ferramentas à sua disposição para resolver problemas complexos. Para organizações de engenharia, isso significa que a manutenção de uma biblioteca robusta de comandos slash customizados tornar-se-á tão vital quanto a manutenção da suíte de testes ou da documentação técnica, servindo como o conhecimento operacional codificado que permite à inteligência artificial navegar e modificar sistemas complexos com precisão e segurança.3

#### **Trabalhos citados**

1. A cheat sheet to slash commands in GitHub Copilot CLI, acesso a fevereiro 4, 2026, [https://github.blog/ai-and-ml/github-copilot/a-cheat-sheet-to-slash-commands-in-github-copilot-cli/](https://github.blog/ai-and-ml/github-copilot/a-cheat-sheet-to-slash-commands-in-github-copilot-cli/)
2. Top 10 GitHub Copilot Slash Commands Every VS Code Developer Must Know in 2025, acesso a fevereiro 4, 2026, [https://medium.com/@shrinivassab/top-10-github-copilot-slash-commands-every-vs-code-developer-must-know-in-2025-4f866360fdad](https://medium.com/@shrinivassab/top-10-github-copilot-slash-commands-every-vs-code-developer-must-know-in-2025-4f866360fdad)
3. hamzafer/cursor-commands: Cursor Custom Slash Commands \- GitHub, acesso a fevereiro 4, 2026, [https://github.com/hamzafer/cursor-commands](https://github.com/hamzafer/cursor-commands)
4. Custom Slash Commands \- Augment \- Introduction, acesso a fevereiro 4, 2026, [https://docs.augmentcode.com/cli/custom-commands](https://docs.augmentcode.com/cli/custom-commands)
5. How to Speed Up Your Claude Code Experience with Slash Commands | alexop.dev, acesso a fevereiro 4, 2026, [https://alexop.dev/posts/claude-code-slash-commands-guide/](https://alexop.dev/posts/claude-code-slash-commands-guide/)
6. CLI Commands | gemini-cli, acesso a fevereiro 4, 2026, [https://google-gemini.github.io/gemini-cli/docs/cli/commands.html](https://google-gemini.github.io/gemini-cli/docs/cli/commands.html)
7. Commands | OpenCode, acesso a fevereiro 4, 2026, [https://opencode.ai/docs/commands/](https://opencode.ai/docs/commands/)
8. Extend Claude with skills \- Claude Code Docs, acesso a fevereiro 4, 2026, [https://code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills)
9. Claude Code can invoke your custom slash commands : r/ClaudeAI \- Reddit, acesso a fevereiro 4, 2026, [https://www.reddit.com/r/ClaudeAI/comments/1noyvmq/claude\_code\_can\_invoke\_your\_custom\_slash\_commands/](https://www.reddit.com/r/ClaudeAI/comments/1noyvmq/claude_code_can_invoke_your_custom_slash_commands/)
10. Claude Code Guide: Professional Setup, Configuration & Workflows (2026) \- Juan Andrés Núñez — Building at the intersection of Frontend, AI, and Humanism, acesso a fevereiro 4, 2026, [https://wmedia.es/en/writing/claude-code-professional-guide-frontend-ai](https://wmedia.es/en/writing/claude-code-professional-guide-frontend-ai)
11. Gemini CLI: Custom slash commands | Google Cloud Blog, acesso a fevereiro 4, 2026, [https://cloud.google.com/blog/topics/developers-practitioners/gemini-cli-custom-slash-commands](https://cloud.google.com/blog/topics/developers-practitioners/gemini-cli-custom-slash-commands)
12. CLI commands \- Gemini CLI, acesso a fevereiro 4, 2026, [https://geminicli.com/docs/cli/commands/](https://geminicli.com/docs/cli/commands/)
13. addyosmani/gemini-cli-tips \- GitHub, acesso a fevereiro 4, 2026, [https://github.com/addyosmani/gemini-cli-tips](https://github.com/addyosmani/gemini-cli-tips)
14. Qwen Code Extensions | Qwen Code Docs, acesso a fevereiro 4, 2026, [https://qwenlm.github.io/qwen-code-docs/en/users/extension/introduction/](https://qwenlm.github.io/qwen-code-docs/en/users/extension/introduction/)
15. Getting Started with Qwen Code Extensions, acesso a fevereiro 4, 2026, [https://qwenlm.github.io/qwen-code-docs/en/developers/extensions/getting-started-extensions/](https://qwenlm.github.io/qwen-code-docs/en/developers/extensions/getting-started-extensions/)
16. Rules | Cursor Docs, acesso a fevereiro 4, 2026, [https://cursor.com/docs/context/rules](https://cursor.com/docs/context/rules)
17. "/Generate Cursor Rules" Custom Command Workaround\! \- Discussions, acesso a fevereiro 4, 2026, [https://forum.cursor.com/t/generate-cursor-rules-custom-command-workaround/139238](https://forum.cursor.com/t/generate-cursor-rules-custom-command-workaround/139238)
18. Commands | Cursor Docs, acesso a fevereiro 4, 2026, [https://cursor.com/docs/context/commands](https://cursor.com/docs/context/commands)
19. Speed Up Your Agents with Cursor Slash Commands \- Egghead.io, acesso a fevereiro 4, 2026, [https://egghead.io/speed-up-your-agents-with-cursor-slash-commands\~ze5ag](https://egghead.io/speed-up-your-agents-with-cursor-slash-commands~ze5ag)
20. Custom Prompts \- OpenAI for developers, acesso a fevereiro 4, 2026, [https://developers.openai.com/codex/custom-prompts/](https://developers.openai.com/codex/custom-prompts/)
21. Slash commands in Codex CLI \- OpenAI for developers, acesso a fevereiro 4, 2026, [https://developers.openai.com/codex/cli/slash-commands/](https://developers.openai.com/codex/cli/slash-commands/)
22. Getting Started with OpenAI Codex CLI: AI-Powered Code Generation from Your Terminal, acesso a fevereiro 4, 2026, [https://www.deployhq.com/blog/getting-started-with-openai-codex-cli-ai-powered-code-generation-from-your-terminal](https://www.deployhq.com/blog/getting-started-with-openai-codex-cli-ai-powered-code-generation-from-your-terminal)
23. Adding repository custom instructions \- GitHub 문서, acesso a fevereiro 4, 2026, [https://docs.github.com/ko/copilot/how-tos/copilot-cli/add-repository-instructions](https://docs.github.com/ko/copilot/how-tos/copilot-cli/add-repository-instructions)
24. Add Plugin System to Copilot SDK by ssfdre38 · Pull Request \#42 \- GitHub, acesso a fevereiro 4, 2026, [https://github.com/github/copilot-sdk/pull/42](https://github.com/github/copilot-sdk/pull/42)
25. Using GitHub Copilot CLI, acesso a fevereiro 4, 2026, [https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli)
26. GitHub Copilot CLI command reference, acesso a fevereiro 4, 2026, [https://docs.github.com/en/copilot/reference/cli-command-reference](https://docs.github.com/en/copilot/reference/cli-command-reference)
27. Plugin system for GitHub Copilot CLI SDK \- enables extensibility through lifecycle hooks ‍☠️, acesso a fevereiro 4, 2026, [https://github.com/barrersoftware/copilot-plugin-system-js](https://github.com/barrersoftware/copilot-plugin-system-js)
28. Feature Request: Extension API for Community Plugins · Issue \#1017 · github/copilot-cli, acesso a fevereiro 4, 2026, [https://github.com/github/copilot-cli/issues/1017](https://github.com/github/copilot-cli/issues/1017)
29. google-gemini/gemini-cli: An open-source AI agent that brings the power of Gemini directly into your terminal. \- GitHub, acesso a fevereiro 4, 2026, [https://github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)
30. Codex CLI \- OpenAI for developers, acesso a fevereiro 4, 2026, [https://developers.openai.com/codex/cli/](https://developers.openai.com/codex/cli/)
31. PatrickJS/awesome-cursorrules: Configuration files that enhance Cursor AI editor experience with custom rules and behaviors \- GitHub, acesso a fevereiro 4, 2026, [https://github.com/PatrickJS/awesome-cursorrules](https://github.com/PatrickJS/awesome-cursorrules)
32. Feature: Support slash commands in CLI via 'opencode run' · Issue \#5073 \- GitHub, acesso a fevereiro 4, 2026, [https://github.com/sst/opencode/issues/5073](https://github.com/sst/opencode/issues/5073)
33. Support for Slash Commands and Custom Command Definitions via .codex File in VS Code Extension \#5392 \- GitHub, acesso a fevereiro 4, 2026, [https://github.com/openai/codex/issues/5392](https://github.com/openai/codex/issues/5392)