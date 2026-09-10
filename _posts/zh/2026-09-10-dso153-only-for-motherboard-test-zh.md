---
audio: false
generated: true
image: false
lang: zh
layout: post
title: DSO153仅用于主板测试
translated: true
type: note
---

Question: 你应该将 **DDS（函数发生器）** 还是你的 **DSO153 示波器** 连接到主板？

Answer: **如果只是简单测量 L-IG41M3，只用 DSO153 即可。**

* **DSO153 = 示波器** → 测量电压/波形。
* **DDS = 信号/函数发生器** → 生成电压波形。
* 主板故障排查时通常**不需要 DDS**。

例如：

```text
L-IG41M3 ─────── 探头 ─────── DSO153
 主板              │
                   └── 测量电压
```

从以下开始：

```text
DSO153 接地夹 → 主板 GND
DSO153 探头   → +5VSB / +5V / +12V / F_PANEL 信号
```

之后，当你故意要向电路**注入已知信号**进行测试时，DDS 就变得有用了。在你确切知道引脚是什么及其允许电压之前，不要将 DDS 信号注入主板引脚。

如果你给我看你的 **DSO153 和 DDS**，我可以告诉你第一次测量时每个连接应该是什么样子。
