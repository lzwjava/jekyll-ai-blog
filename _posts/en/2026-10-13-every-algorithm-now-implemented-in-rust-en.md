---
audio: false
generated: true
image: false
lang: en
layout: post
title: Every Algorithm Now Implemented in Rust
translated: false
type: note
---

All done — **every algorithm from your list is now implemented in Rust** under one command. Zero new warnings (the 8 remaining are pre-existing dead code in `word2vec`/`uno`).

## Usage

```bash
cargo run -- algorithm list              # catalog of all 42 algorithms
cargo run -- algorithm quicksort         # run one
cargo run -- algorithm dijkstra          # names ignore case & dashes
```

## What was built — `src/algorithms/` (2,814 lines, 11 modules)

| Category | Implementations |
| --- | --- |
| **Searching** | linear, binary (iterative), BFS (queue + path reconstruct), DFS |
| **Sorting** | bubble (early-exit), merge, **quick (Lomuto, 10k bench)**, heap (sift-down), tim (natural runs + minrun insertion + pairwise merge), radix (LSD base-256 with sign-bit XOR trick) |
| **Graph** | Dijkstra (BinaryHeap), Bellman-Ford (+neg-cycle detect), Floyd-Warshall, Kruskal (via Union-Find), Prim, topological sort (Kahn), A\* (grid, Manhattan) |
| **DP** | Fibonacci (memo **and** tabulation), 0/1 knapsack (+backtrack), LCS (+recovery), edit distance, matrix-chain (+parenthesization) |
| **Crypto/Hashing** | **SHA-256** (full implementation, passes FIPS `("abc")` test vector), textbook RSA (modpow + extended-gcd inverse), Diffie-Hellman, consistent hashing (BTreeMap ring, shows minimal reshuffling) |
| **Trees & structures** | traversals, **AVL** (4 rotation cases; 1..=15 sorted insert → height 4, not 15), trie, Union-Find (path halving + union by rank) |
| **Divide & Conquer** | Strassen (7-subproblem, verified == naive), **Karatsuba** (base-10⁴ bignum, 1000 random products verified; **179ms → 55ms** on 4000-digit operands) |
| **ML** | batch gradient descent (recovers `y=3x+7`), backprop on XOR (2-2-1 net → `0.012/0.987/0.989/0.010`), k-means, KNN |
| **String** | KMP (LPS table), Rabin-Karp (rolling hash + verify), Boyer-Moore/Horspool — all three find the same `[2, 7, 10]` |
| **Greedy** | Huffman (50% bit saving vs ASCII), activity selection, fractional knapsack |

## Verification

- Every one of the **42 algorithms** was run — no panics, correct outputs (FIPS hash vector, `kitten→sitting=3`, `LCS="BCBA"`, matrix-chain `15125`, MST weight `11` from both Kruskal and Prim, karatsuba==schoolbook, etc.)
- `src/quicksort.rs` was replaced by the new `sorting::quick_sort` (your old `algorithm quicksort` command still works)
- README updated with the full catalog

Changes are uncommitted (`src/algorithms/` is untracked) — say the word if you want a commit.
