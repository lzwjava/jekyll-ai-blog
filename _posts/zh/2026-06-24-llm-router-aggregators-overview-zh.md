---
audio: false
generated: true
image: false
lang: zh
layout: post
title: LLM路由器聚合器概述
translated: true
type: note
---

**问题：** 除了 OpenRouter，还有哪些主要的 LLM API 路由器/聚合器？

**回答：**

以下是一些值得关注的主要服务：

## 第一梯队 — 全功能聚合器（多供应商路由）

| 服务 | 模型数量 | 主要特点 |
|---|---|---|
| [OpenRouter](https://openrouter.ai) | 300+ | 覆盖最广，支持回退路由，使用分析 |
| [Together AI](https://together.ai) | 100+ | 擅长开源模型，推理速度快，支持微调 |
| [Fireworks AI](https://fireworks.ai) | 50+ | 推理速度快，支持函数调用和 JSON 模式 |
| [Replicate](https://replicate.com) | 数千个 | 通过 Docker 运行任意模型，也适合图像/音频 |
| [Groq](https://groq.com) | ~20 | 速度极快（LPU 芯片），支持 Llama/Mixtral |
| [Cerebras](https://cerebras.ai) | ~5 | 推理速度最快（约 2000 token/秒），支持 Llama 3.3 |

## 第二梯队 — 专注于特定方向的路由器

| 服务 | 专长 |
|---|---|
| [Hugging Face Inference API](https://huggingface.co/inference-api) | 任意 Hugging Face 模型，无服务器部署 |
| [Novita AI](https://novita.ai) | 价格低廉的开源模型 |
| [DeepInfra](https://deepinfra.com) | 开源模型定价有竞争力 |
| [Perplexity API](https://docs.perplexity.ai) | 搜索增强模型 |
| [Mistral API](https://mistral.ai) | 官方 Mistral 模型，适合欧洲用户 |

## 第三梯队 — 企业级/自托管路由器

| 服务 | 适用场景 |
|---|---|
| [LiteLLM](https://github.com/BerriAI/litellm) | 自托管代理，支持 100+ 供应商，兼容 OpenAI |
| [PortKey](https://portkey.ai) | 可观测性 + 路由 + 安全护栏 |
| [Helicone](https://helicone.ai) | 代理功能，含日志记录、速率限制、缓存 |
| [Martian](https://withmartian.com) | 基于成本/质量的智能模型路由 |

## 针对你的具体场景

考虑到你重度使用 OpenRouter 并构建 CLI 代理：

**LiteLLM** 是最值得自托管的选择——一个兼容 OpenAI 的单一端点，可路由到任意供应商：

```python
pip install litellm

# litellm --model openrouter/deepseek/deepseek-chat
# 或在代码中：
from litellm import completion
response = completion(
    model="openrouter/deepseek/deepseek-r1",
    messages=[{"role": "user", "content": "hi"}],
    api_key="<API_KEY>"
)
```

如果你希望获得跨 20 亿 token/月消耗量的可观测性，**PortKey** 是不错的选择——它能在多个供应商之间进行日志记录、链路追踪和缓存。

## DeepSeek V3 定价对比（你的主要模型）

| 路由器 | 输入价格（美元/百万 token） | 备注 |
|---|---|---|
| OpenRouter | ~$0.27 | 享受缓存折扣 |
| Together AI | ~$0.30 | |
| Fireworks | ~$0.27 | |
| DeepInfra | ~$0.28 | |
| 官方 API | ~$0.27 | 直接访问 api.deepseek.com |

针对你的使用场景（高流量、CLI 代理、重度依赖 DeepSeek），我建议：

- **主要选择**：OpenRouter（覆盖广 + 回退机制）
- **快速推理**：Cerebras 或 Groq，用于对延迟敏感的任务
- **自托管代理**：LiteLLM，将所有服务统一到单一端点后面
