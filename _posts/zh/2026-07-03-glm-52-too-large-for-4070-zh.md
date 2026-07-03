---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GLM-5.2对4070而言过大
translated: true
type: note
---

**问题：** 我有一块 RTX 4070（12 GB）。应该从 `unsloth/GLM-5.2-GGUF` 下载哪个量化版本？

**回答：**

实话实说：**都不行**。GLM-5.2 对你的 4070 机器来说遥不可及——而在你烧掉 200+ GB 带宽之前知道这一点，可能值得。

**背后的计算（基本原理）：**

GLM-5.2 是一个约 743B 总参数量 / 39B 激活参数的 MoE 模型。GGUF 内存占用 ≈ `总参数量 × 比特数 / 8`——MoE 路由机制不会节省你的磁盘或内存，只会节省算力（FLOPs），因为*所有*专家都必须常驻（任何 token 都可以路由到任意专家）。

```
Q4_K_M:  743B × 4.5 / 8 ≈ 418 GB
Q2_K:    743B × 2.6 / 8 ≈ 240 GB   ← 与报告数字吻合
TQ1_0:   743B × 1.7 / 8 ≈ 158 GB   （1 位动态量化，如果 unsloth 提供的话）
```

即使是激进量化的 2 位 GGUF，占用磁盘约 239 GB，运行时也需要同样大小的内存。你最好的机器（`192.168.1.36`：62 GB RAM + 12 GB VRAM = 74 GB 总量）连 Q2 的需求都差了大约 3 倍。另外请注意：目前该仓库树中只有 `README.md`——量化分片实际上还没有上传完成。

**你的硬件真正能跑什么：**

llama.cpp 中的 MoE 卸载技巧（`--n-cpu-moe`：注意力 + 共享专家在 GPU，路由专家在 RAM）使得约 100B 级别的 MoE 模型成为你工作站的甜点：

```bash
# GLM-4.5-Air：106B 总参数量 / 12B 激活参数——适合你机器的最大的 GLM
huggingface-cli download unsloth/GLM-4.5-Air-GGUF \
  --include "*UD-Q3_K_XL*" --local-dir ~/models   # 约 50 GB

./llama-server -m ~/models/GLM-4.5-Air-UD-Q3_K_XL.gguf \
  --n-gpu-layers 999 --n-cpu-moe 40 -c 32768 -fa
```

12B 激活参数下，内存带宽受限的解码速度预计约 8–15 tok/s——用于交互式编程是可用的。也关注较新的 Air 类版本（GLM-4.6/4.7-Air 级别，Qwen3-30B-A3B 级别）——任何 ≤110B 总参数量 / ≤13B 激活参数的模型，在 Q3–Q4 量化下都是你的上限。

**如果你真的想把 GLM-5.2 权重握在手里：**

你的 MI300X 云实例（192 GB HBM3）是你唯一接近的机器——1 位动态量化版本（约 158 GB）可以装在一张 MI300X 上，还有空间给 KV 缓存，并且 llama.cpp 支持 ROCm。这是一个真正有趣的实验：在单张 GPU 上以 2 美元/小时运行前沿的 743B MoE 模型。但请等待 unsloth 实际上传分片，并在确认前检查 `UD-TQ1_0` 文件夹的大小。对于日常使用 GLM-5.2，Z.ai API 是理性选择——它采用 MIT 许可证并提供按量计费的 API 访问，而你自己在低于约 4 位量化下运行会在它擅长的 agentic 编程任务上损失显著的品质。

**参考链接：**

- [unsloth/GLM-5.2-GGUF](https://huggingface.co/unsloth/GLM-5.2-GGUF)
- [vLLM recipe: zai-org/GLM-5.2](https://recipes.vllm.ai/zai-org/GLM-5.2)
- [GLM-5.2 本地硬件指南](https://www.compute-market.com/blog/glm-5-2-local-hardware-guide-2026)