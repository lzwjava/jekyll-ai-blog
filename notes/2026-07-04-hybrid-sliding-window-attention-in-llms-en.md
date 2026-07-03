---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hybrid Sliding Window Attention in LLMs
translated: false
type: note
---

Question: What does “Sliding window | 512 (hybrid — 35 SWA layers + 7 global layers)” mean in LLMs?

Answer:

This refers to an **attention context strategy** used in transformer-based large language models to reduce compute cost while still keeping some ability to handle long-range dependencies.

### 1. Sliding Window Attention (SWA)

A **sliding window of 512 tokens** means:

* Each token can only attend to the **previous 512 tokens**
* Instead of full attention over the entire context (which is expensive)
* This makes attention cost **linear with sequence length instead of quadratic**

So instead of:

* Full attention: every token sees every other token → very expensive

You get:

* Local attention: each token sees a *window* of recent tokens only

---

### 2. “35 SWA layers + 7 global layers” (Hybrid design)

This means the model is mixing two types of transformer layers:

#### 🔹 SWA layers (35 layers)

* Use sliding window attention (local context only)
* Efficient and fast
* Good for most language patterns (short/mid-range dependencies)

#### 🔹 Global layers (7 layers)

* Use **full attention** or extended attention
* Can attend to the entire sequence
* Used to preserve long-range reasoning and memory

---

### 3. Why mix them?

Pure sliding window models:

* Fast
* But may forget earlier context beyond window

Pure full attention models:

* Accurate long-range reasoning
* But very expensive (O(n²))

Hybrid approach:

* Most layers are cheap (SWA)
* A few layers are “global memory refresh points”

This gives a good tradeoff:

> ⚖️ Efficiency of local attention + reasoning ability of global attention

---

### 4. Intuition

Think of it like reading a book:

* SWA layers → you only remember the last few pages while reading
* Global layers → occasionally you re-scan the whole book and refresh key ideas

---

### 5. Why “512”?

“512” is the **window size**, meaning:

* Each token can only look back 512 tokens
* If sequence is longer, older tokens are ignored in most layers

This is common in efficient LLMs like:

* Mistral-style architectures (variants)
* Long-context optimized transformers
* Many modern inference-optimized models

---

If you want, I can also explain how this compares to **RoPE scaling, ALiBi, or full attention Transformers**, or how it affects training vs inference speed.