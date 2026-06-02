---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast:free
title: 使用LoRA进行高效微调
translated: true
type: note
---

低秩自适应（LoRA）是一种针对大型语言模型的参数高效微调技术。与更新预训练模型全部参数的传统方法不同，LoRA通过引入小型低秩矩阵来适配特定层（通常是注意力层或前馈层）。这些矩阵在保持原始模型参数冻结的同时捕获任务特定的更新，显著降低了内存和计算成本。例如，微调GPT这类大型模型通常需要更新数十亿参数，而LoRA仅需调整极小比例的参数（通常不足总参数量的1%）即可实现相当的性能。这使得LoRA成为资源受限环境的理想选择，无需大量重新训练即可针对特定任务高效定制大型模型。

[LoRA：大型语言模型的低秩自适应](https://arxiv.org/abs/2106.09685)
