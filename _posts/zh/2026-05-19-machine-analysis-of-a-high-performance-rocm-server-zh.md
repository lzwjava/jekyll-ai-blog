---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 高性能ROCm服务器的机器分析
translated: true
type: note
---

## 机器分析：`129.212.178.209`

### 概览

| 属性 | 值 |
| --- | --- |
| 主机名 | `7` |
| 操作系统 | Ubuntu 24.04.4 LTS (Noble Numbat) |
| 内核 | 6.8.0-106-generic (x86_64) |
| 运行时间 | ~54 分钟（新启动） |
| 虚拟化 | **KVM/QEMU** (pc-q35-6.1) |

---

### CPU — Intel Xeon Platinum 8568Y+（虚拟化）

| 属性 | 值 |
| --- | --- |
| vCPU | **20 核心**，1 插槽，每核心 1 线程 |
| ISA | x86_64，AVX-512（完整支持：VL, DQ, BW, BF16, VNNI, VBMI, FP16 等） |
| L1 缓存 | 640 KB（32 KB × 20 实例） |
| L2 缓存 | 总计 80 MB（4 MB × 20） |
| BogoMIPS | 4600.00 |
| 虚拟机监控器 | KVM，支持 VT-x 的全虚拟化 |

这是真实 Intel Xeon 的云 VM 切片——你获得了 20 个专用核心，带有强大的 AVX-512 支持，这对 LLM 服务中的 token 嵌入吞吐量和预填充阶段至关重要。

---

### GPU — AMD Instinct **MI300X VF** (gfx942 / CDNA3)

| 属性 | 值 |
| --- | --- |
| 型号 | AMD Instinct MI300X VF |
| 架构 | **gfx942** (CDNA3) |
| 计算单元 | **304**（32 个 SE × ~9.5 CU/SE） |
| SIMD | 1,216（每 CU 4 个） |
| 最大时钟频率 | **2,100 MHz** |
| **显存** | **191.7 GiB**（205,822,885,888 字节） |
| 显存已用 | ~286 MB（基本空闲） |
| GTT 内存 | ~118 GiB 可用 |
| L2 缓存 | 4 MB |
| L3 缓存 | **256 MB** |
| PCIe | **Gen5 x16 @ 32 GT/s** |
| 计算分区 | SPX（单 GPU） |
| 内存分区 | NPS1（单分区，非 NUMA 拆分） |
| 温度 | 43°C 结温 / 38°C 显存 |
| 功耗 | **157W 空闲** |
| GPU 利用率 | **0%**（完全空闲） |
| 状态 | **低功耗模式**（自动休眠） |

这是顶级的 AMD 数据中心 GPU——192 GB HBM3，非常适合大型模型推理（Llama-405B、DeepSeek-V3 在 FP8 下）。低功耗状态只是表示没有运行任何工作负载；加载任务后会自动升至全时钟频率。

---

### ROCm 软件栈

| 组件 | 版本 |
| --- | --- |
| **ROCm** | **7.2.0** (70200-43) |
| 驱动 | 6.16.13 |
| HIP SDK | 7.2.26015 (AMD clang 22.0.0) |
| rocm-smi-lib | 7.8.0 |
| ROCm LLVM | 22.0.0 |
| ROCgdb | 16.3 |
| MIOpen | ✓ 已安装 |
| MIGraphX | ✓ 已安装 |
| RCCL（NCCL 替代品） | ✓ 已安装 |
| OpenCL | ✓ 2.0 |
| OpenMP | ✓ 已安装 |

完整的 ROCm 工具链已安装——包括 HIP 编译器、调试器、ML 库（MIOpen、MIGraphX、RCCL）。你可以编译 HIP/C++ 内核，或使用带有 ROCm 后端的 PyTorch。

**缺失**：未安装 PyTorch 或任何 Python ML 包（仅有 PyYAML）。你需要安装带有 ROCm 支持的 `torch`。

---

### 内存与存储

| 资源 | 总量 | 已用 | 空闲 |
| --- | --- | --- | --- |
| 系统内存 | **235 GiB** | 5.7 GiB | 229 GiB |
| 交换空间 | 0（未配置） | — | — |
| 系统盘 (vda1) | 719 GB | 87 GB | **610 GB 空闲** |
| **数据盘 (vdc1)** | **5 TB** | — | **未挂载** |

关键观察：**5TB 数据盘已格式化（ext4）但未挂载**。你需要将其挂载——非常适合存放模型权重、数据集或 Docker 卷。

---

### Docker

| 属性 | 值 |
| --- | --- |
| Docker | 29.3.0 + Compose v5.1.0 |
| 运行中的容器 | `rocm` — 端口 **8888**（可能是 Jupyter） |
| GPU 访问 | ✓ 已确认（可访问 /dev/kfd、/dev/dri） |

---

### 网络

| 接口 | IP | 用途 |
| --- | --- | --- |
| eth0 | 129.212.178.209/20 | 公共 / AMD DevCloud |
| eth1 | 10.128.0.2/20 | 私有/内部 |
| docker0 | 172.17.0.1/16 | Docker 桥接 |

---

### 总体评估

这是一个 **AMD DevCloud ATL1 实例**——一个云分配的 MI300X 开发节点。它刚刚启动，完全空闲，配备 192 GB 的大规模 GPU，适合处理大型模型。

**即时建议：**

1. **挂载 5TB 磁盘** — 执行 `mount /dev/vdc1 /data` 或类似操作，然后添加到 fstab
2. **为 ROCm 安装 PyTorch** — `pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm7.2`
3. **唤醒 GPU** — 低功耗状态是正常的；加载工作负载后会自唤醒
4. 如果需要 NUMA 感知的多进程访问，考虑将内存分区切换为 **NPS4**（当前为 NPS1，将 GPU 视为单一内存池——对单进程推理没问题）

需要我挂载 5TB 磁盘并安装 PyTorch 吗？
