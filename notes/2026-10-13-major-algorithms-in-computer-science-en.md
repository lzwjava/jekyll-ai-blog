---
audio: false
generated: true
image: false
lang: en
layout: post
title: Major Algorithms in Computer Science
translated: false
type: note
---

Question: What are the major algorithms in computer science?

Answer:

Here's a categorized overview of the most fundamental and widely-used algorithms:

---

## 🔍 Searching

| Algorithm | Time Complexity | Use Case |
| --- | --- | --- |
| Linear Search | O(n) | Unsorted data |
| **Binary Search** | O(log n) | Sorted arrays |
| BFS (Breadth-First Search) | O(V+E) | Shortest path, graphs |
| DFS (Depth-First Search) | O(V+E) | Cycle detection, trees |

---

## 📊 Sorting

| Algorithm | Best | Worst | Stable? |
| --- | --- | --- | --- |
| Bubble Sort | O(n) | O(n²) | ✅ |
| Merge Sort | O(n log n) | O(n log n) | ✅ |
| **Quick Sort** | O(n log n) | O(n²) | ❌ |
| Heap Sort | O(n log n) | O(n log n) | ❌ |
| Tim Sort | O(n) | O(n log n) | ✅ |
| Radix Sort | O(nk) | O(nk) | ✅ |

---

## 🗺️ Graph Algorithms

- **Dijkstra's** — single-source shortest path (non-negative weights)
- **Bellman-Ford** — shortest path with negative weights
- **Floyd-Warshall** — all-pairs shortest path
- **Kruskal's / Prim's** — Minimum Spanning Tree (MST)
- **Topological Sort** — dependency ordering in DAGs
- **A\*** — heuristic-based pathfinding (used in AI/games)

---

## 🧩 Dynamic Programming

- **Fibonacci** (memoization vs. tabulation)
- **Knapsack Problem** — resource allocation
- **Longest Common Subsequence (LCS)** — diff tools, bioinformatics
- **Edit Distance (Levenshtein)** — spell checkers, NLP
- **Matrix Chain Multiplication**

---

## 🔐 Cryptographic / Hashing

- **MD5 / SHA-256** — data integrity
- **RSA** — public-key encryption
- **Diffie-Hellman** — key exchange
- **Consistent Hashing** — distributed systems

---

## 🌲 Tree & Data Structure Algorithms

- **Tree Traversals** (Inorder, Preorder, Postorder)
- **AVL / Red-Black Tree Rotations** — self-balancing
- **Trie Operations** — autocomplete, prefix search
- **Union-Find (Disjoint Set)** — network connectivity

---

## ⚡ Divide & Conquer

- **Merge Sort**, **Quick Sort**
- **Strassen's Matrix Multiplication** — O(n^2.81) vs naïve O(n³)
- **Karatsuba Algorithm** — fast integer multiplication

---

## 🤖 Machine Learning / AI Algorithms

- **Gradient Descent** — model training optimization
- **Backpropagation** — neural networks
- **K-Means Clustering** — unsupervised learning
- **K-Nearest Neighbors (KNN)** — classification

---

## 📐 String Algorithms

- **KMP (Knuth-Morris-Pratt)** — pattern matching in O(n+m)
- **Rabin-Karp** — rolling hash for string search
- **Boyer-Moore** — fast text search (used in `grep`)

---

## 💡 Greedy Algorithms

- **Huffman Coding** — data compression (ZIP, PNG)
- **Activity Selection Problem**
- **Fractional Knapsack**

---

## Key Algorithmic Paradigms

```
Divide & Conquer  →  Split, solve, merge
Dynamic Programming  →  Overlapping subproblems + memoization
Greedy  →  Locally optimal choice at each step
Backtracking  →  Explore all paths, prune dead ends
Randomized  →  Use randomness to improve average performance
```

---

References:

- [Introduction to Algorithms (CLRS) — MIT Press](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
- [Algorithms — Princeton / Coursera](https://www.coursera.org/learn/algorithms-part1)
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)
- [CP-Algorithms Reference](https://cp-algorithms.com/)
