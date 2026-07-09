---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 控制Arduino的TX和RX指示灯
translated: true
type: note
---

**问题：** 在 Arduino Uno 上，我能否像闪烁 `LED_BUILTIN` 那样闪烁标有 TX、RX 或 R9/R7/R8 的 LED？修改后的延时代码是否正确？

**回答：**

简短回答：**不能直接做到**——TX/RX 由硬件驱动，而非 GPIO 控制。

**原因：**

在 Uno R3 上，USB 接口附近有 3 个板载 LED：

| LED | 驱动源 | 能否通过代码控制？ |
|---|---|---|
| `L`（引脚 13） | ATmega328P PB5，通过电阻（根据版本，丝印通常为 R9） | **可以**——这就是 `LED_BUILTIN` |
| `TX` | ATmega16U2（USB 转串口桥接芯片）的 TXD 线，通过电阻（约 R7） | **不能**——仅硬件控制 |
| `RX` | ATmega16U2 的 RXD 线，通过电阻（约 R8） | **不能**——仅硬件控制 |

TX/RX LED 连接到 **USB 转串口芯片** 的 UART 引脚，而非你的代码可以通过 `digitalWrite` 寻址的任何 GPIO 引脚。每当字节通过 USB 串口传输时（包括 `Serial.print()` 调用和上传代码时），它们会自动点亮。Arduino 核心中没有映射到它们的引脚编号，因此在标准 Uno 硬件上，`digitalWrite(TX_LED, ...)` 是不存在的。

如果你想故意让它们闪烁，唯一的手段是产生串口流量：

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  Serial.println("x");   // TX LED 在此时闪烁
  delay(100);
}
```

这是一种间接且闪烁不定的方式，无法实现干净的亮灭闪烁——不要将其用作你的“闪烁”LED。请使用 `LED_BUILTIN` 进行可控的闪烁。

**你的代码差异：**

意图（100ms 亮 / 100ms 灭，而不是 3000/3000）没问题，但第 10 行的注释已过时（仍然写着 `// 等待 3 秒`，应改为 `100ms`）。更正后：

```cpp
void loop() {
  digitalWrite(LED_BUILTIN, HIGH);  // 点亮 LED
  delay(100);                       // 等待 100ms
  digitalWrite(LED_BUILTIN, LOW);   // 熄灭 LED
  delay(100);                       // 等待 100ms
}
```

这样会在引脚 13（`L`）上产生 5Hz 的闪烁。如果你的目标是在串口/代理通信期间提供视觉指示（例如，当你的 CLI 代理通过串口向板子发送命令时闪烁 LED），这是一种合理的模式——只需使用 `LED_BUILTIN` 或外接一个空闲数字引脚上的 LED，并在检测到传入串口字节（`Serial.available()`）时触发，而不是试图利用 TX/RX 硬件 LED。