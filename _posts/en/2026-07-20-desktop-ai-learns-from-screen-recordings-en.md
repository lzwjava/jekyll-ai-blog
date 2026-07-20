---
audio: false
generated: true
image: false
lang: en
layout: post
title: Desktop AI Learns from Screen Recordings
translated: false
type: note
---

Question: What is this AITNT article about?
[https://m.aitntnews.com/newDetail.html?newId=26238](https://m.aitntnews.com/newDetail.html?newId=26238)

Answer:

This article is about **Agivar**, a desktop AI Agent released by **非十科技 (Fitten Tech)**. The core idea: instead of humans writing complex prompts to tell AI how to operate software, you **show the AI how you work once (screen recording), and it learns the workflow and repeats it**. ([AI TNT][1])

The article frames it as an attempt to replace part of the work currently done by **FDE (Forward Deployed Engineer)** roles. FDEs are engineers who go into companies, understand messy business processes, and translate human workflows into AI automation. The article claims Agivar tries to automate that translation step. ([AI TNT][1])

## Core mechanism

Traditional RPA:

```
human
 |
 | define exact clicks
 v
automation script
 |
 v
computer
```

Example:

```python
click(300,500)
type("invoice number")
click(submit)
```

Very brittle.

Agivar's proposed workflow:

```
human demonstrates task
        |
        v
screen recording
        |
        v
AI observes:
 - UI elements
 - user intention
 - sequence
 - conditions
        |
        v
AI creates executable workflow
        |
        v
runs task repeatedly
```

The article says it does not simply memorize coordinates like old "按键精灵"; instead it attempts to understand the task logic behind the actions. ([AI TNT][1])

---

## Architecture idea

The interesting technical part is the "brain + cerebellum" architecture:

```
              User goal
                  |
                  v
          Large Multimodal Model
              ("brain")
                  |
      planning / reasoning / recovery
                  |
                  v
          Small specialized model
             ("cerebellum")
                  |
      vision + clicking + typing
                  |
                  v
             Desktop OS
```

The article claims:

* Large model:

  * understands videos
  * decomposes tasks
  * handles exceptions

* Small model:

  * recognizes UI
  * executes mouse/keyboard operations
  * provides low latency

([AI TNT][1])

This is actually a very reasonable architecture. You don't want GPT-5-class reasoning for every mouse movement.

Similar analogy:

```
Human:
  cortex      -> "drive from Guangzhou to Shenzhen"
  cerebellum  -> "control steering wheel"

Agent:
  LLM        -> "finish invoice processing"
  small VLM  -> "click this button"
```

---

## Why this is interesting

The biggest bottleneck for enterprise AI is not model intelligence.

It is:

> "How do we connect AI to thousands of ugly internal systems?"

Many companies have:

* old ERP
* internal web apps
* no API
* manual Excel workflows
* government portals
* banking systems

Normal API automation cannot work.

Desktop Agent attacks this layer:

```
No API
 |
 v
Vision + Computer Use
 |
 v
AI employee
```

This is the same direction as:

* OpenAI Computer Use
* Anthropic Claude Computer Use
* Browser-use
* Operator-style agents

The article mentions Claude Cowork and OpenAI Codex desktop agents as part of this broader trend. ([AI TNT][1])

---

## My technical evaluation

The idea is real, but the hard parts are:

### 1. Reliability

LLMs are stochastic.

For a demo:

```
AI clicks button correctly 95%
```

looks amazing.

For enterprise:

```
10000 invoices/day
99.99% correctness required
```

is much harder.

The article mentions:

* multi-agent verification
* rule constraints
* specialized training

to improve determinism. ([AI TNT][1])

---

### 2. Learning workflows from videos

This is basically:

```
video -> action sequence -> latent program
```

A very interesting research direction.

Possible pipeline:

```
screen video
    |
    v
vision encoder
    |
    v
UI state extraction
    |
    v
trajectory modeling
    |
    v
workflow graph
    |
    v
executor
```

It is close to:

* imitation learning
* GUI agents
* multimodal foundation models

---

### 3. The "AI FDE" concept

This is probably the strongest business insight.

Today:

```
Company wants AI automation

        |
        v

Hire consultant/FDE

        |
        v

Engineer studies workflow

        |
        v

Build agent
```

Future:

```
Employee records workflow

        |
        v

AI learns workflow

        |
        v

Agent deployed
```

This reduces deployment cost dramatically.

---

## Relationship to your "multi-agent factory" idea

This is actually very aligned with your previous "AI employee factory" thinking.

A future company could look like:

```
Human expert
     |
     | demonstrate work
     v
Workflow-learning agent
     |
     v
100 copies of AI workers
     |
     v
business output
```

The bottleneck moves from:

> hiring workers

to:

> collecting demonstrations and improving agents.

---

## About Fitten Tech

非十科技 is the company behind:

* Fitten Code (AI coding assistant)
* Agivar desktop agent

The article states the team originated from Tsinghua Computer Science and Jittor deep learning framework development. ([AI TNT][1])

---

My take: **Agivar is not mainly a "better chatbot"; it is an attempt to build the next layer after LLMs: operational agents that learn human workflows.** The key battle will be reliability, latency, and enterprise integration rather than raw model intelligence.

References:

* AITNT article: ([AI TNT][1])
* AITNT platform overview: ([aitntnews.com][2])

[1]: https://m.aitntnews.com/newDetail.html?newId=26238 "

非十科技推出桌面智能体Agivar，从替代年薪300万的前沿部署工程师

"
[2]: https://www.aitntnews.com/?utm_source=chatgpt.com "AITNT-让一部分人先用AI实现商业化"
