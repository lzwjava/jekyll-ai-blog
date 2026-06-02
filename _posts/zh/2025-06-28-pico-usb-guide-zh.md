---
audio: false
generated: true
lang: zh
layout: post
title: Ubuntu系统下树莓派Pico USB连接线指南
translated: true
type: note
---

为您的**Raspberry Pi Pico（带排针版）**——来自**Raspberry Pi Foundation**（假设“duistou”是拼写错误或经销商品牌），您需要合适的USB线缆在Ubuntu系统上进行配置。以下是所需信息：

### USB线缆要求
1. **接口类型**：USB转Micro-USB线缆
   - 树莓派Pico（原装带排针版）使用**Micro-USB**接口进行供电和数据传输
   - 确保线缆支持**数据传输**而非仅支持充电。某些廉价Micro-USB线缆仅支持供电，无法用于编程或通信

2. **线缆规格**：
   - **接口**：USB-A（或根据电脑接口选择USB-C）转Micro-USB
   - **质量**：使用高质量线缆避免连接问题，推荐知名品牌（如Anker、Belkin或手机/平板原装线缆）
   - **长度**：建议使用1-3英尺（30-100厘米）线缆以减少信号衰减

3. **电脑接口**：
   - 若Ubuntu设备配备**USB-A接口**，使用USB-A转Micro-USB线缆
   - 若仅有**USB-C接口**，需使用USB-C转Micro-USB线缆，或通过USB-C扩展坞配合USB-A转Micro-USB线缆

### 设置注意事项
- **连接方式**：将Micro-USB端插入Pico，另一端连接Ubuntu电脑
- **工作模式**：
  - **常规模式**：直接连接即可进行编程（如MicroPython、C/C++）
  - **BOOTSEL模式**：插入时按住**BOOTSEL**键进入大容量存储模式，用于固件更新（将显示为名为`RPI-RP2`的驱动器）
- **验证连接**：连接后可通过我先前回复的步骤验证Ubuntu是否识别Pico（如`lsusb`、`ls /dev/tty*`或`lsblk`命令）

### 线缆问题排查
- 若未检测到Pico（无`/dev/ttyACM0`设备或`RPI-RP2`驱动器），请更换线缆或USB接口
- 避免使用USB集线器，可能引发设备识别问题
- 通过连接其他设备（如手机）测试线缆是否支持数据传输

若对线缆选择仍有疑问或遇到问题，请描述您的配置详情（如电脑接口类型、线缆型号、连接时的设备反应），我将进一步为您提供指导！
