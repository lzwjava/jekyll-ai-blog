---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Uno TX/RX LED无法通过代码控制
translated: true
type: note
---

以下是您系统上**实际源代码**确认的内容：

---

## 1. LED_BUILTIN 定义 — 已确认

**文件：** `~/.arduino15/packages/arduino/hardware/avr/1.8.8/variants/standard/pins_arduino.h`（第 54 行）

```c
#define LED_BUILTIN 13
```

这是 ATmega328P 上的 **引脚 13 (PB5)** —— 即 `L` LED。这是一个完全通过 `digitalWrite` 控制的 GPIO。

## 2. TX/RX LED 定义 — Uno 上不存在

Uno 的 `pins_arduino.h` 中**没有**任何 TX/RX LED 宏定义。其他所有引脚定义（SPI、I2C、模拟）都存在——但 TX/RX 没有。

**确实**定义了 `TX_RX_LED_INIT` 的开发板都是基于 **原生 USB (ATmega32u4)** 的：

| 开发板 | 文件 | TX LED | RX LED |
| ------- | ------ | -------- | -------- |
| Leonardo | `variants/leonardo/pins_arduino.h:94` | PD5 (D5) | PB0 (D8) |
| Micro | `variants/micro/pins_arduino.h:35` | PD5 | PB0 |
| Robot Control | `variants/robot_control/pins_arduino.h:31` | PD5 | PB0 |
| Circuit Playground | `variants/circuitplay32u4/pins_arduino.h:100` | 单独处理 | |

**Uno = 不在该列表中。** 因为 Uno 的 TX/RX LED 位于 **ATmega16U2**（单独的 USB 桥接芯片）上，而不是主 ATmega328P 上。328P 上没有引脚编号可以映射到它们。

## 3. USBCore.cpp — 仅针对原生 USB 编译

**文件：** `~/.arduino15/packages/arduino/hardware/avr/1.8.8/cores/arduino/USBCore.cpp`（第 24–29 行）

```c
#if defined(USBCON)   // ← 在 Uno 的 ATmega328P 上未定义
#define TX_RX_LED_PULSE_MS 100
volatile u8 TxLEDPulse;
volatile u8 RxLEDPulse;
```

TX/RX LED 脉冲系统确实存在，但受 `USBCON` 保护——只有具有原生 USB 的开发板（Leonardo、Micro 等）才会编译此代码。Uno 的 328P 不会。

## 4. 延时代码 — IDE 中无自动修改

我搜索了整个 Arduino IDE 源代码（`arduino-ide-extension/`）中的 "blink"、"delay"、"example"——IDE 只是一个 GUI 外壳。它通过 `ExamplesService` 协议提供内置示例，但**不会**自动生成或修改用户草稿中的延时值。3000ms → 100ms 的更改是您在草稿中手动完成的。

---

## 从源代码得出的结论

之前的回答是**正确的**：

| 声明 | 源代码验证？ |
| ------- | :---: |
| `LED_BUILTIN` = 引脚 13 | ✅ `pins_arduino.h` 第 54 行 |
| 在 Uno 上无法从草稿控制 TX/RX LED | ✅ `variants/standard/` 中无 `TX_RX_LED_INIT` |
| TX/RX LED 由 16U2 驱动，而非 328P | ✅ 由架构确认——328P 上无 `USBCON` |
| `delay(100)` 是有效的 Arduino 代码 | ✅ 不存在 IDE 级别的修改；这是手动草稿编辑 |
| Circuit Playground 使用 ATmega32u4 原生 USB | ✅ `circuitplay32u4` 变体有自己的 `TX_RX_LED_INIT = 0` |
