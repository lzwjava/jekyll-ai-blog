---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Arduino Uno上的两个电源接口
translated: true
type: note
---

**问题：Arduino Uno 上有哪两个电源连接器？**

**答案：**

在 **Arduino Uno** 上，两个常见的电源连接器是：

1. **USB 连接器（通常为 USB-B）**
2. **DC 电源插孔（电池/电源适配器连接器）**

![Image](https://images.openai.com/static-rsc-4/fV9WOLEzti8jngCI4K0AHfglYuZ3vZHdI3EWlasth5hxJkqS3Le0WlKOuBq3DLH8-X9CHNNQ-n6xHsbEgFAJj1qs-d6Fzr7fcQ1h1IGAAVXK0wkTP4YYJvRW_pyrmJHq1keNYCClmYpBpjn6D8dccdjZir4FdZsb_YcsPJlYuXbjj1OymvBAfx3VyeQPVQST?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/UEgTUIPnUyTEGl54Ya7BvI5lgYOs9Qydtd5EmwMdlM-v5evHk0MjsmHapoL4qJsPlA5sV6KeWey7E1sF1OFCz-3vO4-PfXdu4dbQcd9W3XvPRyOV-48PSvFRK5KEzCcH_F3Ef7ehl7JY2e5VYvIefvWR0j0RTus7pxV1g14eqqPk3FYqF1iESqi9yHRkM69G?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/mSYnD211t5TDyoHlXw7FCybCnPsDtfokc7a7L3wO0-1CH0u_JARjJYZLSENrx_5IZ4Kc1Is97cJPn9VKruDHGoNbjUjgFTd0Q0Yaz4uqoVLklBsBuNg4VrQPVENtaDe5PwReISuxPAnK6YFpdl1LSfmpxgZSU8KADz6TGaxkXGfWRkNO0JRvhfatGgbD4v3h?purpose=fullsize)

### 1. DC 电源插孔——外部电源

DC 电源插孔可接受外部电源：

* 推荐：**7–12V DC**
* 中心为正极
* 经过电压稳压器
* 为 Arduino 板提供 **5V** 电压

示例：

```
9V 电池
    |
    v
[DC 电源插孔]
    |
[电压稳压器]
    |
+5V Arduino
```

你可以使用：

* 9V 墙式适配器
* 电池组
* 锂离子电池 + 稳压器

---

### 2. USB 连接器——编程 + 电源

USB 连接器完成两项工作：

#### A. 上传代码

你的电脑：

```
Arduino IDE
     |
 USB 线缆
     |
ATmega328P bootloader
     |
新固件
```

#### B. 提供电源

USB 提供：

```
USB 5V
 |
polyfuse
 |
Arduino 5V 电源轨
```

通常最大约 500mA（取决于 USB 端口）。

---

### Arduino 如何选择电源？

Uno 具有自动电源选择功能。

示例：

```
USB 已连接 + DC 插孔已连接

       9V 适配器
           |
           v
      电压稳压器
           |
           +---- 5V 电源轨
                    |
USB 5V ------------+
```

该板检测较高/合适的电源，并防止逆向馈电至 USB。

---

### 还有其他电源引脚

在排针附近：

```
电源排针

VIN  ---- 外部输入电压
GND
5V   ---- 稳压 5V 输出
3.3V ---- 3.3V 输出
RESET
IOREF
```

`VIN` 的电压基本上与 DC 插孔输入相同。

示例：

```
电池 + ---- VIN
电池 - ---- GND
```

无需使用电源插孔即可工作。

---

### 工程视角

Arduino Uno 是一个简单的嵌入式系统：

```
                 USB
                  |
                  v
PC -----> USB-UART chip -----> ATmega328P
                                  |
                                  |
                             GPIO / ADC / PWM
                                  |
                              传感器
                              电机


电池
  |
  v
电源稳压器
  |
  +---- 5V 逻辑电路
```

电源插孔的存在是因为嵌入式设备通常**在没有计算机的情况下**运行。在开发阶段你使用 USB；在部署后的设备中，你会移除计算机并使用电池/直流电源。

同样的模式随处可见：

* ESP32 开发板 → USB + 电池引脚
* Raspberry Pi → USB-C 电源
* GPU → PCIe 插槽 + 辅助电源连接器
* 服务器 → 冗余电源

这种分离是根本性的：**一个连接器用于开发/调试，另一个用于独立运行。**