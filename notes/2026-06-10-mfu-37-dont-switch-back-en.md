---
audio: false
generated: true
image: false
lang: en
layout: post
title: "MFU 37%: Don't Switch Back"
translated: false
type: note
---

Question: Should I switch back to nanoGPT from nanochat, given that the Model Flops Utilization (MFU) on the AMD MI300X is only 37%?

Answer: Switching back to the original nanoGPT will likely **not** solve your low MFU issue, and it might actually make performance worse.

An MFU of 37% on an AMD MI300X for a relatively small model (~760M parameters, based on your run name) is actually quite standard, if not expected, for this setup. Moving back to vanilla nanoGPT will likely degrade your throughput because it lacks the out-of-the-box optimizations required to make AMD hardware perform well.

Here is a breakdown of why your MFU is at 37% and how you can actually increase it without abandoning your current codebase.

### Why Your MFU is 37% (And Why nanoGPT Won't Fix It)

* **Model Size vs. Hardware Capacity:** The MI300X is an absolute monster with 192 GB of HBM3 memory and immense compute bandwidth. A 760M parameter model is too small to fully saturate the GPU's compute cores at a batch size of 64. The GPU spends a significant amount of time waiting for memory movement rather than doing actual math (it is memory-bandwidth bound, not compute bound).
* **Kernel Launch Overhead:** PyTorch on ROCm (AMD) historically suffers from higher kernel launch overheads than CUDA. Small models mean fast-executing kernels, which paradoxically makes the framework overhead a massive bottleneck. nanoGPT suffers from this exact same framework overhead.

---

### How to Actually Push MFU Higher in nanochat

Instead of switching codebases, you can maximize your MI300X hardware utilization by adjusting your training strategy:

#### 1. Increase the Matrix Size (Kernel Saturation)

To get higher MFU, you need to give the GPU larger matrices to crunch so it spends more time computing and less time moving data.

* **Increase `--device-batch-size`:** Your profile shows that `bs=64, total=1M` hit your highest MFU (37.5%). If you have 192 GB of VRAM and are only using 170 GB, try pushed the limit. If your memory allows, try `--device-batch-size=128` (adjusting gradient accumulation downward to keep your total batch size consistent).
* **Increase Sequence Length:** Notice that moving from `seq=2048` to `seq=4096` kept your MFU relatively stable while scaling workload. If your dataset allows it, training on longer sequences naturally increases MFU because attention calculation scales quadratically ($O(N^2)$), giving the compute engines more work to do relative to memory transfers.

#### 2. Use PyTorch Compilation (`torch.compile`)

If you aren't already using it, compilation is the single best weapon against kernel launch overhead. It fuses operations together, which drastically reduces the time the MI300X spends idling between operations. Check if your `scripts.base_train` script supports a `--compile` flag.

#### 3. Maximize FP8 Tensor Core Usage

Ensure that your network dimensions (embedding dimension, intermediate hidden dimension, vocabulary size) are all strictly multiples of **64** or **128**. FP8 execution units on AMD hardware require strict alignment to hit maximum hardware capabilities. If your dimensions are unaligned, the hardware falls back to slower emulation paths, dragging down your MFU.
