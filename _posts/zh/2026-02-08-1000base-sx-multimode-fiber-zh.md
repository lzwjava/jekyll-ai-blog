---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-haiku
title: 1000Base-SX 使用多模光纤
translated: true
type: note
---

感谢分享这个问题。让我解释一下为什么正确答案是 **C (Multi-mode Fiber)** 而不是 B。

## Understanding 1000Base-SX Standard

**1000Base-SX** 的组成部分：

- **1000** = 1 Gigabit/s (每秒 10 亿比特)
- **Base** = Baseband 传输
- **SX** = Short wavelength (短波长)

## Key Difference: SX vs LX

1000Base Ethernet 主要有两种光纤版本：

**1000Base-SX (Short Wavelength)**

- Wavelength: 850 nm
- Transmission medium: **Multi-mode Fiber**
- Maximum distance: 275m (Full-duplex) 或 550m (Half-duplex)
- 成本较低，适用于短距离应用

**1000Base-LX (Long Wavelength)**

- Wavelength: 1310 nm
- Transmission medium: **Single-mode Fiber**
- Maximum distance: 5 km
- 成本较高，适用于长距离应用

## Why Does SX Use Multi-mode Fiber?

短波长激光 (850 nm) 的特性决定了其与 Multi-mode Fiber 的兼容性：

- 在 850 nm 处，Multi-mode Fiber 的 Modal dispersion 相对较小
- 更具性价比且功耗更低
- 非常适合园区网络和 Data centers 的中短距离传输

Single-mode Fiber 针对长波长 (1310 nm) 进行了优化，能够支持更远的传输距离。

**记忆口诀：SX = Short wavelength = Multi-mode fiber；LX = Long wavelength = Single-mode fiber**
