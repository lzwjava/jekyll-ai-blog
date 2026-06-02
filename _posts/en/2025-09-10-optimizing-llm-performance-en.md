---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Optimizing LLM Performance with Caching
translated: false
type: note
---

Great, let’s dive deeper. You’re basically describing a **prompt/result caching optimization** problem in large language model (LLM) systems. Let’s break it down step by step:

---

## 1. Why caching matters for LLMs

- **High cost per token**: Running inference on big models (Claude Opus, GPT-4, etc.) is expensive because each token runs through billions of parameters.
- **Redundant work**: Many queries share large overlapping sections (e.g., system prompts, doc contexts, JSON wrappers). Without caching, the model recomputes them each time.
- **Low-latency requirement**: Products like copilots, chat assistants, and agents must respond quickly, so cache hits improve both speed and cost.

---

## 2. What gets cached?

There are a few layers:

1. **Prompt prefix caching (Key-Value Cache in Transformers)**
   - Inside the model: once tokens are processed, their hidden states (KV pairs) can be reused without recomputation if the same prefix reappears.
   - Example: If 90% of your prompt is a fixed system context, and only the last 10% changes, you want to reuse that initial work.

2. **Response caching**
   - Outside the model, you can cache standard question → answer pairs (good for FAQs, but less flexible for dynamic contexts).
   - Generally more useful for retrieval systems or simple API calls.

3. **Serialization & representation caching**
   - E.g., Manus’ optimization: by fixing JSON serialization order (`{"a":1,"b":2}` vs `{"b":2,"a":1}`), repeated requests hash to the same cache key.
   - This prevents “accidental cache misses” caused by non-deterministic ordering of otherwise identical inputs.

---

## 3. Prompt construction strategies

Your point is correct: **put stable/static content first, dynamic variables last.**

- **Why?** Model KV-cache works sequentially. If the first N tokens are identical, you can reuse that entire prefix. Any differences earlier in the prompt invalidate reuse.
- **Example**:
  ❌ Bad: `"User: 12345\n[dynamic part]\nSystem rules...\n"`
  ✅ Good: `"[System rules...]\n[Context]\nUser: 12345"`
  → With the good version, all the “rules/context” can be cached.

This applies at scale in copilots (like Cursor, GitHub Copilot, Replit) which serve millions of similar requests where only the user’s last few keystrokes differ.

---

## 4. Impact on different usage settings

- **Individual users**: Low usage → little benefit, since cache reuse across prompts is rare.
- **Enterprise copilots / coding assistants / agents**:
  - Users often share 70–90% of the system + instruction prompt (only user query changes).
  - At scale (thousands/millions of requests per day), cache savings are enormous.
- **Flat-fee SaaS products**:
  - Providers bear the marginal cost, so caching is essential to remain profitable.
- **Per-token billing (e.g., direct API)**:
  - End-user pays anyway, but providers might still cache internally to reduce GPU load.

---

## 5. Additional caching/optimization strategies companies use

- **Attention Key-Value (KV) Reuse**: Persistent KV caches across turns in a conversation, instead of reprocessing past context each time.
- **Chunked prompts**: Split large contexts into frozen + dynamic chunks, reuse frozen.
- **Deterministic hashing** across inputs (normalize whitespace, sort JSON keys, remove irrelevant metadata).
- **Speculative Decoding**: Multiple models (a cheap small one guesses, big one verifies) – not cache, but another form of efficiency optimization.
- **Vector DB + Retrieval**: Instead of always pasting giant context, retrieve only necessary slices → indirectly reduces what needs caching.

---

✅ **Summary:**
You are correct — moving dynamic content to the **end of prompts** increases cache efficiency because the shared static prefix is reused across many requests. Combined with deterministic serialization and other caching techniques, this is a core scaling and cost optimization strategy for LLM-powered copilots and agents. For low-frequency personal use, the gains are negligible, but for large SaaS products serving millions of queries, it’s critical to profitability.

---

Would you like me to also **draw out a diagram / schematic** (like a visual flow of static vs dynamic prompt caching) so it’s easier to see how prefix reuse actually works?
