---
audio: false
generated: true
image: false
lang: en
layout: post
title: Understanding OpenClaw Token Consumption
translated: false
type: note
---

**Question:**
Why does OpenClaw consume ~3 million tokens per day even when I’m not actively using it (as seen in OpenRouter)?

**Answer:**

Short answer: it’s almost certainly *still doing work in the background*.

When a system like OpenClaw (or similar agent-style frameworks) is running, “doing nothing” from your perspective doesn’t mean idle. These systems are often built as **continuous loops** or **autonomous agents**, and they can burn tokens quietly through several mechanisms:

---

### 1. Continuous agent loop (most common cause)

Many agent frameworks run something like:

```
while True:
    observe()
    think()
    act()
```

Even if no meaningful task is happening, the model is still:

* re-evaluating state
* generating thoughts/plans
* calling the LLM repeatedly

Each loop = tokens consumed.

If the loop runs fast (e.g., every 1–5 seconds), you can easily hit millions of tokens/day.

---

### 2. Hidden background tasks

OpenClaw-style systems often include:

* memory summarization
* log analysis
* environment polling (GUI, browser, etc.)
* retry loops for failed tasks

These can trigger LLM calls like:

* “Summarize current state”
* “Decide next action”
* “Check if task complete”

Even if nothing changes, the model is still queried.

---

### 3. Long context accumulation

If the system keeps appending history:

* each new call includes **previous messages**
* token usage grows over time

Example:

* 1k tokens → 2k → 4k → 8k per call
  Now even a few calls = huge daily usage

---

### 4. Multiple parallel agents or threads

Some frameworks silently run:

* planner agent
* executor agent
* evaluator agent

So one “step” might actually be **3–5 LLM calls**.

---

### 5. Retry / failure loops

If something is slightly broken:

* API call fails
* action doesn’t complete

The system may retry endlessly:

```
try → fail → reflect → retry → fail → reflect ...
```

This can explode token usage very quickly.

---

### 6. OpenRouter accounting makes it visible

Platforms like OpenRouter show **total token usage**, so you suddenly notice:

* background loops
* inefficiencies
* runaway agents

Without that visibility, you'd never realize it's happening.

---

### Rough intuition

3 million tokens/day ≈

* ~35 tokens/sec continuously, OR
* ~1,500 tokens per call × 2,000 calls/day

That’s totally consistent with a fast loop + moderate context.

---

### What to check immediately

1. **Is the process still running?**

   * Background script / server / Docker container?

2. **Loop frequency**

   * Look for `while True` or polling intervals

3. **Context size**

   * Are you appending full history every call?

4. **Number of LLM calls per step**

   * Planner + executor + critic?

5. **Retry logic**

   * Any infinite retry loops?

6. **Logs**

   * You’ll likely see constant LLM requests even when idle

---

### Practical fixes

* Add a **sleep interval** (e.g., 5–30 seconds)
* Stop loop when no task exists
* Limit context length (truncate history)
* Disable unused agents
* Add a **hard token budget per day**
* Log every LLM call (you’ll instantly see the culprit)

---

### Key insight

Agent systems are not like normal apps.
If you don’t explicitly **stop them**, they behave like:

> “Always thinking, even when there’s nothing to think about.”

And thinking = tokens = money.

---

If you want, you can paste your OpenClaw config or loop code, and I can pinpoint exactly where the tokens are being burned.
