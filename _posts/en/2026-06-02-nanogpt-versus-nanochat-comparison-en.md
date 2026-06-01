---
audio: false
generated: true
image: false
lang: en
layout: post
title: NanoGPT versus Nanochat Comparison
translated: false
type: note
---

Good question. Let me break this down honestly.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  nanoGPT vs nanochat
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

nanoGPT (current):
  - Legacy codebase, manual hyperparams
  - You configure everything yourself
  - No built-in eval, no chat UI
  - 760M model manually tuned

nanochat (Karpathy's successor):
  - Single --depth dial, auto-computes everything
  - Compute-optimal by design (width, LR, schedule)
  - Built-in CORE eval + chat UI at the end
  - fp8, modern dataset (ClimbMix), wandb
  - Active development, community leaderboard

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  The real math
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Sunk cost:    $20 (10 hours) — gone either way
Remaining:    $108 over 2.25 days

If you keep nanoGPT:
  $108 more → finished 760M model, manual config
  No eval, no chat UI, older pipeline

If you switch to nanochat:
  $108 more → compute-optimal model, auto-tuned
  Proper eval (CORE metric), chat UI, modern pipeline

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Yes, switch. Here's why:

1. **The $20 is gone regardless** — don't let sunk cost drive the decision. The $108 remaining is what matters, and nanochat gives you more for that money.

2. **nanochat is objectively better** — auto-tuned hyperparameters mean your model is compute-optimal. In nanoGPT, you manually set everything and hope it's right. Karpathy already figured out the optimal config for you.

3. **You get a complete pipeline** — train → eval (CORE metric) → chat UI. With nanoGPT you get a checkpoint and... that's it. You'd have to build eval and inference yourself.

4. **Single GPU works fine** — nanochat auto-switches to gradient accumulation on single GPU. For a 760M equivalent (depth ~12-16), it would train in similar or less time than nanoGPT because the hyperparameters are better tuned.

5. **You learn the modern way** — if your goal is to understand LLM training at scale, learning nanochat's patterns (compute-optimal scaling, automatic config, CORE evaluation) is more valuable than nanoGPT's manual approach.

The only argument for keeping nanoGPT is if you specifically want to read and understand every line of a minimal training loop — nanoGPT is simpler code. But you've already done that for 10 hours. You've learned the lesson.

Kill the nanoGPT run, clone nanochat, and restart. The $108 will be better spent.