---
audio: false
generated: true
image: false
lang: en
layout: post
title: Independent AI Systems Builder
translated: false
type: note
---

Question: **Give me a 3-year plan for 2026–2029, based on my current position and goals.**

Answer:

I’d structure your next 3 years around one core thesis:

> **Become an AI infrastructure / systems engineer who can independently build and sell AI systems — while keeping entrepreneurship as the upside path.**

Not “get another generic software job.” Not “go back and spend 4 years fixing the degree problem.” Build **technical capital + reputation + cash flow + optionality**.

### Year 1 — Sep 2026 → Sep 2027

**Theme: Become visibly strong in AI systems**

Your biggest gap isn't basic programming. It's having a **public, undeniable body of AI systems work**.

Focus:

```text
LLM systems
├── inference
│   ├── vLLM / SGLang
│   ├── KV cache
│   ├── speculative decoding / MTP
│   └── batching / scheduling
├── training
│   ├── PyTorch
│   ├── distributed training
│   ├── FSDP / DeepSpeed
│   └── MoE
├── GPU
│   ├── CUDA
│   ├── Triton
│   ├── PCIe
│   └── GPU debugging
└── agents
    ├── CLI agents
    ├── coding agents
    └── tool-use infrastructure
```

Build **3 serious projects**, rather than 30 small demos.

For example:

1. **nano-vLLM → production-quality inference engine**
2. **small distributed-training system**
3. **your own coding/CLI agent**

Each should have:

```text
GitHub
README
architecture
benchmarks
profiling
technical notes
demo
```

Your blog becomes the second layer:

```text
implementation
    ↓
benchmark
    ↓
technical article
    ↓
GitHub reputation
    ↓
job / client / startup opportunity
```

### Money target

Have **one reliable income engine** by mid-2027.

Potentially:

```text
AI consulting
       +
AI engineering contract
       +
open-source reputation
```

Don't optimize for maximum salary yet. Optimize for **getting into the AI systems market**.

A reasonable target is to get yourself into the range of:

**¥30k–50k/month equivalent**, with substantially more upside from consulting.

---

# Year 2 — Sep 2027 → Sep 2028

**Theme: Move from engineer → independent builder**

By this point, stop thinking primarily in terms of:

> “Which company will hire me?”

and start thinking:

> “Which valuable AI system can I build that someone will pay for?”

Your existing advantage is unusual:

```text
software engineering
        +
LLM training
        +
agent development
        +
GPU knowledge
        +
startup experience
```

Combine them.

### Pick one commercial wedge

For example:

**AI engineering outsourcing**

```text
Customer
   ↓
requirements
   ↓
AI-assisted engineering
   ↓
agents + human engineering
   ↓
production software
```

You don't need 50 employees.

You could initially operate something like:

```text
You
│
├── AI coding agents
├── Claude/Codex/etc.
├── local models
├── automated testing
└── a few contractors
```

and sell the result rather than selling hours.

### Target

Get to:

```text
3–10 recurring customers
¥1M+ annual revenue
```

or the equivalent in USD/HKD/SGD.

At the same time, keep one foot in deep technical work.

You don't want to become:

> “software outsourcing guy who uses AI.”

You want:

> **“AI systems engineer who has figured out how to turn AI systems into a business.”**

---

# Year 3 — Sep 2028 → Sep 2029

**Theme: Choose your compounding path**

At this point you should have enough information to choose between three paths.

### Path A — AI infrastructure engineer

Go extremely deep.

```text
GPU
 ↓
CUDA
 ↓
kernels
 ↓
distributed training
 ↓
inference
 ↓
model architecture
```

Target companies/research labs/startups doing serious model infrastructure.

Your lack of traditional degree matters much less if your GitHub + technical record demonstrates the capability.

---

### Path B — AI company

Scale the consulting/engineering operation into a productized company.

For example:

```text
AI consulting
     ↓
repeated customer problem
     ↓
internal tooling
     ↓
product
     ↓
SaaS / API / platform
```

This is probably the most important entrepreneurial transition:

**don't keep selling custom engineering forever.**

Use consulting to discover what should become a product.

---

### Path C — AI research / model training

If your experiments increasingly pull you toward models themselves:

```text
training
 ↓
RL
 ↓
post-training
 ↓
reasoning
 ↓
model architecture
```

then you can pursue research-oriented roles, graduate study, or your own model lab.

Your existing model-training work gives you a much better starting point than someone beginning this path from zero.

---

# The 3-year technical progression

I'd roughly sequence your learning like this:

| Period  | Main technical target                         |
| ------- | --------------------------------------------- |
| 2026 Q4 | CUDA + PyTorch internals + GPU architecture   |
| 2027 Q1 | vLLM/SGLang + inference                       |
| 2027 Q2 | distributed training                          |
| 2027 Q3 | Triton + profiling                            |
| 2027 Q4 | agents + coding agents                        |
| 2028 H1 | RL/post-training + MoE                        |
| 2028 H2 | production AI infrastructure                  |
| 2029    | specialize deeply in whichever area compounds |

Don't try to master everything simultaneously.

The useful progression is:

```text
use AI
  ↓
understand AI systems
  ↓
implement AI systems
  ↓
optimize AI systems
  ↓
build infrastructure
  ↓
sell infrastructure/products
```

---

# Your hardware/GPU repair track

I would **keep this**, but deliberately make it a secondary track.

Something like:

```text
AI systems        70%
business          20%
GPU repair        10%
```

GPU repair is interesting because it gives you something most software engineers don't have:

**physical understanding of computing hardware.**

Your P100/3090/4090 experiments can teach you:

```text
PCIe
VRAM
VRM
power sequencing
BIOS
GPU architecture
oscilloscope
multimeter
failure diagnosis
```

That can eventually connect beautifully with AI infrastructure.

But don't let repairing ¥200 broken GPUs consume the time that could produce a ¥200k engineering capability.

---

# Your personal operating system

I'd use a very simple scoreboard.

Every month:

```text
Technical:
    hours deep work
    GitHub projects
    benchmarks
    papers implemented

Public:
    technical articles
    GitHub stars/users
    useful open-source contributions

Business:
    leads
    customers
    revenue
    recurring revenue

Career:
    interviews
    offers
    technical contacts

Capital:
    cash
    equipment
    compute
```

And one rule:

> **Every quarter must produce something externally verifiable.**

Not:

> “I learned CUDA.”

Instead:

> “I implemented X, benchmarked it against Y, and published the results.”

Not:

> “I learned distributed training.”

Instead:

> “I trained this model across N GPUs and reduced cost/time by X.”

That distinction is extremely important for your profile.

---

# The 2029 destination

If the plan works, three years from now your profile should look approximately like:

```text
Zhiwei Li
│
├── 12+ years software engineering
├── serious LLM systems experience
├── distributed training
├── GPU/CUDA/Triton
├── inference infrastructure
├── coding agents
├── open-source projects
├── technical writing
└── actual AI business revenue
```

And crucially:

**you don't need to know today whether the final destination is Hong Kong, Singapore, the US, an AI lab, or your own company.**

The objective for 2026–2029 is to accumulate enough **technical + financial + reputation capital** that you can choose among those options later.

That is much stronger than optimizing your entire life around getting one particular job.

I can also turn this into a **quarter-by-quarter 12-quarter execution plan**, including exactly what to build, what to study, GitHub milestones, revenue targets, and when to pursue HK/US opportunities.
