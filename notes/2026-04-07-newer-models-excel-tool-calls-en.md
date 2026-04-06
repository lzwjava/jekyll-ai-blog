---
audio: false
generated: true
image: false
lang: en
layout: post
title: Newer Models Excel in Tool Calls
translated: false
type: note
---

Question: Is it correct that **DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf** performs poorly in OpenClaw (tool calls, instruction following), and that trying a newer model like Gemma—preferably released within the last 6 months—is a better approach?

Answer:

Yes — your reasoning is **basically correct**, and this behavior is expected. 👍
There are three separate issues here:

---

# 1. Why DeepSeek-R1-0528-Qwen3-8B Q4 behaves badly in OpenClaw

This model has **three limitations**:

### (1) Small base model (8B)

* Tool-calling agents (like OpenClaw) need:

  * planning ability
  * strict instruction following
  * JSON/tool schema adherence
* 8B models often fail at:

  * calling tools
  * downloading files
  * multi-step reasoning
  * long context execution

So you’ll see:

* ❌ ignores instructions
* ❌ doesn't download when told
* ❌ hallucinated tool calls
* ❌ wrong JSON

This is **normal for 8B**.

---

### (2) Quantization reduces reasoning quality

You're using:

```
Q4_K_M
```

That means:

* smaller memory
* lower precision
* weaker reasoning
* worse tool calling

For agents, **quantization hurts more** than chat.

---

### (3) DeepSeek R1 distills are not tool-trained

DeepSeek-R1 distills are optimized for:

* reasoning
* math
* chain-of-thought

They are **NOT optimized for agents / tool calling**.

So OpenClaw struggles.

---

# 2. Yes — newer models are much better for agents

Your idea is correct:

> best to try models released within last 6 months

Because recent models improve:

* tool calling
* structured output
* function calling
* instruction following
* agent loops

This matters more than raw IQ.

---

# 3. Much better models for OpenClaw (local)

Try these (ranked):

### Best (8B–12B class)

* Gemma 2 / Gemma 4 (newest) ✅
* Qwen2.5-Instruct (newer than Qwen3 distills)
* Llama-3.1-8B-Instruct
* Mistral-Nemo (very good agent behavior)

---

### Even better (if VRAM allows)

* 14B class
* 20B class
* 27B class

Agent performance jumps a lot.

---

# 4. Gemma is a good next test

You're doing the right thing:

> downloading gemma, test next

Gemma usually has:

* better instruction following
* cleaner JSON
* more stable tool calls
* less hallucination

Especially:

* gemma-2-9b
* gemma-4-12b / 26b

These work much better with OpenClaw.

---

# 5. What matters MOST for OpenClaw

Priority order:

1. Instruction following (most important)
2. Tool calling training
3. Long context
4. Reasoning ability
5. Size

DeepSeek-R1-8B only has #4.

That’s why it struggles.

---

# 6. Your conclusion

Yes — correct:

* DeepSeek-R1-8B not ideal for OpenClaw ✅
* tool call problems expected ✅
* try Gemma next ✅
* prefer models released < 6 months ✅

You're choosing correctly.