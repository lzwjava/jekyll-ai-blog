---
audio: false
generated: true
image: false
lang: zh
layout: post
title: M40 + 4070 训练限制
translated: true
type: note
---

**配备 2–3 张 NVIDIA M40 和 1 张 RTX 4070，你可以在训练模型的道路上走多远？**

---

这是一个微妙的配置——纸面上看 VRAM 很大，但存在严重的注意事项。以下是完整分析：

---

## ⚠️ 重大警告：M40 的 PyTorch 支持即将结束

截至 2026 年 9 月 4 日，PyTorch 宣布 **PyTorch 2.14 是最后一个提供任何 CUDA 12.6 wheels 的版本**。从 PyTorch 2.15 开始，Maxwell (SM 5.0)、Pascal (SM 6.0) 和 Volta (SM 7.0) 将**完全弃用**。

M40 是 Maxwell (SM 5.2) 架构。这意味着：**你必须将 PyTorch 锁定在 ≤ 2.14 + CUDA 12.6** 才能使用 M40。现代框架（Unsloth、较新的 HuggingFace TRL 版本等）可能会停止工作。

---

## GPU 规格对比

| | M40（×2 或 ×3） | RTX 4070 |
|---|---|---|
| 架构 | Maxwell (SM 5.2) | Ada Lovelace (SM 8.9) |
| 单卡 VRAM | 24 GB GDDR5 | 12 GB GDDR6X |
| FP32 | ~7 TFLOPS | ~29 TFLOPS |
| 张量核心 (FP16/BF16) | ❌ 无 | ✅ 有 (~116 TFLOPS) |
| 显存带宽 | 288 GB/s | 504 GB/s |
| PyTorch 支持 | ⚠️ 止步于 2.14 | ✅ 完全持续 |

M40 **没有张量核心**，因此所有训练都以 FP32 运行——比现代 GPU 使用 BF16 和张量加速的速度大约慢 4–8 倍。

---

## VRAM 计算

答案会根据你使用全量微调、LoRA 还是 QLoRA 而相差约 16 倍。

7B QLoRA 需要约 12GB VRAM；70B QLoRA 需要约 41–46GB VRAM；而 Qwen 3 30B-A3B MoE 尽管有 30B 参数，运行时仅需约 17.5GB QLoRA。

---

## 每种配置可以训练什么

### 仅使用 RTX 4070（12 GB，现代/快速）

| 任务 | 是否可行？ |
|---|---|
| 7B QLoRA（Llama、Mistral、Qwen） | ✅ 很轻松 |
| 13B QLoRA | ✅ 可以 |
| 7B LoRA | ❌ 太紧张（需要约 14–18 GB） |
| 任何全量微调 | ❌ 不行 |

**最佳用途**：快速、现代的 QLoRA 微调。使用张量核心、BF16 和当前 PyTorch。

---

### 2× M40（合计 48 GB，使用 PyTorch ≤ 2.14）

| 任务 | 是否可行？ |
|---|---|
| 7B 全量微调（梯度检查点） | ✅ 紧张但可行 |
| 13B QLoRA / LoRA | ✅ 可以（单张 M40 也可以） |
| 30B QLoRA | ✅ 可以 |
| 70B QLoRA | ✅ 可以（41–46 GB 足够） |
| 70B LoRA 或全量微调 | ❌ 不行 |

### 3× M40（合计 72 GB，使用 PyTorch ≤ 2.14）

| 任务 | 是否可行？ |
|---|---|
| 13B 全量微调（分布式） | ✅ 可以 |
| 70B QLoRA | ✅ 很轻松 |
| 70B LoRA | ✅ 可行（约 45–55 GB） |
| 70B 全量微调 | ❌ 需要 140+ GB |

---

## 能否将 M40 与 RTX 4070 组合在同一个训练任务中？

**实际上：不可以。不要尝试。**

- 不同架构（SM 5.2 vs SM 8.9）从技术上讲可以运行 DDP，但效率极低
- RTX 4070 会空闲等待 M40（约慢 4 倍）
- 两张卡都没有 NVLink，意味着所有 GPU 间通信都通过慢速 PCIe 进行

**将它们作为独立的工作节点运行**（不同的训练任务，或者在 RTX 4070 上训练的同时，在 M40 上做 CPU 卸载推理）。

---

## 实用建议

| 优先级 | 使用此 GPU | 用于此任务 |
|---|---|---|
| **首选** | RTX 4070 | 所有 7B–13B 模型的 QLoRA 微调，快速迭代 |
| **次选** | 2–3× M40 | 70B QLoRA 或 13B LoRA，锁定 PyTorch 2.14 |
| **避免** | M40 + 4070 混合 | 单个分布式训练任务 |

M40 三卡为你提供了大模型的**原始 VRAM 容量**，但对于任何需要速度、现代框架或张量核心加速的训练，**RTX 4070 才是真正的主力**。请预估 M40 很快将不再受支持，并据此规划你的工作流设计。

---

参考链接：
- [PyTorch Maxwell/Pascal support dropped — CUDA 12.6 wheels ending at PyTorch 2.14](https://dev-discuss.pytorch.org/t/notice-cuda-12-6-wheels-will-no-longer-be-published-from-pytorch-2-15-drops-maxwell-pascal-volta/3432.md)
- [GPU VRAM Requirements for LLM Fine-Tuning 2026](https://www.spheron.network/blog/gpu-vram-requirements-fine-tune-llm-2026/)
- [LLM Hardware Requirements Guide — VRLA Tech, June 2026](https://vrlatech.com/llm-hardware-requirements-guide/)
- [Best GPU for Fine-Tuning LLMs in 2026](https://packet.ai/blog/best-gpu-fine-tuning-llm)
- [PyTorch Issue #157517 — Maxwell/Pascal/Volta deprecation](https://github.com/pytorch/pytorch/issues/157517)