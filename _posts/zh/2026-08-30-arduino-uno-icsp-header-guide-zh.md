---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Arduino Uno ICSP 接头指南
translated: true
type: note
---

**问题：** Arduino Uno 板上的 ICSP 是什么？

**回答：**

**ICSP** 代表 **In-Circuit Serial Programming**（在线串行编程）。它是 Arduino Uno 板上一个 6 针（2×3）排针连接器，用于直接对 AVR 微控制器进行编程——绕过常规的 USB/引导加载程序方法。

**物理位置**
在 Arduino Uno 上，实际上有 **两个** ICSP 排针：

- **ICSP** —— 连接到主 **ATmega328P**（主微控制器）
- **ICSP2** —— 连接到负责 USB 转串行通信的 **ATmega16U2** 芯片

**引脚布局（2×3）**

| MISO | VCC |
|------|-----|
| SCK  | MOSI |
| RST  | GND |

MISO、MOSI 和 SCK 在 ICSP 排针上位于一致的物理位置，并且依赖 SPI 接口的扩展板也会使用这个连接器，从而允许设计出能在所有板上工作的扩展板。

**主要用途**

1. **烧录引导加载程序** —— 如果引导加载程序损坏或想要安装自定义引导加载程序，ICSP 允许直接使用外部编程器或另一块 Arduino 进行烧录。
2. **绕过引导加载程序** —— 直接将固件上传到芯片，以获得更快的上传速度和更多的闪存空间使用。
3. **SPI 通信** —— SPI 接口（以及这些引脚）是用于编程 AVR 微控制器的接口。
4. **备用编程方式** —— 当 Arduino 的 USB 端口损坏或失效时，ICSP 引脚特别有用，因为它们允许从外部源进行编码和启动。

**常规编程 vs. ICSP 编程**

| 方式 | 通过 USB（常规） | 通过 ICSP |
| --- | --- | --- |
| 使用引导加载程序 | ✅ 是 | ❌ 否 |
| 需要额外硬件 | ❌ 否 | ✅ 需要编程器 |
| 引导加载程序占用的闪存 | 约 0.5 KB | 无浪费 |
| 速度 | 较慢 | 较快 |

在日常 Arduino 项目中很少用到 ICSP——它主要用于高级用途，例如恢复引导加载程序或直接芯片编程。

---

**参考：**

- [Arduino as ISP and Arduino Bootloaders – Arduino 文档](https://www.arduino.cc/en/Tutorial/ArduinoISP)
- [安装 Arduino 引导加载程序 – SparkFun](https://learn.sparkfun.com/tutorials/installing-an-arduino-bootloader/hardware-hookup)
- [Arduino 的十六进制文件与 ICSP 引脚 – C# Corner](https://www.c-sharpcorner.com/article/hex-file-and-ics-pins-of-arduino/)
