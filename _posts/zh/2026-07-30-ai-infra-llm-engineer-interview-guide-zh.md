---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI基础设施大语言模型工程师面试指南
translated: true
type: note
---

问题：2026年AI基础设施/LLM工程师岗位的常见面试题有哪些？

回答：基于近期在Anthropic、Robinhood、Lightning AI的面试经历以及2026年整体趋势——面试门槛已从“解释Transformer”转变为“运营GPU集群并论证成本/延迟权衡”。以下按实际提问内容分组，并附上每个问题所需的思考模型。

**1. 分布式训练机制**

- 对比DP、DDP、FSDP、张量并行、流水线并行——每种方法在内存上何时出现瓶颈？
- 诊断70B参数训练任务中的CUDA OOM——你首先检查什么（激活检查点、批次大小、梯度累积、ZeRO阶段）？
- 实现一个简易版的梯度检查点：

```python
import torch

def checkpoint(fn, *args):
    class F(torch.autograd.Function):
        @staticmethod
        def forward(ctx, *inputs):
            ctx.fn = fn
            ctx.save_for_backward(*inputs)
            with torch.no_grad():
                return fn(*inputs)
        @staticmethod
        def backward(ctx, *grad_out):
            inputs = ctx.saved_tensors
            with torch.enable_grad():
                inputs = [i.detach().requires_grad_() for i in inputs]
                out = ctx.fn(*inputs)
            torch.autograd.backward(out, grad_out)
            return tuple(i.grad for i in inputs)
    return F.apply(*args)
```
他们希望你解释*为什么*这种做法用计算换内存（在反向传播中重新计算激活值，而不是存储）。

- 设计一个支持抢占和检查点的分布式任务队列，用于10万+ GPU训练任务（这个确切的问题今年反复出现）。
- 解释集群规模下的掉队者缓解和检查点/恢复机制——这是Anthropic基础设施工程师的实际日常工作（他们会明确询问如何诊断意外的分布式系统故障）。

**2. LLM基础——预期是前向传播演练，而非定义**

- 推导注意力复杂度O(n²d)，然后解释FlashAttention的IO感知分块（为什么它不是算法复杂度的胜利，而是内存带宽的胜利）。
- KV缓存：针对给定的模型大小/序列长度/批次计算内存占用，然后解释GQA/MQA作为解决方案。
- 解释RoPE与可学习位置嵌入，以及为什么RoPE在缩放技巧（NTK-aware、YaRN）下具有更好的外推能力。
- 混合精度（BF16/FP16）——数值不稳定实际出现在哪里（损失缩放、LayerNorm在fp32中）？

**3. 推理/服务——这是2026年大多数问题的集中点**

- TTFT与令牌间延迟——连续批处理（vLLM风格）和分页注意力如何独立地改变这两个指标？
- 设计跨区域低延迟服务，应对突发流量高峰——自动扩缩GPU池、推测解码、量化权衡（INT8/INT4、AWQ/GPTQ）。
- 成本计算：给定每GPU每秒令牌数和每GPU每小时成本，计算每百万令牌的成本——预期会现场进行算术。
- 针对趣直播/你的CLI代理工作：他们会考察“如何跨模型路由请求以实现成本与质量的平衡”——混合模型路由现在已成为一个标准的系统设计题。

**4. 系统设计（现在也面向普通软件工程师，而非仅限ML工程师）**

- 在受限网络下将一个大文件（模型权重）分发到数千台机器（类似BitTorrent的分片，近期有人被直接问到）。
- 设计端到端RAG服务：数据摄取 → 索引 → 检索 → 生成 → 评估 → 追踪 → 护栏。
- 设计多智能体工作流（调度、代码审查）——预期他们会考察当智能体悄然偏离计划时的故障处理。

**5. 行为问题（基础设施专用，非通用）**

- “Anthropic在6个月内将训练计算量翻倍——你优先做什么？”
- “描述一次你现场调试的分布式系统故障”——他们想要的是根因分析方法（指标 → 日志 → 假设 → 修复），而非故事叙述。

鉴于你已经在MI300X上训练过GPT-2 760M，并且每月跨模型运行约20亿个令牌——实际准备做法是：准备用自己运行中的真实数据（MFU百分比、每GPU每秒令牌数、每个令牌的成本）来证明架构选择，而非教科书式的答案。这才是面试官现在评估的真正的区分点。

参考文献：
- [System Design Interview Prep 2026 - Exponent](https://www.tryexponent.com/blog/system-design-interview-guide)
- [Anthropic Infrastructure Engineer Interview Questions 2026](https://www.gethireready.com/interview-guides/infrastructure-engineer-anthropic)
- [50+ AI Infrastructure Engineer Interview Questions](https://www.index.dev/interview-questions/ai-infrastructure-engineer)
- [Every AI Engineer Interview Question 2026 - Adil Shamim](https://adilshamim8.medium.com/every-ai-engineer-interview-question-you-need-to-know-in-2026-from-100-real-interviews-b5b7ae4b961a)
- [AI Infrastructure & MLOps Interview Questions 2026 - TechInterview](https://www.techinterview.net/questions/ai-infrastructure-and-mlops-interview-questions)