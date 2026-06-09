---
audio: false
generated: true
image: false
lang: en
layout: post
title: Keep nanochat, 37% MFU is fine
translated: false
type: note
---

Question: Should I switch back to nanoGPT instead of nanochat since MFU is only ~37% on MI300X?

Answer:

No, switching back to nanoGPT would almost certainly make things worse for your current setup.

What you’re seeing (≈37% MFU on MI300X with FA2 + FP8) is actually **normal to decent for large-scale transformer training**, especially with long sequences (2048–4096) and modern kernels. You are already in the “highly optimized but hardware-limited” region rather than a “framework-limited” region.

### Why nanochat is the better choice here

nanochat (your current stack) already gives you:

* FlashAttention-2 (critical for MI300X efficiency)
* FP8 training path (huge throughput gain)
* Gradient accumulation control
* ROCm-aware environment variables
* MLflow tracking + training pipeline integration

nanoGPT, by contrast:

* Is primarily CUDA-oriented (ROCm support is weaker / less optimized)
* Lacks modern FP8 + kernel fusion optimizations
* Typically uses less efficient attention implementations
* Will likely **reduce throughput and MFU further on MI300X**

So even if nanoGPT feels “simpler,” it is not the performance path for your hardware.

---

### About the 37% MFU number

On MI300X, MFU is often misunderstood. A few important realities:

* 30–45% MFU is common in real training runs with:

  * long context (2048–4096)
  * activation recomputation
  * memory-bound attention
* You are already hitting ~100k tokens/sec, which is strong
* You are likely **not compute-bound anymore**, but:

  * memory bandwidth bound (HBM)
  * kernel launch / pipeline efficiency bound
  * attention + FFN imbalance

So MFU ≠ “bad” here. It just means “not perfectly saturated theoretical FLOPs,” which is almost never achievable in real LLM training.

---

### Why your config is already close to optimal

Your best run:

* bs=64, seq=2048
* FP8 + FA2
* ~101.5k tok/s
* ~37% MFU
* stable memory (~170GB)

This is already a **sweet spot between throughput and stability**. Increasing MFU further usually requires trade-offs.

---

### If you want to push beyond 37% MFU (real options)

Instead of switching frameworks, you’d get more by tuning:

#### 1. Increase compute density per step

* Try slightly larger model width (if memory allows)
* Or increase batch size further (if no instability)

#### 2. Reduce overhead gaps

* Increase `total_batch_size` further to reduce optimizer step frequency
* Reduce eval/sampling even more (you already did partially)

#### 3. Kernel + attention tuning

* Ensure FlashAttention-2 is actually hitting best ROCm kernel paths
* Check if any fallback attention kernels are still used

#### 4. Sequence packing (big one)

If your data allows it:

* pack sequences instead of padding
* this alone can push MFU up several % on MI300X

#### 5. Compilation / graph capture

* torch.compile (if stable in your stack)
* or ROCm graph capture optimizations if supported

---

### Bottom line

* ❌ Don’t switch to nanoGPT for this hardware + FP8 + FA2 setup
* ✅ nanochat is already the correct “modern training stack”
* ⚠️ 37% MFU is not a problem—it’s a sign you’re in a memory/attention bound regime, not an inefficient code regime
* 🚀 Gains now come from **data packing + batch scaling + kernel tuning**, not framework switching

If you want, I can help you push this MI300X setup toward ~45–50% MFU range by systematically tuning batch/seq/accumulation and identifying the real bottleneck.
