---
audio: false
generated: true
image: false
lang: en
layout: post
title: Scaling AI Experimentation Across Organizations
translated: false
type: note
---

Your friend is partly right, but the scale depends on **who you're talking about**.

For a startup or university lab:

* 20–30 concurrent training runs is already a lot.
* If each run uses 8×H100 for 3 days, that's already thousands of GPU-hours.
* Most teams don't have the budget to brute-force everything.

For frontier labs (OpenAI, Anthropic, Google DeepMind, Meta):

* It's not one engineer launching 1,000 full pretraining jobs.
* Instead, there are **hundreds of researchers**, each running many experiments.
* Most experiments are **small-scale ablations**, not full trillion-token training runs.
* Across the entire organization, there can absolutely be **hundreds or even thousands of experiments running simultaneously**.

For example, before committing to a major GPT-scale training run, researchers might explore:

* learning rate schedules
* optimizer variants
* batch size
* weight decay
* architecture changes
* tokenizer changes
* data mixtures
* curriculum learning
* MoE routing
* RLHF/RFT settings
* inference kernels

Most of these are tested on **small models** (e.g. 100M–1B parameters) or short training runs. Only the most promising configurations get promoted to the expensive 100B+ parameter training.

So the expensive part is **not** "1,000 GPT-5 trainings." It's:

* 900 cheap experiments
* 90 medium experiments
* 9 large-scale validation runs
* 1 final production training

That's how modern ML research is usually structured.

So I'd slightly revise your statement:

> Top frontier AI labs often have hundreds or even thousands of experiments running in parallel across the organization. Most are small ablation studies or prototype runs, while only a handful are full-scale pretraining jobs.

Your friend's point about cost is also valid: **time, GPUs, electricity, storage, and engineering effort are all major constraints.** The reason frontier labs can sustain so many experiments is that they have enormous GPU clusters and many research teams operating in parallel, not because every experiment is a massive training run.
