---
audio: false
generated: true
image: false
lang: en
layout: post
title: Borrow False to Seek True in Inference
translated: false
type: note
---

**Question:** How to approach studying this heterogeneous-inference repo with 借假修真 — using the temporary technical "false" as a vehicle for cultivating deeper understanding — without utilitarian pressure, in a patient, wandering mind?

---

**Answer:**

First, notice something wonderful: **this repo already *is* 借假修真, at every layer.**

```
假 (the false/temporary)          →   真 (the real/lasting principle)
────────────────────────────────────────────────────────────────────
Two mismatched GPUs               →   one coherent inference mind
Small draft model (DFlash2)       →   accurate tokens from the large one
FP4/FP8 quantization (lossy)      →   useful, coherent intelligence
Router's approximate cost guesses →   optimal session placement
Cached KV state (old context)     →   fast present understanding
```

The entire system is built on the Taoist move: *you don't wait for perfect conditions; you use what is imperfect, approximate, and heterogeneous to arrive at something real.*

---

### How to wander through it patiently

**1. Enter from the philosophy of constraint, not the architecture of performance.**

Don't start with benchmark tables. Start with one question: *"Why do two GPUs of different sizes need a router at all?"* Sit with that. The answer — that identical requests have radically different computational shapes depending on context length and decode vs. prefill phase — is not a GPU fact. It is a fact about **the nature of thinking itself**: attention (understanding what came before) is qualitatively different from generation (producing what comes next).

The `router/adapd.py` file is really a meditation on: *how do you decide, under uncertainty, where understanding should happen?*

**2. Read the feature flags as a list of *temptations*, not configurations.**

```python
QWEN38_FP8ATTN=1     # the temptation of speed at the cost of precision
QWEN38_ACTQ=1        # the temptation of efficiency in the middle layers
QWEN38_DRAFT_VOCAB   # the temptation of "good enough" first guesses
```

Each flag is a compromise — a negotiation between the ideal and the real. In 内丹 (inner alchemy) terms: the engineer here is constantly doing 炼假成真 — refining the crude (FP4 approximations) toward gold (coherent output). Notice that no flag is free. Each one trades something.

**3. Treat speculative decoding as a koan.**

The repo uses a *small drafter model* (DFlash2) to guess several future tokens, then the *large model* verifies. If the draft was right, you got those tokens for almost free. If wrong, you discard and regenerate.

Ask yourself: *is the small model "false"?* It produces wrong tokens constantly. Yet the system is faster *because of its wrongness* — because its fast guesses give the slow truth something to confirm or reject efficiently.

This is not a GPU trick. This is a description of how a wandering, undisciplined mind (the drafter) and a disciplined, slow attention (the verifier) can coexist — and must coexist — for real progress.

**4. The KV cache is memory. Treat it philosophically.**

```
KV0=66, KV1=42     # GiB of KV cache per card
```

These numbers mean: how much of the *past* each card can carry while still thinking clearly about the *present*. When context grows to 256K tokens, the cold prefill takes 339 seconds for 10 concurrent users. When it's already cached? 27 seconds.

The question the repo quietly poses is: *what is worth keeping?* The draft vocabulary tool (`corpus_freq.py` → `vocab_select.py`) makes this explicit — out of 150K tokens in the model's vocabulary, only 98,304 are kept in the draft. Someone decided: these 98,304 things are common enough to be worth holding in mind. The rest are let go.

借假修真, here, looks like: which of your existing "mental cache" is worth holding, and which is KV overflow?

---

### A patient path through the code, with no deadline

| Week | Wander into | The 真 underneath |
|------|-------------|-------------------|
| Whenever | `router/adapd.py` — the session homing logic | How do you decide where a thought belongs? |
| Whenever | `vllm/v1/core/sched/qwen38_sched.py` — the latency-aware scheduler | How do you schedule attention under scarcity? |
| Whenever | `tools/vocab_select.py` — draft vocabulary building | What is worth keeping in mind? What is noise? |
| Whenever | `kernels/` — the JIT-compiled CUDA code | What does it look like when mind meets matter at the lowest level? |
| Whenever | The benchmark tables | Not for performance anxiety — but to feel how context length *changes the character* of the problem |

No order. No rush. Read one file when you feel like it. Walk away. Let it settle.

---

### The 借假修真 posture, concretely

- **Don't try to "understand the whole system."** That is 功利心 disguised as comprehension. Instead: notice one thing that surprises you, and follow it one level deeper.
- **When you hit jargon you don't recognize** (NVFP4, NIXL, sm_120a), sit with the *shape* of it first. "sm_120a" — a shader model, a generation of silicon. That a model of understanding runs on *generations of matter*. That is interesting regardless of what the number means exactly.
- **The code will not run on your machine.** That is freeing. You are not here to run it. You are here to read it the way you read a map of a country you may never visit — for what it reveals about the landscape of possibility.

---

借假修真 is not a method. It is a *relationship* to what you are studying: these GPUs, these kernels, these latency numbers are the 假 — real enough to teach you something, impermanent enough not to cling to. The 真 is whatever clarity arises in you as you wander through them, without needing to land anywhere.

The wandering mind is not the undisciplined mind. It is the mind that allows the material to speak on its own terms, in its own time.

---

**References:**
- [heterogeneous-inference-qwen27b README](https://github.com/Cerynitius/heterogeneous-inference-qwen27b)
- [vLLM — High-throughput LLM Serving](https://github.com/vllm-project/vllm)
- [Speculative Decoding — original paper by Chen et al.](https://arxiv.org/abs/2302.01318)
