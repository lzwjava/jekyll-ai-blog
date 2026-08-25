---
audio: false
generated: true
image: false
lang: en
layout: post
title: Execution Sprint Focus Plan
translated: false
type: note
---

Question: **What should I focus on during the next few weeks?**

Answer:

I’d make the next **3–4 weeks an execution sprint**, not a period of broad exploration. You already have several potentially important directions—AI engineering, your AI company, Hong Kong, and the 2027 US master’s path. The danger is spending all day researching each one without producing assets.

### 1. Make AI engineering your main technical track

Your strongest differentiator is not another generic software project. It is:

> **software engineer → LLM training/inference/AI infrastructure engineer**

Spend roughly **50% of your time** here.

Build one serious public artifact:

```text
nano-vllm
    ↓
understand every forward-pass component
    ↓
implement / modify KV cache
    ↓
continuous batching
    ↓
paged attention
    ↓
benchmark
    ↓
write technical notes
```

Given that you've already trained GPT-2 and worked with nanochat/nano-vLLM, I'd go deeper rather than starting another model.

Target by late September:

* one clean AI-infra repo
* benchmarks
* architecture diagram
* 2–4 deep technical notes
* reproducible GPU experiments
* something you can show an AI-infra hiring manager

That is much more valuable than ten small demos.

---

### 2. Turn your existing work into a public portfolio

You already have unusually strong raw material:

* GPT-2 124M trained from scratch
* 760M-scale training experience
* FineWeb experiments
* PyTorch/CUDA/ROCm/GPU work
* inference work with vLLM/Ollama
* your own CLI agents
* years of production backend engineering

The missing piece is **compression into evidence**.

For example:

```text
lzwjava.github.io
├── Training GPT-2 124M from scratch
├── What I learned implementing KV cache
├── Building a tiny vLLM
├── 4070 GPU training experiments
└── AI infrastructure notes
```

You don't need to invent another project.

**Package what you've already done.**

---

### 3. Continue the Hong Kong/QMAS investigation, but put a hard time box on it

You've recently spent a lot of energy on Hong Kong:

* QMAS
* whether a job is required
* family application
* documents
* Hong Kong company
* business endorsement
* right to live/work
* software consultancy

I would **finish the QMAS application preparation this week** rather than continuing to research indefinitely.

Create a concrete state:

```text
QMAS
├── eligibility
├── documents
├── translations
├── scans/PDFs
├── application
└── submit
```

Then stop researching unless immigration sends you something requiring action.

The Hong Kong company can be a **parallel business experiment**, but don't confuse:

```text
HK company
≠
HK immigration status
```

You've already identified this distinction correctly.

---

### 4. Spend some time getting actual AI customers

This is the other major thing I'd push.

Your company shouldn't remain:

```text
"I can build AI agents / train models / do AI consulting"
```

Turn it into:

```text
problem → customer → paid project → case study
```

Even **one RMB 20k–50k AI engineering project** is valuable.

I'd spend perhaps **20% of your time** talking to potential customers, especially around things you already know how to ship:

* internal AI agents
* LLM integration
* private deployment
* inference optimization
* model fine-tuning
* AI automation
* GPU/LLM infrastructure

Don't build a SaaS product yet unless customer conversations reveal a repeated problem.

---

### 5. Keep the US master's path alive, but don't let it consume your weeks

The 2027 master's path is strategically useful because your lack of a traditional bachelor's degree can create an HR filter even though your actual engineering experience is strong.

But right now the highest-return activity isn't reading 100 university pages.

Do the minimum necessary:

```text
2027 US Master's
    ├── shortlist programs
    ├── verify admission requirements
    ├── prepare transcripts
    ├── prepare English test materials
    └── application timeline
```

Then return to engineering.

The master's is a **credential/immigration bridge**. Your technical reputation still has to come from your actual work.

---

## My allocation for the next 4 weeks

| Area                               |    Time |
| ---------------------------------- | ------: |
| LLM / AI infrastructure deep work  | **40%** |
| Public technical portfolio         | **20%** |
| AI consulting/customer acquisition | **20%** |
| QMAS / HK execution                | **10%** |
| US master's preparation            | **10%** |

And I'd impose one rule:

> **Every week must produce something externally visible or irreversible.**

For example:

**Week 1**

* finish KV-cache/vLLM deep dive
* publish one technical note
* organize QMAS documents

**Week 2**

* implement/modify an inference component
* benchmark it
* publish results
* start contacting potential AI clients

**Week 3**

* build the next AI-infra component
* publish another deep technical article
* advance QMAS/application

**Week 4**

* polish the repo
* publish a comprehensive write-up
* have actual customer conversations
* finalize the next immigration/education step

The key is that by the end of September you should have **more evidence, more technical depth, and ideally more revenue**, rather than simply knowing more about possible futures.

Your current situation actually has a pretty strong shape:

```text
11 years software engineering
        +
real product/revenue experience
        +
LLM training
        +
AI infrastructure
        +
AI consulting/company
        +
public technical work
        ↓
AI Engineer / AI Infra Engineer
        ↓
HK / Singapore / US opportunities
        ↓
2027 Master's as credential + immigration leverage
```

So I would **stop optimizing the map for a few weeks and start moving on the path**.
