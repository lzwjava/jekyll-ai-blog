---
audio: false
generated: true
image: false
lang: en
layout: post
title: "ESP32 Board: Features and Usage"
translated: false
type: note
---

Question: What is the ESP32 board and how do you use it?

Answer:

The **ESP32** is a low-cost, low-power microcontroller (MCU) developed by **Espressif Systems**. It's widely used in IoT (Internet of Things) projects due to its built-in Wi-Fi and Bluetooth capabilities.

---

**Key Features**

- Dual-core 32-bit processor (up to 240 MHz)
- Built-in Wi-Fi (802.11 b/g/n) and Bluetooth (Classic + BLE)
- Multiple GPIO pins (digital I/O, PWM, ADC, DAC, I2C, SPI, UART)
- Low power consumption with deep sleep modes
- 4MB+ Flash memory (varies by board)
- 3.3V logic level

---

**Common ESP32 Board Variants**

| Board | Notes |
|---|---|
| ESP32 DevKit V1 | Most common starter board |
| ESP32-S3 | Enhanced AI/USB support |
| ESP32-C3 | RISC-V core, budget-friendly |
| ESP32-CAM | Has onboard camera module |

---

**How to Use It**

1. **Install Arduino IDE** or **VS Code + PlatformIO**
2. **Add ESP32 board support** — in Arduino IDE, go to *Preferences → Board Manager URL* and add Espressif's URL
3. **Connect via USB** — the board appears as a COM/Serial port
4. **Write your code** (C/C++ or MicroPython)
5. **Upload** — hold the BOOT button if needed during flashing

**Basic Blink Example (Arduino):**
```cpp
void setup() {
  pinMode(2, OUTPUT); // Built-in LED on GPIO 2
}

void loop() {
  digitalWrite(2, HIGH);
  delay(1000);
  digitalWrite(2, LOW);
  delay(1000);
}
```

---

**Common Use Cases**

- Wi-Fi/Bluetooth sensor nodes
- Smart home automation
- Web servers running on the chip
- Motor controllers & robotics
- MQTT IoT clients

---

References:
- [ESP32 Overview – Espressif Systems](https://www.espressif.com/en/products/socs/esp32)
- [ESP32 Getting Started – Random Nerd Tutorials](https://randomnerdtutorials.com/getting-started-with-esp32/)
- [ESP32 Arduino Core – GitHub](https://github.com/espressif/arduino-esp32)
