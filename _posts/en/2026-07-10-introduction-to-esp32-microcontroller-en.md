---
audio: false
generated: true
image: false
lang: en
layout: post
title: Introduction to ESP32 Microcontroller
translated: false
type: note
---

Question: What is ESP32?

Answer:

![Image](https://images.openai.com/static-rsc-4/T_CVar7hogccqhjIw7dOKBmrDxKOqfJQryMFF0ClRKfaNiODaV5M6k7ydJtchAnvARQn5PxlTseiTSXQLSy9Fwal2UL05GccQ9TU0oL1lp2d6moUKfqAI8gB5irhCfuVWbnejVI47JQ00d4L-dZqE84-qT7OEPN8jcNRAz3F_dpYKYJN0To9E5m_nr87fXe7?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/irAVSQIKbK53TdEmdi33e3F0D0W2sjpF8YVb9igZJMW060iugLQjMXez4Fw_0gTbp_VbxKLqC3DJlxCQRSM-3rO0v0ZE3_ouhIDfry0bSJG-euib_Z1w7QFhM1Oqrq7DRYs0-ZlklusGaVACaqabEm0mMWRRoQ30WKV4tH7V_QoywddLwzAsrKyZdacK2Y73?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/qr5BNyOojpv0uc6Zn_Ma2xLalQMwHbLW6gWa72ZPcSkwpgSexl4gIUchbLT5A7unK8fspQ22KFB8pjDeAz7x_-cByHSccZS08gB8Wy8hN-IP0knMZrpEY1SP55IqZV03BigybcmYLBnmT8Gi8D2DmWI5kpoitWS2yX2knNsX-OJE8HN-2g3EGe1py5K5KBtj?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/9zvFKtSm8nnoZ9TPTu3gPg-CCp7sc09ygY9DplXSrCRWA3edQak0LuayWo5ltMnKRAwa5p2gT7_XMZgSOx8Uy6fLf5J-dM2k1T3f4MPXkWc1HKTHuMhebfBYq6zCSD_KfOVhw9hqTsKG9wN-x53t7FMXFU85a_5oYTXQT4mH2GmTvos54fjq2YblU5WcQyIQ?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/00_34_jyYeXc9tuMoBFaWhug_fOf5PmtiGgdvuSj-oYyzuv4yRltQyzVRxXrN9-4u5P1cXaO2Z4aw38iMi-pczWkClDHdqhMygqHrtxrJVSYzNsUb_3g1-mXXofjfnUE-OpYK-ZP5h92K9v3LQUasx5OQqCOqkcZvWOByt76VKQYXUclrB-kIQDpkdwiwvhN?purpose=fullsize)

The **ESP32** is a low-cost, low-power **microcontroller SoC (System-on-Chip)** made by Espressif Systems. It is one of the most popular chips for:

* IoT (Internet of Things)
* Robotics
* Smart home devices
* Sensor data collection
* Wearables
* Embedded AI
* Home automation

Think of it as a tiny computer designed to interact with the physical world.

### Architecture

A typical ESP32 contains:

```text
                 ESP32 SoC
        +-------------------------+
        |  Dual-core Xtensa CPU   | 160-240 MHz
        |  520 KB SRAM            |
        |  Wi-Fi                  |
        |  Bluetooth (BLE)        |
        |  GPIO pins              |
        |  ADC / DAC              |
        |  SPI / I2C / UART       |
        |  PWM timers             |
        |  RTC                    |
        +-------------------------+
```

Unlike a Raspberry Pi, it **doesn't run Linux**. Your program runs directly on the hardware (bare metal with an RTOS such as FreeRTOS).

### Why everyone uses it

For around **$3–10**, you get:

* Wi-Fi
* Bluetooth
* Plenty of GPIO pins
* Low power consumption
* Good documentation
* Huge community
* Easy programming

That combination is why it's become a standard choice for hobbyists and many commercial IoT products.

### Programming

You can program it with:

* C/C++ (official ESP-IDF)
* Arduino framework
* MicroPython
* Rust
* Zig
* Lua

Example (Arduino):

```cpp
void setup() {
    Serial.begin(115200);
}

void loop() {
    Serial.println("Hello ESP32");
    delay(1000);
}
```

### Hardware connections

Example wiring:

```text
ESP32
│
├── Temperature sensor
├── OLED display
├── Camera
├── Servo motor
├── LEDs
├── Buttons
├── Relay
└── Wi-Fi Router
```

It can both **sense** the environment (temperature, light, motion, GPS, etc.) and **control** actuators (motors, relays, LEDs).

### AI use cases

Given your interest in AI agents and robotics, the ESP32 is often used as the "edge controller" while a larger model runs elsewhere.

For example:

```text
          Cloud LLM
               ▲
               │ HTTP/WebSocket
               │
          Raspberry Pi
               ▲
               │ UART
               │
             ESP32
         ┌─────┴─────┐
     Camera       Motors
     Sensors      LEDs
```

Or with a small local model:

```text
ESP32
   │
Microphone
   │
Wake-word detection
   │
Wi-Fi
   │
LLM Server (vLLM / SGLang)
```

The ESP32 handles real-time hardware tasks while the GPU server performs the heavy AI inference.

### ESP32 vs Raspberry Pi

| Feature          | ESP32                                                       | Raspberry Pi               |
| ---------------- | ----------------------------------------------------------- | -------------------------- |
| CPU              | 160–240 MHz MCU                                             | Multi-core ARM CPU         |
| RAM              | ~520 KB SRAM (plus optional external PSRAM on some modules) | 1–16 GB                    |
| Operating System | No Linux (typically FreeRTOS)                               | Linux                      |
| Wi-Fi            | Yes                                                         | Most models                |
| GPIO             | Yes                                                         | Yes                        |
| Power            | Very low                                                    | Higher                     |
| Price            | ~$3–10                                                      | ~$35+                      |
| Best for         | Embedded control, sensors                                   | AI, servers, desktop Linux |

### Popular ESP32 variants

* **ESP32-WROOM-32** — the classic module used on many development boards.
* **ESP32-S3** — adds vector instructions and USB; well suited for TinyML, cameras, and voice applications.
* **ESP32-C3** — single-core, based on the RISC-V architecture, with Wi-Fi and BLE.
* **ESP32-C6** — adds Wi-Fi 6 and support for Thread and Zigbee.

If you're planning to build **AI-powered robots or hardware agents**, the **ESP32-S3** is currently one of the most popular choices because it combines USB support, camera compatibility, and better AI-oriented capabilities than the original ESP32.

References:

* [Espressif Systems official website](https://www.espressif.com/?utm_source=chatgpt.com)
* [ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/?utm_source=chatgpt.com)
