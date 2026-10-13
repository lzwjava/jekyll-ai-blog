---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 扩展算法库，全部已验证
translated: true
type: note
---

全部完成 — **58 → 80 个算法**，全部通过内置验证。最重的新演示总运行时间：0.28 秒。

## 新增内容（秉承刘汝佳《算法竞赛入门经典》/《训练指南》精神的竞赛经典）

**几何**（`src/algorithms/geometry.rs`）— 从 1 个扩展到 6 个：
- `segment-intersection` — 方向/线段上测试；与 2001 个点的距离采样交叉验证
- `point-in-polygon` — 射线投射法与环绕数法对比，并与手工验证答案核对，包含边界处理
- `closest-pair` — 分治 O(n log n)，与在 79 800 对点上的暴力求解结果完全一致
- `rotating-calipers` — 旋转卡尺法对凸包直径的对踵点扫描，与 O(n²) 结果匹配
- `triangle-centers` — 重心/内心、外心、垂心 + 欧拉线（OG:GH = 1:2）

**图论**（`graph.rs`）— 9 → 12：`euler-path`（Hierholzer 算法，每条边恰好使用一次）、`bridges`（割边/割点，通过删除后重新计数验证）、`two-sat`（蕴含图 + SCC + 拓扑赋值，与 2ⁿ 暴力枚举核对）

**网络流**（新 `flow.rs`）：`max-flow`（Edmonds-Karp；验证流量守恒以及最大流 = 最小割，覆盖全部 16 种割）、`bipartite-matching`（Kuhn 算法与精确暴力枚举对比）

**数论** — 2 → 7：`fast-exponentiation`、`chinese-remainder`、`matrix-exponentiation`（20 次平方算得 fib(10⁶)）、`discrete-log`（BSGS 与不依赖 √p 的全扫描对比）、`miller-rabin`（确定性底数，n < 200 000 时 0 个不匹配，且对 561/2047/3215031751 等强伪素数已验证）

**字符串** — 4 → 7：`manacher`、`aho-corasick`、`suffix-array`（前缀倍增 + Kasai LCP）

**动态规划**：`digit-dp`（B-number 模式，在 N = 100 000 时与扫描验证，然后运行 N = 987 654 321）

**搜索**：`ida-star`（八数码问题；重放其移动序列，并与 BFS 最优深度 30 匹配）

**回溯**（新 `backtracking.rs`）：`n-queens`（与 OEIS A000170 在 n = 10 内一致）、`sudoku`（MRV 求解器，仅用 52 个节点解出）

每个演示都遵循现有风格：独立的 `pub fn`，输出结果 + 独立验证 + 复杂度注释，并在 `mod.rs` 中按类别注册。`README.md` 已更新新的计数和类别列表。