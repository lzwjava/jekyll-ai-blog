---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 用于DP优化的WQS二分搜索
translated: true
type: note
---

**WQS binary search**（也称为 **Aliens trick**、**alien optimization**、**WQS optimization** 或 **Lagrange optimization / convex hull trick variant**）是竞技编程中一种非常强大的技巧，用于优化某些具有额外维度的 **dynamic programming** 问题（通常是计数 / 分组数 / 段数 / 操作数 ≤ K）。

它由传奇的 **IOI 2016 "Aliens"** 问题推广开来（因此得名 "Aliens trick"），但核心思想早在 2012–2013 年左右由 **Wang QinShi (王钦石, WQS)** 在中文训练资料中发明 / 描述。

### Core Idea in One Sentence

当你有一个 DP，需要在使用 **exactly/at most K** 某个东西（分组、合并、操作）时最小化 **cost**，并且最优 cost 作为 K 的函数是 **convex** 的，你可以对 **penalty λ**（一个实数 / 斜率）进行二分搜索，并计算 **(true cost − λ × number_of_items_used)** 的 **unconstrained** 最优值——这会从 DP 中移除 K 维度。

### Typical Problem Shape That It Applies To

你想要解决以下这些问题之一（非常常见的模式）：

- 将 N 个元素分成 **at most K groups** → 最小化所有分组的 **cost(group)** 之和  
  → cost(group) 通常是 convex 的，例如 (size)²、(max−min)²、直径² 等。

- 使用 **at most K operations** 选择 / 合并 → 最小化 penalty

- 用 **≤ K** 个结构覆盖 N 个点 → 最小化总大小 / cost

示例：

- IOI 2016 Aliens（用 ≤ K 个特殊方块覆盖点，最小化覆盖的单元格数）
- 许多 segment DP 问题：将数组分成 ≤ K 个段，每段 cost =（某种 convex 的东西，如 variance / diameter / (max-min)²）
- 任务分组：将 N 个任务分配到 ≤ K 台机器上，cost =（机器上任务数）²
- CF 问题如 "New Year and Handle Change"、"divide into K increasing subsequences" 等。

### Why Convexity Matters

设 f(k) = 使用 **exactly k** 个分组/操作/段的最小 cost。

在许多自然问题中，f(k) 满足：

- f(k) 是 **decreasing** 的（更多分组 → 成本绝不会更差）
- f(k) − f(k+1) 是 **non-increasing** 的（增加一个分组的边际收益变小或相等）

→ 这使得 f(k) **convex**（二阶差分 ≥ 0，或离散凸）

当 f 是 convex 时，函数 g(λ) = min over k of [f(k) + λ · k] 会根据 λ 在不同 k 处取最优，并且随着 λ 增加，最优 k **decreases**（单调！）。

### How the Trick Works (Step by Step)

1. **Rewrite the objective**  
   与其最小化 ≤ K 个分组的 cost，我们针对固定的 **penalty λ**（我们将二分搜索的实数）考虑：  
   min over all possible number of groups m:  
   **real_cost(m) + λ × m**  
   （有时是 real_cost(m) − λ × m ——符号取决于最小化 cost 还是最大化 score）

2. **Compute the DP without the K constraint**  
   现在做 DP，每次“开始新分组 / 为额外项付费”时，向 cost **add λ**。  
   → DP 状态通常变为 **O(N)** 或 **O(N log N)** 而非 **O(N·K)**！

   非常常见的是，这个修改后的 DP 可以用 **convex hull trick / Li Chao tree / divide & conquer optimization**，因为转移变为线性/基于斜率的。

3. **Count how many groups m(λ) were used** 在这个 λ 的最优解中。

4. **Binary search on λ**  
   - If m(λ) > K → 使用了太多分组 → 增加 λ（使开始新分组更昂贵）  
   - If m(λ) < K → 使用太少 → 减少 λ  
   - m(λ) 在 K 附近跳变的交叉点就是我们想要的。

5. **Recover the true answer**  
   二分搜索找到最优 m 围绕 K 的 λ 后：  
   **true minimum cost ≈ DP_value(λ) − λ × K**  
   （或 + λ×K，取决于符号约定）

   因为：  
   DP_value(λ) ≈ real_cost(K) + λ × K  
   → real_cost(K) ≈ DP_value(λ) − λ × K

   重要：由于 convexity，通常存在 λ 范围使得最优 m 完全相同，恢复公式即使固定 m = K 也能给出正确的最小 cost。

### Important Details / Gotchas

- 二分搜索通常在 **real numbers** 上进行 → 设置 lo = -1e9..1e12, hi = 1e9..1e12，运行 ~80–100 次迭代以确保精度。
- 有时恢复略有不同：DP[λ] − λ × actual_m_used，或强制 exactly K 等 —— 取决于 ≤K 或 exactly K，以及更多分组是否总是更好。
- DP 必须能同时计算 **the min modified cost** 和该最优中 **the number of groups used**。
- 如果函数不是严格 convex 或有平坦部分 → 二分搜索可能落在平坦区域 → 但恢复公式通常仍有效。

### Summary Table: When to Suspect Aliens / WQS

| 属性                                | 适合使用 WQS？            |
|-------------------------------------|---------------------------|
| DP has extra dimension ≤ K          | 是                        |
| Cost per group/segment is convex    | 是（关键）                |
| O(N·K) DP is too slow               | 是                        |
| Marginal benefit of +1 group decreases | 是                     |
| You see (size)², (max-min)², etc.   | 强烈提示                  |

这是现代 CP 中最美丽、最令人脑洞大开的优化之一——一旦你内化了“为每个额外分组付费 λ”的直觉，许多看似困难的 DP 问题突然就能在 O(N log N) 或 O(N log² N) 内解决。

如果你想，我可以带你走一个具体的简单示例（例如，将数组分成 ≤ K 个段，最小化每段 (max-min)² 之和）来展示数字。