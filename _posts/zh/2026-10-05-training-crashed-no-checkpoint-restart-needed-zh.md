---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练崩溃，没有检查点，需要重启
translated: true
type: note
---

没有名为 `a` 的 tmux 会话——你有 **`0`**（mihomo 代理）和 **`1`**（训练）两个会话。训练任务在会话 `1` 中，**并且它已经崩溃了**：

```
torch.OutOfMemoryError: CUDA out of memory ... during CORE metric evaluation
```

**发生了什么**

- 正在运行的命令（从进程列表 / pi 会话日志中恢复）：

  ```bash
  NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache ./.venv/bin/python -m scripts.base_train \
      --depth=18 --max-seq-len=1024 --device-batch-size=2 --tracker=none --run=d18-climbmix
  ```

- 它到达了 **第 2000 步 / 3712（约 54%，约 32 小时）**，然后在 `evaluate_core()` 中的 CORE 指标检查点（`--core-metric-every` 默认为 2000）处 OOM。GPU 现在只剩下桌面进程——任务已经死了。
- ⚠️ **本次运行没有检查点。** `/mnt/data/nanochat-cache/base_checkpoints/d18/` 只有 5 步冒烟测试（`save-every` 默认为 `-1` = 仅在结束时保存）。因此重启意味着 **从第 0 步开始训练**。

**如何重启**

```bash
tmux attach -t 1
```

然后在那个窗格中：

```bash
cd /mnt/data/nanochat
NANOCHAT_BASE_DIR=/mnt/data/nanochat-cache ./.venv/bin/python -m scripts.base_train \
    --depth=18 --max-seq-len=1024 --device-batch-size=2 \
    --tracker=none --run=d18-climbmix \
    --save-every=250
```

**重要——否则它会以同样的方式再次崩溃。** CORE 评估 OOM 是因为训练模型 + 优化器（约 7.8 GiB）仍然驻留，而评估 logits 在你 11.6 GiB 的显卡上还需要约 1.5 GiB，并且 CORE 评估还会在*最终*步骤（3712）重新运行。选择其一：

1. **先释放 VRAM**——关闭使用 GPU 的应用程序（仅 Xorg 就占用约 1.1 GiB，加上浏览器/Chrome 标签页）。评估只需要比可用内存多约 0.4 GiB。
2. **降低评估内存**，例如添加 `--core-metric-max-per-task=50`（更少/更精简的评估批次），或者用 `--core-metric-every=-1` 完全禁用它。
3. **减少训练占用**：`--device-batch-size=1`。

我强烈建议无论如何都加上 `--save-every=250`，这样未来的崩溃不会让你再损失 30 多个小时。
