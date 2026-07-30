---
audio: false
generated: true
image: false
lang: en
layout: post
title: Verifiable Signal for RL Training
translated: false
type: note
---

Question: Is it a good idea to do RL or reasoning-process training with internal company data?

Answer:

Yes, but **only if the data has a verifiable signal**. The mistake many teams make is:

> "We have lots of internal documents → let's do RL / reasoning training."

That usually fails.

The better mental model:

```
Internal data
    |
    +--> SFT (teach knowledge/style)
    |
    +--> RAG (retrieve facts)
    |
    +--> RL / reasoning training (teach behavior)
```

Different problems need different techniques.

---

## 1. Internal knowledge → usually RAG, not RL

Example:

Your company has:

```
10 years Java code
API docs
DB schema
business rules
tickets
meeting notes
```

You want:

> "How do I modify payment workflow?"

Do NOT train RL.

Use:

```
User query
    |
embedding
    |
vector DB
    |
retrieve relevant code/docs
    |
LLM
    |
answer
```

Because the knowledge changes.

If your payment rules change tomorrow:

RAG:

```
update document
done
```

Fine-tuning:

```
collect data
train
evaluate
deploy
```

much slower.

---

## 2. Reasoning training needs "process supervision"

This is where models like DeepSeek-R1 and VibeThinker are interesting.

You don't train:

```
Question -> Answer
```

You train:

```
Question
   |
   |
Reasoning process
   |
   |
Answer
```

Example:

Bad SFT:

```
Q:
Why does this distributed transaction fail?

A:
Because timeout.
```

Better:

```
Q:
Why does this distributed transaction fail?

Thinking:
1. Check transaction boundary
2. Check timeout config
3. Check retry mechanism
4. Check idempotency
5. Find mismatch

Answer:
The retry causes duplicate commit because...
```

The model learns the search process.

---

## 3. Internal engineering data is actually very valuable

For software companies, you have a gold mine:

```
Git commits
PR reviews
bug fixes
incident reports
design docs
architecture discussions
test failures
```

Example:

Git history:

```
Bug:
Payment duplicated

Developer:
Changed:
@Transactional
removed retry
added idempotency key

Review:
Why?
Because Kafka retry creates duplicate events
```

This can become:

```
Problem:
payment duplicated

Reasoning:
Analyze:
- database transaction
- message queue
- retry semantics

Solution:
add idempotency
```

This is much better than random internet data.

---

## 4. RL is harder than SFT

A common pipeline:

### Stage 1: SFT

```
dataset:

(input, reasoning trace, answer)

        |
        v

model learns pattern
```

Example:

```
500k-10M examples
```

---

### Stage 2: RL

Now create a reward:

```
model output
      |
      |
 evaluator
      |
      |
 reward
```

For coding:

```
Generate code
      |
 run tests
      |
 pass = +1
 fail = 0
```

For SQL:

```
Generate query
      |
 execute database
      |
 correct result = +1
```

For internal workflows:

```
Generate deployment plan
      |
 simulate / human review
      |
 reward
```

---

## 5. The biggest opportunity: company-specific reasoning models

Imagine a bank.

General model:

```
How do I fix payment bug?
```

answer:
generic advice.

Internal reasoning model:

```
Context:
HSBC payment architecture

Reasoning:
1. Check PayMe service
2. Check Kafka topic
3. Check Db2 transaction
4. Check settlement batch

Solution:
...
```

This is valuable.

---

## 6. But don't leak secrets into training

Important:

Do not directly train:

```
customer data
passwords
API keys
production logs
PII
```

Pipeline:

```
raw data
 |
sanitization
 |
synthetic examples
 |
training
```

Example:

Before:

```
customer_id=938475
card=4111111111111111
```

After:

```
customer_id=<USER_ID>
card=<CARD_NUMBER>
```

---

## 7. For someone building AI infra, the interesting project is

Not:

> "Train a bigger model."

More interesting:

```
Internal coding agent

          |
          v

Codebase
+
Git history
+
PR review
+
CI failures
+
Architecture docs

          |
          v

Reasoning SFT

          |
          v

RL with tests

          |
          v

Company-specific coding model
```

This is probably where many enterprise AI systems are going.

---

Given your background (Java backend + LLM training + vLLM), a very realistic experiment:

1. Pick one open model:

```
Qwen3-8B
DeepSeek-R1-Distill-Qwen-7B
VibeThinker-3B
```

2. Collect:

```
5000-50000
bug -> investigation -> fix
```

3. Train LoRA:

```
PEFT + SFT
```

4. Add verifier:

```
run unit tests
compile project
check output
```

5. Do GRPO/RL:

```
reward = tests passed
```

This is basically a miniature DeepSeek-R1-style pipeline on your own engineering data.
