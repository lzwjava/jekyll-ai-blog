---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在Tmux中成功恢复训练
translated: true
type: note
---

已检查 — 任务在 tmux `1` 中于 02:05 **成功重启**。✅

**正在运行的进程：**
```
./.venv/bin/python -m scripts.base_train --depth=18 --max-seq-len=1024 
    --device-batch-size=2 --tracker=none --run=d18-climbmix 
    --core-metric-max-per-task=50 --save-every=250
```

**状态：**
- **GPU：** 已用 5,330 MiB / 总计 12,282 MiB — 相比之前有更充裕的余量（旧运行在评估时曾推高到 9.35 GiB）
- **配置与崩溃时相同：** d18，701M 参数，3,712 次迭代，每步 1,048,576 tokens，512 梯度累积步
- **阶段：** 启动完成 — 当前处于（或即将完成）`torch.compile` 预热阶段，随后第 0 步开始

**预期：**
- 约 58 秒/步 → 第一个 checkpoint 在**第 250 步**，约 4 小时后出现（`/mnt/data/nanochat-cache/base_checkpoints/d18/`）
- 危险的 CORE 评估现在使用 `max-per-task=50` 而非 500 — 评估批次大幅缩小，应能避免第 2000 步和最后一步的 OOM
- 全部 3,712 步总预计时间：**约 2.4 天**

后续查看：`tmux attach -t 1`