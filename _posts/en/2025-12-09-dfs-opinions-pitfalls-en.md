---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Unpopular DFS Opinions and Pitfalls
translated: false
type: note
---

Question: What are some unpopular opinions about Depth-First Search (DFS)?

Answer:

Here are some genuinely unpopular or contrarian opinions about DFS that you’ll rarely see praised in textbooks, LeetCode comments, or algorithm courses:

- **DFS is often the wrong default choice in interviews and real code**, yet people reach for it first because “recursion feels elegant.” In practice, explicit-stack iterative DFS is almost always better than recursive DFS (avoids stack-overflow surprises, easier to add state like visited timestamps or parent pointers), but most people still write the recursive version and pray the test cases aren’t deep.

- **Iterative DFS with a stack is basically just a manually managed recursion** and is more bug-prone than people admit. You end up re-implementing the call stack yourself and still have the same worst-case memory behavior as recursion, but now with off-by-one errors and harder debugging.

- **DFS is overrated for cycle detection in directed graphs.** Everyone teaches Kosaraju/Tarjan with DFS twice or three times, but a simple topological sort attempt (Kahn’s algorithm with BFS/indegree) detects cycles just as easily and usually runs faster in practice on sparse graphs.

- **Pre-order, in-order, and post-order classifications for trees are mostly useless pedantry outside of specific tree problems.** In 95% of real tree traversal needs (serialization, path finding, subtree checks, etc.), you just need “visit node + recurse on children” in whatever order makes sense for the problem; forcing it into one of the three academic labels adds zero insight.

- **DFS is terrible for “shortest path” problems in unweighted graphs** (people still use it with a visited set and claim it’s BFS). It’s not BFS. You’ll get a path, but almost never the shortest one in terms of number of edges unless you’re extremely lucky with the neighbor ordering.

- **The “DFS + backtracking = magic” mindset has ruined more coding interviews than it has helped.** Half the hard backtracking problems (Sudoku, N-queens, etc.) time out with naive DFS because people never bother to add even basic pruning or heuristics—yet the myth persists that “just DFS everything” is a valid strategy.

- **Graph coloring, Hamiltonian path, and most NP-complete problems don’t actually need fancy algorithms in competitive programming**—a well-pruned DFS with bitmasks beats every “smart” polynomial heuristic 90% of the time under 1-second limits. This is unpopular because textbooks pretend these problems are unsolvable; in contest reality, brute-force DFS wins.

- **DFS forests and discovery/finishing times are overhyped.** Almost nobody in industry uses Tarjan’s SCC or articulation-point algorithms that rely on them. When you actually need strongly connected components at scale, you use Kosaraju (still DFS-based, but simpler) or modern parallel algorithms, not the single-pass DFS magic.

- **Recursive DFS on trees with 10⁵+ nodes will randomly fail in Python/Java/C++** depending on the judge’s recursion limit, yet people copy-paste the same template everywhere instead of just using iterative or increasing the stack size (which is considered “ugly”).

In short: DFS is powerful, but the community has a massive blind spot about its practical pitfalls and overhypes its theoretical beauty.

References:

- [Stack Overflow: Recursive DFS vs Iterative DFS](https://stackoverflow.com/questions/12946923/iterative-depth-first-traversal)
- [LeetCode Discuss: DFS vs BFS for shortest path myths](https://leetcode.com/discuss/general-discussion/1053079/shortest-path-in-unweighted-graph-bfs-vs-dfs)
- [Codeforces blogs on bitmask DP + DFS for NP-complete problems](https://codeforces.com/blog/entry/70647)
