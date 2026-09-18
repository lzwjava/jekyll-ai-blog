---
audio: false
generated: true
image: false
lang: en
layout: post
title: GRPO Training Metrics Explained
translated: false
type: note
---

Question: What do these GRPO/RLHF training metrics mean?

Answer:

This looks like a **GRPO (Group Relative Policy Optimization)** training log — a reinforcement learning fine-tuning method (used in DeepSeek-R1-style training). Here's what each metric means:

---

## 📉 Loss & Optimization

| Metric | Value | Meaning |
|---|---|---|
| `loss` | 0.0001647 | Very low policy loss — model is stable |
| `grad_norm` | 0.6875 | Gradient magnitude; healthy range (not exploding/vanishing) |
| `learning_rate` | 4.571e-06 | Current LR after scheduler decay |
| `num_tokens` | ~101,600 | Tokens processed this step |

---

## 📝 Completion Statistics

| Metric | Value | Meaning |
|---|---|---|
| `mean_length` | 60.25 tokens | Average response length generated |
| `min/max_length` | 9 / 148 | Range of response lengths |
| `clipped_ratio` | 0 | No completions were cut off by `max_new_tokens` — good |
| `terminated_*` | same as above | Lengths of responses that ended naturally (EOS token) |

---

## 🏆 Reward Signals

| Metric | Value | Meaning |
|---|---|---|
| `rewards/reward_format/mean` | **0.0** | ⚠️ Format reward is zero — model is NOT following the expected output format |
| `rewards/reward_correctness/mean` | **0.8125** | ✅ 81.25% of answers are correct |
| `rewards/reward_correctness/std` | 0.5303 | High variance — some correct, some wrong (binary-ish reward) |
| `reward` | 0.8125 | Total reward (format + correctness combined) |
| `reward_std` | 0.5303 | Reward variance across the group |
| `frac_reward_zero_std` | **0.5** | 50% of groups have zero reward variance → half the groups are all-correct or all-wrong |

---

## 📊 Policy Behavior (KL & Entropy)

| Metric | Value | Meaning |
|---|---|---|
| `kl` | 0.008645 | Very small KL divergence from reference model — policy hasn't drifted far |
| `entropy` | 0.7208 | Low entropy → model is fairly confident/deterministic in outputs |
| `clip_ratio/*` | all 0 | No PPO-style clipping triggered — updates are small and safe |

---

## ⏱️ Training Progress

| Metric | Value | Meaning |
|---|---|---|
| `step_time` | 5.263 sec | Time per training step |
| `epoch` | 0.2658 | ~26.6% through epoch 1 — early in training |

---

## 🔍 Key Takeaways

1. **Correctness is high (81%)** — the base model is mostly getting right answers
2. **Format reward is 0** — the model is ignoring your format constraint (e.g., `<think>` tags, JSON, etc.) — this needs attention
3. **`frac_reward_zero_std = 0.5`** means GRPO has no learning signal for half the groups (all same reward), which slows training
4. **KL is tiny** — the model is barely moving from the base, possibly because format reward isn't pushing it

---

References:
- [GRPO Paper (DeepSeekMath)](https://arxiv.org/abs/2402.03300)
- [TRL GRPO Trainer Docs](https://huggingface.co/docs/trl/grpo_trainer)
