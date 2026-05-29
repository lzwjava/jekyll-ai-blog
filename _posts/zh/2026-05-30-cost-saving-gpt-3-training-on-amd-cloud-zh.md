---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD云上节省成本的GPT-3训练
translated: true
type: note
---

问题: 在计划训练 GPT-3 模型时，如何降低 AMD Developer Cloud 的成本？

答案：

在 AMD Developer Cloud 上训练 GPT-3 规模的模型会因 GPU 使用和存储成本而迅速变得昂贵。以下是一种结构化的成本降低方法：

### 1. **管理 GPU Droplets**
- **删除或停止闲置的 droplets：** 从你的快照列表来看，有些 droplets 只运行了 1 小时，但仍可能产生持续的存储成本。停止或删除未使用的 droplets。
- **优先使用较小的实例：** 在实验阶段，使用较小的 GPU 配置或更少的 GPU 来验证代码和模型，然后再进行扩展。
- **共享单个 droplet：** 在可行的情况下，将工作负载合并到单个 GPU droplet 上，而不是启动多个 droplets。

### 2. **优化快照**
- **删除旧快照：** 你有成本为每个 $2-$3 的快照。只保留最新或最关键的快照。
- **压缩或本地导出：** 如果需要备份，考虑将快照下载到本地机器或 S3 存储，然后从云端删除它们。

### 3. **使用 Spot/Preemptible 实例（如果支持）**
- 检查 AMD Developer Cloud 是否提供更低费率的 **spot 实例**。这些实例更便宜，但可能意外终止。如果你实施了检查点保存，那么对于大规模训练来说非常理想。

### 4. **降低训练成本**
- **梯度累积：** 在不增加 GPU 内存使用的情况下模拟更大的批次大小。
- **混合精度训练：** 使用 FP16 以减少内存并加速训练，从而减少 GPU 使用时间。
- **智能检查点保存：** 减少检查点保存的频率，以避免不必要的存储成本。

### 5. **先在本地或用小模型进行实验**
- 在投入完整的 GPT-3 训练之前，先验证你的模型：
  - 使用较小的 GPT-3 变体（例如 125M 或 350M 参数）
  - 在本地使用 AMD ROCm 进行基于 CPU 或低 GPU 的训练

### 6. **监控使用情况**
- 定期检查 **计费仪表板** 以跟踪 droplet 和快照成本。
- 如有可能，设置警报或限制以避免意外费用。

### 7. **考虑混合方法**
- 在本地或在更便宜的云端替代方案（如 AWS、GCP，甚至使用更少 GPU 的 AMD Dev Cloud）上预训练或微调较小的模型。
- 仅在最终的大规模训练时使用完整的 GPU droplet。

> ⚠️ 完整的 GPT-3 训练（175B 参数）即使在 MI300X 等高端 GPU 上也极其昂贵。通常，研究人员会 **微调现有的预训练 GPT-3 模型**，而不是从头开始训练，以节省成本。

参考文献：
- [AMD Developer Cloud 文档](https://developer.amd.com/amd-developer-cloud/)
- [大型语言模型高效训练技巧](https://arxiv.org/abs/2203.15556)
- [OpenAI GPT-3 微调指南](https://platform.openai.com/docs/guides/fine-tuning)

如果你愿意，我可以专门针对 AMD Dev Cloud 创建一个 **GPT-3 微调的成本最小化策略**，明确指出要使用哪些 droplets、快照和训练技巧。