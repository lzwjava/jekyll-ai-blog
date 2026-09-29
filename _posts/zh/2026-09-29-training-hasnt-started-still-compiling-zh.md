---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 训练尚未开始；仍在编译中。
translated: true
type: note
---

## 发现

有 2 个 tmux 会话：
- `0` — 运行 `mihomo`（你的代理/VPN，仅流量日志，无关）
- `1` — 训练运行

**训练尚未开始。** 它仍处于一次性 `torch.compile` 启动阶段。

### 会话 1 中正在发生什么

运行的是 `scripts/base_train.py --depth=18 ... --run=d18-climbmix`（一个 700M 参数模型，18 层）。它在 **15:21** 启动，已运行 **约 4 分钟**，当前卡在最后一行日志：

```
W0929 15:21:26 ... Not enough SMs to use max_autotune_gemm mode
```

之前的所有内容都是配置打印。之后它进入 `torch.compile(model, dynamic=False)` → PyTorch Inductor 追踪/编译 + 自动调优整个模型图。

### 为什么它“慢”（但未卡死）

- **它正在积极工作**：主 PID `1682358` 占用 **103% CPU**（单线程 inductor 代码生成），GPU 使用率 **99%** / 172 W，VRAM 缓慢上升（4318 → 4343 MiB）。卡死的进程会是空闲状态。
- 这是**首次编译，无缓存**：`~/.cache/torch/inductor/` 尚不存在，因此没有可复用的内核缓存。在 RTX 4070 上首次完整图编译一个 700M 模型（含 Flash-Attention-3 + FP8）通常需要 **5–20 分钟**。后续运行将复用缓存，并在数秒内启动。
- `Not enough SMs to use max_autotune_gemm` 行只是一个**警告**（4070 有 46 个 SM，低于激进 GEMM 自动调优的阈值）——它会回退到较轻量的调优模式。这不是错误。
- 额外低效：它生成了 32 个 inductor 编译工作进程，但它们大多空闲（0% CPU），因为主进程中的图代码生成是单线程的——这很正常，工作进程仅在并行 triton 代码生成时才会启动。

### 结论

一切正常——只需等待。编译完成后，进度条会出现，第一个步骤开始。第一步输出将显示 `step ... loss ...`，随后开始训练。

如果需要，我可以通过以下方式加快未来启动速度：
1. 设置一个持久的 `TORCHINDUCTOR_CACHE_DIR`（例如在 `/mnt/data/nanochat-cache/` 下），使编译缓存可复用。
2. 禁用/减少自动调优（`max_autotune=False` / 关闭坐标下降）以缩短首次编译时间，代价是吞吐量降低几个百分点。

需要我持续监控直到第一个训练步骤出现，或者应用上述缓存修复吗？