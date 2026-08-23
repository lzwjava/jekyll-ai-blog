---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解读GPU-Burn基准测试输出
translated: true
type: note
---

**问题：** 如何读取/解读 gpu-burn 基准测试的输出？

**回答：**

以下是输出各个部分的详细说明：

---

### 设置信息
```
GPU 0: NVIDIA GeForce RTX 4070
Initialized device 0 with 11839 MB of memory (10248 MB available, using 9223 MB of it), using FLOATS
Results are 268435456 bytes each, thus performing 34 iterations
```
- **11839 MB** — 显卡总显存
- **10248 MB available** — 测试开始时可用显存（部分被操作系统/驱动保留）
- **9223 MB used by test** — gpu-burn 分配约 90% 的可用显存进行压力测试
- **FLOATS** — 使用 32 位浮点精度（相对于 FP64 的 DOUBLES）
- **34 iterations** — 在分配内存中能容纳的矩阵乘法次数

---

### 进度行
```
65.0%  proc'd: 238 (20497 Gflop/s)   errors: 0   temps: 60 C
```

| 字段 | 含义 |
|---|---|
| `65.0%` | 20 秒压力测试已完成的百分比 |
| `proc'd: 238` | 至此已完成的矩阵乘法批次总数 |
| `20497 Gflop/s` | 吞吐量 — **约 20.5 TFLOPs**，你的 GPU 的 FP32 计算速度 |
| `errors: 0` | 未检测到计算错误（数值与 CPU 参考值对比） |
| `temps: 60 C` | 此时 GPU 核心温度 |

---

### 这些数值对 RTX 4070 的意义

- **~20,400 Gflop/s（约 20.4 TFLOPs）** — 稳定且正常；RTX 4070 标称 FP32 约 29 TFLOPs，但 gpu-burn 由于内存带宽和开销通常只能达到峰值的 60–75%，所以这是**正常表现**
- **温度最高 61°C** — 满负载下非常凉爽；散热余量极佳
- **errors: 0** — GPU 计算稳定，无内存位翻转或计算错误
- **最终判定：`GPU 0: OK`** — 显卡通过了压力测试

---

### 总结

你的 RTX 4070 **状态健康**：在完整的 20 秒压力测试中，吞吐量稳定、温度凉爽、零错误。

---

**参考：**
- [gpu-burn GitHub 仓库](https://github.com/wilicc/gpu-burn)