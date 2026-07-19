---
audio: false
generated: true
image: false
lang: en
layout: post
title: Refining the Domain Model Thesis
translated: false
type: note
---

**Question: Is the argument "domain models are wrong; foundation models + cross-domain capability win" correct? Is Baichuan / Wang Xiaochuan's medical AI strategy a mistake?**

Answer:

Your intuition is pointing at a real trend, but the conclusion needs some refinement.

The key distinction is:

> **"Domain model" as a standalone foundation model vs "domain specialization built on top of frontier models."**

The first one is increasingly hard to win. The second one is exactly where many valuable companies will exist.

---

## 1. "Medical model" cannot beat GPT-class foundation models by data alone

Your point:

> 医疗那点文本数据 有 10% 吗？可能很少

This is directionally correct.

A medical startup usually does not have:

* trillions of tokens
* huge multimodal datasets
* massive RL infrastructure
* frontier reasoning research

Compared with OpenAI / Google / Anthropic / DeepSeek:

```
Foundation model:
    pretraining
        ↓
    world knowledge
        ↓
    reasoning ability
        ↓
    coding/math/language capability

Medical AI:
    foundation model
        ↓
    medical fine-tuning
        ↓
    RAG
        ↓
    clinical workflow integration
        ↓
    hospital deployment
```

The medical layer is usually the second half.

A medical company saying:

> "We have 100 million medical documents, therefore our model wins"

is similar to saying:

> "We have many books about programming, therefore we can beat NVIDIA/CUDA."

The bottleneck is not just knowledge.

It is:

* reasoning
* planning
* tool use
* multimodal understanding
* long context
* agent ability

---

## 2. But "classification is wrong" is only half true

AI itself is becoming more general.

Example:

A doctor today:

```
patient symptoms
       |
       v
medical knowledge
       |
       v
diagnosis
       |
       v
treatment plan
```

Future AI:

```
multimodal foundation model

+
medical knowledge graph

+
clinical database

+
hospital systems

+
medical tools

+
robotics/lab systems
```

The intelligence is centralized.

The applications are specialized.

This is similar to:

```
Linux kernel
    |
    +-- Android
    +-- Ubuntu
    +-- Kubernetes nodes
    +-- embedded devices
```

Nobody says:

> "Operating systems are useless because Linux exists."

The application layer still creates enormous value.

---

## 3. Where Baichuan's strategic problem may be

The article's strongest argument is not:

> "Medical AI is wrong."

It is:

> "Medical AI before owning frontier model capability is risky."

That is a much stronger argument.

Look at the timeline:

### 2023

Everyone thought:

```
Build LLM
    |
    v
Find applications
```

### 2024-2025

Reality became:

```
Strong model
    |
    +--> coding
    +--> agents
    +--> enterprise automation
    +--> research assistant
    +--> healthcare
```

Coding exploded because coding is:

* digital
* measurable
* fast feedback
* low regulation
* global market

Medical is:

* slow adoption
* regulatory barriers
* liability problems
* expensive deployment

So the order matters.

---

## 4. Why Anthropic won with coding

This is the most important part.

Anthropic did not say:

> "We are a coding company."

They built a better general model.

Then coding became the wedge.

```
Claude

     |
     +--- coding agent
     |
     +--- enterprise assistant
     |
     +--- research
     |
     +--- healthcare
```

The model creates markets.

Not the reverse.

This is the biggest difference between Internet era and AI era.

Internet:

```
find users
    |
build product
    |
technology supports it
```

AI:

```
improve intelligence
    |
new capabilities emerge
    |
new products appear
```

---

## 5. Was Wang Xiaochuan "doesn't understand LLM"?

I would phrase it more carefully.

He clearly understands:

* NLP
* search
* language technology
* product strategy
* entrepreneurship

His background is actually very relevant.

But LLM changed the game.

Search era:

```
information retrieval
+
ranking
+
NLP
```

LLM era:

```
pretraining scaling
+
RL
+
post-training
+
agent loops
+
compute economics
```

The winner profile changed.

A great search engineer does not automatically become a great frontier model builder.

Same as:

A great compiler engineer does not automatically build NVIDIA GPUs.

Different bottleneck.

---

## 6. The strongest counterargument against the article

The article assumes:

> "Whoever has the strongest model will win medical AI."

Not necessarily.

Look at software history:

Microsoft did not invent the internet.

Oracle did not invent databases.

Salesforce did not invent relational databases.

The infrastructure layer and application layer can both create huge companies.

A medical AI company could win through:

```
GPT/Claude/DeepSeek
        +
medical data
        +
doctor workflow
        +
hospital integration
        +
regulatory approval
        +
distribution
```

The moat is not the model.

The moat is the system.

---

## My current view

### Baichuan abandoning frontier models completely

Probably risky.

Because:

```
weak model
+
medical data
=
limited ceiling
```

### Medical AI itself

Not wrong.

Actually probably inevitable.

But the winning architecture is more likely:

```
Frontier foundation model

          +

Medical intelligence layer

          +

Agent workflow

          +

Hospital ecosystem
```

not:

```
small medical GPT
+
medical documents
=
future OpenAI
```

---

Your analogy with the 1970s-1990s is quite good:

When programming exploded, the biggest winners were not companies making "banking programming languages" or "hospital programming languages."

They built:

* CPUs
* operating systems
* compilers
* databases
* networks

Then every industry was built on top.

AI is likely similar:

The scarce layer today is **general intelligence infrastructure**.

But once that layer stabilizes, domain systems will still be enormous. The mistake is confusing **domain expertise** with **model intelligence**.
