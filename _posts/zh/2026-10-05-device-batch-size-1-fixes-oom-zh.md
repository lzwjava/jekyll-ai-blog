---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 设备批量大小1解决OOM
translated: true
type: note
---

检查了 tmux `1` — 确认：在**第 0 步，`optimizer.step()`** 处发生 OOM（Muon 堆叠缓冲区，184 MiB），物理空闲仅 62 MiB。eval 标志没问题；问题在于原始稳态 VRAM：参数 + 梯度 + 优化器状态（约 7.5 GB）+ 激活峰值 + 你桌面的 2.05 GB > 11.56 GB。

**减少训练 VRAM 的关键手段：`--device-batch-size=1`**

这将激活峰值减半（CLI 可控的最大内存块，d18/seq1024 下约 680 MB → 约 340 MB），让优化器的堆叠缓冲区有喘息空间。其他一切保持不变 — `total-batch-size` 自动计算为相同的 1,048,576，因此：

- grad-accum 只是从 512 变为 1024 个 micro-steps（数学计算相同，LR scaling 相同，3,712 次迭代不变）
- 每步变慢约 10-15%，这是唯一的代价

```bash
tmux attach -t 1
cd /mnt/data/nanochat
NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache \
./.venv/bin/python -m scripts.base_train \
    --depth=18 --max-seq-len=1024 \
    --device-batch-size=1 \
    --tracker=none --run=d18-climbmix \
    --core-metric-max-per-task=50 \
    --save-every=250
```

注意：
- **别费心添加 `PYTORCH_CUDA_ALLOC_CONF`** — 我查过了：`base_train.py:15` 在导入 torch *之前* 已经设置了 `PYTORCH_ALLOC_CONF=expandable_segments:True`，而且它无论如何都优先于 CUDA 变体。提示此设置的错误消息只是 PyTorch 的通用模板 — 内存是物理耗尽，而不仅仅是碎片化（仅剩 62 MiB 可用）。
- 新估算：~8.3-8.6 GB 进程 + 2.05 GB 桌面 ≈ 在 11.56 GB 的显卡上留有 **0.7-1 GB 余量**。

如果*仍然* OOM，接下来的后备方案（按顺序）：
1. `--eval-tokens=2097156` — 缩小每次 val-eval 遍（默认是巨大的 41.9M tokens ≈ 每 250 步耗时 7 分钟；这也能加速运行）
2. `--eval-every=-1` — 完全跳过 val bpb，只保留 CORE 指标

要我现在把这条命令发到 tmux `1` 中吗？