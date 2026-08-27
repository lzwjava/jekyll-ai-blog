---
audio: false
generated: true
image: false
lang: en
layout: post
title: Yotta Labs Founder and Status
translated: false
type: note
---

## Question: Who is the founder of Yotta Labs (yottalabs.ai), and how is the company doing?

![Image](https://images.openai.com/static-rsc-4/hwu-5VuYZ9wycyE1YcK9LQoXjxtOApezQIGfPcAGWgjhUUjpsjRyswS1pwkJAVlV4w2UoBPxLypvx8nqlW4Co82PjRKu0Dz8BxLLjaLLhw1bMYgpzbWgwmSeumNHXlXmR2R7LQxaHiPKdsYmNXF98R00Oz9LgJ8CHJQkxOigVJtyqEWUK3CEimRdnZ5YZodS?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/poBG_dz0YTEJCcpIwYh2qZpQmBi8AQFPLkkkuzLxPPO6nJXXdU9NoeEvjEgMoTWB1xzN22XbvQvq4OpVlIgl2hqhtwxRD0UJPlONJZnnCUFgX9XeTooqyZJg4xhi9AFlN-BLP4UKZFP_GGxyyJgc1ckWhMk2tvBupI7lonv_cVu4bT0UJclQZLVgfRoogWyk?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/snXD4wO_enKyYPguDgwUHZ0Az395qqtZbD6ys4DQF4fKNDUgdXTG0HMy4s2tCJjLSaHZyUyWux36NKOYuCayngJD2jDzhTOi-jVESq7a_KFGer5w52AahIr73xug8izsi2J72mKAy-NPs5_4uSVZJR_zF7TtAF9eXe2naBUBi6c9wHoVu3uwRgoKbGx8WNVw?purpose=fullsize)

**Yotta Labs** (not to be confused with India's Yotta data center company or Yotta fintech) is a Seattle-based AI infrastructure startup building a **GPU cloud + AI orchestration layer**. ([Crunchbase][1])

### Founders / team

According to company profiles:

* **Da Li** — Founder / CEO
* **Johnny Liu** — Co-founder / CTO
* **Dong Li** — Chief Scientist / co-founder listed in some profiles ([Crunchbase][1])

The team is very small (roughly single digits). LinkedIn lists Yotta Labs as a 2–10 person company headquartered in Seattle. ([LinkedIn][2])

The technical background is interesting:

* Johnny Liu focuses on large-scale ML systems and HPC. ([Crunchbase][3])
* The company emphasizes GPU kernels, heterogeneous hardware, and multi-silicon execution (NVIDIA, AMD, AWS Trainium/Inferentia). ([Yotta Labs][4])

---

## What are they building?

The thesis:

> AI compute will become fragmented, not just "NVIDIA GPU everywhere".

Today:

```
AWS
 ├── NVIDIA
 ├── Trainium

Azure
 ├── NVIDIA
 └── AMD

Google Cloud
 └── TPU

Other GPU clouds
 └── mixed GPUs
```

Every hardware vendor has:

* different drivers
* different kernels
* different scheduling
* different economics

Yotta wants to become the **Kubernetes-like abstraction layer for AI compute**.

Their positioning:

```
                 AI Application
                       |
                 Yotta Layer
                       |
        --------------------------------
        |              |               |
     NVIDIA          AMD          Trainium
     H100            MI300        AWS ASIC
```

They call it an "AI infrastructure OS" / execution layer. ([Yotta Labs Documentation][5])

Products:

* GPU cloud instances
* inference serving
* AI gateway
* workload orchestration
* quantization / optimization tools ([Yotta Labs][6])

---

## How strong is the company?

My assessment:

### Strengths

### 1. The problem is real

This is a very good timing.

In 2023–2026:

* NVIDIA dominates, but supply is constrained.
* AMD MI300/MI350, AWS Trainium, Google TPU are improving.
* Enterprises don't want to rewrite everything per accelerator.

The infrastructure layer is genuinely becoming complicated.

Similar historical patterns:

* VMware abstracted servers
* Kubernetes abstracted containers
* CUDA abstracted GPUs

AI may need another abstraction layer.

---

### 2. Technical direction is deep

Many GPU clouds are basically:

```
buy GPUs
+
rent GPUs
+
nice dashboard
```

That is a commodity business.

Yotta is trying to go deeper:

```
compiler/runtime/kernel/scheduler layer
```

This is much harder and potentially more valuable.

Their docs emphasize hardware-aware scheduling and execution abstraction. ([Yotta Labs Documentation][5])

---

### Weaknesses / risks

### 1. Extremely competitive

They are fighting:

* CoreWeave
* Together AI
* Lambda
* hyperscalers

CoreWeave especially has huge capital and GPU supply advantages.

---

### 2. Platform risk

The question is:

> Will AI companies need a neutral abstraction layer?

Possible futures:

**Scenario A: NVIDIA keeps winning**

Everyone uses CUDA.

Then Yotta's value decreases.

**Scenario B: hardware becomes fragmented**

Then Yotta's thesis becomes much stronger.

---

### 3. Small company

Compared with CoreWeave:

```
CoreWeave:
- billions raised
- huge GPU clusters

Yotta:
- seed-stage
- tiny team
```

Crunchbase lists Yotta as seed-stage with a small employee count. ([Crunchbase][1])

---

## My view from an engineering perspective

I actually think this is one of the more interesting AI infra directions.

The analogy:

1990s:

```
Hardware
   |
Operating System
   |
Applications
```

2020s AI:

```
GPU/ASIC
   |
AI Runtime + Scheduler
   |
Models
   |
Applications
```

The winner may not be the company owning the most GPUs, but the company making heterogeneous compute easy.

This is similar to why NVIDIA CUDA became powerful: not because GPUs were magical, but because software developers stopped thinking about hardware details.

---

For someone like you (training GPT-2, playing with MI300X/ROCm, DeepSpeed, GPU repair), Yotta's area is actually close to your intersection:

```
hardware
   +
distributed training
   +
LLM inference
   +
systems engineering
```

The interesting technical questions are:

* Can they schedule H100 + MI300 + Trainium efficiently?
* Can they automatically choose kernels?
* Can they make PyTorch/vLLM/SGLang portable?
* Can they beat simply using AWS?

Those are very hard engineering problems.

References:

* Yotta Labs About: ([Yotta Labs Documentation][5])
* Crunchbase company profile: ([Crunchbase][1])
* Yotta inference architecture: ([Yotta Labs][4])
* Yotta official site: ([Yotta Labs][6])

[1]: https://www.crunchbase.com/organization/yotta-labs?utm_source=chatgpt.com "Yotta Labs - Crunchbase Company Profile & Funding"
[2]: https://www.linkedin.com/company/yotta-labs?utm_source=chatgpt.com "Yotta Labs | LinkedIn"
[3]: https://www.crunchbase.com/person/johnny-liu-24d9?utm_source=chatgpt.com "Johnny Liu - Crunchbase Person Profile"
[4]: https://www.yottalabs.ai/inference?utm_source=chatgpt.com "Inference Optimized Across All AI Silicon | Yotta Labs"
[5]: https://docs.yottalabs.ai/?utm_source=chatgpt.com "About | Yotta Labs"
[6]: https://www.yottalabs.ai/?utm_source=chatgpt.com "GPU Cloud for AI Training & Inference | Yotta Labs"
