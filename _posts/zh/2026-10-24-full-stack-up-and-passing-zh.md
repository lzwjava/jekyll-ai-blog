---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 全栈上线与通过
translated: true
type: note
---

一切都运行正常——**全栈启动并通过，位于192.168.1.34**。以下是总结：

## ✅ mini-llama.cpp 已克隆、构建并运行

**机器上的设置：**

| 步骤 | 状态 |
| --- | --- |
| `git clone git@github.com:lzwjava/mini-llama.cpp` → `~/projects/` | ✓ |
| `nvidia-cuda-toolkit` **12.4.131** 已安装（apt）— nvcc + libcublas ✓ | ✓ — 安装过程中遇到一次硬冻结/重启，通过 `dpkg --configure -a` + 重新安装修复 |
| 模型 `qwen2.5-0.5b-instruct-q4_k_m.gguf`（468 MB）→ `/mnt/models/`（通过本地 clash 代理从 HF 获取） | ✓ |
| `make` → 所有 3 个目标均已构建 | ✓ |

**运行：**

- `./mini-llama <model>` → `mini-llama.cpp skeleton -- build OK` ✓
- `./mini-llama-gpu <model>`（M1）→ **MILESTONE-1-OK**：GGUF 解析，F32 张量 → M40 精确（err=0），cuBLAS GEMM **32.2 GFLOPS**（rel err 2.4e-7） ✓
- `./mini-llama-m2 <model>`（M2）→ **MILESTONE-2-OK**：反量化普查匹配（Q5_0=133, Q8_0=13, Q4_K=12, Q6_K=12, F32=121），0.630B params → 2.52 GB fp32，实际 `ffn_up` GEMM 在 GPU 上（err 5.6e-6 PASS），VRAM：已使用 573 MB / 空闲 11307 MB ✓

**注意事项：**

- ⚠️ GPU 现在稳定了（M1+M2 运行干净，无冻结）——但要留意：在 CUDA 安装过程中它曾硬冻结过一次，同样是那块在重启前出现过 D-state 锁定的显卡。
- ℹ️ 此 M40 报告 **12 GB** VRAM（11520 MiB），而 README（为机器 .137 编写）假设为 24 GB —— 一切正常，只是让你在规划 M3+ VRAM 时知晓。
- 🚧 按照你的路线图，接下来是：**M3**（RMSNorm/RoPE/attention/KV-cache/SiLU forward pass），**M4**（sampling + CLI），**M5**（speed tuning）。一旦 forward pass 存在，`./mini-llama-m3 <model>` 将从此盒子输出实际 tokens。

要我启动 M3，还是就此打住？
