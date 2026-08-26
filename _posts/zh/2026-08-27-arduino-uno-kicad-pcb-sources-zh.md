---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Arduino Uno KiCad PCB 源代码
translated: true
type: note
---

**问题：** 在哪里可以下载适用于 KiCad 的 Arduino Uno PCB 布局文件？

**回答：**

以下是获取与 KiCad 兼容的 Arduino Uno PCB 布局文件的最佳来源：

**1. 官方 KiCad 模板（GitHub）——最佳起点**
KiCad GitHub 仓库在 `kicad-templates` 项目的 `Projects/Arduino_Uno_R3/` 路径下包含一个官方的 Arduino Uno R3 `.kicad_pcb` 文件。
→ [github.com/KiCad/kicad-templates](https://github.com/KiCad/kicad-templates/blob/master/Projects/Arduino_Uno_R3/Arduino_Uno.kicad_pcb)

**2. Alarm-Siren Arduino KiCad 库——用于扩展板/插座封装**
这是一个积极维护的 KiCad 符号和封装库，适用于大多数 Arduino 模块，包括 Arduino Uno R3 Shield、Mega、Leonardo 等。支持 KiCad 6 及以上版本。
在 KiCad 7+ 中，最快的方法是通过 KiCad 的插件和内容管理器 (PCM) 安装：打开插件和内容管理器，找到 "KiCad Library for Arduino Modules" 并安装。
→ [github.com/Alarm-Siren/arduino-kicad-library](https://github.com/Alarm-Siren/arduino-kicad-library)

**3. SnapMagic (SnapEDA) ——符号、封装和 3D 模型**
SnapMagic 为 Arduino Uno Rev3 提供免费的原理图符号、PCB 封装和 3D 模型，支持直接导出到 KiCad、Altium、Eagle、OrCAD 等工具。
→ [snapeda.com – Arduino Uno Rev3](https://www.snapeda.com/parts/Arduino%20Uno%20Rev3/Arduino/view-part/)

**4. 自定义 KiCad 项目 (GitHub) ——完整设计参考**
一个社区设计的完整 Arduino Uno PCB 文件可在 KiCad 中使用，包含 ATmega328P、USB 转串口接口、电压调节器和 I/O 排针。
→ [github.com/Kalash4152/CREATING-ARDUINO-UNO-PCB](https://github.com/Kalash4152/CREATING-ARDUINO-UNO-PCB)

---

**建议：** 如果你仅需要将 Arduino Uno 作为扩展板/模块插入你自己的 PCB 设计中，请使用**选项 2**（通过 KiCad PCM 安装的 Alarm-Siren 库）。如果你想要完整的板级布局来复制或修改 Arduino Uno 本身，请使用**选项 1** 或**选项 4**。

---

**参考链接：**
- [KiCad 模板 – Arduino Uno R3](https://github.com/KiCad/kicad-templates/blob/master/Projects/Arduino_Uno_R3/Arduino_Uno.kicad_pcb)
- [Alarm-Siren Arduino KiCad 库](https://github.com/Alarm-Siren/arduino-kicad-library)
- [SnapMagic – Arduino Uno Rev3](https://www.snapeda.com/parts/Arduino%20Uno%20Rev3/Arduino/view-part/)
- [自定义 Arduino Uno KiCad 项目](https://github.com/Kalash4152/CREATING-ARDUINO-UNO-PCB)