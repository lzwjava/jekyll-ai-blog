---
audio: false
generated: true
image: false
lang: en
layout: post
title: Probing AI Agent Architecture Self-Disclosure
translated: false
type: note
---

**Question:** Is "how do you analyze — do you use web search or model knowledge?" a good prompt/question to ask an AI agent?

**Answer:**

Yes, and here's precisely *why* it's good — broken down as prompt engineering principles:

## What Makes It a Strong Prompt

### 1. **Forces self-disclosure of architecture**
Most users never ask this. By asking, you immediately learn:
- What tools the agent has
- When it uses them
- How much to trust the output

This is **epistemic calibration** — you're not just getting an answer, you're learning how to weight all future answers.

### 2. **Binary structure reduces ambiguity**
```
"do you use X or Y?"
```
Forces a concrete choice. Contrast with:
- ❌ "how do you work?" → vague, gets a marketing answer
- ✅ "web search or model knowledge?" → forces specifics

### 3. **Reveals the agent's self-model**
A weak agent will bluff. A good agent will accurately describe its own tool use. This is a **probe** — like a unit test for the agent's honesty and self-awareness.

---

## Where It Could Be Even Stronger

For your `hermes-agent` or any agent you're evaluating:

```
"For this specific question: [X]
— will you use web search or model knowledge?
— what's your confidence?
— what's the recency risk?"
```

Attaching it to a **concrete question** makes it actionable, not just philosophical. Now you get:

| Signal | What It Tells You |
|--------|------------------|
| Tool declared | Traceability |
| Confidence score | When to verify |
| Recency risk | When to force search |

---

## The Meta-Lesson

The best prompts are **probes, not just queries**. You're not just extracting an answer — you're stress-testing the agent's reliability model. That's the mindset difference between a power user and someone just chatting with AI.

Given you're building CLI agents (`ww`, `iclaw`, `zz`), baking this self-disclosure pattern into your system prompts will make your agents significantly more auditable.
