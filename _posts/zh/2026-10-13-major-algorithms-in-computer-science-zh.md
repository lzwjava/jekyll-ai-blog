---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 计算机科学中的主要算法
translated: true
type: note
---

问题：计算机科学中有哪些主要算法？

答案：

以下是最基础且广泛使用的算法的分类概述：

---

## 🔍 搜索

| 算法 | 时间复杂度 | 应用场景 |
| --- | --- | --- |
| Linear Search | O(n) | 无序数据 |
| **Binary Search** | O(log n) | 有序数组 |
| BFS (Breadth-First Search) | O(V+E) | 最短路径、图 |
| DFS (Depth-First Search) | O(V+E) | 环检测、树 |

---

## 📊 排序

| 算法 | 最优 | 最差 | 稳定? |
| --- | --- | --- | --- |
| Bubble Sort | O(n) | O(n²) | ✅ |
| Merge Sort | O(n log n) | O(n log n) | ✅ |
| **Quick Sort** | O(n log n) | O(n²) | ❌ |
| Heap Sort | O(n log n) | O(n log n) | ❌ |
| Tim Sort | O(n) | O(n log n) | ✅ |
| Radix Sort | O(nk) | O(nk) | ✅ |

---

## 🗺️ 图算法

- **Dijkstra's** — 单源最短路径（非负权重）
- **Bellman-Ford** — 含负权重的最短路径
- **Floyd-Warshall** — 全源最短路径
- **Kruskal's / Prim's** — 最小生成树 (MST)
- **Topological Sort** — DAG（有向无环图）中的依赖排序
- **A\*** — 基于启发式的寻路（用于 AI/游戏）

---

## 🧩 动态规划

- **Fibonacci**（记忆化 vs 表格化）
- **Knapsack Problem** — 资源分配
- **Longest Common Subsequence (LCS)** — diff 工具、生物信息学
- **Edit Distance (Levenshtein)** — 拼写检查、NLP
- **Matrix Chain Multiplication**

---

## 🔐 加密 / 哈希

- **MD5 / SHA-256** — 数据完整性
- **RSA** — 公钥加密
- **Diffie-Hellman** — 密钥交换
- **Consistent Hashing** — 分布式系统

---

## 🌲 树与数据结构算法

- **Tree Traversals**（中序、前序、后序）
- **AVL / Red-Black Tree Rotations** — 自平衡
- **Trie Operations** — 自动完成、前缀搜索
- **Union-Find (Disjoint Set)** — 网络连通性

---

## ⚡ 分治

- **Merge Sort**、**Quick Sort**
- **Strassen's Matrix Multiplication** — O(n^2.81) vs 朴素 O(n³)
- **Karatsuba Algorithm** — 快速整数乘法

---

## 🤖 机器学习 / AI 算法

- **Gradient Descent** — 模型训练优化
- **Backpropagation** — 神经网络
- **K-Means Clustering** — 无监督学习
- **K-Nearest Neighbors (KNN)** — 分类

---

## 📐 字符串算法

- **KMP (Knuth-Morris-Pratt)** — O(n+m) 时间内的模式匹配
- **Rabin-Karp** — 用于字符串搜索的滚动哈希
- **Boyer-Moore** — 快速文本搜索（用于 `grep`）

---

## 💡 贪心算法

- **Huffman Coding** — 数据压缩（ZIP、PNG）
- **Activity Selection Problem**
- **Fractional Knapsack**

---

## 关键算法范式

```
Divide & Conquer  →  分而治之：拆分、求解、合并
Dynamic Programming  →  重叠子问题 + 记忆化
Greedy  →  每一步做局部最优选择
Backtracking  →  探索所有路径，剪枝死路
Randomized  →  利用随机性提升平均性能
```

---

参考资料：

- [Introduction to Algorithms (CLRS) — MIT Press](https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/)
- [Algorithms — Princeton / Coursera](https://www.coursera.org/learn/algorithms-part1)
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)
- [CP-Algorithms Reference](https://cp-algorithms.com/)
