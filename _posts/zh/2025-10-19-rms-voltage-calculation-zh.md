---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 理解RMS电压计算
translated: true
type: note
---

### 说明

均方根（RMS）电压 \\( V_{RMS} \\) 代表交流电压的有效值，其在阻性负载上产生的功率耗散与同等大小的直流（DC）电压相同。对于正弦波形 \\( v(t) = V_{max} \sin(\omega t) \\)，其中 \\( V_{max} \\) 为峰值（最大）电压，RMS值的推导过程如下：

1. **均方值**：瞬时电压在一个周期 \\( T \\) 内的平方为 \\( v^2(t) = V_{max}^2 \sin^2(\omega t) \\)。\\( \sin^2(\omega t) \\) 在一个周期内的平均值为 \\( \frac{1}{2} \\)，因此均方电压为 \\( \frac{V_{max}^2}{2} \\)。

2. **RMS计算**：取均方值的平方根：
   \\[
   V_{RMS} = \sqrt{\frac{V_{max}^2}{2}} = \frac{V_{max}}{\sqrt{2}}
   \\]

3. **数值近似**：由于 \\( \sqrt{2} \approx 1.414 \\)，因此 \\( \frac{1}{\sqrt{2}} \approx 0.707 \\)。故 \\( V_{RMS} \approx 0.707 \times V_{max} \\)。

由此可确认选项 **B** 正确。其余选项错误原因如下：
- A 高估了结果（忽略了平均值计算）
- C 颠倒了系数（应为 \\( V_{max} = \sqrt{2} \times V_{RMS} \\)）
- D 低估了结果（那是全波整流正弦波的平均值，而非RMS值）
