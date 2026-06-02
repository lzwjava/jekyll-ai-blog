---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 本地 Qwen 3.5 27B oMLX 性能
translated: true
type: note
---

问题：从 Claude 4.6 Opus 蒸馏的 Qwen 3.5 27B 模型的本地性能如何，特别是使用 oMLX 运行时？

回答：
**Qwen 3.5 27B Claude 4.6 Opus Reasoning Distill**（社区常称为“Qwopus”）因其尺寸与智能的出色平衡而备受关注。当与 **oMLX**（一个针对 Apple Silicon 优化的开源 MLX inference server）搭配使用时，它能创建一个高效能的本地开发环境。

以下是基于最近社区测试对其性能和能力的分解：

### 1. 编码和代理能力

* **AI Assistants Integration：** 该模型因驱动如 Cursor 和 OpenCode 等 AI 编码助手而备受赞誉。用户报告称，它开箱即用地处理 plan mode、agent mode 和 ask mode，只需最小配置。
* **Tool Calling：** 它在正确 tool calling 方面非常熟练，适用于编写多个 Python 脚本、调试、测试和执行代码等任务。
* **Comparisons：** 本地社区普遍认为，这个 27B dense 模型在纯编码任务上优于更大的 Qwen 3.5 35B MoE（Mixture of Experts）。许多用户将其能力与前沿模型如 Gemini 3 Flash 相比，并表示它在引导式重构和 sub-agent 工作流方面几乎与 Claude Sonnet 一样出色。

### 2. 硬件和 VRAM 效率

* **Resource Requirements：** 27B 模型的 4-bit 量化版本需要大约 17GB 到 22GB 的 VRAM。这使其成为拥有 24GB–32GB 独立 GPU（如 RTX 3090/4090）或具有统一内存的 Apple Silicon Mac 的用户的完美选择。
* **Speed：** 在如 RTX 4090 运行 `llama.cpp` 的高端消费级硬件上，用户看到预填充约 2,400 tokens/秒，生成约 40 tokens/秒。M 系列 Mac 上的速度也非常可观，得益于 MLX framework 优化。

### 3. Apple Silicon 上 oMLX 的优势

如果您在 Mac 上使用 oMLX 运行此模型，其性能会因特定架构特性而大幅提升：

* **Paged SSD Caching：** oMLX 在热内存层和冷 SSD 层之间持久化 KV cache。这意味着如果您在对话中途更改上下文或返回之前的编码会话，过去的上下文会立即从 SSD 恢复，而不是重新计算。这对于长时间编码会话来说是巨大的时间节省。
* **Continuous Batching：** 它原生支持 continuous batching 和与 OpenAI-compatible 客户端的无缝集成，使其在本地 API 使用中极其稳定，不会让模型“过度思考”或无限循环。

总体而言，Qwen 3.5 27B 的 Claude 4.6 Opus 蒸馏版本目前被认为是日常本地“vibe coding”最实用和最有能力的 open-weights 模型之一，前提是您为其提供适当的规划和清晰的上下文。

参考文献：

* [Distilled qwen 3.5 27b is surprisingly good at driving Cursor. : r/LocalLLaMA - Reddit](https://www.reddit.com/r/LocalLLaMA/comments/1s2ql21/distilled_qwen_35_27b_is_surprisingly_good_at/)
* [Running Qwen3.5-27B locally as the primary model in OpenCode : r/LocalLLaMA - Reddit](https://www.reddit.com/r/LocalLLaMA/comments/1s7p0u9/running_qwen3527b_locally_as_the_primary_model_in/)
* [GitHub - jundot/omlx: LLM inference server with continuous batching & SSD caching for Apple Silicon — managed from the macOS menu bar](https://github.com/jundot/omlx)
* [oMLX - open-source MLX inference server with paged SSD caching for Apple Silicon : r/LocalLLaMA - Reddit](https://www.reddit.com/r/LocalLLaMA/comments/1r3qwyi/omlx_opensource_mlx_inference_server_with_paged/)
