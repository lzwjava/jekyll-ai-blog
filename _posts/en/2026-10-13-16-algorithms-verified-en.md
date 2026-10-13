---
audio: false
generated: true
image: false
lang: en
layout: post
title: 16 Algorithms Verified
translated: false
type: note
---

All 16 algorithms are implemented, registered, and verified. Summary:

## New modules

| File | Contents |
|---|---|
| `src/algorithms/arrays.rs` | `two-pointers`, `prefix-sums`, `monotonic-stack` |
| `src/algorithms/numbertheory.rs` | `sieve`, `extended-gcd` (+ `modinv` demo) |
| `src/algorithms/geometry.rs` | `convex-hull` (Andrew's monotone chain) |

## Added to existing modules

| File | Additions |
|---|---|
| `searching.rs` | `binary-search-on-answer` (ship-capacity predicate, counts its 8 checks vs 29 linear scans) |
| `dp.rs` | `kadane`, `lis` (O(n log n) patience + reconstruction), `coin-change`, `bitmask-dp` (TSP) |
| `graph.rs` | `zero-one-bfs` (cross-checked against the existing `dijkstra_impl`), `tarjan-scc` (verified via mutual reachability) |
| `trees.rs` | `segment-tree` (lazy range-add/sum, public `SegTree`), `fenwick-tree` (public `Fenwick` + inversion counting) |
| `strings.rs` | `z-algorithm` |

## Registry & docs
- `mod.rs`: 16 new `Algorithm` entries, 3 new categories (**Array Techniques**, **Number Theory**, **Geometry**) — catalog now at **58** demos
- `README.md`: updated count and category lists

## Built-in correctness checks (like karatsuba)
- `segment-tree`: 500 random range-add/query ops vs a plain array
- `bitmask-dp`: TSP result vs all 8! = 40320 orderings
- `kadane`/`lis`: 500/300 random arrays vs O(n²) brute force
- `two-pointers`, `monotonic-stack`, `prefix-sums`, `fenwick-tree`, `z-algorithm`, `convex-hull`, `sieve`, `extended-gcd`, `zero-one-bfs`, `tarjan-scc`: each printed `true` against its independent reference

Testing caught two real bugs, both fixed: the segment tree recursed infinitely into uncovered leaves (missing leaf guard → index overflow), and the Fenwick inversion counter sized its value domain one short (`max` vs `max + 1`).

All 58 registered demos run clean with zero new compiler warnings. Changes are not committed yet — say the word if you'd like a `feat: add 16 competitive-programming algorithms` commit.