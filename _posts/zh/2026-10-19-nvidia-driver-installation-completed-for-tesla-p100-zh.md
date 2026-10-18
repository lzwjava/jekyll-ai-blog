---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NVIDIA Tesla P100 驱动程序安装完成
translated: true
type: note
---

已完成。NVIDIA 驱动程序已安装，Tesla P100 现已激活。

## 总结

**检测到的 GPU：** `NVIDIA Tesla P100 PCIe 16GB` (GP100, Pascal)

**执行的安装步骤：**
1. 识别出操作系统（Ubuntu 26.04 LTS）并确认未安装 NVIDIA 驱动程序。
2. 使用 `ubuntu-drivers devices` → 推荐驱动程序 `nvidia-driver-580`。
3. 通过 apt 安装了 `nvidia-driver-580`（版本 **580.178.04**，CUDA 13.0）。
4. 发现 `nouveau`（开源驱动程序）已占用 P100 并阻止了 NVIDIA 模块，因此添加了 `/etc/modprobe.d/blacklist-nouveau.conf`，运行 `update-initramfs -u`，然后解除 nouveau 绑定并加载 NVIDIA 堆栈。

**当前状态 — 正常工作：**
```
NVIDIA-SMI 580.178.04   Driver Version: 580.178.04   CUDA Version: 13.0
Tesla P100-PCIE-16GB | 00000000:01:00.0 | 0MiB / 16384MiB | 0%
```
- P100 绑定至 `nvidia` 驱动程序
- 设备节点存在（`/dev/nvidia0`、`/dev/nvidiactl` 等）
- `nvidia-persistenced` 服务已激活（建议用于 Tesla 卡）
- Nouveau 黑名单已持久化；启动服务（`nvidia-powerd`、挂起/恢复）已启用

**注：** 旧的 `nouveau` 模块仍保留在当前运行的内核会话中，尽管它不再拥有 P100。重启将提供完全干净的状态，并确认持久性自动加载。由于显示器由 Intel `i915` GPU 驱动，重启是可选的——P100 现在已可立即使用。

您可以使用 `nvidia-smi` 进行验证，或者添加 CUDA 工具包后使用 `nvidia-smi -q` / `nvcc --version`。

您是否希望我还安装 CUDA 工具包以用于计算工作负载？