---
audio: false
generated: true
image: false
lang: en
layout: post
title: V100 Tensor Cores for Training
translated: false
type: note
---

Question: What's the V100 GPU, architecturally, and why does it matter for training?

Answer:

**Volta (GV100), 2017.** First NVIDIA chip with dedicated matmul hardware (Tensor Cores) instead of relying purely on FP32 CUDA cores for deep learning.

**Raw specs (SXM2 variant, the one you'd actually rent/cluster):**
```
CUDA cores:      5,120  (64 FP32 + 32 FP64 + 8 Tensor Cores per SM × 80 SMs)
Tensor Cores:    640    (8 per SM, first-gen — FP16 in, FP32 accumulate)
FP64:            7.8 TFLOPS
FP32:            15.7 TFLOPS
FP16 (Tensor):   125 TFLOPS   <- this is the number that matters for training
Memory:          16 or 32 GB HBM2
Mem bandwidth:   900 GB/s
NVLink:          300 GB/s (6 links, 50 GB/s each)
TDP:             300W
```

**Why Tensor Cores matter — the actual math:**

Each tensor core does a 4x4x4 FMA per cycle:
```
D[4x4] = A[4x4] @ B[4x4] + C[4x4]
```
That's 64 multiply-adds = 128 FLOPs per tensor core per cycle. At ~1.5GHz × 640 cores × 128 FLOPs = ~125 TFLOPS FP16, matching the datasheet. Compare to 15.7 TFLOPS FP32 on the same die — that's the ~8x speedup mixed precision buys you, which is why AMP (`torch.cuda.amp` / `bf16` on newer cards) exists at all.

**Arithmetic intensity check (roofline):**
```python
flops = 125e12       # tensor FLOPS/s
bw    = 900e9        # bytes/s
ridge_point = flops / bw   # FLOPs per byte to be compute-bound
# ≈ 139 FLOPs/byte
```
Below ~139 FLOPs/byte of data moved, you're memory-bound, not compute-bound. Small batch sizes, small hidden dims, or attention with short sequences on V100 will bottleneck on HBM2 bandwidth before they touch peak TFLOPS. This is *the* reason batch size and fused kernels matter more than raw TFLOPS on V100 — you're rarely near the roofline.

**Where it sits relative to what you're actually using:**
```
           V100        A100        H100        MI300X
FP16      125 TFLOPS  312 TFLOPS  989 TFLOPS   ~1300 TFLOPS (FP16/BF16 dense)
Mem BW    900 GB/s    2 TB/s      3.35 TB/s    5.3 TB/s
Memory    32 GB       80 GB       80 GB        192 GB
NVLink    300 GB/s    600 GB/s    900 GB/s     896 GB/s (Infinity Fabric)
No native BF16 support (only FP16) — no TF32 either (that's Ampere+)
```

**Practical implication for you:** if you ever land on V100 nodes (cheap spot instances, older clusters), you lose BF16 (FP16-only means you need loss scaling — dynamic scaler in `torch.cuda.amp.GradScaler`, not just autocast), lose the 80GB+ memory headroom you're used to on MI300X, and NVLink bandwidth is 1/3 of A100's. For a GPT-2 760M scale model this is still fine — you fit comfortably in 32GB with room for decent batch size — but you won't get anywhere near MI300X's tokens/sec.

References:
- [NVIDIA Tesla V100 Architecture Whitepaper](https://images.nvidia.com/content/volta-architecture/pdf/volta-architecture-whitepaper.pdf)
- [Cornell Virtual Workshop — Tensor Cores](https://cvw.cac.cornell.edu/gpu-architecture/gpu-example-tesla-v100/tensor_cores)
- [NVIDIA V100 Datasheet](https://images.nvidia.com/content/technologies/volta/pdf/volta-v100-datasheet-update-us-1165301-r5.pdf)
