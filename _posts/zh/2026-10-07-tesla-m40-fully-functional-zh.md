---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Tesla M40 功能完好
translated: true
type: note
---

🎉 **一切完美运行！** Tesla M40 现已完全正常工作：

```
NVIDIA-SMI 550.163.01        Driver Version: 550.163.01     CUDA Version: 12.4
GPU 0: Tesla M40 24GB        Bus-Id: 00000000:01:00.0       Off
Temp: 31C   Perf: P8        Pwr: 16W / 250W     Mem: 6MiB / 24576MiB   Util: 0%
```

## 最终状态 — 全部完成 ✅

| 任务 | 结果 |
| --- | --- |
| SSH密钥认证到 `lzw@192.168.1.137` | ✅ |
| `lzw` 已加入 sudo 组 | ✅ |
| NVIDIA 驱动 550.163.01 已安装（支持 M40） | ✅ |
| BIOS 从 A.50 升级至 **A.A** | ✅ |
| 已启用 "Above 4G Decoding" | ✅ |
| GPU BAR 已分配（BAR1 = 32GB，BAR3 = 32MB） | ✅ |
| `nvidia-smi` 检测到 **Tesla M40 24GB**（24576 MiB） | ✅ |
| CUDA 驱动 v12.4 已激活 | ✅ |

显卡空闲，温度 31°C / 功耗 16W，完全识别。

## 建议的后续步骤（可选）

1. **启用持久模式**，让 GPU 保持初始化状态，避免任务间重置：

   ```bash
   sudo nvidia-smi -pm 1
   ```

2. **安装 CUDA 工具包**，如果你计划运行计算工作负载（PyTorch、TensorFlow 等）：

   ```bash
   sudo apt install nvidia-cuda-toolkit     # Debian 打包的 CUDA
   ```

   或从 NVIDIA 安装特定 CUDA 版本。

3. **测试计算能力**，快速检查，例如：

   ```bash
   nvidia-smi -q | head -20
   ```

需要我现在帮你启用持久模式并/或安装 CUDA 工具包吗？
