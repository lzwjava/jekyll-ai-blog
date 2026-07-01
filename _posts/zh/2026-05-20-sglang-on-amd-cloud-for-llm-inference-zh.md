---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang在AMD云上进行LLM推理
translated: true
type: note
---

**问题：** 什么是 SGLang，为什么它在 AMD 开发者云上作为可选方案提供？

**回答：**

SGLang（结构化生成语言）是一个**高性能 LLM 推理服务框架**——可以将其视为 vLLM 的有力竞争对手，但采用不同的架构理念并具备一些突出的技术优势。

## SGLang 是什么

SGLang 是一个用于大型语言模型和视觉语言模型的高效服务引擎。其核心推理优化包括预填充-解码分离、大规模专家并行、零开销调度器和推测解码。它在业界被广泛用于服务于前沿模型，如 Grok3 和 DeepSeek V3/R1。

该项目由 Lianmin Zheng（伯克利 → xAI）领导。SGLang 是每天处理数万亿令牌的高性能推理基础设施，并于 2025 年初加入 PyTorch 生态系统。它在 NVIDIA 和 AMD GPU 上为 DeepSeek V3/R1 模型提供即日支持，并包含针对 DeepSeek 的专用优化。

## 关键技术特性（对比 vLLM）

| 特性 | SGLang | vLLM |
| --- | --- | --- |
| **调度器** | 零开销，RadixAttention 实现 KV 缓存复用 | 良好但开销更高 |
| **PD 分离** | 一流支持 | 后添加 |
| **MoE 专家并行** | 大规模 EP，支持 96+ GPU | 正在追赶 |
| **推测解码** | 支持 | 支持 |
| **结构化输出** | 原生（名称即体现） | 通过引导解码实现 |

**RadixAttention** 是 SGLang 的关键差异化特性——它能在共享同一前缀（系统提示、少样本示例）的请求间自动复用 KV 缓存。这对于生产环境中许多请求共享长前缀的工作负载而言，在吞吐量方面具有巨大优势。

## 为什么 AMD 开发者云特别使用它

ROCm 7 引入了鲁棒的分布式推理方法，利用了包括 SGLang、vLLM 和 llm-d 在内的开源生态系统。AMD 正全力押注开源推理栈，以挑战 NVIDIA 的 CUDA 护城河。SGLang 原生运行于 ROCm（AMD 的 CUDA 对应物）之上。

AMD 已在 AMD Instinct GPU 上集成 DeepSeek-V3，并通过 SGLang 进行性能优化。MI300X（192GB HBM3）特别适合处理像 DeepSeek-R1（671B 参数）这样的大规模 MoE 模型，而 SGLang 的大规模专家并行能很好地适配该硬件。

## 快速上手（在 AMD 开发者云或任何 ROCm 环境中）

```bash
# 拉取支持 ROCm 的 SGLang 镜像
docker pull lmsysorg/sglang:latest-rocm

# 在 MI300X 上运行 DeepSeek-R1
docker run --device=/dev/kfd --device=/dev/dri \
  --group-add video --shm-size 128g \
  lmsysorg/sglang:latest-rocm \
  python -m sglang.launch_server \
    --model deepseek-ai/DeepSeek-R1 \
    --tp 8 \
    --port 30000
```

```python
# 客户端——兼容 OpenAI 接口
import openai
client = openai.Client(base_url="http://localhost:30000/v1", api_key="none")

resp = client.chat.completions.create(
    model="deepseek-ai/DeepSeek-R1",
    messages=[{"role": "user", "content": "解释 KV 缓存复用"}]
)
```

## 对你工作的简要总结

如果你在 AMD 开发者云（MI300X）上运行推理，SGLang 是**推荐的服务后端**——在以下方面优于 vLLM：

- 长共享前缀工作负载（Agent、RAG）
- DeepSeek 级别的 MoE 模型（大规模专家并行）
- 结合推测解码的高吞吐批量工作负载

它是 xAI/Grok 的生产级栈，已开源。将其视为前沿实验室的非 NVIDIA 锁定推理引擎。

**参考资料：**

- [SGLang GitHub](https://github.com/sgl-project/sglang)
- [AMD ROCm 7 + SGLang 公告](https://www.amd.com/en/blogs/2025/enabling-the-future-of-ai-introducing-amd-rocm-7-and-the-amd-developer-cloud.html)
- [AMD Advancing AI 2025 — Lianmin Zheng SGLang 演讲](https://www.amd.com/en/corporate/events/advancing-ai/2025/advancing-ai-2025.html)
- [AMD 上采用 SGLang 的 DeepSeek-V3](https://amd.com/en/developer/resources/technical-articles/amd-instinct-gpus-power-deepseek-v3-revolutionizing-ai-development-with-sglang.html)
