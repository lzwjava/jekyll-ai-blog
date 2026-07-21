---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FLUX.1-dev或Schnell
translated: true
type: note
---

问题：在 Radeon Cloud 48GB VRAM 上 FLUX.2-dev 出现 OOM 后，我应该选择哪种恢复方案？

回答：

选择 **方案 2：尝试更小的模型，如 FLUX.1-dev**。

理由：

* 你的 GPU 是 **48GB VRAM**（很可能是 AMD MI300 级分区 / Radeon Cloud）。
* `FLUX.2-dev` 是一个非常庞大的扩散 Transformer：

  * 仅 BF16 权重 ≈ 60GB+
  * 完整检查点 ≈ 166GB 磁盘占用
  * 运行时内存需求更高，因为你需要：

    * 模型权重
    * 激活值
    * 注意力 KV/状态
    * VAE
    * 文本编码器

即使使用 CPU 卸载也会很痛苦，因为 AMD ROCm + 扩散卸载的成熟度不如 CUDA。

你的目标很可能是 AMD 黑客马拉松多模态赛道。一个能运行的演示胜过与最大模型作斗争。

推荐路径：

```
2. FLUX.1-dev
```

然后进行优化：

### 方案 A（最佳平衡）

使用：

```
FLUX.1-dev + fp16/bf16
```

预期：

* 磁盘：~23GB
* VRAM：~24-32GB（取决于管线）
* 可轻松容纳在 48GB 中

### 方案 B（演示速度最佳）

使用：

```
FLUX.1-schnell
```

优点：

* 1-4 步生成
* 速度快得多
* 更适合实时演示

缺点：

* 质量低于 dev 版本

对于黑客马拉松评审，我会选择：

```
FLUX.1-schnell
        +
Qwen3-8B / Qwen-VL 图像描述
        +
Gradio/FastAPI 演示
```

一个完整的创意工作流比一个会崩溃的巨型模型得分更高。

避免：

* ❌ 方案 4 仅 CPU 卸载

  * 技术上可能加载，但生成延迟可能达到几分钟/张图。
* ❌ 方案 3 bitsandbytes 4-bit

  * bitsandbytes 主要属于 CUDA 生态；ROCm 支持并非顺畅之路。
* ❌ 方案 1 FP8

  * 有趣，但 FLUX 在 AMD 上的 FP8 支持并非我敢押注黑客马拉松演示的路径。

重启后，我会干净地切换：

```bash
pip install diffusers transformers accelerate sentencepiece
```

然后测试：

```python
from diffusers import FluxPipeline
import torch

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell",
    torch_dtype=torch.bfloat16
)

pipe.to("cuda")

image = pipe(
    "一台运行在 AMD Radeon GPU 上的未来主义 AI 机器人",
    num_inference_steps=4
).images[0]

image.save("test.png")
```

对于你的 AMD GPU 演示，一个稳定的 FLUX.1-schnell 管线加上智能体工作流，很可能比 FLUX.2-dev 提交更出色。
