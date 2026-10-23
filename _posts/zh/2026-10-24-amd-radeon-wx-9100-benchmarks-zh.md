---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AMD Radeon WX 9100 基准测试
translated: true
type: note
---

现在一切都一致了。以下是完整的情况。

## 环境

`nvidia-smi` 运行失败——这台机器上**没有 NVIDIA GPU 或驱动程序**（只有过时的 NVIDIA 用户空间包）。实际使用的 GPU 是：

- **AMD Radeon PRO WX 9100** — Vega 10，`gfx900`，64 个计算单元，1500 MHz，15.98 GiB HBM2，2048 位总线
- 工具链：**ROCm 7.1 / hipcc (clang 21)** 可正常工作

## 基准测试程序

我创建了 `gpu_bench.hip`（自包含，无需 rocBLAS 头文件）：

```bash
hipcc -O3 --offload-arch=gfx900 -o gpu_bench gpu_bench.hip
./gpu_bench --size 4096 --iters 20 --burn 20
```

该程序运行一个朴素的分块 SGEMM、一个寄存器分块的 SGEMM、一个 D2D 复制带宽测试，以及一个持续的 FMA 烧机循环。

## 结果（WX 9100）

| 测试项 | 结果 | 相对于峰值的百分比 |
|---|---|---|
| 复制带宽（读写） | **351 GB/s** | 约 ~484 GB/s HBM2 的 ~72% |
| FP32 GEMM（朴素，每线程 1 元素） | **2.22 TFLOPS** | 18% |
| FP32 GEMM（寄存器分块 4×4） | **4.12 TFLOPS** | 约 ~12.3 TFLOPS 的 ~34% |
| 烧机循环（持续 FMA） | **3.77 TFLOPS** | ~31% |

在烧机负载下，显卡保持在 **1500 MHz SCLK / 945 MHz MCLK，功耗约 170 W**，结温稳定在 **90–99 °C** 左右（边缘温度约 66 °C，显存温度约 67 °C）。显卡运行稳定，但结温接近 99 °C 较高——在运行长时间任务前建议检查气流。

## 备注

- 寄存器分块内核通过复用寄存器中的操作数，将 FP32 吞吐量大致**翻倍**。经过调整/缓存的内核（如 rocBLAS）或更宽的向量化加载加上双缓冲将更接近约 12 TFLOPS 的 FP32 性能上限。
- 过程中遇到一个 Bug：烧机循环最初在没有同步的情况下排队内核，导致大量积压。已通过同步每次启动并修正 FLOP 计算（只有 `grid*block` 数量的线程处于活动状态，而非所有 64M 元素）修复。
- 文件已保留在位置：`/home/lzw/projects/nanoGPT/gpu_bench.hip` 以及编译后的 `gpu_bench` 二进制文件。

需要我尝试 `rocBLAS` 版本（需 `librocblas-dev`）或 FP16 路径来测量更接近峰值的结果吗？