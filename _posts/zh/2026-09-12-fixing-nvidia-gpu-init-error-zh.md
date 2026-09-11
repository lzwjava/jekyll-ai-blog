---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复NVIDIA GPU初始化错误
translated: true
type: note
---

**问题：** 此 GPU 初始化错误是什么意思，如何修复？

**回答：**

此屏幕显示来自 **NVIDIA 的 MODS（模块化诊断套件）** 在 **GeForce GT 730 (GK208)** GPU 上运行 GPU 测试（`gputest.js`）的输出。该 GPU 初始化失败。

**屏幕关键信息：**

| 字段 | 值 |
| --- | --- |
| 设备 ID | GK208 (GT 730) |
| 修订版本 | b1 |
| NV Base | 0xf6000000 |
| FB Base | 0xe0000000 |
| IRQ | 11 |

**错误解析：**

- `Error 229 – Gpu.Initialize`：硬件未初始化——GPU 未能完成其初始化序列。
- `Error 229 – Global.PrintGpuInitError`：确认初始化失败。
- `Error 229 – Global.InitializeGpuTests`：由于硬件未就绪，GPU 测试无法运行。
- `Error 237 – Global.EnableUserInterface unable to set mode`：因上述失败，无法设置显示模式。

**红色 `#` 字符块** 是 MODS 视觉呈现的故障模式（本质上是一个"FAIL"图形）。

**可能的原因与修复方法：**

1. **GPU 故障或未插紧** — 重新插拔 PCIe 插槽中的显卡；清洁金手指。
2. **电源功率不足** — 检查 PCIe 电源连接器是否已正确连接。
3. **VBIOS 损坏** — GPU BIOS 可能已损坏；可能需要重新刷写。
4. **硬件故障** — GPU 可能存在显存故障或硅片损坏（在二手 GT 730 上常见）。
5. **驱动/操作系统不匹配** — 确保在运行 MODS 前加载了正确的 NVIDIA 驱动。

由于 MODS 是低级诊断工具（通常用于制造/维修领域），如果此测试持续失败，GPU 本身很可能存在**缺陷**。

**参考来源：**

- [NVIDIA MODS 文档](https://developer.nvidia.com/mods)
- [GK208 (GT 730) 架构概述](https://www.techpowerup.com/gpu-specs/nvidia-gk208.g186)
