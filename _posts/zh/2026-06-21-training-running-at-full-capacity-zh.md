---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 满负荷进行训练
translated: true
type: note
---

训练运行正常，完全没有卡住。

状态：

- 进程 PID 71496：运行中，CPU 占用 99%，已运行 83 分钟
- GPU：RTX 4070，利用率 100%，显存占用 5050 MiB，温度 65°C，功耗 208W
- 脚本：`train.py config/train_github_code_124m.py`，基于 nanoGPT

目前为止仅有的输出是两条警告（已弃用的 GradScaler API + “not enough SMs for max_autotune_gemm”），但 GPU 满负载运行且占用 5GB 显存，确认正在进行实际计算。inductor/compile 步骤可能起初较慢，但现在正在全力运算中。
