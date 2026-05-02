---
audio: false
generated: true
image: false
lang: en
layout: post
title: Kullback-Leibler Divergence in Machine Learning
translated: false
type: note
---

Question: What does KL mean here?

Answer:

Here, **KL** stands for **Kullback–Leibler divergence**, a way to measure how different two probability distributions are.

---

## 1. Intuition first

Think of two models predicting actions:

* Teacher: “I think A is 70%, B is 30%”
* Student: “I think A is 40%, B is 60%”

KL divergence answers:

> “How much information do I lose if I use one distribution to approximate the other?”

So it’s a **distance-like measure between probability distributions** (but not symmetric, and not a true distance metric).

---

## 2. Formal definition

For two distributions (P) and (Q):

[
\mathrm{KL}(P ,|, Q) = \sum_x P(x)\log \frac{P(x)}{Q(x)}
]

or in continuous form:

[
\mathrm{KL}(P ,|, Q) = \int P(x)\log \frac{P(x)}{Q(x)} dx
]

---

## 3. Key properties

### (1) Asymmetry matters

[
\mathrm{KL}(P ,|, Q) \neq \mathrm{KL}(Q ,|, P)
]

This is why people talk about **forward KL vs reverse KL**.

---

### (2) Always ≥ 0

[
\mathrm{KL}(P ,|, Q) \ge 0
]

It is zero only when the two distributions are identical.

---

## 4. Intuition in ML / RL

In your context (distillation / policies):

* (P) = teacher policy (what expert would do)
* (Q) = student policy (what model currently does)

Then KL measures:

> how badly the student fails to match the teacher’s action probabilities

---

## 5. Why it matters in distillation

When training models:

* Minimizing **KL(teacher || student)** → student learns to imitate teacher’s full behavior distribution
* Minimizing **KL(student || teacher)** → student avoids actions teacher considers unlikely (more “sharp” behavior)

---

## 6. Simple analogy

Imagine guessing a friend’s choices:

* If you model them poorly, KL is high (your guesses are “surprising” compared to reality)
* If your model matches well, KL is low

---

## 7. One-line summary

> KL divergence measures how different two probability distributions are, and in machine learning it is used to quantify how much a student model differs from a teacher model.

---

If you want, I can also explain why KL shows up everywhere in **RLHF, PPO, diffusion models, and variational inference**—it’s actually one of the central building blocks in modern ML.