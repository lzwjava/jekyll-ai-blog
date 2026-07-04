---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GTX 1060：一款十余年的老显卡
translated: true
type: note
---

**问题：** 什么是 GTX 1060 GPU？

**回答：**

NVIDIA GeForce GTX 1060 是一款2016年7月发布的中端消费级GPU，基于Pascal架构（GP106核心，台积电16nm工艺）。它曾是最受欢迎的游戏显卡之一——多年占据Steam硬件调查榜首。

关键规格（6GB版本）：

| 规格 | 数值 |
| ------ | ------ |
| 架构 | Pascal (GP106) |
| CUDA核心数 | 1280 |
| 显存 | 6 GB GDDR5（另有缩减版3GB版本，1152个核心） |
| 显存带宽 | 192 GB/s（192-bit位宽） |
| FP32算力 | ~4.4 TFLOPS |
| TDP功耗 | 120 W |
| 计算能力 | 6.1 |

从机器学习角度——这对你来说更关键：

- **无Tensor Core。** Tensor Core随Volta/Turing架构才出现。因此不支持硬件加速混合精度；Pascal消费级显卡上的FP16大致以FP32速度运行（GP106/GP104上的FP16吞吐量被刻意削弱）。
- **6 GB显存** 对于玩具级训练来说够用但紧张。你可以运行nanoGPT的莎士比亚字符级模型或小规模GPT-2（124M），配合小批量大小和梯度累积。你之前在MI300X上训练的GPT-2 760M——没有激进卸载的话完全不可能。
- **计算能力6.1** 意味着现代框架正在放弃支持：最新的PyTorch构建仍可运行，但FlashAttention需要sm_80+（Ampere），而Triton内核越来越多地假设Ampere及以上。在CUDA 12.x工具链中它已处于弃用路径上。
- 与你RTX 4070的粗略对比：4070拥有约7倍FP32吞吐量（29 TFLOPS），支持FP16/BF16/FP8的Tensor Core，12 GB显存，以及约504 GB/s带宽。对于训练工作负载，1060基本上落后了十年。

如果你遇到一块1060，快速检查方式：

```bash
nvidia-smi --query-gpu=name,memory.total,compute_cap --format=csv
python -c "import torch; print(torch.cuda.get_device_capability())"  # (6, 1)
```

总结：适合运行老游戏和推理小型量化模型（通过llama.cpp，一个3B模型Q4量化可塞进6 GB），但2026年不值得为机器学习购买——二手市场价格约60-80美元，甚至一块二手RTX 3060 12GB对于本地推理来说性价比高得多。
