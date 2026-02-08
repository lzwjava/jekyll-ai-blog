---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-haiku
title: 光纤信号传播详解
translated: true
type: note
---

光纤中的 **Dispersion**（色散）是指光信号在通过光纤传输时发生的**信号展宽**现象，这会导致信号失真和变弱。

可以这样理解：当你通过光纤发送一个光脉冲时，该光信号的不同成分以略微不同的速度传播。当信号到达另一端时，曾经清晰锐利的脉冲变得拉伸且模糊——就像看着墨水在水中扩散一样。

**主要有两种类型：**

**Chromatic Dispersion**（色散）- 不同波长（颜色）的光在光纤中以不同的速度传播。包含多个波长的脉冲会因为每个波长到达时间略有不同而发生展宽。

**Modal Dispersion**（模式色散）- 在 Multi-mode fiber（如 1000Base-SX 所使用的）中，光可以通过光纤内的多条路径传播。每条路径的传播距离略有不同，因此以不同 Mode 传输的光会在不同时间到达，导致信号展宽。

**为什么它对 1000Base-SX 很重要：**

275m 的 Full-duplex 限制部分原因就是由于 Dispersion。在更长的距离上，信号扩展非常严重，以至于：
- 脉冲彼此重叠
- 接收端无法清晰区分 1 和 0
- Bit errors（误码率）增加

Multi-mode fiber 的 Dispersion 情况比 Single-mode fiber 更严重，这就是为什么 1000Base-SX 的传输距离（275m）远短于 1000Base-LX 等 Single-mode 替代方案（可达 10km）的原因。