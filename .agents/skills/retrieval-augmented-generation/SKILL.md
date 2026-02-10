---
name: retrieval-augmented-generation
description: |
  Design and implement RAG systems, covering indexing, retrieval, and generation strategies.
  Use when: building Q&A systems, semantic search, or grounding LLMs on private/proprietary data.
---

# Retrieval-Augmented Generation (RAG)

RAG combines the reasoning capabilities of LLMs with the factual precision of external retrieval systems. It transforms "closed-book" exams into "open-book" ones.

## How to Index Data

The quality of retrieval depends on how data is ingested.

1.  **Chunking**:
    -   *Fixed-Size*: Simple, but splits semantic units (sentences/paragraphs).
    -   *Recursive Character*: Respects separators (`

`, `
`, `.`). **Preferred**.
    -   *Semantic*: Splits based on embedding similarity changes.
2.  **Overlap**: Always include 10-20% overlap between chunks to preserve context at boundaries.
3.  **Embeddings**: Choose models based on domain (e.g., `text-embedding-3-small` for general, `biobert` for medical).
4.  **Metadata**: Attach `source`, `date`, `author` to chunks for pre-filtering.

## How to Retrieve Context

Don't rely solely on basic vector search.

-   **Hybrid Search**: Combine Dense (Vector) + Sparse (BM25/Keyword). Weights: `0.7` Vector / `0.3` Keyword usually works best.
-   **Pre-Filtering**: Use metadata (e.g., `year > 2023`) to narrow the search space before calculating similarity.
-   **Re-Ranking**: Retrieve $N$ (e.g., 50) documents, then use a Cross-Encoder (e.g., Cohere Rerank) to sort the top $K$ (e.g., 5) by true relevance.

## How to Generate Responses

1.  **Context Window**: Use strict templates. Put context *before* the question or in a dedicated system message section.
2.  **Citation**: Instruct model to reference chunk IDs (e.g., `[Doc 1]`) in the response.
3.  **Fallback**: Explicitly instruct: "If the context contains no relevant information, answer 'I don't know'."

> See [Advanced Patterns](references/advanced-patterns.md) for techniques like HyDE and Parent Document Retrieval.

## Common Pitfalls

| Issue | Cause | Fix |
|-------|-------|-----|
| **Hallucination** | Irrelevant context forced into prompt. | Use Re-ranking and "I don't know" instruction. |
| **Lost in the Middle** | Key info buried in long context. | Put most relevant chunks at start/end of context window. |
| **Outdated Info** | Old docs rank higher. | Recency weighting in search or metadata filtering. |

## Examples

### Example: Standard RAG Prompt

**Input:** Query "How do I reset my password?" + 3 retrieved chunks.

**Prompt Template:**
```text
You are a helpful support assistant. Use the following pieces of retrieved context to answer the user's question.
If the answer is not in the context, say "I don't know".

Context:
---
[Doc 1] To reset password, go to settings...
[Doc 2] Passwords must be 8 chars...
---

Question: How do I reset my password?
```

## References

-   [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (Lewis et al.)](https://arxiv.org/abs/2005.11401)
-   [LangChain RAG Documentation](https://python.langchain.com/docs/expression_language/cookbook/retrieval)
-   [Advanced Patterns](references/advanced-patterns.md)
