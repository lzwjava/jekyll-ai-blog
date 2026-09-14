---
audio: false
generated: true
image: false
lang: en
layout: post
title: "¥400 Tesla P100: Worth Buying?"
translated: false
type: note
---

Question: **Should you buy a used NVIDIA Tesla P100 for ~¥400?**

Answer: **Yes — if it is the 16GB PCIe version and you want it as a cheap CUDA/LLM tinkering card. But I would *not* buy it as a serious modern training GPU.**

At ¥400 (~$55), the price is low enough that the P100 becomes interesting.

### Why it's actually a fun ¥400 GPU

The P100 16GB has:

* **16GB HBM2**
* **732 GB/s memory bandwidth**
* **3584 CUDA cores**
* ~**9.3–10.6 TFLOPS FP32**
* ~**18–21 TFLOPS FP16**
* PCIe 3.0 x16
* 250W TDP
* Compute Capability **6.0** ([GPUPoet][1])

The killer feature is really **16GB + 732 GB/s for ¥400**.

For experiments like:

```text
CUDA kernels
PyTorch
small LLM inference
quantized 7B/8B models
embedding/reranking
vLLM experiments
distributed-training experiments
CUDA extension development
```

it's a pretty entertaining toy.

A 4-bit ~7B/8B model can fit in 16GB in principle, although context/KV cache and runtime overhead reduce the usable capacity. ([GetDeploying][2])

### But there is a huge catch for you

**Pascal is ancient for modern ML.**

P100 has **no Tensor Cores**, and doesn't have modern BF16/TF32/FP8 hardware. That's a massive difference from V100/A100 and newer GPUs. ([GetDeploying][2])

So don't think:

```text
P100 16GB
    ↓
cheap 16GB AI GPU
    ↓
great local training
```

It's more like:

```text
P100
 ├── 16GB HBM2       ← excellent
 ├── 732 GB/s         ← excellent
 ├── CUDA             ← excellent
 ├── FP32             ← okay
 ├── FP16 CUDA cores  ← okay
 └── Tensor Cores     ← FUCK NO
```

For modern transformer training, the lack of Tensor Cores makes it dramatically less attractive.

### The ¥400 calculation

Current used listings I found are all over the place, but there are P100 16GB cards around **$120–170** and some much higher depending on seller; one tracker currently shows used P100s starting around $74. ([GPUPoet][1])

So **¥400 is cheap enough that I wouldn't worry much about resale value**.

I'd classify it:

| Use                     |    ¥400 P100 |
| ----------------------- | -----------: |
| CUDA experimentation    | 🟢 Excellent |
| 16GB local inference    |      🟢 Good |
| 7B/8B 4-bit LLM         |      🟢 Good |
| GPU programming         | 🟢 Excellent |
| FP32 scientific compute |      🟢 Good |
| Stable Diffusion        |       🟡 Meh |
| Modern LLM inference    |      🟡 Slow |
| LLM fine-tuning         |      🔴 Poor |
| LLM training            | 🔴 Very poor |
| BF16 workloads          |        🔴 No |
| FP8                     |        🔴 No |
| Gaming                  |     🔴 Don't |

### One thing I'd check VERY carefully

Make sure it's:

```text
Tesla P100 16GB PCIe
```

**not**

```text
P100 12GB
P100 SXM2
```

The SXM2 version is a completely different physical situation and isn't something you casually stick into a normal PC. The PCIe 16GB model is the one you want. ([Exxact Corporation][3])

Also remember these are **passively cooled server cards**. NVIDIA specifies ~250W board power, so your case needs serious airflow. ([HPE Support][4])

### My verdict

**At ¥400: buy it if you want a GPU playground.**

Given that you're already doing CUDA/model work, I'd actually consider it worthwhile specifically because **16GB HBM2 + 732GB/s at ¥400 is an unusually cheap way to get another CUDA device**.

But if your actual goal is:

> "I want the maximum AI compute I can get for ¥400–1000"

then I'd **hunt for a used P40 / V100 / 2080 Ti / 3060 12GB / 4060 Ti 16GB deal instead**, depending on local prices.

In particular, **if you can find a V100 16GB for only ~¥600–800 more, I'd take the V100 over the P100 without hesitation**. V100 adds Tensor Cores and is vastly more useful for modern deep learning.

### [NVIDIA Tesla P100 16GB](https://studio-supplies.com/products/nvidia-331011867-01-216985?utm_campaign=openai_catalog&utm_content=product_card&utm_medium=feed&variant=51251263537459&utm_source=chatgpt.com)

*$121.22*

### [HPE Tesla P100 16GB](https://www.newegg.com/hpe-proliant-q0e21a-tesla-p100-16gb-graphics-card/p/2VV-002K-00007?item=9SIB1PGJAB1355&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$167.00*

### [NVIDIA Tesla V100 16GB](https://www.newegg.com/nvidia-tesla-v100-16gb-video-cards-workstation/p/2VV-000H-000P0?item=9SIC6VHKXB9874&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$799.19*

### [NVIDIA Tesla P40 24GB](https://www.newegg.com/p/2RC-00RS-000K5?item=9SIBT5SKT21966&negg_topt=1015&utm_campaign=ais_openai_product_feed&utm_medium=ai_search&utm_source=chatgpt.com)

*$397.99*

**If you send me the exact P100 listing/photo/specs, I can tell you whether that particular ¥400 card is a good buy or a trap.**

References:

* [NVIDIA Tesla P100 specifications](https://www.nvidia.com/?utm_source=chatgpt.com)
* ([GPUPoet][1]) 

[1]: https://gpupoet.com/gpu/learn/card/nvidia-tesla-p100?utm_source=chatgpt.com "NVIDIA Tesla P100 16GB Specs, Benchmarks & Pricing"
[2]: https://getdeploying.com/gpus/nvidia-p100?utm_source=chatgpt.com "P100 Cloud Pricing: Compare 6+ Providers (2026)"
[3]: https://www.exxactcorp.com/blog/HPC/taking-a-look-at-the-nvidia-tesla-p100-gpu-accelerator-for-pcie-servers?utm_source=chatgpt.com "NVIDIA Tesla P100 GPU Accelerator For PCIe Servers"
[4]: https://support.hpe.com/hpesc/public/docDisplay?docId=a00114012en_us&docLocale=en_US&page=NVIDIA_Tesla_P100_GPU_Blade.html&utm_source=chatgpt.com "NVIDIA Tesla P100 GPU Blade | XC50-LC Hardware ..."
