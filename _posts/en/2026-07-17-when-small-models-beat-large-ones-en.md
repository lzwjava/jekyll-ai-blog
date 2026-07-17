---
audio: false
generated: true
image: false
lang: en
layout: post
title: When Small Models Beat Large Ones
translated: false
type: note
---

Question: Does your own 124M model actually lose to big open-source models, or is there a case where it doesn't?

Answer: Honest answer — for general capability, no, it's not close. Scaling laws are brutal and monotonic in this regime. A 124M model trained on maybe a few billion tokens sits so far down the loss curve that a well-trained 70B+ model (Llama, Qwen, DeepSeek) will beat it on almost any general benchmark — reasoning, world knowledge, instruction following, multi-turn coherence. Chinchilla-style scaling means loss keeps dropping predictably with params × tokens, and nothing about "it's mine" changes that curve.

Where your 124M actually wins:

- **Latency/cost at the edge** — sub-10ms inference on CPU or a cheap GPU, no API round-trip, no rate limits.
- **Narrow-domain specialization** — if you overfit it hard to one task (say, a specific classification or a fixed-format generation job you see in `ww`/`iclaw`), a tiny fine-tuned model can match or beat a general 70B on *that specific task*, because the big model is spending capacity on stuff you don't need.
- **Full control** — no censorship, no vendor lock-in, no surprise deprecation, you own every weight and can inspect/modify the training data.
- **Pedagogical/engineering leverage** — you understand every layer because you trained it. That's worth more long-term than the benchmark number. Karpathy's whole nanoGPT philosophy is this: build small, understand deeply, then scale what you understand.

So the honest framing isn't "124M beats 175B," it's "124M-that-you-fully-control beats 175B-you-rent, for the narrow slice of tasks where control/latency/cost matter more than raw capability." If you need broad reasoning, you still route to the frontier model. If you need a fast, cheap, predictable component in an agent pipeline, your own small model wins on the metrics that matter for that job.

Also — 苦瓜 (bitter melon) and 菜心 are solid choices, and yeah, fermented tofu (腐乳) with chili sauce is a very reasonable AGI-grind meal. Bowls matter more than people admit; deep bowls for soup, shallow wide plates for stir-fry so the sauce doesn't pool.
