---
audio: false
generated: true
image: false
lang: en
layout: post
title: Root Node Pass Prevents Tree Expansion
translated: false
type: note
---

Found it. The root node has status `pass` (not `ACTIVE`), so `_is_expandable` returns `False` — it never gets added to the frontier and no children are generated.

**Why the root is `pass` not `active`:** the node FSM transitions through states. A node becomes `pass` when the review model marks it as a **terminal** or complete step. With a simple problem like the one you tried, the model likely concluded the root already contained the full answer — so it sealed it as `pass` immediately.

**To get a real tree with branches**, try a harder multi-step problem that the model can't resolve in one step, e.g.:

> *A rocket burns fuel at 50 kg/s with exhaust velocity 3000 m/s. Starting from rest with initial mass 10000 kg, find the velocity after 60 seconds using the Tsiolkovsky equation, accounting for gravity losses.*

Or increase `max_children_per_expansion` in the scheduler config JSON in the UI — but the real fix is a problem complex enough that the model doesn't treat the root as already-done.
