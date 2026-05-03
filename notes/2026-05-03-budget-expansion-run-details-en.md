---
audio: false
generated: true
image: false
lang: en
layout: post
title: Budget and Expansion Run Details
translated: false
type: note
---

Clear. Here's exactly what **RUN BUDGET** means:

- **`expansion_budget`** = total number of node expansions the scheduler is allowed to perform in the session lifetime. Set to `8` by default on session creation.
- **RUN BUDGET input** = `additional_budget` — how many **more** expansions to add on top of what's already been done when you click "Run Next Step".

**What happens:**
- `budget = 0` → just re-runs the scheduler against the **existing** budget (resumes if it was paused mid-budget)
- `budget = 4` → adds 4 more expansion slots and immediately runs them

**Each expansion = one node built** (planning call + modeling call + review/eval call). So `budget = 4` means 4 new nodes will be added to the tree.

**In your case:** session started with `expansion_budget = 8`. The root build + one expansion round likely used all 8. Set the input to `4` and click Run — that adds 4 more nodes to the tree.