---
audio: false
generated: true
image: false
lang: zh
layout: post
title: M40 运行 ComfyUI 但有注意事项
translated: true
type: note
---

简短回答：**可以运行——但有限制。** 还有一个修正：这不是一台笔记本。`chassis_type=3` 和 `MSI MS-7977` 表示这是一台**台式机**（Haswell/Skylake 时代的 MSI 主板）。实际情况如下：

## 你的硬件

| 组件 | 规格 | ComfyUI 评估 |
| --- | --- | --- |
| GPU | NVIDIA **Tesla M40, 11.5 GB 显存** | ✅ 显存充足，可运行 SD1.5/SDXL |
| GPU 架构 | **Maxwell, compute 5.2 (sm_52)** | ⚠️ **主要瓶颈** |
| CPU | i5-6600, 4 核 / 4 线程 | 🟡 可驱动队列，但 VAE/解码较慢 |
| 内存 | **7.2 GB**（≈4 GB 可用，3.7 GB 交换） | ⚠️ 紧张 |
| 磁盘 | 829 GB 可用 | ✅ 没问题 |
| 系统/驱动 | Ubuntu 26.04, 驱动 580, CUDA 13.0 | 🟡 驱动仍支持 Maxwell（580 是最后一个支持的驱动分支） |

## 关键问题：Maxwell (sm_52)

近期 **PyTorch CUDA 版本已移除 Maxwell/Pascal/Volta 内核**，CUDA 13 工具包也不再支持 sm_52。你的驱动（580）是 NVIDIA 为 Maxwell 支持的*最后一个*驱动分支，因此仍能驱动显卡——但如今直接执行 `pip install torch` 安装的版本很可能**不包含 `sm_52` 内核**，导致 `torch.cuda.is_available()` 或首次内核启动失败。

**解决方法：** 固定使用较旧的软件栈：

- **PyTorch ≤ 2.6.x，搭配 CUDA 12.4（`cu124`）**——仍包含 Maxwell 内核
- **Python 3.11 或 3.12**（你已通过 uv 使用 3.12；系统自带的 Python 3.14 对这些版本来说太新）

## 其他 M40 注意事项

- **Maxwell 不支持 FP16 加速** → 请以 fp32 模式运行 ComfyUI。采样速度会比现代显卡慢。
- **无显示输出**（服务器/计算卡）——没问题，你用 Intel HD 530 驱动桌面，M40 用于计算。
- 250 W 涡轮风扇散热卡；请确保它有足够气流。

## 实际预期

- **SD 1.5：流畅运行。** SDXL：可用，中等步数下每张图约 10–30 秒。
- **Flux / 视频 / 大模型：吃力**——M40 速度慢且无 fp16，尽管显存名义上够用。
- **7 GB 内存是另一个瓶颈**——模型加载和浏览器操作会导致交换。16 GB 会好很多。

## 安装方案（使用 uv，符合你的项目结构）

```bash
git clone https://github.com/comfyanonymous/ComfyUI ~/ComfyUI && cd ~/ComfyUI
uv venv --python 3.12
uv pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 \
  --index-url https://download.pytorch.org/whl/cu124
uv pip install -r requirements.txt
# 验证 sm_52 是否正常工作：
uv run python -c "import torch; print(torch.__version__, torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

然后如果遇到半精度错误，请使用 `--fp32`（或 `--force-fp32`）启动。

总结：**可以运行，12 GB 显存确实有用——但必须固定使用旧的 PyTorch 版本，而且速度不会很快。** 需要我帮你设置并确认 GPU 在 torch 下实际可用吗？
