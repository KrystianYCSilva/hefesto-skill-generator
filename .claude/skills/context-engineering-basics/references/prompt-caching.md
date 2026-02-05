# Prompt Caching

## Overview

Prompt caching optimizes repeated context reuse by storing and reusing previously processed context, reducing computation costs and latency. Different providers implement caching with varying mechanisms and capabilities.

**Key Benefits:**
- **Cost Reduction**: Cached tokens cost 10-90% less than fresh tokens
- **Latency Reduction**: Skip re-processing of static context
- **Consistency**: Same context produces same initial state
- **Scalability**: Handle more requests with same resources

**Use Cases:**
- Static system prompts that rarely change
- Large knowledge bases queried repeatedly
- Few-shot examples shared across requests
- Conversation context in multi-turn dialogues

---

## Provider Implementations

### 1. Anthropic Claude (Prompt Caching)

Claude offers native prompt caching via the `cache_control` parameter.

#### Basic Usage

```python
import anthropic

client = anthropic.Anthropic(api_key="your-key")

# Mark content for caching
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert assistant with access to the following knowledge base...",
        },
        {
            "type": "text",
            "text": large_knowledge_base_content,  # e.g., 50K tokens
            "cache_control": {"type": "ephemeral"}  # Cache this block
        }
    ],
    messages=[
        {"role": "user", "content": "What is X?"}
    ]
)

# Subsequent requests with same cached content are faster/cheaper
response2 = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert assistant with access to the following knowledge base...",
        },
        {
            "type": "text",
            "text": large_knowledge_base_content,  # Same content = cache hit
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {"role": "user", "content": "What is Y?"}  # Different query, same context
    ]
)
```

#### Cache Behavior

- **TTL**: 5 minutes (ephemeral cache)
- **Minimum Size**: 1024 tokens minimum for caching
- **Prefix Matching**: Cache matches on exact prefix
- **Cost**: Cached tokens cost 10% of regular input tokens

#### Multi-Level Caching

```python
# Cache multiple levels with different lifetimes
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": static_guidelines,  # Level 1: Static
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": knowledge_base,  # Level 2: Semi-static
            "cache_control": {"type": "ephemeral"}
        },
        {
            "type": "text",
            "text": user_profile  # Level 3: User-specific
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=messages
)
```

#### Conversational Caching

```python
class CachedConversation:
    def __init__(self, client, system_prompt, knowledge_base):
        self.client = client
        self.system_prompt = system_prompt
        self.knowledge_base = knowledge_base
        self.messages = []

    def add_turn(self, user_message):
        """Add user message and get response"""
        self.messages.append({"role": "user", "content": user_message})

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": self.system_prompt,
                    "cache_control": {"type": "ephemeral"}
                },
                {
                    "type": "text",
                    "text": self.knowledge_base,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=self.messages
        )

        assistant_message = response.content[0].text
        self.messages.append({"role": "assistant", "content": assistant_message})

        return assistant_message

# Usage
conversation = CachedConversation(client, system_prompt, kb)
response1 = conversation.add_turn("Tell me about X")
response2 = conversation.add_turn("What about Y?")
# system_prompt and kb are cached across both turns
```

---

### 2. OpenAI (Application-Level Caching)

OpenAI doesn't have native prompt caching, so implement at application level.

#### Simple Cache Implementation

```python
import hashlib
import json
from datetime import datetime, timedelta

class OpenAICache:
    def __init__(self, ttl_minutes=5):
        self.cache = {}
        self.ttl = timedelta(minutes=ttl_minutes)

    def _compute_key(self, system_prompt, messages):
        """Compute cache key from context"""
        content = json.dumps({
            'system': system_prompt,
            'messages': messages
        }, sort_keys=True)
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, system_prompt, messages):
        """Get cached response if available"""
        key = self._compute_key(system_prompt, messages)

        if key in self.cache:
            entry = self.cache[key]
            if datetime.now() - entry['timestamp'] < self.ttl:
                return entry['response']
            else:
                # Expired
                del self.cache[key]

        return None

    def set(self, system_prompt, messages, response):
        """Cache response"""
        key = self._compute_key(system_prompt, messages)
        self.cache[key] = {
            'response': response,
            'timestamp': datetime.now()
        }

    def generate_with_cache(self, client, system_prompt, messages, **kwargs):
        """Generate with caching"""
        # Check cache
        cached = self.get(system_prompt, messages)
        if cached:
            return cached

        # Generate
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                *messages
            ],
            **kwargs
        )

        # Cache result
        self.set(system_prompt, messages, response)

        return response

# Usage
cache = OpenAICache(ttl_minutes=5)
response = cache.generate_with_cache(
    client,
    system_prompt="You are a helpful assistant",
    messages=[{"role": "user", "content": "Hello"}],
    model="gpt-4"
)
```

#### Prefix Caching Pattern

```python
class PrefixCache:
    """Cache static prefixes separately"""

    def __init__(self):
        self.prefix_cache = {}

    def compute_prefix_embedding(self, prefix):
        """
        For models that support embeddings of prompts,
        cache the embedding representation
        """
        # Placeholder: In practice, use model's internal representation
        return hashlib.sha256(prefix.encode()).hexdigest()

    def generate_with_prefix(self, client, static_prefix, dynamic_content, **kwargs):
        """Generate with cached prefix"""
        prefix_id = self.compute_prefix_embedding(static_prefix)

        # In real implementation, pass prefix_id to model to reuse KV-cache
        # For OpenAI, combine and generate normally
        full_prompt = static_prefix + "\n\n" + dynamic_content

        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": full_prompt}
            ],
            **kwargs
        )

        return response
```

---

### 3. Google Gemini (Context Caching)

Gemini offers context caching for long-context scenarios.

#### Basic Usage

```python
import google.generativeai as genai

genai.configure(api_key="your-key")

# Create cached content
cache = genai.caching.CachedContent.create(
    model='models/gemini-1.5-flash-001',
    display_name='knowledge_base_cache',
    system_instruction='You are an expert assistant',
    contents=[
        {'text': large_knowledge_base}
    ],
    ttl='3600s'  # 1 hour
)

# Use cached content
model = genai.GenerativeModel.from_cached_content(cached_content=cache)
response = model.generate_content('What is X in the knowledge base?')

# Reuse cache for subsequent requests
response2 = model.generate_content('Tell me about Y')
```

#### Cache Management

```python
class GeminiCacheManager:
    def __init__(self):
        self.caches = {}

    def get_or_create_cache(self, cache_key, content, ttl_seconds=3600):
        """Get existing cache or create new one"""
        if cache_key in self.caches:
            cache = self.caches[cache_key]
            # Check if still valid
            try:
                cache.get()  # Will raise if expired
                return cache
            except:
                del self.caches[cache_key]

        # Create new cache
        cache = genai.caching.CachedContent.create(
            model='models/gemini-1.5-flash-001',
            contents=[{'text': content}],
            ttl=f'{ttl_seconds}s'
        )

        self.caches[cache_key] = cache
        return cache

    def list_caches(self):
        """List all active caches"""
        return genai.caching.CachedContent.list()

    def delete_cache(self, cache_key):
        """Delete specific cache"""
        if cache_key in self.caches:
            self.caches[cache_key].delete()
            del self.caches[cache_key]
```

---

### 4. Local Models (KV-Cache Optimization)

For local models (Llama, Mistral, etc.), optimize KV-cache usage.

#### llama.cpp Example

```python
from llama_cpp import Llama

class KVCacheOptimizedModel:
    def __init__(self, model_path):
        self.llm = Llama(
            model_path=model_path,
            n_ctx=8192,  # Context window
            n_gpu_layers=35  # Offload layers to GPU
        )
        self.static_prefix = None
        self.prefix_tokens = None

    def set_static_prefix(self, prefix):
        """Set and tokenize static prefix"""
        self.static_prefix = prefix
        self.prefix_tokens = self.llm.tokenize(prefix.encode('utf-8'))

    def generate(self, dynamic_content, max_tokens=256):
        """Generate with cached prefix"""
        if self.prefix_tokens:
            # Tokenize dynamic content
            dynamic_tokens = self.llm.tokenize(dynamic_content.encode('utf-8'))

            # Combine tokens
            full_tokens = self.prefix_tokens + dynamic_tokens

            # Generate (model internally caches KV for prefix)
            response = self.llm.generate(full_tokens, max_tokens=max_tokens)
        else:
            response = self.llm(dynamic_content, max_tokens=max_tokens)

        return response

# Usage
model = KVCacheOptimizedModel("model.gguf")
model.set_static_prefix("You are an expert assistant with knowledge of...")

response1 = model.generate("What is X?")
response2 = model.generate("What is Y?")
# Prefix KV-cache reused automatically
```

---

## Cache Strategies

### 1. Hierarchical Caching

Cache at multiple levels with different TTLs.

```python
class HierarchicalCache:
    def __init__(self):
        self.levels = {
            'static': {'ttl': 3600, 'cache': {}},      # 1 hour - rarely changes
            'semi_static': {'ttl': 300, 'cache': {}},  # 5 min - periodic updates
            'dynamic': {'ttl': 60, 'cache': {}}        # 1 min - frequent changes
        }

    def build_context(self, static_content, semi_static_content, dynamic_content):
        """Build context with multi-level caching"""
        context_parts = []

        # Try to get each level from cache
        for level_name, level_content in [
            ('static', static_content),
            ('semi_static', semi_static_content),
            ('dynamic', dynamic_content)
        ]:
            level = self.levels[level_name]
            cache_key = hashlib.sha256(level_content.encode()).hexdigest()

            cached = self._get_from_level(level_name, cache_key)
            if cached:
                context_parts.append(cached)
            else:
                # Process and cache
                processed = self._process_content(level_content)
                self._set_in_level(level_name, cache_key, processed)
                context_parts.append(processed)

        return "\n\n".join(context_parts)

    def _get_from_level(self, level_name, key):
        """Get from specific cache level"""
        level = self.levels[level_name]
        if key in level['cache']:
            entry = level['cache'][key]
            if datetime.now() - entry['timestamp'] < timedelta(seconds=level['ttl']):
                return entry['content']
        return None

    def _set_in_level(self, level_name, key, content):
        """Set in specific cache level"""
        level = self.levels[level_name]
        level['cache'][key] = {
            'content': content,
            'timestamp': datetime.now()
        }

    def _process_content(self, content):
        """Process content (e.g., embed, compress)"""
        # Placeholder for actual processing
        return content
```

### 2. Incremental Caching

Cache grows incrementally as conversation progresses.

```python
class IncrementalCache:
    def __init__(self, client):
        self.client = client
        self.cached_context = []
        self.cache_version = 0

    def add_to_cache(self, content):
        """Add content to cached context"""
        self.cached_context.append(content)
        self.cache_version += 1

    def generate(self, user_message):
        """Generate using incrementally cached context"""
        # Build full context from cache + new message
        full_context = self.cached_context + [user_message]

        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=[
                {
                    "type": "text",
                    "text": "\n".join(self.cached_context),
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        return response.content[0].text

# Usage
cache = IncrementalCache(client)
cache.add_to_cache("You are an expert assistant.")
cache.add_to_cache("You have access to database schema: ...")

response1 = cache.generate("Show me users table")
# Next query benefits from cached context
response2 = cache.generate("What are the columns?")
```

### 3. Cache Warming

Pre-populate cache before heavy load.

```python
def warm_cache(client, common_contexts):
    """Warm up cache with common contexts"""
    for context_name, context_content in common_contexts.items():
        # Make dummy request to populate cache
        client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1,
            system=[
                {
                    "type": "text",
                    "text": context_content,
                    "cache_control": {"type": "ephemeral"}
                }
            ],
            messages=[
                {"role": "user", "content": "ping"}
            ]
        )
        print(f"Warmed cache: {context_name}")

# Usage
common_contexts = {
    'product_catalog': load_product_catalog(),
    'support_docs': load_support_docs(),
    'company_policy': load_policies()
}

warm_cache(client, common_contexts)
# Now all subsequent requests will hit warm cache
```

---

## Performance Monitoring

### Cache Hit Rate Tracking

```python
class CacheMonitor:
    def __init__(self):
        self.stats = {
            'hits': 0,
            'misses': 0,
            'total_cached_tokens': 0,
            'cost_saved': 0.0
        }

    def record_hit(self, cached_tokens):
        """Record cache hit"""
        self.stats['hits'] += 1
        self.stats['total_cached_tokens'] += cached_tokens

        # Calculate cost saved (assuming cached tokens cost 10% of normal)
        normal_cost = cached_tokens * 0.000003  # $3 per 1M tokens
        cached_cost = cached_tokens * 0.0000003  # 10% of normal
        self.stats['cost_saved'] += (normal_cost - cached_cost)

    def record_miss(self):
        """Record cache miss"""
        self.stats['misses'] += 1

    def get_metrics(self):
        """Get cache performance metrics"""
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = self.stats['hits'] / total_requests if total_requests > 0 else 0

        return {
            'hit_rate': hit_rate,
            'total_requests': total_requests,
            'cache_hits': self.stats['hits'],
            'cache_misses': self.stats['misses'],
            'total_cached_tokens': self.stats['total_cached_tokens'],
            'cost_saved_usd': self.stats['cost_saved']
        }

    def print_report(self):
        """Print performance report"""
        metrics = self.get_metrics()
        print(f"""
Cache Performance Report
========================
Hit Rate: {metrics['hit_rate']:.2%}
Total Requests: {metrics['total_requests']}
Cache Hits: {metrics['cache_hits']}
Cache Misses: {metrics['cache_misses']}
Cached Tokens: {metrics['total_cached_tokens']:,}
Cost Saved: ${metrics['cost_saved_usd']:.4f}
        """)
```

---

## Best Practices

### 1. Cache Key Design

```python
# GOOD: Stable cache keys
cache_key = hashlib.sha256(
    json.dumps({
        'version': 'v1',
        'content': static_content,
        'type': 'knowledge_base'
    }, sort_keys=True).encode()
).hexdigest()

# BAD: Unstable keys (includes timestamp)
cache_key = f"{static_content}_{datetime.now()}"
```

### 2. Cache Invalidation

```python
class VersionedCache:
    def __init__(self):
        self.cache = {}
        self.versions = {}

    def set(self, key, value, version='v1'):
        """Set with version"""
        versioned_key = f"{key}:{version}"
        self.cache[versioned_key] = value
        self.versions[key] = version

    def get(self, key):
        """Get latest version"""
        version = self.versions.get(key, 'v1')
        versioned_key = f"{key}:{version}"
        return self.cache.get(versioned_key)

    def invalidate(self, key):
        """Invalidate by bumping version"""
        current_version = self.versions.get(key, 'v0')
        new_version = f"v{int(current_version[1:]) + 1}"
        self.versions[key] = new_version
```

### 3. Cost-Benefit Analysis

```python
def should_cache(content, request_frequency, cache_ttl_hours=1):
    """Decide if content should be cached"""
    tokens = count_tokens(content)

    # Only cache if > 1024 tokens (Anthropic minimum)
    if tokens < 1024:
        return False

    # Estimate requests within TTL
    requests_in_ttl = request_frequency * cache_ttl_hours

    # Cost without caching
    cost_without = tokens * requests_in_ttl * 0.000003  # $3/1M tokens

    # Cost with caching (first request normal, rest at 10%)
    cost_with = (tokens * 0.000003) + (tokens * (requests_in_ttl - 1) * 0.0000003)

    savings = cost_without - cost_with

    # Cache if savings > $0.01
    return savings > 0.01
```

---

## Resources

- **Anthropic Caching Docs**: https://docs.anthropic.com/claude/docs/prompt-caching
- **Gemini Caching Guide**: https://ai.google.dev/gemini-api/docs/caching
- **llama.cpp**: https://github.com/ggerganov/llama.cpp

---

**Last Updated**: 2026-02-05
