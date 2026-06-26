---
audio: false
generated: true
image: false
lang: en
layout: post
title: Long Prompts Aid Echo, Not Power
translated: false
type: note
---

Partly true, but the framing needs correction.

A long prompt helps a 124M model in one specific way: it conditions the output toward a narrower region of the distribution. Your own analysis shows this — the table-echo prompts (4, 5) produced *perfect* reproduction because the long structured input pinned down exactly what came next. The model rode the prompt. That's real, and it's why a one-line prompt looks dumber: there's nothing to constrain it, so it defaults to its loop attractors ("product candidates", "raise additional capital").

But "powerful" is the wrong word, and your doc proves why. The model is strong at **echo/continuation while the prompt is doing the work**, and collapses the moment it has to *generate* — note prompts 4 and 5 produced perfect echo then went blank or broke within ~50 tokens. Long prompt buys you coherent continuation for roughly 100–200 tokens, then the same failure modes hit: loops, arithmetic that doesn't add up, domain drift to biotech.

So the precise statement is:

A long prompt **extends the horizon over which the model stays coherent** and **suppresses default loop attractors**, because more context = lower-entropy next-token distribution = the model has less room to wander. A one or two sentence prompt underestimates the model because you're measuring it at its highest-entropy, least-constrained operating point.

It does **not** add capability. No prompt length gives 124M numerical consistency or long-range memory of the original company — those require parameters/depth the model doesn't have. You're not unlocking power, you're reducing the search space so the existing (limited) power isn't wasted.

The mechanism, concretely: at 124M with ~12 layers, the effective "reasoning width" per token is tiny. Long context doesn't increase that width — it just feeds the attention heads a strong signal to copy from, so induction heads dominate (copy what came before) over the weak generative circuits. That's exactly why echo >> generation in your results. Induction is cheap and works at small scale; genuine generation isn't.

So: yes, judge it on long, structured prompts, not toy one-liners — but expect "coherent autocomplete that rides the prompt," not power.
