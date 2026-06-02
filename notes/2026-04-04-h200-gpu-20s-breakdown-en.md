---
audio: false
generated: true
image: false
lang: en
layout: post
title: H200 GPU 20s Iteration Breakdown
translated: false
type: note
---

Question: Why does one training iteration take 20 seconds on a DigitalOcean H200 GPU?

Answer:
Twenty seconds per iteration might feel slow, but it is actually expected and **incredibly fast** for the sheer volume of work the GPU is processing.

Here is the breakdown of why it takes ~21 seconds:

### 1. You are doing 64 micro-steps per "iteration"

In your config, `gradient_accumulation_steps = 64`. An "iteration" in nanoGPT is only logged *after* all 64 accumulation steps are completely finished.

* **Time per micro-step:** 21 seconds ÷ 64 steps = **~0.32 seconds** per forward/backward pass.
* Processing a batch of 16 sequences (16,384 tokens) through a massive 1.5 Billion parameter model in 0.32 seconds is top-tier performance.

### 2. The math proves the H200 is crushing it

* **Tokens per iteration:** 16 (batch) × 1024 (block) × 64 (accumulation) = **1,048,576 tokens**.
* **Throughput:** 1,048,576 tokens ÷ 21 seconds = **~49,900 tokens per second**.
* Pushing ~50k tokens per second through a 1.5B model means the H200 is fully saturated and highly efficient. For comparison, an older A100 GPU would likely take over a minute for this exact same iteration.

### 3. The 164% MFU Mystery

Seeing a Model FLOPs Utilization (MFU) of 164% looks like an error, but it is actually a hardcoded artifact in the code. The `nanoGPT` codebase calculates MFU based on the peak performance of an **A100 GPU** (312 TFLOPs). Because your H200 is vastly more powerful, nanoGPT calculates the math and reports >100% relative to what an A100 could achieve.

### How to adjust the pacing

If you want the console to update more frequently (so it doesn't look frozen for 20 seconds at a time), you can lower the `gradient_accumulation_steps`.

For example, if you change `gradient_accumulation_steps = 16`, an iteration will only take **~5 seconds**. However, note that doing this drops your effective batch size to ~262k tokens, meaning you would need to increase `max_iters` to 40,000 to still cover the full 10B dataset. Your current 21-second setup is perfectly optimal for GPU utilization.
