---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Bellman-Ford算法概述
translated: true
type: note
---

问题：Bellman-Ford 算法是如何工作的？

答案：

Bellman-Ford 算法是一种单源最短路径算法，用于计算加权图中从单个源顶点到所有其他顶点的最短距离。它甚至适用于负边权并能检测负环。

### 主要特点
- 可以处理负权重（与 Dijkstra 算法不同）。
- 检测是否存在负权重环（负权重环会导致最短路径无定义）。
- 时间复杂度：O(V × E)，其中 V 是顶点数，E 是边数。

### 工作原理（分步）

1. **初始化**：
   - 将到源顶点 `source` 的距离设置为 0：`dist[source] = 0`。
   - 将到所有其他顶点的距离设置为无穷大：`dist[v] = ∞` (对于 v ≠ source)。
   - （可选）保留一个前驱数组以重建路径。

2. **松弛阶段**（重复 V-1 次）：
   - 对于图中每条权重为 w 的边 (u, v)：
     - 如果 `dist[v] > dist[u] + w`：
       - 更新 `dist[v] = dist[u] + w`。
       - （可选）更新 `predecessor[v] = u`。
   - 这恰好执行 |V| - 1 次，因为在没有负环的图中，到任何顶点的最短路径最多包含 |V| - 1 条边。

   每次迭代都确保正确计算最多 k 条边的最短路径。

3. **负环检测**：
   - 执行一次额外的松弛遍历（第 V 次迭代）。
   - 如果任何距离仍然可以改进（即，对于某些边，`dist[v] > dist[u] + w`），则存在从源点可达的负环。
   - 如果没有更新发生，则 `dist[]` 中的距离就是真实的最短路径。

### 伪代码

```python
def bellman_ford(graph, source):
    dist = {vertex: float('inf') for vertex in graph.vertices}
    dist[source] = 0

    for _ in range(len(graph.vertices) - 1):
        for u, v, w in graph.edges:  # 每条边 (u → v) 权重为 w
            if dist[u] != float('inf') and dist[v] > dist[u] + w:
                dist[v] = dist[u] + w

    # 检查负环
    for u, v, w in graph.edges:
        if dist[u] != float('inf') and dist[v] > dist[u] + w:
            raise ValueError("Graph contains a negative-weight cycle")

    return dist
```

### 为什么它有效
在没有负环的图中，任意两个顶点之间的最短路径最多包含 V-1 条边。通过对所有边进行 V-1 次松弛，我们保证能找到所有最短路径。额外的遍历能够可靠地检测是否因负环而可能进一步松弛。

### 示例
考虑一个图：
- 顶点：A, B, C
- 边：A→B（权重 4），A→C（权重 2），C→B（权重 -3）

从 A 运行 Bellman-Ford：
- 初始化后：dist[A]=0, dist[B]=∞, dist[C]=∞
- 第一次迭代：dist[B]=4, dist[C]=2
- 第二次迭代：dist[B]=2 + (-3) = -1（松弛 C→B）
- 不再有变化 → 最短距离：A:0, B:-1, C:2

此处没有负环。如果我们添加 B→C 且权重为 -5，则会形成并检测到负环。
