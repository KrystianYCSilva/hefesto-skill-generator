# PromptOS: Arquitetura de cérebro simplificado para programação paralela humano-agente

Um sistema operacional de prompts requer três pilares fundamentais: **arquitetura cognitiva inspirada em neurociência**, **auto-incrementação com supervisão humana**, e **geração dinâmica de skills**. O framework CoALA (Cognitive Architectures for Language Agents) emergiu como padrão dominante, combinando memórias especializadas com ciclos de decisão que espelham cognição biológica. Para PromptOS, a abordagem mais prática é simplificar radicalmente esses modelos, mantendo apenas os componentes funcionalmente essenciais enquanto adiciona loops de aprovação humana em pontos críticos do fluxo.

---

## Arquitetura cognitiva simplificada para PromptOS

O CoALA framework sintetiza décadas de pesquisa em ACT-R, SOAR e Global Workspace Theory em uma arquitetura prática para agentes LLM. A essência é uma separação clara entre **memória de trabalho** (contexto ativo limitado), **memórias de longo prazo** (episódica, semântica, procedural), e um **ciclo de decisão** iterativo.

```
┌─────────────────────────────────────────────────────────────┐
│                    PROMPTOS BRAIN ARCHITECTURE               │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────┐  │
│  │           GLOBAL WORKSPACE (Hub de Atenção)           │  │
│  │  • Foco atual / goal ativo                            │  │
│  │  • Contexto de trabalho (~10K tokens)                 │  │
│  │  • Broadcast para todos os módulos                    │  │
│  └───────────────────────────────────────────────────────┘  │
│           ↕                ↕                ↕                │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │   RECALL    │   │   REASON    │   │     ACT     │       │
│  │  (Memória)  │   │    (LLM)    │   │   (Tools)   │       │
│  ├─────────────┤   ├─────────────┤   ├─────────────┤       │
│  │• Episódica  │   │• Planning   │   │• Web search │       │
│  │• Semântica  │   │• Reflection │   │• Code exec  │       │
│  │• Procedural │   │• Evaluation │   │• File ops   │       │
│  │  (Skills)   │   │• Generation │   │• Human gate │       │
│  └─────────────┘   └─────────────┘   └─────────────┘       │
└─────────────────────────────────────────────────────────────┘
```

O **Global Workspace** implementa a teoria de Baars: múltiplos módulos competem por atenção, e o vencedor faz broadcast de informação para todo o sistema. Em termos práticos, isso significa um buffer central que mantém o estado atual e distribui contexto relevante para cada operação.

### Sistema de memórias especializadas

| Tipo | Função biológica | Implementação PromptOS | Persistência |
|------|------------------|------------------------|--------------|
| **Working Memory** | Manipulação ativa de informação | Context window do LLM + message buffer | Sessão |
| **Episódica** | Eventos específicos passados | Vector DB com timestamps (ChromaDB) | Persistente |
| **Semântica** | Conhecimento geral/fatos | Knowledge base + embeddings | Persistente |
| **Procedural** | Skills e "como fazer" | Biblioteca de SKILL.md files | Persistente |

A memória episódica registra cada interação com contexto temporal, permitindo retrieval por similaridade semântica + filtro temporal. A memória semântica armazena conhecimento domain-specific em formato vetorial. A memória procedural—crítica para PromptOS—mantém skills como código executável indexado por descrições semânticas.

---

## Ciclo de decisão com human-in-the-loop

O fluxo **Pesquisa → Geração → Aprovação → Commit** implementa o padrão SOAR de impasse-handling com gates humanos em pontos críticos. Quando o agente encontra incerteza ou operações de alto risco, o sistema interrompe para aprovação.

```
┌────────────────────────────────────────────────────────────────────────┐
│              FLUXO: PESQUISA → GERAÇÃO → APROVAÇÃO → COMMIT            │
├────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐        │
│  │ PESQUISA │───▶│ GERAÇÃO  │───▶│ REVIEW   │───▶│  COMMIT  │        │
│  │  (Web)   │    │ (Skill)  │    │ (Human)  │    │  (Save)  │        │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘        │
│       │               │               │               │               │
│       ▼               ▼               ▼               ▼               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐        │
│  │ Buscar   │    │ Template │    │ Aprovar/ │    │ Salvar   │        │
│  │ fontes + │    │ + Meta-  │    │ Editar/  │    │ Skill +  │        │
│  │ validar  │    │ prompt   │    │ Rejeitar │    │ Indexar  │        │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘        │
│                                        │                              │
│                          ┌─────────────┴─────────────┐                │
│                          │     Se rejeitado:         │                │
│                          │  • Feedback → refinar     │                │
│                          │  • Loop até aprovação     │                │
│                          └───────────────────────────┘                │
└────────────────────────────────────────────────────────────────────────┘
```

### Implementação com LangGraph interrupt pattern

```python
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

def skill_approval_node(state: dict) -> Command:
    """Pausa para aprovação humana antes de persistir skill."""
    
    response = interrupt({
        "type": "skill_review",
        "skill_name": state["generated_skill"]["name"],
        "skill_content": state["generated_skill"]["content"],
        "sources": state["research_sources"],
        "question": "Aprovar este skill? (approve/edit/reject)"
    })
    
    if response["action"] == "approve":
        return Command(goto="commit_skill")
    elif response["action"] == "edit":
        state["generated_skill"]["content"] = response["edited_content"]
        return Command(goto="commit_skill")
    else:  # reject
        state["rejection_reason"] = response["reason"]
        return Command(goto="refine_skill")

# Retomar após input humano
graph.invoke(Command(resume={"action": "approve"}), config=config)
```

### Níveis de autonomia graduada

O sistema deve suportar **cinco níveis de autonomia** que evoluem conforme confiança:

| Nível | Papel do usuário | Aprovação necessária |
|-------|------------------|---------------------|
| **L1** | Operador | Toda ação requer aprovação |
| **L2** | Colaborador | Agente sugere, humano revisa tudo |
| **L3** | Consultor | Rotinas auto-executam, incertezas escalam |
| **L4** | Aprovador | Planos completos → yes/no |
| **L5** | Observador | Autonomia total, auditorias periódicas |

Para PromptOS focado em programação, iniciar em **L2-L3** é recomendado: skills read-only auto-aprovam, skills que modificam código requerem review.

---

## Geração dinâmica de skills e personas

A abordagem mais prática combina o formato **SKILL.md** (padrão Anthropic) com otimização via **DSPy** e validação multi-camada.

### Template universal de skill

```yaml
---
name: code-reviewer
description: Analisa código para bugs, segurança e boas práticas
version: 1.0.0
domain: programming
triggers:
  - "revisar código"
  - "code review"
  - "analisar este código"
---

# Code Reviewer

## Instruções
Você é um revisor de código experiente. Ao receber código:
1. Identifique bugs potenciais e edge cases
2. Verifique vulnerabilidades de segurança
3. Sugira melhorias de performance
4. Avalie legibilidade e manutenabilidade

## Output esperado
- **Severidade**: crítico/alto/médio/baixo
- **Localização**: linha(s) afetada(s)
- **Problema**: descrição clara
- **Sugestão**: código corrigido

## Exemplos
### Input
```python
def login(user, pwd):
    query = f"SELECT * FROM users WHERE user='{user}' AND pwd='{pwd}'"
    return db.execute(query)
```

### Output
**Severidade**: Crítico
**Localização**: Linha 2
**Problema**: SQL Injection - concatenação direta de input do usuário
**Sugestão**:
```python
def login(user, pwd):
    query = "SELECT * FROM users WHERE user=? AND pwd=?"
    return db.execute(query, (user, pwd))
```

## Constraints
- NUNCA sugerir código inseguro
- SEMPRE explicar o "porquê" das sugestões
- Priorizar problemas por severidade
```

### Template de persona

```yaml
---
name: senior-backend-dev
type: persona
expertise: ["Python", "APIs", "databases", "system design"]
communication_style: technical-but-accessible
---

# Senior Backend Developer

## Identidade
- **Role**: Desenvolvedor backend sênior com 10+ anos de experiência
- **Especialidades**: Python, FastAPI, PostgreSQL, Redis, arquitetura de microsserviços
- **Estilo**: Pragmático, foca em soluções que funcionam em produção

## Comportamentos core
1. Sempre considera implicações de performance e escalabilidade
2. Sugere testes para código produzido
3. Explica trade-offs de diferentes abordagens
4. Antecipa problemas de manutenção futura

## Padrões de interação
- **Ao receber task vaga**: Faz perguntas específicas antes de implementar
- **Ao encontrar bug**: Explica root cause, não apenas fix
- **Ao revisar código**: Prioriza feedback acionável

## Constraints
- Não assume stack tecnológico sem confirmar
- Sempre menciona quando não tem certeza
- Prefere simplicidade sobre over-engineering
```

### Pipeline de geração de skills

```python
class SkillGenerationPipeline:
    def __init__(self, llm, validator, storage):
        self.llm = llm
        self.validator = validator
        self.storage = storage
    
    async def generate_skill(self, request: SkillRequest) -> Skill:
        # 1. PESQUISA: Buscar informações relevantes
        research = await self.research_phase(request.description)
        
        # 2. GERAÇÃO: Criar skill via meta-prompt
        draft = await self.generation_phase(request, research)
        
        # 3. VALIDAÇÃO: Checar estrutura e qualidade
        validation = await self.validation_phase(draft)
        
        if not validation.passed:
            draft = await self.refinement_phase(draft, validation.issues)
        
        # 4. HUMAN GATE: Pausar para aprovação
        approved_skill = await self.approval_gate(draft, research.sources)
        
        # 5. COMMIT: Persistir e indexar
        await self.storage.save_skill(approved_skill)
        await self.storage.index_embeddings(approved_skill)
        
        return approved_skill

    async def research_phase(self, description: str) -> ResearchResult:
        """Busca web + validação de fontes."""
        queries = self.llm.generate_search_queries(description)
        results = await asyncio.gather(*[
            self.web_search(q) for q in queries
        ])
        return self.synthesize_research(results)
    
    async def generation_phase(self, request, research) -> Skill:
        """Meta-prompt gera skill estruturado."""
        meta_prompt = f"""
        Gere um skill seguindo o template SKILL.md.
        
        Requisição: {request.description}
        Domínio: {request.domain}
        Pesquisa: {research.summary}
        
        O skill deve incluir:
        - YAML frontmatter com metadata
        - Instruções claras e específicas
        - Pelo menos 2 exemplos concretos
        - Constraints explícitos
        """
        return self.llm.generate(meta_prompt, schema=SkillSchema)
```

### Validação multi-camada

| Camada | Verificação | Método |
|--------|-------------|--------|
| **Estrutural** | YAML válido, campos obrigatórios | JSON Schema |
| **Semântica** | Descrição match comportamento | LLM-as-judge |
| **Funcional** | Outputs corretos para inputs conhecidos | Golden set tests |
| **Segurança** | Sem prompt injection vectors | Red team patterns |
| **Performance** | Latência aceitável | Benchmark |

---

## Arquitetura de programação paralela humano-agente

Ferramentas como Cursor, Claude Code e GitHub Copilot Workspace convergem em padrões similares de colaboração. O modelo híbrido—**síncrono para exploração**, **assíncrono para execução**—emerge como mais eficiente.

### Quando usar cada modo

| Cenário | Modo recomendado |
|---------|------------------|
| Explorar problema, entender código | Síncrono |
| Bug com causa conhecida | Assíncrono |
| Arquitetura, decisões críticas | Síncrono |
| Testes, docs, refactoring | Assíncrono |
| Código sensível (auth, crypto) | Síncrono com review |

### Divisão de trabalho ideal

**Humano deve fazer:**
- Decisões de arquitetura e trade-offs
- Especificação clara de requisitos
- Review final antes de merge
- Código security-critical
- Curadoria de contexto (quais arquivos o agente deve ver)

**Agente deve fazer:**
- Boilerplate e CRUD
- Testes unitários
- Documentação
- Refactoring com padrões definidos
- Busca e explicação de código

### Padrão CLAUDE.md/AGENTS.md para PromptOS

```markdown
# PROMPTOS.md

## Contexto do projeto
Este é um sistema de geração de skills para programação.
Stack: Python 3.11, FastAPI, ChromaDB, LangGraph

## Convenções
- Usar type hints em todas as funções
- Docstrings no formato Google
- Testes com pytest, mínimo 80% coverage
- Commits semânticos (feat:, fix:, docs:)

## Skills disponíveis
- code-reviewer: Análise de código
- test-generator: Geração de testes
- doc-writer: Documentação técnica

## Comandos úteis
- `/skill create <descrição>` - Gera novo skill
- `/skill list` - Lista skills disponíveis
- `/skill test <nome>` - Testa skill existente

## Constraints
- NUNCA commitar diretamente em main
- SEMPRE rodar testes antes de PR
- Skills novos requerem aprovação humana
```

---

## State-of-the-art 2024-2026

### Padrões que definem o estado da arte

**Voyager Skill Library Pattern**: Skills como código executável indexado por embeddings semânticos. Permite composição de skills existentes para resolver novas tarefas. PromptOS deve implementar isso para skills de programação—cada skill pode chamar outros skills.

**ADAS Meta-Agent Pattern**: Um meta-agente que gera novos agentes programaticamente, testando-os e mantendo arquivo de descobertas. Para PromptOS, isso significa capacidade de auto-gerar e auto-testar novos skills.

**MCP (Model Context Protocol)**: Padrão universal para conexão de tools, adotado por OpenAI, Anthropic, Google, Microsoft. PromptOS deve ser MCP-compatible para interoperabilidade.

### Repositórios de referência

| Repositório | Stars | Padrão relevante |
|-------------|-------|------------------|
| **LangGraph** | LangChain | Workflows graph-based, checkpointing |
| **MetaGPT** | 53k+ | SOPs em prompts, assembly line |
| **Voyager** | 6.6k | Skill library evolutiva |
| **ADAS** | 1.5k | Meta-agent search |
| **agentic-memory** | - | Implementação CoALA completa |

---

## Template completo de configuração PromptOS

```yaml
# promptos-config.yaml
version: "1.0"

kernel:
  llm:
    primary: "claude-sonnet-4-20250514"
    fallback: "gpt-4o"
  
  memory:
    working:
      type: "context_window"
      max_tokens: 16000
    episodic:
      type: "chromadb"
      collection: "interactions"
      retention_days: 90
    semantic:
      type: "chromadb"
      collection: "knowledge"
    procedural:
      type: "filesystem"
      path: "./skills/"
      index: "embeddings"

  scheduler:
    max_concurrent_tasks: 3
    timeout_seconds: 300

skills:
  directory: "./skills/"
  templates: "./templates/"
  auto_index: true
  validation:
    schema: true
    golden_set: true
    llm_judge: false  # Enable for production

personas:
  directory: "./personas/"
  default: "senior-backend-dev"

workflows:
  generation:
    steps:
      - research
      - generate
      - validate
      - human_review
      - commit
    human_gates:
      - human_review
  
  execution:
    steps:
      - retrieve_skill
      - execute
      - verify
    auto_approve:
      - read_only_operations

human_in_the_loop:
  default_level: "L2"  # Colaborador
  escalation_triggers:
    - "file_modification"
    - "external_api_call"
    - "uncertainty_high"
  channels:
    - type: "cli"
    - type: "slack"
      channel: "#promptos-approvals"

observability:
  tracing: true
  cost_tracking: true
  skill_analytics: true
```

---

## Implementação mínima viável

Para começar rapidamente, implemente estas camadas em ordem:

**Fase 1 (MVP):**
1. Working memory como sliding context window
2. Skill storage em filesystem com SKILL.md format
3. Retrieval por keyword matching
4. Human gate via CLI input()
5. Single LLM para todas operações

**Fase 2 (Enhanced):**
6. Vector DB para retrieval semântico
7. Episodic memory com timestamps
8. Validação automática de schema
9. Múltiplos canais de aprovação (Slack, web)
10. Skill versioning com Git

**Fase 3 (Advanced):**
11. Meta-agent para auto-geração de skills
12. DSPy optimization de prompts
13. Multi-agent coordination
14. MCP compatibility
15. Analytics e dashboards

A arquitetura proposta combina o melhor de CoALA (memórias especializadas), Voyager (skill library evolutiva), e padrões de human-in-the-loop modernos (LangGraph interrupts). O resultado é um sistema que pode crescer organicamente—começando simples e adicionando sofisticação conforme necessário—enquanto mantém o humano no controle de decisões críticas.