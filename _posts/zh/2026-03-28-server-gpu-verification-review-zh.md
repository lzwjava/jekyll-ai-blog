---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 服务器硬件与 GPU 验证审查
translated: true
type: note
---

### 📋 Review: How I Checked the Server

**What I did (single SSH command, chained):**

1. **`lscpu`** — 从 `/proc/cpuinfo` 获取 CPU architecture 详情。显示 cores、threads、model 以及 flags（如 AVX-512 等 instruction sets）。

2. **`free -h`** — 读取 `/proc/meminfo` 并以 human-readable 格式显示 total/used/available memory。

3. **`nvidia-smi`** — NVIDIA 的管理工具。报告 GPU model、VRAM、driver version、temperature 和 utilization。*Failed* 原因是 driver 未安装。

4. **`lspci | grep -i gpu`** — 原始 PCIe bus 扫描。无论 driver 状态如何，都能显示物理连接的 hardware。正是通过这个命令发现了 RTX 3090。

5. **`cat /proc/driver/nvidia/version`** — 检查 kernel module 是否已加载。*Failed* — 确认没有 driver。

---

**What I could've done better:**

- **`lshw` 或 `dmidecode`** — 更详细的 hardware inventory（BIOS、具体的 memory DIMMs 等）。
- **`cuda-smi` 或 `glxinfo`** — 如果存在 CUDA runtime 但没有完整 driver，可作为替代的 GPU 检查方式。
- **`/proc/driver/nvidia/gpus/*/information`** — 另一个 driver-level 检查。
- **Stress test** — 在 driver 安装后，使用 `gpu-burn` 或 `cuda-samples` 实际测试 GPU 的 benchmark。
- **VRAM size** — 我根据 RTX 3090 的型号名称推断为 24 GB，但实际上没有进行经验验证（没有 driver 无法验证）。

**What went well:**

- Single-shot command — 减少了不必要的交互次数。
- `lspci` 在 `nvidia-smi` 失败时挽救了局面 — 良好的 fallback 机制。
- 发现了差异：Alibaba 称其为 "G39"，但实际硬件是 RTX 3090。

Want me to dig deeper with `lshw` or `dmidecode` for a more complete picture?