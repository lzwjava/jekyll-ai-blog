---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 单GPU上的DeepSpeed
translated: true
type: note
---

问题：RTX 4070（单 GPU）能否使用 DeepSpeed？

答案：

可以。单张 RTX 4070 完全可以运行 DeepSpeed。事实上，DeepSpeed 的许多优化在 `world_size=1` 时也能生效。

然而，**并非所有 DeepSpeed 功能在单张 12 GB GPU 上都有用**。

| 功能                     | 单张 RTX 4070 | 值得使用吗？             |
| ------------------------ | ------------- | ------------------------ |
| Fused Adam               | ✅            | 是                       |
| CPU Adam                 | ✅            | 有时                     |
| 混合精度 (BF16/FP16)     | ✅            | 是                       |
| 梯度累积                 | ✅            | 是                       |
| 激活检查点               | ✅            | 是                       |
| ZeRO Stage 1             | ✅            | 收益较小                 |
| ZeRO Stage 2             | ✅            | 有时                     |
| ZeRO Stage 3             | ✅            | 模型勉强能放下时有用     |
| 流水线并行               | ❌            | 需要多 GPU               |
| 张量并行                 | ❌            | 需要多 GPU               |
| 通信重叠                 | 基本无用      | 否                       |

### DeepSpeed 在单 GPU 上真正提供什么

对于单 GPU，DeepSpeed 主要是一个**内存优化器**，而非速度优化器。

普通 PyTorch 存储

```
参数
梯度
优化器状态
```

对于 Adam：

```
权重        1 倍
梯度        1 倍
m           1 倍
v           1 倍

≈ 4 倍参数量内存
```

DeepSpeed 可以

* 将优化器状态卸载到 CPU
* 将参数卸载到 CPU/NVMe
* 对激活值做检查点
* 使用融合 CUDA 内核

这让你能够训练原本会内存溢出（OOM）的模型。

---

### 示例

不使用 DeepSpeed

```
python train.py
```

使用 DeepSpeed

```
deepspeed train.py \
    --deepspeed ds_config.json
```

配置示例：

```json
{
  "train_micro_batch_size_per_gpu": 1,

  "gradient_accumulation_steps": 16,

  "bf16": {
    "enabled": true
  },

  "zero_optimization": {
    "stage": 2
  }
}
```

---

### 对于 RTX 4070 12 GB

我粗略排序如下：

```
1. bf16
2. Flash Attention
3. 梯度检查点
4. 梯度累积
5. DeepSpeed ZeRO
6. CPU 卸载
7. QLoRA
```

如果你在训练完整模型，ZeRO 有帮助。

如果你在做 LoRA/QLoRA，DeepSpeed 通常收益不大，因为 PEFT 已经大幅降低了内存需求。

---

### 与 FSDP 对比

如今许多项目选择：

```
PyTorch FSDP
    +
torch.compile
    +
Flash Attention
```

而非 DeepSpeed。

当你需要以下功能时，DeepSpeed 仍然最强：

* ZeRO-3
* CPU/NVMe 卸载
* 超大型模型
* Microsoft 的训练栈

---

### 针对你的工作负载

根据你最近的实验（在 RTX 4070 上训练 GPT-2，以及在 12 GB VRAM 上运行 FLUX），我会建议：

* **GPT-2 / Transformer 预训练（<1B 参数）：** 纯 PyTorch + Flash Attention + 梯度检查点。DeepSpeed 可选。
* **7B–14B 全量微调：** DeepSpeed ZeRO-2/3 变得有价值。
* **LoRA / QLoRA：** 除非遇到内存限制，否则跳过 DeepSpeed。
* **FLUX / 扩散模型训练：** 优先使用 Hugging Face Accelerate（可选 DeepSpeed 后端），而非直接使用 DeepSpeed。

参考资料：

* [DeepSpeed GitHub 仓库](https://github.com/deepspeedai/deepspeed?utm_source=chatgpt.com)
* [DeepSpeed 文档](https://deepspeed.readthedocs.io/en/latest/?utm_source=chatgpt.com)