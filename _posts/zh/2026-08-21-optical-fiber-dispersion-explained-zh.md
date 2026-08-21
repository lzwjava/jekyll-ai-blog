---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 光纤色散解析
translated: true
type: note
---

问题：在光纤的语境中，“dispersion（色散）”是什么意思？

答案：

色散是指光信号在光纤中传输时随时间的**展宽**，导致接收端信号失真或减弱。

**简单类比：**
想象一下同时让一群跑步者出发——他们一起起跑，但由于速度稍有不同，到达时间不同。最终，队伍被“拉散”。在光纤中，光脉冲也有类似现象——它们展宽并开始**重叠**，使得区分单个比特（0 和 1）变得困难。

**主要色散类型：**

| 类型 | 原因 | 发生场景 |
| --- | --- | --- |
| **模态色散** | 不同光模式走不同路径 | 多模光纤 |
| **色度色散** | 不同波长以不同速度传输 | 两者均有，多模更严重 |
| **偏振模色散（PMD）** | 光偏振态变化 | 单模光纤，长距离 |

**为什么重要：**

- 色散越大，信号劣化越严重
- 限制**距离和带宽**——光纤越长，情况越糟
- 这是**多模光纤比单模光纤传输距离短**的主要原因

**实际表现：**

- 一端发送的清晰脉冲 ▐█▌ 可能在另一端变成模糊的波形 ∿
- 当色散足够大时，比特互相模糊 → **数据错误**

参考文献：

- [Dispersion in Optical Fiber – RP Photonics](https://www.rp-photonics.com/dispersion.html)
- [Modal Dispersion – Fiber Optic Association](https://www.thefoa.org/tech/ref/fiber/dispersion.html)
