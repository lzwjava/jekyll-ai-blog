---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 因桌面应用导致内存不足
translated: true
type: note
---

已检查 tmux `1` — 再次失败，但**这次出在另一个位置**：不是 eval 阶段，而是第一个优化器步骤。

**发生了什么**

```
Step 00000 | Validation bpb: 3.171073     ← 启动 + step-0 评估正常
...
optimizer.step() → muon_step_fused (已编译内核)
buf20 = empty_strided_cuda((18, 4608, 1152), ...)   # 184 MiB Muon 缓冲区
torch.OutOfMemoryError: ... 61.81 MiB 空闲
```

`--core-metric-max-per-task=50` 这个改动没问题 — CORE 评估甚至还没开始。任务在 **step 0, optimizer.step()** 时崩溃，需要一个 184 MiB 的连续缓冲区，但只有 **62 MiB 空闲**。

**根本原因：桌面应用正在吃掉你的显存**

| 进程 | 显存 |
| --- | --- |
| Xorg | 1,184 MiB |
| gnome-shell | 218 MiB |
| **Chromium** | 153 MiB |
| **GitHub Desktop** | 86 MiB |
| **VS Code** | 160 MiB |
| Warp 终端 | 204 MiB |
| **非训练总计** | **~2.05 GiB** |

当你的原始训练还在运行时，这些应用只用了 **~1.05 GiB**。训练过程本身需要约 9 GiB（701M 参数：bf16 权重 + 梯度 + AdamW/Muon 状态 ≈ 8.1 GiB，再加上评估/优化器临时空间）。9 + 2.05 显然放不进 11.56 — 超支了约 400-500 MiB。

**修复：关闭三个可关闭的应用，然后重新启动**

```bash
# 1. 释放显存（~400 MiB）
pkill -f 'snap/chromium'        # Chromium
pkill -f github-desktop         # GitHub Desktop
pkill -f 'snap/code'            # VS Code  （如果还需要它打开则跳过）

# 2. 重新启动（和之前相同的参数）
tmux attach -t 1
cd /mnt/data/nanochat
NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache \
PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
./.venv/bin/python -m scripts.base_train \
    --depth=18 --max-seq-len=1024 --device-batch-size=2 \
    --tracker=none --run=d18-climbmix \
    --core-metric-max-per-task=50 \
    --save-every=250
```

（`PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` 是为了防止错误显示的 648 MiB 碎片化预留内存，脚本里已经设置了 `PYTORCH_ALLOC_CONF`，这是 torch 2.9 的主要变量，但加上这个也没有额外成本。）

我现在就可以做所有这些事 — 杀掉那 3 个应用并在 tmux `1` 中重新启动。只需确认一下：**可以关闭 Chromium、GitHub Desktop 和 VS Code 吗？**（Xorg/gnome-shell/Warp 不能关闭 — 它们是你的会话。）
