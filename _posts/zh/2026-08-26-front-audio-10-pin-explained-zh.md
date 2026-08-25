---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 前音频10针接口详解
translated: true
type: note
---

**问题：** 主板上的前置音频（F_AUDIO）接口为什么有 10 个针脚？

**答案：**

前置音频接口采用 **10 针布局（严格来说是 9 针 + 1 个空位/防呆口）**，原因如下：

**信号需求（各针脚承载的功能）：**

| 针脚 | 功能 |
| ----- | ---------- |
| 1 | MIC2_L（麦克风左声道） |
| 2 | GND（接地） |
| 3 | MIC2_R（麦克风右声道） |
| 4 | −ACZ_DET（音频编解码器检测） |
| 5 | LINE2_R（耳机右声道） |
| 6 | FAUDIO_JD（插孔检测） |
| 7 | FAUDIO_GND（音频接地） |
| 8 | **KEY（物理阻塞——缺失针脚）** |
| 9 | LINE2_L（耳机左声道） |
| 10 | FAUDIO_JD（第二个插孔检测） |

**为什么是 10 针而不是更少？**

- 接口需要传输两路独立的音频信号——耳机输出和麦克风输入——以及各自对应的接地参考。
- 高清音频（HD Audio）还包括**插孔检测传感针脚**——这些额外的针脚用于告知系统何时有插头物理插入前置插孔，从而实现前后音频的自动切换。这是旧版 AC'97 标准（7 针）所不具备的功能。
- **第 8 针物理缺失（“防呆针”）**——其唯一作用是在插入排线时防止反向或错位，相当于一个防呆对准指南。

**简而言之：** 10 针设计（英特尔高清音频标准）容纳了立体声耳机输出 + 立体声麦克风输入 + 接地线 + 插孔检测信号，同时利用第 8 针作为物理防呆设计，防止错误插入。

**参考资料：**

- [AAFP 接口详解 — CGDirector](https://www.cgdirector.com/aafp-connector-on-motherboard/)
- [主板上的 AAFP 是什么 — SunbeamTech](https://sunbeamtech.com/hardware-guides/what-is-aafp-on-motherboard/)
- [前置面板接口完整引脚参考 — LCSC](https://www.lcsc.com/blog/front-panel-connectors-complete-pinout-reference-for-engineers-systems-builders/)