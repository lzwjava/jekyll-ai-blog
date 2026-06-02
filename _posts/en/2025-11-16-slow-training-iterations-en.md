---
audio: false
generated: true
image: false
lang: en
layout: post
model: openai/gpt-5
title: Understanding Slow Training Iterations
translated: false
type: note
---

Those big jumps are completely normal. They aren’t “slow iterations” — they are **evaluation + checkpoint** iterations, which always take much longer than the normal training steps.

Here’s what’s happening in your log:

### 1. Normal iterations

These are the lines like:

```
iter 100: time 168ms
iter 200: time 170ms
...
iter 900: time 168ms
```

Those are pure forward+backward passes on a single training batch. They stay in a stable range (~160–180 ms), which matches your GPU capability.

### 2. The “slow” ones

Examples:

```
iter 0: time 12543ms
iter 500: time 5985ms
iter 1000: time 5726ms
```

These lines follow exactly after the "**step X**" blocks where NanoGPT does:

* full **validation loss evaluation**
* full **training loss evaluation**
* **saving a checkpoint** to disk (which is often the slowest part, depending on SSD speed)
* sometimes GPU syncs / CPU-GPU sync latency before logging

That entire sequence happens every *eval_interval* or *log_interval* depending on config. In your output, you can see the pattern:

```
step 500: train loss..., val loss...
saving checkpoint
iter 500: loss..., time 5985ms
```

and

```
step 1000: train loss..., val loss...
saving checkpoint
iter 1000: loss..., time 5726ms
```

So *iter 1000 time* isn't the training step's compute time — it's the **combined cost of evaluation + checkpoint writing + the actual training step**.

### Why iter 0 is even larger (~12 seconds)?

The very first step includes:

* full graph compilation/warmup (PyTorch/CUDA kernels)
* loading initial data into GPU
* initial evaluation
* first checkpoint write (if configured)

That’s why it's extra huge.

---

### Summary

Your “slow iterations” are not real training steps. They only happen at evaluation+checkpoint boundaries.

Normal iterations (those that matter for throughput) are ~170ms and stable.

If you want fewer slow spikes, you can reduce:

* `eval_interval`
* `always_save_checkpoint`
* or checkpoint frequency

Let me know if you want recommended settings for faster overall training on 4070/4080/4090.
