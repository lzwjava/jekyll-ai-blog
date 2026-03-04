---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 外星人传奇DP挑战
translated: true
type: note
---

**IOI 2016 "Aliens"** 是 competitive programming 历史上最传奇且备受谈论的问题之一。它是 **International Olympiad in Informatics 2016**（在俄罗斯喀山举办）的 **Day 2 Problem 3**。

### 问题摘要（非常简化的）

给定 **N 个兴趣点**（最多 2000 个）位于一个 **grid** 上（坐标高达 ~10^9，但 N 较小）。  
需要使用 **至多 K 个 axis-aligned squares**（最难子任务中 K 高达 2000）覆盖所有这些点。  
每个 square 可以是 **任意大小** 并放置在任意位置（但有一个特殊属性：两个对角角位于同一条对角线上——实际上是在 taxicab/Chebyshev 距离意义下的 45° 旋转 squares）。

square 的 cost 是 **(side length)²** ——基本上是它覆盖的 **unit cells** 数量。  
目标：**最小化覆盖的总 cells 数量**（所有 squares 的 union），同时覆盖每个点至少一次，使用 ≤ K 个 squares。

这本质上是一个 **minimum cost set cover** 类型的几何问题，被转化为一个非常巧妙的 DP。

### 难度 —— 它难吗？

**是的 —— 极难**，尤其是拿满分。

- 子任务给予部分分数（例如 small K，或宽松约束）→ 许多人得到 30–60 分
- 满分 100 分的解法需要多种非常高级的技术组合：
  - DP on sorted points（coordinate compression / sorting by x+y 或类似排序后）
  - **Convex Hull Trick**（CHT / Li Chao tree 风格）用于优化 DP transitions
  - 著名的 **"Aliens trick"**（也称为 **WQS binary search**、**alien optimization** 或 **convex hull optimization + binary search on slope**）

这个 **"Aliens trick"** 变得 **如此著名**，以至于该优化技术本身现在在 CP 社区中普遍被称为 **"Aliens trick"** 或 **"WQS binary search"** ——即使问题与 aliens 无关。

许多顶尖选手认为它是 IOI 有史以来最难/最具创新性的问题之一。

### 谁解出了它（满分）？

在 IOI 2016，**只有一名选手**在 Aliens 上取得了 **满 100 分**。

那个人是来自中国的 **Qinshi Wang** (王钦石)。

他常被称为“you've never heard of 的 legend”，因为他没有像一些重复获奖者那样公开著名，但独自在赛中完全解决 Aliens 被视为非凡成就。

很少人（即使是金牌得主）在赛中完全解决它。大多数顶尖解法是在数月/数年后，人们研究官方分析时出现的。

如今，这个问题（尤其是 **"Aliens trick"**）被广泛研究——它是 advanced DP optimization + binary search on the dual / Lagrangian relaxation 思想的经典例子。

如果你对该技术感兴趣，许多博客使用这个问题（或更简单的变体，如 cost = (group size)^2 的分组任务）来解释它。