---
audio: false
generated: true
image: false
lang: en
layout: post
title: "FreeToken: Beyond VRAM for Local AI"
translated: false
type: note
---

Question: **How will FreeToken affect the trend of local model serving and the broader AI ecosystem?**

Answer:

I think **FreeToken is more important as a direction than as a serving engine itself**.

The key idea is:

> **The future definition of "GPU memory" becomes less important than "total local memory bandwidth + interconnect + compute."**

FreeToken explicitly treats **GPU VRAM + system RAM + CPU + PCIe** as one inference machine, instead of assuming the entire model must fit inside VRAM. Its paper reports serving models as large as **284B on a gaming desktop** and **753B GLM-5.2 on a single workstation GPU**. ([arXiv][1])

---

## 1. The old local-LLM model

Historically, local serving looked roughly like:

```text
                GPU VRAM
       ┌──────────────────────┐
       │ entire model         │
       │ KV cache             │
       │ activations          │
       └──────────────────────┘
                 │
              compute
                 │
              tokens
```

So people naturally ask:

```text
"Can my RTX 4090 24GB run this model?"
```

If:

```text
model_size > VRAM
```

you're basically screwed, or you accept huge CPU offload penalties.

This creates the familiar obsession:

```text
12 GB → 16 GB → 24 GB → 48 GB → 80 GB → 96 GB → 192 GB
```

---

# 2. FreeToken changes the mental model

For MoE:

```text
                 System RAM
        ┌─────────────────────────┐
        │ Expert 0                │
        │ Expert 1                │
        │ Expert 2                │
        │ ...                     │
        │ Expert N                │
        └────────────┬────────────┘
                     │ PCIe
                     ▼
              ┌──────────────┐
              │ GPU VRAM     │
              │              │
              │ hot experts  │
              │ KV cache     │
              │ shared stuff │
              └──────┬───────┘
                     │
                     ▼
                  Tensor Cores
```

The important property of MoE is:

```text
total parameters ≫ active parameters
```

For example:

```text
284B total
      ↓
only a small subset of experts activated/token
```

So you don't necessarily need:

```text
284B × bytes_per_parameter
```

inside VRAM.

Instead, you need:

```text
VRAM
+ RAM
+ PCIe bandwidth
+ GPU compute
+ expert locality/cache
```

FreeToken's `offload` backend keeps experts in host RAM and maintains an LRU cache of experts on the GPU; cache misses are streamed over PCIe. ([GitHub][2])

That's the really interesting architectural shift.

---

# 3. This makes PCIe a much more important part of AI infrastructure

This is probably the part I'd pay the most attention to.

Historically:

```text
GPU:
  compute
  HBM/VRAM

CPU:
  orchestration
```

PCIe was mostly considered an I/O bus.

FreeToken effectively says:

```text
PCIe = model-serving memory fabric
```

For example:

```text
RAM
 │
 │  ~10-30 GB/s depending on platform
 │
 ▼
PCIe Gen4/Gen5
 │
 ▼
GPU VRAM
 │
 ▼
Tensor cores
```

Now hardware purchasing starts looking different.

Instead of:

> "How much VRAM does this GPU have?"

you start asking:

```text
VRAM capacity
VRAM bandwidth
PCIe generation
PCIe lanes
CPU memory bandwidth
RAM capacity
RAM bandwidth
GPU compute
expert cache locality
```

This is a **big conceptual change**.

---

# 4. It could make cheap used GPUs much more valuable

This is particularly interesting for the kind of hardware you have been looking at.

Suppose you have:

```text
RTX 3090
24GB VRAM
```

and:

```text
128GB DDR4/DDR5
PCIe Gen4 x16
```

You don't necessarily need to buy a $5k–$10k accelerator just because the model has hundreds of billions of parameters.

You can construct:

```text
        128GB RAM
             │
             │ PCIe
             ▼
       RTX 3090 24GB
             │
             ▼
          MoE model
```

The GPU becomes the **hot execution/cache layer**, rather than the complete model's storage.

FreeToken's documentation explicitly describes this model: system RAM can contain the complete expert pool while VRAM holds shared/non-expert weights, KV state and recently used experts. ([FreeToken Wiki][3])

That means:

**used GPU + lots of RAM + good PCIe motherboard**

becomes a much more interesting local-AI configuration.

---

# 5. But there's an important catch

This doesn't magically make:

```text
284B model
```

equivalent to:

```text
24B model
```

The bottleneck becomes **bandwidth**.

Imagine an expert fetch requires:

```text
1 GB
```

and PCIe effectively gives you:

```text
20 GB/s
```

The theoretical transfer alone is:

```text
1 GB / 20 GB/s
= 50 ms
```

That's already:

```text
~20 tok/s
```

before considering computation, synchronization, multiple experts, kernels, etc.

So the real equation becomes something like:

$$
T_{token}
\approx
\max(
T_{GPU},
T_{CPU},
T_{PCIe}
)
$$

with good overlap.

This is why FreeToken has bandwidth-adaptive execution and multiple backends:

```text
fused
offload
cpu
hybrid
```

The `hybrid` mode can fetch some experts through PCIe while computing others on CPU. ([GitHub][2])

---

# 6. And this is where the research gets really interesting

FreeToken isn't just:

```text
"CPU offloading"
```

That's old.

The interesting problem is:

> **Where should every piece of the model live at this exact moment?**

You have:

```text
GPU
 ├── compute
 ├── VRAM
 └── high bandwidth

CPU
 ├── compute
 ├── RAM
 └── huge capacity

PCIe
 └── transport
```

And the runtime dynamically decides:

```text
expert A → GPU
expert B → RAM
expert C → CPU
expert D → GPU
```

based on:

```text
routing
cache state
PCIe bandwidth
CPU performance
GPU availability
KV-cache pressure
```

That's much closer to **distributed systems / memory scheduling** than traditional inference.

---

# 7. This also changes what "local AI" means

I think there are three stages.

### Stage 1 — GPU-local

```text
model
  ↓
VRAM
  ↓
GPU
```

Examples:

```text
7B
14B
32B
70B
```

depending on quantization.

---

### Stage 2 — CPU/GPU offload

```text
RAM
 ↓
PCIe
 ↓
GPU
```

You can run larger models, but performance becomes painful.

This is what many existing local inference systems have historically done.

---

### Stage 3 — heterogeneous inference

FreeToken is pushing toward:

```text
                 ┌──── GPU
                 │
Model state ─────┼──── CPU
                 │
                 ├──── RAM
                 │
                 ├──── PCIe
                 │
                 └──── KV cache
```

with the runtime deciding how to distribute computation and state.

That's a much more scalable architecture.

---

# 8. MoE makes this particularly powerful

I think this is the biggest reason FreeToken's timing is interesting.

The industry is increasingly interested in:

```text
MoE
```

because:

```text
Total parameters ↑
Active parameters ↓
```

For example:

```text
Model:

300B parameters

but each token:
     ↓
only ~20B active
```

That is almost perfect for heterogeneous local inference.

You can store:

```text
300B
```

across:

```text
RAM + VRAM
```

but only move/use:

```text
active experts
```

per token.

FreeToken's supported model list already spans models such as DeepSeek-V4-Flash, Qwen3.6/3.5 MoE, GLM-5.2, gpt-oss, Gemma-4 and MiniMax-M2.5. ([GitHub][2])

So I think **MoE + quantization + heterogeneous memory** is going to be one of the major local-inference trends.

---

# 9. The bigger implication: model size will continue exploding

This is the interesting feedback loop.

Imagine the industry discovers:

```text
300B MoE
```

can be served reasonably well on:

```text
one workstation GPU
+
128/256GB RAM
+
PCIe Gen5
```

Then model designers have less reason to constrain:

```text
total parameter count
```

because serving doesn't require:

```text
all parameters in VRAM
```

So you can get:

```text
35B
 ↓
100B
 ↓
300B
 ↓
700B
 ↓
1T+
```

while active computation might remain much smaller.

This creates an interesting future:

> **"Huge model, small active model" becomes normal.**

---

# 10. This could also reduce the importance of "consumer GPU VRAM" as the only metric

Imagine these two machines:

### Machine A

```text
GPU:
RTX 5090
32GB VRAM

RAM:
64GB

PCIe:
Gen4
```

### Machine B

```text
GPU:
RTX 4090
24GB VRAM

RAM:
256GB

PCIe:
Gen5 x16
```

For traditional inference:

```text
A > B
```

because A has more VRAM.

For huge MoE inference:

```text
B might be surprisingly competitive
```

because:

```text
256GB RAM
+
higher host capacity
+
fast PCIe
```

can compensate for the smaller VRAM pool.

That's a significant change in hardware economics.

---

# 11. But don't overestimate FreeToken yet

There is a very important reality check.

FreeToken itself is still young.

The repository is moving extremely quickly, and even its own issue tracker contains performance problems. For example, one recent report found an automatic `hybrid` choice achieving only **0.67 tok/s** versus **5.58 tok/s** with forced `offload` on a 2×3090 DeepSeek-V4-Flash setup. ([GitHub][4])

So I wouldn't conclude:

> "FreeToken solved local 700B inference."

Rather:

> **FreeToken demonstrates that a different serving architecture is viable.**

That's the important part.

---

# 12. I think the real trend is bigger than FreeToken

I'd rank the coming local inference stack roughly like this:

```text
                    Local AI
                       │
        ┌──────────────┼──────────────┐
        │              │              │
       MoE         Quantization    KV/cache
        │              │              │
        └──────────────┼──────────────┘
                       │
              Heterogeneous memory
                       │
        ┌──────────────┼──────────────┐
        │              │              │
       GPU            CPU            RAM
        │              │              │
        └──────────────┼──────────────┘
                       │
                    PCIe/CXL
                       │
                local AI server
```

And then:

```text
Speculative decoding
MTP
expert caching
prefix caching
KV compression
quantization
kernel optimization
```

all stack on top.

---

# 13. This creates a new type of AI engineer

This is actually relevant to what you've been learning recently.

The valuable skill won't simply be:

> "I know vLLM."

It becomes:

```text
PyTorch
   ↓
CUDA
   ↓
Triton
   ↓
attention
   ↓
MoE
   ↓
quantization
   ↓
KV cache
   ↓
expert cache
   ↓
PCIe
   ↓
CPU/GPU scheduling
   ↓
distributed/heterogeneous serving
```

You're essentially becoming a **model systems engineer**.

And FreeToken is a very good project to study because you can literally see this boundary:

```text
LLM architecture
        ↓
MoE routing
        ↓
memory placement
        ↓
GPU kernels
        ↓
PCIe transfers
        ↓
scheduler
        ↓
serving API
```

That's much deeper than just calling an inference API.

---

# 14. My prediction

I'd make these bets:

| Trend                                                    |   My confidence |
| -------------------------------------------------------- | --------------: |
| MoE becomes increasingly dominant                        |   **Very high** |
| Quantization becomes increasingly aggressive             |   **Very high** |
| Local inference becomes heterogeneous                    |   **Very high** |
| CPU/RAM becomes an active part of model serving          |        **High** |
| PCIe bandwidth becomes an important AI metric            |        **High** |
| 100B–1T open models become increasingly runnable locally |        **High** |
| One consumer GPU serving frontier MoE becomes normal     |        **High** |
| FreeToken itself becomes the dominant runtime            | **Low/unknown** |
| vLLM/TensorRT-LLM disappear                              |    **Very low** |

The last distinction matters.

**FreeToken doesn't need to win for this architecture to win.**

Someone else can implement the same idea in:

```text
vLLM
llama.cpp
SGLang
TensorRT-LLM
MLC
new runtime
```

and the architectural trend still wins.

---

## The most important takeaway

I would summarize FreeToken in one sentence:

> **FreeToken is an early example of moving local LLM serving from "fit the model into VRAM" toward "compose GPU compute, VRAM, RAM, CPU and interconnect into one inference system."**

And I think **that is a genuinely important direction for the next 2–5 years of local AI**.

The really interesting research question isn't:

```text
"How do I make a 300B model fit into a 24GB GPU?"
```

It's:

```text
"Given 24GB VRAM + 256GB RAM + PCIe Gen5,
how do I schedule every byte and every expert
to maximize tokens/sec?"
```

That is a **systems problem**, and it's exactly where CUDA/Triton/MoE/KV-cache knowledge starts becoming extremely valuable.

References:

* [FreeToken GitHub repository](https://github.com/FlashML-org/FreeToken?utm_source=chatgpt.com)
* [FreeToken paper — Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](https://arxiv.org/abs/2608.16157?utm_source=chatgpt.com)
* [FreeToken supported models and MoE backends](https://github.com/FlashML-org/FreeToken/blob/main/docs/models.md?utm_source=chatgpt.com)
* [FreeToken CLI / serving architecture](https://github.com/FlashML-org/FreeToken/blob/main/docs/cli.md?utm_source=chatgpt.com)
* [FreeToken roadmap](https://github.com/FlashML-org/FreeToken/issues/79?utm_source=chatgpt.com)

[1]: https://arxiv.org/abs/2608.16157?utm_source=chatgpt.com "FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution"
[2]: https://github.com/FlashML-org/FreeToken/blob/main/docs/models.md?utm_source=chatgpt.com "FreeToken/docs/models.md at main · FlashML-org/FreeToken · GitHub"
[3]: https://www.freetoken.wiki/hardware/FreeToken-vram?utm_source=chatgpt.com "FreeToken vram: Setup Guide for Local MoE Inference - FreeToken Wiki"
[4]: https://github.com/FlashML-org/FreeToken/issues/151?utm_source=chatgpt.com "`ft bench bw` picks `hybrid` on Ampere, but `offload` is 8.3x faster (DeepSeek-V4-Flash, 2x RTX 3090) · Issue #151 · FlashML-org/FreeToken · GitHub"