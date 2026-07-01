---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-haiku
title: FDM核心原理详解
translated: true
type: note
---

## Question Content

本题考查 **Frequency Division Multiplexing (FDM)** 的概念。

## Key Information Extraction

题干中的核心要素：

- **在频域内**将信道带宽划分
- 划分为**多个子信道**
- 将信号调制在**各子信道的载波信号上**
- 在一条信道上**同时传输多路信号**

## Comparison of All Options

| 选项 | 名称 | 工作域 | 特点 |
| -------- | ------ | ----------------- | ----------------- |
| **A** | **Frequency Division Multiplexing (FDM)** | **频域 (Frequency Domain)** | **将频率划分为多个子频带，每路信号占用不同频率** |
| B | Time Division Multiplexing (TDM) | 时域 (Time Domain) | 将时间划分为多个时隙，每路信号占用不同时间 |
| C | Wavelength Division Multiplexing (WDM) | 光域 (Optical Domain) | 基于光纤传输，不同波长的光信号 |
| D | Code Division Multiplexing (CDM) | 码域 (Code Domain) | 使用不同的编码序列来区分信号 |

## Analysis of Your Answer

你选择了 **C (Wavelength Division Multiplexing)**，这是错误的。

**原因：**

- WDM 主要应用于 **Fiber Optic Communication** 系统。
- 题目明确指出“**在频域内**划分”，这直接指向了 Frequency Division Multiplexing。
- WDM 本质上是 FDM 在光域的应用，但题目问的是通用的信道复用技术。

## Correct Answer

**✓ A Frequency Division Multiplexing (FDM)**

**解析：**
题干完全描述了 FDM 的工作原理：在频域划分带宽 → 多个子信道 → 用不同载波调制 → 同时传输多路信号。

---

**Learning Tip：** 区分四种复用技术的工作域（频域、时域、码域、光域）是解决此类问题的关键。
