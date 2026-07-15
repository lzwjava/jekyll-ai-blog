---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Inkling 开放权重模型概述
translated: true
type: note
---

问题：Inkling是什么，Thinking Machines Lab的新发布？

答案：这是Thinking Machines Lab的首个开放权重模型，于2026年7月15日发布。关键规格如下：

**架构**

- MoE transformer，总参数量975B，激活参数41B，支持最多1M token上下文
- 每层256个路由专家 + 2个共享专家，每个token激活6个路由专家，sigmoid路由器，无辅助损失的负载均衡（DeepSeek-V3风格）
- 注意力机制：滑动窗口/全局层交错比例为5:1，8个KV头，使用学习到的相对位置偏置替代RoPE（声称在长上下文外推方面更优）+ QK/V和残差分支上的短卷积
- 在45万亿token的文本、图像、音频和视频数据上预训练
- 优化器：大矩阵使用Muon，其余使用Adam，结合其modular-manifolds权重衰减/学习率耦合工作
- 完全在NVIDIA GB300 NVL72系统上训练

**强化学习**

- 将强化学习扩展到超过3000万次rollout，奖励呈对数线性提升
- 可控的“思考努力” —— 通过在强化学习期间变化系统提示和每个token成本进行训练，从而像旋钮一样调节推理长度/成本
- 注意到训练过程中CoT压缩现象（语法缩减但仍可理解）—— 与Cognition在SWE-1.7上报道的现象相同

**变体**

- Inkling-Small（预览版）：总参数量276B，激活参数12B，在多个基准测试上达到或超越完整版Inkling —— 针对较小尺寸优化了预训练数据混合，完整权重尚未发布。

**相比前沿模型的表现**

- 表现不错但未达SOTA。在智能体编程（Terminal Bench 2.1）上大致与GLM 5.2/DeepSeek V4 Pro持平，远落后于Claude Fable 5/GPT 5.6 Sol。
- 在Terminal Bench 2.1上，Inkling仅用Nemotron 3 Ultra三分之一的token就达到了同等水平 —— 这才是其真正卖点：每token的效率，而非峰值分数。
- 多模态：无编码器，图像作为40×40 patch经过4层hMLP处理，音频作为dMel频谱图 —— 没有独立的视觉/音频编码器塔。
- 现在可在Tinker（其平台）上进行微调，权重在Hugging Face上（`thinkingmachines/inkling`），推理支持已在vLLM、SGLang、llama.cpp、transformers中落地。

鉴于您已经在运行自己的GPU集群训练GPT-2 760M —— 如果您想要一个原生支持音频/视觉的MoE基础模型，而不是自己拼接编码器，这款模型确实可以拉取权重并在本地微调。

参考资料：

- [Inkling：我们的开放权重模型](https://thinkingmachines.ai/news/introducing-inkling/)
- [模型卡](https://thinkingmachines.ai/model-card/inkling/)
- [Hugging Face权重](https://huggingface.co/thinkingmachines/inkling)
- [Tinker文档](https://tinker-docs.thinkingmachines.ai/tinker/)
