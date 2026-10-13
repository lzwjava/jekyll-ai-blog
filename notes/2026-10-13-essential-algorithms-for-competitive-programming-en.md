---
audio: false
generated: true
image: false
lang: en
layout: post
title: Essential Algorithms for Competitive Programming
translated: false
type: note
---

Good question — your current catalog covers the *textbook/classroom* set, but competitive programming leans heavily on a few practical workhorses you don't have yet. Here's what I'd recommend, prioritized:

## Tier 1 — Used in almost every contest

| Algorithm | Why you need it | Status |
|---|---|---|
| **Binary search on answer** (parametric search) | Turns "find min/max feasible value" into O(log) predicate checks | ❌ |
| **Two pointers / sliding window** | Subarray sum/subarray distinct problems in O(n) | ❌ |
| **Prefix sums & difference arrays** | Range-sum queries in O(1), range updates in O(1) | ❌ |
| **Segment tree** | Range query + range update — *the* contest data structure | ❌ |
| **Fenwick tree (BIT)** | Simpler alternative to segment tree, inversion counting | ❌ |
| **Kadane's algorithm** | Maximum subarray in O(n) — classic DP warm-up | ❌ |
| **LIS in O(n log n)** (patience/binary search) | Longest increasing subsequence, scheduling | ❌ |
| **Monotonic stack / queue** | Next-greater-element, largest-histogram, sliding-window-max | ❌ |
| **Coin change DP** | Unbounded knapsack variant, appears constantly | ❌ |
| **Bitmask DP (TSP)** | `dp[mask][i]` over subsets — classic CP pattern | ❌ |

## Tier 2 — Graph algorithms contests love

| Algorithm | Use case |
|---|---|
| **0/1 BFS** (deque) | Shortest path with 0/1 weights, O(V+E) vs Dijkstra |
| **Tarjan SCC** | Strongly connected components, 2-SAT, condensation graphs |
| **Bridges & articulation points** (Tarjan) | Critical edges/nodes in networks |
| **Binary lifting / LCA** | k-th ancestor, tree distance queries |
| **Tree DP + rerooting** | Path/dependency problems on trees |
| **Bipartite matching** (Hopcroft-Karp) | Assignment problems, flow reduction |
| **Max flow** (Dinic's) | Min-cut, circulation, matching |
| **Bipartite coloring check** | Even-cycle detection in O(V+E) |

## Tier 3 — Number theory (huge on Codeforces/AtCoder)

- **Sieve of Eratosthenes** (+ linear sieve) — prime enumeration
- **Extended GCD & CRT** — you have `modinv` hidden inside `crypto.rs`, deserves its own entry
- **Modular exponentiation + matrix exponentiation** — Fibonacci/linear recurrences in O(log n)
- **Miller-Rabin primality + Pollard's rho** — factorization for big numbers
- **Combinatorics mod M** — nCr with factorial precomputation, Lucas theorem
- **Digit DP** — count numbers with property in O(digits × states)

## Tier 4 — Strings beyond KMP

- **Z-algorithm** — often simpler than KMP for pattern-in-text
- **Manacher's algorithm** — longest palindromic substring in O(n)
- **Aho-Corasick** — multi-pattern matching (trie + failure links)
- **Rolling hash (double)** — substring equality, Rabin-Karp generalization (you have single)
- **Suffix array + LCP** — advanced, but classic "substring search on steroids"

## Tier 5 — Geometry & misc

- **Convex hull** (Andrew's monotone chain) — geometry gateway problem
- **Point orientation / cross product** basics
- **Backtracking** (N-Queens, subsets, Sudoku)
- **Meet-in-the-middle** — 2^(n/2) for n≈40 subset problems
- **Sparse table (RMQ)** — O(1) idempotent range queries after O(n log n) build
- **Coordinate compression + Mo's algorithm** — offline range queries
- **Top-K / priority-queue greedy** — you have heaps, but not the pattern

---

## My suggestion for the next batch

If you want to extend the catalog, I'd start with **Tier 1's ten** + **0/1 BFS, Tarjan SCC, sieve, extended GCD, Z-algorithm, convex hull** — that's **16 additions**, and they'd slot right into your existing registry as:

```bash
cargo run -- algorithm segment-tree
cargo run -- algorithm binary-search-on-answer
cargo run -- algorithm tarjan-scc
...
```

Each would follow your current style: self-contained demo with printed input/output and a complexity footnote, verifiable output (e.g. segment tree results compared against brute force).

Want me to implement Tier 1 (10 algorithms), Tier 1+2 (18), or the full 16 I suggested? I can also include built-in correctness checks against brute force in each demo, like the karatsuba one does.