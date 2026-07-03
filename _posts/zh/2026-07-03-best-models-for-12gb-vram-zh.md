---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 12GB显存的最佳模型
translated: true
type: note
---

简短回答：**都不行。** 即使是最激进的量化版本（TQ1_0，约158 GB）也超出你显存13倍，超出你系统内存+显存总和2倍。

前面的回复说得对——你的RTX 4070 12 GB在任何量化精度下都无法运行743B参数的模型。**没有例外。**

**你的GPU能运行什么：**

在12 GB显存 + 系统内存卸载的场景下，MoE模型的最佳甜蜜点是**总参数量80–110B / 激活参数量10–15B**。目前你最好的选择：

| 模型 | 总参数量 | 激活参数量 | Q4_K_M大小 | 你的预估速度 |
| --- | --- | --- | --- | --- |
| GLM-4.5-Air (UD-Q3_K_XL) | 106B | 12B | ~50 GB | 8–15 tok/s（卸载） |
| Qwen3-30B-A3B | 30B | 3B | ~18 GB | 30–50 tok/s，基本全部放入显存 |
| DeepSeek-V3-Lite | ~68B | ~8B | ~35 GB | 15–25 tok/s（卸载） |

GLM-4.5-Air 配合 `--n-cpu-moe`（注意力层和共享专家放在GPU，路由专家放在系统内存）是真正能在你硬件上运行的GLM系列最近似模型。Qwen3-30B-A3B 更小但速度更快，因为大部分数据可以留在GPU上。

**那么你应该下载什么？**

```bash
# 选择其中一个：
huggingface-cli download unsloth/GLM-4.5-Air-GGUF --include "*UD-Q3_K_XL*" --local-dir ~/models
# 或者
huggingface-cli download unsloth/Qwen3-30B-A3B-GGUF --include "*Q4_K_M*" --local-dir ~/models
```

不要浪费带宽下载GLM-5.2——即使量化到1–2比特，它也需要数据中心级GPU（MI300X、H100）才能运行。
