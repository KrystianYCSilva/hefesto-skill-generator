---
name: data-structures
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Data Structures

## Linear
-   **Stack**: LIFO (Last In, First Out). `push`, `pop`. Recursion, undo mechanisms.
-   **Queue**: FIFO (First In, First Out). `enqueue`, `dequeue`. Task scheduling.
-   **Deque**: Double-ended queue.

## Trees
-   **Binary Search Tree (BST)**: Left child < Node < Right child.
-   **Heap (Priority Queue)**: Binary tree where parent >= children (Max-Heap). Access max in $O(1)$.
-   **Trie (Prefix Tree)**: Optimized for string search/autocomplete.

## Hashing
-   **Hash Function**: Maps data to fixed size integer (hash code).
-   **Collision Resolution**:
    -   *Chaining*: Linked list at each bucket.
    -   *Open Addressing*: Probe next slot.

