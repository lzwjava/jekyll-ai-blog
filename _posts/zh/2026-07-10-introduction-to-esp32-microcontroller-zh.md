---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ESP32微控制器简介
translated: true
type: note
---

**问题：什么是ESP32？**

**答案：**

![Image](https://images.openai.com/static-rsc-4/T_CVar7hogccqhjIw7dOKBmrDxKOqfJQryMFF0ClRKfaNiODaV5M6k7ydJtchAnvARQn5PxlTseiTSXQLSy9Fwal2UL05GccQ9TU0oL1lp2d6moUKfqAI8gB5irhCfuVWbnejVI47JQ00d4L-dZqE84-qT7OEPN8jcNRAz3F_dpYKYJN0To9E5m_nr87fXe7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/irAVSQIKbK53TdEmdi33e3F0D0W2sjpF8YVb9igZJMW060iugLQjMXez4Fw_0gTbp_VbxKLqC3DJlxCQRSM-3rO0v0ZE3_ouhIDfry0bSJG-euib_Z1w7QFhM1Oqrq7DRYs0-ZlklusGaVACaqabEm0mMWRRoQ30WKV4tH7V_QoywddLwzAsrKyZdacK2Y73?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/qr5BNyOojpv0uc6Zn_Ma2xLalQMwHbLW6gWa72ZPcSkwpgSexl4gIUchbLT5A7unK8fspQ22KFB8pjDeAz7x_-cByHSccZS08gB8Wy8hN-IP0knMZrpEY1SP55IqZV03BigybcmYLBnmT8Gi8D2DmWI5kpoitWS2yX2knNsX-OJE8HN-2g3EGe1py5K5KBtj?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/9zvFKtSm8nnoZ9TPTu3gPg-CCp7sc09ygY9DplXSrCRWA3edQak0LuayWo5ltMnKRAwa5p2gT7_XMZgSOx8Uy6fLf5J-dM2k1T3f4MPXkWc1HKTHuMhebfBYq6zCSD_KfOVhw9hqTsKG9wN-x53t7FMXFU85a_5oYTXQT4mH2GmTvos54fjq2YblU5WcQyIQ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/00_34_jyYeXc9tuMoBFaWhug_fOf5PmtiGgdvuSj-oYyzuv4yRltQyzVRxXrN9-4u5P1cXaO2Z4aw38iMi-pczWkClDHdqhMygqHrtxrJVSYzNsUb_3g1-mXXofjfnUE-OpYK-ZP5h92K9v3LQUasx5OQqCOqkcZvWOByt76VKQYXUclrB-kIQDpkdwiwvhN?purpose=fullsize)

**ESP32** 是由乐鑫科技（Espressif Systems）制造的一款低成本、低功耗的**微控制器SoC（片上系统）**。它是以下领域最流行的芯片之一：

* IoT（物联网）
* 机器人技术
* 智能家居设备
* 传感器数据采集
* 可穿戴设备
* 嵌入式AI
* 家庭自动化

可以把它看作一台用于与物理世界交互的微型计算机。

### 架构

典型的 ESP32 包含：

```text
                 ESP32 SoC
        +-------------------------+
        |  双核 Xtensa CPU        | 160-240 MHz
        |  520 KB SRAM            |
        |  Wi-Fi                  |
        |  蓝牙（BLE）            |
        |  GPIO 引脚              |
        |  ADC / DAC              |
        |  SPI / I2C / UART       |
        |  PWM 定时器             |
        |  RTC                    |
        +-------------------------+
```

与 Raspberry Pi 不同，它**不运行 Linux**。你的程序直接在硬件上运行（裸机，配有 FreeRTOS 等 RTOS）。

### 为什么人人都用它

只需大约 **3–10 美元**，你就能获得：

* Wi-Fi
* 蓝牙
* 丰富的 GPIO 引脚
* 低功耗
* 良好的文档
* 庞大的社区
* 易于编程

正是这种组合使它成为爱好者以及许多商用 IoT 产品的标准选择。

### 编程方式

你可以使用以下语言进行编程：

* C/C++（官方 ESP-IDF）
* Arduino 框架
* MicroPython
* Rust
* Zig
* Lua

示例（Arduino）：

```cpp
void setup() {
    Serial.begin(115200);
}

void loop() {
    Serial.println("Hello ESP32");
    delay(1000);
}
```

### 硬件连接

示例接线：

```text
ESP32
│
├── 温度传感器
├── OLED 显示屏
├── 摄像头
├── 舵机
├── LED
├── 按钮
├── 继电器
└── Wi-Fi 路由器
```

它既能**感知**环境（温度、光线、运动、GPS 等），也能**控制**执行器（电机、继电器、LED）。

### AI 应用场景

鉴于你对 AI 智能体与机器人技术的兴趣，ESP32 常被用作“边缘控制器”，而更大的模型在其他地方运行。

例如：

```text
          云端 LLM
               ▲
               │ HTTP/WebSocket
               │
          Raspberry Pi
               ▲
               │ UART
               │
             ESP32
         ┌─────┴─────┐
     摄像头         电机
     传感器         LED
```

或者配合本地小模型：

```text
ESP32
   │
麦克风
   │
唤醒词检测
   │
Wi-Fi
   │
LLM 服务器（vLLM / SGLang）
```

ESP32 负责实时硬件任务，GPU 服务器则执行繁重的 AI 推理。

### ESP32 与 Raspberry Pi 对比

| 特性              | ESP32                                                       | Raspberry Pi               |
| ----------------- | ----------------------------------------------------------- | -------------------------- |
| CPU               | 160–240 MHz 微控制器                                        | 多核 ARM CPU               |
| RAM               | ~520 KB SRAM（部分模组可选外部 PSRAM）                      | 1–16 GB                    |
| 操作系统          | 无 Linux（通常为 FreeRTOS）                                 | Linux                      |
| Wi-Fi             | 是                                                          | 大部分型号                 |
| GPIO              | 是                                                          | 是                         |
| 功耗              | 很低                                                        | 较高                       |
| 价格              | ~3–10 美元                                                  | ~35 美元以上               |
| 最佳用途          | 嵌入式控制、传感器                                          | AI、服务器、桌面 Linux     |

### 常见 ESP32 型号

* **ESP32-WROOM-32** — 经典模组，广泛用于开发板。
* **ESP32-S3** — 新增向量指令和 USB，适合 TinyML、摄像头和语音应用。
* **ESP32-C3** — 单核，基于 RISC-V 架构，支持 Wi-Fi 和 BLE。
* **ESP32-C6** — 新增 Wi-Fi 6 以及对 Thread 和 Zigbee 的支持。

如果你计划构建**AI 驱动的机器人或硬件智能体**，**ESP32-S3** 目前是最受欢迎的选择之一，因为它结合了 USB 支持、摄像头兼容性以及比原始 ESP32 更强的 AI 能力。

参考资料：

* [乐鑫科技官方网站](https://www.espressif.com/?utm_source=chatgpt.com)
* [ESP-IDF 编程指南](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/?utm_source=chatgpt.com)