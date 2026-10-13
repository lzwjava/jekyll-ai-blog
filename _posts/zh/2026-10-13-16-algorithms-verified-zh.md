---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 16个已验证算法
translated: true
type: note
---

所有16个算法均已实现、注册并通过验证。摘要：

## 新模块

| 文件 | 内容 |
|---|---|
| `src/algorithms/arrays.rs` | `two-pointers`, `prefix-sums`, `monotonic-stack` |
| `src/algorithms/numbertheory.rs` | `sieve`, `extended-gcd`（+ `modinv` 演示） |
| `src/algorithms/geometry.rs` | `convex-hull`（Andrew 单调链） |

## 对现有模块的新增

| 文件 | 新增内容 |
|---|---|
| `searching.rs` | `binary-search-on-answer`（船容量谓词，计算其8次检查对比29次线性扫描） |
| `dp.rs` | `kadane`、`lis`（O(n log n) patience 排序 + 重构）、`coin-change`、`bitmask-dp`（TSP） |
| `graph.rs` | `zero-one-bfs`（与现有 `dijkstra_impl` 交叉验证）、`tarjan-scc`（通过互相可达性验证） |
| `trees.rs` | `segment-tree`（懒标记区间加/求和，公开 `SegTree`）、`fenwick-tree`（公开 `Fenwick` + 逆序计数） |
| `strings.rs` | `z-algorithm` |

## 注册表与文档
- `mod.rs`：新增16个 `Algorithm` 条目，3个新类别（**数组技巧**、**数论**、**几何**）——目录现包含 **58** 个演示
- `README.md`：更新了计数和类别列表

## 内置正确性检查（类似 karatsuba）
- `segment-tree`：500次随机区间加/查询操作与普通数组对比
- `bitmask-dp`：TSP结果与所有 8! = 40320 种排列对比
- `kadane`/`lis`：500/300个随机数组与 O(n²) 暴力解法对比
- `two-pointers`、`monotonic-stack`、`prefix-sums`、`fenwick-tree`、`z-algorithm`、`convex-hull`、`sieve`、`extended-gcd`、`zero-one-bfs`、`tarjan-scc`：每个均输出 `true` 以对照其独立参考

测试发现并修复了两个真实bug：线段树无限递归到未覆盖的叶子节点（缺少叶子保护导致索引溢出），以及 Fenwick 逆序计数器将其值域大小设置少了一位（`max` vs `max + 1`）。

所有58个已注册的演示均运行干净，零新增编译器警告。更改尚未提交——如果您希望提交一条 `feat: add 16 competitive-programming algorithms`，请说一声。