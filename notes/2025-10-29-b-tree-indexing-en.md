---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: B-Trees for Efficient Database Indexing
translated: false
type: note
---

### What is a B-Tree?

A B-tree (short for "balanced tree") is a self-balancing tree data structure designed for efficient storage, insertion, deletion, and retrieval of large volumes of data. It's particularly optimized for systems where data is stored on disk (like databases), as it minimizes the number of expensive disk I/O operations by keeping the tree as shallow as possible.

#### Key Properties of a B-Tree
- **Order (or Degree)**: Defined by a parameter *t* (minimum degree), where each node can have between *t-1* and *2t-1* keys (and up to *2t* children). This allows nodes to hold multiple keys, making the tree wider and shorter.
- **Balanced Structure**: All leaf nodes are at the same level, ensuring logarithmic time complexity for operations (O(log n), where n is the number of keys).
- **Sorted Keys**: Keys in each node are stored in sorted order, and the tree maintains this invariant. Subtrees to the left of a key contain smaller values, and to the right contain larger ones.
- **Node Structure**: Internal nodes have keys that guide searches to child nodes. Leaf nodes store the actual data (or pointers to it).

Unlike binary search trees (BSTs), which are limited to two children per node and can become unbalanced (leading to O(n) worst-case performance), B-trees are multi-way trees that stay balanced through splitting and merging nodes during insertions/deletions.

#### Simple Example
Imagine a B-tree of order 3 (*t=3*, so 2-5 keys per node). A small tree might look like this in text form:

```
       [10, 20, 30]
      /    |    |    \
 [5,7]  [15] [22,25] [35,40]
```

- Searching for 25: Start at root, compare with 10/20/30 → go right to [22,25] → found.

This structure allows efficient range queries (e.g., all keys between 15 and 25) by traversing a few nodes.

### How Databases Use B-Trees

Databases (like relational ones: MySQL, PostgreSQL, SQL Server) heavily rely on B-trees (or variants like B+ trees) for **indexing** to speed up queries on large tables stored on disk. Without indexes, queries would require full table scans (O(n) time, slow for millions of rows).

#### Primary Uses in Databases
1. **Primary and Secondary Indexes**:
   - A **primary index** is built on the primary key (unique identifier). It organizes the table's rows in B-tree order for fast lookups.
   - **Secondary indexes** are on other columns (e.g., name, date). The leaf nodes point to the actual row locations (via row IDs).

2. **Efficient Disk Access**:
   - Disks read data in blocks (e.g., 4KB pages). B-tree nodes are sized to fit one disk block, so a search typically requires reading only 3-4 blocks (tree height), vs. potentially thousands in a linked list.
   - Height is logarithmic: For 1 billion keys, height might be just 4-5 levels.

3. **B+ Tree Variant (Common in DBs)**:
   - Most databases use **B+ trees**, a B-tree tweak where:
     - Only leaf nodes store data/pointers.
     - Internal nodes have keys for routing only.
     - Leaves are linked (doubly-linked list) for efficient sequential scans and range queries (e.g., `SELECT * WHERE age BETWEEN 20 AND 30`).
   - This improves range operations and cache efficiency.

4. **Operations in Practice**:
   - **INSERT/UPDATE/DELETE**: The tree splits or merges nodes to maintain balance. Databases handle concurrency with latches/locks.
   - **Query Optimization**: The query planner uses index statistics to choose B-tree indexes over table scans.
   - **Clustered vs. Non-Clustered**: In clustered indexes (e.g., InnoDB in MySQL), the table data is physically stored in B-tree leaf order. Non-clustered ones just point to data.

#### Benefits and Trade-offs
- **Pros**: Fast for equality, range, and sorted queries; handles growing data well.
- **Cons**: Overhead for inserts/deletes (tree maintenance); not ideal for very frequent updates without batching.

In summary, B-trees are the backbone of database performance for indexed access, turning what could be linear searches into near-constant-time operations via their balanced, disk-friendly design.

#### References
- [B-tree - Wikipedia](https://en.wikipedia.org/wiki/B-tree)
- [B+ Tree in DBMS - GeeksforGeeks](https://www.geeksforgeeks.org/introduction-of-b-tree/)
- [How Indexes Work in SQL Databases - Use The Index, Luke](https://use-the-index-luke.com/sql/anatomy/index-btree)
