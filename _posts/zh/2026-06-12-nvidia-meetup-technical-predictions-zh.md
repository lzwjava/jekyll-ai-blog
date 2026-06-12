---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA 技术预测聚会
translated: true
type: note
---

**问题：** 基于NVIDIA加速计算开发者见面会（深圳，2026年6月13日，与Google Cloud和腾讯联合主办）的议程，预测每个环节在实际技术层面将涵盖哪些内容。

**回答：**

以下是我逐环节的预测，基于截至2026年6月每个话题的公开信息。

## 1. NVIDIA × 腾讯：Hy3 Preview推理优化

背景：Hy3 Preview于2026年4月23日发布——一种快/慢思考混合MoE，总参数量295B，激活参数21B，最大上下文256K。他们将反复强调的要点：通过深度模型-框架协同设计实现整体推理效率提升40%，覆盖完整推理栈、内核性能和量化算法。

预计演讲会将那40%分解为：

- **在Hopper/Blackwell上的MoE专用服务**：专家并行（EP）布局、专家FFN的分组GEMM、全对全分发/合并优化，很可能涉及TensorRT-LLM和/或SGLang集成（Hy3官方支持vLLM和SGLang）
- **量化**：FP8权重/KV缓存，可能在Blackwell上使用NVFP4，以及他们如何在量化后保持快/慢思考路由器的精度
- **PD分离 + MTP（多token预测）推测解码**——2026年MoE服务的标准做法
- **生产数据**：在CodeBuddy/WorkBuddy上首token延迟降低54%，端到端延迟降低47%，驱动智能体工作流高达495步——他们将展示内核层面的胜利如何转化为智能体产品的胜利，以及可能的经济效益（¥1.2/百万输入token）

## 2. 利用Google Cloud进行AI编码 + Next 26回顾

两个环节，相同素材来源。Next '26（4月，拉斯维加斯）发布了260多项公告，聚焦“智能体时代”：Gemini Enterprise Agent Platform和第八代TPU。与编码相关的内容几乎肯定是：

- **Antigravity**作为AI编码明星：Google正在将其开发者工具统一到一个名为Antigravity（附带Antigravity CLI）的单一多智能体平台，Gemini Code Assist和Gemini CLI将于2026年6月18日停止对个人层级提供服务——注意这距本次见面会仅5天，因此预计会有强烈的“立即迁移”推动。Antigravity 2.0是一款独立的桌面应用，用于编排智能体，由Gemini 3.5 Flash驱动。
- 现场演示：规格说明 → 多智能体计划 → 并行编码智能体 → 审查，外加MCP集成（BYO-MCP让你将Gemini Enterprise连接至自定义工具）
- Next 26回顾将精选：Gemini 3.1 Pro的访问、Agent Platform作为端到端智能体工作空间，以及值得注意的Claude Opus 4.7被添加为开放模型选择，还有第八代TPU（双芯片设计用于训练与推理）和Virgo Network——新的超大规模数据中心结构

## 3. SM120推理优化与工作流中的AI智能体

SM120 = 计算能力12.0 = 消费级/工作站Blackwell（RTX 5090、RTX PRO 6000/4000）。这是对你RTX 4070 → Blackwell演进路径最相关的环节。痛点已有充分记录，并将很可能构成演讲的结构：

- 原生的NVFP4 CUTLASS路径在SM120上一直存在问题——TMA warp专用的分组GEMM内核在运行时失败，迫使回退到Marlin W4A16，后者将FP4反量化为FP16；社区对FlashInfer的SM120能力检查的补丁首次在桌面Blackwell上实现了正确的原生FP4 MoE输出。预计NVIDIA将展示官方的CUTLASS/FlashInfer修复和调优后的tile配置。
- FlashInfer是SGLang在SM120上的主要内核库，包含JIT编译的SM120内核和专用的MLA变体——很可能会有注意力后端选择的讲解
- “工作流中的AI智能体”角度：使用编码智能体自行完成优化循环——用nsys/ncu进行profile，让智能体提出内核tile配置，基准测试，迭代。这与2026年智能体驱动内核自动调优的趋势相符。真实数据如仅通过配置修复，RTX PRO 4000上的吞吐量提升6.5倍（36 → 234 tok/s），说明了其重要性。

## 4. SGLang上下文并行（CP）设计与实现

很可能是最深入的技术演讲。CP将序列维度分片到多个GPU上（与TP分片隐藏/头维度不同），解决两个问题：O(N²)的预填充注意力和KV缓存超过单GPU HBM。预计涵盖：

- **预填充CP与zigzag环形注意力**：长上下文预填充（256K+）通过KV缓存耗尽HBM，并且O(N²)注意力瓶颈造成TTFT；zigzag CP为每个rank分配头部+尾部块，使因果注意力负载均衡，在PD分离部署中每个rank仅传输1/CP的KV到解码节点，并行进行，无需聚合步骤

zigzag技巧的核心逻辑（约10行）——为何头部+尾部块能平衡因果注意力：

```python
# 朴素切分：rank 0获得token [0:N/4]，rank 3获得[3N/4:N]
# → rank 3需注意约4倍于rank 0的key（因果掩码）。负载不均衡。
# Zigzag：rank i获得块i AND块(2*CP - 1 - i)
def zigzag_shard(tokens, cp_size):
    chunks = split(tokens, 2 * cp_size)
    return [concat(chunks[i], chunks[2*cp_size - 1 - i]) for i in range(cp_size)]
# rank 0：块(0, 7)，rank 3：块(3, 4) → 每个rank看到
# ~平等的因果注意力FLOPs。在rank间环形传递KV块。
```

- **解码CP**：在解码时跨设备对上下文进行分区，以避免KV缓存冗余（仅用TP时，每个rank持有完整的KV副本），受Helix Parallelism论文启发，采用环形注意力或reduce-scatter/all-gather通信，并在调度器中设置context_parallel_size拓扑
- **可组合性**：CP如何与TP/PP/EP堆叠——DeepSeek V3.2已在SGLang中运行CP8+PP2+TP8配置，他们将CP与最近的PP工作进行对比（分块流水线并行配合异步P2P在DeepSeek-V3.1上实现PP4 TP8相比仅TP8达到了3.31倍预填充吞吐量，TTFT降低67.9%）——预计会提供“何时使用CP vs PP vs 两者结合”的决策框架，以及针对DeepSeek风格模型的DSA/稀疏注意力交互

## 元预测

贯穿所有四个环节的联系主线是：**智能体推理经济学**。智能体工作流（495步Hy3运行、Antigravity多智能体编排）产生长上下文和巨大的KV压力——这正是CP、SM120内核工作和MoE协同设计所解决的问题。如果你参加，SGLang CP演讲是最值得做笔记的；它直接是你的DeepSeek v4 MoE探索的上游，而zigzag/环形注意力设计也清晰地映射到你在nanoGPT规模的训练CP中要实现的内容上。

**参考文献：**

- [腾讯混元Hy3 preview发布 — Tencent](https://www.tencent.com/zh-cn/articles/2202320.html)
- [实测混元Hy3 preview — 钛媒体](https://www.tmtpost.com/7964254.html)
- [Pipeline Parallelism in SGLang — LMSYS Blog](https://www.lmsys.org/blog/2026-01-15-chunked-pipeline/)
- [Prefill CP with Zigzag Ring Attention — sglang#22223](https://github.com/sgl-project/sglang/issues/22223)
- [Decode Context Parallel proposal — sglang#12196](https://github.com/sgl-project/sglang/issues/12196)
- [NVFP4 MoE on SM120 debug report — cutlass#3096](https://github.com/NVIDIA/cutlass/issues/3096)
- [Google Cloud Next 26 wrap-up](https://cloud.google.com/blog/topics/google-cloud-next/google-cloud-next-2026-wrap-up)
- [Gemini for Google Cloud release notes (Antigravity migration)](https://docs.cloud.google.com/gemini/docs/release-notes)
