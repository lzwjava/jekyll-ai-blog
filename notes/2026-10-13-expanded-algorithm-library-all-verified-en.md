---
audio: false
generated: true
image: false
lang: en
layout: post
title: Expanded Algorithm Library, All Verified
translated: false
type: note
---

All done — **58 → 80 algorithms**, all passing their built-in verifications. Total runtime of the heaviest new demos: 0.28s.

## What was added (contest classics in the spirit of 刘汝佳《算法竞赛入门经典》/《训练指南》)

**Geometry** (`src/algorithms/geometry.rs`) — expanded from 1 → 6:

- `segment-intersection` — orientation/on-segment tests; cross-checked against a 2001-point distance sampler
- `point-in-polygon` — ray casting vs. winding number vs. hand-checked answers, boundary handling
- `closest-pair` — divide & conquer O(n log n), identical to brute force over 79 800 pairs
- `rotating-calipers` — antipodal sweep for the convex diameter, matches O(n²)
- `triangle-centers` — centroid / in-, circum-, orthocenter + Euler line (OG:GH = 1:2)

**Graph** (`graph.rs`) — 9 → 12: `euler-path` (Hierholzer, every edge used once), `bridges` (cut edges/vertices verified by delete-and-recount), `two-sat` (implication graph + SCC + topo assignment, checked against 2ⁿ brute force)

**Network Flow** (new `flow.rs`): `max-flow` (Edmonds-Karp; verifies conservation + max-flow = min-cut over all 16 cuts), `bipartite-matching` (Kuhn vs. exact brute force)

**Number Theory** — 2 → 7: `fast-exponentiation`, `chinese-remainder`, `matrix-exponentiation` (fib(10⁶) in 20 squarings), `discrete-log` (BSGS vs. √p-free full scan), `miller-rabin` (deterministic bases, 0 mismatches for all n < 200 000, fools-proofed against 561/2047/3215031751)

**String** — 4 → 7: `manacher`, `aho-corasick`, `suffix-array` (prefix doubling + Kasai LCP)

**DP**: `digit-dp` (B-number pattern, verified vs. scan at N = 100 000, then runs N = 987 654 321)

**Searching**: `ida-star` (8-puzzle; replays its move list and matches BFS-optimal depth 30)

**Backtracking** (new `backtracking.rs`): `n-queens` (matches OEIS A000170 through n = 10), `sudoku` (MRV solver, solved in 52 nodes)

Every demo follows the existing house style: self-contained `pub fn`, prints a result + independent verification + a complexity footnote, registered in `mod.rs` under a category. `README.md` updated with the new counts and category lists.
