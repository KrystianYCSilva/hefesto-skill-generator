# Dynamic Context Discovery

## Overview

Dynamic context discovery enables AI systems to identify and retrieve relevant information from large knowledge bases in real-time. Instead of loading entire datasets, intelligent retrieval strategies select only the most relevant content for each query.

**Key Objectives:**
- Maximize relevance while minimizing token usage
- Balance precision (relevant results) with recall (comprehensive coverage)
- Adapt retrieval strategy based on query characteristics
- Support multi-modal retrieval (text, code, structured data)

---

## Core Retrieval Strategies

### 1. Semantic Search (Vector Similarity)

Semantic search uses embeddings to find content with similar meaning, even when exact keywords don't match.

#### Basic Implementation

```python
import numpy as np
from sentence_transformers import SentenceTransformer

class SemanticSearcher:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.documents = []
        self.embeddings = None

    def index_documents(self, documents):
        """Index documents for semantic search"""
        self.documents = documents
        self.embeddings = self.model.encode(
            documents,
            show_progress_bar=True,
            convert_to_numpy=True
        )

    def search(self, query, top_k=5, threshold=0.0):
        """Search for semantically similar documents"""
        query_embedding = self.model.encode([query], convert_to_numpy=True)

        # Cosine similarity
        similarities = np.dot(self.embeddings, query_embedding.T).flatten()

        # Get top results above threshold
        top_indices = np.argsort(similarities)[::-1][:top_k]
        results = [
            {
                'document': self.documents[idx],
                'score': float(similarities[idx]),
                'index': int(idx)
            }
            for idx in top_indices
            if similarities[idx] >= threshold
        ]

        return results
```

#### Advanced: Using Vector Databases

```python
import chromadb
from chromadb.utils import embedding_functions

class VectorDBSearcher:
    def __init__(self, collection_name='documents'):
        self.client = chromadb.Client()
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name='all-MiniLM-L6-v2'
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )

    def add_documents(self, documents, metadata=None, ids=None):
        """Add documents to vector database"""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]
        if metadata is None:
            metadata = [{} for _ in documents]

        self.collection.add(
            documents=documents,
            metadatas=metadata,
            ids=ids
        )

    def search(self, query, top_k=5, filter_metadata=None):
        """Search with optional metadata filtering"""
        results = self.collection.query(
            query_texts=[query],
            n_results=top_k,
            where=filter_metadata  # e.g., {"category": "technical"}
        )

        return [
            {
                'document': results['documents'][0][i],
                'score': results['distances'][0][i],
                'metadata': results['metadatas'][0][i],
                'id': results['ids'][0][i]
            }
            for i in range(len(results['documents'][0]))
        ]
```

#### Embedding Model Selection

| Model | Dimensions | Speed | Quality | Use Case |
|-------|------------|-------|---------|----------|
| `all-MiniLM-L6-v2` | 384 | Fast | Good | General purpose, low latency |
| `all-mpnet-base-v2` | 768 | Medium | Better | Higher quality, balanced |
| `text-embedding-ada-002` (OpenAI) | 1536 | API | Best | Production, high accuracy |
| `BGE-large-en-v1.5` | 1024 | Medium | Excellent | SOTA open-source |

---

### 2. Keyword Search (BM25)

BM25 (Best Match 25) is a probabilistic keyword-based ranking algorithm, excellent for exact term matching.

#### Implementation

```python
from rank_bm25 import BM25Okapi
import nltk
from nltk.tokenize import word_tokenize

class BM25Searcher:
    def __init__(self):
        self.documents = []
        self.tokenized_docs = []
        self.bm25 = None

    def index_documents(self, documents):
        """Index documents for BM25 search"""
        self.documents = documents
        self.tokenized_docs = [
            word_tokenize(doc.lower())
            for doc in documents
        ]
        self.bm25 = BM25Okapi(self.tokenized_docs)

    def search(self, query, top_k=5):
        """Search using BM25 algorithm"""
        tokenized_query = word_tokenize(query.lower())
        scores = self.bm25.get_scores(tokenized_query)

        # Get top results
        top_indices = np.argsort(scores)[::-1][:top_k]
        results = [
            {
                'document': self.documents[idx],
                'score': float(scores[idx]),
                'index': int(idx)
            }
            for idx in top_indices
        ]

        return results
```

#### When to Use BM25

**Advantages:**
- Fast and deterministic
- No model required (no embedding costs)
- Excellent for exact keyword matches
- Works well with technical terms, codes, IDs

**Disadvantages:**
- Misses semantic similarity
- Sensitive to vocabulary mismatch
- Poor with synonyms or paraphrasing

---

### 3. Hybrid Search (BM25 + Semantic)

Combine keyword and semantic search for best of both worlds.

#### Reciprocal Rank Fusion (RRF)

```python
class HybridSearcher:
    def __init__(self):
        self.semantic_searcher = SemanticSearcher()
        self.bm25_searcher = BM25Searcher()

    def index_documents(self, documents):
        """Index for both search methods"""
        self.semantic_searcher.index_documents(documents)
        self.bm25_searcher.index_documents(documents)

    def search(self, query, top_k=10, alpha=0.5):
        """
        Hybrid search with Reciprocal Rank Fusion

        Args:
            query: Search query
            top_k: Number of results to return
            alpha: Weight for semantic vs BM25 (0=all BM25, 1=all semantic)
        """
        # Get results from both methods
        semantic_results = self.semantic_searcher.search(query, top_k=top_k*2)
        bm25_results = self.bm25_searcher.search(query, top_k=top_k*2)

        # Reciprocal Rank Fusion
        scores = {}
        k = 60  # RRF constant

        # Add semantic scores
        for rank, result in enumerate(semantic_results, start=1):
            doc_id = result['index']
            scores[doc_id] = scores.get(doc_id, 0) + alpha / (k + rank)

        # Add BM25 scores
        for rank, result in enumerate(bm25_results, start=1):
            doc_id = result['index']
            scores[doc_id] = scores.get(doc_id, 0) + (1 - alpha) / (k + rank)

        # Sort by combined score
        ranked_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

        # Return top results
        documents = self.semantic_searcher.documents
        return [
            {
                'document': documents[doc_id],
                'score': scores[doc_id],
                'index': doc_id
            }
            for doc_id in ranked_ids[:top_k]
        ]
```

#### Weighted Combination

```python
def weighted_hybrid_search(query, top_k=5, semantic_weight=0.7):
    """Combine scores with weighted average"""
    semantic_results = semantic_search(query, top_k=top_k*2)
    bm25_results = bm25_search(query, top_k=top_k*2)

    # Normalize scores to [0, 1]
    semantic_scores = normalize_scores([r['score'] for r in semantic_results])
    bm25_scores = normalize_scores([r['score'] for r in bm25_results])

    # Combine scores
    combined_scores = {}
    for i, result in enumerate(semantic_results):
        doc_id = result['index']
        combined_scores[doc_id] = semantic_weight * semantic_scores[i]

    for i, result in enumerate(bm25_results):
        doc_id = result['index']
        combined_scores[doc_id] = combined_scores.get(doc_id, 0) + \
                                   (1 - semantic_weight) * bm25_scores[i]

    # Rank and return
    ranked = sorted(combined_scores.items(), key=lambda x: x[1], reverse=True)
    return [{'document': documents[doc_id], 'score': score}
            for doc_id, score in ranked[:top_k]]

def normalize_scores(scores):
    """Min-max normalization"""
    min_score = min(scores)
    max_score = max(scores)
    if max_score == min_score:
        return [1.0] * len(scores)
    return [(s - min_score) / (max_score - min_score) for s in scores]
```

---

### 4. Multi-Factor Relevance Scoring

Go beyond similarity to consider recency, frequency, user preferences, and context.

#### Comprehensive Relevance Scorer

```python
from datetime import datetime, timedelta
import math

class RelevanceScorer:
    def __init__(self, weights=None):
        self.weights = weights or {
            'semantic': 0.4,
            'keyword': 0.2,
            'recency': 0.15,
            'frequency': 0.10,
            'context_fit': 0.15
        }

    def score(self, document, query, metadata):
        """
        Multi-factor relevance scoring

        Args:
            document: The document text
            query: The search query
            metadata: Dict with 'timestamp', 'access_count', 'conversation_history'
        """
        scores = {
            'semantic': self.semantic_similarity(document, query),
            'keyword': self.keyword_match(document, query),
            'recency': self.time_decay(metadata.get('timestamp')),
            'frequency': self.frequency_score(metadata.get('access_count', 0)),
            'context_fit': self.context_overlap(
                document,
                metadata.get('conversation_history', [])
            )
        }

        # Weighted average
        total_score = sum(
            self.weights[factor] * scores[factor]
            for factor in scores
        )

        return total_score, scores

    def semantic_similarity(self, doc, query):
        """Compute semantic similarity (0-1)"""
        # Use embedding model
        doc_emb = self.embed(doc)
        query_emb = self.embed(query)
        return cosine_similarity(doc_emb, query_emb)

    def keyword_match(self, doc, query):
        """Compute keyword overlap (0-1)"""
        doc_words = set(doc.lower().split())
        query_words = set(query.lower().split())
        overlap = len(doc_words & query_words)
        return overlap / max(len(query_words), 1)

    def time_decay(self, timestamp, half_life_days=7):
        """Exponential time decay (0-1)"""
        if timestamp is None:
            return 0.5  # Neutral if unknown

        age_days = (datetime.now() - timestamp).days
        decay_rate = math.log(2) / half_life_days
        return math.exp(-decay_rate * age_days)

    def frequency_score(self, access_count, max_count=100):
        """Score based on access frequency (0-1)"""
        # Log scale to avoid over-emphasizing very popular docs
        return math.log(access_count + 1) / math.log(max_count + 1)

    def context_overlap(self, doc, conversation_history):
        """Score based on overlap with conversation context (0-1)"""
        if not conversation_history:
            return 0.5  # Neutral if no context

        # Extract entities/topics from conversation
        context_entities = extract_entities(" ".join(conversation_history))
        doc_entities = extract_entities(doc)

        # Compute overlap
        overlap = len(context_entities & doc_entities)
        return overlap / max(len(context_entities), 1)
```

#### Usage Example

```python
scorer = RelevanceScorer(weights={
    'semantic': 0.5,
    'recency': 0.3,
    'frequency': 0.2
})

results = []
for doc in candidate_documents:
    score, breakdown = scorer.score(
        document=doc['text'],
        query=user_query,
        metadata={
            'timestamp': doc['created_at'],
            'access_count': doc['views'],
            'conversation_history': recent_messages
        }
    )
    results.append({
        'document': doc,
        'score': score,
        'score_breakdown': breakdown
    })

# Sort by total score
results.sort(key=lambda x: x['score'], reverse=True)
top_results = results[:5]
```

---

### 5. Query Expansion

Improve retrieval by expanding the query with synonyms, related terms, or reformulations.

#### Synonym Expansion

```python
from nltk.corpus import wordnet

def expand_query_synonyms(query, max_synonyms=3):
    """Expand query with WordNet synonyms"""
    words = query.split()
    expanded_terms = []

    for word in words:
        expanded_terms.append(word)  # Original word

        # Get synonyms from WordNet
        synsets = wordnet.synsets(word)
        synonyms = set()

        for synset in synsets[:max_synonyms]:
            for lemma in synset.lemmas():
                synonym = lemma.name().replace('_', ' ')
                if synonym.lower() != word.lower():
                    synonyms.add(synonym)

        expanded_terms.extend(list(synonyms)[:max_synonyms])

    return " ".join(expanded_terms)

# Example
original = "car repair"
expanded = expand_query_synonyms(original)
# Result: "car auto automobile motorcar repair fix fixing mend"
```

#### LLM-Based Query Expansion

```python
def expand_query_llm(query, llm):
    """Use LLM to generate query variations"""
    prompt = f"""
Given this search query: "{query}"

Generate 3 alternative phrasings that preserve the same intent but use different words.
Format as a comma-separated list.

Alternative queries:"""

    response = llm.generate(prompt, max_tokens=100)
    alternatives = [q.strip() for q in response.split(',')]

    return [query] + alternatives

# Example
original = "how to reset password"
expanded = expand_query_llm(original, llm)
# Result: [
#   "how to reset password",
#   "steps to change my password",
#   "password recovery process",
#   "resetting account credentials"
# ]
```

#### Multi-Query Retrieval

```python
def multi_query_search(original_query, retriever, llm):
    """Search using multiple query reformulations"""
    # Generate query variations
    queries = expand_query_llm(original_query, llm)

    # Search with each query
    all_results = []
    for query in queries:
        results = retriever.search(query, top_k=5)
        all_results.extend(results)

    # Deduplicate and rerank
    unique_docs = {}
    for result in all_results:
        doc_id = result['index']
        if doc_id not in unique_docs:
            unique_docs[doc_id] = result
        else:
            # Average scores if doc appears multiple times
            unique_docs[doc_id]['score'] = (
                unique_docs[doc_id]['score'] + result['score']
            ) / 2

    # Sort by score
    ranked = sorted(
        unique_docs.values(),
        key=lambda x: x['score'],
        reverse=True
    )

    return ranked[:10]
```

---

### 6. Reranking Algorithms

After initial retrieval, rerank results using more sophisticated models.

#### Cross-Encoder Reranking

```python
from sentence_transformers import CrossEncoder

class Reranker:
    def __init__(self, model_name='cross-encoder/ms-marco-MiniLM-L-6-v2'):
        self.model = CrossEncoder(model_name)

    def rerank(self, query, documents, top_k=5):
        """
        Rerank documents using cross-encoder

        Cross-encoders jointly encode query+document for more accurate
        relevance scoring, but are slower than bi-encoders.
        """
        # Create query-document pairs
        pairs = [[query, doc] for doc in documents]

        # Score all pairs
        scores = self.model.predict(pairs)

        # Sort by score
        ranked_indices = np.argsort(scores)[::-1]

        # Return top results
        return [
            {
                'document': documents[idx],
                'score': float(scores[idx]),
                'rank': rank
            }
            for rank, idx in enumerate(ranked_indices[:top_k], start=1)
        ]

# Usage: Two-stage retrieval
# Stage 1: Fast retrieval with bi-encoder (get top 100)
initial_results = semantic_search(query, top_k=100)

# Stage 2: Rerank top results with cross-encoder (get top 5)
reranker = Reranker()
final_results = reranker.rerank(
    query,
    [r['document'] for r in initial_results],
    top_k=5
)
```

#### LLM-Based Reranking

```python
def llm_rerank(query, documents, llm, top_k=5):
    """Use LLM to rerank documents by relevance"""
    # Format documents with indices
    doc_list = "\n".join([
        f"{i+1}. {doc[:200]}..."  # First 200 chars
        for i, doc in enumerate(documents)
    ])

    prompt = f"""
Given this query: "{query}"

Rank the following documents by relevance (most relevant first).
Output only the document numbers in order, comma-separated.

Documents:
{doc_list}

Ranking (e.g., "3,1,5,2,4"):"""

    response = llm.generate(prompt, max_tokens=50)

    # Parse ranking
    try:
        ranking = [int(x.strip()) - 1 for x in response.split(',')]
        reranked = [documents[i] for i in ranking if 0 <= i < len(documents)]
        return reranked[:top_k]
    except:
        # Fallback to original order
        return documents[:top_k]
```

---

### 7. Context-Aware Retrieval

Adapt retrieval based on conversation context and user history.

#### Conversational Retrieval

```python
class ConversationalRetriever:
    def __init__(self, base_retriever):
        self.base_retriever = base_retriever
        self.conversation_context = []

    def add_to_context(self, message):
        """Add message to conversation context"""
        self.conversation_context.append(message)

        # Keep only recent messages
        if len(self.conversation_context) > 10:
            self.conversation_context = self.conversation_context[-10:]

    def retrieve(self, query, top_k=5):
        """Retrieve with conversation context"""
        # Build contextualized query
        context_summary = self._summarize_context()
        contextualized_query = f"{context_summary}\n\nCurrent question: {query}"

        # Retrieve with context
        results = self.base_retriever.search(contextualized_query, top_k=top_k)

        # Filter out previously retrieved docs if needed
        results = self._filter_redundant(results)

        return results

    def _summarize_context(self):
        """Summarize conversation context"""
        if not self.conversation_context:
            return ""

        # Extract key topics/entities
        entities = set()
        for msg in self.conversation_context:
            entities.update(extract_entities(msg))

        return f"Context: discussing {', '.join(list(entities)[:5])}"

    def _filter_redundant(self, results):
        """Remove documents already shown in conversation"""
        shown_docs = set()
        for msg in self.conversation_context:
            # Extract doc IDs from previous results
            # (implementation depends on how you track shown docs)
            pass

        return [r for r in results if r['index'] not in shown_docs]
```

#### User Profile-Based Retrieval

```python
class PersonalizedRetriever:
    def __init__(self, base_retriever):
        self.base_retriever = base_retriever
        self.user_profiles = {}

    def create_profile(self, user_id, preferences=None):
        """Create user profile for personalization"""
        self.user_profiles[user_id] = {
            'preferences': preferences or {},
            'interaction_history': [],
            'favorite_topics': set()
        }

    def update_profile(self, user_id, interaction):
        """Update profile based on user interaction"""
        profile = self.user_profiles.get(user_id)
        if profile:
            profile['interaction_history'].append(interaction)

            # Extract topics from positive interactions
            if interaction.get('rating', 0) >= 4:
                topics = extract_topics(interaction['query'])
                profile['favorite_topics'].update(topics)

    def retrieve(self, query, user_id, top_k=5):
        """Personalized retrieval"""
        profile = self.user_profiles.get(user_id, {})

        # Boost results matching user preferences
        results = self.base_retriever.search(query, top_k=top_k*2)

        # Rescore based on profile
        for result in results:
            doc_topics = extract_topics(result['document'])
            topic_overlap = len(doc_topics & profile.get('favorite_topics', set()))

            # Boost score if topics match user interests
            result['score'] *= (1 + 0.1 * topic_overlap)

        # Re-sort and return top results
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
```

---

## Advanced Patterns

### Pattern 1: Hierarchical Retrieval

Retrieve at multiple granularities (documents → sections → paragraphs).

```python
class HierarchicalRetriever:
    def __init__(self):
        self.document_index = {}  # doc_id -> document
        self.section_index = {}   # section_id -> section
        self.paragraph_index = {} # para_id -> paragraph

    def index(self, documents):
        """Index at multiple levels"""
        for doc_id, doc in enumerate(documents):
            # Index full document
            self.document_index[doc_id] = doc

            # Split into sections
            sections = split_into_sections(doc)
            for sec_id, section in enumerate(sections):
                section_key = f"{doc_id}_{sec_id}"
                self.section_index[section_key] = {
                    'text': section,
                    'doc_id': doc_id,
                    'section_id': sec_id
                }

                # Split into paragraphs
                paragraphs = split_into_paragraphs(section)
                for para_id, para in enumerate(paragraphs):
                    para_key = f"{doc_id}_{sec_id}_{para_id}"
                    self.paragraph_index[para_key] = {
                        'text': para,
                        'doc_id': doc_id,
                        'section_id': sec_id,
                        'para_id': para_id
                    }

    def retrieve(self, query, granularity='adaptive', top_k=5):
        """
        Retrieve at specified granularity

        granularity: 'document', 'section', 'paragraph', or 'adaptive'
        """
        if granularity == 'adaptive':
            # Decide based on query specificity
            if is_specific_query(query):
                granularity = 'paragraph'
            elif is_broad_query(query):
                granularity = 'document'
            else:
                granularity = 'section'

        # Search at appropriate level
        if granularity == 'document':
            return self._search_level(self.document_index, query, top_k)
        elif granularity == 'section':
            return self._search_level(self.section_index, query, top_k)
        else:  # paragraph
            return self._search_level(self.paragraph_index, query, top_k)

    def _search_level(self, index, query, top_k):
        """Search at specific index level"""
        # Implement search logic (semantic, BM25, hybrid)
        pass
```

### Pattern 2: Iterative Retrieval

Retrieve iteratively, expanding based on initial results.

```python
def iterative_retrieval(query, retriever, max_iterations=3):
    """
    Iterative retrieval with query refinement

    1. Initial retrieval
    2. Analyze results to generate refined query
    3. Repeat until sufficient results or max iterations
    """
    all_results = []
    current_query = query
    retrieved_doc_ids = set()

    for iteration in range(max_iterations):
        # Retrieve with current query
        results = retriever.search(current_query, top_k=5)

        # Add new results (avoid duplicates)
        new_results = [
            r for r in results
            if r['index'] not in retrieved_doc_ids
        ]

        all_results.extend(new_results)
        retrieved_doc_ids.update(r['index'] for r in new_results)

        # Check if we have enough high-quality results
        if len(all_results) >= 5 and all_results[0]['score'] > 0.8:
            break

        # Refine query based on results
        current_query = refine_query(query, new_results)

    return all_results

def refine_query(original_query, results):
    """Generate refined query based on initial results"""
    if not results:
        return original_query

    # Extract key terms from top results
    top_docs = [r['document'] for r in results[:3]]
    key_terms = extract_key_terms(top_docs)

    # Combine with original query
    refined = f"{original_query} {' '.join(key_terms[:5])}"
    return refined
```

### Pattern 3: Ensemble Retrieval

Combine multiple retrieval strategies and vote.

```python
class EnsembleRetriever:
    def __init__(self, retrievers):
        """
        Initialize with multiple retriever instances

        retrievers: List of (name, retriever, weight) tuples
        """
        self.retrievers = retrievers

    def retrieve(self, query, top_k=5, aggregation='weighted_vote'):
        """
        Ensemble retrieval with multiple strategies

        aggregation: 'weighted_vote', 'rank_fusion', or 'score_fusion'
        """
        # Get results from all retrievers
        all_results = {}
        for name, retriever, weight in self.retrievers:
            results = retriever.search(query, top_k=top_k*2)
            all_results[name] = (results, weight)

        # Aggregate results
        if aggregation == 'weighted_vote':
            return self._weighted_vote(all_results, top_k)
        elif aggregation == 'rank_fusion':
            return self._rank_fusion(all_results, top_k)
        else:  # score_fusion
            return self._score_fusion(all_results, top_k)

    def _weighted_vote(self, all_results, top_k):
        """Vote based on which documents appear most often (weighted)"""
        votes = {}
        for name, (results, weight) in all_results.items():
            for result in results:
                doc_id = result['index']
                votes[doc_id] = votes.get(doc_id, 0) + weight

        # Sort by votes
        ranked = sorted(votes.items(), key=lambda x: x[1], reverse=True)
        return [{'index': doc_id, 'votes': vote} for doc_id, vote in ranked[:top_k]]

    def _rank_fusion(self, all_results, top_k):
        """Reciprocal Rank Fusion across retrievers"""
        scores = {}
        k = 60

        for name, (results, weight) in all_results.items():
            for rank, result in enumerate(results, start=1):
                doc_id = result['index']
                scores[doc_id] = scores.get(doc_id, 0) + weight / (k + rank)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [{'index': doc_id, 'score': score} for doc_id, score in ranked[:top_k]]

    def _score_fusion(self, all_results, top_k):
        """Normalize and combine scores"""
        # Normalize scores from each retriever
        normalized_results = {}
        for name, (results, weight) in all_results.items():
            scores = [r['score'] for r in results]
            norm_scores = normalize_scores(scores)

            for result, norm_score in zip(results, norm_scores):
                doc_id = result['index']
                normalized_results[doc_id] = normalized_results.get(doc_id, 0) + \
                                              weight * norm_score

        ranked = sorted(normalized_results.items(), key=lambda x: x[1], reverse=True)
        return [{'index': doc_id, 'score': score} for doc_id, score in ranked[:top_k]]
```

---

## Performance Optimization

### 1. Indexing Strategies

```python
# Pre-compute and cache embeddings
class CachedEmbeddingRetriever:
    def __init__(self, cache_path='embeddings.npy'):
        self.cache_path = cache_path
        self.embeddings = None
        self.documents = None

    def index_documents(self, documents, force_reindex=False):
        """Index with caching"""
        # Try to load from cache
        if not force_reindex and os.path.exists(self.cache_path):
            self.embeddings = np.load(self.cache_path)
            self.documents = documents
            print(f"Loaded {len(documents)} embeddings from cache")
            return

        # Compute embeddings
        print(f"Computing embeddings for {len(documents)} documents...")
        self.embeddings = self.model.encode(documents)

        # Save to cache
        np.save(self.cache_path, self.embeddings)
        self.documents = documents
        print(f"Saved embeddings to {self.cache_path}")
```

### 2. Approximate Nearest Neighbor (ANN)

For large-scale retrieval, use ANN algorithms instead of exhaustive search.

```python
import faiss

class FAISSRetriever:
    def __init__(self, dimension=384, index_type='IVF'):
        self.dimension = dimension
        self.index_type = index_type
        self.index = None
        self.documents = None

    def build_index(self, embeddings, documents):
        """Build FAISS index for fast ANN search"""
        self.documents = documents

        if self.index_type == 'IVF':
            # IVF (Inverted File) index - good for large datasets
            n_clusters = int(4 * math.sqrt(len(embeddings)))
            quantizer = faiss.IndexFlatL2(self.dimension)
            self.index = faiss.IndexIVFFlat(quantizer, self.dimension, n_clusters)

            # Train index
            self.index.train(embeddings)
            self.index.add(embeddings)
        else:
            # Flat index - exact search (slower but accurate)
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(embeddings)

    def search(self, query_embedding, top_k=5):
        """Fast ANN search"""
        # Search
        distances, indices = self.index.search(
            query_embedding.reshape(1, -1),
            top_k
        )

        # Return results
        return [
            {
                'document': self.documents[idx],
                'score': 1 / (1 + float(distances[0][i])),  # Convert distance to similarity
                'index': int(idx)
            }
            for i, idx in enumerate(indices[0])
            if idx != -1  # FAISS returns -1 for unfilled slots
        ]
```

### 3. Batch Processing

```python
def batch_retrieve(queries, retriever, batch_size=32):
    """Process multiple queries efficiently"""
    results = []

    for i in range(0, len(queries), batch_size):
        batch = queries[i:i+batch_size]

        # Batch embedding (much faster than one-by-one)
        query_embeddings = retriever.model.encode(batch)

        # Batch search
        for query, embedding in zip(batch, query_embeddings):
            result = retriever.search_by_embedding(embedding)
            results.append(result)

    return results
```

---

## Evaluation Metrics

### 1. Retrieval Quality Metrics

```python
def evaluate_retrieval(retrieved_docs, relevant_docs):
    """
    Compute standard IR metrics

    Args:
        retrieved_docs: List of retrieved document IDs
        relevant_docs: Set of truly relevant document IDs
    """
    retrieved_set = set(retrieved_docs)
    relevant_set = set(relevant_docs)

    # Precision: What fraction of retrieved docs are relevant?
    precision = len(retrieved_set & relevant_set) / len(retrieved_set) if retrieved_set else 0

    # Recall: What fraction of relevant docs were retrieved?
    recall = len(retrieved_set & relevant_set) / len(relevant_set) if relevant_set else 0

    # F1 Score: Harmonic mean of precision and recall
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    # Mean Reciprocal Rank (MRR): Rank of first relevant doc
    mrr = 0
    for rank, doc_id in enumerate(retrieved_docs, start=1):
        if doc_id in relevant_set:
            mrr = 1 / rank
            break

    # Normalized Discounted Cumulative Gain (NDCG)
    dcg = sum([
        1 / math.log2(rank + 1)
        for rank, doc_id in enumerate(retrieved_docs, start=1)
        if doc_id in relevant_set
    ])
    idcg = sum([1 / math.log2(i + 2) for i in range(len(relevant_set))])
    ndcg = dcg / idcg if idcg > 0 else 0

    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'mrr': mrr,
        'ndcg': ndcg
    }
```

### 2. A/B Testing Framework

```python
class RetrievalABTest:
    def __init__(self, variant_a, variant_b):
        self.variant_a = variant_a
        self.variant_b = variant_b
        self.results = {'A': [], 'B': []}

    def run_test(self, test_queries, ground_truth):
        """Run A/B test on retrieval strategies"""
        for query, relevant_docs in test_queries:
            # Get results from both variants
            results_a = self.variant_a.search(query)
            results_b = self.variant_b.search(query)

            # Evaluate both
            metrics_a = evaluate_retrieval(
                [r['index'] for r in results_a],
                relevant_docs
            )
            metrics_b = evaluate_retrieval(
                [r['index'] for r in results_b],
                relevant_docs
            )

            self.results['A'].append(metrics_a)
            self.results['B'].append(metrics_b)

    def report(self):
        """Generate comparison report"""
        metrics = ['precision', 'recall', 'f1', 'mrr', 'ndcg']

        report = {}
        for metric in metrics:
            avg_a = np.mean([r[metric] for r in self.results['A']])
            avg_b = np.mean([r[metric] for r in self.results['B']])
            improvement = (avg_b - avg_a) / avg_a * 100 if avg_a > 0 else 0

            report[metric] = {
                'variant_a': avg_a,
                'variant_b': avg_b,
                'improvement_percent': improvement
            }

        return report
```

---

## Resources

### Tools and Libraries

- **Sentence Transformers**: https://www.sbert.net/
- **Chroma (Vector DB)**: https://www.trychroma.com/
- **FAISS (Meta)**: https://github.com/facebookresearch/faiss
- **Rank-BM25**: https://github.com/dorianbrown/rank_bm25
- **LangChain Retrieval**: https://python.langchain.com/docs/modules/data_connection/

### Research Papers

- **Dense Passage Retrieval**: https://arxiv.org/abs/2004.04906
- **ColBERT**: https://arxiv.org/abs/2004.12832
- **BEIR Benchmark**: https://arxiv.org/abs/2104.08663
- **Hypothetical Document Embeddings (HyDE)**: https://arxiv.org/abs/2212.10496

---

**Last Updated**: 2026-02-05
