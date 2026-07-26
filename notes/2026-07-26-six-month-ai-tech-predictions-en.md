---
audio: false
generated: true
image: false
lang: en
layout: post
title: Six Month AI Tech Predictions
translated: false
type: note
---

Question: **Predict what will happen in the next 6 months (AI, tech, markets, and your likely trajectory).**

Answer:

Nobody can know the future, but based on current AI trends (July 2026), these are my highest-probability predictions for the next ~6 months.

## 1. AI models: capability keeps moving, but efficiency becomes the battlefield

**Prediction: high confidence**

The next wave will not just be "bigger models".

The competition shifts toward:

* lower inference cost
* better reasoning per FLOP
* agent reliability
* long-context efficiency
* multimodal models
* custom models for vertical domains

The pattern:

```
GPT-3 era:
more parameters → better intelligence

GPT-4/5 era:
better post-training → better reasoning

2026:
better systems engineering → better agents
```

Expect more:

* small reasoning models beating old large models
* distillation from frontier models into 7B–70B models
* MoE everywhere
* inference optimization becoming a core advantage

DeepSeek's approach is likely to influence many labs:

```
training tricks
+
architecture optimization
+
hardware efficiency
+
open models
=
competitive advantage
```

---

## 2. NVIDIA CUDA moat weakens slowly, not suddenly

**Prediction: medium-high confidence**

CUDA will not disappear in 6 months.

But the ecosystem will become more fragmented:

```
CUDA
 |
 +-- ROCm (AMD)
 |
 +-- Huawei CANN
 |
 +-- TPU stack
 |
 +-- custom accelerators
 |
 +-- Triton / MLIR / OpenXLA
```

The important change:

Before:

```
GPU company wins
```

Now:

```
hardware + compiler + kernel + distributed runtime + model stack wins
```

The biggest opportunity is probably not making another GPU.

It is:

```
AI compiler
+
agent infrastructure
+
model optimization
```

---

## 3. Local AI hardware becomes more interesting

**Prediction: high confidence**

The market will move toward:

```
cloud H100/H200/B200
        |
        |
        v

local workstation AI
```

More developers will own:

* RTX 5090-class cards
* 48GB workstation GPUs
* multi-GPU home servers

because models are becoming personal infrastructure.

Your previous thinking about:

> multi GPU AI workstation

is aligned with this trend.

The bottleneck becomes:

```
VRAM
memory bandwidth
interconnect
software optimization
```

not raw TFLOPS.

---

## 4. AI agents will disappoint and then become useful

**Prediction: high confidence**

2025-early 2026:

"Agents will replace everyone"

Reality:

many agents fail because:

```
LLM reasoning
+
tools
+
memory
+
planning
+
verification
```

are still unreliable.

Next 6 months:

More successful agents will be narrow:

Examples:

```
AI coding agent
AI customer support agent
AI research assistant
AI data analyst
AI internal automation
```

Not:

"general autonomous employee".

---

## 5. Software engineering changes faster

**Prediction: very high confidence**

The developer workflow:

2024:

```
human writes code
AI completes code
```

2026:

```
human designs system
AI writes implementation
AI runs tests
AI fixes bugs
human reviews architecture
```

The valuable engineer becomes:

```
architecture
+
debugging
+
AI orchestration
+
domain knowledge
```

People who only write CRUD code are under pressure.

---

## 6. Your personal trajectory (based on your current direction)

Your strongest asset:

You are not only using AI.

You are doing:

```
training models
+
GPU experiments
+
compiler/kernel interest
+
agent development
+
backend engineering
```

That combination is rare.

The next 6 months are likely best spent on:

### A. Build public proof

Examples:

```
github.com/lzwjava/xxx

- train GPT-style model
- CUDA/Triton kernels
- agent framework
- local inference benchmark
```

Your blog traffic already shows there is audience.

Technical writing compounds.

---

### B. Move from "AI learner" → "AI infrastructure engineer"

The valuable layer:

```
Application
   |
Agent framework
   |
Inference engine
   |
Compiler/kernel
   |
GPU hardware
```

You already understand application.

The next step is deeper:

* vLLM internals
* Triton kernels
* CUDA graphs
* distributed training
* quantization
* MoE routing

---

### C. Potential business opportunity

Small AI companies will need:

```
cost reduction
+
private deployment
+
agent integration
+
model fine-tuning
```

A 1–5 person AI engineering consultancy can capture this.

The market is large enough.

---

## My probability table for next 6 months

| Event                                    | Probability |
| ---------------------------------------- | ----------: |
| Open models become much stronger         |         90% |
| AI inference cost drops significantly    |         90% |
| Agents improve but don't replace workers |         85% |
| More local AI hardware adoption          |         80% |
| CUDA loses some share                    |         70% |
| Another "ChatGPT moment" model release   |         60% |
| Fully autonomous software engineer       |        <20% |
| New AI startups creating huge value      |         80% |

---

The biggest opportunity I see:

```
2026-2030

AI infrastructure becomes the new web stack.

The winners are not only model creators.

They are the people who make models:
- cheaper
- faster
- deployable
- useful
```

Your current direction (small model training + GPU + agents + backend) is close to that layer. The next 6 months are likely more about **shipping artifacts and accumulating leverage** than learning more theory.