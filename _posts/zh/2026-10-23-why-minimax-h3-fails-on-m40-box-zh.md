---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 为什么 MiniMax-H3 在 M40 设备上运行失败
translated: true
type: note
---

官方文档已经说明了一切——MiniMax 建议用 **4 块 GPU** 来运行 H3（`--num-gpus 4`），而 Comfy 中唯一能接近 24GB 容量的量化格式（`int8_convrot`）明确是为 **torch with cu130**（CUDA-13/Blackwell 时代的技术栈）构建的。

## 结论：MiniMax-H3 无法在 `192.168.1.137` 上搭建——4 个独立的阻断性障碍

**1. 磁盘——立即失败。** `.137` 只有 **18 GB 可用空间**。最小可能的文件集（int8）：

| 文件 | 大小 |
| --- | --- |
| `qwen3vl_32b_minimax_h3_int8_convrot.safetensors`（32B 文本编码器） | 27.1 GB |
| `minimax_h3_fl2va_pruned_int8_convrot.safetensors`（扩散模型） | 21.0 GB |
| `minimax_h3_video_vae_int8` + audio_vae | 3.4 GB |
| **总计** | **≈ 51.5 GB**（+ComfyUI 运行时）——可用磁盘的 3 倍 |

**2. 显存——失败。** 24 GB 显卡，但 int8 编码器本身就有 **27 GB**。完整模型流水线（32B Qwen3-VL 编码器 + FL2VA MoE 扩散）从根本上需要 4 块 80GB 级 GPU。

**3. 系统内存——失败。** 总共 7.7 GB。Comfy 对 32B 编码器的标准 CPU offload 路径需要约 28 GB 以上的主机内存。

**4. GPU 架构——失败（核心原因）。** Tesla M40 = **Maxwell 2015，计算能力 5.2**，而 H3 的需求与 Maxwell 所具备的一切完全相反：

- 所有权重都以 **BF16/Fp8/Int8-with-Triton-ops** 形式提供 → M40 **完全没有 fp16/bf16 数据通路**
- H3 的推荐运行环境是 **torch cu130**（见上方 Comfy 文档）；CUDA ≥12 已彻底移除 Maxwell kernels；这台机器的驱动是 550 = CUDA 12.4
- **来自同型号机器 `.34` 的实证（上一次会话）**：torch `2.14.1+cu130` 和旧版 `1.13.1+cu117` 都会使驱动卡在 `nvidia_uvm`（D-state，不可杀，需要重启）。在这一代驱动上，M40 甚至无法初始化*任何* PyTorch CUDA 上下文。

我刻意**没有**把 50 GB 下载到只有 18 GB 可用空间的机器上，也没有再硬塞另一个驱动——它会在加载任何权重之前就撞上磁盘这堵墙死掉。

## 我建议的做法

1. **最干净的选择**——让一块现代 GPU 上线。现实可行的 H3 显卡：**A100/H100 80GB、2×RTX 4090、RTX 5090**（Comfy 自己的指南：H3 在 bf16 下需要 ≥48 GB 显存，int8_fp8 下约需 40 GB）。目前这个局域网里没有任何这类硬件。

2. **如果你想在 M40 24GB 上做*任何*图像生成**：唯一能触达这张卡的软件栈是 2021 年时代的（torch 1.13+cu117、SD1.5/SD2.1 fp32，512px 下约 10-15 it/s）——并且前提是驱动 **550** 能避免 580 曾有的 UVM hang（尚未测试；需要一个限定时间的探针测试，如果卡死可能需要重启）。它永远不能跑 H3。

3. **之前遗留的问题**：`.34` 在卡死的 GPU 驱动中仍有 3 个 D-state 进程——方便时需要**重启**。你说一声，我就清理我在那里创建的 venvs/缓存（`.34`：`~/dsenv`、`~/dslegacy`、uv 缓存 ≈ 40GB；还有 `~/dsvenv`）。

你希望我 (a) 仍然在 `.137` 上运行实证 torch 探针，以了结这个问题并为你的记录留档，(b) 在 `.137` 上尝试旧版 SD1.5 路线，还是 (c) 准备一台*能够*运行 MiniMax-H3 的机器的购买/构建规格？
