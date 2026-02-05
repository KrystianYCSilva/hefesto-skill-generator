---
name: coala-framework
description: |
  Implementa o framework CoALA (Cognitive Architectures for Language Agents) com memórias especializadas e ciclo de decisão.
  Use quando: projetar arquiteturas de agentes de linguagem, implementar sistemas de memória para LLMs,
  criar agentes com raciocínio multi-etapas, ou estruturar tomada de decisão em agentes autônomos.
license: MIT
metadata: ./metadata.yaml
---

# CoALA Framework

Skill para implementação do framework **CoALA (Cognitive Architectures for Language Agents)** - uma arquitetura cognitiva que organiza agentes de linguagem em três dimensões fundamentais: **memória modular**, **espaço de ações estruturado** e **processo de decisão generalizado**.

---

## When to Use

Use esta skill quando precisar:

- **Projetar arquiteturas de agentes de linguagem** com separação clara de responsabilidades
- **Implementar sistemas de memória persistente** para LLMs (além do context window)
- **Criar agentes com raciocínio multi-etapas** e planejamento deliberativo
- **Estruturar ciclos de decisão** com fases de planejamento e execução
- **Desenvolver agentes que aprendem com experiências** passadas
- **Organizar ações internas vs. externas** em sistemas agentic
- **Migrar de prompts monolíticos** para arquiteturas modulares

**Não use para**: Simples chamadas de API a LLMs sem estado, pipelines de processamento batch sem interatividade, ou quando overhead arquitetural não é justificado.

---

## Quick Reference

### Componentes Principais

```
┌─────────────────────────────────────────────────────────────┐
│                     COALA AGENT                             │
├─────────────────────────────────────────────────────────────┤
│  MEMORY SYSTEM                                              │
│  ├── Working Memory (curto prazo): input, goals, cache      │
│  └── Long-Term Memory (longo prazo):                        │
│      ├── Episodic: experiências (ações + resultados)        │
│      ├── Semantic: fatos e conhecimento                     │
│      └── Procedural: como fazer (skills, workflows)         │
├─────────────────────────────────────────────────────────────┤
│  ACTION SPACE                                               │
│  ├── Internal: reasoning, retrieval, learning               │
│  └── External: tool_use, communication                      │
├─────────────────────────────────────────────────────────────┤
│  DECISION CYCLE                                             │
│  PLAN → EXECUTE → OBSERVE → LEARN → (repeat)               │
└─────────────────────────────────────────────────────────────┘
```

### Ciclo de Decisão CoALA

```python
# Pseudocódigo simplificado
while not goal_achieved and iterations < max:
    # 1. PLAN: Propor e avaliar ações
    actions = plan_actions(working_memory, long_term_memory)
    best_action = select_best(actions)
    
    # 2. EXECUTE: Executar ação selecionada
    result = execute(best_action);
    
    # 3. OBSERVE: Processar resultado
    observation = observe(result);
    
    # 4. LEARN: Atualizar memórias
    learn(best_action, result, observation);
    
    # Atualizar working memory
    working_memory.update(observation);
```

---

## Instructions

### Step 1: Definir Sistema de Memória

#### Working Memory (RAM do Agente)

Memória de curto prazo que persiste entre chamadas LLM no mesmo ciclo:

```python
class WorkingMemory:
    def __init__(self, max_tokens=8000):
        self.current_input = None      # Input do usuário
        self.active_goals = []         # Objetivos atuais
        self.intermediate_results = {} # Resultados de raciocínio
        self.retrieved_cache = {}      # Cache de memória recuperada
        self.max_tokens = max_tokens   # Limite de contexto
```

**Princípios**:
- Volátil: limpa ao final de cada tarefa
- Limitada: respeita context window do LLM
- Rápida: acesso O(1) para todos os dados

#### Long-Term Memory (Disco do Agente)

Três tipos especializados:

**Episodic Memory**: Experiências passadas
```python
# Armazena: "Tentei X, resultado foi Y, lição Z"
episodic_memory.store_experience(
    action="chamar API com timeout=5s",
    result="TimeoutError",
    outcome="failure",
    lesson="API lenta requer timeout maior"
)
```

**Semantic Memory**: Fatos e conhecimento
```python
# Armazena: "API X requer autenticação OAuth2"
semantic_memory.store_fact(
    fact="API X usa OAuth2 com escopo 'read-write'",
    category="authentication",
    confidence=0.95
)
```

**Procedural Memory**: Como fazer
```python
# Armazena: procedimentos e workflows
procedural_memory.store_procedure(
    name="debug_null_pointer",
    steps=["1. Check line in stack trace", 
           "2. Verify variable initialization",
           "3. Add null checks"],
    preconditions=["error is NullPointerException"]
)
```

**Implementação**: Use vector databases (Pinecone, Weaviate) ou bancos com suporte a embeddings.

### Step 2: Definir Espaço de Ações

Classifique todas as ações do agente:

| Tipo | Exemplos | Quando Usar |
|------|----------|-------------|
| **Internal - Reasoning** | Analisar, planejar, decidir | Antes de executar ação externa |
| **Internal - Retrieval** | Buscar na memória de longo prazo | Quando precisa de contexto histórico |
| **Internal - Learning** | Atualizar memórias | Após observar resultado |
| **External - Tool Use** | API calls, database queries, code execution | Interagir com mundo externo |
| **External - Communication** | Responder usuário, enviar mensagens | Entregar resultado ou pedir esclarecimento |

**Regra de Ouro**: Sempre prefira ações internas antes de externas (mais baratas, mais rápidas).

### Step 3: Implementar Ciclo de Decisão

O ciclo CoALA segue quatro fases:

#### Fase 1: PLAN (Planejamento)

```python
def plan_actions(agent_state, goal):
    """
    Usa LLM para raciocinar sobre quais ações tomar.
    Retorna lista de ações candidatas ordenadas por prioridade.
    """
    prompt = f"""
    Contexto: {agent_state.working_memory}
    Objetivo: {goal}
    Memórias relevantes: {retrieve_similar_experiences(goal)}
    
    Quais ações devem ser tomadas? Liste em ordem de prioridade.
    Considere ações internas primeiro, depois externas.
    """
    
    response = llm.generate(prompt)
    return parse_actions(response)
```

**Estratégias de Seleção**:
- **Greedy**: Escolhe ação com maior valor esperado
- **Epsilon-greedy**: Explora aleatoriamente com probabilidade ε
- **UCB**: Balanceia exploração vs. explotação

#### Fase 2: EXECUTE (Execução)

```python
def execute_action(action):
    if action.type == "internal":
        return execute_internal(action)
    else:
        return execute_external(action)

def execute_internal(action):
    if action.subtype == "reasoning":
        return llm.reason(action.prompt)
    elif action.subtype == "retrieval":
        return memory.retrieve(action.query)
    elif action.subtype == "learning":
        return memory.store(action.content)

def execute_external(action):
    if action.subtype == "tool_use":
        return call_tool(action.tool_name, action.parameters)
    elif action.subtype == "communication":
        return send_message(action.content)
```

#### Fase 3: OBSERVE (Observação)

Processa o resultado bruto em formato estruturado:

```python
def observe_result(raw_result):
    return {
        "content": raw_result,
        "success": is_successful(raw_result),
        "timestamp": now(),
        "relevance": assess_relevance(raw_result, goal)
    }
```

#### Fase 4: LEARN (Aprendizado)

Atualiza memórias de longo prazo:

```python
def learn(action, result, observation):
    # Armazenar experiência
    episodic_memory.store_experience(
        action=action,
        result=result,
        outcome="success" if observation["success"] else "failure"
    )
    
    # Extrair e armazenar fatos (se sucesso)
    if observation["success"]:
        facts = extract_facts(result)
        for fact in facts:
            semantic_memory.store_fact(fact)
```

### Step 4: Integração Completa

Template de agente CoALA mínimo:

```python
class CoALAAgent:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.working_memory = WorkingMemory()
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()
        self.procedural = ProceduralMemory()
        self.max_iterations = 10
    
    def run(self, user_input, goal=None):
        # Setup
        self.working_memory.current_input = user_input
        if goal:
            self.working_memory.active_goals.append(goal)
        
        # Ciclo principal
        for iteration in range(self.max_iterations):
            # 1. PLAN
            actions = self.plan()
            action = self.select_action(actions)
            
            # 2. EXECUTE
            result = self.execute(action)
            
            # 3. OBSERVE
            observation = self.observe(result)
            
            # 4. LEARN
            self.learn(action, result, observation)
            
            # Check completion
            if self.is_complete():
                break
        
        # Cleanup
        response = self.generate_response()
        self.working_memory.clear()
        return response
    
    def plan(self):
        # Recuperar contexto relevante
        context = self.working_memory.intermediate_results
        similar = self.episodic.retrieve_similar(
            self.working_memory.current_input
        )
        
        # Usar LLM para propor ações
        prompt = build_planning_prompt(context, similar)
        response = self.llm.generate(prompt)
        return self.parse_actions(response)
    
    def select_action(self, actions):
        # Seleciona primeira ação válida (simplificado)
        for action in actions:
            if self.check_preconditions(action):
                return action
        return actions[0] if actions else None
    
    def execute(self, action):
        if action.is_internal:
            return self.execute_internal(action)
        else:
            return self.execute_external(action)
    
    def observe(self, result):
        return {
            "content": result,
            "success": self.is_success(result),
            "timestamp": datetime.now()
        }
    
    def learn(self, action, result, observation):
        self.episodic.store_experience(
            action=action.description,
            result=result,
            outcome="success" if observation["success"] else "failure"
        )
        
        if observation["success"]:
            facts = self.extract_facts(result)
            for fact in facts:
                self.semantic.store_fact(fact)
```

---

## Best Practices

### DO (✅)

- **Mantenha working memory enxuta**: Limite a 80% da capacidade do context window
- **Recupere antes de raciocinar**: Busque memórias relevantes antes de chamar LLM
- **Use embeddings para retrieval**: Semantic search > keyword matching
- **Implemente decay de memórias**: Memórias antigas devem ter menos peso
- **Limite iterações**: Sempre tenha max_iterations para evitar loops
- **Log decisões**: Útil para debugging e análise posterior

```python
# Exemplo: Decay de memórias
def retrieve_with_decay(self, query, k=5):
    results = self.retrieve(query, k*2)
    
    # Aplicar decay exponencial baseado na idade
    now = datetime.now()
    scored = []
    for result in results:
        age_days = (now - result.timestamp).days
        decay = 0.95 ** age_days
        relevance = calculate_relevance(result, query)
        scored.append((relevance * decay, result))
    
    scored.sort(reverse=True)
    return [r for _, r in scored[:k]]
```

### DON'T (❌)

- **Não armazene tudo na working memory**: Use LTM para persistência
- **Não ignore falhas**: Aprenda com experiências negativas também
- **Não misture interno/externo sem clareza**: Separe responsabilidades
- **Não recupere sem filtro**: Sempre filtre por relevância
- **Não esqueça de limpar**: Working memory deve ser limpa após tarefa

---

## Examples

### Example 1: Agente de Pesquisa Simples

```python
agent = CoALAAgent(llm_client=openai_client)
agent.register_tool("web_search", search_function)

result = agent.run(
    user_input="Quais são os principais papers sobre RAG em 2024?",
    goal="Encontrar e sintetizar papers relevantes"
)

# Ciclo:
# 1. Recupera buscas similares passadas (episodic)
# 2. Busca conhecimento sobre RAG (semantic)
# 3. Executa web_search (external action)
# 4. Sintetiza resposta (internal reasoning)
# 5. Armazena experiência (learning)
```

### Example 2: Agente de Debugging

```python
class DebugAgent(CoALAAgent):
    def __init__(self):
        super().__init__()
        # Procedimentos pré-definidos
        self.procedural.store_procedure(
            name="debug_null_pointer",
            steps=["Check line", "Verify init", "Add checks"],
            preconditions=["NullPointerException"]
        )
    
    def run(self, error_log):
        # Recupera procedimento adequado
        procedure = self.procedural.retrieve(error_log)
        
        if procedure:
            return self.follow_procedure(procedure, error_log)
        else:
            # Explora solução nova
            return super().run(error_log)
```

---

## References

- Sumers, T. R., Yao, S., Narasimhan, K., & Griffiths, T. L. (2023). **Cognitive Architectures for Language Agents**. arXiv:2309.02427 [cs.AI]. https://arxiv.org/abs/2309.02427

- Laird, J. E. (2012). **The Soar Cognitive Architecture**. MIT Press.

- Anderson, J. R., & Lebiere, C. (2003). **The Newell Test for a theory of cognition**. Behavioral and Brain Sciences.

- Atkinson, R. C., & Shiffrin, R. M. (1968). **Human memory: A proposed system and its control processes**. Psychology of Learning and Motivation.

- Baddeley, A. D., & Hitch, G. J. (1974). **Working memory**. Psychology of Learning and Motivation.

- Yao, S., et al. (2022). **ReAct: Synergizing Reasoning and Acting in Language Models**. arXiv:2210.03629.

Para implementações detalhadas e patterns avançados, consulte:
- `./references/memory-implementation.md`
- `./references/action-space-patterns.md`
- `./references/decision-cycle-advanced.md`
- `./references/integration-examples.md`

---

**Tags**: coala, cognitive-architecture, language-agents, memory-systems, decision-making, ai-agents, llm-agents, episodic-memory, semantic-memory, procedural-memory
