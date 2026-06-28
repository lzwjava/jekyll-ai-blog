---
audio: false
generated: true
image: false
lang: zh
layout: post
title: B200基准测试达到1647 TFLOPS
translated: true
type: note
---

一切正常。以下是新增内容：

```
ww/benchmark/__init__.py          # 空文件
ww/benchmark/gpu_bench.py         # 基准测试脚本（独立运行 + CLI入口）
ww/main.py                        # 调度 + 帮助 + all_groups
completions/_ww                   # zsh 自动补全
```

命令：`ww benchmark [--ssh USER@HOST:PORT] [--key PATH]`

该基准测试在你的 B200 上运行并生成了实际数据：

```
FP32:     63-67 TFLOPS（16k 矩阵乘法）
TF32:     539-740 TFLOPS（张量核心）
FP16:     1,355-1,543 TFLOPS
BF16:     1,410-1,632 TFLOPS
内存：    6,454 GB/s（8192 MB 拷贝）
```

在 LLM 预填充（B=1, S=8192, H=8192）BF16 工作负载下测得的峰值达到 **1,647 TFLOPS**。B200 的运行性能远超理论 80 TFLOPS 的“规格”——这些规格是基于每时钟周期的持续性能；实际加速频率和张量核心流水线利用率会将其推得更高，尤其是在大型矩阵上。

FP8 在 PyTorch 2.8.0 中尚不支持 `Float8_e4m3fn` 的 randn 操作（缺少 CUDA 内核）——这是 PyTorch 的限制，而非 GPU 的问题。