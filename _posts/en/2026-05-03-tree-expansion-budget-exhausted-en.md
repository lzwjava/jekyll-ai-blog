---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tree Expansion Budget Exhausted
translated: false
type: note
---

Now I have the full picture. Here's the answer:

**The frontier is empty because the expansion budget ran out mid-run**, not because the tree is done.

The tree has 4 nodes (root + 3 route children). The 3 children ARE expandable — each would generate a child at step 1 (`choose one active correction`). But the session used all its budget building those 3 children before it could add them to the frontier for the *next* round.

**"remaining 12"** = budget you can still add via Run.

**To continue and see the result:**
1. Type `3` in the Run Budget field (one expansion per branch)
2. Click **Run Next Step** — each of the 3 route branches (dependency, constraint, invariant) will grow one more node at depth 2
3. Repeat — step 2 and step 3 nodes get built, eventually the deepest nodes become `SOLVED` (not just `PASS`)

**The "result" in this system is not a single answer box** — it's the highest-scoring `SOLVED` leaf node in the tree. Click any node to see its full proposal, equations, and reasoning in the detail panel on the right.