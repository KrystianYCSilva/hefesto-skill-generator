# Context Engineering Basics

## Overview

Master context engineering fundamentals for AI agents and LLM applications. Learn strategies for dynamic context discovery, compression techniques, prompt caching optimization, memory consolidation patterns, and just-in-time context loading to maximize token efficiency and response quality.

**Use when:**
- Building AI agents with limited context windows
- Optimizing token usage in LLM applications
- Implementing memory systems for conversational AI
- Managing large knowledge bases with selective retrieval
- Designing multi-turn conversations with persistent context

**Core Techniques:**
- Dynamic Context Discovery (relevance scoring, semantic search)
- Context Compression (summarization, entity extraction, pruning)
- Prompt Caching (KV-cache optimization, prefix reuse)
- Memory Consolidation (episodic/semantic memory patterns)
- JIT Context Loading (lazy loading, incremental context expansion)

---

## Skill Metadata

```yaml
---
name: context-engineering-basics
description: |
  Context engineering fundamentals for AI systems: dynamic discovery,
  compression, caching, memory consolidation, and JIT loading patterns.
  Use when optimizing token efficiency or managing large knowledge bases.
license: MIT
metadata: ./metadata.yaml
---
```

---

## Core Concepts

### 1. Context Window Constraints

Modern LLMs have finite context windows (4K-200K tokens). Effective context engineering maximizes information density within these limits.

**Key Constraints:**
- **Token Limits**: GPT-4 (8K-128K), Claude (200K), Gemini (1M-2M)
- **Cost**: Tokens cost money; larger contexts = higher costs
- **Latency**: Longer contexts increase processing time
- **Attention Decay**: Information at context boundaries may be less attended

**Strategy**: Progressive disclosure - load essential context first, expand as needed.

---

### 2. Dynamic Context Discovery

Identify and retrieve relevant information from large knowledge bases in real-time.

**Techniques:**

#### Semantic Search
```python
# Vector similarity search
query_embedding = embed(user_query)
relevant_chunks = vector_db.search(
    query_embedding,
    top_k=5,
    threshold=0.75
)
```

#### Relevance Scoring
```python
def score_relevance(chunk, query, conversation_history):
    """Multi-factor relevance scoring"""
    scores = {
        'semantic': cosine_similarity(chunk, query),
        'recency': time_decay(chunk.timestamp),
        'frequency': access_count(chunk.id),
        'context_fit': overlap_with_history(chunk, conversation_history)
    }
    return weighted_average(scores, weights=[0.4, 0.2, 0.1, 0.3])
```

#### Hybrid Search
Combine keyword matching (BM25) with semantic search for better precision:

```python
# Hybrid retrieval
keyword_results = bm25_search(query, top_k=10)
semantic_results = vector_search(query, top_k=10)
combined = rerank(keyword_results + semantic_results, query)
```

**See**: `references/dynamic-context-discovery.md` for advanced patterns.

---

### 3. Context Compression

Reduce token count while preserving essential information.

**Compression Strategies:**

#### Summarization
```python
def compress_conversation(history, target_ratio=0.3):
    """Compress conversation history to target ratio"""
    if len(history) < 5:
        return history  # Don't compress short conversations

    # Summarize older messages, keep recent ones verbatim
    cutoff = int(len(history) * 0.7)
    old_messages = history[:cutoff]
    recent_messages = history[cutoff:]

    summary = llm.summarize(old_messages, style="bullet_points")
    return [summary] + recent_messages
```

#### Entity Extraction
```python
# Extract key entities to reduce noise
entities = extract_entities(text, types=['PERSON', 'ORG', 'DATE', 'LOCATION'])
compressed = f"Entities: {entities}\nSummary: {summarize(text, max_length=100)}"
```

#### Pruning Strategies
- **Recency**: Keep recent messages, summarize old ones
- **Importance**: Score each message, keep high-scoring ones
- **Redundancy**: Remove duplicate or highly similar information

**See**: `references/context-compression.md` for complete techniques.

---

### 4. Prompt Caching

Optimize repeated context reuse through caching mechanisms.

**KV-Cache Optimization:**

```python
# Prefix caching pattern
system_context = """
You are an expert assistant...
[Large static context: 5000 tokens]
"""

# Cache this prefix across requests
@cache_prefix(system_context)
def handle_request(user_message):
    return llm.generate(
        prefix=system_context,  # Cached, not re-processed
        message=user_message
    )
```

**Claude Prompt Caching:**
```python
# Anthropic's prompt caching
messages = [
    {
        "role": "system",
        "content": large_knowledge_base,
        "cache_control": {"type": "ephemeral"}  # Cache this
    },
    {
        "role": "user",
        "content": user_query
    }
]
```

**Cache Strategies:**
- **Static Prefixes**: System prompts, guidelines, knowledge bases
- **Session Context**: User profile, conversation metadata
- **Incremental Updates**: Append to cached context without reprocessing

**See**: `references/prompt-caching.md` for provider-specific implementations.

---

### 5. Memory Consolidation

Organize information into structured memory systems.

**Memory Hierarchies:**

```python
class AgentMemory:
    def __init__(self):
        self.working_memory = []      # Current conversation (short-term)
        self.episodic_memory = []     # Past conversations (events)
        self.semantic_memory = {}     # Facts and knowledge
        self.procedural_memory = {}   # Learned skills/patterns

    def consolidate(self):
        """Move working memory to long-term storage"""
        # Extract important facts
        facts = extract_facts(self.working_memory)
        self.semantic_memory.update(facts)

        # Store conversation as episode
        episode = {
            'timestamp': now(),
            'summary': summarize(self.working_memory),
            'key_entities': extract_entities(self.working_memory)
        }
        self.episodic_memory.append(episode)

        # Clear working memory
        self.working_memory = []
```

**CoALA Framework Integration:**
```python
# Cognitive Architecture for Language Agents
memory = CoALAMemory(
    working_memory_size=10,
    episodic_retention_days=30,
    semantic_index_type='faiss'
)

# Automatic consolidation triggers
memory.set_consolidation_triggers(
    max_working_size=15,
    time_interval=3600,  # Every hour
    importance_threshold=0.7
)
```

**See**: `references/memory-consolidation.md` for advanced patterns.

---

### 6. Just-In-Time (JIT) Context Loading

Load context incrementally based on need, not upfront.

**Lazy Loading Pattern:**

```python
class JITContextLoader:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.loaded_context = set()

    def load_on_demand(self, query, current_context):
        """Load only what's needed for this query"""
        # Identify required context
        required_topics = identify_topics(query)

        # Load only new required context
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
# Start with minimal context
context = {
    'system': base_system_prompt,
    'user_profile': essential_user_data
}

# Expand based on query complexity
if is_complex(query):
    context['examples'] = load_few_shot_examples(query)
    context['documentation'] = load_relevant_docs(query)

# Expand based on errors/uncertainty
if model_uncertain(response):
    context['additional_knowledge'] = search_knowledge_base(query)
```

**See**: `references/jit-context-loading.md` for implementation patterns.

---

## Best Practices

### 1. Token Budget Management

```python
class TokenBudget:
    def __init__(self, max_tokens=8000, reserve=500):
        self.max_tokens = max_tokens
        self.reserve = reserve  # Reserve for response
        self.allocated = {
            'system': 0,
            'context': 0,
            'history': 0,
            'query': 0
        }

    def can_add(self, component, tokens):
        """Check if we can add more context"""
        total = sum(self.allocated.values()) + tokens
        return total + self.reserve <= self.max_tokens

    def add(self, component, content):
        """Add content with token tracking"""
        tokens = count_tokens(content)
        if self.can_add(component, tokens):
            self.allocated[component] += tokens
            return True
        return False
```

### 2. Context Quality over Quantity

**Prioritize:**
- High-relevance over completeness
- Recent over historical (unless historical is critical)
- Unique information over redundant
- Structured over unstructured

### 3. Monitoring and Metrics

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

### 4. Graceful Degradation

```python
def build_context(query, max_tokens=8000):
    """Build context with fallback levels"""
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
            logger.warning(f"Skipped {level} context due to token limits")
            break

    return context
```

---

## Common Patterns

### Pattern 1: Sliding Window with Summarization

```python
class SlidingWindowContext:
    def __init__(self, window_size=10, compression_ratio=0.3):
        self.window_size = window_size
        self.compression_ratio = compression_ratio
        self.messages = []
        self.summary = None

    def add_message(self, message):
        self.messages.append(message)

        if len(self.messages) > self.window_size:
            # Compress oldest messages
            to_compress = self.messages[:5]
            self.summary = update_summary(self.summary, to_compress)
            self.messages = self.messages[5:]

    def get_context(self):
        context = []
        if self.summary:
            context.append(f"[Previous conversation summary: {self.summary}]")
        context.extend(self.messages)
        return context
```

### Pattern 2: Hierarchical Context

```python
class HierarchicalContext:
    """Context organized by abstraction levels"""

    def __init__(self):
        self.layers = {
            'meta': "",        # High-level goals, constraints
            'domain': "",      # Domain knowledge, ontologies
            'task': "",        # Current task context
            'dialogue': []     # Conversation history
        }

    def render(self, detail_level='full'):
        """Render context at specified detail level"""
        if detail_level == 'minimal':
            return self.layers['meta'] + self.layers['task']
        elif detail_level == 'medium':
            return self.layers['meta'] + self.layers['task'] + \
                   summarize(self.layers['dialogue'])
        else:  # full
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
    """Route queries to appropriate context subsets"""

    def __init__(self):
        self.context_stores = {
            'product_info': ProductKnowledgeBase(),
            'user_history': UserHistoryDB(),
            'company_policy': PolicyDocuments(),
            'technical_docs': TechnicalDocs()
        }

    def route(self, query):
        """Determine which context stores to query"""
        query_type = classify_query(query)

        routing_rules = {
            'product_question': ['product_info', 'technical_docs'],
            'account_issue': ['user_history', 'company_policy'],
            'technical_support': ['technical_docs', 'user_history']
        }

        stores_to_query = routing_rules.get(query_type, ['product_info'])

        # Retrieve from relevant stores only
        context = []
        for store_name in stores_to_query:
            store = self.context_stores[store_name]
            context.extend(store.search(query, top_k=3))

        return context
```

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Context Dumping

```python
# DON'T: Load entire knowledge base
context = load_entire_database()  # 100K tokens!
response = llm.generate(query, context)
```

**Fix**: Use dynamic retrieval
```python
# DO: Load only relevant chunks
context = semantic_search(query, top_k=5)  # ~2K tokens
response = llm.generate(query, context)
```

### ❌ Anti-Pattern 2: Ignoring Recency

```python
# DON'T: Treat all history equally
context = all_messages  # Includes irrelevant old messages
```

**Fix**: Apply time decay
```python
# DO: Prioritize recent context
recent = messages[-10:]
summary_of_old = summarize(messages[:-10])
context = [summary_of_old] + recent
```

### ❌ Anti-Pattern 3: Static Context

```python
# DON'T: Use same context for all queries
context = fixed_knowledge_base
for query in queries:
    response = llm.generate(query, context)
```

**Fix**: Dynamic context per query
```python
# DO: Adapt context to each query
for query in queries:
    context = retrieve_relevant(query, knowledge_base)
    response = llm.generate(query, context)
```

### ❌ Anti-Pattern 4: No Token Tracking

```python
# DON'T: Add context blindly
context = system + history + knowledge + examples  # Hope it fits!
```

**Fix**: Track and limit tokens
```python
# DO: Manage token budget
budget = TokenBudget(max_tokens=8000)
if budget.can_add('system', system_prompt):
    budget.add('system', system_prompt)
# ... add components with budget checks
```

---

## Testing Context Strategies

### Test 1: Relevance Accuracy

```python
def test_retrieval_relevance():
    """Test that retrieved context is actually relevant"""
    test_cases = [
        {
            'query': "How do I reset my password?",
            'expected_topics': ['authentication', 'password_reset'],
            'unexpected_topics': ['billing', 'shipping']
        }
    ]

    for case in test_cases:
        retrieved = retrieve_context(case['query'])
        topics = extract_topics(retrieved)

        assert all(t in topics for t in case['expected_topics'])
        assert not any(t in topics for t in case['unexpected_topics'])
```

### Test 2: Compression Quality

```python
def test_compression_preserves_key_info():
    """Ensure compression doesn't lose critical information"""
    original = long_conversation_history
    compressed = compress_context(original, ratio=0.3)

    # Extract key facts from both
    original_facts = extract_facts(original)
    compressed_facts = extract_facts(compressed)

    # Should preserve 80%+ of key facts
    preservation_rate = len(compressed_facts) / len(original_facts)
    assert preservation_rate >= 0.8
```

### Test 3: Token Budget Compliance

```python
def test_token_limits():
    """Verify context stays within token limits"""
    max_tokens = 8000
    for query in test_queries:
        context = build_context(query, max_tokens=max_tokens)
        actual_tokens = count_tokens(context)

        assert actual_tokens <= max_tokens
        assert actual_tokens >= max_tokens * 0.7  # Use at least 70% of budget
```

---

## Platform-Specific Considerations

### OpenAI (GPT-4, GPT-3.5)

- Context window: 8K-128K depending on model
- No native prompt caching (use application-level caching)
- Function calling can reduce context needs
- Use `max_tokens` to reserve space for responses

### Anthropic (Claude)

- Context window: 200K tokens (Claude 3.5)
- Native prompt caching with `cache_control` parameter
- Extended context enables document analysis
- System prompts can be cached separately

### Google (Gemini)

- Context window: 1M-2M tokens (Gemini 1.5/2.0)
- Massive context enables different strategies
- Can include entire codebases or documents
- Still benefits from relevance filtering

### Local Models (Llama, Mistral)

- Smaller context windows (4K-32K typically)
- Context compression critical
- Optimize for inference speed
- Consider quantization impact on context handling

---

## Integration Examples

### Example 1: RAG with Context Engineering

```python
class ContextEngineeredRAG:
    def __init__(self, vector_db, llm):
        self.vector_db = vector_db
        self.llm = llm
        self.budget = TokenBudget(max_tokens=8000)

    def query(self, question, conversation_history=None):
        # 1. Dynamic retrieval
        candidates = self.vector_db.search(question, top_k=20)

        # 2. Rerank by relevance
        relevant = self.rerank(candidates, question, conversation_history)

        # 3. Compress if needed
        context = self.build_context(relevant, conversation_history)

        # 4. Generate with budget compliance
        if count_tokens(context) > self.budget.max_tokens:
            context = self.compress(context)

        return self.llm.generate(question, context)

    def rerank(self, candidates, question, history):
        """Rerank by multiple factors"""
        scored = [
            (doc, score_relevance(doc, question, history))
            for doc in candidates
        ]
        return [doc for doc, score in sorted(scored, key=lambda x: x[1], reverse=True)]

    def build_context(self, docs, history):
        """Build context with token budget"""
        context_parts = []

        # Add compressed history
        if history:
            compressed_history = compress_conversation(history)
            if self.budget.can_add('history', compressed_history):
                self.budget.add('history', compressed_history)
                context_parts.append(compressed_history)

        # Add documents until budget exhausted
        for doc in docs:
            if self.budget.can_add('context', doc):
                self.budget.add('context', doc)
                context_parts.append(doc)
            else:
                break

        return "\n\n".join(context_parts)
```

### Example 2: Multi-Agent Context Sharing

```python
class SharedContextManager:
    """Manage context across multiple agents"""

    def __init__(self):
        self.global_context = {}
        self.agent_contexts = defaultdict(list)

    def update_global(self, key, value):
        """Update shared context available to all agents"""
        self.global_context[key] = value

    def get_agent_context(self, agent_id, query):
        """Get personalized context for specific agent"""
        # Combine global + agent-specific + query-relevant
        context = {
            'global': self.global_context,
            'agent_history': self.agent_contexts[agent_id][-10:],
            'relevant': self.retrieve_relevant(query)
        }
        return self.render_context(context)

    def consolidate_agent_output(self, agent_id, output):
        """Extract learnings from agent output to shared context"""
        facts = extract_facts(output)
        for fact in facts:
            if is_globally_relevant(fact):
                self.update_global(fact['key'], fact['value'])

        self.agent_contexts[agent_id].append(output)
```

---

## Resources

### References

1. **Dynamic Context Discovery** (`references/dynamic-context-discovery.md`)
   - Advanced retrieval strategies
   - Hybrid search implementations
   - Relevance scoring algorithms

2. **Context Compression** (`references/context-compression.md`)
   - Summarization techniques
   - Entity extraction methods
   - Redundancy elimination

3. **Prompt Caching** (`references/prompt-caching.md`)
   - Provider-specific implementations
   - Cache invalidation strategies
   - Performance optimization

4. **Memory Consolidation** (`references/memory-consolidation.md`)
   - Memory hierarchy patterns
   - CoALA framework integration
   - Long-term storage strategies

5. **JIT Context Loading** (`references/jit-context-loading.md`)
   - Lazy loading patterns
   - Incremental expansion
   - Performance considerations

### External Resources

- **LangChain Context Management**: https://python.langchain.com/docs/modules/memory/
- **Anthropic Prompt Caching**: https://docs.anthropic.com/claude/docs/prompt-caching
- **OpenAI Best Practices**: https://platform.openai.com/docs/guides/prompt-engineering
- **CoALA Framework Paper**: https://arxiv.org/abs/2309.02427
- **RAG Evaluation**: https://arxiv.org/abs/2401.15884

---

## License

MIT License - See LICENSE file for details

---

**Version**: 1.0.0
**Last Updated**: 2026-02-05
**Maintainer**: Hefesto Skill Generator
