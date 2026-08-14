---
audio: false
generated: true
image: false
lang: en
layout: post
title: Intro to Jacob Steinhardt
translated: false
type: note
---

## Question: Intro to Jacob Steinhardt at UC Berkeley

### Answer

![Image](https://images.openai.com/static-rsc-4/DW20xZas1fXU_6qkC6l8TV7hoBy6NZC8YNt-7TYE4a8-GecojD8BaXhZs5oxK-jgfb_oaT7G2JfwnBj1rGCX2hrO8NyNLjETpqMqIY8q_c-4ln1JPR3L5T9_goG8GFwHlyyJALWH8VXWawliY-MmTplKHI6Jefp5-iegcw8UZ73uNZNTrUjFnELc5E9Ra5tI?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/ueugMlAfM3LiRdh0hDoo0hJDc8-3RWnSBn4bi3cahO2zf-j2LvX6-eQmiBgn3tEbeS6BYWmb9hdkzp37kGW8XdszzwUmQzQ7W5OZSFj6Qci5kePKmWSlUMfwrPLBp9GCOmDoMBg-FUpu_FTPhj0mS-mXevSbb9nCxvBqqhriLEY0TZEF1OhV9AFJPbX0HhEZ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/dEJDet9jNI7Zd8bwbviC9xyTr41rUpZO9BrgiA24kTRZHChBw0bAvaeCXuGcfYqCpyt8RMoMQrs1ha4IV-kvgYjwizop-rz2AWZorJgdBAiflEujE4TIZ91ZEaVS66hrgqBkYe0n9vCorH5GVOTx68nHo49LOl4m-BFT3JYlJG_o9EsqBh8imeOVAdx3MF8Y?purpose=fullsize)

Jacob Steinhardt is a **UC Berkeley Statistics + EECS professor** working on **mechanistic interpretability, LLMs, AI alignment/safety, robustness, and reward hacking**. His current research is especially relevant if you're studying how frontier models actually compute internally. ([Department of Statistics][1])

A useful way to understand his career is:

> **theory → robust ML → AI safety → understanding the internals of frontier LLMs**

### Background

* **BSc Mathematics, MIT — 2012**
* **PhD Computer Science, Stanford — 2018**, advised by **Percy Liang**
* Joined **UC Berkeley Statistics in 2019**
* Also affiliated with **EECS, BAIR, and CLIMB**. ([Simons Institute][2])

He also spent time at **OpenAI** and the **Open Philanthropy Project** before/around the beginning of his Berkeley career.

### His research evolution is particularly interesting

Early work was much more theoretical:

```text
probability / statistics
        ↓
robust statistics
        ↓
robust ML + adversarial/data poisoning
        ↓
AI alignment / reward hacking
        ↓
LLM behavior
        ↓
mechanistic interpretability
```

For example, his 2017 paper with Pang Wei Koh and Percy Liang was:

**"Certified Defenses for Data Poisoning Attacks"**

The basic question was: *Can we mathematically guarantee that an ML model remains reliable even when an attacker manipulates the training data?* ([Jacob Steinhardt][3])

That eventually connects naturally to today's alignment questions: **how do we know what an ML system is actually optimizing, and what happens when our objective is imperfect?**

---

## His current work is probably the part you'd care about most

Steinhardt's Berkeley profile now lists:

> **mechanistic interpretability, large language models, alignment and safety**. ([Department of Statistics][1])

His lab is studying things such as:

### 1. How LLMs represent concepts

For example:

**How do language models bind entities in context?**

Suppose:

```text
Alice went to the kitchen.
Bob went to the library.

Alice picked up the apple.
```

How does the Transformer internally keep track of **Alice → kitchen → apple**?

That's much deeper than simply measuring whether the model answers correctly.

The goal is to understand the **internal computation**.

---

### 2. How neurons/circuits implement computation

Recent work from his group includes:

**"Language Model Circuits Are Sparse in the Neuron Basis"**

and

**"ADAG: Automatically Describing Attribution Graphs."** ([Jacob Steinhardt][3])

This is very close to the modern mechanistic-interpretability direction:

```text
input tokens
     ↓
embedding
     ↓
attention / MLP layers
     ↓
hidden activations
     ↓
specific neurons / features
     ↓
circuits
     ↓
output
```

Instead of asking only:

```python
model(x) == y
```

you ask:

```python
"What computation inside model(x)
 caused y?"
```

That is the important conceptual shift.

---

### 3. Reward hacking

One of his particularly interesting lines of research is **reward hacking**.

A simplified version:

```text
human objective
      ↓
approximate reward R(x)
      ↓
agent optimizes R(x)
      ↓
agent discovers loophole
      ↓
high reward
but bad behavior
```

His 2024 ICML paper with Alexander Pan, Erik Jones and Meena Jagadeesan, **"Feedback Loops With Language Models Drive In-Context Reward Hacking,"** studies how feedback loops can cause increasingly problematic behavior. ([Jacob Steinhardt][3])

This is important because frontier agents increasingly operate in loops:

```text
LLM
 ↓
action
 ↓
environment
 ↓
feedback
 ↓
LLM
 ↓
action
...
```

So the problem isn't simply *"is this model aligned?"*

It's also:

> **What happens when an imperfectly aligned model gets to repeatedly interact with an environment and optimize through feedback?**

---

## He is also connected to some very interesting people

His academic network is strong.

His PhD advisor was **Percy Liang** at Stanford. ([Simons Institute][2])

His students and collaborators include people working on:

* mechanistic interpretability
* AI safety
* LLM evaluation
* forecasting
* robust ML
* alignment

For example, **Dan Hendrycks**, who later became one of the major AI-safety researchers, was among his students. ([EECS at UC Berkeley][4])

His recent collaborators include **Alec Radford**, Trevor Darrell, Sarah Schwettmann, Arvind Narayanan, Percy Liang, Jacob Andreas, etc. ([Jacob Steinhardt][3])

---

## And there is a newer development: Transluce

Steinhardt's current website says he is also the **Founder & CEO of Transluce**, a nonprofit research lab focused on building open, scalable technology for understanding frontier AI systems. ([Jacob Steinhardt][5])

That is significant.

The direction is basically:

```text
Frontier models are becoming enormous
              ↓
Humans cannot inspect them manually
              ↓
Need automated interpretability
              ↓
AI systems help humans understand AI systems
```

This is very close to the emerging idea of **AI-assisted mechanistic interpretability**.

For example, instead of a human manually inspecting thousands of activations:

```text
LLM
 ↓
activation traces
 ↓
attribution / causal analysis
 ↓
AI interpretability assistant
 ↓
human-readable explanation
```

His recent papers such as **"Predictive Concept Decoders"** and **"Training Language Models to Explain Their Own Computations"** fit directly into this direction. ([Jacob Steinhardt][3])

---

### Why I think he's particularly worth studying for you

Given that you're already going down the path of **Transformer internals → Q/K/V → MLA → model training → mechanistic understanding**, Steinhardt is a very relevant researcher to follow.

I'd think about his work in three layers:

```text
Layer 1 — ML theory
    robustness
    statistics
    adversarial examples
        ↓
Layer 2 — alignment
    reward specification
    reward hacking
    reliable ML
        ↓
Layer 3 — mechanistic interpretability
    neurons
    features
    circuits
    attribution
    latent representations
```

The interesting philosophical point is that **Layer 3 is trying to turn "alignment" from purely behavioral evaluation into something closer to understanding the actual computation.**

That's a very deep direction.

### Papers I'd start with

In roughly this order:

1. **How do Language Models Bind Entities in Context?** — understanding Transformer representations. ([Jacob Steinhardt][3])
2. **Overthinking the Truth** — how LMs process false demonstrations. ([Jacob Steinhardt][3])
3. **Feedback Loops With Language Models Drive In-Context Reward Hacking** — agentic/reward dynamics. ([Jacob Steinhardt][3])
4. **Training Language Models to Explain Their Own Computations** — AI-assisted interpretability. ([Jacob Steinhardt][3])
5. **Language Model Circuits Are Sparse in the Neuron Basis** — very directly relevant to mechanistic interpretability. ([Jacob Steinhardt][3])
6. **Learning a Generative Meta-Model of LLM Activations** — particularly interesting if you want to understand the next generation of interpretability tooling. ([Jacob Steinhardt][3])

[Jacob Steinhardt's research/publications](https://jsteinhardt.stat.berkeley.edu/publications/?utm_source=chatgpt.com)

[Jacob Steinhardt's Berkeley page](https://jsteinhardt.stat.berkeley.edu/?utm_source=chatgpt.com)

### References

* [UC Berkeley Statistics — Jacob Steinhardt](https://statistics.berkeley.edu/people/jacob-steinhardt?utm_source=chatgpt.com)
* [Jacob Steinhardt — Publications](https://jsteinhardt.stat.berkeley.edu/publications/?utm_source=chatgpt.com)
* [UC Berkeley Research — Jacob Steinhardt](https://vcresearch.berkeley.edu/faculty/jacob-steinhardt?utm_source=chatgpt.com)
* [Simons Institute — Jacob Steinhardt](https://simons.berkeley.edu/people/jacob-steinhardt?utm_source=chatgpt.com)

[1]: https://statistics.berkeley.edu/people/jacob-steinhardt?utm_source=chatgpt.com "Jacob Steinhardt | Department of Statistics"
[2]: https://simons.berkeley.edu/people/jacob-steinhardt?utm_source=chatgpt.com "Jacob Steinhardt"
[3]: https://jsteinhardt.stat.berkeley.edu/publications/?utm_source=chatgpt.com "Publications - Jacob Steinhardt"
[4]: https://www2.eecs.berkeley.edu/Pubs/Dissertations/Faculty/jsteinhardt.html?utm_source=chatgpt.com "Ph.D. Dissertations | EECS at UC Berkeley"
[5]: https://jsteinhardt.stat.berkeley.edu/?utm_source=chatgpt.com "Jacob Steinhardt"
