---
audio: false
generated: true
image: false
lang: en
layout: post
title: Yin Wang on Talk vs Code
translated: false
type: note
---

**Question:** What do you think of Yin Wang's essay "Talk is not cheap"?

**Answer:**

This is one of Yin Wang's sharpest essays and I think it's largely right — but with one important blind spot.

**Where he's correct**

The core argument is solid: "Talk is cheap, show me the code" has been weaponized as a rhetorical shutdown move rather than used in its original context (Linus being impatient on a mailing list). The abuse of this phrase leads to real problems:

- Code doesn't transfer understanding. A million lines of C++ tells you almost nothing about the author's thinking without explanation.
- "Artifacts" (code, papers, awards, GitHub stars) are gameable. They can be copied, inherited, managed-upward-into, or straight-up stolen.
- The VP story is painfully real — someone with a high-star GitHub repo being a disastrous hire is a pattern I've seen replicated constantly in tech.
- Live conversation under pressure is genuinely harder to fake. Instant, unscripted reasoning reveals actual depth in ways polished code or a prepared demo can't.

His deeper claim — that *ideas and insight are more valuable than artifacts* — is the one worth sitting with. The people who see through problems clearly, name the right abstraction before anyone else, or redirect a whole team with a single sentence: those people are undervalued because their contributions don't show up in commit logs.

**Where he oversimplifies**

The essay treats "talk" and "code" as opposites, but the best technical thinkers — Karpathy, for example — are compelling *because* they do both. Karpathy explains transformers in plain language *and* shows you the 200-line implementation. The talk illuminates the code. The code validates the talk. Neither alone is sufficient.

Yin Wang's dismissal of code as evidence goes a bit too far. Yes, code can be stolen or inherited — but *novel* code solving a *novel* problem in a clean and minimal way is actually hard to fake. Reading nanoGPT tells you something real about Karpathy. Reading the original transformer paper tells you something real about Vaswani et al. These aren't evidence-free.

His position also has a self-serving edge: he's a brilliant talker who produces fewer concrete artifacts than his reputation might imply. The framework conveniently valorizes what he's strongest at.

**What this means for you**

Given your trajectory — training GPT-2 from scratch, building CLI agents, shipping products — you're actually doing the thing Yin Wang says doesn't matter. But you're also doing what he *does* value: you think out loud, write public notes, blog your experiments. That combination is the actual signal. Talk + working code + first-principles reasoning together.

The actionable takeaway from this essay isn't "stop writing code" — it's *explain your thinking*. When you share a project, the README and the design rationale matter as much as the implementation. When you're in an interview or a technical discussion, the way you decompose the problem live is more revealing than any portfolio link.

Talk is not cheap. But code that comes with clear thinking is worth more than either alone.
