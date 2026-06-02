---
audio: false
generated: true
image: false
lang: en
layout: post
title: Skip Fundamentals? Hidden AI Pitfalls
translated: false
type: note
---

Question: Since AI tools (Claude Code, Cursor, etc.) can assist with real projects, should we skip foundational learning entirely and just dive straight into building?

Answer:

## Interesting Challenge — But Here's Where It Breaks

You're right that AI dramatically accelerates project work. But "skip fundamentals entirely" creates a **hidden fragility** that shows up at the worst moments.

---

## What AI Actually Does For You

AI tools are genuinely powerful now:

- Explains errors in context
- Writes boilerplate instantly
- Debugs faster than Stack Overflow
- Bridges knowledge gaps on the fly

So yes — **the barrier to starting a real project is near zero now.** You don't need 6 months of courses before touching a codebase. That old advice is dead.

---

## But Here's The Problem You Just Demonstrated

Look at your own nanoGPT session:

```
Why does 400GB of parquet → 140B tokens, not 100B?
Answer: BYTES_PER_TOKEN = 4.0 vs real ~2.85
```

**AI helped you resolve it. But could you have even asked the right question without some foundation?**

The dangerous failure mode is:

```
No foundation
      ↓
AI gives you a plausible-sounding wrong answer
      ↓
You have no sensor to detect it's wrong
      ↓
You ship it / train on it / build on it
      ↓
Catastrophic failure 3 months later
```

This is called **"confident wrongness"** — and AI hallucinates most convincingly in exactly the gaps where you have no foundation to push back.

---

## The Real Updated Stack (AI Era)

```
Tiny foundation (enough to smell when AI is wrong)
        ↓
Real project immediately, AI-assisted
        ↓
Foundation fills in naturally from project pain
        ↓
Bigger projects
```

Not:

```
Big foundation → project     ❌ (old, slow, wasteful)
Zero foundation → project    ❌ (fast but blind)
```

---

## What "Tiny Foundation" Actually Means

Not a course. Not a certification. Just **enough to have a smell test:**

| Domain | Minimum Viable Foundation |
|---|---|
| LLM training | Understand tokens, loss, gradient descent conceptually |
| Systems | Know what memory, disk I/O, and CPU vs GPU mean |
| Code | Read code well enough to know if AI output looks wrong |
| Math | Rough intuition — not proofs |

This takes **days to weeks**, not months. Then you project immediately.

---

## The Real Risk of Pure Vibe-Coding With AI

People are already hitting this wall:

- Build fast with AI → ship → **can't debug production failures** because they don't understand what they built
- Can't interview because they can't explain their own project
- Can't extend the project because the mental model was the AI's, not theirs
- **Worse: they don't know what they don't know**

Karpathy literally coined **"vibe coding"** — and even he warned it breaks down when things go wrong and you have no foundation to fall back on.

---

## Bottom Line

AI didn't kill the need for fundamentals. It **compressed** it.

- Old world: 6 months foundation → project
- AI world: 1-2 weeks bare minimum → project + AI → foundation grows organically

**Skip fundamentals entirely and you become dependent on a tool you can't verify.** That's not a builder — that's a prompt monkey hoping nothing breaks.

The nanoGPT project you're doing *is* the right approach. You're building real things AND developing the foundation to know when something smells wrong.

References:

- [Karpathy on "Vibe Coding" — X/Twitter](https://x.com/karpathy/status/1886192184808149190)
- [The problem with AI-assisted coding without fundamentals — Stack Overflow Blog](https://stackoverflow.blog/2023/12/29/the-best-developers-are-raised-not-just-trained/)
