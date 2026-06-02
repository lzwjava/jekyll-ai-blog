---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 使用nvidia-smi监控GPU使用情况
translated: true
type: note
---

要实时查看 GPU 使用率变化，只需使用循环标志：

**基础实时刷新**

```
nvidia-smi -l 1
```

该命令每秒更新一次。您可以将 `1` 替换为任意秒数间隔。

**如需查看更详细统计（按进程使用情况）**

```
nvidia-smi pmon -s um -d 1
```

该命令每秒显示各进程的 GPU 利用率（`u`）和显存占用（`m`）。

**如需持续获取完整 GPU 统计信息**

```
nvidia-smi --query-gpu=timestamp,utilization.gpu,utilization.memory,memory.used,memory.total --format=csv -l 1
```

该命令每秒输出一行包含利用率和显存信息的简洁数据。

如需将输出记录到文件或需要自定义格式，请随时告知。
