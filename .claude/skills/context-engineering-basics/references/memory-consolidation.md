# Memory Consolidation

## Overview

Memory consolidation organizes information into structured memory systems that persist across conversations and sessions. Inspired by cognitive architectures (Soar, ACT-R, CoALA), these patterns enable agents to maintain state, learn from experience, and build knowledge over time.

**Memory Types:**
- **Working Memory**: Current conversation context (short-term, immediate access)
- **Episodic Memory**: Past conversations and events (autobiographical, time-stamped)
- **Semantic Memory**: Facts, knowledge, concepts (timeless, general knowledge)
- **Procedural Memory**: Skills, patterns, learned behaviors (how-to knowledge)

---

## Memory Architectures

### 1. Basic Memory System

Simple three-tier memory architecture.

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any
import json

@dataclass
class MemoryItem:
    content: str
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)
    access_count: int = 0
    importance: float = 0.5

    def to_dict(self):
        return {
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata,
            'access_count': self.access_count,
            'importance': self.importance
        }

class BasicMemorySystem:
    def __init__(self, working_memory_size=10):
        self.working_memory = []
        self.episodic_memory = []
        self.semantic_memory = {}
        self.working_memory_size = working_memory_size

    def add_to_working_memory(self, content, metadata=None):
        """Add to current working memory"""
        item = MemoryItem(
            content=content,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        self.working_memory.append(item)

        # Trigger consolidation if full
        if len(self.working_memory) >= self.working_memory_size:
            self.consolidate()

    def consolidate(self):
        """Move working memory to long-term storage"""
        if not self.working_memory:
            return

        # Create episode from working memory
        episode = {
            'timestamp': datetime.now(),
            'messages': [item.to_dict() for item in self.working_memory],
            'summary': self._summarize_episode(self.working_memory)
        }
        self.episodic_memory.append(episode)

        # Extract facts for semantic memory
        facts = self._extract_facts(self.working_memory)
        for fact in facts:
            key = fact['key']
            if key not in self.semantic_memory:
                self.semantic_memory[key] = []
            self.semantic_memory[key].append({
                'value': fact['value'],
                'source': episode['timestamp'].isoformat(),
                'confidence': fact.get('confidence', 0.8)
            })

        # Clear working memory
        self.working_memory = []

    def _summarize_episode(self, items):
        """Generate episode summary"""
        # Simple concatenation (in practice, use LLM summarization)
        contents = [item.content for item in items]
        return " | ".join(contents[:5])  # First 5 items

    def _extract_facts(self, items):
        """Extract facts from memory items"""
        facts = []
        for item in items:
            # Simple keyword extraction (in practice, use NER/LLM)
            if 'user_name' in item.metadata:
                facts.append({
                    'key': 'user_name',
                    'value': item.metadata['user_name'],
                    'confidence': 1.0
                })
        return facts

    def recall_episodes(self, query, top_k=5):
        """Retrieve relevant past episodes"""
        # Simple recency-based recall (in practice, use semantic search)
        recent_episodes = self.episodic_memory[-top_k:]
        recent_episodes.reverse()
        return recent_episodes

    def recall_facts(self, key):
        """Retrieve semantic facts by key"""
        return self.semantic_memory.get(key, [])

    def get_context(self):
        """Build context from all memory tiers"""
        context = []

        # Add relevant semantic facts
        if self.semantic_memory:
            context.append("[Semantic Memory]")
            for key, values in list(self.semantic_memory.items())[:5]:
                context.append(f"{key}: {values[-1]['value']}")

        # Add recent episodes
        if self.episodic_memory:
            context.append("\n[Recent Episodes]")
            for episode in self.episodic_memory[-3:]:
                context.append(f"{episode['timestamp']}: {episode['summary']}")

        # Add working memory
        if self.working_memory:
            context.append("\n[Current Conversation]")
            for item in self.working_memory:
                context.append(item.content)

        return "\n".join(context)
```

---

### 2. CoALA Framework Integration

Implementing Cognitive Architectures for Language Agents (CoALA).

```python
class CoALAMemory:
    """
    CoALA memory system with specialized memory modules

    Based on: https://arxiv.org/abs/2309.02427
    """

    def __init__(self):
        self.working_memory = WorkingMemory(capacity=10)
        self.episodic_memory = EpisodicMemory()
        self.semantic_memory = SemanticMemory()
        self.procedural_memory = ProceduralMemory()

    def process_input(self, input_data):
        """Process input and update memories"""
        # Add to working memory
        self.working_memory.add(input_data)

        # Extract and store facts
        facts = extract_facts(input_data)
        for fact in facts:
            self.semantic_memory.store(fact)

        # If working memory full, consolidate
        if self.working_memory.is_full():
            self.consolidate_working_memory()

    def consolidate_working_memory(self):
        """Consolidate working memory to long-term storage"""
        # Create episodic memory
        episode = self.working_memory.to_episode()
        self.episodic_memory.store(episode)

        # Extract procedural patterns
        patterns = self.working_memory.extract_patterns()
        for pattern in patterns:
            self.procedural_memory.learn(pattern)

        # Clear working memory
        self.working_memory.clear()

    def retrieve(self, query, memory_type='all'):
        """Retrieve from specified memory type(s)"""
        results = {}

        if memory_type in ['all', 'episodic']:
            results['episodic'] = self.episodic_memory.search(query)

        if memory_type in ['all', 'semantic']:
            results['semantic'] = self.semantic_memory.search(query)

        if memory_type in ['all', 'procedural']:
            results['procedural'] = self.procedural_memory.match(query)

        return results

class WorkingMemory:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.items = []

    def add(self, item):
        self.items.append(item)
        if len(self.items) > self.capacity:
            self.items.pop(0)  # Remove oldest

    def is_full(self):
        return len(self.items) >= self.capacity

    def to_episode(self):
        """Convert working memory to episodic format"""
        return {
            'timestamp': datetime.now(),
            'items': self.items.copy(),
            'summary': summarize(self.items)
        }

    def extract_patterns(self):
        """Extract behavioral patterns"""
        # Placeholder: Identify recurring actions/decisions
        return []

    def clear(self):
        self.items = []

class EpisodicMemory:
    def __init__(self):
        self.episodes = []

    def store(self, episode):
        self.episodes.append(episode)

    def search(self, query, top_k=5):
        """Semantic search over episodes"""
        # Implement semantic search (simplified here)
        return self.episodes[-top_k:]

class SemanticMemory:
    def __init__(self):
        self.facts = {}
        self.vector_store = None  # Would use FAISS/Chroma in practice

    def store(self, fact):
        """Store fact in semantic memory"""
        key = fact.get('key', fact['content'])
        if key not in self.facts:
            self.facts[key] = []
        self.facts[key].append(fact)

    def search(self, query):
        """Search semantic memory"""
        # Implement semantic search
        return list(self.facts.values())[:5]

class ProceduralMemory:
    def __init__(self):
        self.procedures = []

    def learn(self, pattern):
        """Learn a new procedure/pattern"""
        self.procedures.append(pattern)

    def match(self, situation):
        """Find matching procedure for situation"""
        # Pattern matching logic
        return []
```

---

### 3. Decay and Forgetting

Implement realistic memory decay.

```python
import math

class DecayingMemory:
    def __init__(self, decay_rate=0.1):
        self.memories = []
        self.decay_rate = decay_rate

    def add(self, content, importance=0.5):
        """Add memory with initial strength"""
        memory = {
            'content': content,
            'created_at': datetime.now(),
            'last_accessed': datetime.now(),
            'access_count': 0,
            'importance': importance,
            'strength': 1.0  # Initial strength
        }
        self.memories.append(memory)

    def access(self, memory_id):
        """Access memory, updating strength"""
        memory = self.memories[memory_id]

        # Update access info
        memory['last_accessed'] = datetime.now()
        memory['access_count'] += 1

        # Boost strength on access
        memory['strength'] = min(1.0, memory['strength'] + 0.1)

        return memory

    def decay_all(self):
        """Apply time-based decay to all memories"""
        now = datetime.now()

        for memory in self.memories:
            # Time since last access
            time_delta = (now - memory['last_accessed']).total_seconds() / 3600  # hours

            # Exponential decay
            decay = math.exp(-self.decay_rate * time_delta)
            memory['strength'] *= decay

    def prune_weak_memories(self, threshold=0.1):
        """Remove memories below strength threshold"""
        self.memories = [
            m for m in self.memories
            if m['strength'] >= threshold or m['importance'] > 0.8
        ]

    def get_active_memories(self, min_strength=0.3):
        """Get memories above strength threshold"""
        self.decay_all()
        return [
            m for m in self.memories
            if m['strength'] >= min_strength
        ]
```

---

### 4. Hierarchical Memory

Multi-level memory with different granularities.

```python
class HierarchicalMemory:
    def __init__(self):
        self.layers = {
            'detailed': [],      # Fine-grained, recent
            'summarized': [],    # Mid-level summaries
            'abstract': []       # High-level concepts
        }

    def add_detailed(self, content):
        """Add detailed memory"""
        self.layers['detailed'].append({
            'content': content,
            'timestamp': datetime.now()
        })

        # Trigger consolidation if needed
        if len(self.layers['detailed']) >= 20:
            self.consolidate_to_summarized()

    def consolidate_to_summarized(self):
        """Consolidate detailed memories to summaries"""
        # Group detailed memories
        chunk_size = 10
        detailed = self.layers['detailed']

        for i in range(0, len(detailed), chunk_size):
            chunk = detailed[i:i+chunk_size]
            summary = self._summarize_chunk(chunk)

            self.layers['summarized'].append({
                'summary': summary,
                'timestamp': datetime.now(),
                'source_count': len(chunk)
            })

        # Clear detailed layer
        self.layers['detailed'] = []

        # Check if summarized layer needs consolidation
        if len(self.layers['summarized']) >= 10:
            self.consolidate_to_abstract()

    def consolidate_to_abstract(self):
        """Consolidate summaries to abstract concepts"""
        summaries = self.layers['summarized']
        abstract_concept = self._extract_concepts(summaries)

        self.layers['abstract'].append({
            'concept': abstract_concept,
            'timestamp': datetime.now(),
            'source_count': len(summaries)
        })

        # Clear summarized layer
        self.layers['summarized'] = []

    def _summarize_chunk(self, chunk):
        """Summarize chunk of memories"""
        contents = [item['content'] for item in chunk]
        return " | ".join(contents[:3])  # Simplified

    def _extract_concepts(self, summaries):
        """Extract high-level concepts"""
        # Simplified concept extraction
        return "General concept from summaries"

    def get_context(self, detail_level='auto'):
        """Get context at specified detail level"""
        if detail_level == 'auto':
            # Adaptively choose based on available content
            if self.layers['detailed']:
                detail_level = 'detailed'
            elif self.layers['summarized']:
                detail_level = 'summarized'
            else:
                detail_level = 'abstract'

        if detail_level == 'detailed':
            return self.layers['detailed']
        elif detail_level == 'summarized':
            return self.layers['abstract'] + self.layers['summarized'] + self.layers['detailed'][-5:]
        else:  # abstract
            return self.layers['abstract']
```

---

## Consolidation Triggers

### 1. Time-Based Triggers

```python
class TimeBasedConsolidation:
    def __init__(self, interval_seconds=3600):
        self.interval = interval_seconds
        self.last_consolidation = datetime.now()
        self.memory = BasicMemorySystem()

    def should_consolidate(self):
        """Check if enough time has passed"""
        elapsed = (datetime.now() - self.last_consolidation).total_seconds()
        return elapsed >= self.interval

    def update(self):
        """Check and perform consolidation if needed"""
        if self.should_consolidate():
            self.memory.consolidate()
            self.last_consolidation = datetime.now()
```

### 2. Size-Based Triggers

```python
class SizeBasedConsolidation:
    def __init__(self, max_working_size=15):
        self.max_size = max_working_size
        self.memory = BasicMemorySystem()

    def add(self, content):
        """Add to memory, consolidating if size exceeded"""
        self.memory.add_to_working_memory(content)

        if len(self.memory.working_memory) >= self.max_size:
            self.memory.consolidate()
```

### 3. Importance-Based Triggers

```python
class ImportanceBasedConsolidation:
    def __init__(self, importance_threshold=0.7):
        self.threshold = importance_threshold
        self.memory = BasicMemorySystem()

    def add(self, content, importance=0.5):
        """Add to memory with importance score"""
        self.memory.add_to_working_memory(content, metadata={'importance': importance})

        # Consolidate if important information present
        if self.has_important_memories():
            self.memory.consolidate()

    def has_important_memories(self):
        """Check if working memory has important items"""
        for item in self.memory.working_memory:
            if item.metadata.get('importance', 0) >= self.threshold:
                return True
        return False
```

---

## Retrieval Strategies

### 1. Recency-Weighted Retrieval

```python
def retrieve_with_recency_bias(memories, query, top_k=5, recency_weight=0.3):
    """Retrieve memories with recency bias"""
    now = datetime.now()
    scored_memories = []

    for memory in memories:
        # Semantic relevance (simplified)
        relevance = compute_relevance(memory['content'], query)

        # Recency score
        age_hours = (now - memory['timestamp']).total_seconds() / 3600
        recency = math.exp(-0.1 * age_hours)  # Decay over time

        # Combined score
        score = (1 - recency_weight) * relevance + recency_weight * recency

        scored_memories.append({
            'memory': memory,
            'score': score
        })

    # Sort and return top-k
    scored_memories.sort(key=lambda x: x['score'], reverse=True)
    return [item['memory'] for item in scored_memories[:top_k]]
```

### 2. Frequency-Based Retrieval

```python
def retrieve_by_frequency(memories, query, top_k=5, frequency_weight=0.2):
    """Boost frequently accessed memories"""
    scored_memories = []

    for memory in memories:
        # Base relevance
        relevance = compute_relevance(memory['content'], query)

        # Frequency bonus
        access_count = memory.get('access_count', 0)
        frequency_score = math.log(access_count + 1) / 10  # Log scale

        # Combined score
        score = (1 - frequency_weight) * relevance + frequency_weight * frequency_score

        scored_memories.append({
            'memory': memory,
            'score': score
        })

    scored_memories.sort(key=lambda x: x['score'], reverse=True)
    return [item['memory'] for item in scored_memories[:top_k]]
```

---

## Practical Examples

### Example 1: Customer Support Agent

```python
class SupportAgentMemory:
    def __init__(self):
        self.customer_profiles = {}  # Semantic memory: customer facts
        self.interaction_history = []  # Episodic memory: past interactions
        self.current_session = []  # Working memory: current conversation

    def start_session(self, customer_id):
        """Start new customer session"""
        self.current_customer = customer_id
        self.current_session = []

        # Load customer profile from semantic memory
        return self.customer_profiles.get(customer_id, {})

    def add_message(self, role, content):
        """Add message to current session"""
        self.current_session.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now()
        })

    def end_session(self, resolution):
        """End session and consolidate"""
        # Create interaction record
        interaction = {
            'customer_id': self.current_customer,
            'timestamp': datetime.now(),
            'messages': self.current_session,
            'resolution': resolution
        }
        self.interaction_history.append(interaction)

        # Update customer profile
        self._update_customer_profile(interaction)

        # Clear working memory
        self.current_session = []

    def _update_customer_profile(self, interaction):
        """Extract facts from interaction to update profile"""
        customer_id = interaction['customer_id']

        if customer_id not in self.customer_profiles:
            self.customer_profiles[customer_id] = {
                'interaction_count': 0,
                'common_issues': [],
                'preferences': {}
            }

        profile = self.customer_profiles[customer_id]
        profile['interaction_count'] += 1

        # Extract issue type
        issue_type = interaction['resolution'].get('issue_type')
        if issue_type:
            profile['common_issues'].append(issue_type)

    def get_context(self, customer_id):
        """Build context for customer"""
        context = []

        # Customer profile (semantic memory)
        profile = self.customer_profiles.get(customer_id, {})
        if profile:
            context.append(f"Customer profile: {profile['interaction_count']} past interactions")
            if profile['common_issues']:
                context.append(f"Common issues: {', '.join(profile['common_issues'][-3:])}")

        # Recent interactions (episodic memory)
        recent = [i for i in self.interaction_history if i['customer_id'] == customer_id][-3:]
        if recent:
            context.append("\nRecent interactions:")
            for inter in recent:
                context.append(f"- {inter['timestamp']}: {inter['resolution'].get('summary', 'N/A')}")

        # Current session (working memory)
        if self.current_session:
            context.append("\nCurrent conversation:")
            for msg in self.current_session[-5:]:
                context.append(f"{msg['role']}: {msg['content']}")

        return "\n".join(context)
```

---

## Resources

- **CoALA Paper**: https://arxiv.org/abs/2309.02427
- **Soar Architecture**: https://soar.eecs.umich.edu/
- **ACT-R**: http://act-r.psy.cmu.edu/
- **MemGPT**: https://arxiv.org/abs/2310.08560

---

**Last Updated**: 2026-02-05
