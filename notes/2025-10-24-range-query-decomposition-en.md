---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Square Root Decomposition for Range Queries
translated: false
type: note
---

### Square Root Decomposition

Square Root Decomposition (often abbreviated as √-decomposition) is a technique in computer science and competitive programming used to optimize range queries and updates on large arrays or data structures. It's particularly useful when you need to answer queries like "find the sum/max/min of elements in a subarray" efficiently, without relying on heavy machinery like segment trees or Fenwick trees, which can be more complex to implement.

#### Why Use It?
- **Time Complexity Trade-off**: For an array of size \\( n \\), naive range queries take \\( O(n) \\) time per query. Square Root Decomposition reduces this to \\( O(\sqrt{n}) \\) per query and update, which is a good balance for many problems where \\( n \\) is up to \\( 10^5 \\) or \\( 10^6 \\).
- **Simplicity**: It's easier to code and debug compared to advanced data structures.
- **Applications**: Common in problems involving range sum queries, range minimum queries (RMQ), or frequency counting in sliding windows.

#### How It Works
1. **Divide into Blocks**: Split the array into blocks of size \\( \sqrt{n} \\) (rounded down). If \\( n = 100 \\), block size \\( b = 10 \\), so you get 10 blocks.
   - Each block stores precomputed information (e.g., sum of elements in that block for sum queries).

2. **Query a Range [L, R]**:
   - **Full Blocks**: For complete blocks entirely within [L, R], just fetch the precomputed value in \\( O(1) \\) per block. At most \\( O(\sqrt{n}) \\) full blocks.
   - **Partial Blocks**: For the edges (left and right partial blocks), iterate through the individual elements manually, which takes \\( O(\sqrt{n}) \\) time total (since each partial block is size \\( \sqrt{n} \\)).
   - Total: \\( O(\sqrt{n}) \\).

3. **Updates**: When updating an element, rebuild the precomputed value for its block in \\( O(\sqrt{n}) \\) time (by re-summing the block).

#### Simple Example: Range Sum Query
Suppose we have an array `A = [1, 3, 2, 4, 5]` and \\( n=5 \\), so block size \\( b = \sqrt{5} \approx 2 \\). Blocks:
- Block 0: [1, 3] → sum = 4
- Block 1: [2, 4] → sum = 6
- Block 2: [5] → sum = 5 (last block may be smaller)

Query sum from index 1 to 4 (0-based: elements 3,2,4,5):
- Partial left: Index 1 (in Block 0) → add 3
- Full Block 1: Add 6
- Partial right: Index 4 (in Block 2) → add 5
- Total: 3 + 6 + 5 = 14

To implement in code (Python pseudocode):
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
            # Left partial
            for i in range(left, (l_block + 1) * self.b):
                res += self.arr[i]
            # Full blocks
            for blk in range(l_block + 1, r_block):
                res += self.block_sums[blk]
            # Right partial
            for i in range(r_block * self.b, right + 1):
                res += self.arr[i]
        return res
```

This is a basic version—adapt it for min/max by storing min/max per block instead of sums.

For deeper dives, check resources like [GeeksforGeeks on Square Root Decomposition](https://www.geeksforgeeks.org/sqrt-decomposition-algorithm-square-root-decomposition-technique-set-1-introduction/) or [CP-Algorithms](https://cp-algorithms.com/data_structures/sqrt_decomposition.html).
