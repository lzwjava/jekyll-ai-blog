---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tesla M40 DeepSpeed 故障
translated: true
type: note
---

🎮 这些 GPU——两块“超级计算机级”的老古董

两个节点各有一块 PCIe GPU，均为 NVIDIA Tesla M40：

- .34：Tesla M40（12 GB），driver 580.178.04，“CUDA 13.0”
- .137：Tesla M40 24 GB，driver 550.163.01，“CUDA 12.4”

Tesla M40 是 2015 年的 Maxwell 架构数据中心显卡（GM200，compute capability 5.2，约 6.8 TFLOPS FP32，无 FP16/tensor cores）。

❌ DeepSpeed：实际测试——不行（而且它把 driver 卡死了）

我在 .34 上安装并测试了两个软件代际（下载过程非常艰难：在这条 CN 网络上，pypi.org/download.pytorch.org 被限速到 13 KB/s，所以我通过 Aliyun 镜像以 28 MB/s 的速度下载）：

1. 现代栈——PyPI torch 2.14.1+cu130 + DeepSpeed 0.16：torch.cuda.is_available() 挂起——CUDA ≥12/13 完全放弃了对 Maxwell 的支持。
2. 旧版栈——torch 1.13.1+cu117（最后一个支持 Maxwell 的 CUDA 代）：CUDA 初始化也挂起。
3. 根本原因（syslog）：两次测试都在内核中把 nvidia_uvm 卡死了——/var/log/syslog 中的堆栈跟踪显示 uvm_api_register_gpu → uvm_ioctl → thread_context_non_interrupt_add。nvidia-smi 本身现在也挂起。driver 的 UVM 无法注册这个 GPU，而且挂起发生在不可杀的 D-state。

⚠️ .34 上需要操作：3 个卡住的进程（PID 88864 nvidia-smi、88959、89100 python）处于 D-state——kill -9 也无法移除。重启 .34 以清理卡死的 GPU driver。.137 没有被测试（相同的 GPU 架构 → 相同的结论）。

### 那么，你能用 DeepSpeed 训练吗？不能——实际上不行：

- 软件墙：DeepSpeed 需要支持 CUDA 的 torch；没有现代 torch 能在 Maxwell 上运行，而且这里系统安装的 driver 甚至无法初始化 CUDA compute。
- 硬件墙：即使你降级所有东西（旧 driver + 2021 时代的栈）：1 GPU/节点，12/24 GB VRAM，4 核 i5，8–11 GB RAM，1 GbE 上行链路，每 GPU 算力 ≈ 单张 RTX 4090 的 1/12。通过 1 GbE 跑 DeepSpeed 多节点将毫无意义。

### 实际选项：

1. 不要用 M40 来训练——它们是显示/旧款显卡。把训练推到任何有现代 GPU 的地方。
2. 如果必须使用这些硬件：在其中一台机器上换装现代 GPU（例如 RTX 3090/4090）——那么 DeepSpeed 就能正常工作（[.34 有 733 GB 可用空间和 915 GB 磁盘；但 12 GB RAM 对于 CPU-offload 来说仍然受限]）。
3. 使用旧版 cu110/cu117 构建 + 旧 driver 做 GPU 推理（而不是训练）——即便如此，仍然需要降级 driver（例如 470/550 分支，不会像 580 那样卡死）。

备注：我在 .34 上留下了两个 venv（~/dsvenv 约 2.5 GB，其中是现代 torch 坏了；~/dslegacy 中是 torch 1.13.1）以及一个约 40 GB 的 uv 下载缓存——可以用 rm -rf ~/dsvenv ~/dslegacy ~/.cache/uv ~/.local/share/uv 随意删除。需要我清理这些和/或检查 .137 上的其他东西吗？