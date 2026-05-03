---
audio: false
generated: true
image: false
lang: en
layout: post
title: Root Node Status Explained
translated: false
type: note
---

Now I have the full picture. Here's what's actually happening:

**The root node IS correctly `ACTIVE` + `PASS`** — that means it passed evaluation and is ready to expand. The "PASS" badge is `result_state`, not the overall status. The node is healthy.

**Why only one node:** The root gets added to the frontier, then the expansion loop runs. It calls `_extract_child_contexts(root_problem_context)` which synthesizes child contexts from `route_options`. At `step_index=0` with no `selected_route_family`, it creates **one child per route option**, capped by `route_surface_budget` (= `max_children_per_expansion`, default 4).

**The real issue is the budget.** After building the root, `expansions_used = 0`. But then the loop runs and **building the root itself counts as the expansion**. With `expansion_budget = 8` and the root taking significant model calls, the frontier expansion starts — but kimi-k2 is slow, so those 8 slots might be exhausted building just the root + a few nodes before they render.

**What to do:** click "Run Next Step" with a larger number (e.g. `4`) in the budget input. Each click expands the frontier further. The route branches (dependency, constraint, invariant, scaling) should appear as children of the root after the next run. The tree only grows when you explicitly add budget after `run_on_create` finishes.