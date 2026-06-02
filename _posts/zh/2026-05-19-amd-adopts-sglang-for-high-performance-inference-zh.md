---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD采用SGLang进行高性能推理
translated: true
type: note
---

问题：什么是SGLang，为什么它会出现在 AMD 开发者云上？

答案：

## 什么是 SGLang？

**SGLang**（**Structured Generation Language** 的缩写）是一个用于大语言模型（LLM）和多模态模型的开源高性能服务框架。它由加州大学伯克利分校开发，由 LMSYS 组织托管，结合了 Python 嵌入式前端语言与高度优化的后端运行时。

---

## 核心架构

SGLang 建立在两大基础支柱之上：

**1. 后端 — RadixAttention**

与传统推理方法相比（传统方法在 KV 缓存分配上浪费 60–80% 的 GPU 内存），SGLang 引入了 **RadixAttention**——一种基于基数树的前缀缓存系统，能够自动发现并复用请求间的共享前缀，从而显著提升内存效率和吞吐量。

**2. 前端 — 结构化编程语言（DSL）**

灵活的前端语言提供了直观且强大的 LLM 编程接口，支持可链式调用的生成调用、高级提示工程、复杂控制流、多模态输入、并行执行以及与外部系统的交互。

---

## 主要特性

SGLang 的快速运行时提供了高效的服务能力，包括基于 RadixAttention 的前缀缓存、零开销的 CPU 调度器、预填充-解码分离、推测解码、连续批处理、分页注意力、张量/流水线/专家/数据并行、结构化输出、分块预填充、量化（FP4/FP8/INT4/AWQ/GPTQ）以及多 LoRA 批处理。

它还拥有广泛的硬件支持，可运行在 NVIDIA GPU（GB200/B300/H100/A100）、AMD GPU（MI355/MI300）、Intel Xeon CPU、Google TPU、昇腾 NPU 等设备上。

---

## 模型支持

SGLang 支持主流生成式模型，如 Llama、Gemma、Mistral、Qwen、DeepSeek 和 LLaVA，同时也支持嵌入模型和奖励模型，并提供了简单机制来扩展支持新模型。

---

## 行业规模与应用

SGLang 已大规模部署，每天在生产环境中生成数万亿 tokens。它受到众多领先企业和机构的信赖，包括 xAI、AMD、NVIDIA、Intel、LinkedIn、Cursor、Oracle Cloud、Google Cloud、Microsoft Azure、AWS、斯坦福大学、加州大学伯克利分校以及清华大学。目前，SGLang 在全球超过 40 万张 GPU 上运行。

---

## 为什么它会出现在 AMD 开发者云上？

AMD 已将 SGLang 深度集成为其平台上的**一级推理框架**：

- AMD 开发者云提供包含 SGLang 的**快速启动包**——预构建的 Docker 容器，容器内启动 Jupyter，用户可直接访问 SGLang AI/ML 软件栈，并附带示例 notebook 助你快速上手。

- AMD 的 ROCm 7 与开源生态（包括 SGLang、vLLM 和 llm-d）合作，引入了分布式推理。AMD 拥抱开放策略，共同开发共享接口和原语，以在 AMD 平台上实现高效的分布式推理。

- AMD 提供了基于 MI300X GPU 优化的 SGLang Docker 容器，开发者可在 AMD 开发者云 droplet 上以极简设置运行 Qwen 3.5 等模型。

- AMD 开发者云为开发者提供对 AMD Instinct GPU 的原始访问权限，用于运行推理、训练、微调或任何自定义工作负载，使用他们已熟悉的框架——包括 vLLM、SGLang、PyTorch 等。

---

## 性能对比

在 H100 GPU 上，SGLang 相比 vLLM 吞吐量提升 29%（16,215 vs 12,553 tokens/秒），延迟更低（首 token 延迟 79ms vs 103ms）。部署 DeepSeek R1 或 V3 的组织在使用 SGLang 时，相比通用推理引擎可获得 2–3 倍的吞吐量提升。

---

## 总结表格

| 方面 | 详情 |
|---|---|
| **全称** | Structured Generation Language |
| **来源** | 加州大学伯克利分校 / LMSYS |
| **主要用途** | LLM 和多模态模型推理服务 |
| **关键创新** | RadixAttention（前缀缓存） |
| **硬件支持** | NVIDIA、AMD、Intel、TPU 等 |
| **AMD 集成** | AMD 开发者云上的预构建 Docker 快速启动 |
| **许可证** | 开源 |

参考资料：

- [SGLang GitHub 仓库](https://github.com/sgl-project/sglang)
- [SGLang 官方文档](https://sgl-project.github.io/)
- [SGLang on AMD Instinct GPUs — ROCm Blogs](https://rocm.blogs.amd.com/artificial-intelligence/sglang/README.html)
- [How to Get Started on the AMD Developer Cloud](https://www.amd.com/en/developer/resources/technical-articles/2025/how-to-get-started-on-the-amd-developer-cloud-.html)
- [AMD ROCm AI Developer Hub](https://www.amd.com/en/developer/resources/rocm-hub/dev-ai.html)
- [SGLang Complete Guide — Inference.net](https://inference.net/content/sglang-complete-guide/)
