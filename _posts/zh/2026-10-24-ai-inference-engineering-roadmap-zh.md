---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI推理工程路线图
translated: true
type: note
---

**问题：** AI基础设施、推理工程以及vLLM和SGLang等工具的学习路径/路线图是什么？

---

**答案：**

以下是一份结构化的路线图——从基础到生产级AI推理工程。

## 🧱 第一层 — 基础

**接触推理工具前的先决条件：**

- **Python + 软件工程** — Git、Docker、API、日志记录、测试
- **ML/DL 基础** — 训练与推理的区别、Transformer架构
- **LLM 内部原理** — 学习注意力机制、GQA（分组查询注意力）、KV cache，以及训练与推理的根本区别
- **硬件基础** — 了解CPU与GPU的区别、GPU内存和带宽如何影响推理，以及CUDA、PCIe、NVLink和NVSwitch等概念

## ⚙️ 第二层 — 推理基础

了解关键的推理指标：**延迟（Latency）**、**吞吐量（Throughput）**、**TTFT**（Time to First Token，首个Token生成时间）和**TPOT**（Time Per Output Token，每个输出Token生成时间）。同时学习量化和精度格式，如FP8和FP4。

关键服务概念：
- **连续/流式批处理** — 同时服务多个请求
- **分块预填充（Chunked Prefill）** — 将大提示分解成块
- **KV缓存管理** — 高吞吐服务中的核心瓶颈

## 🚀 第三层 — 推理引擎（该领域的核心）

2026年领先的LLM推理引擎包括**vLLM**、**TensorRT-LLM**、**Hugging Face TGI**和**SGLang**。这一层的设计会极大地影响延迟、吞吐量和基础设施成本。

### **vLLM — 生产标准**

vLLM 已成为服务大语言模型最广泛采用的推理引擎之一，常用于 AI 聊天平台和大规模推理 API。其核心创新是 **PagedAttention** —— 像操作系统管理虚拟内存一样管理 KV 缓存，从而显著减少 GPU 内存浪费。

### **SGLang — 自主/结构化生成引擎**

如果说 vLLM 侧重于高效地服务请求，那么 SGLang 则侧重于控制生成过程的具体展开方式。SGLang 的真正价值体现在复杂的生产系统中——现代 AI 应用已不再是简单的提示-响应 API。

SGLang 的核心创新是 **RadixAttention** —— 不像 vLLM 那样为每个请求缓存前缀，SGLang 存储了跨请求观察到的所有前缀的树状结构，并在会话间重用它们，这使得它在 agent 和多轮对话工作负载中效率更高。

### **性能基准 (H100, 2026)**

PremAI 的测量结果显示，SGLang 大约为 16,200 tok/s，而 vLLM 为 12,500 tok/s —— SGLang 的吞吐量优势约为 29%。在测试的每个并发级别下，SGLang 的 TTFT p95 也始终比 vLLM 低 5–8%。

### **何时使用哪个**

没有通用的赢家。vLLM 优化了大规模下的效率和吞吐量。SGLang 优化了结构化推理和基于 agent 的工作流程。

| 用例 | 推荐引擎 |
|---|---|
| 高吞吐API服务 | vLLM |
| Agent / 多轮 / 工具调用 | SGLang |
| 批量推理、长提示 | SGLang / LMDeploy |
| NVIDIA企业级 + 多框架 | Triton Inference Server |
| Hugging Face生态迁移 | vLLM（现为HF默认） |

> Hugging Face 于 2025 年底将 TGI 置于维护模式，并建议新部署使用 vLLM 或 SGLang。

## 🌐 第四层 — 分布式与生产基础设施

在掌握单引擎部署之后，可以深入学习：**分布式推理**（张量/流水线并行）、**Kubernetes上的推理**（GPU调度、NVIDIA GPU Operator）、用于流式推理的**Layer 7负载均衡**，以及**推理可观测性**（追踪、指标、仪表盘）。

高效推理正日益成为一门**基础设施工程学科**。最快的系统将高效的推理引擎与智能调度、批处理和基础设施编排相结合。

## 🗺️ 建议学习顺序

```
1. Python + Docker + Linux 基础
2. Transformer & LLM 内部原理（KV cache、注意力机制）
3. GPU 架构基础（CUDA、内存带宽）
4. 使用 vLLM 本地部署模型（兼容 OpenAI API）
5. 使用 SGLang 进行基准测试，比较 TTFT/吞吐量
6. 添加量化（AWQ、GPTQ、FP8）
7. 多 GPU 推理（张量并行）
8. Kubernetes + GPU Operator 部署
9. 可观测性（延迟追踪、GPU 利用率）
10. 构建生产级推理栈
```

---

**参考文献：**
- [Best LLM Inference Engines in 2026 — yottalabs.ai](https://www.yottalabs.ai/post/best-llm-inference-engines-in-2026-vllm-tensorrt-llm-tgi-and-sglang-compared)
- [vLLM vs SGLang Benchmarked on H100s — techsy.io](https://techsy.io/en/blog/vllm-vs-sglang)
- [LLM Inference Servers Compared: vLLM vs TGI vs SGLang vs Triton — premai.io](https://blog.premai.io/llm-inference-servers-compared-vllm-vs-tgi-vs-sglang-vs-triton-2026)
- [AI Inference Engineering Roadmap — LinkedIn / Ahmed Sayed](https://sa.linkedin.com/in/ahmed-sayed-a0090628)
- [Best vLLM Alternatives for Self-Hosted Inference — futureagi.com](https://futureagi.com/blog/best-vllm-self-hosted-inference-alternatives-2026/)