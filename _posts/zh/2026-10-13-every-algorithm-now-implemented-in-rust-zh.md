---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 所有算法现已用Rust实现
translated: true
type: note
---

全部完成 — **你列表中的每个算法现在都已用 Rust 实现**，只需一条命令即可运行。零新增 warnings（剩下的 8 个是 `word2vec`/`uno` 中已存在的 dead code）。

## 用法

```bash
cargo run -- algorithm list              # 所有 42 个算法的目录
cargo run -- algorithm quicksort         # 运行一个
cargo run -- algorithm dijkstra          # 名称忽略大小写和连字符
```

## 构建内容 — `src/algorithms/`（2,814 行，11 个模块）

| 类别 | 实现 |
| --- | --- |
| **搜索** | linear, binary (iterative), BFS (queue + path reconstruct), DFS |
| **排序** | bubble (early-exit), merge, **quick (Lomuto, 10k bench)**, heap (sift-down), tim (natural runs + minrun insertion + pairwise merge), radix (LSD base-256 with sign-bit XOR trick) |
| **图** | Dijkstra (BinaryHeap), Bellman-Ford (+neg-cycle detect), Floyd-Warshall, Kruskal (via Union-Find), Prim, topological sort (Kahn), A\* (grid, Manhattan) |
| **动态规划** | Fibonacci (memo **and** tabulation), 0/1 knapsack (+backtrack), LCS (+recovery), edit distance, matrix-chain (+parenthesization) |
| **加密/哈希** | **SHA-256** (full implementation, passes FIPS `("abc")` test vector), textbook RSA (modpow + extended-gcd inverse), Diffie-Hellman, consistent hashing (BTreeMap ring, shows minimal reshuffling) |
| **树与结构** | traversals, **AVL** (4 rotation cases; 1..=15 sorted insert → height 4, not 15), trie, Union-Find (path halving + union by rank) |
| **分治** | Strassen (7-subproblem, verified == naive), **Karatsuba** (base-10⁴ bignum, 1000 random products verified; **179ms → 55ms** on 4000-digit operands) |
| **机器学习** | batch gradient descent (recovers `y=3x+7`), backprop on XOR (2-2-1 net → `0.012/0.987/0.989/0.010`), k-means, KNN |
| **字符串** | KMP (LPS table), Rabin-Karp (rolling hash + verify), Boyer-Moore/Horspool — all three find the same `[2, 7, 10]` |
| **贪心** | Huffman (50% bit saving vs ASCII), activity selection, fractional knapsack |

## 验证

- **42 个算法**中的每一个都已运行 — 无 panic，输出正确（FIPS hash vector、`kitten→sitting=3`、`LCS="BCBA"`、matrix-chain `15125`、来自 Kruskal 和 Prim 的 MST 权重均为 `11`、karatsuba==schoolbook 等）
- `src/quicksort.rs` 已被新的 `sorting::quick_sort` 替换（你旧的 `algorithm quicksort` 命令仍然有效）
- README 已更新，包含完整目录

更改尚未提交（`src/algorithms/` 处于未跟踪状态）— 如果需要 commit，请说一声。
