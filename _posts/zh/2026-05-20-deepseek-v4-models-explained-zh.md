---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DeepSeek V4模型解析
translated: true
type: note
---

**问题：** 为什么 DeepSeek V4 Pro 和 V4 Flash 如此出色？为什么它们在 OpenRouter 上排名靠前？它们有多便宜？社区反馈如何？

---

**回答：**

DeepSeek 于 2026 年 4 月 24 日发布了 V4 Pro 和 V4 Flash。以下是完整解析——架构、基准测试、定价计算以及来自社区的坦诚反馈。

---

## 架构：为何又快又便宜

三个关键创新解释了其成本/性能优势：

### 1. 极高稀疏度的 MoE

V4 Pro 拥有 1.6T 总参数，但每个 token 仅激活 49B。V4 Flash 总参数 284B，每个 token 激活 13B。推理成本仅为密集模型所需的一小部分。

### 2. KV 缓存压缩

该模型结合了压缩稀疏注意力 (Compressed Sparse Attention) 和混合压缩注意力 (Hybrid Compression Attention)，将 KV 缓存内存减少到 V3.2 所需内存的仅 10%。这使得 1M token 的上下文窗口在生成环境中切实可行。

### 3. 用于稳定训练的流形约束超连接 (mHC)

标准残差连接只传递单个前向向量。超连接将其扩展为多个并行流——理论上提高了表达能力。无约束的超连接在 DeepSeek 的 27B 实验中导致了灾难性的训练发散，信号放大超过 3000 倍。mHC 框架通过使用 Sinkhorn-Knopp 算法将残差连接混合矩阵约束到 Birkhoff 多面体来解决这一问题——将信号放大降至 1.6 倍，从而实现了 1.6T 参数的稳定训练。

他们还使用 Muon 优化器进行预训练——选择它的原因是相比标准 AdamW 收敛更快、稳定性更高。值得注意的是，V4 是在华为昇腾 950PR 芯片上训练的，而非 NVIDIA 硬件——这是一个重要的地缘政治和供应链信号。

---

## 定价：实际计算

| 模型 | 输入 $/M | 输出 $/M |
|---|---|---|
| DeepSeek V4 Pro | $1.74 | $3.48 |
| DeepSeek V4 Flash | $0.14 | $0.28 |
| Claude Opus 4.6 | ~$15 | ~$25 |
| GPT-5.5 | $5 | $30 |

与 Claude Opus 4.6 相比，在编码基准测试中性能几乎相同的情况下，价格差距达 7 倍。V4-Flash 的每个输出 token 成本比 Claude Opus 4.6 低 89 倍。

规模化来看：每月 1 亿个输出 token，V4-Pro 花费 348 美元，而 Claude Opus 4.6 需 2500 美元。

V4 Flash 甚至在 OpenRouter 上提供了免费层级——输入 $0/M，输出 $0/M，拥有 1M token 上下文和 384K 最大输出。

---

## 基准测试现实检验

### V4 Pro 真正领先的领域（编码）

在 SWE-bench Verified 上，得分为 80.6%，与 V4-Pro 的 80.6% 相同——与 Claude 相差 0.2 个百分点。在 Terminal-Bench 2.0 上，V4-Pro 领先 Claude（67.9% vs 65.4%）。在 LiveCodeBench 上，得分 93.5%，而 Claude 为 88.8%。

### V4 Flash 的表现

V4-Flash 是一个真正严肃的模型，而非精简版替代品。在 SWE-bench Verified 上，得分 79.0%，V4-Pro 为 80.6%——差距仅 1.6 个百分点。在 LiveCodeBench 上，得分 91.6%，V4-Pro 为 93.5%。对于大多数开发者的编码任务，这些结果在功能上是等效的。

### 仍然落后的领域

HLE（人类最后的考试）得分 37.7%，V4-Pro 低于 Claude（40.0%）、GPT-5.4（39.8%），远低于 Gemini-3.1-Pro（44.4%）。SimpleQA-Verified 得分 57.9%，而 Gemini 为 75.6%，显示了事实知识检索方面的显著差距。

---

## 社区反馈

褒贬不一，但总体积极：

Reddit 反应："DS-V4 不错，但只是中等水平，并非最先进。" 在编码方面，它与前沿模型竞争甚至领先。在推理方面，它落后。

在 38 项基准测试中，DeepSeek V4 Pro 获得了唯一一个金融研究 10/10 满分——它在一个 NVDA 博弈论任务中生成了最强答案。其相对弱点是呈现格式而非分析质量——生成了结构良好的 markdown 研究报告，但 Claude 更易于生成仪表盘就绪的图表和指标卡片。

对于需要 30+ 次连续工具调用或持续复杂规划的任务，V4 Pro 表现出比 Claude Opus 4.7 更大的漂移。对于较短的智能体循环（例如标准智能体编码工作流程），性能差异小得多，通常无关紧要。

更广泛的趋势：阿里巴巴的 Qwen 3.6 Plus 在编码特定基准测试中处于类似水平。GLM 5.1 在 2026 年初也曾引起类似关注。开放权重模型与封闭模型之间的性能差距正在以两年前看似不可能的速度缩小。

---

## 实用路由策略（针对您的智能体/CLI 工作负载）

根据您的使用情况（约 15 亿 token/年，CLI 智能体，OpenRouter）：

```python
# 用于成本优化的智能体栈的模型路由启发式方法
def route_model(task):
    if task.type in ["code_generation", "code_review", "agentic_coding"]:
        if task.complexity == "high" or task.tool_calls > 30:
            return "deepseek/deepseek-v4-pro"   # 输出 $3.48/M，前沿编码能力
        else:
            return "deepseek/deepseek-v4-flash"  # 输出 $0.28/M，SWE-bench 分数相近
    elif task.type in ["factual_recall", "complex_reasoning", "writing"]:
        return "anthropic/claude-opus-4-6"       # 在 HLE、SimpleQA 上领先
    else:
        return "deepseek/deepseek-v4-flash:free" # 零成本，1M 上下文
```

该 API 同时兼容 OpenAI ChatCompletions 和 Anthropic API 格式，因此集成到您现有的 OpenRouter 设置中零摩擦。

**总结**：对于您的用例（编码密集、智能体密集、高 token 量），V4 Flash 目前可能最有吸引力——在 OpenRouter 上几乎免费的情况下达到 79% SWE-bench 分数，1M 上下文，生产级吞吐量。当您需要更深的推理深度并能承受约 $3.50/M 的输出成本时，Pro 是合理选择。

---

**参考文献：**

- [DeepSeek V4 Pro — OpenRouter](https://openrouter.ai/deepseek/deepseek-v4-pro)
- [DeepSeek V4 Flash — OpenRouter](https://openrouter.ai/deepseek/deepseek-v4-flash)
- [DeepSeek V4-Pro 评测：基准测试、定价与架构](https://www.buildfastwithai.com/blogs/deepseek-v4-pro-review-2026)
- [DeepSeek V4 vs Claude vs GPT-5.4：38 项基准测试](https://fundaai.substack.com/p/deepdeepseek-v4-vs-claude-vs-gpt)
- [DeepSeek V4 编码基准测试 — BSWEN](https://docs.bswen.com/blog/2026-04-26-deepseek-v4-vs-claude-opus-gpt-coding-benchmarks-2026/)
- [DeepSeek V4：开源前沿模型评测 — MindStudio](https://www.mindstudio.ai/blog/deepseek-v4-open-source-frontier-model-review)
- [DeepSeek V4 — DataCamp](https://www.datacamp.com/blog/deepseek-v4)
