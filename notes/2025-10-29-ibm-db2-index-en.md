---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: IBM DB2 Index Structure Explained
translated: false
type: note
---

### How IBM DB2 Indexes Work

IBM DB2 uses **B+ trees** as the primary data structure for its indexes. This is a balanced tree variant optimized for disk-based storage and range queries, common in relational databases. B+ trees ensure efficient searches, insertions, and deletions with logarithmic time complexity (O(log n)), making them ideal for large datasets. Below, I'll break down the structure, key operations, and DB2-specific notes.

#### B+ Tree Structure in DB2
A B+ tree in DB2 is organized into a hierarchy of **pages** (also called nodes), each typically 4KB in size on disk. The tree is self-balancing, meaning all leaf nodes are at the same depth, and it grows or shrinks dynamically as data changes. Here's the breakdown:

- **Root Page**: The entry point at the top of the tree. It contains sorted key values and pointers to child pages below it. For small indexes, the root may directly point to leaf pages.

- **Internal (Non-Leaf) Pages**: These intermediate levels act as directories. Each page holds:
  - A sorted list of **index keys** (the values from the indexed column(s), e.g., employee IDs).
  - Pointers to child pages (one more pointer than keys, separating ranges).
  - Specifically, each entry is the **highest key value** in the subtree below it, paired with a **Record Identifier (RID)**—a unique pointer to the page and slot where the actual data row lives in the table.

  Non-leaf pages do *not* store actual data pointers; they guide traversal.

- **Leaf Pages**: The bottom level, linked bidirectionally (forward and backward) for efficient range scans. Each leaf page contains:
  - Full sorted **key values** from the indexed column(s).
  - Associated **RIDs** pointing directly to the table rows.
  - Pointers to adjacent leaf pages, enabling sequential access (e.g., for `WHERE column BETWEEN x AND y`).

The tree starts with at least 2 levels (root + leaves) and can grow to 3–5+ levels for massive tables (millions of rows). The number of levels (NLEVELS) is queryable via `SYSCAT.INDEXES` and impacts performance—fewer levels mean faster traversals, but DB2 auto-manages this.

Indexes are stored separately from tables in their own tablespace, consuming disk space proportional to the indexed data (e.g., a unique index on a 1M-row table might take ~10–20% of the table size).

#### How Searching Works
1. Start at the **root page** and load it into memory.
2. Compare the search key (e.g., `WHERE id = 123`) to the sorted keys in the current page.
3. Select the appropriate child pointer (e.g., if search key > current key, go right).
4. Repeat down the tree (1–5 I/O operations typically) until reaching a **leaf page**.
5. In the leaf, scan the sorted keys to find matches, then use the RID to fetch the exact row from the table (one more I/O).

This path compression keeps traversals shallow. For range queries, once at the starting leaf, follow sibling links to scan sequentially without jumping back up the tree.

#### Insertion and Deletion
- **Insertion**:
  1. Traverse to the correct leaf (as in search).
  2. Insert the new key + RID into the sorted leaf page.
  3. If the page overflows (exceeds max entries, ~200–500 depending on key size), split it into two pages and insert a separator key into the parent (internal) page.
  4. If the parent overflows, split upward (may create a new root). DB2 locks pages briefly for concurrency.

- **Deletion**:
  1. Traverse to the leaf and remove the key + RID.
  2. If the page underflows (too few entries), borrow from a sibling or merge with it, removing the separator key from the parent.
  3. Propagate merges upward if needed. DB2 may delay reorganization to batch changes for efficiency.

These operations maintain balance automatically, with minimal page splits/merges (~1% of operations).

#### DB2-Specific Features
- **Optimized B+ Trees** (in DB2 for z/OS): Enhanced for mainframe concurrency, with fractal prefetching to predict and preload pages, reducing I/O.
- **Clustering**: Indexes can be "clustered" (data physically sorted by index order) for better range performance.
- **Types**: Supports unique, composite (multi-column), and bitmap indexes, all B+ based. No native hash indexes.
- **Maintenance**: Run `RUNSTATS` after bulk changes to update statistics for the optimizer. Tools like `INSPECT` check for issues.

B+ trees excel in DB2 because they minimize random I/O (key for disk-bound systems) and support sorted access without full table scans.

[Index structure - IBM](https://www.ibm.com/docs/en/db2/11.1.0?topic=indexes-index-structure)
[DB2 LUW Indexes: B-Tree Details](https://datageek.blog/2013/09/19/db2-luw-basics-indexes/)
[Inside Db2 for z/OS: How Optimized B+ Trees Power High-Speed Indexing](https://planetmainframe.com/2025/06/inside-db2-for-z-os-how-optimized-b-trees-power-high-speed-indexing/)
[How to Understand DB2 B-Tree Index Quickly](https://srinimf.com/2021/07/26/db2-how-to-understand-b-tree-structure-of-index/)
[Db2 Index Overview](https://www.idug.org/news/db2-index-overview)
