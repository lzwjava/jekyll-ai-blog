---
audio: false
generated: true
image: false
lang: en
layout: post
title: Building a Token Factory
translated: false
type: note
---

Question: How to build a "token factory" — a small AI factory where engineers each have 10–20 GPUs/computers and operate as super-agents running many experiments?

Answer:

What you are describing is closer to an **AI research factory / agentic lab** than a traditional software company.

The core idea:

> Human engineers become "research directors".
> Their agents become thousands of virtual researchers.
> GPUs become the experimental production line.
> Tokens are the output.

Think of how semiconductor fabs work:

* TSMC has machines → produces wafers
* AI factory has GPUs → produces tokens, models, experiments, data

A small version could look like this:

```
                 AI Factory

              Founder / Research Lead
                       |
        -----------------------------------
        |                 |               |
    Agent Team A      Agent Team B    Agent Team C

    Data Agent        Training Agent  Eval Agent
    Coding Agent      Debug Agent    Benchmark Agent
    Paper Agent       Infra Agent    Deployment Agent

        |                 |               |

    10 GPUs           10 GPUs          10 GPUs

        |
        v

  Experiments / Models / Datasets / Agents
```

---

## 1. The unit of production is not "employee"

Traditional company:

```
1 engineer
   |
   v
write code
   |
   v
ship feature
```

AI factory:

```
1 engineer
   |
   v
creates agent workforce

20 agents
   |
   v
100 experiments/day
   |
   v
best ideas survive
```

The engineer becomes like a **principal scientist managing a colony**.

---

## 2. Each engineer needs a "personal AI lab"

Example:

```
Engineer workstation:

RTX 5090 x 4
+
server GPU access
+
agent runtime
+
experiment database
```

Software:

```
~/factory/

agents/
    researcher.py
    coder.py
    critic.py
    evaluator.py

experiments/
    exp001/
    exp002/

models/
datasets/
logs/
```

Every experiment automatically records:

```
experiment_id
model_version
dataset
hyperparameters
GPU hours
result
leaderboard score
```

---

## 3. The key is massive parallel experimentation

Humans are bad at trying 100 ideas.

Agents are good.

Example:

You want improve a small LLM.

Human says:

"Try changing attention."

Agent swarm:

```
Agent 1:
  replace attention with MLA

Agent 2:
  increase RoPE theta

Agent 3:
  change tokenizer

Agent 4:
  synthetic data generation

Agent 5:
  curriculum learning

Agent 6:
  optimizer experiments

Agent 7:
  architecture search
```

After 24 hours:

```
Experiment #431
beats baseline +7%

merge
```

This is how AlphaGo-style research works.

---

## 4. Build the "factory operating system"

The most important component is not GPUs.

It is orchestration.

Something like:

```
                Task Queue

                   |
                   v

             Agent Scheduler

                   |
       -------------------------
       |           |           |

    GPU #1      GPU #2      GPU #30

       |
       v

 Experiment Runner

       |
       v

 Results Database

       |
       v

 AI Reviewer
```

Possible stack:

```
Ray
Kubernetes
Slurm
Docker
vLLM
PyTorch
MLflow
Weights & Biases
PostgreSQL
```

But honestly a small company can start simpler:

```
Python
+
SSH
+
Docker
+
SQLite
+
Git
```

---

## 5. The "super-agent employee"

A future AI engineer may look like:

Morning:

```
Human:
"Improve our 7B model for coding."

Agent:

08:00
reads papers

08:30
creates 50 experiment plans

09:00
launches training jobs

12:00
evaluates benchmarks

15:00
writes report

18:00
human reviews top 3 ideas
```

The human spends time on:

* choosing direction
* judging quality
* talking to customers
* architecture decisions

---

## 6. Small OPC version (one-person company)

Actually one person can build a miniature version.

Example:

Hardware:

```
Your PC:
RTX 4070

+
2 x RTX 3090 server

+
cloud GPU when needed
```

Agents:

```
Research Agent
   |
   +-- Paper reading

Coding Agent
   |
   +-- Implementation

Training Agent
   |
   +-- GPU jobs

Critic Agent
   |
   +-- Finds problems

Marketing Agent
   |
   +-- Writes content
```

Your daily output:

```
10 experiments
3 blog posts
2 open-source contributions
1 product iteration
```

---

## 7. The biggest bottleneck will change

Today:

```
GPU shortage
```

Future:

```
attention shortage
```

Everybody will have agents.

The advantage becomes:

Who has the best:

* experiment loop
* evaluation system
* taste
* data pipeline
* customer feedback

---

Your idea is very close to what many frontier labs are moving toward:

```
Old:
100 researchers + 100 GPUs

New:
10 researchers + 1000 agents + 1000 GPUs
```

The company becomes a **learning machine**.

A good name for this concept would be:

> "AI factory = a self-improving experiment engine that converts compute into intelligence."

The interesting part is that an OPC with strong engineering background can actually build a tiny version today. The first milestone is not 100 GPUs — it is making one agent reliably create, run, evaluate, and improve experiments without you touching every step.
