---
audio: false
generated: true
image: false
lang: en
layout: post
title: Manual Control of Tree Expansion Budget
translated: false
type: note
---

Here's what's happening:

**"Run Next Step"** calls `POST /api/tot/sessions/{id}/run` with `additional_budget`. The scheduler then:

1. **Picks the best node** from the frontier (scored, ranked by priority)
2. **Calls the modeling model** — proposes one local reasoning step
3. **Calls the review/eval model** — scores that step
4. **Adds the new child node** to the tree
5. Decrements the budget counter

Each click = one expansion cycle (one branch grows by one node). The tree grows incrementally rather than all at once.

**Why you need to click manually:** when you create a session with `run_on_create: true` it auto-runs the initial budget (default 8 expansions). After that budget is exhausted the scheduler stops and waits. "Run Next Step" lets you spend more budget on demand — you stay in control of how deep the tree grows instead of it running forever.

**To auto-run more steps:** increase the budget number in the input field next to the button before clicking, e.g. set it to `4` to run 4 more expansions at once.