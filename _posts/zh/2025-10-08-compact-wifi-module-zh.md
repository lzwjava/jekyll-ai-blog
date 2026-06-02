---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 物联网紧凑型WiFi模块
translated: true
type: note
---

ESP-01S是一款基于乐鑫科技ESP8266微控制器芯片的紧凑型WiFi模块。作为原始ESP-01的升级版本，它主要面向物联网应用场景，可为Arduino或树莓派等其他微控制器增添无线连接功能。

### 核心特性：
- **WiFi能力**：支持802.11 b/g/n标准，可独立作为WiFi接入点、站点或双重模式运行。内置TCP/IP协议栈便于网络集成。
- **处理器与内存**：搭载Tensilica L106 32位RISC处理器，主频80MHz（可超频至160MHz）。配备1MB（部分变体为4MB）SPI闪存用于代码与数据存储。
- **I/O引脚**：采用8引脚布局（VCC、GND、CH_PD、RST、TX、RX、GPIO0、GPIO2），支持串行通信（UART）及基础GPIO控制（如控制LED或继电器）。
- **功耗与尺寸**：工作电压3.3V（不兼容5V），传输功耗约80mA，尺寸仅24.75×14.5毫米，非常适合小型项目。
- **相比ESP-01的改进**：优化PCB布局提升WiFi信号强度，闪存容量提升至1MB（原512KB），GPIO2状态指示灯改为蓝色（原TX引脚指示灯）。

### 典型应用场景：
- 将传感器或设备接入互联网实现远程监控/控制
- 通过Arduino IDE（需安装ESP8266开发板支持）或串行AT命令进行编程
- 智能家居设备原型开发（如WiFi开关、气象站）

使用时需配备USB转串口适配器（如FTDI）烧录固件，因模块本身未集成USB接口。该模块价格低廉（5美元以内）且易于获取，但需注意避免引脚损坏。

[ESP-01S模块使用指南](https://www.taydaelectronics.com/datasheets/files/ESP-01S.pdf)
[ESP8266 ESP-01入门教程](https://www.instructables.com/Getting-Started-With-the-ESP8266-ESP-01/)
[ESP-01S模块详解](https://lonelybinary.com/en-us/blogs/learn/what-is-esp-01s)
[ESP-01S/ESP01S ESP8266模块](https://hobbycomponents.com/esp8266/1176-esp-01s-esp01s-esp8266-module)
