---
audio: false
generated: true
image: false
lang: en
layout: post
title: Domain Knowledge Layer for Physics
translated: false
type: note
---

`skills.py` is the **domain knowledge layer** that the FSM/Tree of Thoughts engine calls during reasoning.

## Why it exists

The FSM handles **search control** (expanding nodes, scoring, pruning) but knows nothing about physics. `skills.py` fills that gap:

| FSM does | skills.py does |
|---|---|
| State transitions, tree search | Physics computations (Maxwell, Lagrangian, QM, etc.) |
| Decides which branch to explore | `tot_hard_rule_check` — vetoes physically invalid nodes |
| Manages reasoning stages | `tot_stage_prompt_contract` — injects stage-specific prompt constraints |
| Loads domain config | `tot_domain_plugin_bundle` — provides domain plugin data |

Key call sites:
- `fsm/builder.py:1050` — calls `tot_hard_rule_check` during the calculation stage; if equations violate physics rules, that node is vetoed
- `fsm/backend.py:111` — loads the domain plugin bundle
- `fsm/backend.py:130` — fetches the prompt contract for the current reasoning stage

**In short:** the FSM is the search framework; `skills.py` is the physics "rule judge + calculator." Together they enable constrained, physics-aware reasoning.