---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 并查集算法入门
translated: true
type: note
---

### 并查集算法简介

**并查集**算法（又称**不相交集合并**或**DSU**）是一种用于管理不相交集合（元素互不重叠的组）的数据结构及操作集合。该算法在处理分组、合并或连通性检查等问题时非常高效，常用于图算法或聚类分析。

核心操作：

- **查找**：确定元素所属的集合（通常通过查找集合的"根节点"或代表元素实现）
- **合并**：将两个集合合并为一个

该算法的优势在于优化技术，如**路径压缩**（在查找过程中扁平化树结构）和**按秩合并/按大小合并**（将较小树合并到较大树以保持结构平衡）。这使得每次操作的摊还时间接近O(1)——对于大型数据集来说极其高效。

#### 核心数据结构

- 数组 `p[]`（父数组）：`p[i]` 指向元素 `i` 的父节点。初始时每个元素都是自己的父节点（`p[i] = i`）
- 可选：`rank[]` 数组用于按秩合并以平衡合并操作

#### 查找操作（含路径压缩）

`find` 函数从元素回溯到其根节点。你提到的那行代码——`if (p[i] != -1) i = p[i]`——是这个过程中的递归或迭代步骤。它沿着父指针一直追溯到根节点（其中 `p[root] == root` 或对于哨兵值 `p[root] == -1`）。

以下是简单的迭代伪代码实现：

```
function find(i):
    if p[i] != -1:  # 不是根节点（或哨兵）
        i = p[i]     # 移动到父节点（这是你提到的代码行！）
        return find(i)  # 递归：继续直到找到根节点
    else:
        return i     # 找到根节点
```

**使用完整路径压缩**（优化后续查找），我们通过将所有节点直接指向根节点来扁平化路径：

```
function find(i):
    if p[i] != i:  # 不是根节点
        p[i] = find(p[i])  # 压缩：将父节点设置为找到的根节点
    return p[i]
```

- `-1` 常被用作根节点的哨兵值（而不是使用 `i` 表示自指向），特别在某些实现中用于区分未初始化或无效节点
- 没有压缩时，重复查找可能使结构变成长链（最坏情况O(n)）。压缩使其几乎扁平化

#### 合并操作

要合并 `x` 和 `y` 的集合：

1. 查找根节点：`rootX = find(x)`，`rootY = find(y)`
2. 如果 `rootX != rootY`，将其中一个连接到另一个（例如按秩合并：将较小秩的树附加到较大秩的树）

伪代码：

```
function union(x, y):
    rootX = find(x)
    rootY = find(y)
    if rootX != rootY:
        if rank[rootX] > rank[rootY]:
            p[rootY] = rootX
        elif rank[rootX] < rank[rootY]:
            p[rootX] = rootY
        else:
            p[rootY] = rootX
            rank[rootX] += 1  # 增加新父节点的秩
```

#### 算法使用指南

并查集非常适合动态连通性问题。以下是带示例的分步指南：

1. **初始化**：
   - 创建大小为 `n`（元素数量）的 `p[]`：`for i in 0 to n-1: p[i] = -1`（或使用 `i` 表示自指向）
   - 可选：`rank[]` 全部设为 0 或 1

2. **基本使用流程**：
   - 检查两个元素是否在同一集合中：`if find(a) == find(b)`
   - 合并：`union(a, b)`
   - 可以按任意顺序处理查询/合并——这是动态的！

3. **示例：检测图中的连通分量**
   假设有5个节点（0-4）和边 (0-1), (1-2), (3-4)

   ```
   // 初始化
   p = [-1, -1, -1, -1, -1]
   rank = [0, 0, 0, 0, 0]

   // 合并边
   union(0, 1)  // 合并0和1，假设 p[0]=-1, p[1]=0
   union(1, 2)  // 将2合并到{0,1}，p[2]=0
   union(3, 4)  // 合并{3,4}，假设 p[3]=-1, p[4]=3

   // 查询：0和2连通吗？find(0)=0, find(2)=0 → 是
   // 2和3连通吗？find(2)=0, find(3)=-1 → 否
   ```

4. **实际应用场景**：
   - **Kruskal最小生成树**：按权重排序边，合并不会形成环的边（如果 `find(u) == find(v)` 则跳过）
   - **社交网络好友关系**：合并好友，查找共同连接
   - **图像分割**：合并颜色相似的相邻像素
   - **无向图中的环检测**：合并端点；如果已在同一集合，则存在环

#### 简单Python实现

```python
class UnionFind:
    def __init__(self, n):
        self.p = [-1] * n
        self.rank = [0] * n

    def find(self, i):
        if self.p[i] != -1 and self.p[i] != i:  # 处理哨兵值 + 自指向
            self.p[i] = self.find(self.p[i])  # 路径压缩
        return self.p[i] if self.p[i] != -1 else i

    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            if self.rank[px] > self.rank[py]:
                self.p[py] = px
            elif self.rank[px] < self.rank[py]:
                self.p[px] = py
            else:
                self.p[py] = px
                self.rank[px] += 1

# 使用示例
uf = UnionFind(5)
uf.union(0, 1)
uf.union(1, 2)
print(uf.find(0) == uf.find(2))  # True
```

这保持了高效性——尝试使用更大的 `n` 来体验其速度！

如需深入了解，请查看 [GeeksforGeeks: Union-Find Algorithm](https://www.geeksforgeeks.org/union-find-algorithm-set-2-union-by-rank-and-path-compression/) 或 [CP-Algorithms: DSU](https://cp-algorithms.com/data_structures/disjoint_set_union.html)。
