---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 4090 AI Workload Limits
translated: false
type: note
---

Question: What's the RTX 4090 (24GB) actually good for in terms of training/inference workloads, and what are its real specs/limits?

Answer:

**Silicon**: AD102 (Ada Lovelace), TSMC 4N (5nm-class). 16384 CUDA cores, 512 4th-gen Tensor cores, 128 3rd-gen RT cores. No NVLink — this matters, it means no fast GPU-to-GPU interconnect if you ever go multi-4090, you're stuck with PCIe 4.0 x16 (~32GB/s bidirectional) for cross-GPU comms.

**Memory**: 24GB GDDR6X, 384-bit bus, ~1008 GB/s bandwidth. Compare to your MI300X (192GB HBM3, ~5.3TB/s) — the 4090 is ~5.3x less bandwidth and 8x less capacity. Totally different class of card: 4090 is a prosumer inference/fine-tune box, MI300X is a training node.

**Compute**: ~82.6 TFLOPS FP32 dense, ~165 TFLOPS FP16 tensor dense (~330 with sparsity), no native FP64 to speak of (1:64 ratio, useless for scientific compute). 450W TDP, PCIe 4.0 x16.

**What actually fits in 24GB**:

```
# rule of thumb: params * bytes_per_param + kv_cache + activations

# 7B model, fp16 inference
7e9 * 2 bytes = 14GB weights
+ KV cache (grows with context, ~1-2GB for 4k ctx on 7B)
+ activations/overhead
→ fits comfortably, room for decent batch size

# 7B QLoRA fine-tune (4-bit base + fp16 adapters)
7e9 * 0.5 bytes = 3.5GB base
+ optimizer states for LoRA params only (small)
+ activations
→ easily fits, can push to 13B QLoRA too

# 13B full fine-tune fp16 (weights + grads + adam states)
13e9 * 2 (weights) + 13e9 * 2 (grads) + 13e9 * 4*2 (adam m,v fp32)
≈ 26 + 26 + 104 = way over 24GB
→ not happening without offload (DeepSpeed ZeRO-Offload / CPU) or LoRA
```

So on a single 4090: full fine-tuning tops out around 1-3B params (with gradient checkpointing pushing higher), QLoRA/LoRA gets you comfortably to 13B-34B, and pure inference (especially quantized, GGUF/AWQ/GPTQ 4-bit) can run 30B-70B models if you're patient about speed and use CPU offload for the overflow.

For your stack — training GPT-2 760M is trivially small for this card even at fp32 with room for large batches. If you're prototyping architecture changes before scaling to MI300X, the 4090 is the right dev box: fast iteration, cheap power draw, and numerically identical results to what you'd get on datacenter cards for anything that fits.

**Practical gotcha**: GDDR6X on the 4090 runs hot and power-hungry per GB compared to HBM — under sustained full-tensor-core load you'll want to watch thermals if it's in a dense build, and `nvidia-smi -pl` to cap power if you're running 24/7 unattended training jobs.

```bash
nvidia-smi --query-gpu=name,memory.total,memory.used,utilization.gpu,power.draw,temperature.gpu --format=csv
```

References:

- [NVIDIA RTX 4090 Specifications](https://www.nvidia.com/en-us/geforce/graphics-cards/40-series/rtx-4090/)
- [Ada Lovelace Architecture Whitepaper](https://images.nvidia.com/aem-dam/Solutions/geforce/ada/nvidia-ada-gpu-architecture.pdf)
