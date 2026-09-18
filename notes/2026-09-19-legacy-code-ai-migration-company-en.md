---
audio: false
generated: true
image: false
lang: en
layout: post
title: Legacy Code AI Migration Company
translated: false
type: note
---

Question: Given my background and future direction, what startup idea fits me best?

Answer:

Your strongest startup opportunity is **not “another AI app.”** Your edge is the intersection of:

* 12 years of engineering + ability to ship alone
* Deep LLM/agent curiosity
* Real experience with **AI coding agents / CLI agents**
* Model training and inference infrastructure
* Experience selling software/consulting
* Chinese + international market exposure
* Willingness to work very hands-on with GPUs and infrastructure
* You already have an audience/distribution asset through your technical writing and AI community

I would structure your opportunities like this:

| Idea                                          |   Fit |  Capital | Time to revenue | Long-term upside |
| --------------------------------------------- | ----: | -------: | --------------: | ---------------: |
| **AI Engineering Agent for companies**        | ★★★★★ |      Low |            Fast |            ★★★★★ |
| **AI-native software outsourcing → product**  | ★★★★★ |      Low |       Very fast |            ★★★★☆ |
| **LLM inference/optimization infrastructure** | ★★★★☆ |   Medium |          Medium |            ★★★★★ |
| **GPU repair / GPU lab business**             | ★★★☆☆ |      Low |            Fast |            ★★★☆☆ |
| AI knowledge/search website                   | ★★★☆☆ | Very low |            Slow |            ★★★☆☆ |
| Consumer AI app                               | ★★☆☆☆ |   Medium |       Uncertain |            ★★★★☆ |

## 1. My strongest suggestion: an AI Engineering Company that gradually becomes a product

Think:

> **“Give us a legacy codebase. Our agents understand it, modify it, test it, migrate it, and maintain it.”**

This matches something unusually valuable in your background: you've actually lived inside large enterprise codebases.

For example:

```text
Customer
   │
   ▼
Git repository
   │
   ├── Java / Spring
   ├── SQL / DB2
   ├── Angular
   ├── Jenkins
   ├── WebSphere
   └── thousands of docs/scripts
          │
          ▼
     Agent system
          │
    ┌─────┼─────────┐
    ▼     ▼         ▼
Understand  Modify   Verify
    │       │         │
    └───────┼─────────┘
            ▼
       Pull Request
            │
            ▼
       CI / tests
```

The important part is **not the LLM**.

The moat is the engineering system around it:

```text
repo indexing
     +
code graph
     +
dependency analysis
     +
agent planning
     +
tool execution
     +
test generation
     +
CI verification
     +
human approval
```

You could start as a service:

> “We reduce the engineering cost of maintaining old enterprise systems using autonomous coding agents.”

Then observe which jobs repeat.

Eventually:

```text
consulting
   ↓
repeatable workflow
   ↓
internal agent platform
   ↓
SaaS / enterprise product
```

This is much more realistic for you than trying to invent a consumer product from zero.

---

# 2. An even more interesting niche: Legacy → AI migration

There is an enormous amount of software that looks like:

```text
Java
Spring
WebSphere
Oracle / DB2
Angular
Jenkins
Ansible
shell scripts
Excel
PDF documentation
```

The software isn't economically attractive enough for humans to rewrite manually.

That creates an interesting equation:

```text
old software
     +
expensive engineers
     +
LLMs
     +
automated verification
     ↓
AI migration company
```

Examples:

### Java modernization

```text
WebSphere
    ↓
Spring Boot
    ↓
Docker
    ↓
Kubernetes
```

### Angular modernization

```text
AngularJS
   ↓
modern Angular
```

### Documentation reconstruction

```text
10,000 source files
       ↓
AI
       ↓
architecture map
API documentation
dependency graph
runbooks
test cases
```

### Test generation

```text
legacy code
    ↓
agent
    ↓
unit tests
integration tests
regression tests
    ↓
CI
```

Your previous enterprise experience gives you something that a 22-year-old AI startup founder usually doesn't have:

**you know what this mess actually looks like.**

That is a genuine founder advantage.

---

# 3. Your second path: AI-native outsourcing

You have previously explored an AI software outsourcing company. I think this is actually a strong bootstrap path.

But don't build:

> “a normal outsourcing company with ChatGPT.”

Build:

> **a company where AI agents are the production machinery.**

Suppose a normal software company has:

```text
10 engineers
$1M/year payroll
```

Your company might eventually have:

```text
2 humans
+
20 specialized agents
+
CI/CD
+
GPU/API infrastructure
```

For example:

```text
customer request
      ↓
PM agent
      ↓
architect agent
      ↓
coding agents
      ↓
review agents
      ↓
test agents
      ↓
deployment agent
      ↓
human approval
```

The customer buys the **outcome**, not the agents.

That's important.

Don't sell:

> “We use Claude/Codex/GPT.”

Sell:

> “We deliver this software system for $30k.”

Your gross margin comes from increasing the amount of engineering work one human can supervise.

---

# 4. A potentially huge technical bet: inference infrastructure

This one fits your technical interests particularly well.

You are already interested in:

* vLLM
* SGLang
* KV cache
* speculative decoding
* MTP
* MoE
* Triton
* CUDA
* GPU clusters
* model training
* inference economics

You could build an **LLM inference optimization company**.

For example:

```text
Company has
    ↓
20 GPUs
    ↓
$100k/month inference bill
    ↓
your system
    ↓
profiling
quantization
batching
KV optimization
speculative decoding
model routing
GPU utilization
    ↓
$60k/month
```

You charge based on:

```text
20% of savings
```

rather than:

```text
$X/user/month
```

That makes the ROI extremely easy to explain.

The difficult part is sales and access to sufficiently large inference workloads.

So I'd treat this as a **second-stage company**, not necessarily your first startup.

---

# 5. Your GPU repair idea is interesting—but I would not make it your primary startup

Your GPU repair experiments are valuable because they teach you:

```text
PCB
 ↓
power rails
 ↓
VRM
 ↓
PCIe
 ↓
VRAM
 ↓
GPU
```

And you are actually willing to buy broken hardware, measure it, and learn.

That's rare.

But the business ceiling is different.

A repair business tends to be:

```text
your time
   ↓
diagnosis
   ↓
repair
   ↓
money
```

Whereas an AI infrastructure company can become:

```text
software
   ↓
10 customers
   ↓
100 customers
   ↓
1000 customers
```

So I would use GPU repair as a **technical laboratory / cash-flow side business**, not necessarily the central company.

---

# 6. Your AI knowledge/search site is useful—but mostly as distribution

You have another unusual asset:

```text
AI notes
+
technical blog
+
community
+
GitHub
+
CLI tools
```

Don't think of that primarily as an advertising website.

Think:

> **distribution.**

For example:

```text
lzwjava.com
     ↓
AI engineering articles
     ↓
GitHub projects
     ↓
developers
     ↓
OSS agent
     ↓
enterprise users
     ↓
paid product
```

This is much more powerful than:

```text
SEO article
 ↓
AdSense
 ↓
$0.02
```

Your technical content can become the marketing department of the startup.

---

# 7. There is a common theme across all of these

I wouldn't build five unrelated businesses.

I'd build around one thesis:

> **AI should turn expensive software engineering work into an increasingly automated production process.**

Then you can move along this curve:

```text
                 PRODUCT
                   ▲
                   │
            ┌──────┴──────┐
            │ AI platform  │
            └──────▲──────┘
                   │
             internal tools
                   ▲
                   │
             repeatable jobs
                   ▲
                   │
               consulting
                   ▲
                   │
                 sales
```

This is particularly compatible with your current position because you don't need $10M first.

You can start with:

```text
1 founder
+
Claude/Codex/GPT/etc.
+
GitHub
+
a few scripts
+
one customer
```

And progressively turn your own delivery process into software.

---

# 8. What I would personally optimize for in your position

Not valuation first.

I'd optimize for this:

```text
2026
  │
  ├── get customers
  │
  ├── solve painful engineering problems
  │
  ├── build agents internally
  │
  └── collect proprietary workflow knowledge
  │
2027
  │
  ├── identify repeated workflow
  │
  ├── productize it
  │
  └── reduce human labor/customer
  │
2028
  │
  └── software becomes the main business
```

The critical transition is:

**service → software**

not:

**idea → fundraising → startup → hope.**

And I would avoid spending a year building an impressive agent framework before anyone pays for it.

Get the ugly customer problem first.

---

## If I had to choose one

I'd choose:

> **AI agents for enterprise legacy software modernization and maintenance.**

Not because it sounds glamorous, but because your personal graph is unusually aligned:

```text
12yr software engineering
        +
enterprise/legacy systems
        +
LLM agents
        +
coding
        +
AI infrastructure
        +
consulting
        +
technical distribution
        ↓
AI software engineering company
```

That's a much stronger founder-market fit than “I want to build an AI startup.”

The key question I'd investigate next is **which exact $10k–$100k enterprise engineering problem you can solve with 2–5 agents and one human**, because that determines whether this becomes a real company or merely a cool demo.
