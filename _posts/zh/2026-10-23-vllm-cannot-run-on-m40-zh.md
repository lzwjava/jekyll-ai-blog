---
audio: false
generated: true
image: false
lang: zh
layout: post
title: vLLM 无法在 M40 上运行
translated: true
type: note
---

**不行——vLLM 无法在 `.137` 的 M40 上运行。** 官方 vLLM 文档设定的下限是：

> **GPU：compute capability 7.5 或更高（例如 T4、RTX 20xx、A100、L4、H100、B200）**

Tesla M40 的 **compute capability 是 5.2（Maxwell，2015 年）**——比 vLLM 的最低要求整整低两代（它甚至达不到他们为 Volta 时代显卡划出的“7.0”分界线；Maxwell/Pascal 根本不在他们的支持表中）。

它失败的原因和我们在实践中已经撞过的墙一样：

1. **GPU kernels** — vLLM 的 tensor-parallel/quant/attention kernels 是为 SM 7.5+ 编译的；5.2 上没有对应的 kernels。甚至没有任何代码路径可以执行。
2. **Software stack** — vLLM 运行在较新的 torch（cu12x/cu130）上。我们在同配置机器（`.34`）上已经证明，*任何* torch CUDA 初始化都会让这块 GPU 的驱动挂起（`nvidia_uvm` 进入 D-state 卡死 → 需要重启）。`.137` 的 driver 550 = CUDA 12.4（≥12 意味着 Maxwell kernels 已被移除）。
3. **fp16/bf16** — vLLM 的 pipeline 假设使用半精度；M40 **没有原生的 fp16/bf16**。

## 在 `.137` 上真正能跑 LLM 的方案（现实选项）

| 方案 | 方式 | 可行性 |
| --- | --- | --- |
| **llama.cpp / Ollama——仅 CPU** | GGUF 量化模型，完全不碰 GPU | ✅ **零风险，今天就能用**——但 7.7 GB 内存只能跑小模型（Qwen2.5-3B/4B、Llama-3.2-3B、Gemma-2-2B 的 Q4 量化约 2–3 GB），在 4 核 i5 上约 4–8 tok/s |
| **llama.cpp——在 M40 上用 CUDA** | 对旧架构的容忍度比 vLLM 高得多 | ⚠️ 未知——这不是上面那种零风险方式；driver 550 上的 legacy CUDA *也许*不会卡死（设备对 UVM 的触发方式不同），但如果卡了，预计要付出 **1 次重启** 的代价 |
| vLLM | — | ❌ 绝无可能 |

需要我现在就在 `.137` 上搭建 **llama.cpp + 一个小型 GGUF 模型，并带 OpenAI 兼容的 API 服务**吗（CPU 模式——对机器没有风险）？这样你今天就能在局域网里得到一个可用的推理端点。
