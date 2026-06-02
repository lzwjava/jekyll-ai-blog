---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI300X ROCm 状态报告
translated: true
type: note
---

====================================================================
               ROCm 与 GPU 状态综合报告
====================================================================

系统

  主机名:     snapshots-gpu-mi300x1-192gb-devcloud-atl1
  内核:       6.8.0-117-generic (Ubuntu 24.04)
  架构:       x86_64

ROCm 栈

  版本:       7.2.0
  HIP:        7.2.26015 (AMD clang 22.0.0)
  HSA 运行时: 1.18
  ROCk 模块:  6.16.13 (已加载)
  安装路径:   /opt/rocm-7.2.0 -> /opt/rocm
  共享库:     60 个 (rocblas, hipfft, rccl, MIOpen 等)
  二进制工具: hipcc, rocm-smi, rocminfo, rocgdb, rocprof, hipify-clang ...

GPU 硬件

  设备:       AMD Instinct MI300X VF
  GFX 目标:   gfx942 (也支持 gfx9-4-generic)
  芯片 ID:    0x74b5
  SKU:        M3000100
  计算单元:   304
  每 CU 的 SIMD: 4
  着色引擎:   32
  波前大小:   64
  最大时钟:   2100 MHz
  快速 FP16:  是
  SRAMECC:    已启用
  XNACK:      已禁用

内存

  VRAM 总量:  ~192 GB (205,822,885,888 字节)
  VRAM 已用:  ~299 MB (299,687,936 字节)
  VRAM 空闲:  ~191.5 GB
  L1 缓存:    32 KB
  L2 缓存:    4 MB
  L3 缓存:    256 MB

温度与功耗

  结温:       43.0 C
  内存温度:   37.0 C
  当前功耗:   157.0 W
^[[40;1R  功耗上限:   750.0 W
  风扇:       不支持 (被动/液冷)

时钟与性能

  fclk:      1300 MHz
  mclk:      900 MHz
  sclk:      131 MHz (空闲)
  socclk:    889 MHz
  性能等级:   auto
  GPU 繁忙:   0% (空闲)

CPU

  型号:        Intel Xeon Platinum 8568Y+
  计算单元:   20
  L1 缓存:    32 MB
  系统内存:   ~247 GB

环境

  PATH:        /opt/rocm/bin (本次会话已添加并持久化到 .bashrc)
  LD_LIBRARY:  /opt/rocm/lib (已持久化到 .bashrc)
  ROCM_PATH:   未设置
  HIP_PATH:    未设置
  PyTorch:     未安装

状态

GPU:         已检测到且空闲
  ROCm:        已完全安装
  工具:        全部存在 (hipcc, rocm-smi, rocminfo, rocgdb, rocprof)
  PATH:        已修复 (添加了 /opt/rocm/bin)
  缺失:        PyTorch/ROCm，ROCM_PATH 和 HIP_PATH 环境变量
====================================================================

关键要点：

- ROCm 7.2.0 已完全安装，包含所有开发/调试/性能分析工具
- MI300X (192GB HBM3) 已检测到，空闲，温度低 (43C)，随时可用
- PyTorch 未安装——如需，可安装 ROCm 版本的 PyTorch
- ROCM_PATH 和 HIP_PATH 环境变量未设置（可选但建议设置）

需要我安装支持 ROCm 的 PyTorch 或设置剩余的环境变量吗？
