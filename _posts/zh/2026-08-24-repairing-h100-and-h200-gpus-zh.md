---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复H100和H200 GPU
translated: true
type: note
---

**问题：** 数据中心技术人员如何修复 H100、H200 及类似高端 GPU 卡？

**回答：**

在数据中心修复这些卡涉及分层方法——真正的修复主要通过诊断和组件更换完成，而非板级焊接。实际流程如下：

---

### 1. 首先进行诊断

在接触硬件之前，技术人员会运行软件工具来确认故障：

- NVIDIA 提供 `nvidia-healthmon`，它会输出一份故障排除报告，针对常见问题列出可能解决方案，并按可能性从高到低排列。如果未发现软件或配置问题，则运行 **NVIDIA Field Diagnostic**——这是一款基于 Linux 的综合工具，用于验证 GPU 数值引擎完整性、数据传输完整性以及全内存地址空间覆盖。

---

### 2. 现场可更换单元（FRU）——主要修复方法

数据中心不进行芯片级修复。标准模型如下：

- **现场可更换单元（FRU）** 是一种电路板或组件，可由技术人员在现场拆卸并更换，无需将整个系统送至维修设施。通过标准故障排除找到有缺陷的单元，将其移除，然后丢弃或送回工厂。FRU 方案通常是维护复杂系统最具成本效益的方式。

- NVIDIA 自身的 RMA 检查清单指示技术人员首先**重新插拔** FRU 模块，然后**将其与已知良好的 FRU 交换**，以确认故障在模块本身还是插槽。

---

### 3. 物理更换——实际操作内容

对于 DGX H100/H200 等系统：

- GPU 和散热器的拆卸必须由**经过培训的技术人员**执行。该流程需要两人合作，并使用能够支撑高达 400 磅（181 千克）的起重设备。技术人员必须检查所有连接器和插槽——连接器损坏或插槽内有碎屑的 GPU 不应重复使用。

- 拆卸 GPU 基板时，技术人员使用**扭矩螺丝刀（设置为 0.6 牛·米，即 5.3 英寸·磅）**按特定顺序拧松 Torx T15 螺丝，小心地将 GPU 放置在平坦的静电防护表面上。如果该单元需寄送进行 RMA，则保持手柄连接。

- 对于网卡更换，流程包括：标记所有线缆，滑出主板托架，更换网卡，将托架滑回，按标记重新连接所有线缆，上电，测试——然后将故障单元寄回 NVIDIA Enterprise Support。

---

### 4. RMA——当卡彻底损坏时的处理流程

当组件需要超出现场更换范围的维修时，技术人员联系 **NVIDIA Enterprise Support** 获取 RMA 编号。仅使用 NVIDIA 提供的替换组件。故障单元返回 NVIDIA 进行分析。

---

### 5. 边缘情况：独立板级修复

有些第三方技术人员会进行更深入的修复。一个著名的实际案例：

- 一名维修技术人员修复了一块价值 30,000 美元的损坏 H200 卡，其 12VHPWR 连接器受损。他通过切割并修整替换引脚，然后将其**焊接**到 H200 的电源连接器上。当 PCB 短路导致无法开机时，他通过**断开**连接感测引脚与卡的电阻器，绕过了感测引脚——恢复了功能。

这种组件级 PCB 工作在数据中心很少见（会导致保修失效，且需要专业知识），但在独立维修生态系统中确实存在。

---

### 总结

| 修复级别 | 执行者 | 方法 |
|---|---|---|
| 软件/配置问题 | 内部运维 | nvidia-healthmon、重装驱动 |
| 组件更换（FRU） | 经过培训的数据中心技术人员 | 热/冷插拔、扭矩工具、ESD 防护措施 |
| 整卡故障 | NVIDIA 通过 RMA | 退回并更换 |
| 板级修复 | 专业维修店 | 焊接、电阻器旁路（罕见，会导致保修失效） |

---

**参考资料：**
- [NVIDIA DGX H100/H200 Service Manual](https://docs.nvidia.com/dgx/dgxh100-service-manual/introduction.html)
- [NVIDIA RMA Process Guide](https://docs.nvidia.com/deploy/rma-process/index.html)
- [NVIDIA RMA Checklist](https://network.nvidia.com/support/rma-checklist/)
- [Lenovo H100/H200 GPU Removal Docs](https://pubs.lenovo.com/sr780a-v3/remove_the_h100_gpu_baseboard)
- [Tom's Hardware — H200 板级修复](https://www.tomshardware.com/pc-components/gpus/busted-12vhpwr-connector-sidelines-usd30-000-h200-hopper-gpu-repair-technician-saves-the-data-center-day-by-fixing-power-port)
- [Field-Replaceable Unit — TechTarget](https://www.techtarget.com/searchdatacenter/definition/field-replaceable-unit)