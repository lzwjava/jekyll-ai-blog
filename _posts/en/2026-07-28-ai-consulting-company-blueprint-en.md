---
audio: false
generated: true
image: false
lang: en
layout: post
title: AI Consulting Company Blueprint
translated: false
type: note
---

## Question: How to build an AI consulting company?

## Answer:

An AI consulting company is basically a **services + engineering + knowledge business**. The core loop is:

```
Find expensive business problem
        ↓
Build AI solution prototype
        ↓
Prove ROI
        ↓
Deploy + maintain
        ↓
Turn into reusable product/service
```

For someone with your background (full-stack + LLM training + GPU infra + agents), the best positioning is not "AI consultant" in a generic sense. It should be:

> "We help companies integrate private AI agents, LLM systems, and AI infrastructure into production."

---

## 1. Pick a narrow wedge first

Bad:

> "We do AI transformation consulting."

Too broad. Every consulting company says this.

Good:

### Option A: Enterprise AI Agent Engineering

Target:

* companies with internal documents
* customer support teams
* sales teams
* operations teams

Deliver:

```
Company Data
    |
    v
RAG pipeline
    |
    v
Private AI Agent
    |
    +-- Slack/WeChat/Teams
    +-- CRM
    +-- ERP
    +-- Database
```

Example projects:

* Internal knowledge assistant
* Customer service agent
* Sales assistant
* Code review agent
* Report generation agent

---

### Option B: LLM Infrastructure Consulting

Your GPU/model experience is valuable.

Many companies don't know:

* which model to choose
* local vs cloud inference
* vLLM deployment
* fine-tuning
* evaluation
* GPU cost optimization

Services:

```
OpenAI / Claude / Gemini
          |
          |
     Model Router
          |
          |
   Private Models
          |
          |
     vLLM Cluster
```

---

### Option C: AI Training / Fine-tuning

Companies have private data:

```
PDF
Database
Chat logs
Tickets
Code
Documents

       |
       v

Fine-tuned model
+
RAG
+
Agent
```

You can sell:

* dataset preparation
* LoRA fine-tuning
* evaluation
* deployment

---

# 2. Build a "consulting product"

Do not sell hours.

Bad:

```
Engineer:
$100/hour
```

Hard to scale.

Better:

```
AI Agent Starter Package

2 weeks

Includes:
- data ingestion
- RAG
- agent workflow
- deployment
- training

Price:
$10k-$30k
```

Then:

```
Monthly AI Operation

$2k-$10k/month

Includes:
- monitoring
- prompt optimization
- model updates
- cost optimization
```

---

# 3. Create demo systems

Consulting sells trust.

Build 3-5 impressive demos.

Example:

## Demo 1: Enterprise Knowledge Agent

Stack:

```
FastAPI
    |
LangGraph / custom agent
    |
Qwen / Claude / GPT
    |
Vector DB
    |
Postgres + pgvector
```

Features:

* upload PDF
* ask questions
* cite sources
* remember users

---

## Demo 2: Coding Agent

Your existing experience helps.

Architecture:

```
User

 |
 v

Agent Planner

 |
 +----> Search code
 |
 +----> Modify files
 |
 +----> Run tests
 |
 +----> Git commit
```

---

## Demo 3: AI Employee System

This matches your Hermes idea.

Multiple agents:

```
              Manager Agent

                   |
     +-------------+-------------+

 Research Agent   Coding Agent   Sales Agent

     |                |              |

 Reports          PRs           Leads
```

The future consulting market will likely involve deploying these "digital employees".

---

# 4. Find first customers

Do not start with large enterprises.

Start:

## Phase 1

Friends/network:

* software companies
* factories
* trading companies
* education companies
* e-commerce

Offer:

> "I will build a working AI prototype in 2 weeks."

Charge:

$3k-$10k first projects.

---

## Phase 2

Turn successful projects into case studies:

Example:

Before:

```
Customer support:
20 people
5000 tickets/month
```

After:

```
AI handles 60%
Response time:
2 hours -> 30 seconds
```

Then sell.

---

# 5. Company structure

Initially:

```
Founder (you)

 |
 +-- AI engineer
 |
 +-- Sales / BD
 |
 +-- Part-time designer
```

Do not hire many people.

AI allows one engineer to deliver what used to require a team.

---

# 6. Technical stack

A practical stack:

```
Frontend:
React / Next.js

Backend:
Python FastAPI

Agent:
LangGraph
or custom state machine

Models:
Claude
GPT
Gemini
Qwen

Inference:
vLLM

Database:
Postgres
pgvector

Deployment:
Docker
Kubernetes

Monitoring:
Langfuse
OpenTelemetry
```

---

# 7. Your unfair advantage

Your background is actually closer to an AI infrastructure company than a normal consultant:

You have:

* distributed systems
* Java/backend
* Linux
* GPU training
* PyTorch
* model experiments
* agent development

Most AI consultants only know:

```
ChatGPT API
+
Zapier
+
Prompt engineering
```

Your positioning should be:

> AI systems engineer who can take companies from prototype → production.

---

# 12-month roadmap

## Month 1-2

Build:

```
AI Agent Platform
+
3 demos
+
website
+
GitHub
```

---

## Month 3-6

Get:

```
5 customers

$5k-$20k/project
```

Focus on delivery.

---

## Month 6-12

Productize:

```
Vertical AI Agent

Example:

AI Agent for Chinese manufacturers

AI Agent for banks

AI Agent for software teams
```

Move from:

```
consulting
```

to:

```
AI company
```

---

A good mental model:

* Consulting gives you **cash**
* Projects give you **data**
* Data gives you **products**
* Products give you **scale**

For your profile, I would lean toward **AI agent engineering + private LLM infrastructure consulting**, because it matches your existing experiments (GPT training, Hermes, agents, GPU clusters) and has higher differentiation than generic AI automation.
