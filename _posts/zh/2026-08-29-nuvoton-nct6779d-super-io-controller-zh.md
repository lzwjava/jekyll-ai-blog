---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 新唐NCT6779D超级I/O控制器
translated: true
type: note
---

**问题：** MSI B85M-E45 主板内的 Nuvoton NCT6779D 芯片是什么？

**答案：**

Nuvoton NCT6779D 是主板的 **Super I/O（超级输入/输出）控制器**——本质上是一个负责实时监控和管理系统健康状态的芯片。它是现代主板上最重要的“幕后”芯片之一。

---

**它的功能：**

**1. 硬件监控**
NCT6779D 监控 PC 硬件中的多个关键参数，包括电源电压、风扇转速和温度。这使得 HWiNFO、HWMonitor 或 MSI 自带工具等软件能够显示实时系统读数。

**2. 温度检测**
该芯片支持多达 25 个温度监控源。其中最多 6 个是直接温度传感器输入，其余为特殊源，如 PECI（用于 CPU 温度）、PCH 和 SMBus。

**3. 风扇转速控制**
NCT6779D 支持 Smart Fan 控制系统，包括 SMART FAN I 和 SMART FAN IV，增强了系统稳定性和用户友好性。它可监控最多 5 个风扇，并提供 3 个风扇转速控制输出。这就是驱动你在 BIOS 中配置的自动风扇转速曲线的关键。

**4. 电压监控**
拥有 8 到 15 个模拟电压传感器，用于跟踪 12V、5V、3.3V 和 CPU VCore 等电压轨，确保一切保持在安全范围内。

**5. 传统 I/O 功能**
NCT6779D 提供两个高速串行通信端口（UART），并支持 PC 兼容的打印机端口（SPP）、双向打印机端口（BPP）、增强型并行端口（EPP）和扩展功能端口（ECP）。它还处理 **PS/2 键盘和鼠标**接口。

**6. 与系统的接口**
这是一款高度集成的 LPC Super I/O 控制器，专为 PC 和嵌入式主板平台设计，通过 LPC 总线结合了广泛的硬件监控、风扇控制和传统 I/O 功能，以最少的外部组件实现全面的系统管理。

---

**通俗来说：** NCT6779D 就是“守护”你 PC 的芯片——读取温度、控制风扇转速，并维持传统端口（如 PS/2）的运作。监控软件显示 CPU/主板温度和电压时，读取的来源正是它。

---

**参考资料：**

- [NCT6779D 特性与应用 – Avaq](https://www.avaq.com/technology/nct6779d-nuvoton-datasheet-pdf-features-and-application)
- [NCT6779D 数据手册 – Datasheetgo](https://datasheetgo.com/NCT6779D-datasheet-pdf-788178/)
- [NCT6779D 的 Linux 内核 hwmon 驱动](https://www.kernel.org/doc/Documentation/hwmon/nct6775)
- [NCT6779D 数据手册 PDF – TheRetroWeb](https://theretroweb.com/chip/documentation/nct6779d-novoton-644e9adf2d0db520875332.pdf)
