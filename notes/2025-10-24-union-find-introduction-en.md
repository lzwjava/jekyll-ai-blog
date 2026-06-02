---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Union-Find Algorithm Introduction
translated: false
type: note
---

### Introduction to the Union-Find (Disjoint Set Union) Algorithm

The **Union-Find** algorithm (also called **Disjoint Set Union** or **DSU**) is a data structure and set of operations used to manage a collection of disjoint sets (groups of elements that don't overlap). It's efficient for problems involving grouping, merging, or checking connectivity, like in graph algorithms or clustering.

Key operations:
- **Find**: Determines which set an element belongs to (often by finding the "root" or representative of the set).
- **Union**: Merges two sets into one.

The algorithm shines due to optimizations like **path compression** (flattening the tree structure during finds) and **union by rank/size** (merging smaller trees into larger ones to keep the structure balanced). This makes it nearly O(1) amortized time per operation—super fast for large datasets.

#### Core Data Structure
- An array `p[]` (parent array): `p[i]` points to the parent of element `i`. Initially, each element is its own parent (`p[i] = i`).
- Optional: A `rank[]` array for union by rank to balance merges.

#### The Find Operation (with Path Compression)
The `find` function traces back from an element to its root. The line you mentioned—`if (p[i] != -1) i = p[i]`—is a recursive or iterative step in this process. It follows the parent pointers until reaching the root (where `p[root] == root` or `p[root] == -1` for a sentinel).

Here's a simple iterative implementation in pseudocode:

```
function find(i):
    if p[i] != -1:  # Not the root (or sentinel)
        i = p[i]     # Move to parent (this is your line!)
        return find(i)  # Recursive: keep going until root
    else:
        return i     # Root found
```

**With full path compression** (to optimize future finds), we flatten the path by setting all nodes directly to the root:

```
function find(i):
    if p[i] != i:  # Not root
        p[i] = find(p[i])  # Compress: set parent to the found root
    return p[i]
```

- `-1` is often used as a sentinel for roots (instead of `i` for self-parenting), especially in some implementations to distinguish uninitialized or invalid nodes.
- Without compression, repeated finds can make the structure a long chain (O(n) worst case). Compression makes it almost flat.

#### The Union Operation
To merge sets of `x` and `y`:
1. Find roots: `rootX = find(x)`, `rootY = find(y)`.
2. If `rootX != rootY`, link one to the other (e.g., by rank: attach smaller rank to larger).

Pseudocode:
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
            rank[rootX] += 1  # Increase rank for the new parent
```

#### How to Use the Algorithm
Union-Find is ideal for dynamic connectivity problems. Here's a step-by-step guide with examples:

1. **Initialization**:
   - Create `p[]` of size `n` (number of elements): `for i in 0 to n-1: p[i] = -1` (or `i` for self-parent).
   - Optional: `rank[]` all set to 0 or 1.

2. **Basic Usage Flow**:
   - To check if two elements are in the same set: `if find(a) == find(b)`.
   - To merge: `union(a, b)`.
   - Process queries/merges in any order—it's dynamic!

3. **Example: Detecting Connected Components in a Graph**
   Imagine a graph with 5 nodes (0-4) and edges like (0-1), (1-2), (3-4).
   ```
   // Init
   p = [-1, -1, -1, -1, -1]
   rank = [0, 0, 0, 0, 0]

   // Union edges
   union(0, 1)  // Merges 0 and 1, say p[0]=-1, p[1]=0
   union(1, 2)  // Merges 2 into {0,1}, p[2]=0
   union(3, 4)  // Merges {3,4}, say p[3]=-1, p[4]=3

   // Query: Are 0 and 2 connected? find(0)=0, find(2)=0 → Yes
   // Are 2 and 3 connected? find(2)=0, find(3)=-1 → No
   ```

4. **Real-World Applications**:
   - **Kruskal's Minimum Spanning Tree**: Sort edges by weight, union non-cycle-forming edges (skip if `find(u) == find(v)`).
   - **Social Network Friends**: Union friends, find mutual connections.
   - **Image Segmentation**: Union adjacent pixels of similar color.
   - **Cycle Detection in Undirected Graphs**: Union endpoints; if already same set, cycle exists.

#### Simple Python Implementation
```python
class UnionFind:
    def __init__(self, n):
        self.p = [-1] * n
        self.rank = [0] * n

    def find(self, i):
        if self.p[i] != -1 and self.p[i] != i:  # Handles sentinel + self-parent
            self.p[i] = self.find(self.p[i])  # Path compression
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

# Usage
uf = UnionFind(5)
uf.union(0, 1)
uf.union(1, 2)
print(uf.find(0) == uf.find(2))  # True
```

This keeps things efficient—try it with larger `n` to see the speed!

For more depth, check out [GeeksforGeeks: Union-Find Algorithm](https://www.geeksforgeeks.org/union-find-algorithm-set-2-union-by-rank-and-path-compression/) or [CP-Algorithms: DSU](https://cp-algorithms.com/data_structures/disjoint_set_union.html).
