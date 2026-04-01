---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPT-2 训练的非常规 H100 策略
translated: true
type: note
---

这里有一些 **不受欢迎** 的（但技术上合理的）在云端 H100 上训练 GPT-2 124M 的想法：

---

### 1. **使用 1 个 H100 来训练 124M 模型**
大多数人会为这个小型模型使用单个 A100 甚至 V100。使用 H100 是过度杀鸡用牛刀——但这正是重点。  
**不受欢迎的转折**：不要并行化。在 **一个 H100** 上运行，使用巨大的 batch size，利用 H100 的 FP8 支持通过 gradient accumulation 模拟更大的有效 batch size。这保持简单，避免通信开销，并且不浪费 GPU 潜力。

---

### 2. **使用 FP8 训练，不使用 FP32 的 master weights**
H100 原生支持 FP8。大多数人会保留 FP32 的 master weights 以确保稳定性。不受欢迎的想法：**完全使用 FP8** 进行前向和反向传播，使用 H100 的 transformer engine 自动处理缩放。这有风险，但能加速训练并减少内存——对于如此小的模型，你甚至可以增加超出合理范围的 batch size。

---

### 3. **使用 8 个 H100，但禁用所有并行机制**
不要使用 data parallelism、tensor parallelism 或 pipeline parallelism，只需在同一实例上启动 **8 个独立的训练运行**，每个使用不同的 random seed。并行进行 hyperparameter sweep。  
为什么不受欢迎？人们期望分布式训练加速单个模型，但这里你能在相同时间内获得 8 个训练变体。

---

### 4. **故意欠拟合以加速迭代**
训练的 token 数量远少于 Chinchilla-optimal。使用 H100，你可以在几小时内达到 compute-optimal。相反，训练 **1/10 的 token** 以迭代架构变更、数据混合或评估协议。大多数人优化最终模型质量；不受欢迎的是优化 **每美元的洞见**。

---

### 5. **使用基于 CPU 的 dataloader，不进行 GPU prefetch**
在 H100 上，即使是 124M 模型，IO 也可能成为瓶颈。不受欢迎的修复：避免复杂的 GPU dataloader。使用单线程 CPU dataloader，并设置 `pin_memory=False`，让 GPU 略微空闲。这能及早暴露瓶颈，并迫使你思考数据管道——不受欢迎是因为每个人都追求 100% GPU utilization。

---

### 6. **在 H100 上运行，但限制功率上限**
将 H100 设置为更低的功率限制（例如 300W 而非 700W），以节省成本并减少冷却需求。性能会下降，但对于如此小的模型，你仍然严重过度配置。大多数人追求最大速度；不受欢迎的是在过度硬件上优化 **成本效率**。

---

### 7. **不使用分布式优化器（如 ZeRO）**
即使使用 8 个 H100，也跳过 ZeRO stages。只使用 DDP 并完全复制模型。这个模型很小；你会浪费内存，但获得简单性和避免通信开销。不受欢迎是因为每个人拿到 H100 都假设需要 sharding。

---

### 8. **使用极低精度和激进的 gradient clipping 进行训练**
使用 FP8 并设置极小的 gradient clipping 阈值（例如 0.1）来稳定训练。结合无 warmup，这很不寻常，但能以牺牲最终 perplexity 为代价获得快速收敛曲线——非常适合原型开发。

---

### 9. **使用小型辅助模型实时生成 synthetic data**
不要使用静态数据集，而是使用另一个小型模型（例如 GPT-2 124M 本身）在同一 H100 上并行运行生成 synthetic text，并在其上训练。这在理论上低效，但允许无限数据变异——不受欢迎是因为被视为浪费。

---

### 10. **保留一个 H100 仅用于 logging 和 evaluation**
取一个 8×H100 节点，使用 7 个进行训练，保留 1 个空闲用于连续 evaluation、logging 和 checkpointing。这按照传统分布式训练标准是“浪费”的，但能提供实时洞见而不减慢训练步骤。

---

如果你想，我可以为这些方法之一勾勒一个 **slurm script** 或 **PyTorch DDP config**。