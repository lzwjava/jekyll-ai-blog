---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MCU在Arduino UNO中的含义
translated: true
type: note
---

问题：在Arduino UNO原理图中，MCU代表什么？

答案：

**MCU = 微控制器单元**（也称**单片机**）。

在Arduino UNO的上下文中：

```
MCU
 |
 +-- CPU内核
 +-- 闪存
 +-- SRAM
 +-- EEPROM
 +-- GPIO引脚
 +-- 定时器
 +-- ADC
 +-- UART/SPI/I2C外设
```

它是一个**集成在单芯片上的完整微型计算机**，专为控制硬件而设计。

对于Arduino UNO：

```
                Arduino UNO

             +----------------+
             |   ATmega328P   |
             |                |
             |  MCU           |
             |                |
             |  CPU           |
             |  32KB闪存      |
             |  2KB SRAM      |
             |  GPIO           |
             |  ADC            |
             |  定时器         |
             +----------------+
                    |
        +-----------+-----------+
        |           |           |
      LED        传感器       电机
```

该芯片：

Microchip Technology的**ATmega328P**是Arduino UNO R3内部的MCU。

---

### MCU vs CPU vs SoC

一个有用的层级关系：

```
CPU
 |
 |-- 通用处理器
 |
 +-- 需要外部RAM、存储、外设


MCU
 |
 |-- CPU
 |-- RAM
 |-- 闪存
 |-- GPIO
 |-- 定时器
 |-- 通信接口
 |
 +-- 全部集成在单芯片中


SoC
 |
 |-- CPU
 |-- GPU/NPU
 |-- 内存控制器
 |-- 众多外设
 |
 +-- 更大的集成系统
```

示例：

| 芯片             | 类别              | 示例           |
| ---------------- | ----------------- | -------------- |
| Intel Core i9    | CPU               | PC             |
| NVIDIA H100      | GPU/加速器        | AI训练         |
| ATmega328P       | MCU               | Arduino        |
| ESP32            | MCU               | IoT设备        |
| Apple M系列      | SoC               | Mac            |

---

### 为什么叫"微控制器"？

因为其原始用途是：

> 一个用来控制机器的小型计算机。

示例：

温度控制器：

```
温度传感器
        |
        v
     MCU
        |
        v
 加热器继电器
```

代码：

```c
while (1) {
    temp = read_sensor();

    if (temp < 20) {
        turn_on_heater();
    } else {
        turn_off_heater();
    }
}
```

MCU永远运行这个循环。

---

### 在Arduino原理图中

当你看到：

```
U1
ATmega328P
```

那就是MCU。

板上的其余部分用于支持它：

```
USB连接器
     |
ATmega16U2
     |
UART
     |
ATmega328P  <-- MCU
     |
GPIO引脚
     |
你的电子设备
```

---

一个很好的思维模型：

* **RTX 4070** = 用于矩阵乘法的大型并行计算机
* **Arduino MCU** = 控制物理事物的微型常开大脑

AI机器人通常将两者结合：

```
                 机器人

摄像头
  |
  v
RTX GPU / AI计算机
  |
  | 决策
  v
MCU
  |
  | 实时控制
  v
电机 / 传感器
```

GPU负责思考；MCU负责接触真实世界。
