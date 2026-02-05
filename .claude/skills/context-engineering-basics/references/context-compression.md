# Context Compression

## Overview

Context compression reduces token count while preserving essential information, enabling efficient use of limited context windows. Effective compression maintains semantic meaning, factual accuracy, and actionable details while eliminating redundancy and noise.

**Compression Targets:**
- Conversation history (multi-turn dialogues)
- Retrieved documents (RAG systems)
- Code context (large codebases)
- User profiles and metadata

**Key Metrics:**
- **Compression Ratio**: `compressed_tokens / original_tokens`
- **Information Retention**: Percentage of key facts preserved
- **Semantic Similarity**: Cosine similarity between original and compressed embeddings
- **Task Performance**: Does compressed context maintain task success rate?

---

## Compression Strategies

### 1. Summarization

Generate concise summaries that capture essential information.

#### Extractive Summarization

Select important sentences from the original text.

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ExtractiveSummarizer:
    def __init__(self, num_sentences=3):
        self.num_sentences = num_sentences

    def summarize(self, text):
        """Extract most important sentences"""
        # Split into sentences
        sentences = self._split_sentences(text)

        if len(sentences) <= self.num_sentences:
            return text  # Already short enough

        # Compute TF-IDF vectors
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(sentences)

        # Compute sentence scores (similarity to document centroid)
        centroid = tfidf_matrix.mean(axis=0)
        scores = cosine_similarity(tfidf_matrix, centroid).flatten()

        # Get top sentences
        top_indices = np.argsort(scores)[-self.num_sentences:]
        top_indices = sorted(top_indices)  # Maintain original order

        summary = " ".join([sentences[i] for i in top_indices])
        return summary

    def _split_sentences(self, text):
        """Simple sentence splitter"""
        import re
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

# Usage
summarizer = ExtractiveSummarizer(num_sentences=3)
original = """
The project is behind schedule due to resource constraints.
We need two additional developers to meet the deadline.
The client has been informed of the delay.
Weekly status meetings will continue every Monday.
Budget approval is pending from the finance team.
"""
summary = summarizer.summarize(original)
# Result: "The project is behind schedule due to resource constraints. We need two additional developers to meet the deadline. Budget approval is pending from the finance team."
```

#### Abstractive Summarization

Generate new sentences that capture the essence.

```python
class AbstractiveSummarizer:
    def __init__(self, llm, style='bullet_points'):
        self.llm = llm
        self.style = style

    def summarize(self, text, max_length=100):
        """Generate abstractive summary"""
        if self.style == 'bullet_points':
            prompt = f"""
Summarize the following text as concise bullet points (max {max_length} words):

{text}

Summary:
"""
        elif self.style == 'single_sentence':
            prompt = f"""
Summarize the following text in a single sentence:

{text}

Summary:
"""
        else:  # paragraph
            prompt = f"""
Summarize the following text concisely (max {max_length} words):

{text}

Summary:
"""

        summary = self.llm.generate(prompt, max_tokens=max_length)
        return summary.strip()

# Usage
summarizer = AbstractiveSummarizer(llm, style='bullet_points')
summary = summarizer.summarize(long_document, max_length=50)
```

#### Progressive Summarization

Summarize at multiple levels of detail.

```python
class ProgressiveSummarizer:
    def __init__(self, llm):
        self.llm = llm

    def summarize_progressive(self, text, levels=3):
        """
        Create multiple summary levels

        Returns dict with keys: 'detailed', 'medium', 'brief'
        """
        summaries = {}

        # Level 1: Detailed summary (50% compression)
        summaries['detailed'] = self._summarize_to_ratio(text, ratio=0.5)

        # Level 2: Medium summary (25% compression)
        summaries['medium'] = self._summarize_to_ratio(
            summaries['detailed'],
            ratio=0.5
        )

        # Level 3: Brief summary (single sentence)
        summaries['brief'] = self._summarize_to_sentence(summaries['medium'])

        return summaries

    def _summarize_to_ratio(self, text, ratio=0.5):
        """Summarize to target compression ratio"""
        current_tokens = count_tokens(text)
        target_tokens = int(current_tokens * ratio)

        prompt = f"""
Summarize the following text to approximately {target_tokens} tokens while preserving all key information:

{text}

Summary:
"""
        return self.llm.generate(prompt, max_tokens=target_tokens * 2)

    def _summarize_to_sentence(self, text):
        """Compress to single sentence"""
        prompt = f"""
Compress the following into a single sentence that captures the essence:

{text}

One sentence summary:
"""
        return self.llm.generate(prompt, max_tokens=50)

# Usage
summarizer = ProgressiveSummarizer(llm)
summaries = summarizer.summarize_progressive(long_text)

# Use appropriate level based on available tokens
if available_tokens > 500:
    context = summaries['detailed']
elif available_tokens > 200:
    context = summaries['medium']
else:
    context = summaries['brief']
```

---

### 2. Entity Extraction

Extract structured information (entities, facts, relationships).

#### Named Entity Recognition (NER)

```python
import spacy

class EntityExtractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text, entity_types=None):
        """
        Extract named entities

        entity_types: List of types to extract (e.g., ['PERSON', 'ORG', 'DATE'])
                      If None, extract all types.
        """
        doc = self.nlp(text)

        entities = {}
        for ent in doc.ents:
            if entity_types is None or ent.label_ in entity_types:
                if ent.label_ not in entities:
                    entities[ent.label_] = []
                entities[ent.label_].append(ent.text)

        # Deduplicate
        for label in entities:
            entities[label] = list(set(entities[label]))

        return entities

    def compress_with_entities(self, text):
        """Compress by extracting entities and key facts"""
        entities = self.extract_entities(text)

        # Format as structured summary
        compressed = []
        for entity_type, entity_list in entities.items():
            compressed.append(f"{entity_type}: {', '.join(entity_list)}")

        return "\n".join(compressed)

# Usage
extractor = EntityExtractor()

original = """
John Smith, CEO of TechCorp, announced yesterday that the company
will acquire DataSystems for $500 million. The deal is expected to
close in Q3 2026. Microsoft and Google were also interested but
TechCorp's offer was superior.
"""

entities = extractor.extract_entities(original)
# {
#   'PERSON': ['John Smith'],
#   'ORG': ['TechCorp', 'DataSystems', 'Microsoft', 'Google'],
#   'MONEY': ['$500 million'],
#   'DATE': ['yesterday', 'Q3 2026']
# }

compressed = extractor.compress_with_entities(original)
# "PERSON: John Smith
#  ORG: TechCorp, DataSystems, Microsoft, Google
#  MONEY: $500 million
#  DATE: yesterday, Q3 2026"
```

#### Relationship Extraction

```python
class RelationshipExtractor:
    def __init__(self, llm):
        self.llm = llm

    def extract_relationships(self, text):
        """Extract subject-predicate-object triples"""
        prompt = f"""
Extract key relationships from the text as (Subject, Predicate, Object) triples.
Format each triple as: Subject | Predicate | Object

Text:
{text}

Triples:
"""

        response = self.llm.generate(prompt, max_tokens=200)

        # Parse triples
        triples = []
        for line in response.strip().split('\n'):
            if '|' in line:
                parts = [p.strip() for p in line.split('|')]
                if len(parts) == 3:
                    triples.append({
                        'subject': parts[0],
                        'predicate': parts[1],
                        'object': parts[2]
                    })

        return triples

    def compress_as_triples(self, text):
        """Compress text as relationship triples"""
        triples = self.extract_relationships(text)

        compressed = "\n".join([
            f"{t['subject']} {t['predicate']} {t['object']}"
            for t in triples
        ])

        return compressed

# Usage
extractor = RelationshipExtractor(llm)

original = """
TechCorp acquired DataSystems for $500M. John Smith is the CEO of TechCorp.
The acquisition will complete in Q3 2026.
"""

triples = extractor.extract_relationships(original)
# [
#   {'subject': 'TechCorp', 'predicate': 'acquired', 'object': 'DataSystems'},
#   {'subject': 'Acquisition', 'predicate': 'cost', 'object': '$500M'},
#   {'subject': 'John Smith', 'predicate': 'is CEO of', 'object': 'TechCorp'},
#   {'subject': 'Acquisition', 'predicate': 'completes in', 'object': 'Q3 2026'}
# ]
```

---

### 3. Redundancy Elimination

Remove duplicate or highly similar information.

#### Deduplication

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Deduplicator:
    def __init__(self, similarity_threshold=0.85):
        self.similarity_threshold = similarity_threshold

    def deduplicate_messages(self, messages):
        """Remove duplicate or highly similar messages"""
        if len(messages) <= 1:
            return messages

        # Vectorize messages
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(messages)

        # Compute pairwise similarities
        similarities = cosine_similarity(tfidf_matrix)

        # Keep only unique messages
        unique_messages = []
        unique_indices = []

        for i, msg in enumerate(messages):
            # Check if similar to any already-kept message
            is_duplicate = False
            for j in unique_indices:
                if similarities[i][j] >= self.similarity_threshold:
                    is_duplicate = True
                    break

            if not is_duplicate:
                unique_messages.append(msg)
                unique_indices.append(i)

        return unique_messages

# Usage
deduplicator = Deduplicator(similarity_threshold=0.85)

messages = [
    "The meeting is scheduled for Monday at 10am",
    "We have a meeting on Monday morning at 10",
    "Budget approval is pending",
    "The Monday 10am meeting is confirmed",
    "Waiting for budget approval from finance"
]

unique = deduplicator.deduplicate_messages(messages)
# Result: [
#   "The meeting is scheduled for Monday at 10am",
#   "Budget approval is pending"
# ]
```

#### Content-Aware Merging

```python
class ContentMerger:
    def __init__(self, llm):
        self.llm = llm

    def merge_similar_content(self, texts):
        """Merge similar texts into consolidated versions"""
        # Group similar texts
        groups = self._group_similar(texts)

        # Merge each group
        merged = []
        for group in groups:
            if len(group) == 1:
                merged.append(group[0])
            else:
                merged_text = self._merge_group(group)
                merged.append(merged_text)

        return merged

    def _group_similar(self, texts, threshold=0.7):
        """Group texts by similarity"""
        # Simple clustering by similarity
        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform(texts)
        similarities = cosine_similarity(tfidf)

        groups = []
        assigned = set()

        for i in range(len(texts)):
            if i in assigned:
                continue

            group = [texts[i]]
            assigned.add(i)

            for j in range(i+1, len(texts)):
                if j not in assigned and similarities[i][j] >= threshold:
                    group.append(texts[j])
                    assigned.add(j)

            groups.append(group)

        return groups

    def _merge_group(self, group):
        """Merge a group of similar texts"""
        combined = "\n".join(group)

        prompt = f"""
The following texts say similar things. Merge them into a single concise version
that preserves all unique information:

{combined}

Merged version:
"""

        merged = self.llm.generate(prompt, max_tokens=150)
        return merged.strip()
```

---

### 4. Conversation Compression

Specialized compression for multi-turn dialogues.

#### Sliding Window with Summarization

```python
class ConversationCompressor:
    def __init__(self, llm, window_size=10, compression_trigger=15):
        self.llm = llm
        self.window_size = window_size
        self.compression_trigger = compression_trigger
        self.messages = []
        self.summary = None

    def add_message(self, role, content):
        """Add message to conversation"""
        self.messages.append({'role': role, 'content': content})

        # Trigger compression if needed
        if len(self.messages) >= self.compression_trigger:
            self.compress()

    def compress(self):
        """Compress old messages into summary"""
        # Determine how many messages to compress
        to_compress_count = len(self.messages) - self.window_size

        if to_compress_count <= 0:
            return  # Nothing to compress

        # Split messages
        to_compress = self.messages[:to_compress_count]
        to_keep = self.messages[to_compress_count:]

        # Create or update summary
        old_summary = self.summary
        new_content_summary = self._summarize_messages(to_compress)

        if old_summary:
            # Merge old summary with new content
            self.summary = self._merge_summaries(old_summary, new_content_summary)
        else:
            self.summary = new_content_summary

        # Update message list
        self.messages = to_keep

    def _summarize_messages(self, messages):
        """Summarize a list of messages"""
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in messages
        ])

        prompt = f"""
Summarize this conversation excerpt, preserving key facts and context:

{conversation_text}

Summary:
"""

        summary = self.llm.generate(prompt, max_tokens=150)
        return summary.strip()

    def _merge_summaries(self, old_summary, new_summary):
        """Merge two summaries"""
        prompt = f"""
Merge these two conversation summaries into one concise summary:

Previous summary:
{old_summary}

Recent conversation:
{new_summary}

Merged summary:
"""

        merged = self.llm.generate(prompt, max_tokens=200)
        return merged.strip()

    def get_context(self):
        """Get current conversation context"""
        context = []

        if self.summary:
            context.append(f"[Previous conversation: {self.summary}]")

        context.extend([
            f"{msg['role']}: {msg['content']}"
            for msg in self.messages
        ])

        return "\n".join(context)

# Usage
compressor = ConversationCompressor(llm, window_size=5, compression_trigger=10)

# Add messages over time
compressor.add_message("user", "What's the weather today?")
compressor.add_message("assistant", "It's sunny and 75°F.")
# ... 10 more messages ...
compressor.add_message("user", "Remind me about the weather")

context = compressor.get_context()
# Result:
# [Previous conversation: User asked about weather (sunny, 75°F), discussed lunch plans, and scheduled a meeting for tomorrow.]
# user: Remind me about the weather
```

#### Turn-Based Compression

```python
class TurnBasedCompressor:
    def __init__(self, llm, keep_recent_turns=3):
        self.llm = llm
        self.keep_recent_turns = keep_recent_turns
        self.turns = []  # Each turn is (user_msg, assistant_msg)

    def add_turn(self, user_message, assistant_message):
        """Add a conversation turn"""
        self.turns.append({
            'user': user_message,
            'assistant': assistant_message
        })

    def get_compressed_context(self):
        """Get compressed conversation context"""
        if len(self.turns) <= self.keep_recent_turns:
            # No compression needed
            return self._format_turns(self.turns)

        # Split into old and recent
        old_turns = self.turns[:-self.keep_recent_turns]
        recent_turns = self.turns[-self.keep_recent_turns:]

        # Summarize old turns
        old_summary = self._summarize_turns(old_turns)

        # Format result
        context = f"[Previous conversation: {old_summary}]\n\n"
        context += self._format_turns(recent_turns)

        return context

    def _summarize_turns(self, turns):
        """Summarize conversation turns"""
        formatted = self._format_turns(turns)

        prompt = f"""
Summarize this conversation, preserving key topics and decisions:

{formatted}

Summary:
"""

        summary = self.llm.generate(prompt, max_tokens=100)
        return summary.strip()

    def _format_turns(self, turns):
        """Format turns as conversation"""
        lines = []
        for turn in turns:
            lines.append(f"User: {turn['user']}")
            lines.append(f"Assistant: {turn['assistant']}")
        return "\n".join(lines)
```

---

### 5. Selective Information Retention

Intelligently choose what to keep and what to discard.

#### Importance Scoring

```python
class ImportanceBasedCompressor:
    def __init__(self, llm):
        self.llm = llm

    def compress_by_importance(self, messages, target_ratio=0.5):
        """Keep only most important messages"""
        # Score each message
        scored_messages = []
        for msg in messages:
            importance = self._score_importance(msg)
            scored_messages.append({
                'message': msg,
                'importance': importance
            })

        # Sort by importance
        scored_messages.sort(key=lambda x: x['importance'], reverse=True)

        # Keep top N to achieve target ratio
        target_count = int(len(messages) * target_ratio)
        important_messages = scored_messages[:target_count]

        # Restore chronological order
        # (assumes messages have timestamps or indices)
        important_messages.sort(key=lambda x: messages.index(x['message']))

        return [item['message'] for item in important_messages]

    def _score_importance(self, message):
        """Score message importance (0-1)"""
        prompt = f"""
Rate the importance of this message on a scale of 0-10:
0 = completely irrelevant/unimportant
10 = critical information that must be preserved

Message: {message}

Importance score (0-10):
"""

        response = self.llm.generate(prompt, max_tokens=5)

        try:
            score = float(response.strip()) / 10.0
            return max(0.0, min(1.0, score))  # Clamp to [0, 1]
        except:
            return 0.5  # Default to medium importance
```

#### Rule-Based Filtering

```python
class RuleBasedCompressor:
    def __init__(self):
        self.rules = []

    def add_rule(self, predicate, action='keep'):
        """
        Add compression rule

        predicate: Function that takes a message and returns True/False
        action: 'keep' or 'discard'
        """
        self.rules.append({'predicate': predicate, 'action': action})

    def compress(self, messages):
        """Apply rules to compress messages"""
        result = []

        for msg in messages:
            should_keep = self._evaluate_rules(msg)
            if should_keep:
                result.append(msg)

        return result

    def _evaluate_rules(self, message):
        """Evaluate all rules for a message"""
        # Default: keep if no rules match
        decision = True

        for rule in self.rules:
            if rule['predicate'](message):
                decision = (rule['action'] == 'keep')
                break  # First matching rule wins

        return decision

# Usage
compressor = RuleBasedCompressor()

# Define rules
compressor.add_rule(
    predicate=lambda msg: 'error' in msg.lower() or 'critical' in msg.lower(),
    action='keep'
)
compressor.add_rule(
    predicate=lambda msg: len(msg) < 10,  # Very short messages
    action='discard'
)
compressor.add_rule(
    predicate=lambda msg: 'TODO' in msg or 'FIXME' in msg,
    action='keep'
)

messages = [
    "Hi",
    "Error: connection failed",
    "Just checking in",
    "TODO: fix the login bug",
    "ok"
]

compressed = compressor.compress(messages)
# Result: ["Error: connection failed", "TODO: fix the login bug"]
```

---

### 6. Code Context Compression

Specialized compression for code and technical content.

#### Function Signature Extraction

```python
import ast

class CodeCompressor:
    def __init__(self):
        pass

    def compress_python_code(self, code, include_docstrings=True):
        """
        Compress Python code to signatures and docstrings

        Preserves:
        - Function/class signatures
        - Docstrings (optional)
        - Important comments

        Removes:
        - Function bodies
        - Implementation details
        """
        try:
            tree = ast.parse(code)
        except SyntaxError:
            return code  # Return original if can't parse

        compressed_lines = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Extract function signature
                args = [arg.arg for arg in node.args.args]
                signature = f"def {node.name}({', '.join(args)}):"
                compressed_lines.append(signature)

                # Extract docstring if present
                if include_docstrings and ast.get_docstring(node):
                    docstring = ast.get_docstring(node)
                    compressed_lines.append(f'    """{docstring}"""')

                compressed_lines.append("    ...")  # Placeholder for body
                compressed_lines.append("")

            elif isinstance(node, ast.ClassDef):
                # Extract class definition
                compressed_lines.append(f"class {node.name}:")

                if include_docstrings and ast.get_docstring(node):
                    docstring = ast.get_docstring(node)
                    compressed_lines.append(f'    """{docstring}"""')

                compressed_lines.append("    ...")
                compressed_lines.append("")

        return "\n".join(compressed_lines)

# Usage
original_code = """
class DataProcessor:
    '''Processes data from various sources'''

    def __init__(self, source):
        self.source = source
        self.cache = {}

    def process(self, data):
        '''Process input data and return results'''
        if data in self.cache:
            return self.cache[data]

        result = self._transform(data)
        self.cache[data] = result
        return result

    def _transform(self, data):
        # Complex transformation logic
        transformed = data.upper()
        return transformed
"""

compressor = CodeCompressor()
compressed = compressor.compress_python_code(original_code)
# Result:
# class DataProcessor:
#     """Processes data from various sources"""
#     ...
#
# def __init__(self, source):
#     ...
#
# def process(self, data):
#     """Process input data and return results"""
#     ...
#
# def _transform(self, data):
#     ...
```

#### Dependency Graph Compression

```python
class DependencyGraphCompressor:
    def __init__(self):
        pass

    def compress_codebase(self, files, entry_point):
        """
        Compress codebase to dependency graph + entry point context

        Args:
            files: Dict of {filename: code_content}
            entry_point: Main file to analyze
        """
        # Build dependency graph
        dependencies = self._extract_dependencies(files)

        # Find all files reachable from entry point
        reachable = self._find_reachable(entry_point, dependencies)

        # Compress only reachable files
        compressed = {}
        for filename in reachable:
            if filename in files:
                compressed[filename] = self._compress_file(files[filename])

        return compressed

    def _extract_dependencies(self, files):
        """Extract import dependencies"""
        dependencies = {}

        for filename, code in files.items():
            imports = self._find_imports(code)
            dependencies[filename] = imports

        return dependencies

    def _find_imports(self, code):
        """Find all imports in code"""
        imports = []

        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
        except:
            pass

        return imports

    def _find_reachable(self, start, graph):
        """Find all nodes reachable from start"""
        reachable = set()
        to_visit = [start]

        while to_visit:
            current = to_visit.pop()
            if current in reachable:
                continue

            reachable.add(current)

            # Add dependencies
            if current in graph:
                to_visit.extend(graph[current])

        return reachable

    def _compress_file(self, code):
        """Compress individual file"""
        compressor = CodeCompressor()
        return compressor.compress_python_code(code)
```

---

## Compression Quality Metrics

### 1. Information Retention

```python
def evaluate_compression_quality(original, compressed, llm):
    """
    Evaluate how well compression preserves information

    Returns metrics: retention_score, semantic_similarity, fact_preservation
    """
    # Extract facts from both
    original_facts = extract_facts(original, llm)
    compressed_facts = extract_facts(compressed, llm)

    # Fact preservation rate
    preserved_facts = set(original_facts) & set(compressed_facts)
    fact_preservation = len(preserved_facts) / len(original_facts) if original_facts else 0

    # Semantic similarity
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')

    orig_embedding = model.encode([original])
    comp_embedding = model.encode([compressed])

    semantic_similarity = cosine_similarity(orig_embedding, comp_embedding)[0][0]

    # Compression ratio
    compression_ratio = count_tokens(compressed) / count_tokens(original)

    # Overall retention score (balanced metric)
    retention_score = (fact_preservation + semantic_similarity) / 2

    return {
        'retention_score': retention_score,
        'fact_preservation': fact_preservation,
        'semantic_similarity': semantic_similarity,
        'compression_ratio': compression_ratio
    }

def extract_facts(text, llm):
    """Extract factual statements from text"""
    prompt = f"""
Extract all factual statements from the text as a numbered list.
Include only objective facts, not opinions or filler.

Text:
{text}

Facts:
"""

    response = llm.generate(prompt, max_tokens=300)

    # Parse facts
    facts = []
    for line in response.strip().split('\n'):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-')):
            # Remove numbering
            fact = line.lstrip('0123456789.-) ').strip()
            if fact:
                facts.append(fact)

    return facts
```

### 2. Task Performance Testing

```python
def test_compression_task_performance(original_context, compressed_context, test_queries, llm):
    """
    Test if compressed context maintains task performance

    Returns: accuracy_with_original, accuracy_with_compressed, degradation_percent
    """
    results_original = []
    results_compressed = []

    for query, expected_answer in test_queries:
        # Test with original context
        answer_orig = llm.generate(
            f"Context: {original_context}\n\nQuestion: {query}\n\nAnswer:",
            max_tokens=100
        )
        correct_orig = evaluate_answer(answer_orig, expected_answer)
        results_original.append(correct_orig)

        # Test with compressed context
        answer_comp = llm.generate(
            f"Context: {compressed_context}\n\nQuestion: {query}\n\nAnswer:",
            max_tokens=100
        )
        correct_comp = evaluate_answer(answer_comp, expected_answer)
        results_compressed.append(correct_comp)

    accuracy_orig = sum(results_original) / len(results_original)
    accuracy_comp = sum(results_compressed) / len(results_compressed)
    degradation = (accuracy_orig - accuracy_comp) / accuracy_orig * 100 if accuracy_orig > 0 else 0

    return {
        'accuracy_original': accuracy_orig,
        'accuracy_compressed': accuracy_comp,
        'degradation_percent': degradation
    }

def evaluate_answer(answer, expected):
    """Simple answer evaluation (can be more sophisticated)"""
    # Simple substring matching
    answer_lower = answer.lower()
    expected_lower = expected.lower()

    return expected_lower in answer_lower or answer_lower in expected_lower
```

---

## Best Practices

### 1. Adaptive Compression

Choose compression strategy based on content type and constraints.

```python
class AdaptiveCompressor:
    def __init__(self, llm):
        self.llm = llm
        self.strategies = {
            'conversation': ConversationCompressor(llm),
            'code': CodeCompressor(),
            'document': AbstractiveSummarizer(llm),
            'entity_rich': EntityExtractor()
        }

    def compress(self, text, target_tokens=None, content_type='auto'):
        """
        Adaptively compress based on content and constraints

        Args:
            text: Text to compress
            target_tokens: Target token count (None = auto)
            content_type: 'auto', 'conversation', 'code', 'document', 'entity_rich'
        """
        # Detect content type if auto
        if content_type == 'auto':
            content_type = self._detect_content_type(text)

        # Calculate target ratio if target_tokens specified
        if target_tokens:
            current_tokens = count_tokens(text)
            if current_tokens <= target_tokens:
                return text  # Already small enough

            target_ratio = target_tokens / current_tokens
        else:
            target_ratio = 0.5  # Default 50% compression

        # Apply appropriate strategy
        strategy = self.strategies.get(content_type)
        if not strategy:
            strategy = self.strategies['document']  # Default

        if hasattr(strategy, 'compress'):
            return strategy.compress(text, ratio=target_ratio)
        elif hasattr(strategy, 'summarize'):
            max_length = int(count_tokens(text) * target_ratio * 4)  # Rough word estimate
            return strategy.summarize(text, max_length=max_length)
        else:
            return text

    def _detect_content_type(self, text):
        """Detect content type heuristically"""
        # Check for code markers
        code_markers = ['def ', 'class ', 'function ', 'import ', '# ', '//', '/*']
        if any(marker in text for marker in code_markers):
            return 'code'

        # Check for conversation markers
        conversation_markers = ['User:', 'Assistant:', 'Human:', 'AI:']
        if any(marker in text for marker in conversation_markers):
            return 'conversation'

        # Check entity density
        extractor = EntityExtractor()
        entities = extractor.extract_entities(text)
        total_entities = sum(len(v) for v in entities.values())
        entity_density = total_entities / len(text.split()) if text.split() else 0

        if entity_density > 0.1:  # High entity density
            return 'entity_rich'

        return 'document'  # Default
```

### 2. Compression Pipeline

Chain multiple compression techniques.

```python
class CompressionPipeline:
    def __init__(self):
        self.stages = []

    def add_stage(self, name, compressor, condition=None):
        """
        Add compression stage

        Args:
            name: Stage name
            compressor: Callable that takes text and returns compressed text
            condition: Optional callable that takes text and returns bool
                       (whether to apply this stage)
        """
        self.stages.append({
            'name': name,
            'compressor': compressor,
            'condition': condition or (lambda x: True)
        })

    def compress(self, text, verbose=False):
        """Apply compression pipeline"""
        current = text

        if verbose:
            print(f"Initial: {count_tokens(current)} tokens")

        for stage in self.stages:
            if stage['condition'](current):
                current = stage['compressor'](current)

                if verbose:
                    print(f"After {stage['name']}: {count_tokens(current)} tokens")

        return current

# Usage
pipeline = CompressionPipeline()

# Stage 1: Remove duplicates
deduplicator = Deduplicator()
pipeline.add_stage(
    name='deduplication',
    compressor=lambda text: '\n'.join(deduplicator.deduplicate_messages(text.split('\n')))
)

# Stage 2: Extract entities if text is entity-rich
entity_extractor = EntityExtractor()
pipeline.add_stage(
    name='entity_extraction',
    compressor=entity_extractor.compress_with_entities,
    condition=lambda text: count_tokens(text) > 1000  # Only for large texts
)

# Stage 3: Summarize if still too large
summarizer = AbstractiveSummarizer(llm)
pipeline.add_stage(
    name='summarization',
    compressor=lambda text: summarizer.summarize(text, max_length=200),
    condition=lambda text: count_tokens(text) > 500
)

compressed = pipeline.compress(long_text, verbose=True)
```

---

## Resources

### Libraries and Tools

- **spaCy**: https://spacy.io/
- **NLTK**: https://www.nltk.org/
- **Gensim (Summarization)**: https://radimrehurek.com/gensim/
- **Sumy**: https://github.com/miso-belica/sumy
- **Transformers (Summarization)**: https://huggingface.co/models?pipeline_tag=summarization

### Research Papers

- **BART for Abstractive Summarization**: https://arxiv.org/abs/1910.13461
- **Pegasus**: https://arxiv.org/abs/1912.08777
- **LongT5**: https://arxiv.org/abs/2112.07916
- **Compressive Transformers**: https://arxiv.org/abs/1911.05507

---

**Last Updated**: 2026-02-05
