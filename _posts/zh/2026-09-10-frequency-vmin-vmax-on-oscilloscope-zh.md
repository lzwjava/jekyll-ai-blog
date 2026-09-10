---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 示波器上的频率、最小电压、最大电压
translated: true
type: note
---

问题：示波器上的 **频率、Vmin 和 Vmax** 是什么意思？

回答：

它们描述的是您正在测量的电压波形：

* **频率（Hz）**——波形重复的快慢。

  * `1 Hz` = 1 周期/秒
  * `1 kHz` = 1,000 周期/秒
  * `1 MHz` = 1,000,000 周期/秒
  * 周期与频率的关系为：

    $$
    f=\frac{1}{T}
    $$

* **Vmax** —— 在测量窗口内波形达到的最高电压。

* **Vmin** —— 波形达到的最低电压。

例如，如果示波器显示一个在 **0 V 和 5 V** 之间以 **1 kHz** 切换的方波：

```text
Voltage
  5V ──┐    ┌────┐    ┌────
       │    │    │    │
  0V ──┴────┘    └────┘
       <--- 1 ms --->

Frequency = 1 kHz
Vmax      = 5 V
Vmin      = 0 V
```

则有：

$$
V_{pp}=V_{max}-V_{min}=5V
$$

对于您的 **主板/GPU 维修测量**，这三个数值尤其有用：**Vmin/Vmax 告诉您电源轨是否实际达到了预期电压，而频率则告诉您开关稳压器是否在运行。**

例如，一个 buck 转换器可能显示如下：

```text
Vmin ≈ 0.2 V
Vmax ≈ 12 V
Frequency ≈ 500 kHz
```

这与看到平坦的 `12 V` 直流信号截然不同。

如果您愿意，接下来我可以向您展示 **究竟应该将示波器的红/黑探针放在主板的哪个位置，才能测量一个开关稳压器并实际读取到频率/Vmin/Vmax 数值**。
