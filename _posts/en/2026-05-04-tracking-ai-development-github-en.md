---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tracking AI Development on GitHub
translated: false
type: note
---

Question: Is it a good idea to use GitHub to track how fast AI development is accelerating (e.g., by analyzing top AI contributors and comparing activity over time)?

Answer:

It’s a **smart idea in spirit**, but the way you’re framing it right now is a bit too naive to actually work well. GitHub can absolutely give signals about AI velocity—but “tracking top 100 vibe coders” won’t reliably measure what you think it does.

Let’s break it down.

---

## 1. Why your idea is interesting

Using GitHub as a data source makes sense because:

* It’s where a huge portion of AI tooling is built (models, frameworks, infra, agents)
* You can observe **real behavior**, not hype (commits, repos, forks)
* It’s timestamped → perfect for **year-over-year comparison**

So your instinct is right:
👉 *AI progress leaves footprints in code, not just papers or tweets.*

---

## 2. The core problem: “top contributors” is misleading

Tracking “top 100 AI developers” sounds appealing, but breaks down quickly:

### (1) Commits ≠ impact

* Someone can spam commits with small changes
* A single breakthrough repo (e.g., PyTorch or TensorFlow) matters more than thousands of minor commits

### (2) Many top AI builders don’t code publicly

* People at OpenAI, Google DeepMind, or Anthropic often work in private repos

### (3) “Vibe coding” is invisible

* If AI tools generate code, commit counts may:

  * increase artificially (more code)
  * or decrease (less manual work)

So raw GitHub stats can actually **mislead you about speed**.

---

## 3. A better way to measure “AI acceleration”

Instead of focusing on people, track **systems and signals**:

### A. Repo-level signals (high value)

Track top AI repos over time:

* stars growth rate
* fork velocity
* contributor count

Examples:

* LangChain
* LlamaIndex
* AutoGPT

👉 Compare:

* 2024: how long to reach 10k stars
* 2026: how long to reach 10k stars

This directly shows **acceleration of adoption**

---

### B. Time-to-build complexity

Track how fast similar tools appear:

Example:

* 2023: basic chatbot frameworks
* 2024: agent frameworks
* 2025–2026: multi-agent systems, autonomous coding tools

Measure:

* Time between “idea → open-source implementation”

👉 This captures **“idea-to-code latency” shrinking**

---

### C. Code volume vs output

Look at:

* LOC per project
* features shipped per month

Hypothesis:

> If “vibe coding” works, output per developer should increase.

---

### D. Ecosystem density

Track:

* number of new AI repos per month
* % of repos tagged “AI”, “LLM”, “agent”

You’ll likely see exponential growth.

---

## 4. What you *can* do practically

Here’s a concrete version of your idea that would actually work:

### Step 1 — Define AI repo set

Use GitHub topics:

* `llm`
* `ai`
* `agent`
* `deep-learning`

---

### Step 2 — Track metrics over time

For each repo:

* stars per day
* contributors
* commits per week

---

### Step 3 — Compare across years

Example:

| Metric                    | 2024     | 2026    |
| ------------------------- | -------- | ------- |
| Avg time to 10k stars     | 6 months | 2 weeks |
| Avg contributors per repo | 20       | 200     |
| New AI repos/month        | 5k       | 50k     |

---

### Step 4 — Optional: track individuals (carefully)

You *can* track some visible builders like:

* Karpathy (education + code)
* open-source founders

But treat them as **case studies**, not global metrics.

---

## 5. The deeper insight you’re aiming for

What you’re really trying to measure is:

> “Is AI making humans code faster?”

GitHub alone won’t fully answer that.

You’re actually measuring a combination of:

* tooling improvement (Copilot, agents)
* community scaling
* hype cycles
* capital inflow

---

## 6. A sharper framing of your idea

Instead of:

> “Track top 100 vibe coders”

Upgrade it to:

> “Measure the compression of idea-to-production time in AI software using GitHub ecosystem signals.”

That’s a **research-grade idea**.

---

## 7. Final take

Your idea is directionally strong, but:

* ❌ People-based tracking → noisy and misleading
* ✅ Ecosystem + repo dynamics → powerful signal

If you build this well, you could create something like:

> “AI Development Speed Index”

Which would actually be valuable.

---

If you want, I can help you design:

* a full data pipeline (GitHub API + metrics)
* or even a dashboard spec for this idea
