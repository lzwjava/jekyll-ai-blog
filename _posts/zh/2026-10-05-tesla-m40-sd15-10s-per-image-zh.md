---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 特斯拉M40 SD1.5 每张图像10秒
translated: true
type: note
---

在 M40 上确认了端到端生成——真实、连贯的 SD1.5 输出。

## 基准测试结果 —— Tesla M40

工作流程：**512×512，20 步，Euler，CFG 7，SD 1.5（fp16）**，通过 ComfyUI API 运行。

| 运行次数 | 墙钟时间 |
|---|---|
| 第 1 次运行（含初始模型加载） | 57.8 秒 |
| 预热运行 2 | 10.2 秒 |
| 预热运行 3 | 10.5 秒 |
| 预热运行 4 | 10.6 秒 |
| **稳态平均** | **~10.4 秒/图**（~0.52 秒/步） |

（首次尝试中的“0.5 秒”是 ComfyUI 提示缓存命中——相同的提示被重复使用。改变种子后得到了上述真实数值。）

**生成期间的 GPU 状态：** 已用 3,996 MiB / 11,520 MiB VRAM，51 °C，~72 W —— 显卡几乎未满负荷。有大量 VRAM 余量（可容纳 SDXL，并能进行批处理）。

## 这意味着什么
- **SD 1.5 在此硬件上非常可用** —— 每张 512×512 图像约 10 秒。交互性足够。
- **SDXL** 的负载大约是其 4–6 倍（更大的 UNet + 双文本编码器），因此 1024×1024 下预计 **~40–90 秒/图**。VRAM 充足；速度是瓶颈。
- **FP16 运行无误** —— SD1.5 无需 `--fp32`。

## 你当前的工作配置
- 服务器**当前运行于**：http://127.0.0.1:8189（后台进程由 `run.sh` 启动）。
- 检查点：`models/checkpoints/v1-5-pruned-emaonly-fp16.safetensors`
- 输出存放于 `~/projects/ComfyUI/output/`（宇航员图像为 `bench_00005_.png`）。
- 随时用 `cd ~/projects/ComfyUI && ./run.sh` 启动。

需要我再拿一个 SDXL 检查点并计时一次 1024×1024 运行，或者安装 ComfyUI-Manager 以使用自定义节点吗？