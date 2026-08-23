---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'FNIRSI DSO-153: 30美元示波器评测'
translated: true
type: note
---

**问题：** FNIRSI 二合一迷你数字示波器+信号发生器，带宽1MHz，售价仅为219元人民币（约30美元），它的表现如何？

---

**回答：**

这几乎可以肯定是 **FNIRSI DSO-153**。以这个价格来说，它是一款出乎意料功能强大的小工具——但也存在一些重要的局限性需要注意。

### ✅ 优点

它提供 **5 MS/s** 的实时采样率、**1 MHz 带宽**，支持高达 **±400V** 的电压——并具备完整的触发模式（自动/正常/单次），使其适用于周期性模拟信号和非周期性数字信号。

内置的 DDS 信号发生器可以输出 **14 种不同波形**（正弦波、方波、锯齿波、噪声、指数波等），最大输出频率可达 **10 kHz**。

它配备 **2.8 英寸 320×240 LCD 屏幕**、**1000 mAh 电池**（续航约 **4 小时**），并通过 **Type-C** USB 充电。支持 **8 种语言**（包括英语和中文），并具有一键 AUTO 模式，无需手动调整即可显示波形。

真正的价值在于将两种必备工具集成在一个紧凑、电池供电、重量不到 200 克的小巧设备中——当你需要验证信号完整性或激励电路，而不想携带多台设备时，非常实用。

---

### ⚠️ 需要注意的局限性

- **1 MHz 带宽非常有限。** 它适用于音频信号、低速串行通信（低波特率下的 UART/I2C/SPI）、电源纹波和传感器输出——但对于任何射频、高速数字信号或实际超过 ~500 kHz 的信号（经验法则：要获得清晰波形，带宽需为信号频率的 5 倍）则完全无效。
- **5 MS/s 采样率** 并不高。较高频率的信号会出现混叠或波形保真度差的问题。
- **信号发生器最高输出 10 kHz**——如果你需要生成超出音频频率范围的测试信号，这将是一个很大的限制。
- 它被描述为“非常实用且性价比高”——但其目标受众是爱好者和学习者，而非专业人士。

---

### 🎯 总结

以 219 元人民币（约 30 美元）的价格，对于其目标用户——电子专业学生、爱好者和从事基本汽车或家电诊断的技术人员来说，**性价比极高**。不要指望它能取代一台真正的台式示波器。如果你需要更高的带宽（即使是 10–50 MHz），FNIRSI 自身的产品线中有更好的选择，例如 DSO-510（10 MHz）或 2C23T（10 MHz 并带万用表），价格略高。

---

**参考链接：**

- [FNIRSI DSO-153 官方产品页面](https://www.fnirsi.com/products/dso-153)
- [Martview 上 DSO-153 的完整规格](https://www.martview.com/fnirsi-dso-153-2-in-1-portable-1mhz-bandwidth-digital-oscilloscope-signal-generator.html)
- [亚马逊上的 DSO153](https://www.amazon.com/FNIRSI-DSO153-Oscilloscope-Generator-Automotive/dp/B0D2TGM82J)
- [DSO153 评测 – AliExpress Wiki](https://www.aliexpress.com/s/wiki-ssr/article/fnirsi-dso153-oscilloscope-signal-generator-oscope-meter-products-info-and-review)
