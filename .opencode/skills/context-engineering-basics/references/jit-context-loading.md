# Just-In-Time (JIT) Context Loading

## Overview

JIT context loading defers loading context until it's actually needed, rather than loading everything upfront. This pattern reduces initial token usage, improves latency, and enables handling of contexts that would exceed window limits if loaded entirely.

**Key Principles:**
- **Lazy Evaluation**: Load only when accessed
- **Incremental Expansion**: Start small, grow as needed
- **Smart Prefetching**: Anticipate likely needs
- **Graceful Degradation**: Function with partial context

---

## Lazy Loading Patterns

### 1. Basic Lazy Loader

```python
class LazyContextLoader:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.loaded_chunks = {}
        self.access_log = []

    def get_context(self, query):
        """Load only relevant context for query"""
        # Identify required topics
        required_topics = self._identify_topics(query)

        # Load only unloaded required topics
        context = []
        for topic in required_topics:
            if topic not in self.loaded_chunks:
                chunk = self.kb.get_topic(topic)
                self.loaded_chunks[topic] = chunk
                self.access_log.append({
                    'topic': topic,
                    'timestamp': datetime.now()
                })

            context.append(self.loaded_chunks[topic])

        return "\n\n".join(context)

    def _identify_topics(self, query):
        """Identify topics relevant to query"""
        # Simple keyword-based topic detection
        # In practice, use semantic classification
        topics = []
        query_lower = query.lower()

        if 'authentication' in query_lower or 'login' in query_lower:
            topics.append('auth')
        if 'payment' in query_lower or 'billing' in query_lower:
            topics.append('billing')
        if 'shipping' in query_lower or 'delivery' in query_lower:
            topics.append('shipping')

        return topics if topics else ['general']

# Usage
kb = KnowledgeBase()
loader = LazyContextLoader(kb)

# Query 1: Only loads 'auth' context
context1 = loader.get_context("How do I reset my password?")

# Query 2: Loads 'billing' context, reuses 'auth' if needed
context2 = loader.get_context("What payment methods do you accept?")
```

### 2. Dependency-Aware Lazy Loading

```python
class DependencyAwareLoader:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.loaded = set()
        self.dependencies = {
            'api_usage': ['api_auth', 'api_basics'],
            'advanced_features': ['basic_features', 'setup'],
            'troubleshooting': ['installation', 'configuration']
        }

    def load(self, topic, context=None):
        """Load topic and its dependencies"""
        if context is None:
            context = []

        # Check if already loaded
        if topic in self.loaded:
            return context

        # Load dependencies first
        if topic in self.dependencies:
            for dep in self.dependencies[topic]:
                context = self.load(dep, context)

        # Load the topic itself
        content = self.kb.get_content(topic)
        context.append(content)
        self.loaded.add(topic)

        return context

    def get_context(self, query):
        """Get context with automatic dependency resolution"""
        topic = self._classify_query(query)
        context = self.load(topic)
        return "\n\n".join(context)

    def _classify_query(self, query):
        """Classify query to topic"""
        # Simplified classification
        if 'api' in query.lower():
            return 'api_usage'
        elif 'error' in query.lower() or 'problem' in query.lower():
            return 'troubleshooting'
        else:
            return 'basic_features'
```

---

## Incremental Expansion

### 1. Progressive Context Builder

```python
class ProgressiveContextBuilder:
    def __init__(self, max_tokens=4000):
        self.max_tokens = max_tokens
        self.context_levels = []

    def add_level(self, name, loader, priority=0):
        """Add context level with priority"""
        self.context_levels.append({
            'name': name,
            'loader': loader,
            'priority': priority,
            'loaded': False
        })

    def build(self, query, essential_only=False):
        """Build context progressively"""
        context = []
        token_count = 0

        # Sort by priority
        sorted_levels = sorted(
            self.context_levels,
            key=lambda x: x['priority'],
            reverse=True
        )

        for level in sorted_levels:
            # Load content
            content = level['loader'](query)
            content_tokens = count_tokens(content)

            # Check if we have room
            if token_count + content_tokens <= self.max_tokens:
                context.append(f"[{level['name']}]\n{content}")
                token_count += content_tokens
                level['loaded'] = True
            else:
                if essential_only and level['priority'] < 5:
                    break  # Skip non-essential levels

                # Try to fit partial content
                available_tokens = self.max_tokens - token_count
                if available_tokens > 100:  # Minimum useful size
                    partial = self._truncate_to_tokens(content, available_tokens)
                    context.append(f"[{level['name']} - Partial]\n{partial}")
                    token_count += available_tokens
                break  # Can't fit more

        return "\n\n".join(context)

    def _truncate_to_tokens(self, text, max_tokens):
        """Truncate text to fit token limit"""
        # Simple implementation: truncate by characters
        # In practice, use proper tokenization
        estimated_chars = max_tokens * 4
        return text[:estimated_chars] + "..."

# Usage
builder = ProgressiveContextBuilder(max_tokens=4000)

builder.add_level(
    name='System Prompt',
    loader=lambda q: "You are a helpful assistant.",
    priority=10  # Highest priority
)

builder.add_level(
    name='User Profile',
    loader=lambda q: load_user_profile(current_user),
    priority=8
)

builder.add_level(
    name='Relevant Docs',
    loader=lambda q: search_docs(q, top_k=3),
    priority=6
)

builder.add_level(
    name='Examples',
    loader=lambda q: load_examples(q),
    priority=4
)

context = builder.build("How do I use the API?")
```

### 2. Query-Complexity Adaptive Loading

```python
class AdaptiveContextLoader:
    def __init__(self):
        self.context_strategies = {
            'simple': ['essential'],
            'medium': ['essential', 'recommended'],
            'complex': ['essential', 'recommended', 'supplemental']
        }

    def load_context(self, query):
        """Load context based on query complexity"""
        complexity = self._assess_complexity(query)
        strategy = self.context_strategies.get(complexity, ['essential'])

        context = []
        for level in strategy:
            content = self._load_level(level, query)
            if content:
                context.append(content)

        return "\n\n".join(context)

    def _assess_complexity(self, query):
        """Assess query complexity"""
        # Simple heuristics (in practice, use ML classifier)
        word_count = len(query.split())
        has_multiple_questions = query.count('?') > 1
        has_technical_terms = any(term in query.lower() for term in ['api', 'integration', 'configure'])

        if word_count > 50 or has_multiple_questions:
            return 'complex'
        elif word_count > 20 or has_technical_terms:
            return 'medium'
        else:
            return 'simple'

    def _load_level(self, level, query):
        """Load specific context level"""
        if level == 'essential':
            return self._load_essential(query)
        elif level == 'recommended':
            return self._load_recommended(query)
        elif level == 'supplemental':
            return self._load_supplemental(query)
        return ""

    def _load_essential(self, query):
        """Load essential context only"""
        return "Core documentation for query"

    def _load_recommended(self, query):
        """Load recommended additional context"""
        return "Examples and common patterns"

    def _load_supplemental(self, query):
        """Load supplemental context"""
        return "Advanced topics and edge cases"
```

---

## Smart Prefetching

### 1. Predictive Prefetching

```python
class PredictivePrefetcher:
    def __init__(self):
        self.access_patterns = {}
        self.prefetch_cache = {}

    def record_access(self, topic):
        """Record topic access for pattern learning"""
        if topic not in self.access_patterns:
            self.access_patterns[topic] = {'count': 0, 'follows': {}}

        self.access_patterns[topic]['count'] += 1

    def record_sequence(self, topic_a, topic_b):
        """Record that topic_b was accessed after topic_a"""
        if topic_a not in self.access_patterns:
            self.access_patterns[topic_a] = {'count': 0, 'follows': {}}

        follows = self.access_patterns[topic_a]['follows']
        follows[topic_b] = follows.get(topic_b, 0) + 1

    def prefetch(self, current_topic):
        """Prefetch likely next topics"""
        if current_topic not in self.access_patterns:
            return []

        # Get topics that commonly follow current topic
        follows = self.access_patterns[current_topic]['follows']

        # Sort by frequency
        likely_next = sorted(
            follows.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Prefetch top 3 likely topics
        prefetched = []
        for topic, frequency in likely_next[:3]:
            if topic not in self.prefetch_cache:
                content = self._load_topic(topic)
                self.prefetch_cache[topic] = content
                prefetched.append(topic)

        return prefetched

    def get_or_fetch(self, topic):
        """Get from prefetch cache or fetch"""
        if topic in self.prefetch_cache:
            content = self.prefetch_cache[topic]
            del self.prefetch_cache[topic]  # Remove from cache after use
            return content
        else:
            return self._load_topic(topic)

    def _load_topic(self, topic):
        """Load topic content"""
        return f"Content for {topic}"

# Usage
prefetcher = PredictivePrefetcher()

# Learn pattern: 'auth' often followed by 'api_keys'
prefetcher.record_sequence('auth', 'api_keys')
prefetcher.record_sequence('auth', 'api_keys')
prefetcher.record_sequence('auth', 'permissions')

# Access 'auth' topic
content = prefetcher.get_or_fetch('auth')
prefetcher.record_access('auth')

# Prefetch likely next topics
prefetched = prefetcher.prefetch('auth')
# Prefetches: ['api_keys', 'permissions']
```

### 2. Conversation-Aware Prefetching

```python
class ConversationPrefetcher:
    def __init__(self):
        self.conversation_state = None
        self.prefetched = {}

    def analyze_conversation(self, messages):
        """Analyze conversation to predict needed context"""
        # Extract conversation intent
        last_user_msg = messages[-1]['content'] if messages else ""

        predictions = []

        # Predict based on conversation flow
        if 'getting started' in last_user_msg.lower():
            predictions = ['installation', 'quick_start', 'basic_concepts']
        elif 'error' in last_user_msg.lower():
            predictions = ['troubleshooting', 'error_codes', 'debugging']
        elif 'how do I' in last_user_msg.lower():
            predictions = ['tutorials', 'examples', 'api_reference']

        return predictions

    def prefetch_for_conversation(self, messages):
        """Prefetch context based on conversation"""
        predictions = self.analyze_conversation(messages)

        for topic in predictions:
            if topic not in self.prefetched:
                content = self._load_content(topic)
                self.prefetched[topic] = {
                    'content': content,
                    'prefetched_at': datetime.now()
                }

    def get_context(self, query, conversation):
        """Get context, using prefetched content when available"""
        # Prefetch for conversation
        self.prefetch_for_conversation(conversation)

        # Identify needed topics
        needed_topics = self._identify_topics(query)

        # Build context from prefetched content
        context = []
        for topic in needed_topics:
            if topic in self.prefetched:
                context.append(self.prefetched[topic]['content'])
            else:
                # Fetch on-demand
                content = self._load_content(topic)
                context.append(content)

        return "\n\n".join(context)

    def _load_content(self, topic):
        """Load topic content"""
        return f"[{topic} content]"

    def _identify_topics(self, query):
        """Identify topics from query"""
        return ['relevant_topic']
```

---

## Context Routing

### 1. Query Router

```python
class ContextRouter:
    def __init__(self):
        self.routes = {}
        self.default_route = None

    def register_route(self, pattern, loader):
        """Register context loader for pattern"""
        self.routes[pattern] = loader

    def set_default(self, loader):
        """Set default loader for unmatched queries"""
        self.default_route = loader

    def route(self, query):
        """Route query to appropriate context loader"""
        for pattern, loader in self.routes.items():
            if self._matches_pattern(query, pattern):
                return loader(query)

        # Use default route
        if self.default_route:
            return self.default_route(query)

        return ""

    def _matches_pattern(self, query, pattern):
        """Check if query matches pattern"""
        # Simple keyword matching
        # In practice, use more sophisticated matching
        if isinstance(pattern, str):
            return pattern.lower() in query.lower()
        elif callable(pattern):
            return pattern(query)
        return False

# Usage
router = ContextRouter()

# Register routes
router.register_route(
    pattern='api',
    loader=lambda q: load_api_docs(q)
)

router.register_route(
    pattern='billing',
    loader=lambda q: load_billing_docs(q)
)

router.register_route(
    pattern=lambda q: 'error' in q.lower(),
    loader=lambda q: load_troubleshooting_docs(q)
)

router.set_default(
    loader=lambda q: load_general_docs(q)
)

# Route queries
context1 = router.route("How do I use the API?")  # Routes to API docs
context2 = router.route("Billing question")  # Routes to billing docs
context3 = router.route("General question")  # Routes to default
```

### 2. Multi-Source Router

```python
class MultiSourceRouter:
    def __init__(self):
        self.sources = {}

    def register_source(self, name, source, condition):
        """
        Register context source

        Args:
            name: Source identifier
            source: Callable that loads context
            condition: Callable that checks if source should be used
        """
        self.sources[name] = {
            'loader': source,
            'condition': condition
        }

    def route_and_merge(self, query, max_sources=3):
        """Route to multiple sources and merge results"""
        active_sources = []

        # Evaluate conditions
        for name, source in self.sources.items():
            if source['condition'](query):
                active_sources.append((name, source['loader']))

        # Load from active sources (limit to max_sources)
        contexts = []
        for i, (name, loader) in enumerate(active_sources[:max_sources]):
            try:
                content = loader(query)
                contexts.append(f"[Source: {name}]\n{content}")
            except Exception as e:
                print(f"Error loading from {name}: {e}")

        return "\n\n".join(contexts)

# Usage
router = MultiSourceRouter()

router.register_source(
    name='documentation',
    source=lambda q: search_docs(q),
    condition=lambda q: True  # Always include
)

router.register_source(
    name='code_examples',
    source=lambda q: search_code_examples(q),
    condition=lambda q: 'example' in q.lower() or 'code' in q.lower()
)

router.register_source(
    name='community_answers',
    source=lambda q: search_stackoverflow(q),
    condition=lambda q: 'how' in q.lower() or '?' in q
)

context = router.route_and_merge("How do I authenticate with the API?")
# Loads from documentation + code_examples + community_answers
```

---

## Performance Optimization

### 1. Concurrent Loading

```python
import concurrent.futures

class ConcurrentContextLoader:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers

    def load_contexts(self, context_specs):
        """Load multiple contexts concurrently"""
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all loading tasks
            futures = {
                executor.submit(spec['loader'], spec.get('query', '')): spec['name']
                for spec in context_specs
            }

            # Collect results
            results = {}
            for future in concurrent.futures.as_completed(futures):
                name = futures[future]
                try:
                    content = future.result()
                    results[name] = content
                except Exception as e:
                    print(f"Error loading {name}: {e}")
                    results[name] = ""

        return results

# Usage
loader = ConcurrentContextLoader()

context_specs = [
    {'name': 'docs', 'loader': lambda q: search_docs(q), 'query': query},
    {'name': 'examples', 'loader': lambda q: load_examples(q), 'query': query},
    {'name': 'faq', 'loader': lambda q: search_faq(q), 'query': query}
]

results = loader.load_contexts(context_specs)
# All sources loaded in parallel
```

### 2. Streaming Context

```python
class StreamingContextLoader:
    def __init__(self):
        self.chunks = []

    def stream_context(self, query):
        """Stream context chunks as they become available"""
        # Yield essential context immediately
        yield self._load_essential()

        # Yield additional context as loaded
        for chunk_name in ['examples', 'details', 'advanced']:
            chunk = self._load_chunk(chunk_name, query)
            if chunk:
                yield chunk

    def _load_essential(self):
        """Load essential context (fast)"""
        return "Essential context"

    def _load_chunk(self, chunk_name, query):
        """Load context chunk (may be slow)"""
        # Simulate loading
        import time
        time.sleep(0.1)
        return f"[{chunk_name}] content"

# Usage
loader = StreamingContextLoader()

for chunk in loader.stream_context("How do I start?"):
    print(f"Received chunk: {chunk[:50]}...")
    # Can process/send chunk immediately without waiting for all context
```

---

## Graceful Degradation

### 1. Fallback Levels

```python
class GracefulContextLoader:
    def __init__(self):
        self.fallback_chain = []

    def add_fallback(self, name, loader):
        """Add fallback level"""
        self.fallback_chain.append({
            'name': name,
            'loader': loader
        })

    def load_with_fallbacks(self, query):
        """Load context, falling back on errors"""
        for fallback in self.fallback_chain:
            try:
                context = fallback['loader'](query)
                if context:  # Non-empty context
                    return context
            except Exception as e:
                print(f"Fallback '{fallback['name']}' failed: {e}")
                continue

        # All fallbacks failed
        return "Minimal context: Unable to load full context"

# Usage
loader = GracefulContextLoader()

loader.add_fallback(
    name='full_context',
    loader=lambda q: load_full_knowledge_base(q)
)

loader.add_fallback(
    name='cached_context',
    loader=lambda q: load_from_cache(q)
)

loader.add_fallback(
    name='minimal_context',
    loader=lambda q: load_essential_only(q)
)

context = loader.load_with_fallbacks(query)
# Tries full_context first, falls back to cached, then minimal
```

### 2. Partial Context Handling

```python
class PartialContextHandler:
    def __init__(self, min_context_threshold=0.3):
        self.threshold = min_context_threshold

    def load_with_quality_check(self, query, context_loader):
        """Load context and check quality"""
        context = context_loader(query)

        # Evaluate context quality
        quality = self._evaluate_quality(context, query)

        if quality >= self.threshold:
            return context, quality
        else:
            # Partial context - augment with alternatives
            augmented = self._augment_partial_context(context, query)
            return augmented, quality

    def _evaluate_quality(self, context, query):
        """Evaluate context quality (0-1)"""
        if not context:
            return 0.0

        # Simple heuristic: check keyword coverage
        query_words = set(query.lower().split())
        context_words = set(context.lower().split())

        coverage = len(query_words & context_words) / len(query_words)
        return coverage

    def _augment_partial_context(self, partial_context, query):
        """Augment partial context with fallback information"""
        augmented = partial_context + "\n\n"
        augmented += "[Note: Context may be incomplete. Additional information may be needed.]"
        return augmented
```

---

## Resources

- **Lazy Evaluation Pattern**: https://en.wikipedia.org/wiki/Lazy_evaluation
- **Prefetching Algorithms**: https://en.wikipedia.org/wiki/Prefetching
- **Streaming Patterns**: https://en.wikipedia.org/wiki/Stream_processing

---

**Last Updated**: 2026-02-05
