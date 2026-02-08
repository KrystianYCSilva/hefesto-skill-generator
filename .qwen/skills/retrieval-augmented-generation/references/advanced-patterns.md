# Advanced RAG Patterns

## Query Transformations

Techniques to improve the user's raw query before retrieval.

-   **HyDE (Hypothetical Document Embeddings)**: LLM generates a *hypothetical* answer. Retrieve documents similar to the *answer*, not the *question*.
-   **Multi-Query**: Break complex questions into sub-questions. Retrieve for each, then synthesize.
-   **Query Expansion**: Add synonyms or related terms to the query (good for BM25).

## Retrieval Optimization

-   **Parent Document Retrieval**: Index small chunks (for better vector match) but retrieve the *parent* (larger chunk/full doc) for the LLM context.
-   **Sentence Window**: Retrieve the matching sentence + $N$ sentences before/after.
-   **MMR (Maximal Marginal Relevance)**: Select documents that are relevant *and* diverse (not just duplicates of the top result).

## Post-Retrieval

-   **Long-Context Reordering**: "Lost in the Middle" mitigation. Reorder retrieved chunks so the most relevant are at the top and bottom of the context window.
