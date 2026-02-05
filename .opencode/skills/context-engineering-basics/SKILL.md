---
name: context-engineering-basics
description: |
  Context engineering fundamentals for AI systems: dynamic discovery,
  compression, caching, memory consolidation, and JIT loading patterns.
  Use quando: construir agentes AI, otimizar uso de tokens, gerenciar
  memória conversacional, implementar RAG, carregar contexto incremental.
license: MIT
metadata: ./metadata.yaml
---

# Context Engineering Basics

Master context engineering fundamentals for AI agents and LLM applications. Learn strategies for dynamic context discovery, compression techniques, prompt caching optimization, memory consolidation patterns, and just-in-time context loading to maximize token efficiency and response quality.

---

## When to Use

Use esta skill quando precisar:

- **Construir agentes AI** com janelas de contexto limitadas
- **Otimizar uso de tokens** em aplicações LLM
- **Implementar sistemas de memória** para AI conversacional
- **Gerenciar bases de conhecimento** grandes com recuperação seletiva
- **Projetar conversas multi-turno** com contexto persistente

**Não use para**: Frameworks específicos (use langchain-fundamentals, etc.), infraestrutura, deployment.

---

## Instructions

### Step 1: Entender Restrições de Contexto

Antes de implementar estratégias de contexto:

1. **Identificar limites do modelo**
   - GPT-4: 8K-128K tokens
   - Claude: 200K tokens
   - Gemini: 1M-2M tokens
   - Modelos locais: 4K-32K tokens

2. **Calcular custo e latência**
   - Tokens custam dinheiro
   - Contextos maiores aumentam latência
   - Informação nas bordas pode ter menos atenção

3. **Definir estratégia**
   - Progressive disclosure: essencial primeiro, expandir conforme necessário
   - Token budget management: reservar tokens para resposta

### Step 2: Implementar Dynamic Context Discovery

**Semantic Search:**
```python
query_embedding = embed(user_query)
relevant_chunks = vector_db.search(
    query_embedding,
    top_k=5,
    threshold=0.75
)
```

**Relevance Scoring:**
```python
def score_relevance(chunk, query, history):
    scores = {
        'semantic': cosine_similarity(chunk, query),
        'recency': time_decay(chunk.timestamp),
        'frequency': access_count(chunk.id),
        'context_fit': overlap_with_history(chunk, history)
    }
    return weighted_average(scores, weights=[0.4, 0.2, 0.1, 0.3])
```

**Hybrid Search:**
```python
keyword_results = bm25_search(query, top_k=10)
semantic_results = vector_search(query, top_k=10)
combined = rerank(keyword_results + semantic_results, query)
```

**Consulte:** `references/dynamic-context-discovery.md`

### Step 3: Aplicar Context Compression

**Summarization:**
```python
def compress_conversation(history, target_ratio=0.3):
    if len(history) < 5:
        return history
    
    cutoff = int(len(history) * 0.7)
    old_messages = history[:cutoff]
    recent_messages = history[cutoff:]
    
    summary = llm.summarize(old_messages, style="bullet_points")
    return [summary] + recent_messages
```

**Entity Extraction:**
```python
entities = extract_entities(text, types=['PERSON', 'ORG', 'DATE'])
compressed = f"Entities: {entities}\nSummary: {summarize(text, max_length=100)}"
```

**Pruning Strategies:**
- **Recency**: Manter mensagens recentes, resumir antigas
- **Importance**: Pontuar cada mensagem, manter scores altos
- **Redundancy**: Remover informação duplicada ou similar

**Consulte:** `references/context-compression.md`

### Step 4: Otimizar com Prompt Caching

**KV-Cache Pattern:**
```python
system_context = """
You are an expert assistant...
[Large static context: 5000 tokens]
"""

@cache_prefix(system_context)
def handle_request(user_message):
    return llm.generate(
        prefix=system_context,  # Cached
        message=user_message
    )
```

**Claude Prompt Caching:**
```python
messages = [
    {
        "role": "system",
        "content": large_knowledge_base,
        "cache_control": {"type": "ephemeral"}
    },
    {"role": "user", "content": user_query}
]
```

**Cache Strategies:**
- Static Prefixes: System prompts, guidelines, knowledge bases
- Session Context: User profile, conversation metadata
- Incremental Updates: Append sem reprocessar

**Consulte:** `references/prompt-caching.md`

### Step 5: Implementar Memory Consolidation

**Memory Hierarchies:**
```python
class AgentMemory:
    def __init__(self):
        self.working_memory = []      # Current conversation
        self.episodic_memory = []     # Past conversations
        self.semantic_memory = {}     # Facts and knowledge
        self.procedural_memory = {}   # Learned skills
    
    def consolidate(self):
        facts = extract_facts(self.working_memory)
        self.semantic_memory.update(facts)
        
        episode = {
            'timestamp': now(),
            'summary': summarize(self.working_memory),
            'key_entities': extract_entities(self.working_memory)
        }
        self.episodic_memory.append(episode)
        self.working_memory = []
```

**CoALA Framework Integration:**
```python
memory = CoALAMemory(
    working_memory_size=10,
    episodic_retention_days=30,
    semantic_index_type='faiss'
)

memory.set_consolidation_triggers(
    max_working_size=15,
    time_interval=3600,
    importance_threshold=0.7
)
```

**Consulte:** `references/memory-consolidation.md`

### Step 6: Carregar Contexto Just-In-Time

**Lazy Loading:**
```python
class JITContextLoader:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.loaded_context = set()
    
    def load_on_demand(self, query, current_context):
        required_topics = identify_topics(query)
        
        new_context = []
        for topic in required_topics:
            if topic not in self.loaded_context:
                chunk = self.kb.get_topic(topic)
                new_context.append(chunk)
                self.loaded_context.add(topic)
        
        return current_context + new_context
```

**Incremental Expansion:**
```python
context = {
    'system': base_system_prompt,
    'user_profile': essential_user_data
}

if is_complex(query):
    context['examples'] = load_few_shot_examples(query)
    context['documentation'] = load_relevant_docs(query)

if model_uncertain(response):
    context['additional_knowledge'] = search_knowledge_base(query)
```

**Consulte:** `references/jit-context-loading.md`

### Step 7: Gerenciar Token Budget

**Token Budget Management:**
```python
class TokenBudget:
    def __init__(self, max_tokens=8000, reserve=500):
        self.max_tokens = max_tokens
        self.reserve = reserve
        self.allocated = {
            'system': 0, 'context': 0, 'history': 0, 'query': 0
        }
    
    def can_add(self, component, tokens):
        total = sum(self.allocated.values()) + tokens
        return total + self.reserve <= self.max_tokens
    
    def add(self, component, content):
        tokens = count_tokens(content)
        if self.can_add(component, tokens):
            self.allocated[component] += tokens
            return True
        return False
```

### Step 8: Implementar Graceful Degradation

**Fallback Levels:**
```python
def build_context(query, max_tokens=8000):
    context_levels = [
        ('essential', load_essential_context),
        ('recommended', load_recommended_context),
        ('optional', load_optional_context)
    ]
    
    context = ""
    for level, loader in context_levels:
        candidate = loader(query)
        if count_tokens(context + candidate) < max_tokens:
            context += candidate
        else:
            logger.warning(f"Skipped {level} context")
            break
    
    return context
```

---

## Best Practices

### 1. Qualidade sobre Quantidade

**Priorize:**
- Alta relevância sobre completude
- Recente sobre histórico (exceto quando crítico)
- Informação única sobre redundante
- Estruturado sobre não estruturado

### 2. Monitoramento

```python
@monitor_context
def generate_response(query, context):
    metrics = {
        'total_tokens': count_tokens(context),
        'compression_ratio': original_size / compressed_size,
        'cache_hit_rate': cache_hits / total_requests,
        'retrieval_latency': time_to_retrieve_context,
        'relevance_score': avg_relevance(context, query)
    }
    log_metrics(metrics)
    return llm.generate(query, context)
```

### 3. Testing

**Test Relevance:**
```python
def test_retrieval_relevance():
    test_cases = [{
        'query': "How do I reset my password?",
        'expected_topics': ['authentication', 'password_reset'],
        'unexpected_topics': ['billing', 'shipping']
    }]
    
    for case in test_cases:
        retrieved = retrieve_context(case['query'])
        topics = extract_topics(retrieved)
        assert all(t in topics for t in case['expected_topics'])
```

**Test Compression:**
```python
def test_compression_preserves_key_info():
    original = long_conversation_history
    compressed = compress_context(original, ratio=0.3)
    
    original_facts = extract_facts(original)
    compressed_facts = extract_facts(compressed)
    
    preservation_rate = len(compressed_facts) / len(original_facts)
    assert preservation_rate >= 0.8
```

---

## Common Patterns

### Pattern 1: Sliding Window with Summarization

```python
class SlidingWindowContext:
    def __init__(self, window_size=10):
        self.window_size = window_size
        self.messages = []
        self.summary = None
    
    def add_message(self, message):
        self.messages.append(message)
        
        if len(self.messages) > self.window_size:
            to_compress = self.messages[:5]
            self.summary = update_summary(self.summary, to_compress)
            self.messages = self.messages[5:]
    
    def get_context(self):
        context = []
        if self.summary:
            context.append(f"[Summary: {self.summary}]")
        context.extend(self.messages)
        return context
```

### Pattern 2: Hierarchical Context

```python
class HierarchicalContext:
    def __init__(self):
        self.layers = {
            'meta': "",        # High-level goals
            'domain': "",      # Domain knowledge
            'task': "",        # Current task
            'dialogue': []     # Conversation history
        }
    
    def render(self, detail_level='full'):
        if detail_level == 'minimal':
            return self.layers['meta'] + self.layers['task']
        elif detail_level == 'medium':
            return self.layers['meta'] + self.layers['task'] + \
                   summarize(self.layers['dialogue'])
        else:
            return "\n".join([
                self.layers['meta'],
                self.layers['domain'],
                self.layers['task'],
                format_dialogue(self.layers['dialogue'])
            ])
```

### Pattern 3: Context Routing

```python
class ContextRouter:
    def __init__(self):
        self.context_stores = {
            'product_info': ProductKnowledgeBase(),
            'user_history': UserHistoryDB(),
            'company_policy': PolicyDocuments(),
            'technical_docs': TechnicalDocs()
        }
    
    def route(self, query):
        query_type = classify_query(query)
        
        routing_rules = {
            'product_question': ['product_info', 'technical_docs'],
            'account_issue': ['user_history', 'company_policy'],
            'technical_support': ['technical_docs', 'user_history']
        }
        
        stores_to_query = routing_rules.get(query_type, ['product_info'])
        
        context = []
        for store_name in stores_to_query:
            store = self.context_stores[store_name]
            context.extend(store.search(query, top_k=3))
        
        return context
```

---

## Anti-Patterns

### ❌ Context Dumping
```python
# DON'T
context = load_entire_database()  # 100K tokens!

# DO
context = semantic_search(query, top_k=5)  # ~2K tokens
```

### ❌ Ignoring Recency
```python
# DON'T
context = all_messages

# DO
recent = messages[-10:]
summary_of_old = summarize(messages[:-10])
context = [summary_of_old] + recent
```

### ❌ Static Context
```python
# DON'T
context = fixed_knowledge_base
for query in queries:
    response = llm.generate(query, context)

# DO
for query in queries:
    context = retrieve_relevant(query, knowledge_base)
    response = llm.generate(query, context)
```

---

## Platform-Specific

**OpenAI (GPT-4):**
- Context: 8K-128K tokens
- No native caching (use app-level)
- Function calling reduces context needs

**Anthropic (Claude):**
- Context: 200K tokens
- Native prompt caching (`cache_control`)
- Extended context enables document analysis

**Google (Gemini):**
- Context: 1M-2M tokens
- Massive context enables different strategies
- Still benefits from relevance filtering

**Local Models:**
- Context: 4K-32K tokens (typically)
- Context compression critical
- Optimize for inference speed

---

## References

Para técnicas avançadas e implementações detalhadas:

- **[Dynamic Context Discovery](./references/dynamic-context-discovery.md)** - Advanced retrieval, hybrid search, reranking
- **[Context Compression](./references/context-compression.md)** - Summarization, entity extraction, pruning
- **[Prompt Caching](./references/prompt-caching.md)** - KV-cache optimization, provider implementations
- **[Memory Consolidation](./references/memory-consolidation.md)** - Memory hierarchies, CoALA framework
- **[JIT Context Loading](./references/jit-context-loading.md)** - Lazy loading, incremental expansion

---

## Sources

1. **Anthropic Prompt Caching** - https://docs.anthropic.com/claude/docs/prompt-caching - Official docs
2. **OpenAI Prompt Engineering** - https://platform.openai.com/docs/guides/prompt-engineering - Official docs
3. **LangChain Memory Management** - https://python.langchain.com/docs/modules/memory/ - Framework docs
4. **CoALA Framework** - https://arxiv.org/abs/2309.02427 - Research paper
5. **RAG Evaluation** - https://arxiv.org/abs/2401.15884 - Research paper
6. **Lost in the Middle** - https://arxiv.org/abs/2307.03172 - Research paper
7. **LlamaIndex** - https://docs.llamaindex.ai - Framework docs
8. **Efficient Memory Management** - https://arxiv.org/abs/2309.06180 - Research paper
