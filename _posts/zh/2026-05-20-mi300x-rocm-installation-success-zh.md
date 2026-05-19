---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MI300X ROCm 安装成功
translated: true
type: note
---

一切正常。以下是最终结果：

---

## ROCm 栈 — 完全可用

**`rocm-smi`**（AMD 的 nvidia-smi 对应工具）：
```
GPU  Temp    Power   SCLK    MCLK   PwrCap   VRAM%  GPU%
0    37.0°C  154.0W  139MHz  900MHz 750.0W   0%     0%
```

**`rocminfo`** — 完整 GPU 规格：
```
AMD Instinct MI300X VF (gfx942)
  304 Compute Units | 1216 SIMDs | 32 Shader Engines
  191 GB HBM3 | 2100 MHz max clock
  Wavefront: 64 | Workgroup: 1024
```

**HIP 计算测试：**
```
HIP devices: 1
Device 0: AMD Instinct MI300X VF
  Memory: 191 GB
  Compute units: 304
  Clock: 2100 MHz
```

---

## 是什么损坏了以及如何修复

| 步骤 | 问题 | 修复 |
|------|------|------|
| 1 | `rocm-smi` 未安装 | 从 AMD 仓库使用 `apt install rocm-smi` |
| 2 | `rocm-smi` 显示“未检测到 AMD GPU” | MI300X 缺少固件 |
| 3 | 带版本号与不带版本号的包冲突 | 强制清除，安装带版本号的 `*7.2.3` 包 |
| 4 | 缺少 `libxml2.so.2`（Ubuntu 25.10 包含 `.so.16`） | 创建符号链接：`libxml2.so.2 → libxml2.so.16` |
| 5 | 缺少固件文件（psp/gc/sdma/vcn） | `apt install linux-firmware` + 重新绑定 GPU |
| 6 | GPU 驱动初始化失败 → HIP 检测到 0 个设备 | 安装固件并重新绑定后：GPU 初始化成功，HIP 检测到 1 个设备 |

## 现在可用的命令

```
rocm-smi              # GPU 状态（温度、功耗、时钟、利用率）
rocminfo              # 完整硬件拓扑
amd-smi               # 原有的 PCI 级别信息工具（仍然可用）
hipcc                 # HIP C++ 编译器
rocm_agent_enumerator # 列出 GPU 架构
```

环境已通过 `/etc/profile.d/rocm.sh` 永久设置（PATH、ROCM_PATH、LD_LIBRARY_PATH）。