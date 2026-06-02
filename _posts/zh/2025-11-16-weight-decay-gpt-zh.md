---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: GPT模型训练中的权重衰减
translated: true
type: note
---

权重衰减（Weight decay）是训练GPT模型（以及几乎所有大语言模型）时常用的正则化技术，用于防止过拟合并提升泛化能力。

### 实际作用机制
权重衰减通过在损失函数中增加惩罚项，促使模型权重向较小数值收敛。数学表达上，若原始损失为ℒ（如交叉熵），加入权重衰减后的优化目标为：

ℒ_总损失 = ℒ + (λ / 2) × ||w||²

其中：
- w 代表模型参数（权重）
- ||w||² 表示权重的L2范数平方
- λ（lambda）是权重衰减系数（GPT风格训练中通常取0.01~0.1）

这个附加项会抑制模型学习过大的权重，除非它们能显著降低原始损失值。

### 实际实现方式（AdamW）
在大多数GPT训练场景中（OpenAI的GPT-2、GPT-3、LLaMA、Mistral等），人们并不使用标准L2正则化的原始Adam优化器，而是采用AdamW（解耦权重衰减的Adam）。

核心区别在于：
- 标准L2正则化会将惩罚项直接加入梯度计算
- AdamW采用解耦方式：将权重衰减作为独立的更新步骤执行，这种方式更适配Adam等自适应优化器

当在训练配置中看到如下代码时：
```python
optimizer = AdamW(model.parameters(), lr=5e-5, weight_decay=0.1)
```
其中的0.1即对应上文中的λ，且采用的是正确的解耦实现方式。

### 典型GPT风格模型的实际参数

| 模型 / 论文           | 权重衰减系数 | 备注                                      |
|----------------------|--------------|------------------------------------------|
| GPT-2 (OpenAI)       | 0.01         |                                          |
| GPT-3 (OpenAI)       | 0.1          | Brown et al. 2020                        |
| LLaMA 1 & 2 (Meta)   | 0.1          | 常与归一化层/偏置项不计衰减结合使用         |
| PaLM (Google)        | 0.1          |                                          |
| Grok-1 (xAI)         | 0.1          | 根据开源配置信息                          |
| Mistral / Mixtral    | 0.1          |                                          |

### 关键细节：哪些参数需要权重衰减？
现代实践（自LLaMA起）通常仅对特定层应用权重衰减：
- 应用范围：线性层（权重矩阵）、嵌入矩阵
- 排除范围：偏置项、LayerNorm权重、所有一维参数

通常通过PyTorch参数分组实现：
```python
decay = set()
no_decay = set()
for name, param in model.named_parameters():
    if "bias" in name or "layer_norm" in name or param.ndim == 1:
        no_decay.add(param)
    else:
        decay.add(param)

optimizer = AdamW([
    {"params": list(decay),   "weight_decay": 0.1},
    {"params": list(no_decay), "weight_decay": 0.0}
], lr=...)
```

### 对GPT级模型的重要意义
当参数规模达到数十亿甚至数百亿时，模型极易记忆训练数据。权重衰减作为最简单有效的工具之一（与Dropout、随机深度等技术协同），能有效控制模型实际容量并提升下游任务性能。

简而言之：权重衰减≈L2正则化，但通过AdamW优化器的正确实现和选择性应用，已成为所有现代GPT风格预训练方案的标准组成部分。
