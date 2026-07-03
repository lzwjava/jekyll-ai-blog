---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070 Gemma 4 指南
translated: true
type: note
---

**问题：** `unsloth/gemma-4-26B-A4B-it-qat-GGUF` 是否适合我的 RTX 4070（12 GB）机器？我应该下载哪个文件？

**回答：**

是的——这个模型实际上非常适合你的工作站。与 GLM-5.2 相比，体验有天壤之别。

**该仓库只有一个量化版本，这是有意为之。** 目录树中包含一个单独的模型文件 `gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf`（14.2 GB），以及 mmproj 视觉编码器文件。`qat` 后缀表示量化感知训练：Google 在训练过程中内嵌了 4 位量化机制对权重进行微调，因此这里的 Q4 能够恢复接近 BF16 的质量——这与 Gemma 3 QAT 发布的策略相同。无需在其他仓库中寻找 Q5/Q6；QAT 检查点的 Q4 是预期精度，通常优于非 QAT 模型的后处理 Q6。

**内存计算：**

```
权重：        14.2 GB  （26B 总参数 × ~4.4 位/8）
每 token 激活：~4B 参数 → 每次前向传播约 2.2 GB 涉及
你的显存：     12 GB
你的内存：     62 GB
```

14.2 GB 无法完全放入 12 GB 显存，但 26B-A4B 是一个 MoE（混合专家模型）——因此你可以使用相同的专家卸载技巧：注意力层、嵌入层和共享层放在 GPU 上；路由专家放在系统内存中。由于每个 token 仅激活约 4B 参数，CPU 端每步传输的数据量很少。预计解码速度约为 25–45 tok/s——这类模型（如 Qwen3-30B-A3B）在你的硬件上会感觉**非常快**。

**下载与运行：**

```bash
# 仅文本
huggingface-cli download unsloth/gemma-4-26B-A4B-it-qat-GGUF \
  --include "gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf" --local-dir ~/models

# 可选：视觉（这是一个图像文本到文本模型）
huggingface-cli download unsloth/gemma-4-26B-A4B-it-qat-GGUF \
  --include "mmproj-F16.gguf" --local-dir ~/models

./llama-server \
  -m ~/models/gemma-4-26B-A4B-it-qat-UD-Q4_K_XL.gguf \
  --mmproj ~/models/mmproj-F16.gguf \
  --n-gpu-layers 999 \
  --n-cpu-moe 12 \
  -c 16384 -fa on
```

调整 `--n-cpu-moe`：从 12 开始，逐渐减小直到出现 OOM（显存不足），然后回退 2。每将一个专家层移回 GPU 都能免费提升速度。使用 `nvidia-smi` 监控——目标显存占用约 11.3 GB，为 KV 缓存留出余量。如果需要更长的上下文，添加 `--cache-type-k q8_0 --cache-type-v q8_0` 可将 KV 内存占用减半。

**工具使用注意事项：** Gemma 4 刚刚发布，因此请确保你使用的是最新的 llama.cpp 主分支（`git pull && cmake --build build -j`）——新架构通常需要更新的图支持，而 MoE 卸载标志（`--n-cpu-moe`）仅在架构正确连接时才有效。如果 `llama-server` 报错 `unknown architecture: gemma4`，那就表示你需要重新编译。

也请下载 mmproj-F16（1.19 GB）——在如此速度下，本地视觉模型对于 CLI 工具中的截图驱动代理循环来说非常实用。

**参考：**

- [unsloth/gemma-4-26B-A4B-it-qat-GGUF](https://huggingface.co/unsloth/gemma-4-26B-A4B-it-qat-GGUF/tree/main)