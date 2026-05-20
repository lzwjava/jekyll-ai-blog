---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI300X 运行 DeepSeek V4 Flash
translated: true
type: note
---

**问题：** 给定一块拥有 192GB 显存的 AMD MI300X，在当前（2026 年 5 月）HuggingFace 热门趋势和 OpenRouter 排名中，用它可以做哪些最令人印象深刻且切实可行的事情？

**回答：**

自原始提示编写以来，格局已发生巨大变化。以下是当前真正热门的内容以及你的 MI300X 能用来做什么。

---

## 当前排名中主导的内容

截至 2026 年 5 月初，OpenRouter 显示 Anthropic 以 1.6T 周 tokens 领先，OpenAI 为 518B，Google 为 514B——60 多个提供商提供 400 多个活跃模型。

OpenRouter 工具调用排名中最热门的模型是 **DeepSeek-V3.2**，它引入了 DeepSeek Sparse Attention (DSA)，一种细粒度稀疏注意力机制，在保持长上下文场景质量的同时降低训练/推理成本——据报道性能达到 GPT-5 级别，并在 2025 IMO 和 IOI 中获得金牌。

截至 2026 年 5 月的开放权重前沿模型：

在 2026 年 5 月 12 日的 LiveBench 快照中，**Kimi K2.6 Thinking** 以 78.57 Coding Avg 和 58.33 Agentic Coding Avg 领先所有开源模型。其架构为 MoE，总参数约 1T / 32B 活跃参数。DeepSeek V4 Pro（总参 1.6T / 活跃 49B，MIT 许可证）和 GLM 5.1 在 agentic coding 上紧随其后。**DeepSeek V4** 于 2026 年 4 月 24 日发布，上下文窗口为 1M tokens。

来自智谱 AI 的 **GLM-5.1** 是一个 744B MoE，40B 活跃参数，使用 DeepSeek Sparse Attention 在 28.5 万亿 tokens 上训练——专为长周期 agentic 工程任务设计，能在数百轮和数千次工具调用中保持生产性。

---

## 适合你单张 MI300X (192GB) 的模型

以下是当今前沿模型与你硬件的真实映射：

| 模型 | 架构 | 总参数 | 活跃参数 | VRAM 需求 (Q4_K_M) | 是否合适？ |
|---|---|---|---|---|---|
| **DeepSeek V3.2** | MoE | 671B | 37B | ~390 GB (FP16), ~150GB (Q2_K) | Q2_K 勉强；FP16 需要 8× |
| **DeepSeek V4 Flash** | MoE | 284B | 13B | ~160 GB (Q4_K_M) | ✅ 舒适容纳 |
| **Kimi K2.6** | MoE | ~1T | 32B | 单卡过大 | ❌ 需要多 GPU |
| **GLM-5.1** | MoE | 744B | 40B | 单卡过大 | ❌ 需要多 GPU |
| **Qwen 3.6 27B** | Dense | 27B | 27B | ~17 GB | ✅ 轻松容纳，快速 |
| **DeepSeek R1 671B** | MoE | 671B | 37B | 与 V3 相同 | 仅 Q2_K |

**2026 年你显卡的真正甜区：**

**DeepSeek V4 Flash**——总参 284B，每个 token 仅 13B 活跃，1M token 上下文窗口——专为像你这样的部署场景设计的高效优化 MoE。以 ~160GB Q4_K_M 占用，剩余约 30GB 用于 KV 缓存。仅有 13B 活跃参数，吞吐量接近 13B 密集模型（估计 80-120 t/s），但质量远超后者。

---

## 你实际能做的最令人印象深刻的事情

### 1. 本地运行前沿编码 Agent——零 API 成本

**DeepSeek V4** 为自托管 GPU 部署提供了最佳的推理成本性能比，工具调用可靠性相比 V3 有大幅提升——部分函数调用或格式错误的 JSON payload 大大减少。它是团队在 GPU 集群上自托管、需要前沿编码性能的首选推荐。

使用你的 MI300X 运行 DeepSeek V4 Flash（适合 192GB），你将获得一个本地的 **Claude Code 级别编码 agent**。无速率限制，无每 token 成本，完整 1M 上下文用于整个代码库。通过 llama-server 的 OpenAI 兼容端点将其连接到你的 `ww`/`iclaw`/`zz` CLI 工具：

```bash
# llama.cpp server, OpenAI 兼容，将 Claude Code 指向它
llama-server \
  --model DeepSeek-V4-Flash-Q4_K_M.gguf \
  --n-gpu-layers 999 \
  --ctx-size 65536 \
  --host 0.0.0.0 --port 8080

# 然后在 Claude Code 或任何 OpenAI 兼容客户端中：
export OPENAI_BASE_URL=http://localhost:8080/v1
export OPENAI_API_KEY=dummy
```

### 2. 以 Q2_K 运行 DeepSeek R1 671B——本地完整推理模型

在 Q2_K（约 150 GB）下，DeepSeek R1 勉强塞入。这是一个在数学和编码基准测试中达到前沿水平的推理/思考模型。你将获得链式思维推理，速度约 5-10 t/s——缓慢但零成本且完全私有。这正是云提供商收费 $15-30/M tokens 的服务。

### 3. 使用 LoRA 微调 70B 模型——全精度

192GB 允许你在 **bf16 下使用 LoRA 微调 70B 模型**，无需分片到 CPU。这就是单张 MI300X 与消费级设置的区别：

```python
# QLoRA on 70B——192GB 舒适容纳
from transformers import AutoModelForCausalLM
import torch

model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen3-72B",
    torch_dtype=torch.bfloat16,
    device_map="cuda"
)
# 全 70B 在 bf16 下 = ~140GB。LoRA 优化器状态剩余 52GB 空间。
```

使用 LoRA rank 64，你可以用自己的数据（银行领域、代码风格等）微调 72B 模型——这通常需要 4× A100。

### 4. 为你的团队提供私有 OpenAI 兼容 API 服务

单张 MI300X 可以通过 vLLM 以 120,000 tokens 上下文运行 Llama 3.1 70B——这是一个完整的私有 API 服务器，支持长上下文 RAG、文档分析和多轮 agent，可同时服务多个用户。

```bash
docker run --device=/dev/kfd --device=/dev/dri \
  rocm/vllm-dev:latest \
  vllm serve Qwen/Qwen3-72B \
  --tensor-parallel-size 1 \
  --max-model-len 120000 \
  --gpu-memory-utilization 0.85
```

### 5. 从头训练 GPT-2 规模 → Qwen3-8B 规模

你已经在 H200/H100 上训练过 GPT-2。在具有 192GB 的 MI300X 上，你可以将其扩展到 **从头开始训练 8B 参数模型**，使用 bf16，无需任何内存技巧：

- 8B 模型 bf16 = ~16GB 权重
- Adam 优化器状态 = ~64GB
- 激活 + 梯度 = ~60GB
- **总计：~140GB**——有富余空间

这是在单卡上完整的 Llama-3/Qwen3-8B 规模预训练运行。Karpathy 的 nanoGPT 可直接扩展。

---

## 诚实的优先级顺序

鉴于 OpenRouter 排名和 HuggingFace 趋势的指向，以下是你今天应该用 MI300X 实际做的事情：

1. **通过 llama.cpp 运行 DeepSeek V4 Flash (284B MoE, 13B 活跃)**——当前最佳单卡前沿模型。适合、快速、前沿质量。
2. **使用 LoRA 在银行领域数据上微调 Qwen3 72B**——192GB 使其单卡完成，无需基础设施麻烦。
3. **运行 DeepSeek R1 671B Q2_K**——用于需要本地链式思维的数学/推理任务。
4. **为团队提供 vLLM 服务器**——在 120K 上下文下为 5-10 个并发用户提供 Qwen3 72B 服务。
5. **将 nanoGPT 扩展到 8B 预训练**——你现在拥有从“玩具”到“真实模型”领域的 VRAM。

最令人印象深刻的炫技：一个私有的、零成本的、前沿质量的编码 agent（DeepSeek V4 Flash）在本地运行，具有 1M token 上下文用于完整代码库分析。无需 Claude/GPT API 账单。无速率限制。完全归你所有。

---

参考资料：

- [Performance of llama.cpp on AMD GPU (MI300X) — GitHub Discussion #14640](https://github.com/ggml-org/llama.cpp/discussions/14640)
- [Best Open Source Self-Hosted LLMs for Coding — Pinggy (May 2026)](https://pinggy.io/blog/best_open_source_self_hosted_llms_for_coding/)
- [Best Open-Source LLMs for Agentic Coding 2026 — MindStudio](https://www.mindstudio.ai/blog/best-open-source-llms-agentic-coding-2026)
- [The Best Open-Source LLMs in 2026 — BentoML](https://www.bentoml.com/blog/navigating-the-world-of-open-source-large-language-models)
- [OpenRouter Homepage — Live Rankings](https://openrouter.ai/)
- [Llama.cpp Meets Instinct: AMD ROCm Blog](https://rocm.blogs.amd.com/ecosystems-and-partners/llama-cpp/README.html)