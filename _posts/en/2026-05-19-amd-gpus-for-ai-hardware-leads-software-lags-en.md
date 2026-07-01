---
audio: false
generated: true
image: false
lang: en
layout: post
title: "AMD GPUs for AI: Hardware Leads, Software Lags"
translated: false
type: note
---

**Question:** AMD GPUs vs NVIDIA GPUs for AI/ML workloads — are AMD GPUs roughly 70% of NVIDIA's capability? Is AMD Developer Cloud via DigitalOcean a good option?

**Answer:**

The "70%" figure is a rough ballpark but it depends heavily on what you're measuring. Here's the breakdown:

## AMD MI300X vs NVIDIA H100 — Real Numbers

| Metric | AMD MI300X | NVIDIA H100 SXM | AMD % of NVIDIA |
| --- | --- | --- | --- |
| FP16 TFLOPS | 1307 | 989 | **132%** ✅ |
| BF16 TFLOPS | 1307 | 989 | **132%** ✅ |
| HBM Memory | **192 GB** | 80 GB | **240%** ✅ |
| Memory BW | 5.3 TB/s | 3.35 TB/s | **158%** ✅ |
| FP8 TFLOPS | 2614 | 1979 | **132%** ✅ |

**On paper, MI300X beats H100 raw specs.** So where does the "70%" feeling come from?

## The Real Gap: Software Stack

The bottleneck is **ROCm vs CUDA**:

- **CUDA ecosystem**: 15+ years of optimization, cuDNN, cuBLAS, FlashAttention, Triton — all battle-tested
- **ROCm**: catching up fast but kernel-level optimizations are ~1-2 years behind
- **PyTorch on ROCm**: works, but custom CUDA kernels don't port automatically
- **FlashAttention**: ROCm port exists but historically slower
- **Triton**: AMD support improved significantly in 2024

So the "70%" is really about **software efficiency**, not hardware specs. Raw FLOPS AMD wins or ties. Actual training throughput on real workloads — maybe 70-85% of H100 depending on the model.

## AMD Developer Cloud (via DigitalOcean)

This is the **Instinct MI300X** offering. Key facts:

- MI300X has **192GB HBM3** — this is a massive advantage for large model inference (fits 70B models in full precision on one card)
- Good for: inference, fine-tuning, models that are memory-bound
- Watch out for: custom CUDA kernels in your code — need ROCm ports
- `torch.compile()` + ROCm has improved a lot in PyTorch 2.x

## For Your Use Case (Training, Fine-tuning, Agents)

```bash
# Check if your stack is ROCm-compatible
pip install torch --index-url https://download.pytorch.org/whl/rocm6.0

# Most things just work:
# ✅ PyTorch training loops
# ✅ HuggingFace Transformers
# ✅ LoRA / PEFT
# ✅ vLLM (has ROCm support)
# ⚠️  Custom CUDA kernels → need HIP port
# ⚠️  Flash Attention → use `flash-attn` ROCm fork or `xformers`
```

## Bottom Line

- **For training nanoGPT-scale models**: AMD works fine, ROCm + PyTorch is solid
- **For LoRA fine-tuning**: works well, HuggingFace stack is compatible
- **For inference with large models**: MI300X's 192GB VRAM is actually a **killer advantage** over H100
- **Cost**: typically 30-50% cheaper than H100 equivalents
- **Gotcha**: if you hit ROCm-incompatible ops, debugging is harder than CUDA

The channel you found sounds legit — AMD + DigitalOcean partnership is real. Worth testing for your workloads. The 192GB VRAM alone makes it compelling for running 70B models locally.
