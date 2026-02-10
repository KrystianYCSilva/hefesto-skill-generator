---
name: processing
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# XML Processing Strategies

## DOM (Document Object Model)
-   **How**: Loads entire XML into memory as a tree.
-   **Pros**: Easy traversal, modification, XPath support.
-   **Cons**: High memory usage. Crashes on large files.

## SAX (Simple API for XML)
-   **How**: Event-based. Reads file sequentially and triggers events (`startElement`, `endElement`).
-   **Pros**: Low memory (stream), fast.
-   **Cons**: Read-only, forward-only, harder code logic.

## StAX (Streaming API for XML)
-   **How**: Pull-parsing. Client requests next event (iterator).
-   **Pros**: Efficient like SAX but easier control flow. Java standard.

## XPath (XML Path Language)
Query language for selecting nodes in an XML document.
-   `/bookstore/book[1]`: First book.
-   `//title[@lang='en']`: All titles with English lang attribute.
-   `book[price>35.00]`: Filter by value.

