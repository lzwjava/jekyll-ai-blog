---
audio: false
generated: true
image: false
lang: en
layout: post
title: Forward vs Reverse KL Distillation
translated: false
type: note
---

Question: What does the comment “this is different from previous distillation, reverse KL” mean?

Answer:

Your friend is pointing out a **technical difference in how the student learns from the teacher**, specifically the **direction of KL divergence used in distillation**.

Let’s break it down simply.

---

## 1. What “distillation” usually means

In standard knowledge distillation, the student tries to match the teacher’s probability distribution:

[
\text{KL}(P_{\text{teacher}} ,|, P_{\text{student}})
]

This is called **forward KL (or KL teacher → student)**.

### Intuition:

* Teacher says: “these are the likely actions”
* Student tries to **cover all modes the teacher considers important**
* Penalizes student if it misses any high-probability teacher action

So it encourages **coverage of teacher behavior**

---

## 2. What “reverse KL” means

Reverse KL flips the direction:

[
\text{KL}(P_{\text{student}} ,|, P_{\text{teacher}})
]

Now:

* Student distribution is “leading”
* Teacher distribution is the reference

### Intuition:

* Student is penalized if it puts probability mass where teacher doesn’t
* Encourages **mode-seeking behavior** (pick one best action instead of covering all)

---

## 3. Why your friend said “this is different”

They are likely noticing that:

> The method described (e.g. on-policy distillation or RL-style training) uses **reverse KL instead of the usual forward KL distillation**

So instead of:

* “student tries to mimic all teacher possibilities”

It becomes:

* “student tries to avoid actions teacher considers bad”

---

## 4. Key behavioral difference

| Type                           | Effect                             | Behavior                               |
| ------------------------------ | ---------------------------------- | -------------------------------------- |
| Forward KL (teacher → student) | “cover everything teacher likes”   | more diverse, safer imitation          |
| Reverse KL (student → teacher) | “avoid teacher-disallowed actions” | sharper, more aggressive, mode-seeking |

---

## 5. Why RL / on-policy methods often use reverse KL

In reinforcement learning / policy optimization:

* You already have a **current policy (student)**
* You want to **constrain it toward a reference (teacher or old policy)**

Reverse KL naturally appears in:

* PPO-style updates (approximate KL constraints)
* policy regularization
* RLHF-style training

So it’s less about “copying teacher perfectly” and more about:

> “stay close, but optimize your own trajectory”

---

## 6. Simple intuition

* **Forward KL distillation**:
  “Teacher is the expert, copy everything they might do.”

* **Reverse KL / RL-style distillation**:
  “You are acting in the world; just don’t drift too far from expert behavior.”

---

## 7. One-line summary

Your friend means:

> This method is not classic imitation distillation (teacher → student forward KL), but a reinforcement-learning style training where the loss uses reverse KL (student → teacher), leading to different behavior: more mode-seeking and policy-optimization-like dynamics.

---

If you want, I can show you how this connects directly to **PPO, KL-regularized RL, and why RLHF uses reverse KL implicitly**—that’s where this becomes very intuitive.
