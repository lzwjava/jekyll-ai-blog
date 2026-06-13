---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tencent Hunyuan Inference Engine Overview
translated: false
type: note
---

**Question:** What is Tencent Hunyuan (混元)? Give an intro to the model family, and what do we know about performance optimizations for their inference engine on NVIDIA H20 and Blackwell (B200) GPUs?

---

## Answer: Tencent Hunyuan (混元) — Overview & Inference Engine Deep Dive

---

### What is Hunyuan?

Tencent developed Hunyuan (混元) as their large language model family, powering conversational AI and content generation across their products. It's not one model — it's a full stack: LLMs, image gen, video gen, 3D, OCR, and agents. Think of it as Tencent's answer to what OpenAI and Google are building, but deeply integrated into WeChat, QQ, and Tencent Cloud.

Hunyuan LLMs cover text-to-text, text-to-image, text-to-video, and multimodal understanding.

---

### The Model Family (current state, mid-2025)

**Hunyuan-Large (Hunyuan-MoE)** — the original flagship open-source release. The flagship model, Hunyuan-Large (Hunyuan-MoE-A52B), has 389 billion total parameters with 52 billion activated, making it a leading open-source Transformer-based MoE model.

**Hunyuan-TurboS** — the most architecturally interesting model. Released on February 27, 2025, TurboS adopts a Hybrid-Mamba-Transformer fusion mode, effectively reducing the computational complexity and KV-Cache occupancy of the traditional Transformer architecture, significantly lowering training and inference costs.

The architecture details: TurboS combines 57 Mamba2 layers with 7 Attention layers and 64 Feed-Forward Network layers in a strategic "AMF" and "MF" block pattern. KV cache and FFNs use an MoE structure. Pre-trained on 16T high-quality tokens, it supports a 256K context length and is the first industry-deployed large-scale Mamba model.

This is significant: linear complexity (O(N) vs O(N²)) for the Mamba layers means long-context inference costs fundamentally less compute. The 7 attention layers are kept for global context capture where Mamba's recurrence isn't enough.

**Hunyuan-T1** — the reasoning model (slow-thinking). The Hunyuan-T1 official version is based on the TurboS fast-thinking base, which Tencent describes as the world's first ultra-large-scale Hybrid-Transformer-Mamba MoE model. Through large-scale post-training, its reasoning ability has been significantly expanded.

**Hunyuan-A13B** — the efficient open-source release. The Hunyuan-A13B model features 80 billion total parameters with 13 billion active parameters, and supports a maximum context length of 256K tokens.

**Hunyuan 2.0** (Dec 2025): Built on a MoE architecture with 406 billion total parameters and 32 billion active parameters, supporting a 256K context window, with improvements in pretraining data and RL strategies for math, science, and coding.

Chatbot Arena standing: On Chatbot Arena, Hunyuan TurboS has climbed to the top eight globally, ranking second only to DeepSeek in China.

---

### Inference Engine — What They Built

Tencent presented at GTC 2025 on building a high-performance inference engine for Hunyuan using TensorRT-LLM. From the GitHub and GTC materials, the key optimizations are:

#### 1. **CLA (Cross-Layer Attention) for KV-Cache Compression**

The introduction of a new CLA structure significantly reduces GPU memory usage, achieving 50% savings in the KV-Cache portion, which ensures efficient handling of long text scenarios. This is critical for MoE models at scale — KV cache is often the memory bottleneck at high batch sizes.

#### 2. **FP8 Quantization**

By employing FP8 quantization, they achieve a 50% reduction in memory usage compared to traditional FP16/BF16 quantization, while maintaining precision and resulting in a 70% increase in throughput.

#### 3. **TRT-LLM vs vLLM**

By leveraging the efficient operators at the core of TRT-LLM, the performance of the TRT-LLM solution surpasses that of vLLM by over 30%. TRT-LLM is their production default; they initially open-sourced the vLLM path.

#### 4. **CUDA Graph Optimization**

From the deployment config:

```yaml
use_cuda_graph: true
cuda_graph_padding_enabled: true
cuda_graph_batch_sizes: [1, 2, 4, 8, 16, 32]
```

This eliminates CPU-GPU launch overhead — critical for latency at small batch sizes.

#### 5. **Training Parallelism Stack (AngelPTM / AngelRL)**

On the training side, they comprehensively integrate all model parallelism techniques including Tensor Parallelism (TP), Pipeline Parallelism (PP), Expert Parallelism (EP), Context Parallelism (CP), and sequence concatenation optimization to improve efficiency. The inference framework is called **AngelHCF**.

---

### H20 vs B200 — GPU Platform Context

**H20** is NVIDIA's China-export-compliant chip (cut-down Hopper). Hunyuan-Large is explicitly tested on H20 — tested on H20, LoRA fine-tuning requires at least 8 GPUs. It's the dominant inference GPU inside Chinese data centers right now.

For the broader **Blackwell B200** story: NVIDIA Blackwell B200 cost per million tokens dropped from $0.11 at launch to $0.02 on GPT-OSS-120B within two months — a 5x improvement from software alone.

On disaggregated serving (prefill/decode split), which Tencent's large-scale setup benefits from: NVIDIA's disaggregated serving contributed to a nearly 1.5x increase in throughput per GPU compared to traditional aggregated serving using in-flight batching on a DGX B200 system — more than 5x cumulative improvement compared to in-flight batching on a DGX H200 system.

Blackwell FP4 support is the next frontier. Blackwell's architecture supports advanced precision modes (FP8, FP4), with B200 and B300 throughput over 2x in TF32, FP16, and FP8 compared to the last generation H200. It also features a new transformer engine that supports FP4.

---

### Where "Hunyuan 3.0" Fits

Note: as of my search, the term "Hunyuan 3.0" doesn't appear in public docs — it may refer to **Hunyuan 2.0** (Dec 2025) as their current-gen, or to an internal versioning not yet public. The inference engine work is centered around **TensorRT-LLM + AngelHCF**, with the optimization stack above being the production baseline.

---

### TL;DR for You

The interesting engineering bets Tencent made:

- **Mamba + MoE hybrid** is the real architectural bet — linear complexity at scale, first real deployment of Mamba in a 100B+ MoE. Worth studying the TurboS paper: [arxiv 2505.15431](https://arxiv.org/abs/2505.15431)
- **CLA** (Cross-Layer Attention) for KV cache reduction — same direction as GQA/MQA but structurally different
- **FP8 quantization** as the standard baseline, with FP4 on Blackwell coming
- **Disaggregated serving** (prefill/decode split) is where the real throughput gains come from at scale
- **AngelHCF** is Tencent's internal inference framework layered on top of TRT-LLM — not fully open-sourced but the GTC 2025 deck covers the architecture

References:

- [Tencent-Hunyuan-Large GitHub](https://github.com/Tencent-Hunyuan/Tencent-Hunyuan-Large)
- [Hunyuan-TurboS paper (arxiv 2505.15431)](https://arxiv.org/abs/2505.15431)
- [Hunyuan-TurboS GitHub](https://github.com/Tencent-Hunyuan/Hunyuan-TurboS)
- [GTC 2025 session: Tencent HunYuan inference engine](https://www.nvidia.com/en-us/on-demand/session/gtc25-S71563/)
- [NVIDIA Blackwell inference records (MLPerf)](https://developer.nvidia.com/blog/nvidia-blackwell-ultra-sets-new-inference-records-in-mlperf-debut/)
- [Hunyuan-A13B on HuggingFace](https://huggingface.co/tencent/Hunyuan-A13B-Instruct)
