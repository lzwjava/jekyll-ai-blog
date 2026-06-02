---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 大语言模型作为创客必备副驾驶
translated: true
type: note
---

Question: 在现今进行任何新的或具有挑战性的项目（例如 Arduino、Raspberry Pi 或 Pico 项目以及构建机器人）时，是否真的需要一直开着笔记本电脑并运行 AI chatbots，因为 LLMs 已经成为我们处理即时问题和理解现状的“第二大脑”？

Answer:

是的，这非常精准地描述了 2025–2026 年的现状——特别是对于大多数爱好者、学生，甚至许多从事 embedded systems、robotics 或任何 hardware+software 项目的专业工程师而言。

### 为什么 LLMs 几乎成为了此类项目必备的“第二大脑”

1. 所需知识面极其广泛
   你需要同时理解：
   - 基础与高级 electronics
   - 多种 programming languages (MicroPython, CircuitPython, Arduino C++, Rust, C)
   - 不同 platform 下的 frameworks 和 libraries
   - 数十种 boards 之间的 pinout 差异
   - Communication protocols (I2C, SPI, UART, CAN, OneWire 等)
   - Sensor/actuator 的 datasheets 和特性
   - Power supply 规则、电流限制、电压等级
   - Debugging 奇怪的 hardware 行为
   现在已经没有任何人能把所有这些知识都留在快速访问记忆中了。

2. 实时“即时学习”优于预先学习
   当 servo 抖动、I2C 设备没有 ACK、NeoPixel 灯带显示颜色错误或 motor driver 发烫时，你希望在 **15–40 秒内**得到答案，而不是在阅读了三个论坛帖子和一份 datasheet 之后。
   现代 LLMs（尤其是具有最新知识的模型）通常能立即给出准确度达 80–90% 的首选方案。

3. 2026 年的典型 workflow 如下
   - Breadboard / PCB 摆在面前
   - Multimeter + oscilloscope（如果运气好的话）
   - Code editor 开启
   - **Large LLM 窗口始终可见**（通常有两个标签页：一个通用模型，一个专业或 long-context 模型）
   人们不断地在以下内容之间切换窗口或分屏：
   - “解释来自 picowgo / arduino-cli 的这个错误”
   - “为什么我的 MPU6050 在所有轴上都返回 32767？”
   - “给我一个安全的方法，用 Raspberry Pi Pico 驱动 4 个 A4988 steppers”
   - “将这个 Arduino sketch 转换为适用于 RP2040 的 MicroPython”

4. 仍然不需要它的边缘情况（但正变得越来越少）
   - 机械性地重复你已经构建过 20 多次的完全相同的项目
   - 遵循说明书极其完美的已测试 kit（例如官方的 Elegoo / SunFounder / Hiwonder 机器人套件）
   - 进行极低层级的 bare-metal 开发，其中每一个 datasheet 段落都至关重要，且你已经是该领域的专家

对于几乎所有人来说——尤其是当：

- 组合来自不同供应商的零件时
- 尝试新的 sensor/module 时
- 在不同平台之间进行 code 移植时
- Debugging 间歇性问题时
- 优化 power / interrupts / timing 时

→ 开启了 LLM 的笔记本电脑基本上在 95–100% 的项目活跃时间内都是打开的。

### 一句话总结

在 2026 年，对于 physical computing / robotics / maker hardware 项目，笔记本电脑 + 始终开启的 LLM chat 已成为基础设施——正如今天没有人会在不打开 Stack Overflow / GitHub / 官方文档标签页的情况下进行严肃的 software development 一样。LLM 只是将十个标签页折叠成了一个极快且具有交互性的标签页。

所以，是的——你描述的正是该领域大多数人的现状。

References:

- 无（这反映了 2025–2026 年 maker 社区、subreddits、Discord 服务器和 YouTube 评论区中广泛观察到的现实行为；无需单一引用来源）
