---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'Inkling-Small: 模型、基准测试与设置'
translated: true
type: note
---

**问题：Thinking Machines Lab 的 Inkling-Small 模型是什么——架构、基准测试、如何运行？**

**回答：**

发布于 2026 年 7 月 30 日（昨天），Apache 2.0 许可，开放权重。这是 TML（Mira Murati 的实验室）旗舰模型 "Inkling" 的较小版本。

**架构** —— 稀疏 MoE 解码器，原生多模态（文本/图像/音频输入，文本输出）：

- 42 层仅解码器 Transformer，具有稀疏的专家混合前馈骨干网络：每个 token 被路由到 256 个专家中的 6 个，外加 2 个共享专家在每个 token 上激活
- 注意力机制是局部和全局层的混合
- 图像通过分层补丁编码器编码，音频通过离散 token 编码——所有模态投影到共享隐藏空间并由解码器共同处理
- 总计 276B 参数，12B 活跃参数——因此稀疏率约为 4.3%，与你的 GPT-2 760M 规模扩展实验属于相同的活跃参数级别，但采用了 MoE 而非密集架构
- 上下文窗口高达 1M 个 token，数值格式：BF16、MXFP8 和 NVFP4

**基准测试**（与相似活跃参数数量的开放权重同行及闭源模型对比）：

- SWE-Bench Verified：80.2% —— 击败 Qwen3.5-397B-A17B 的 76.4% 和 DeepSeek-V4-Flash 的 79.0%，输给 GPT-5.6-Luna 的 93.0%
- Terminal-Bench 2.1（最佳 harness）：64.7%
- GPQA Diamond：89.5%，与 GPT-5.6-Luna 持平
- ARC-AGI-2：40.1% —— 显著高于完整版 "Inkling" 模型的 36.5%，远高于 Claude 4.5 Haiku 的 4.0%
- SimpleQA Verified（事实性）较弱：20.6%，比大多数同行差——这是为代理/推理而非死记硬背知识优化的小型 MoE 的预期权衡

在代理编码和推理方面，其表现远超其活跃参数级别；事实性/知识回忆是薄弱环节，这对于较小的 MoE 来说很常见。

**自行运行** —— 这对于你的技术栈来说才是关键：

```
BF16 检查点：600GB+ 聚合显存
  - 4 块 B300，或 8 块 H200

NVFP4 检查点：180GB+ 聚合显存
  - 在 1 块 B300 上运行 W4A4（需要 SM100+）
  - 在 2 块 H200 上运行 W4A16
```

在 GPU 硬件上直接运行模型需要一个推理部署框架——可以是 SGLang、vLLM、TokenSpeed、Unsloth 或 Hugging Face。

HF 上的权重：`thinkingmachines/Inkling-Small` 和 `thinkingmachines/Inkling-Small-NVFP4`。可通过其 Tinker 平台 + `tml-renderers` pip 包 + GitHub 上的 tinker-cookbook 进行微调。

对于你的 MI300X 配置——NVFP4 在 180GB 范围内，但请注意 W4A4 快速路径仅限 Blackwell（SM100+）；在 MI300X 上，你需要通过 vLLM/SGLang ROCm 构建来运行 BF16，因此请预算完整的 600GB+ 显存层级，或者跨节点拆分运行。

参考资料：

- [Inkling-Small 模型卡](https://thinkingmachines.ai/model-card/inkling-small/)
- [Tinker Cookbook](https://github.com/thinking-machines-lab/tinker-cookbook)
