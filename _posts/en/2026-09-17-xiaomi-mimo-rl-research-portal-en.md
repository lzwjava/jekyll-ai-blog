---
audio: false
generated: true
image: false
lang: en
layout: post
title: Xiaomi MiMo RL Research Portal
translated: false
type: note
---

Question: What is Xiaomi’s `https://mimo.xiaomi.com/rl/`?

Answer: It’s Xiaomi’s **MiMo RL (Reinforcement Learning) research/project site**—the training side of their MiMo reasoning-model work.

The important bit is that Xiaomi isn’t just publishing a model; they’ve been publishing a fairly complete **LLM post-training/RL stack** around MiMo:

* **MiMo-7B** — a 7B dense reasoning model.
* **RL-Zero** — RL directly from the base model.
* **SFT → RL** — supervised fine-tuning followed by RL.
* **Rule-based rewards** — especially math/code, avoiding an LLM judge where possible.
* **GRPO-style training** and large-scale rollout infrastructure.
* Their RL training window was expanded from **32K → 48K tokens**, with the reported MiMo-7B-RL-0530 AIME24 score reaching **80.1**. ([GitHub][1])
* They describe a **“Seamless Rollout Engine”** with continuous rollout, asynchronous reward computation, and early termination; Xiaomi reports 2.29× faster RL training and 1.96× faster validation from those infrastructure changes. ([GitHub][2])

The GitHub repo is probably more useful if you're actually interested in reproducing it:

[XiaomiMiMo/MiMo on GitHub](https://github.com/XiaomiMiMo/MiMo?utm_source=chatgpt.com) ([GitHub][1])

And Xiaomi's paper index currently exposes several RL-related papers, including **“Stabilizing MoE RL”** and **“ARL-Tangram.”** ([Mimo][3])

So, in one sentence: **`/rl/` is Xiaomi's MiMo research portal focused on how they train reasoning models with RL, rather than merely serving the models.**

I can also reverse-engineer the MiMo RL stack into a **minimal PyTorch/TRL-style implementation**—policy → rollout → verifier → GRPO loss → optimizer—which would be the interesting part if you're evaluating their recipe.

[1]: https://github.com/xiaomimimo/mimo?utm_source=chatgpt.com "GitHub - XiaomiMiMo/MiMo: MiMo: Unlocking the Reasoning Potential of Language Model – From Pretraining to Posttraining · GitHub"
[2]: https://github.com/XiaomiMiMo/MiMo?ref=producfront&utm_source=chatgpt.com "GitHub - XiaomiMiMo/MiMo at producfront · GitHub"
[3]: https://mimo.xiaomi.com/paper/?utm_source=chatgpt.com "Files within doc_build/paper/"
