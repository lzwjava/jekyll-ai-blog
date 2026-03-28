---
audio: false
generated: true
image: false
lang: en
layout: post
title: Overcoming Decision Friction for Cloud Computing
translated: false
type: note
---

Question: Why did you not use cloud GPUs earlier, and what reflections do you have now after finally using Alibaba Cloud's GPU instance?

Answer:

## Your Reflection — A Honest Self-Assessment

You identified the real blockers clearly:

| Blocker | Reality Check |
|--------|---------------|
| "I have a local 4070, good enough" | 4070 is ~20 TFLOPS FP32. T4 is similar, but cloud GPUs scale — you can rent A100/H100 when needed |
| "Cloud setup is too troublesome" | One-time friction. After the first setup, it's faster than managing local hardware |
| "Lambda payment didn't work" | A logistics problem, not a capability problem. Gave up too easily |
| "Chinese cloud UI is bad / unfamiliar" | UI preference — a very minor issue dressed up as a reason |
| "Bias against smaller GPU providers" | Justified sometimes, but cost you years |

---

## The Core Insight You Had

> **"The most important thing is to train a model with GPT-3 / GPT-4 level capability. Everything else is secondary."**

This is the right framing. When you remember the **goal**, the excuses dissolve:

- UI language? Irrelevant to model quality.
- Payment friction? Solvable in one afternoon.
- Preference for local GPU? Fine for experiments, not for serious training runs.

---

## What This Means Going Forward

- **Compute is now unblocked.** You have access to real GPU hours.
- **Don't optimize the environment — optimize the model.**
- Local 4070 → fast iteration, debugging, small experiments
- Cloud GPU (T4 / A10 / A100) → actual training runs
- The two-to-three years lost were not about GPU access. They were about **decision friction**. Now that friction is gone.

---

## One Reminder

Cloud GPU time costs money per hour. The discipline now shifts to:

1. Be clear on **what experiment you are running** before you start the instance
2. **Stop the instance** when not in use
3. Track your runs — don't repeat failed experiments

The goal is real. The compute is now available. Execute.