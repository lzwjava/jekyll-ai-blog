---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FLUX Models for RTX 4070
translated: true
type: note
---

问题：RTX 4070（12 GB 显存）实际能够运行哪些 FLUX 模型？

答案：

对于 RTX 4070（12 GB 显存），限制因素是**显存**，而非算力。FLUX 模型是 transformer 重型的，文本/图像 transformer 占据了主要内存使用。

以下是实用总结：

| 模型            | RTX 4070 12GB           | 备注                                              |
| -------------- | ----------------------- | ------------------------------------------------- |
| FLUX.1 Schnell | ✅ 良好                  | 最佳选择。速度快，专为消费级 GPU 设计。            |
| FLUX.1 Dev     | ⚠️ 可以，需卸载          | 由于 CPU 卸载而变慢；需要低显存模式。              |
| FLUX.1 Pro     | ❌ 不行                  | 封闭 API 模型。无法本地运行。                      |
| FLUX.2 Dev     | ❌ 不行                  | 单独 transformer 远大于 12GB。                     |
| FLUX.2 Pro     | ❌ 不行                  | 仅限云/API。                                       |

你实际上已经在 FLUX.2 上遇到了这个问题：

> Transformer ≈ **60 GB BF16**

这意味着即使 **48 GB** 的 GPU 也无法在未进行激进分片/卸载的情况下容纳该模型。12 GB 的 RTX 4070 远远不够。

### 运行良好的情况

对于图像生成：

```text
RTX 4070
    ↓
FLUX.1 Schnell
    ↓
1024×1024
20–30 步
≈10–20 秒/图
```

这是最佳平衡点。

---

对于 FLUX.1 Dev：

```python
pipe.enable_model_cpu_offload()
```

或

```python
pipe.enable_sequential_cpu_offload()
```

它可以运行，但由于权重在 CPU 内存和 GPU 显存之间持续移动，生成速度会变得非常慢。

---

## 量化版本

社区项目已经产出了 GGUF 和其他量化版本的 FLUX.1 模型，可通过以下工具运行：

* llama.cpp
* ComfyUI
* Forge WebUI

示例包括：

* Q4
* Q5
* FP8

这些模型大幅减少了显存使用。12 GB 的 4070 通常能够以可接受的速度和图像质量运行量化后的 FLUX.1 Dev，使其比原始 BF16 checkpoint 实用得多。

---

## 如果你的目标是理解 FLUX

由于你感兴趣的是研究前沿模型而不仅仅是生成图像，我建议按照以下顺序学习：

1. **FLUX.1 Schnell** —— 理解推理流程。
2. **FLUX.1 Dev** —— 检查架构和 transformer 块。
3. 研究代码库中的 DiT 实现和 MMDiT 组件。
4. 阅读 FLUX.2 论文/博客以了解架构变化，而不是尝试本地运行 FLUX.2。

本地运行 FLUX.2 真正开始有意义的硬件包括：

* RTX 5090（32 GB）
* H100（80 GB）
* MI300X（192 GB）
* 多 GPU 设置

单张 RTX 4070 根本不是 FLUX.2 的目标硬件。

参考：

* [Black Forest Labs](https://blackforestlabs.ai?utm_source=chatgpt.com)
* [FLUX GitHub（官方推理示例）](https://github.com/black-forest-labs/flux?utm_source=chatgpt.com)
