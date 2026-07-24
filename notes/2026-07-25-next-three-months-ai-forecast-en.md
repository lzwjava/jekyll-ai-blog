---
audio: false
generated: true
image: false
lang: en
layout: post
title: Next Three Months AI Forecast
translated: false
type: note
---

Question: Predict the next 3 months (from July 24, 2026)

Answer:

For the next 3 months (late July → late October 2026), my prediction based on current AI trends, your trajectory, and the market:

## 1. AI models: smaller + cheaper frontier models accelerate

**High probability**

The biggest shift will not be "bigger models only", but:

* better inference efficiency
* more MoE
* better post-training
* agent architectures
* specialized models

Expect:

* 30B–100B open models approaching today's frontier quality for many tasks
* more local AI deployment
* more companies optimizing cost/token

The DeepSeek lesson continues:

> Algorithmic efficiency becomes a bigger moat than raw GPU count.

Likely winners:

* DeepSeek
* Qwen
* Kimi/Moonshot
* OpenAI
* Anthropic
* Google

## 2. GPU market: VRAM becomes the bottleneck

Your recent GPU discussions are exactly aligned with where things go.

The next 3 months:

* 16GB consumer GPUs become increasingly constrained
* 24GB VRAM becomes the practical minimum for serious local AI
* used RTX 3090 market remains interesting
* AMD ROCm improves but CUDA ecosystem remains dominant

The important metric changes:

2023:

> TFLOPS

2026:

> usable VRAM + memory bandwidth + software stack

A $1000 GPU with 48GB VRAM may beat a $2000 GPU with 24GB for AI developers.

## 3. AI coding agents explode

This is probably the biggest near-term change.

Expect:

* Claude Code style agents everywhere
* OpenAI Codex-style workflows
* terminal-native agents
* autonomous repo modification

The programming workflow:

Before:

```
human
 ↓
write code
 ↓
compile/test
```

After:

```
human
 ↓
specification
 ↓
agent
 ↓
code + tests + debugging
 ↓
human review
```

Your direction with:

* ww
* iclaw
* CLI agents
* agent workflows

is very aligned.

## 4. Open source AI infrastructure grows

Expect more importance around:

* inference engines
* compilers
* kernels
* distributed serving

Examples:

* vLLM
* SGLang
* TensorRT-LLM
* ROCm
* Triton kernels

The "CUDA monopoly" discussion will continue, but replacement happens gradually.

The stack:

```
Model
 ↓
Framework
 ↓
Compiler
 ↓
Kernel
 ↓
Hardware
```

becomes the battlefield.

## 5. AI startups: many small teams become possible

I expect more "2-10 person AI companies".

Because:

2020 startup:

```
10 engineers
backend
frontend
infra
ML
```

2026 startup:

```
2 founders
AI agents
cloud GPUs
open models
```

The bottleneck moves from coding to:

* finding valuable problems
* distribution
* proprietary data

## 6. Your personal trajectory prediction

Given your recent experiments:

* GPT-2 training
* ROCm exploration
* GPU kernels
* agents
* AI consulting direction

I expect your next 3 months likely look like:

### Month 1

More infrastructure learning:

* PyTorch internals
* CUDA/ROCm
* inference optimization
* vLLM/SGLang

Possible:

* another GPU purchase decision

### Month 2

A more concrete AI product:

Examples:

* vertical agent
* AI workflow SaaS
* enterprise automation
* AI consulting demo

### Month 3

More public proof:

* GitHub projects
* blog posts
* technical writeups
* customer acquisition

Your strongest advantage is not competing with OpenAI training a 1T model.

It is:

```
Frontier AI knowledge
+
engineering ability
+
shipping ability
+
cheap compute
```

That combination is rare.

## My probability ranking for the next 3 months:

| Event                                        | Probability |
| -------------------------------------------- | ----------: |
| AI coding agents become mainstream           |         90% |
| Open models improve significantly            |         85% |
| VRAM shortage continues                      |         80% |
| More AI startups emerge                      |         80% |
| CUDA replaced quickly                        |         20% |
| A new DeepSeek-level efficiency breakthrough |         40% |
| Consumer local AI adoption grows             |         70% |

The biggest opportunity window is probably **AI agents + cheap inference + domain workflows**, not training another foundation model from scratch.