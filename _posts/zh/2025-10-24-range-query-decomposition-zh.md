---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 区间查询的平方根分解
translated: true
type: note
---

### 平方根分块

平方根分块（常简称为√-分解）是计算机科学和竞赛编程中用于优化大型数组或数据结构上区间查询与更新的技术。当需要高效回答"查找子数组元素之和/最大值/最小值"这类查询时特别有用，无需依赖线段树或树状数组等实现更复杂的重型工具。

#### 为何使用？
- **时间复杂度权衡**：对于大小为 \\( n \\) 的数组，朴素区间查询每次耗时 \\( O(n) \\)。平方根分块将每次查询和更新降至 \\( O(\sqrt{n}) \\)，对于 \\( n \\) 达到 \\( 10^5 \\) 或 \\( 10^6 \\) 的许多问题是不错的平衡点。
- **实现简单**：相比高级数据结构更易编写和调试。
- **应用场景**：常见于区间求和查询、区间最小值查询（RMQ）或滑动窗口频率统计等问题。

#### 实现原理
1. **分块处理**：将数组分割为大小为 \\( \sqrt{n} \\)（向下取整）的块。若 \\( n = 100 \\)，则块大小 \\( b = 10 \\)，共10个块。
   - 每个块存储预计算信息（例如针对求和查询存储块内元素总和）。

2. **区间查询 [L, R]**：
   - **完整块**：对完全位于 [L, R] 内的整块，直接获取预计算值，每块耗时 \\( O(1) \\)。最多涉及 \\( O(\sqrt{n}) \\) 个整块。
   - **边缘块**：对左右两侧的不完整块，手动遍历单个元素，总耗时 \\( O(\sqrt{n}) \\)（因为每个边缘块大小不超过 \\( \sqrt{n} \\)）。
   - 总计：\\( O(\sqrt{n}) \\)。

3. **更新操作**：当更新元素时，以 \\( O(\sqrt{n}) \\) 时间重建所在块的预计算值（通过重新计算块内总和）。

#### 简单示例：区间求和查询
设数组 `A = [1, 3, 2, 4, 5]`，\\( n=5 \\)，则块大小 \\( b = \sqrt{5} \approx 2 \\)。分块结果：
- 块0: [1, 3] → 总和 = 4
- 块1: [2, 4] → 总和 = 6
- 块2: [5] → 总和 = 5（末尾块可能更小）

查询索引1到4的和（0基索引：元素3,2,4,5）：
- 左侧边缘：索引1（位于块0）→ 加3
- 完整块1：加6
- 右侧边缘：索引4（位于块2）→ 加5
- 总计：3 + 6 + 5 = 14

代码实现（Python伪代码）：
```python
import math

class SqrtDecomp:
    def __init__(self, arr):
        self.n = len(arr)
        self.b = int(math.sqrt(self.n))
        self.arr = arr[:]
        self.block_sums = [0] * ((self.n + self.b - 1) // self.b)
        self._build()

    def _build(self):
        for i in range(self.n):
            block_id = i // self.b
            self.block_sums[block_id] += self.arr[i]

    def update(self, idx, val):
        diff = val - self.arr[idx]
        self.arr[idx] = val
        block_id = idx // self.b
        self.block_sums[block_id] += diff

    def query(self, left, right):
        res = 0
        l_block, r_block = left // self.b, right // self.b

        if l_block == r_block:
            for i in range(left, right + 1):
                res += self.arr[i]
        else:
            # 左侧边缘
            for i in range(left, (l_block + 1) * self.b):
                res += self.arr[i]
            # 完整块
            for blk in range(l_block + 1, r_block):
                res += self.block_sums[blk]
            # 右侧边缘
            for i in range(r_block * self.b, right + 1):
                res += self.arr[i]
        return res
```

这是基础版本——通过存储每块的最小值/最大值而非总和，可适配最值查询。

深入探索可查阅[GeeksforGeeks关于平方根分块](https://www.geeksforgeeks.org/sqrt-decomposition-algorithm-square-root-decomposition-technique-set-1-introduction/)或[CP-Algorithms](https://cp-algorithms.com/data_structures/sqrt_decomposition.html)等资源。
