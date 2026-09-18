---
audio: false
generated: true
image: false
lang: en
layout: post
title: KL Divergence in RL Fine-Tuning
translated: false
type: note
---

Question: What does KL divergence mean in the context of RL fine-tuning?

Answer:

## KL Divergence — Plain English First

**KL Divergence** (Kullback–Leibler Divergence) measures **how different two probability distributions are** from each other.

In RL fine-tuning, the question it answers is:

> *"How far has the trained model drifted from the original reference model?"*

---

## 🎯 Intuition

Imagine the model as a person giving answers. Before training, it has certain habits (the **reference policy**). As RL training pushes it toward higher rewards, its habits change (the **current policy**).

KL divergence measures **how much the habits have changed**.

```
KL(current policy || reference policy)

= 0.0   → identical to the original model
= small → slightly different (safe)
= large → very different (potentially unstable / reward hacking)
```

---

## 📐 The Formula (simplified)

$$KL(P \| Q) = \sum P(x) \log \frac{P(x)}{Q(x)}$$

Where:
- **P** = current (trained) model's output distribution
- **Q** = reference model's output distribution
- It asks: *"for each possible token, how much more/less likely does the new model generate it?"*

---

## 🛡️ Why It Matters in GRPO / PPO

Without a KL penalty, RL training can **reward hack** — the model finds weird outputs that score high rewards but are nonsensical. KL acts as a **leash**:

```
Total Objective = Reward  −  β × KL
```

| β (KL weight) | Effect |
|---|---|
| Too small | Model drifts freely → reward hacking risk |
| Too large | Model barely moves → slow / no learning |
| Just right | Model improves while staying coherent |

---

## 📊 Your Value: `kl = 0.008645`

This is **very small** — meaning:

- ✅ The model has barely drifted from the base model
- ✅ No reward hacking is happening
- ⚠️ But combined with `reward_format = 0`, it suggests the model isn't really learning the format behavior yet — it's playing it safe

---

## 🔁 Quick Summary

| Term | Meaning |
|---|---|
| KL = 0 | Trained model = reference model (no change) |
| KL small | Safe, minor drift |
| KL large | Dangerous drift, reward hacking likely |
| KL penalty | Regularizer that keeps model grounded |

---

References:
- [KL Divergence — Wikipedia](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence)
- [Illustrating RLHF — Hugging Face Blog](https://huggingface.co/blog/rlhf)
- [DeepSeek GRPO Paper](https://arxiv.org/abs/2402.03300)
