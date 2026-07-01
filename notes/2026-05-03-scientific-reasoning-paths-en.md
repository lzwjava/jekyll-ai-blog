---
audio: false
generated: true
image: false
lang: en
layout: post
title: Explores Multiple Scientific Reasoning Paths
translated: false
type: note
---

Now I have enough to walk through the whole flow.

---

## How this solves hard science problems requiring long, divergent reasoning chains

### The core idea

A single LLM call collapses too early — it picks one reasoning path and commits. For problems like "derive the radiation correction to Hydrogen energy levels", there are many plausible routes (perturbation theory vs. path integral vs. Green's functions…) and the wrong early choice wastes everything.

ToT fixes this by **spreading the search across multiple branches and only killing branches that violate physics**.

---

### Step-by-step code walkthrough

**Step 1 — Meta-analysis: break the problem into a route map** (`backend.py:49-56`)

Before any tree is built, a planning model analyzes the problem once:

```
objective, givens, unknowns,
minimal_subproblems, step_ordering,
first_step, completion_signals
```

Crucially: *"keep the plan coarse... preserves many modeling routes"* — it deliberately does NOT solve anything, just maps the strategy space.

---

**Step 2 — Root node built by FSM** (`scheduler.py:148`, `builder.py`)

The FSM for each node runs through these stages:

```
PROPOSE → CALCULATE → EVALUATE → (REFLECT?) → FINALIZED
```

- **PROPOSE**: modeling model proposes one atomic reasoning step (`thought_step`, `equations`, `known_vars`)
- **CALCULATE**: `skills.py` runs `tot_hard_rule_check` — checks equations against physics hard rules
- **EVALUATE**: review model scores on 4 axes (physical 50%, grounding 25%, relevance 10%, simplicity 15%)
- **REFLECT**: if recoverable violation, retry with critique injected

---

**Step 3 — Tree expansion with budget control** (`scheduler.py:162-195`)

```python
while self._frontier and len(self._expanded_node_ids) < self.expansion_budget:
    # pop best node from frontier
    # build N children (each a different reasoning branch)
    built_children = [_build_node(...) for child_context in child_contexts]

    # rank siblings by score
    ranked_children = sorted(built_children, key=_node_ranking_key)

    # apply scheduler controls (diversity, dedup, budget)
    scheduler_action = self._apply_scheduler_controls(child_node, parent_node)
```

`expansion_budget=8` limits total nodes expanded. `max_frontier_per_diversity_key=2` prevents the tree from flooding with near-identical branches.

---

**Step 4 — Hard rules kill bad branches, scores just reprioritize** (`builder.py:69-77`)

```
Physical hard-rule violations → PRUNED_BY_RULE + DROP  (no soft score can rescue)
Low scores → stay ACTIVE, just ranked lower downstream
```

This is the key insight: the tree **keeps exploring** weak-but-not-wrong branches while eliminating physically impossible ones immediately.

---

**Step 5 — Orchestrator ensures each node adds exactly one delta** (`backend.py:63`, `builder.py:70`)

The proposal prompt enforces:
> *"each node must add exactly one explicit local delta beyond the parent: one correction, one boundary condition, or one control parameter"*

This prevents the classic LLM failure of restating the parent node — every step in the tree genuinely advances the reasoning.

---

### Why this works for hard science

| Problem with naive LLM | ToT solution |
| --- | --- |
| Commits to one strategy early | Explores multiple routes in parallel via tree branches |
| No way to detect physics errors mid-chain | `skills.py` hard-rule check vetoes wrong equations immediately |
| Long chains drift off-topic | Each node scored on contextual relevance; scope drift logged |
| Repetition across steps | Semantic delta check (`SEMANTIC_DELTA_TEXT_SIMILARITY = 0.72`) detects near-duplicate nodes |
| Can't recover from one bad step | Recoverable violations → REFLECT, not DROP |
