---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 磁盘已完全设置并验证
translated: true
type: note
---

完成 — 磁盘已完全设置并验证。✅

## 摘要 — `192.168.1.137` TOSHIBA DT01ACA050（500 GB）

| 步骤 | 状态 |
|---|---|
| 检测 | 重启后 `sda` 现在可被枚举（之前：Q170 AHCI 上热插拔不可见） |
| 旧数据 | 原本是空的 NTFS（3 个分区，仅 94 MB 元数据）——已安全擦除 |
| 分区 | GPT，单一分区 `/dev/sda1` |
| 格式化 | ext4，卷标 `MODELS` |
| 挂载 | `/mnt/models` — **总计 458 GB，可用 435 GB** |
| 持久化 | `/etc/fstab` UUID 条目，带 `nofail`（即使磁盘缺失也能安全启动） |
| 属主 | `lzw:lzw` |
| 性能 | **写入 167 MB/s / 读取 168 MB/s**（健康的 7200 rpm 硬盘；SATA 链路 6 Gbps） |
| 目录布局 | `/mnt/models/{comfy, models/{diffusion_models,text_encoders,vae,loras,embeddings}, hf-cache}` — 已为 ComfyUI + H3 做好准备 |

## 这对 MiniMax-H3 意味着什么

✅ **存储瓶颈 — 已解决。** 最小的 H3 组合（int8: 27.1 GB encoder + 21 GB diffusion + 3.4 GB VAEs ≈ 51.5 GB）现在能装下，还剩约 380 GB 空间——即使完整的 `text_encoder` + `fl2va` int8 + ComfyUI 也绰绰有余。

⚠️ **但另外三道墙没有改变** —— 在下载约 52 GB 之前要保持清醒：
1. **VRAM**: 仅 int8 Qwen3-VL encoder 就需要 27 GB > M40 上的 24 GB（H3 官方流程要求 4×80 GB GPU）
2. **RAM**: 7.7 GB —— 没有空间对 32B encoder 做 CPU offload
3. **算力**: H3 的运行时是 torch cu130（Comfy 正好为此提供 `int8_convrot`）；CUDA ≥12 没有任何 Maxwell kernel——而且我们已经用实验证明，当 torch 接触 M40 时，这个驱动家族会挂起（不只是失败）。你很可能会以同样的方式让 `.137` 的驱动卡死，然后需要再次重启。

所以我的建议不变：**保留这块 435 GB 磁盘备用**（它也很适合 SD1.5/旧版实验，或未来换 GPU），但先不要下载 H3 权重，除非你准备好让这张卡上的驱动必然挂起。

**接下来的选项：**
- **(a)** 我在 `.137` 上实证验证 ComfyUI + torch cu130 的实际挂起风险（简短、限时，但之后预计需要重启）——由你决定
- **(b)** 仍然开始拉取 H3 文件，作为暂存演练（下载可行；推理不行）
- **(c)** 把这台机器标记为存储就绪，继续前进 —— 仍待处理：`.34` 的 NVIDIA 驱动卡住，需要在你方便时自行重启