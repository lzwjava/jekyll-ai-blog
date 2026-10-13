---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 竞赛编程核心算法
translated: true
type: note
---

好问题——你目前的目录涵盖了*教科书/课堂*上的那一套，但算法竞赛非常依赖一些你还没有收录的实用主力算法。以下是我按优先级给出的建议：

## 第 1 级 — 几乎每场竞赛都会用到

| 算法 | 为什么需要它 | 状态 |
| --- | --- | --- |
| **Binary search on answer** (parametric search) | 把“寻找最小/最大可行值”转化为 O(log) 次谓词检查 | ❌ |
| **Two pointers / sliding window** | 在 O(n) 内解决子数组和/子数组不同元素问题 | ❌ |
| **Prefix sums & difference arrays** | O(1) 区间和查询，O(1) 区间更新 | ❌ |
| **Segment tree** | 区间查询 + 区间更新——*竞赛*数据结构之王 | ❌ |
| **Fenwick tree (BIT)** | 线段树的更简单替代方案；逆序对计数 | ❌ |
| **Kadane's algorithm** | O(n) 求最大子数组——经典 DP 热身 | ❌ |
| **LIS in O(n log n)** (patience/binary search) | 最长递增子序列、调度 | ❌ |
| **Monotonic stack / queue** | 下一个更大元素、最大直方图、滑动窗口最大值 | ❌ |
| **Coin change DP** | 完全背包变体，经常出现 | ❌ |
| **Bitmask DP (TSP)** | 子集上的 `dp[mask][i]`——经典竞赛编程模式 | ❌ |

## 第 2 级 — 竞赛青睐的图算法

| 算法 | 使用场景 |
| --- | --- |
| **0/1 BFS** (deque) | 0/1 权重最短路，O(V+E)，相对 Dijkstra 更优 |
| **Tarjan SCC** | 强连通分量、2-SAT、缩点图 |
| **Bridges & articulation points** (Tarjan) | 网络中的关键边/关键点 |
| **Binary lifting / LCA** | k 级祖先、树上距离查询 |
| **Tree DP + rerooting** | 树上的路径/依赖问题 |
| **Bipartite matching** (Hopcroft-Karp) | 分配问题、可归约到最大流 |
| **Max flow** (Dinic's) | 最小割、循环流、匹配 |
| **Bipartite coloring check** | O(V+E) 检测偶环（even cycle） |

## 第 3 级 — 数论（在 Codeforces/AtCoder 上出现频率非常高）

- **Sieve of Eratosthenes**（+ 线性筛）——素数枚举
- **Extended GCD & CRT**——你的 `crypto.rs` 里藏着 `modinv`，它值得单独作为一个条目
- **Modular exponentiation + matrix exponentiation**——O(log n) 求解 Fibonacci/线性递推
- **Miller-Rabin primality + Pollard's rho**——大数分解
- **Combinatorics mod M**——带阶乘预处理的 nCr，Lucas 定理
- **Digit DP**——在 O(位数 × 状态数) 内统计满足性质的数字

## 第 4 级 — KMP 之外的字符串算法

- **Z-algorithm**——在文本中查找模式时通常比 KMP 简单
- **Manacher's algorithm**——O(n) 求最长回文子串
- **Aho-Corasick**——多模式匹配（trie + 失败链接）
- **Rolling hash (double)**——子串相等性判断，Rabin-Karp 的推广（你目前只有单哈希）
- **Suffix array + LCP**——进阶内容，但它是经典的“加强版子串搜索”

## 第 5 级 — 几何与杂项

- **Convex hull**（Andrew 单调链）——几何问题的入门题
- **Point orientation / cross product** 基础
- **Backtracking**（N 皇后、子集、数独）
- **Meet-in-the-middle**——n≈40 的子集问题，2^(n/2) 复杂度
- **Sparse table (RMQ)**——O(n log n) 构建后 O(1) 幂等区间查询
- **Coordinate compression + Mo's algorithm**——离线区间查询
- **Top-K / priority-queue greedy**——你已经有堆，但还没有这个模式

---

## 我对下一批内容的建议

如果你想扩展算法目录，我会从**第 1 级中的十个** + **0/1 BFS、Tarjan SCC、sieve、extended GCD、Z-algorithm、convex hull** 开始——也就是 **16 个新增**，它们可以直接嵌入你现有的注册表中：

```bash
cargo run -- algorithm segment-tree
cargo run -- algorithm binary-search-on-answer
cargo run -- algorithm tarjan-scc
...
```

每个都会遵循你目前的风格：自包含的演示程序，带输入/输出打印和复杂度脚注，输出可验证（例如线段树结果与暴力解法结果对比）。

需要我实现第 1 级（10 个算法）、第 1 级 + 第 2 级（18 个），还是我建议的全部 16 个？我还可以在每个演示中加入内置的暴力解法正确性检查，就像 karatsuba 那个一样。
