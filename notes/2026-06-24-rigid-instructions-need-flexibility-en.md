---
audio: false
generated: true
image: false
lang: en
layout: post
title: Rigid Instructions Need Flexibility
translated: false
type: note
---

Question: Are overly rigid custom instructions counterproductive, and how can they be made more useful?

Answer:

Yeah, you're right. A few problems with that prompt:

**It's too prescriptive and repetitive.** Mentioning Karpathy/Yin Wang as style targets every response gets stale fast. It's a vibe-setting instruction that wears out — and I end up pattern-matching to the names rather than actually thinking like them.

**The format template is rigid.** `Question: / Answer: / References:` for every single response adds friction for quick exchanges like this one.

**It over-explains your backstory.** Background context is useful once, but restating your full resume every conversation is noise.

**The "randomly check if I'm focused on LLM training" idea is actually good** — but it needs to be an active mechanism, not a passive note. You could implement it as a simple rule like: "10% of the time, at the end of a response, ask me: 'Is this aligned with your LLM training focus?' and flag drift."

**What would actually be more useful:**

A leaner prompt with three sections:

1. **Static context** (devices, preferences, stack) — just a table, no prose
2. **Active rules** (redaction, format, depth level) — concrete and short
3. **Focus enforcement** — a real probabilistic interrupt rule

The "I want to grow like Karpathy" framing should be removed entirely. Instead, just say: "assume strong ML/systems background, go to first principles, show code." The outcome is the same without the cliché.

Want me to rewrite your system prompt from scratch — leaner, more mechanical, with the focus-check mechanic built in?
