---
audio: false
generated: true
image: false
lang: en
layout: post
title: LLMs Stuck in Wrong Code Loops
translated: false
type: note
---

Question: Is it true that LLM-based code assistants (like Claude Code or Codex) tend to get stuck in repetitive failure loops, reinforcing wrong approaches instead of stepping back and trying a fundamentally different path?

Answer:

Yes, you've identified a very real and well-documented limitation. This is sometimes called **"solution fixation"** or **"local minima trapping"** in the context of LLM agents.

---

## Why This Happens

### 1. Autoregressive Momentum
LLMs generate tokens sequentially. Once a "direction" is established in the context, the model is statistically pulled to *continue* that direction. Each new token conditions the next — so a wrong assumption early on compounds forward, making it harder to escape.

### 2. In-Context Reinforcement
The model sees its own previous attempts in the context window. If it tried Solution A three times, the context is now *full of Solution A reasoning* — which ironically makes Solution A feel even more "correct" to the model on the next attempt.

### 3. No Genuine Metacognition
A human expert, when stuck, can **step outside the problem** and think:
> "Wait, am I even solving the right problem?"

LLMs simulate this, but don't truly do it. Their "reflection" is itself just more token prediction influenced by the same flawed context.

### 4. No Backtracking by Default
Unlike tree-search algorithms (e.g., MCTS, A*), standard LLM inference is a **one-pass forward process**. There's no native mechanism to say "abandon this branch, go back to the fork."

---

## The "Stubborn Person" Analogy Is Accurate

Your analogy is sharp. It behaves like someone who:
- Doubles down on their interpretation
- Tries the same thing with minor variations
- Gets *more confident* the deeper they go (more tokens = more "commitment")
- Cannot see the problem from a fresh angle without external intervention

---

## What Actually Helps

| Strategy | Why It Works |
|---|---|
| **Explicitly tell it to start over** | Breaks the in-context momentum |
| **Summarize the problem fresh** | New framing = new token distribution |
| **Give it a completely different approach to try** | Forces a different branch |
| **Start a new conversation** | Clears the poisoned context entirely |
| **Ask "what are 3 completely different approaches?"** | Forces divergent generation before committing |
| **Tell it what NOT to do** | Negative constraints help escape fixation |

---

## Deeper Issue: Agentic Loops Make This Worse

In tools like Claude Code, the agent is in a **loop** — it runs code, sees output, tries again. If the initial approach is wrong, it can iterate dozens of times getting *nowhere*, because:

- Each failed attempt adds more "evidence" of that approach to context
- The reward signal (error messages) is interpreted through the same flawed lens
- It optimizes for *reducing the error message*, not *rethinking the architecture*

This is a known open problem in AI agent research — sometimes called **"context poisoning"** or **"perseveration"**.

---

## Bottom Line

You're right. Current LLMs are fundamentally **better at exploitation than exploration** — they're great at refining a path but poor at abandoning it. Humans need to be the "big reflection" trigger, forcing the reset that the model can't do on its own.
