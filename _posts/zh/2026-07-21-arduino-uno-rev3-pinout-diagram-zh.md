---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Arduino UNO Rev3 引脚图
translated: true
type: note
---

问题：这是什么PDF？（[https://docs.arduino.cc/resources/pinouts/A000066-full-pinout.pdf](https://docs.arduino.cc/resources/pinouts/A000066-full-pinout.pdf)）

答案：

这是 **Arduino UNO Rev3（SKU A000066）完整引脚图**。它本质上是一个 **地图，展示了Arduino板上的每个引脚以及每个引脚内部连接了什么**。([Arduino Documentation][1])

![Image](https://images.openai.com/static-rsc-4/LWeyio-9Fb_NjWkei2BssmUiuoCgqPlsiDKeEB1nF5Jb7zg3tiatX_z6Z4WRvbw0aBMBoB7Xf2QMgIq4AvDgpi1hSvWgIcuIR1_PuM2A7T22Jj_fL5e07VaI4mJegDIb05NLygFT8tkvIq_GSKRvZcSX5MJIxQ9nQ_ycvB32oNlfIpTHkWJqcJ_AsH9t5KgD?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/U-KZVzBfa4XxhQ8LCZkhOuSZzW2UJuly651Gu6ZQ0IwwiIqSSfjNLi6be8igOQkFLm5gHVmvXKq1bSs8Td6yQC68yMXEHHiKTmm5iDCh8MrjqV9mWO6T3Sv8sIaRDU4N1NQ5nFvq8OBp9TtzWto5Rle_dSpsvkoQq5LT96j9Xc3jz3otfbDGaYRZ1ZVPjl0e?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/VhAPgmy9BwKrtPTgefnojVyqF_WdhkscPAv__2GDO2NbakygyXaQsNZC_IjGTU4fwOkUa4QPW5iTuiwIY911tfu_Bj1274zhm1WsNAzzbd6YaGUUNT4rLIJy5GkCrj8fr8rSMJ2OfuuByButH45ue9Lx1v2oaEBuWWOSY8oDKIlYYgr6TqJTPXC11oOVafnO?purpose=fullsize)

![Image](https://images.openai.com/static-rsc-4/yLgtOwt910YYWkN1evIc1ET-LVkXHX7QdybnptJ-xcjkKZHQE99lvctZkr8zzHOVBjQmAlOv_c4DMMFcPV3m9aY2_jLr2YRunzj9QEeHpEqJzNsbtUknnTA_FBc2Jg-ZQnobh3EJBjHaMXq82rSSJJ96OMdpeBW-B4a3J93ed-A1NTZqG69w4tSse3lPmBW1?purpose=fullsize)

可以把它想象成一个微型微控制器板的“主板手册”。

该板：

* MCU：**ATmega328P**
* 时钟：**16 MHz**
* 逻辑电压：**5V**
* 数字GPIO：**14个引脚（D0-D13）**
* 模拟输入：**6个引脚（A0-A5）**
* Flash：**32 KB**
* SRAM：**2 KB**
* EEPROM：**1 KB**
  ([Arduino Official Store][2])

---

## 引脚图的主要部分

### 1. 数字引脚（D0-D13）

这些是通用输入/输出引脚。

示例：

```
D13 ---- LED_BUILTIN
D12 ---- GPIO
D11 ---- PWM / SPI MOSI
D10 ---- PWM / SPI SS
D9  ---- PWM
D8  ---- GPIO
...
D0  ---- UART RX
D1  ---- UART TX
```

你可以这样写：

```cpp
pinMode(13, OUTPUT);

digitalWrite(13, HIGH);
```

来点亮板载LED。

---

### 2. 模拟引脚（A0-A5）

这些连接到ATmega328P内部的ADC。

示例：

```
传感器输出
      |
      v
     A0
      |
      v
10位ADC
      |
      v
0 ~ 1023 值
```

代码：

```cpp
int value = analogRead(A0);
```

如果电压是：

```
0V    -> 0
5V    -> 1023
```

---

### 3. 电源引脚

PDF显示了：

```
VIN
5V
3.3V
GND
RESET
IOREF
```

典型用法：

```
外部7-12V
       |
       v
      VIN

Arduino稳压器

       |
       +---- 5V 电源轨
```

---

### 4. 通信引脚

Arduino提供了几个硬件协议。

#### UART

```
D0 RX
D1 TX
```

用于串行通信：

```
Arduino <---- USB串行 ----> 电脑
```

---

#### SPI

引脚：

```
D10 SS
D11 MOSI
D12 MISO
D13 SCK
```

用于：

* SD卡
* 显示屏
* 高速传感器

示例：

```
Arduino
  |
 SPI
  |
SD卡
```

---

#### I2C

引脚：

```
A4 SDA
A5 SCL
```

用于：

* OLED显示屏
* IMU传感器
* RTC模块

示例：

```
Arduino

A4 SDA -------- 传感器 SDA
A5 SCL -------- 传感器 SCL
```

---

## 有趣的部分：Arduino引脚编号 vs MCU引脚

Arduino抽象层隐藏了实际的芯片引脚。

示例：

Arduino:

```
D13
```

实际上映射到：

```
ATmega328P PB5
```

PDF有助于转换：

```
Arduino 引脚
      |
      v
ATmega328P 寄存器
      |
      v
硬件端口
```

对于底层编程：

```c
PORTB |= (1 << PB5);
```

等同于：

```cpp
digitalWrite(13, HIGH);
```

但速度快得多。

---

## 为什么这个PDF很重要

对于初学者：

```
Arduino 引脚
      |
      v
连接 LED / 传感器 / 电机
```

对于嵌入式工程师：

```
Arduino 引脚
      |
      v
ATmega328P GPIO
      |
      v
AVR 寄存器
      |
      v
硬件外设
```

它相当于微控制器的 **GPU 框图或主板 PCIe 通道图**。

对于你的人工智能硬件背景，类比：

```
Arduino 引脚图 PDF
        ≈
NVIDIA GPU 架构图
        ≈
服务器主板框图
```

它告诉你物理资源映射。

---

参考文献：

* Arduino UNO R3 文档 ([Arduino Documentation][1])
* Arduino UNO Rev3 技术规格 ([Arduino Official Store][2])
* Arduino UNO R3 数据手册 ([Arduino Documentation][3])

[1]: https://docs.arduino.cc/hardware/uno-rev3/?utm_source=chatgpt.com "UNO R3 | Arduino Documentation"
[2]: https://store.arduino.cc/products/arduino-uno-rev3?utm_source=chatgpt.com "Arduino UNO Rev3 – Reliable ATmega328P Board with Digital & Analog I/O — Arduino Official Store"
[3]: https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf?hkey=EF798316E3902B6ED9A73243A3159BB0&utm_source=chatgpt.com "Arduino® UNO R3"
