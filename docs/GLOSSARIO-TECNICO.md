# GLOSSARIO TECNICO - Itzamna PromptOS v1.0.0 (Piloto)

> **Version:** 1.0.0 | **Last Updated:** 2026-02-02
> **Purpose:** Referência completa de termos, conceitos e taxonomias
> **Usage:** Consultar antes de pesquisar - evita web searches desnecessários

---

## 📑 ÍNDICE

1. [Arquiteturas Cognitivas](#1-arquiteturas-cognitivas)
2. [Engenharia de Prompts](#2-engenharia-de-prompts)
3. [Agentes e Multi-Agentes](#3-agentes-e-multi-agentes)
4. [Memória e Contexto](#4-memória-e-contexto)
5. [LLMs e Modelos](#5-llms-e-modelos)
6. [Programação e Desenvolvimento](#6-programação-e-desenvolvimento)
7. [DevOps e Cloud](#7-devops-e-cloud)
8. [Arquitetura de Software](#8-arquitetura-de-software)
9. [Dados e AI/ML](#9-dados-e-aiml)
10. [Segurança](#10-segurança)
11. [Metodologias e Processos](#11-metodologias-e-processos)
12. [Ferramentas e Plataformas](#12-ferramentas-e-plataformas)
13. [Taxonomia de Skills](#13-taxonomia-de-skills)
14. [Acrônimos e Siglas](#14-acrônimos-e-siglas)

---

## 1. ARQUITETURAS COGNITIVAS

### 1.1 Frameworks Teóricos

| Termo | Definição | Aplicação no PromptOS |
|-------|-----------|----------------------|
| **CoALA** | Cognitive Architectures for Language Agents - Framework que define memória, ação e decisão para agentes LLM | Base teórica do sistema de memórias |
| **ACT-R** | Adaptive Control of Thought-Rational - Arquitetura cognitiva com memória declarativa e procedural | Inspiração para separação de skills |
| **SOAR** | State, Operator And Result - Arquitetura com espaços de problema e impasse handling | Modelo de decisão e escalação |
| **Global Workspace Theory** | Teoria de consciência com "broadcast" de informação | Hub de atenção no PromptOS |

### 1.2 Componentes Cognitivos

| Termo | Definição |
|-------|-----------|
| **Working Memory** | Memória de curto prazo para manipulação ativa de informação |
| **Long-Term Memory** | Armazenamento persistente de conhecimento |
| **Episodic Memory** | Memória de eventos específicos com contexto temporal |
| **Semantic Memory** | Conhecimento factual e conceitual geral |
| **Procedural Memory** | Conhecimento de "como fazer" (skills, hábitos) |
| **Attention Mechanism** | Processo de seleção de informação relevante |
| **Metacognition** | Pensamento sobre o próprio pensamento |

### 1.3 Ciclos de Decisão

| Termo | Definição |
|-------|-----------|
| **OODA Loop** | Observe-Orient-Decide-Act - Ciclo de decisão militar adaptado |
| **PDCA Cycle** | Plan-Do-Check-Act - Ciclo de melhoria contínua |
| **Sense-Plan-Act** | Paradigma clássico de robótica |
| **Reactive Architecture** | Resposta direta a estímulos sem planejamento |
| **Deliberative Architecture** | Planejamento antes da ação |
| **Hybrid Architecture** | Combinação de reativo e deliberativo |

---

## 2. ENGENHARIA DE PROMPTS

### 2.1 Técnicas Fundamentais

| Técnica | Definição | Quando Usar |
|---------|-----------|-------------|
| **Zero-Shot** | Prompt sem exemplos | Tarefas simples, modelos capazes |
| **Few-Shot** | Prompt com 1-5 exemplos | Tarefas que precisam de formato específico |
| **Chain-of-Thought (CoT)** | Pedir raciocínio passo a passo | Problemas de lógica, matemática |
| **Tree-of-Thought (ToT)** | Explorar múltiplos caminhos de raciocínio | Problemas complexos com backtracking |
| **ReAct** | Reasoning + Acting intercalados | Tarefas que requerem ações externas |
| **Self-Consistency** | Gerar múltiplas respostas e votar | Aumentar confiabilidade |
| **Self-Refine** | Modelo critica e melhora própria resposta | Qualidade iterativa |

### 2.2 Estruturas de Prompt

| Estrutura | Componentes | Uso |
|-----------|-------------|-----|
| **RICE** | Role, Instructions, Context, Examples | Prompts gerais |
| **CRISPE** | Capacity, Role, Insight, Statement, Personality, Experiment | Personas detalhadas |
| **CO-STAR** | Context, Objective, Style, Tone, Audience, Response | Conteúdo criativo |
| **RISEN** | Role, Instructions, Steps, End goal, Narrowing | Tarefas complexas |
| **APE** | Action, Purpose, Expectation | Prompts concisos |

### 2.3 Componentes de Prompt

| Componente | Função |
|------------|--------|
| **System Prompt** | Instrução persistente que define comportamento base |
| **User Prompt** | Input do usuário para a tarefa específica |
| **Assistant Response** | Resposta do modelo |
| **Few-Shot Examples** | Pares input/output de demonstração |
| **Delimiters** | Separadores para estruturar seções (```, ---, XML tags) |
| **Output Format** | Especificação do formato desejado |
| **Constraints** | Limitações e regras a seguir |
| **Persona** | Papel/identidade que o modelo assume |

### 2.4 Otimização

| Termo | Definição |
|-------|-----------|
| **Prompt Compression** | Reduzir tokens mantendo semântica |
| **Token Efficiency** | Maximizar output por token de input |
| **Prompt Injection** | Tentativa maliciosa de alterar comportamento |
| **Jailbreaking** | Bypass de safety guardrails |
| **Grounding** | Ancorar respostas em dados fornecidos |
| **Hallucination** | Geração de informação falsa como se fosse verdadeira |

---

## 3. AGENTES E MULTI-AGENTES

### 3.1 Tipos de Agentes

| Tipo | Definição | Exemplo |
|------|-----------|---------|
| **Reactive Agent** | Responde a estímulos sem estado | Chatbot simples |
| **Deliberative Agent** | Planeja antes de agir | Agente de coding |
| **Hybrid Agent** | Combina reativo e deliberativo | Claude Code |
| **BDI Agent** | Beliefs, Desires, Intentions | Agentes com goals |
| **Utility-Based Agent** | Maximiza função de utilidade | Trading bots |

### 3.2 Padrões Multi-Agente

| Padrão | Definição | Uso |
|--------|-----------|-----|
| **Orchestrator-Workers** | Um agente coordena outros | Tarefas paralelizáveis |
| **Hierarchical** | Agentes em níveis de autoridade | Sistemas complexos |
| **Peer-to-Peer** | Agentes comunicam como iguais | Colaboração |
| **Blackboard** | Espaço compartilhado de informação | Problemas mal-definidos |
| **Pipeline** | Agentes em sequência | Processamento linear |
| **Debate** | Agentes argumentam para melhor resposta | Verificação |

### 3.3 Componentes de Agente

| Componente | Função |
|------------|--------|
| **Perception** | Receber e processar inputs |
| **Reasoning** | Processar informação e decidir |
| **Action** | Executar ações no ambiente |
| **Learning** | Adaptar comportamento com experiência |
| **Communication** | Trocar informação com outros agentes |
| **Goal Management** | Manter e priorizar objetivos |

### 3.4 Ferramentas de Agentes

| Ferramenta | Tipo | Descrição |
|------------|------|-----------|
| **Web Search** | Information | Buscar informação na web |
| **Code Execution** | Action | Executar código |
| **File Operations** | Action | Ler/escrever arquivos |
| **API Calls** | Action | Chamar serviços externos |
| **Database Query** | Information | Consultar bancos de dados |
| **Human Handoff** | Control | Escalar para humano |

---

## 4. MEMÓRIA E CONTEXTO

### 4.1 Tipos de Memória em LLMs

| Tipo | Persistência | Escopo | Implementação |
|------|--------------|--------|---------------|
| **In-Context** | Sessão | Conversation | Context window |
| **Short-Term** | Sessão | Task | Buffer de mensagens |
| **Long-Term** | Persistente | User/Project | Vector DB, arquivos |
| **Shared** | Persistente | Multi-user | Database centralizado |

### 4.2 Técnicas de Memória

| Técnica | Definição |
|---------|-----------|
| **RAG** | Retrieval-Augmented Generation - Buscar info relevante antes de gerar |
| **MemGPT** | Memória virtual com paginação (core/recall/archival) |
| **Memory Consolidation** | Comprimir e resumir memórias antigas |
| **Memory Indexing** | Organizar memórias para busca eficiente |
| **Forgetting** | Descartar memórias irrelevantes estrategicamente |

### 4.3 Context Engineering

| Conceito | Definição |
|----------|-----------|
| **Context Window** | Limite de tokens que modelo pode processar |
| **Context Pollution** | Informação irrelevante degradando performance |
| **Context Compression** | Reduzir tamanho mantendo informação |
| **Recency Bias** | Modelo priorizar informação mais recente |
| **Lost in the Middle** | Modelo ignorar informação no meio do contexto |
| **Prompt Caching** | Reusar prefixos de prompt para economia |

### 4.4 Retrieval

| Técnica | Definição |
|---------|-----------|
| **Semantic Search** | Busca por similaridade de significado |
| **Keyword Search** | Busca por palavras exatas |
| **Hybrid Search** | Combina semântica e keyword |
| **Embedding** | Representação vetorial de texto |
| **Chunking** | Dividir documentos em pedaços |
| **Reranking** | Reordenar resultados por relevância |

---

## 5. LLMS E MODELOS

### 5.1 Famílias de Modelos

| Família | Empresa | Modelos Principais |
|---------|---------|-------------------|
| **Claude** | Anthropic | Opus 4.5, Sonnet 4.5, Haiku 4.5 |
| **GPT** | OpenAI | GPT-4o, GPT-4o-mini, o1, o3 |
| **Gemini** | Google | Gemini 2.0, Flash, Pro |
| **Llama** | Meta | Llama 3.1, 3.2, 3.3 |
| **Mistral** | Mistral AI | Mistral Large, Medium, Small |
| **DeepSeek** | DeepSeek | DeepSeek-V3, R1 |
| **Qwen** | Alibaba | Qwen 2.5, QwQ |

### 5.2 Características de Modelos

| Característica | Definição |
|----------------|-----------|
| **Context Length** | Tamanho máximo de entrada em tokens |
| **Output Length** | Tamanho máximo de saída |
| **Latency** | Tempo de resposta |
| **Throughput** | Tokens por segundo |
| **Cost** | Preço por token (input/output) |
| **Multimodal** | Suporta texto, imagem, áudio, vídeo |
| **Tool Use** | Capacidade de usar ferramentas |
| **Reasoning** | Capacidade de raciocínio complexo |

### 5.3 Modos de Operação

| Modo | Definição |
|------|-----------|
| **Chat** | Conversação multi-turno |
| **Completion** | Completar texto dado início |
| **Instruct** | Seguir instruções específicas |
| **Reasoning** | Raciocínio profundo (o1, R1) |
| **Agentic** | Operação autônoma com ferramentas |

### 5.4 Parâmetros de Inferência

| Parâmetro | Função | Range Típico |
|-----------|--------|--------------|
| **Temperature** | Aleatoriedade da saída | 0.0-2.0 |
| **Top-P** | Nucleus sampling | 0.0-1.0 |
| **Top-K** | Limitar vocabulário | 1-100 |
| **Max Tokens** | Limite de saída | 1-128K |
| **Stop Sequences** | Strings que param geração | Lista |
| **Frequency Penalty** | Penalizar repetição | -2.0-2.0 |
| **Presence Penalty** | Penalizar tokens já usados | -2.0-2.0 |

---

## 6. PROGRAMAÇÃO E DESENVOLVIMENTO

### 6.1 Paradigmas

| Paradigma | Definição | Linguagens |
|-----------|-----------|------------|
| **Imperativo** | Sequência de comandos | C, Python |
| **Declarativo** | Descrever o quê, não como | SQL, HTML |
| **OOP** | Organização em objetos | Java, C++, Python |
| **Funcional** | Funções puras, imutabilidade | Haskell, Scala, Elixir |
| **Reativo** | Streams de dados assíncronos | RxJS, Reactor |
| **Concurrent** | Múltiplas execuções simultâneas | Go, Erlang |

### 6.2 Linguagens por Domínio

| Domínio | Linguagens Principais |
|---------|----------------------|
| **Backend** | Python, Java, Go, Rust, C#, Node.js |
| **Frontend** | JavaScript, TypeScript, HTML, CSS |
| **Mobile** | Swift, Kotlin, Dart (Flutter), React Native |
| **Data/ML** | Python, R, Julia, SQL |
| **Systems** | C, C++, Rust, Zig |
| **DevOps** | Bash, Python, Go, HCL (Terraform) |
| **Embedded** | C, C++, Rust, Assembly |

### 6.3 Conceitos Fundamentais

| Conceito | Definição |
|----------|-----------|
| **Algorithm** | Sequência finita de instruções para resolver problema |
| **Data Structure** | Forma de organizar e armazenar dados |
| **Complexity** | Medida de recursos (tempo/espaço) de algoritmo |
| **Big O** | Notação para complexidade assintótica |
| **Recursion** | Função que chama a si mesma |
| **Iteration** | Repetição com loops |
| **Abstraction** | Esconder detalhes de implementação |
| **Encapsulation** | Agrupar dados e métodos relacionados |
| **Inheritance** | Herdar comportamento de classe pai |
| **Polymorphism** | Mesma interface, diferentes implementações |
| **Composition** | Construir objetos a partir de outros |
| **Dependency Injection** | Injetar dependências externamente |

### 6.4 Estruturas de Dados

| Estrutura | Complexidade (avg) | Uso |
|-----------|-------------------|-----|
| **Array** | O(1) access, O(n) search | Acesso indexado |
| **Linked List** | O(n) access, O(1) insert | Inserções frequentes |
| **Stack** | O(1) push/pop | LIFO, undo/redo |
| **Queue** | O(1) enqueue/dequeue | FIFO, BFS |
| **Hash Table** | O(1) avg | Lookup rápido por chave |
| **Binary Tree** | O(log n) balanced | Dados ordenados |
| **Heap** | O(log n) insert/extract | Priority queues |
| **Graph** | Varies | Relacionamentos complexos |
| **Trie** | O(m) m=key length | Autocomplete, prefixos |

### 6.5 Algoritmos Clássicos

| Categoria | Algoritmos |
|-----------|------------|
| **Sorting** | QuickSort, MergeSort, HeapSort, TimSort |
| **Searching** | Binary Search, BFS, DFS, A* |
| **Graph** | Dijkstra, Bellman-Ford, Kruskal, Prim |
| **Dynamic Programming** | Fibonacci, Knapsack, LCS, Edit Distance |
| **Greedy** | Huffman, Activity Selection |
| **Divide & Conquer** | Merge Sort, Quick Sort, Karatsuba |
| **Backtracking** | N-Queens, Sudoku Solver |

---

## 7. DEVOPS E CLOUD

### 7.1 Conceitos DevOps

| Conceito | Definição |
|----------|-----------|
| **CI/CD** | Continuous Integration / Continuous Deployment |
| **Infrastructure as Code** | Definir infra em código (Terraform, Pulumi) |
| **GitOps** | Git como fonte de verdade para infra |
| **Observability** | Logs, Metrics, Traces |
| **SRE** | Site Reliability Engineering |
| **Platform Engineering** | Criar plataformas internas para devs |
| **DevSecOps** | Integrar segurança no pipeline |

### 7.2 Containerização

| Termo | Definição |
|-------|-----------|
| **Container** | Ambiente isolado para executar aplicação |
| **Image** | Template imutável para criar containers |
| **Dockerfile** | Instruções para construir imagem |
| **Registry** | Repositório de imagens (Docker Hub, ECR) |
| **Orchestration** | Gerenciar múltiplos containers (K8s) |
| **Pod** | Menor unidade deployável em Kubernetes |
| **Service** | Abstração de rede para pods |
| **Deployment** | Controller para gerenciar réplicas |
| **Ingress** | Roteamento HTTP externo |
| **Helm** | Package manager para Kubernetes |

### 7.3 Cloud Providers

| Provider | Principais Serviços |
|----------|---------------------|
| **AWS** | EC2, S3, Lambda, RDS, EKS, DynamoDB |
| **GCP** | Compute Engine, GCS, Cloud Run, BigQuery |
| **Azure** | VMs, Blob Storage, AKS, Cosmos DB |
| **Vercel** | Frontend hosting, Serverless functions |
| **Cloudflare** | CDN, Workers, R2, D1 |

### 7.4 Padrões de Deploy

| Padrão | Definição |
|--------|-----------|
| **Blue-Green** | Dois ambientes, switch instantâneo |
| **Canary** | Deploy gradual para subset de usuários |
| **Rolling** | Atualizar instâncias incrementalmente |
| **A/B Testing** | Testar variantes com usuários reais |
| **Feature Flags** | Ativar features por configuração |

---

## 8. ARQUITETURA DE SOFTWARE

### 8.1 Estilos Arquiteturais

| Estilo | Definição | Quando Usar |
|--------|-----------|-------------|
| **Monolith** | Aplicação única, código junto | Projetos pequenos, início |
| **Microservices** | Serviços independentes | Escala, times grandes |
| **Serverless** | Funções sob demanda | Event-driven, variável |
| **Event-Driven** | Comunicação via eventos | Desacoplamento |
| **Layered** | Camadas (UI, Business, Data) | CRUD tradicional |
| **Hexagonal** | Ports & Adapters | Testabilidade |
| **CQRS** | Command Query Responsibility Segregation | Read/write diferentes |
| **Event Sourcing** | Estado como sequência de eventos | Audit, replay |

### 8.2 Design Patterns

| Categoria | Patterns |
|-----------|----------|
| **Creational** | Singleton, Factory, Builder, Prototype, Abstract Factory |
| **Structural** | Adapter, Bridge, Composite, Decorator, Facade, Proxy |
| **Behavioral** | Observer, Strategy, Command, State, Template Method, Iterator |
| **Concurrency** | Thread Pool, Producer-Consumer, Read-Write Lock |
| **Integration** | API Gateway, Circuit Breaker, Saga, Outbox |

### 8.3 Princípios de Design

| Princípio | Definição |
|-----------|-----------|
| **SOLID** | Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, Dependency Inversion |
| **DRY** | Don't Repeat Yourself |
| **KISS** | Keep It Simple, Stupid |
| **YAGNI** | You Ain't Gonna Need It |
| **Separation of Concerns** | Dividir sistema em partes distintas |
| **Loose Coupling** | Minimizar dependências entre módulos |
| **High Cohesion** | Módulos focados em uma responsabilidade |

### 8.4 APIs

| Estilo | Características |
|--------|-----------------|
| **REST** | Resources, HTTP verbs, stateless |
| **GraphQL** | Query language, single endpoint, typed |
| **gRPC** | Binary protocol, streaming, code gen |
| **WebSocket** | Bidirectional, persistent connection |
| **Webhook** | Event callbacks via HTTP |
| **Server-Sent Events** | Unidirectional streaming |

---

## 9. DADOS E AI/ML

### 9.1 Bancos de Dados

| Tipo | Exemplos | Uso |
|------|----------|-----|
| **Relational** | PostgreSQL, MySQL, SQLite | Dados estruturados, ACID |
| **Document** | MongoDB, CouchDB | JSON-like, flexível |
| **Key-Value** | Redis, DynamoDB | Cache, sessões |
| **Wide Column** | Cassandra, ScyllaDB | Time-series, escala |
| **Graph** | Neo4j, Neptune | Relacionamentos complexos |
| **Vector** | Pinecone, Weaviate, Chroma | Embeddings, similarity |
| **Time-Series** | InfluxDB, TimescaleDB | Métricas, IoT |

### 9.2 Conceitos de ML

| Conceito | Definição |
|----------|-----------|
| **Supervised Learning** | Aprender de dados rotulados |
| **Unsupervised Learning** | Encontrar padrões sem rótulos |
| **Reinforcement Learning** | Aprender por recompensa |
| **Neural Network** | Modelo inspirado em neurônios biológicos |
| **Deep Learning** | Redes neurais profundas |
| **Transformer** | Arquitetura com self-attention |
| **Fine-Tuning** | Ajustar modelo pré-treinado para tarefa |
| **Transfer Learning** | Reusar conhecimento entre tarefas |
| **Embedding** | Representação vetorial densa |
| **Attention** | Mecanismo de foco em partes relevantes |

### 9.3 Tipos de Modelos

| Tipo | Uso | Exemplos |
|------|-----|----------|
| **LLM** | Texto, código, raciocínio | GPT, Claude, Llama |
| **Image Generation** | Criar imagens | DALL-E, Midjourney, Stable Diffusion |
| **Speech-to-Text** | Transcrição | Whisper, AssemblyAI |
| **Text-to-Speech** | Síntese de voz | ElevenLabs, Azure TTS |
| **Vision** | Análise de imagens | GPT-4V, Claude Vision |
| **Multimodal** | Múltiplas modalidades | GPT-4o, Gemini |

### 9.4 MLOps

| Conceito | Definição |
|----------|-----------|
| **Feature Store** | Repositório de features para ML |
| **Model Registry** | Versionamento de modelos |
| **Model Serving** | Deployment de modelos |
| **A/B Testing** | Comparar modelos em produção |
| **Model Monitoring** | Detectar drift e degradação |
| **Data Versioning** | Versionar datasets (DVC) |

---

## 10. SEGURANÇA

### 10.1 Conceitos Fundamentais

| Conceito | Definição |
|----------|-----------|
| **CIA Triad** | Confidentiality, Integrity, Availability |
| **Authentication** | Verificar identidade |
| **Authorization** | Verificar permissões |
| **Encryption** | Codificar dados para proteção |
| **Hashing** | Função one-way para verificação |
| **Zero Trust** | Never trust, always verify |
| **Defense in Depth** | Múltiplas camadas de proteção |

### 10.2 Vulnerabilidades Comuns

| Vulnerabilidade | Definição | Prevenção |
|-----------------|-----------|-----------|
| **SQL Injection** | Injetar SQL malicioso | Parameterized queries |
| **XSS** | Cross-Site Scripting | Input sanitization, CSP |
| **CSRF** | Cross-Site Request Forgery | CSRF tokens |
| **SSRF** | Server-Side Request Forgery | URL validation |
| **RCE** | Remote Code Execution | Input validation |
| **Path Traversal** | Acessar arquivos fora do escopo | Path validation |
| **Insecure Deserialization** | Executar código via deserialize | Validate before deserialize |

### 10.3 Autenticação

| Método | Descrição |
|--------|-----------|
| **Password** | Usuário/senha tradicional |
| **MFA** | Multi-Factor Authentication |
| **OAuth 2.0** | Authorization framework |
| **OIDC** | OpenID Connect (identity layer) |
| **JWT** | JSON Web Token |
| **SAML** | Security Assertion Markup Language |
| **Passkeys** | WebAuthn/FIDO2 passwordless |
| **API Keys** | Tokens para APIs |

### 10.4 Criptografia

| Tipo | Exemplos | Uso |
|------|----------|-----|
| **Symmetric** | AES, ChaCha20 | Encriptação de dados |
| **Asymmetric** | RSA, ECC | Key exchange, signatures |
| **Hashing** | SHA-256, SHA-3 | Verificação de integridade |
| **Password Hashing** | Argon2, bcrypt | Armazenar senhas |
| **TLS** | TLS 1.3 | Comunicação segura |

---

## 11. METODOLOGIAS E PROCESSOS

### 11.1 Metodologias de Desenvolvimento

| Metodologia | Características |
|-------------|-----------------|
| **Agile** | Iterativo, adaptativo, colaborativo |
| **Scrum** | Sprints, roles (PO, SM, Dev), ceremonies |
| **Kanban** | Flow-based, WIP limits, visualização |
| **XP** | Pair programming, TDD, CI |
| **Waterfall** | Sequencial, fases distintas |
| **Lean** | Eliminar desperdício, entregar valor |

### 11.2 Práticas de Engenharia

| Prática | Definição |
|---------|-----------|
| **TDD** | Test-Driven Development - Teste primeiro |
| **BDD** | Behavior-Driven Development - Comportamento |
| **DDD** | Domain-Driven Design - Modelo de domínio |
| **Pair Programming** | Dois devs, um computador |
| **Mob Programming** | Time inteiro, um computador |
| **Code Review** | Revisão por pares |
| **Refactoring** | Melhorar código sem mudar comportamento |
| **Technical Debt** | Compromissos que custam depois |

### 11.3 Testes

| Tipo | Escopo | Velocidade |
|------|--------|------------|
| **Unit** | Função/classe | Rápido |
| **Integration** | Múltiplos componentes | Médio |
| **E2E** | Sistema completo | Lento |
| **Contract** | APIs | Médio |
| **Performance** | Load/stress | Lento |
| **Security** | Vulnerabilidades | Médio |

### 11.4 Documentação

| Tipo | Propósito |
|------|-----------|
| **README** | Introdução ao projeto |
| **API Docs** | Referência de endpoints |
| **Architecture Decision Record (ADR)** | Registrar decisões |
| **Runbook** | Procedimentos operacionais |
| **Changelog** | Histórico de mudanças |
| **Contributing** | Guia para contribuidores |

---

## 12. FERRAMENTAS E PLATAFORMAS

### 12.1 IDEs e Editores

| Ferramenta | Linguagens/Uso |
|------------|----------------|
| **VS Code** | Universal, extensível |
| **Cursor** | AI-first, fork do VS Code |
| **IntelliJ IDEA** | JVM languages |
| **PyCharm** | Python |
| **Neovim** | Terminal, customizável |
| **Zed** | Performance, colaboração |

### 12.2 CLI Tools para AI

| Ferramenta | Descrição |
|------------|-----------|
| **Claude Code** | Anthropic CLI para coding |
| **GitHub Copilot CLI** | Copilot no terminal |
| **Gemini CLI** | Google AI CLI |
| **Aider** | AI pair programming |
| **Cursor** | AI IDE |
| **Continue** | AI coding assistant |

### 12.3 Version Control

| Ferramenta | Uso |
|------------|-----|
| **Git** | Version control |
| **GitHub** | Hosting, CI/CD, Projects |
| **GitLab** | DevOps completo |
| **Bitbucket** | Atlassian ecosystem |
| **Git LFS** | Large files |

### 12.4 Comunicação e Colaboração

| Ferramenta | Uso |
|------------|-----|
| **Slack** | Team messaging |
| **Discord** | Communities |
| **Linear** | Issue tracking |
| **Notion** | Docs + wikis |
| **Miro** | Whiteboarding |
| **Figma** | Design collaboration |

---

## 13. TAXONOMIA DE SKILLS

### 13.1 Categorias Acadêmicas

```
academic/
├── fundamentals/
│   ├── algorithm-design
│   ├── data-structures
│   ├── computational-complexity
│   ├── discrete-mathematics
│   └── linear-algebra
│
├── software-engineering/
│   ├── design-patterns
│   ├── clean-code
│   ├── refactoring
│   ├── software-architecture
│   └── testing-fundamentals
│
├── programming-paradigms/
│   ├── object-oriented
│   ├── functional-programming
│   ├── reactive-programming
│   └── concurrent-programming
│
├── web-mobile/
│   ├── web-fundamentals
│   ├── frontend-development
│   ├── mobile-development
│   └── progressive-web-apps
│
├── systems/
│   ├── operating-systems
│   ├── computer-networks
│   ├── distributed-systems
│   └── database-theory
│
├── data/
│   ├── data-modeling
│   ├── data-warehousing
│   ├── etl-pipelines
│   └── data-visualization
│
├── ai-ml/
│   ├── machine-learning-fundamentals
│   ├── deep-learning
│   ├── nlp
│   ├── computer-vision
│   └── reinforcement-learning
│
└── security/
    ├── security-fundamentals
    ├── cryptography
    ├── web-security
    └── secure-coding
```

### 13.2 Categorias Tecnológicas

```
technology/
├── cloud/
│   ├── docker
│   ├── kubernetes
│   ├── aws-fundamentals
│   ├── gcp-fundamentals
│   ├── terraform
│   └── serverless
│
├── languages/
│   ├── python
│   ├── javascript
│   ├── typescript
│   ├── go
│   ├── rust
│   ├── java
│   └── csharp
│
├── frameworks/
│   ├── react
│   ├── nextjs
│   ├── fastapi
│   ├── spring-boot
│   ├── django
│   └── express
│
├── databases/
│   ├── postgresql
│   ├── mongodb
│   ├── redis
│   ├── elasticsearch
│   └── vector-databases
│
├── practices/
│   ├── ci-cd
│   ├── code-review
│   ├── testing-automation
│   ├── observability
│   └── devops
│
└── ai-tools/
    ├── langchain
    ├── llamaindex
    ├── prompt-engineering
    ├── rag-systems
    └── agent-frameworks
```

### 13.3 Formato de Skill (Correto)

```
.prompt-os/skills/
├── {skill-name}/
│   └── SKILL.md          # Arquivo principal da skill
├── docker/
│   └── SKILL.md
├── kubernetes/
│   └── SKILL.md
└── python/
    └── SKILL.md
```

**Exemplo de path:**
- ✅ Correto: `.prompt-os/skills/docker/SKILL.md`
- ❌ Errado: `.prompt-os/skills/technology/cloud/docker.md`

---

## 14. ACRÔNIMOS E SIGLAS

### 14.1 Desenvolvimento

| Sigla | Significado |
|-------|-------------|
| **API** | Application Programming Interface |
| **REST** | Representational State Transfer |
| **CRUD** | Create, Read, Update, Delete |
| **SDK** | Software Development Kit |
| **CLI** | Command Line Interface |
| **GUI** | Graphical User Interface |
| **IDE** | Integrated Development Environment |
| **ORM** | Object-Relational Mapping |
| **MVC** | Model-View-Controller |
| **MVVM** | Model-View-ViewModel |
| **SPA** | Single Page Application |
| **SSR** | Server-Side Rendering |
| **SSG** | Static Site Generation |
| **PWA** | Progressive Web App |

### 14.2 Infraestrutura

| Sigla | Significado |
|-------|-------------|
| **DNS** | Domain Name System |
| **CDN** | Content Delivery Network |
| **LB** | Load Balancer |
| **VPC** | Virtual Private Cloud |
| **VPN** | Virtual Private Network |
| **SSL/TLS** | Secure Sockets Layer / Transport Layer Security |
| **HTTP/S** | HyperText Transfer Protocol (Secure) |
| **TCP/IP** | Transmission Control Protocol / Internet Protocol |
| **SSH** | Secure Shell |
| **FTP** | File Transfer Protocol |

### 14.3 AI/ML

| Sigla | Significado |
|-------|-------------|
| **LLM** | Large Language Model |
| **NLP** | Natural Language Processing |
| **RAG** | Retrieval-Augmented Generation |
| **RLHF** | Reinforcement Learning from Human Feedback |
| **SFT** | Supervised Fine-Tuning |
| **DPO** | Direct Preference Optimization |
| **CoT** | Chain-of-Thought |
| **ToT** | Tree-of-Thought |
| **MoE** | Mixture of Experts |
| **GPU** | Graphics Processing Unit |
| **TPU** | Tensor Processing Unit |
| **FLOPS** | Floating Point Operations Per Second |

### 14.4 Metodologias

| Sigla | Significado |
|-------|-------------|
| **TDD** | Test-Driven Development |
| **BDD** | Behavior-Driven Development |
| **DDD** | Domain-Driven Design |
| **CI/CD** | Continuous Integration / Continuous Deployment |
| **SRE** | Site Reliability Engineering |
| **DORA** | DevOps Research and Assessment |
| **OKR** | Objectives and Key Results |
| **KPI** | Key Performance Indicator |

### 14.5 Protocolos e Padrões

| Sigla | Significado |
|-------|-------------|
| **JSON** | JavaScript Object Notation |
| **YAML** | YAML Ain't Markup Language |
| **XML** | Extensible Markup Language |
| **JWT** | JSON Web Token |
| **OAuth** | Open Authorization |
| **OIDC** | OpenID Connect |
| **SAML** | Security Assertion Markup Language |
| **gRPC** | Google Remote Procedure Call |
| **MCP** | Model Context Protocol |
| **LSP** | Language Server Protocol |

---

## 📌 QUICK REFERENCE CARDS

### Card 1: Complexidade de Algoritmos

```
O(1)      → Constante      → Hash lookup
O(log n)  → Logarítmica    → Binary search
O(n)      → Linear         → Array scan
O(n log n)→ Linearítmica   → Merge sort
O(n²)     → Quadrática     → Bubble sort
O(2^n)    → Exponencial    → Recursive fibonacci
O(n!)     → Fatorial       → Permutations
```

### Card 2: HTTP Status Codes

```
1xx → Informational
2xx → Success (200 OK, 201 Created, 204 No Content)
3xx → Redirect (301 Moved, 304 Not Modified)
4xx → Client Error (400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found)
5xx → Server Error (500 Internal, 502 Bad Gateway, 503 Service Unavailable)
```

### Card 3: Git Commands

```
git init                    # Iniciar repo
git clone <url>             # Clonar repo
git add .                   # Stage all
git commit -m "msg"         # Commit
git push origin main        # Push
git pull                    # Pull
git branch <name>           # Criar branch
git checkout -b <name>      # Criar e mudar
git merge <branch>          # Merge
git rebase <branch>         # Rebase
git stash                   # Guardar mudanças
git log --oneline           # Histórico
```

### Card 4: Docker Commands

```
docker build -t <name> .    # Build image
docker run -d -p 8080:80    # Run container
docker ps                   # List running
docker logs <id>            # Ver logs
docker exec -it <id> bash   # Shell no container
docker-compose up -d        # Start compose
docker-compose down         # Stop compose
docker images               # List images
docker system prune         # Cleanup
```

### Card 5: Kubernetes Commands

```
kubectl get pods            # List pods
kubectl get svc             # List services
kubectl apply -f <file>     # Apply config
kubectl delete -f <file>    # Delete config
kubectl logs <pod>          # Pod logs
kubectl exec -it <pod> bash # Shell no pod
kubectl describe pod <name> # Detalhes
kubectl port-forward        # Port forward
kubectl scale deploy <n> --replicas=3
```

---

**Itzamna PromptOS v1.0.0 (Piloto)** | **Entries:** 500+ | **Last Updated:** 2026-02-02
