---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CH340 Arduino Nano克隆指南
translated: true
type: note
---

根据我的研究，以下是完整情况：

### 您的连接设备：CH340 USB转串口芯片（`1a86:7523`）

CH340芯片是一款**通用USB转串口转换器**，并非特定开发板原生USB接口。这意味着：

| 开发板 | 是否使用CH340？ | VID:PID |
| ------- | ------------- | --------- |
| **Arduino Nano（克隆版）** | ✅ **最常见** | `1a86:7523` |
| **Arduino Uno（克隆版）** | ⚠️ 有时使用 | `1a86:7523` |
| **Circuit Playground**（Adafruit） | ❌ 否 — 原生USB | `0x239A:0x8011` |
| **Arduino BT** | ❌ 否 — 蓝牙 | — |

**Circuit Playground** 和 **Arduino BT** 已被排除——它们的硬件完全不同（分别为ATmega32u4原生USB和蓝牙）。

### 您几乎肯定拥有的是：**Arduino Nano克隆版**（ATmega328P）

CH340正是廉价Arduino Nano克隆版的标志性特征。请选择：

> **开发板：`Arduino Nano`**
> **处理器：`ATmega328P`**

### 一个需要注意的问题——旧版与新版引导加载程序

近5年内售出的Nano克隆版使用**新版引导加载程序**（115200波特率）。但如果您的版本较旧或来自随机廉价批次，可能需要：

> **处理器：`ATmega328P（旧版引导加载程序）`**（57600波特率）

**请先尝试新版**（`ATmega328P`）。如果上传失败并出现超时/avrdude错误，请切换至`ATmega328P（旧版引导加载程序）`。

### 如果它实际上是Uno

如果开发板物理尺寸较大，且USB接口和电源插孔位于同一端，则它是**Arduino Uno**——请选择`Arduino UNO`。但CH340在Uno上较少见（大多数使用原装FTDI或16U2芯片）。
