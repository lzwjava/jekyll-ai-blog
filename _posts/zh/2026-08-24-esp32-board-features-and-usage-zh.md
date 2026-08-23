---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ESP32开发板：特性与用法
translated: true
type: note
---

问题：什么是ESP32板？如何使用它？

答案：

**ESP32** 是由 **Espressif Systems** 开发的一款低成本、低功耗的微控制器（MCU）。由于其内置的 Wi-Fi 和蓝牙功能，它在物联网（IoT）项目中得到了广泛应用。

---

**主要特性**

- 双核 32 位处理器（最高 240 MHz）
- 内置 Wi-Fi（802.11 b/g/n）和蓝牙（经典 + BLE）
- 多个 GPIO 引脚（数字 I/O、PWM、ADC、DAC、I2C、SPI、UART）
- 低功耗，支持深度睡眠模式
- 4MB+ 闪存（因板型而异）
- 3.3V 逻辑电平

---

**常见 ESP32 开发板型号**

| 板型 | 说明 |
|---|---|
| ESP32 DevKit V1 | 最常见的入门板 |
| ESP32-S3 | 增强的 AI/USB 支持 |
| ESP32-C3 | RISC-V 内核，经济实惠 |
| ESP32-CAM | 板载摄像头模块 |

---

**如何使用**

1. **安装 Arduino IDE** 或 **VS Code + PlatformIO**
2. **添加 ESP32 板支持** — 在 Arduino IDE 中，进入 *偏好设置 → 附加开发板管理器网址*，添加 Espressif 的 URL
3. **通过 USB 连接** — 开发板会显示为一个 COM/串口
4. **编写代码**（C/C++ 或 MicroPython）
5. **上传** — 如果烧录时遇到问题，可按住 BOOT 按钮

**基础闪烁示例（Arduino）：**
```cpp
void setup() {
  pinMode(2, OUTPUT); // 板载 LED 在 GPIO 2
}

void loop() {
  digitalWrite(2, HIGH);
  delay(1000);
  digitalWrite(2, LOW);
  delay(1000);
}
```

---

**常见用途**

- Wi-Fi/蓝牙传感器节点
- 智能家居自动化
- 在芯片上运行的 Web 服务器
- 电机控制器与机器人
- MQTT IoT 客户端

---

参考资料：
- [ESP32 概述 – Espressif Systems](https://www.espressif.com/en/products/socs/esp32)
- [ESP32 入门 – Random Nerd Tutorials](https://randomnerdtutorials.com/getting-started-with-esp32/)
- [ESP32 Arduino 核心 – GitHub](https://github.com/espressif/arduino-esp32)