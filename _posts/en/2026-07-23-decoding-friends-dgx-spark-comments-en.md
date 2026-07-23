---
audio: false
generated: true
image: false
lang: en
layout: post
title: Decoding Friend's DGX Spark Comments
translated: false
type: note
---

Question: How to understand your friend's comments about DGX Spark, 30T/s bandwidth, and LPDDR vs GDDR?

Answer:

Your friend is talking from the perspective of **LLM local inference / AI workstation users**, not normal developers.

Let's decode each sentence.

---

### 1. "单人30tk没法用啊"

"30tk" likely means **30 tokens/s** (tokens per second).

For LLM inference:

* 5 tok/s → feels slow but usable for chat
* 20 tok/s → comfortable
* 30 tok/s → quite fast for one user
* 100+ tok/s → workstation/server class

So why say "30 tok/s can't be used"?

Because for a **single person**, 30 tok/s may sound good, but:

* Large models have huge latency from prompt processing (prefill)
* Long context slows down
* Coding agents generate many tool calls
* Multiple agents/users destroy throughput

Example:

You run a coding agent:

```
User:
"Refactor this repo"

Agent:
- read 50 files
- call grep
- analyze
- edit
- run tests
- repeat
```

It is not just generating text. It needs:

```
prefill + decode + tool loop
```

A 30 tok/s machine may feel much slower than Claude/GPT cloud systems.

---

### 2. "DGX Spark纯玩具"

NVIDIA DGX Spark is basically a small AI workstation.

The criticism is:

It has:

* limited memory bandwidth
* limited VRAM/unified memory
* limited scaling

It can run models locally, but compared with:

* H100
* H200
* GB200
* multi-GPU servers

it is tiny.

The analogy:

A gaming laptop can run Unreal Engine.

But nobody calls it a game studio render farm.

DGX Spark is similar:

```
good:
- experiment
- learn
- prototype
- private inference

bad:
- serious serving
- large batch inference
- training frontier models
```

---

### 3. "带宽太小了"

This is the important hardware point.

For LLM inference, memory bandwidth often dominates.

The basic equation:

```
tokens/sec ≈ memory bandwidth / model size
```

Example:

A 70B model:

FP16:

```
70B × 2 bytes ≈ 140GB
```

Every generated token needs to move a large part of this weight data.

If your bandwidth:

```
1 TB/s
```

then theoretical maximum:

```
1000GB/s / 140GB ≈ 7 tokens/s
```

(real world lower)

That is why H100/H200 are fast:

H100 SXM:

```
~3.35 TB/s HBM bandwidth
```

H200:

```
~4.8 TB/s
```

The memory system is the bottleneck.

---

### 4. "LPDDR现在确实比n社自家卖的GDDR便宜多了"

This is actually an interesting point.

NVIDIA normally uses:

* GDDR6/GDDR6X
* HBM

for GPUs.

But DGX Spark uses:

* LPDDR5X unified memory

because it is cheaper.

Comparison:

| Memory     | Bandwidth      | Cost           |
| ---------- | -------------- | -------------- |
| LPDDR5X    | lower          | cheap          |
| GDDR6X     | higher         | expensive      |
| HBM3/HBM3e | extremely high | very expensive |

Apple has proven this approach:

M-series chips:

```
CPU + GPU + unified LPDDR
```

works very well for many workloads.

NVIDIA is borrowing this idea:

```
large cheap unified memory
+
small AI workstation
```

instead of:

```
expensive GPU VRAM
```

---

The core tradeoff:

```
DGX Spark:
        cheap memory
        large capacity
        low bandwidth

H100:
        expensive memory
        smaller capacity
        extreme bandwidth
```

For LLM:

```
capacity helps you load the model
bandwidth helps you run the model fast
```

DGX Spark optimizes:

"Can I fit a big model?"

H100 optimizes:

"How fast can I generate tokens?"

---

For someone like you who runs local models, agents, FLUX, etc., the practical view:

DGX Spark is interesting if:

```
I want:
- Qwen 70B locally
- private assistant
- learning
- edge AI
```

But if your goal is:

```
- many agents
- coding agent loops
- high token throughput
- serving users
```

then bandwidth matters much more.

A used RTX 3090/4090-class machine can sometimes be more useful because the GPU bandwidth is higher, even if memory capacity is smaller.