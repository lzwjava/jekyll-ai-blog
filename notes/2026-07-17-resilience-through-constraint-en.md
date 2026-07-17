---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resilience Through Constraint
translated: false
type: note
---

Yeah, that's a healthy reframe. A dead motherboard forces a constraint you don't usually have to think about — and constraints are clarifying. Most of what actually matters (algorithm design, data prep, eval harnesses, debugging training loops) is CPU-bound anyway. The GPU is just the last mile.

And cloud GPU means the "outage" is really just a cash-flow decision, not a blocker. Rent an MI300X or H100 by the hour for the runs that actually need it, keep iterating locally for everything else. Arguably a more resilient setup than owning hardware that can single-point-of-failure on you mid-project.

Gratitude's fine, but the more useful version of this insight is probably: build your workflow so a dead motherboard is a minor inconvenience, not a crisis. If it wasn't already, it is now.

How long's the repair turnaround? If it's more than a few days, worth spinning up a cloud box for anything time-sensitive in the meantime.
