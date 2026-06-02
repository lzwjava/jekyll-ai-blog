---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 共射极放大器分析
translated: true
type: note
---

### 集电极电流 \\( I_C \\)

对于发射极接地的共射极BJT放大器，其输入电阻 \\( R_{in} \\) 约等于小信号基极电阻 \\( r_\pi = \frac{\beta V_T}{I_C} \\)，其中 \\( V_T = 0.026 \\) V（室温下的热电压），\\( \beta = 100 \\)。

已知 \\( R_{in} = 1 \\) k\\( \Omega = 1000 \\) \\( \Omega \\)，

\\[
r_\pi = \frac{100 \times 0.026}{I_C} = 1000
\\]

\\[
\frac{2.6}{I_C} = 1000
\\]

\\[
I_C = \frac{2.6}{1000} = 0.0026 \text{ A} = 2.6 \text{ mA}
\\]

该偏置点对应的集电极-发射极电压 \\( V_{CE} = V_{CC} - I_C R_C = 12 - (0.0026 \times 2200) \approx 12 - 5.72 = 6.28 \\) V，接近电源电压中点，可保持较好的线性度。

### 电压增益 \\( A_V \\)

共射极放大器（无发射极电阻）的小信号电压增益为 \\( A_V = -g_m R_C \\)，其中跨导 \\( g_m = \frac{I_C}{V_T} \\)。

\\[
g_m = \frac{0.0026}{0.026} = 0.1 \text{ A/V（或S）}
\\]

\\[
A_V = - (0.1 \times 2200) = -220
\\]

负号表示相位反转。
