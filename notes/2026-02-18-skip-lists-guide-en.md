---
audio: false
generated: true
image: false
lang: en
layout: post
title: Skip Lists Simplified Guide
translated: false
type: note
---

Question: Can you provide a comprehensive introduction to the Skip List data structure and its algorithm?

Answer:

# Skip List: A Comprehensive Introduction

## Overview

A **Skip List** is a probabilistic data structure that allows for average-case $O(\log n)$ complexity for search, insertion, and deletion operations. It was invented by **William Pugh** in 1989 as a simpler alternative to balanced binary search trees (such as AVL trees or Red-Black trees).

## Core Concept

The fundamental idea behind a Skip List is to maintain multiple layers of linked lists.

- The **bottom layer** is a standard sorted linked list containing all elements.
- **Higher layers** act as "express lanes" that skip over sections of the bottom list, allowing for faster traversal.

Imagine a subway system where some trains stop at every station (bottom layer), while express trains stop only at major hubs (higher layers). To travel quickly, you take the express train as far as possible, then drop down to the local train to reach your specific destination.

## Structure

Each node in a Skip List contains:

1. **Value:** The data stored in the node.
2. **Forward Pointers:** An array of pointers pointing to the next node at various levels.

### Levels

- The level of a node is determined randomly during insertion.
- A node at level $k$ has pointers to the next node at levels $0, 1, ..., k$.
- The maximum level of the entire list is usually determined by the number of elements ($L = \log_{1/p} N$).

## Algorithms

### 1. Search Algorithm

To search for a target value $x$:

1. Start at the head node at the **highest level**.
2. Move **right** along the current level as long as the next node's value is less than $x$.
3. If the next node's value is greater than $x$ or null, move **down** one level.
4. Repeat steps 2 and 3 until you reach level 0.
5. Check the next node at level 0. If it equals $x$, the search is successful.

### 2. Insertion Algorithm

To insert a value $x$:

1. **Search** for the position where $x$ should be inserted, keeping track of the nodes at each level that precede the insertion point (update stack).
2. **Determine Level:** Randomly generate a level $L$ for the new node. This is typically done by flipping a coin (probability $p = 0.5$). If heads, increase level and flip again; if tails, stop.
3. **Create Node:** Allocate a new node with level $L$.
4. **Update Pointers:** For each level from 0 to $L$, update the forward pointers of the predecessor nodes to point to the new node, and set the new node's pointers to the subsequent nodes.

### 3. Deletion Algorithm

To delete a value $x$:

1. **Search** for the node containing $x$, keeping track of predecessor nodes at each level.
2. If found, update the forward pointers of the predecessor nodes at each level to bypass the deleted node.
3. Free the memory of the deleted node.
4. Optionally, decrease the maximum level of the list if the highest levels become empty.

## Complexity Analysis

| Operation | Average Case | Worst Case | Space Complexity |
| :--- | :--- | :--- | :--- |
| **Search** | $O(\log n)$ | $O(n)$ | $O(n)$ |
| **Insert** | $O(\log n)$ | $O(n)$ | $O(n)$ |
| **Delete** | $O(\log n)$ | $O(n)$ | $O(n)$ |

- **Average Case:** Achieved through randomization. The expected number of levels is $\log_{1/p} n$.
- **Worst Case:** Occurs if the random level generation produces a degenerate structure (e.g., all nodes at level 0), effectively becoming a simple linked list. However, this is statistically highly improbable.

## Advantages vs. Balanced Trees

| Feature | Skip List | Balanced BST (AVL/Red-Black) |
| :--- | :--- | :--- |
| **Implementation** | Simpler, easier to debug | Complex, many edge cases |
| **Concurrency** | Easier to implement lock-free | Difficult to implement lock-free |
| **Performance** | Comparable average case | Guaranteed worst-case bounds |
| **Memory** | Slightly higher (multiple pointers) | Lower (fixed pointers per node) |

## Use Cases

- **Databases:** LevelDB and Redis use Skip Lists for in-memory sorted sets.
- **Concurrent Systems:** Java's `ConcurrentSkipListMap` and `ConcurrentSkipListSet`.
- **Approximate Counting:** Used in some probabilistic algorithms.

## Conclusion

Skip Lists provide a robust, efficient, and implementation-friendly alternative to balanced binary search trees. While they rely on probability rather than strict balancing rules, their performance characteristics make them ideal for high-concurrency environments and systems where implementation simplicity is valued.

References:

- [William Pugh's Original Paper](https://dl.acm.org/doi/10.1145/78973.78977)
- [Wikipedia: Skip List](https://en.wikipedia.org/wiki/Skip_list)
