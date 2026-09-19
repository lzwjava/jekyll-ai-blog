---
audio: false
generated: true
image: false
lang: en
layout: post
title: What an FDE Does
translated: false
type: note
---

Question: **What does an FDE (Forward Deployed Engineer) do, and what are their responsibilities?**

Answer:

**FDE = Forward Deployed Engineer.** The core idea is:

> **Take a company's technology/model and make it actually work for a specific customer in the customer's real environment.**

It's somewhere between **software engineer + solutions architect + technical consultant + product engineer**.

### 1. Typical FDE workflow

```text
Customer has a problem
        ↓
FDE talks to customer / understands workflow
        ↓
Translate business problem → technical problem
        ↓
Build integration / prototype / agent / data pipeline
        ↓
Deploy into customer's environment
        ↓
Debug production problems
        ↓
Iterate with customer
        ↓
Turn successful solution into reusable product
```

For an AI company, for example:

```text
Customer:
"We have 10M internal documents.
Employees want to ask questions about them."

FDE:
  ├── understand data sources
  ├── inspect permissions
  ├── build ingestion pipeline
  ├── chunk / embed / index
  ├── implement RAG
  ├── integrate SSO
  ├── build evaluation set
  ├── deploy
  ├── debug hallucinations / latency
  └── measure whether users actually get useful answers
```

That's very different from a normal backend engineer who might receive a well-defined ticket such as:

```text
Implement POST /documents
Store document metadata in PostgreSQL
Return document_id
```

The FDE often starts with a much fuzzier question:

> "How can we make this customer's workflow actually work?"

---

## 2. Main responsibilities

### A. Customer discovery

Understand what the customer actually needs.

Not:

> "What API do you want?"

But:

> "Show me how your employees do this today."

You might spend time looking at:

* existing software
* databases
* APIs
* internal workflows
* data formats
* security requirements
* user behavior
* operational constraints

The FDE needs to discover the **real technical bottleneck**.

---

### B. Rapid prototyping

FDEs usually write a lot of code.

For an AI startup:

```python
docs = load_customer_data()

chunks = chunk(docs)

vectors = embed(chunks)

index = build_index(vectors)

answer = llm(
    question,
    context=retrieve(index, question)
)
```

Then:

```text
Customer: "The answers aren't reliable."

FDE:
  → collect failure cases
  → create eval dataset
  → modify retrieval
  → modify prompt
  → test different models
  → add reranking
  → measure accuracy
```

The goal isn't beautiful architecture on day 1.

It's:

> **Get something useful into the customer's hands quickly.**

---

### C. Integration

A huge part of FDE work is connecting things.

For example:

```text
Customer's systems

Salesforce
    │
Postgres
    │
S3
    │
Slack
    │
Internal APIs
    ↓
FDE's integration layer
    ↓
AI platform
    ↓
Customer application
```

You may write:

* API integrations
* ETL pipelines
* authentication
* webhooks
* SDK integrations
* database connectors
* agent tools
* deployment scripts
* monitoring
* evaluation systems

---

### D. Deployment

FDEs often need to understand infrastructure.

For example:

```bash
docker build .
docker push <REGISTRY>/<IMAGE>

kubectl apply -f deployment.yaml

kubectl logs deployment/agent
```

Or customer requirements might force:

```text
AWS
Kubernetes
VPC
PrivateLink
SSO
OAuth
Vault
Terraform
GPU cluster
on-prem servers
```

So an FDE can be much more hands-on than a traditional solutions consultant.

---

### E. Production debugging

This is an important distinction.

The FDE doesn't stop when the demo works.

Customer:

> "It worked yesterday but now responses take 12 seconds."

FDE investigates:

```text
request
  ↓
API gateway        20 ms
  ↓
retrieval          800 ms
  ↓
reranker           1.2 s
  ↓
LLM                 8 s
  ↓
serialization      100 ms
```

Then discovers:

```text
LLM queueing ↑
GPU utilization 98%
KV cache pressure
```

and fixes the actual production bottleneck.

---

### F. Customer-facing technical communication

This is probably the part that differentiates FDE from ordinary SWE most strongly.

You might be in a meeting with:

```text
CTO
VP Engineering
Staff Engineer
Security team
Data team
Product manager
```

and simultaneously need to understand:

```text
business requirement
        ↓
architecture
        ↓
implementation
        ↓
deployment
        ↓
ROI
```

You therefore need to be comfortable saying:

> "This approach will work, but the retrieval quality is the bottleneck, not the model. I tested 500 representative queries and recall@10 is only 71%."

That's much more valuable than simply saying:

> "We should use RAG."

---

## 3. FDE vs SWE

A useful mental model:

|                      | Software Engineer     | FDE                     |
| -------------------- | --------------------- | ----------------------- |
| Primary customer     | Internal product/team | External customer       |
| Requirements         | Relatively defined    | Often ambiguous         |
| Coding               | High                  | High                    |
| Customer interaction | Low–medium            | High                    |
| Deployment           | Sometimes             | Frequently              |
| Architecture         | Product-focused       | Customer + product      |
| Debugging            | Product               | Customer environment    |
| Travel               | Usually low           | Can be significant      |
| Speed                | Important             | **Extremely important** |
| Success              | Software works        | **Customer gets value** |

FDE is **not a less-technical sales engineer**.

A strong FDE can be extremely technical.

---

## 4. FDE vs Solutions Engineer

There is some overlap:

```text
Sales Engineer
    ↓
Solutions Engineer
    ↓
Forward Deployed Engineer
    ↓
Software / Product Engineer
```

But this isn't a strict hierarchy.

A rough distinction:

**Solutions Engineer**

```text
"Here's how our product solves your problem."
```

**FDE**

```text
"Let me actually build the thing that solves your problem."
```

An FDE might spend days writing Python, debugging Kubernetes, profiling an LLM pipeline, modifying an agent, and deploying it.

---

## 5. AI companies particularly need FDEs

This role has become especially interesting with LLM products because the technology is powerful but **customer problems are extremely heterogeneous**.

For example, an AI company might sell:

```text
Agent platform
```

But Customer A needs:

```text
Agent + Salesforce + SQL + Slack
```

Customer B:

```text
Agent + proprietary documents + RAG + SSO
```

Customer C:

```text
Agent + internal APIs + Kubernetes + private model
```

Customer D:

```text
Coding agent + GitHub + CI/CD + security policies
```

The FDE bridges:

```text
general-purpose AI platform
             ↓
       customer's messy reality
```

That's why companies such as Palantir Technologies historically emphasized forward-deployed engineering, and many modern AI startups have adopted similar customer-embedded engineering models.

---

## 6. What makes a good FDE?

The unusual combination is:

```text
              Technical depth
                    ▲
                    │
                    │
Customer empathy ───┼─── Product sense
                    │
                    │
                    ▼
              Execution speed
```

You need enough engineering depth to build things, but also enough customer understanding to determine **what should be built**.

For someone with your background, the interesting part is that you already have several components that map naturally to FDE work:

```text
Java/backend
   +
Python
   +
LLM/agents
   +
AI infrastructure
   +
customer-facing consulting
   +
rapid prototyping
```

That combination is quite close to the modern **AI FDE** profile.

The biggest additional skill is probably not another programming language. It's learning to turn:

```text
"We want an AI agent"
```

into:

```text
business workflow
→ measurable objective
→ technical architecture
→ prototype
→ evaluation
→ production deployment
→ measurable customer outcome
```

I can also map **your current 12-year engineering background → a realistic AI FDE job description and interview loop** if you want.
