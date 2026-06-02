---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 语音 PCM 中的折叠二进制代码
translated: true
type: note
---

问题：在 PCM 系统中，3-bit natural binary 和 3-bit folded binary 编码规则如表 31 所示。填入位置 ①、②、③ 和 ④ 的值。列出 folded binary coding 的特点，并分析为什么 folded binary code 大多用于语音信号 PCM 系统。

答案：

## 第一部分：填入编码表

PCM 的标准 3-bit 编码表如下：

| Quantization Level | Signal Polarity | Natural Binary Code | Folded Binary Code |
|---|---|---|---|
| +3 | 正 | 111 | **① 111** |
| +2 | 正 | 110 | **② 101** |
| +1 | 正 | 101 | 110 |
| 0+ | 正 | 100 | 100 |
| 0− | 负 | 011 | 000 |
| −1 | 负 | 010 | **③ 001** |
| −2 | 负 | 001 | **④ 011** |
| −3 | 负 | 000 | 010 |

**答案：**

- ① = `111`
- ② = `101`
- ③ = `001`
- ④ = `011`

---

## 第二部分：Folded Binary Code 的特点

Folded binary code 使用最左边（最高有效位，MSB）作为 **sign/polarity bit**（1 = 正，0 = 负），其余位表示幅度。其关键特点是：

**1. MSB 是 polarity bit；码字围绕零镜像对称。**
码表围绕零电平“折叠”对称。如果将负码折叠叠加到正码上，它们会完美匹配——因此得名“folded binary”。

**2. 具有相同绝对值（但极性相反）的信号共享相同的幅度位。**
Folded binary code (FBC) 使用 MSB 作为 sign bit，然后用剩余位从原点向正负两个方向计数。距离原点等距的码字（除符号位外）相同。这意味着编码器可以对幅度相等的正负信号应用相同的量化过程。

**3. 小信号中的位错误影响更小。**
因为小信号编码靠近零边界（低幅度位），小信号码字中的单个位错误仅使解码值小幅度偏移——与大信号码字中的位错误相比，影响微小。

---

## 第三部分：为什么在语音 PCM 系统中使用 Folded Binary Code

这两个原因共同作用：

**原因 1：语音信号具有高概率的小幅度信号。**
在真实的电话和语音通信中，信号幅度大多数时间较低。大幅度变化（响亮声音）发生的频率远低于小幅度信号（安静语音、停顿和背景）。统计上，语音信号集中在零电平附近。

**原因 2：Folded binary code 最小化了对小信号的位错误影响。**
使用 folded binary code，零附近的相邻量化电平仅在幅度部分相差一位。因此，当传输错误（位翻转）发生在较低幅度位——这些位对应小信号——时，解码错误很小，对语音质量的感知退化最小。

**综合效果：** 由于语音信号主要为小幅度，且 folded binary code 最有效地保护小信号免受位错误影响，因此在语音 PCM 系统中使用 folded binary coding，在噪声信道条件下，与 natural binary coding 相比，显著 **改善感知音频质量**。

> 总之：folded binary code 被优选，因为它精确匹配语音的统计特性（大多小幅度）与错误鲁棒性，正好在最关键的地方——近零信号电平。

References:

- [PCM Folded Binary Code – SlideShare](https://www.slideshare.net/SubaShree87/pcmpart-1pptx)
- [Folded Binary Code (FBC) – UCSB ECE](https://courses.ece.ucsb.edu/ECE146/146B_S09Gibson/LogPCM.pdf)
- [Telecomms Principles – PCM](https://www.technologyuk.net/telecommunications/telecom-principles/pulse-code-modulation.shtml)
