---
name: algorithms
description: |
  Documentation file for agent operations and skill usage.
  Use when: you need procedural guidance for agent execution and context management.
---

# Fundamental Algorithms

## Sorting
-   **Quick Sort**: Divide and conquer. Pivot selection is key. $O(n \log n)$ average.
-   **Merge Sort**: Stable sort. Divides array in half recursively. $O(n \log n)$ always.
-   **Bubble/Insertion Sort**: Simple but slow $O(n^2)$. Good for tiny datasets.

## Searching
-   **Binary Search**: Requires sorted array. Check middle, discard half. $O(\log n)$.
-   **DFS (Depth-First Search)**: Explore deep before wide. Uses Stack/Recursion.
-   **BFS (Breadth-First Search)**: Explore neighbors before children. Uses Queue. Shortest path in unweighted graphs.

## Dynamic Programming (DP)
-   **Memoization**: Top-down. Cache results of function calls.
-   **Tabulation**: Bottom-up. Fill table iteratively.
-   **Use Case**: Optimization problems with overlapping subproblems (Knapsack, Fibonacci).

