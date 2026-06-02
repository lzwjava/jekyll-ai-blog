---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: AI 基础设施与推理核心要素
translated: true
type: note
---

Question: What does AI infra mean? What about inference / scheduler? What does it involve?

Answer:

**AI infra**（**AI infrastructure** 的缩写）是指为支持人工智能工作负载的全生命周期而构建的 **hardware**、**software**、**networking** 及相关系统的专门组合。这包括开发、training、fine-tuning，尤其是 **deploying/running** AI models（特别是近年来的 large language models 和 generative AI）。

它与传统的 IT infrastructure 不同，因为 AI 工作负载具有极高的 compute-intensive 特性，对 memory 需求巨大，且通常涉及大规模的 parallel processing、海量 datasets 以及 low-latency 要求。

### AI infra 支持的主要阶段

- **Training** — 构建/微调模型（非常依赖 GPU，属于长耗时任务）
- **Inference** — 运行已训练好的模型，为用户生成预测、答案、图像等（这是目前大多数已部署 AI 产品的主要成本来源）

### 在此语境下 "inference" 的含义

**Inference** 是“推理”或“生产”阶段，即预训练模型接收新输入（prompt、图像等）并产生输出的过程。
对于像 GPT、Llama、Claude 等大型模型：

- 它是 autoregressive 的（一次生成一个 token）
- 它是 memory-intensive 的（特别是由于 KV cache 会随 context length 增加而增长）
- 它需要速度快（针对聊天/应用的 low latency）且成本低（通过 high throughput 来服务大量用户）

一旦模型被广泛部署，Inference 通常比 training 消耗更多的总计算资金。

### 什么是 "inference scheduler"（或简称 "scheduler"）

AI infra 中的 **scheduler**（特别是针对 **inference**）是一个软件组件，用于智能地决定：

- 接下来处理哪些请求 (user prompts)
- 如何将多个请求进行 **batch**（批处理）以最大化 GPU utilization
- 如何在并发用户之间分配 GPU memory 和 compute 资源
- 何时抢占 (preempt)、优先处理或剔除请求
- 如何将请求路由到最合适的 GPU/node（考虑负载、prefix caching 等因素）

2025–2026 年的流行示例：

- vLLM scheduler (continuous batching, PagedAttention)
- TensorRT-LLM scheduler
- Run:AI scheduler (enterprise/multi-tenant fairness)
- 自定义的智能 inference schedulers (prefix-cache aware routing, load balancing)

优秀的 schedulers 能显著提升 **throughput** (tokens/second)，降低 **tail latency**，并减少每百万 token 的成本。

### AI infra 通常涉及的内容（核心组件）

- **Compute** — 主要是 NVIDIA GPUs (H100, H200, B200, Blackwell)，有时也包括 AMD Instinct, Google TPUs 或定制 silicon
- **High-speed networking** — 用于连接数千个 GPU 的 InfiniBand 或 ultra-low-latency Ethernet
- **Storage** — 高速 NVMe、分布式文件系统（例如用于 checkpoints, datasets）、用于海量训练数据的 Object storage
- **Orchestration & scheduling** — Kubernetes + operators, Slurm (HPC 风格), 或 Run:AI, KubeRay 等专门平台，以及 cloud-native schedulers
- **Inference engines & serving frameworks** — vLLM, TGI (Text Generation Inference), TensorRT-LLM, SGLang, LMDeploy 等
- **Model optimization** — quantization (4-bit, 8-bit), pruning, distillation, speculative decoding
- **Monitoring & observability** — GPU utilization, queue depth, latency histograms, cost tracking
- **MLOps / platform layer** — experiment tracking, model registry, 模型的 CI/CD, autoscaling

简而言之：当今的 "AI infra" 核心在于构建高效、可扩展且具成本效益的系统，以实现大规模的 **run inference** —— 而 schedulers 是决定你的 GPU cluster 效率是提升 2 倍还是 5 倍的最关键环节之一。

References:

- [What is AI Infrastructure? - IBM](https://www.ibm.com/think/topics/ai-infrastructure)
- [AI Infrastructure: Key Components - Cloudian](https://cloudian.com/guides/ai-infrastructure/ai-infrastructure-key-components-and-6-factors-driving-success)
- [Life of an inference request (vLLM)](https://www.ubicloud.com/blog/life-of-an-inference-request-vllm-v1)
- [LLM Inference Scheduling Overview](https://www.emergentmind.com/topics/llm-inference-scheduling)
- [What Is AI Infrastructure? | NVIDIA Glossary](https://www.nvidia.com/en-us/glossary/ai-infrastructure)
