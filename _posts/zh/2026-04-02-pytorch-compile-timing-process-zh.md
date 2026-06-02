---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 理解 PyTorch 编译过程与时序
translated: true
type: note
---

幕后正在发生什么：

## torch.compile() — 它做了什么

`torch.compile()` 通过 **TorchInductor** 将您的模型转换为优化的 CUDA kernels。它不仅仅是简单意义上的 just-in-time —— 它经历了多个阶段：

### 阶段 1：Graph Tracing（您在 iter 0 看到的）

- Torch 运行一次模型，将每个操作记录到 computational graph 中
- 这很慢，因为它运行的是未优化的版本
- iter 0 的 113s 就是这个阶段

### 阶段 2：Kernel Compilation（现在正在发生）

- Inductor 分析 graph 并为每个 operation 生成 **C++/CUDA kernels**
- 它跨 24 个 workers（`--workers=24`）并行化以加速
- 每个 kernel 独立编译，然后链接在一起
- 这就是为什么您仍然看到 21s/step —— kernel compilation 仍在进行

### 阶段 3：Code Generation & Optimization

- 一旦 kernels 准备好，Inductor 融合 ops（例如，将 matmul + bias + activation 结合到一个 kernel 中）
- 减少 memory bandwidth 和 kernel launch overhead

## 为什么现在很慢

compile workers 仍在后台构建 kernels。您的 GPU 利用率为 100%，因为它在运行未优化的模型 + 同时编译新 kernels。这就是为什么：

- 功耗高 (691W) —— GPU 正在努力工作
- 但 step time 仍是 21s —— 因为 compute graph 尚未融合/优化

## 何时会变快

一旦所有 workers 完成（对于 1.5B 模型，通常在训练开始后 2-10 分钟），您将看到：

- Step time 从 21s 降至 **1-3s**
- MFU 跃升至现实数字 (50-70%+)
- “compiling the model...” 消息不会再出现

## 您的当前状态

```
GPU: 100% Util ✓ — 正在工作，不是空闲
Power: 691W ✓ — 负载下
Memory: 77GB ✓ — model 已正确加载
Workers: 24 compile workers 正在运行 — 等待完成
```

一切看起来都正确。21s/step 是临时的 compilation overhead。到 iter 100-200，您很可能就会看到真实速度。

## 还有一件事

如果 `compile = True` 但您宁愿跳过等待并直接运行（较慢但立即可用），您可以设置 `compile = False`。但由于您还有 4-5 小时的训练时间，compile 等待（5-10 分钟）是值得的 —— 它将后续每个 step 加速 5-10 倍。🦞
