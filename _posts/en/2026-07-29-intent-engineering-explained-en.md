---
audio: false
generated: true
image: false
lang: en
layout: post
title: Intent Engineering Explained
translated: false
type: note
---

Question: Explain the IntentLab article “Turn Your Intent Into Production Systems” and why it matters.

Answer:

I read the article. The core idea is:

> **The next evolution of AI engineering is not prompt engineering. It is intent engineering: converting human goals into executable specifications that agents can reliably achieve in production.** ([RJL.pub][1])

This is very aligned with the direction you have been exploring: **loop engineering, multiple agents, digital employees, Hermes notifications, agent orchestration.**

The article is basically saying:

```
Prompt:
"Build me a user management page"

          ↓

Task:
"Create CRUD APIs"

          ↓

Intent:
"Enable admins to manage users safely,
under these constraints,
with measurable success criteria,
and stop when conditions fail"

          ↓

Production system
```

---

## 1. Prompt → Context → Intent

The author argues that AI development has gone through stages:

### Stage 1: Prompt engineering

Human:

```
Write a Python script to parse CSV
```

AI:

```
generates code
```

Problem:

* no business context
* no constraints
* no definition of success

---

### Stage 2: Context engineering

Give AI:

```
CLAUDE.md
AGENTS.md
repo structure
architecture docs
database schema
API docs
coding rules
```

Now the agent understands the environment.

This matches the broader industry movement: reliable agents need high-quality context, retrieval, tools, and memory instead of only better prompts. ([elastic.co][2])

Example:

```
You are working in Spring Boot 3.

Database:
PostgreSQL 16

Rules:
- no direct SQL in controllers
- use MyBatis mapper
- all APIs require JWT
```

Much better.

---

### Stage 3: Intent engineering

But context still answers:

> "How do I do things?"

It does not answer:

> "Why am I doing this?"

Intent adds:

```
objective
success criteria
constraints
permissions
stop conditions
human escalation rules
```

Example:

`migration.intent.yaml`

```yaml
objective:
  migrate legacy user API to v2

success:
  - all tests pass
  - latency < 100ms p95
  - zero breaking API changes

constraints:
  - don't modify database schema
  - don't touch payment module

permissions:
  - edit backend/src/user

stop_conditions:
  - unclear business rule
  - test failure after 3 retries

escalate:
  owner: backend-team
```

Now an agent has a contract.

---

# Why this is important

Traditional software:

```
Human
 |
 v
Requirement
 |
 v
Engineer
 |
 v
Code
 |
 v
Production
```

AI-native software:

```
Human intent
      |
      v
Intent specification
      |
      v
Agent workers
      |
      +---- coder agent
      |
      +---- tester agent
      |
      +---- security agent
      |
      +---- reviewer agent
      |
      v
Production
```

The human moves upward.

You stop being:

```
person who writes every line
```

You become:

```
person who defines goals,
constraints,
architecture,
evaluation.
```

---

# Connection to your "loop engineering"

Your previous idea:

> agent wakes up → checks state → fixes → retries → reports completion

is actually very close.

A production agent loop looks like:

```python
while True:

    state = observe()

    if goal_completed(state):
        notify_user()
        break

    action = agent.decide(
        intent=intent_spec,
        context=context,
        tools=tools
    )

    execute(action)

    evaluate()
```

The missing piece in many agent systems is:

```
evaluate()
```

Without evaluation:

```
agent thinks:
"I finished"

human sees:
"it broke production"
```

Intent provides the evaluator.

---

# Multi-agent example

Imagine an AI software company.

Human:

```
Build a SaaS billing system
```

Intent:

```yaml
objective:
  launch Stripe subscription billing

success:
  - customer can subscribe
  - invoices generated
  - refunds work
  - security review passed

constraints:
  - PCI compliance
  - no storing card numbers

```

Agents:

```
CEO agent
 |
 +-- product agent
 |
 +-- architect agent
 |
 +-- backend agent
 |
 +-- frontend agent
 |
 +-- QA agent
 |
 +-- security agent
```

Each agent receives:

```
same intent
different responsibility
```

---

# The interesting business implication

This changes AI consulting.

Old consulting:

```
"We will build an AI chatbot"
```

New consulting:

```
"We will convert your business process into
intent specifications + autonomous workflows."
```

The valuable artifact is no longer code.

It is:

```
Business process
        ↓
Intent model
        ↓
Agent workflow
        ↓
Evaluation system
```

---

# My take for your AI company direction

This article is basically describing the product category you are already approaching.

Your stack could become:

```
Intent Layer
    |
    +-- intent.yaml
    |
Agent Runtime
    |
    +-- Claude/OpenAI/Qwen
    |
Tools
    |
    +-- MCP
    +-- shell
    +-- browser
    +-- database
    |
Evaluation
    |
    +-- tests
    +-- metrics
    +-- human approval
```

A minimal implementation:

```
project/
├── intent.yaml
├── context.md
├── agents/
│   ├── coder.py
│   ├── tester.py
│   └── reviewer.py
├── tools/
└── evals/
```

Basically:

**GitHub Actions + Claude Code + MCP + eval framework + intent files.**

This is probably where AI engineering is moving: from "calling LLM APIs" to "operating autonomous production systems." ([RJL.pub][1])

References:

* ([RJL.pub][1])
* ([elastic.co][2])

[1]: https://rjl.pub/?utm_source=chatgpt.com "RJL.pub - AI-Native Development Journey | RJ Lindelof"
[2]: https://www.elastic.co/elasticsearch/context-engineering?utm_source=chatgpt.com "Context engineering for AI agents | Elastic"
