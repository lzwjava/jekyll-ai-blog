---
audio: false
generated: true
image: false
lang: en
layout: post
title: How to Use Loop Engineering
translated: false
type: note
---

Question: How to use loop engineering?

Answer:

**Loop engineering** is the practice of designing software/AI workflows as a continuous feedback loop:

```
Observe → Decide → Act → Verify → Learn → Repeat
```

It is especially useful for **AI agents**, because LLMs are not deterministic programmers. Instead of writing every step, you build a system where the agent can inspect reality, take actions, detect failures, and improve.

A simple mental model:

```
             ┌──────────────┐
             │   Goal       │
             └──────┬───────┘
                    ↓
             ┌──────────────┐
             │   Observe    │
             │ logs/files/db│
             └──────┬───────┘
                    ↓
             ┌──────────────┐
             │   Reason     │
             │ LLM planning │
             └──────┬───────┘
                    ↓
             ┌──────────────┐
             │    Act       │
             │ tools/code   │
             └──────┬───────┘
                    ↓
             ┌──────────────┐
             │  Evaluate    │
             │ tests/checks │
             └──────┬───────┘
                    │
              success?
              /     \
            yes      no
            stop    retry
                    ↑
                    └────────
```

## 1. Traditional engineering vs loop engineering

Traditional:

```
Human:
  understand problem
  write design
  write code
  test
  deploy
```

Loop engineering:

```
Human:
  define objective

Agent:
  inspect repository
  find missing pieces
  modify code
  run tests
  read errors
  fix
  repeat
```

The human becomes the **goal setter + system designer**.

The agent becomes the **execution loop**.

---

## 2. Basic coding agent loop

Example:

Goal:

> "Make this old Java project run."

Agent loop:

### Step 1: Observe

```
ls
find .
cat pom.xml
git status
```

Agent discovers:

```
pom.xml exists
mysql dependency missing
database config missing
tests failing
```

### Step 2: Plan

LLM:

```
Problem:
- application cannot start

Hypothesis:
- missing database schema

Action:
- create docker mysql
- generate schema
- update config
```

### Step 3: Act

Agent:

```bash
docker compose up mysql

mvn test
```

Failure:

```
Table user does not exist
```

### Step 4: Feedback

Agent reads error:

```
CREATE TABLE user ...
```

Creates migration:

```
db/migration/V1__init.sql
```

Runs again.

Loop continues.

---

## 3. The important part: verification loop

Bad agent:

```
ask LLM
write code
done
```

Good agent:

```
write code
↓
compile
↓
test
↓
inspect error
↓
fix
↓
repeat
```

Example:

```python
while True:
    plan = llm(goal, context)

    result = execute(plan)

    feedback = evaluate(result)

    if feedback.success:
        break

    context.append(feedback.error)
```

This is the core of modern coding agents.

---

## 4. Multi-agent loop engineering

For larger systems:

```
             Manager Agent
                  |
     ┌────────────┼────────────┐
     ↓            ↓            ↓

Research     Coding       Testing
 Agent        Agent        Agent

     ↑            ↑            |
     └────────────┴────────────┘
              Feedback
```

Example:

Software migration:

```
Manager:
"Upgrade Spring Boot 2 → 3"

Research agent:
- find breaking changes

Coding agent:
- modify dependencies

Testing agent:
- run CI

Reviewer agent:
- inspect diff
```

---

## 5. Production AI employee loop

For your "digital employee" idea:

Each agent should have:

```
Agent
 |
 +-- Goal
 |
 +-- Memory
 |
 +-- Tools
 |
 +-- Event loop
 |
 +-- Notification
 |
 +-- Evaluation
```

Example:

Database agent:

```
Event:
  application failed

Loop:

1. Read logs
2. Identify missing table
3. Search migration history
4. Create SQL
5. Apply migration
6. Verify
7. Notify human
```

Notification:

```
Hermes:
"Database repair completed.
Created table:
orders

Verification:
127 tests passed"
```

---

## 6. The key engineering principle

Do not optimize the prompt.

Optimize the **loop**.

Weak:

```
"You are an expert developer.
Fix this issue."
```

Strong:

```
Goal:
Fix application startup.

Loop:

1. Inspect error logs
2. Form hypothesis
3. Make smallest change
4. Run test
5. Analyze failure
6. Repeat until green
7. Report changes
```

The loop creates reliability.

---

## 7. Useful architecture

A practical stack:

```
                 User

                  |
             Task Queue

                  |
             Agent Runtime

        ┌─────────┼─────────┐

     Planner   Executor   Critic

        |          |          |

     LLM       Tools       Tests

                  |
              Environment

                  |
              Feedback
```

Technologies:

* Agent runtime: Python/TypeScript
* Tools: shell, git, browser, database
* Memory: SQLite/Postgres/vector DB
* Evaluation: pytest, CI, benchmarks
* Events: Redis/Kafka/NATS

---

## 8. For your current projects (ww / iclaw / hermes)

A good direction is:

```
Task
 |
 ↓
Agent Session
 |
 ↓
Tool calls
 |
 ↓
Artifacts
 |
 ↓
Verifier
 |
 ↓
Notification
 |
 ↓
Human approval
```

Example:

```
Agent A:
"Research latest CUDA changes"

↓

writes:
research.md

↓

Agent B:
"Review research"

↓

Agent C:
"Create blog post"

↓

Hermes:
ding!

"3 agents finished.
Waiting for publish approval."
```

The future "software engineer" is not a chatbot. It is a **controlled autonomous loop**.

References:

* [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629?utm_source=chatgpt.com)
* [AutoGPT GitHub](https://github.com/Significant-Gravitas/AutoGPT?utm_source=chatgpt.com)
* [SWE-agent GitHub](https://github.com/SWE-agent/SWE-agent?utm_source=chatgpt.com)