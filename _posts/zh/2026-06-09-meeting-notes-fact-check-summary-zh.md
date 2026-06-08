---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 会议记录事实核查摘要
translated: true
type: note
---

以下是会议记录的事实核查与修正：

---

会议记录_01.organized.md 的事实修正

1. "SGLAN" → 应为 "SGLang"
   - 文档中出现了7次。正确名称是 SGLang (<https://github.com/sgl-project/sglang)，由> LMSYS 开发。它是一个面向 LLM 的高性能服务框架。

2. "VLLM" → 应为 "vLLM"
   - 正确的写法是 vLLM（小写 v）。它是另一个主流开源 LLM 服务框架。

3. "QDA" → 很可能指的是 "CUDA Graph"
   - 整个关于 QDA 的段落描述的是 CUDA Graph 的功能（记录 CPU→GPU 内核启动，无需 CPU 参与即可重放）。目前没有名为 "QDA" 的知名框架做这件事。发言者可能是在讨论 CUDA Graphs。

4. "GrokQ" → 应为 "Groq"
   - 该公司名为 Groq (<https://groq.com)，以其> LPU（语言处理单元）定制推理芯片闻名。"GrokQ" 并非真实实体。（注意：Groq 与 xAI 的 Grok 模型无关。）

5. "cuBLAS LTE" → 应为 "cuBLAS LT" (Light)
   - 正确名称是 cuBLASLt（cuBLAS Light），是 cuBLAS 之上更灵活的 API。"LTE" 并不存在。

6. SGLang 的描述不准确
   - 笔记称 SGLang "提供分布式处理优化，通过预处理和隔离每个用户的内存来处理多个设备"。这含糊且错误。SGLang 的关键创新包括：
     - RadixAttention：使用基数树进行前缀缓存（不仅仅是“分布式处理”）
     - 用于结构化输出的压缩有限状态机（JSON 解码速度提升 3 倍）
     - 零开销 CPU 批处理调度器
     - Prefill-Decode 分离
     - 针对 MoE 模型（如 DeepSeek）的专家并行
   - 它主要不是关于“用户内存隔离”——这更像是 vLLM 的 PagedAttention 所关注的。

7. "Triton 是 CUDA 的简化版本"
   - 略有误导。Triton（由 OpenAI 开发）是一种用于编写 GPU 内核的 DSL（领域特定语言）。它比 CUDA 抽象层次更高——你编写基于 tile 的操作，而不是线程级代码。它可以通过 LLVM 后端同时支持 NVIDIA 和 AMD GPU。它不是“简化的 CUDA”，而是一种不同的编程模型。

8. "参数通常由 CPU 处理，而权重是 GPU 的事"
   - 这过于简化。在深度学习中，“权重”和“参数”基本上是同义词（权重是可学习的参数）。发言者可能想区分：推理时模型权重存放在 GPU 显存中，而 CPU 负责控制流、分词和编排。权重包括权重矩阵（W）和偏置（b），以及嵌入表、LayerNorm 参数等。

9. "HBM3 提供 192 GB 显存"
   - 仅适用于 AMD MI300X 这一种 GPU。HBM3 是一种内存标准——不同 GPU 容量不同。H100 有 80 GB HBM3，H200 有 141 GB HBM3e。192 GB 是 MI300X 的特定数值。

10. "Flash Attention 作者声称……DeepSeek V4 上每秒 500 个 token"
    - 截至 2026 年初，不存在“DeepSeek V4”。最新的是 DeepSeek-V3/V3.2。关于 Flash Tri Dao 优化能媲美定制芯片的说法方向正确（他确实提出过此类观点），但具体模型名称有误。

11. "GrokQ 的公司可能已被 NVIDIA 收购"
    - 截至知识截止时间，Groq 并未被 NVIDIA 收购。这似乎是猜测或混淆。

---

主要修正项：SGLAN→SGLang（7 次）、QDA→CUDA Graph、GrokQ→Groq、cuBLAS LTE→cuBLAS LT，以及 SGLang 技术描述需要重写。需要我应用这些修正来更新文件吗？
