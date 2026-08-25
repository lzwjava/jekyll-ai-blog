---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 主板上的LED极性
translated: true
type: note
---

**问题：为什么主板有独立的 Power LED+ 和 Power LED− 针脚，而不是只有一个？**

**回答：** 因为 LED 是**极性元件**——它们只允许电流单向流动。这是基本的电子学原理：

- **Power LED+** 是**阳极**（正极端）——电流从此处流入
- **Power LED−** 是**阴极**（负极端）——电流从此处流出

如果将 LED 接反（极性颠倒），它**不会发光**（在某些情况下还可能损坏）。因此，主板明确分开这两个针脚，让你能正确连接接口。

**为什么不能只有一个针脚？**  
单个针脚无法独自构成回路。每个电路都需要一个电源端（+）和一个返回路径（−/地线）。两个针脚共同形成完整的回路：

```
主板 3.3V → LED+ → [LED 点亮] → LED− → 地线
```

有些主板确实通过**单个 3 针或组合接口**简化了设计，但它们内部仍然同时具备 + 和 − 连接——只是物理上合并了。

**实用小贴士：** 如果前面板电源 LED 不亮，尝试**将接口翻转 180°**——极性问题是最常见的原因。

参考来源：

- [LED 工作原理——极性详解](https://learn.sparkfun.com/tutorials/polarity/diode-and-led-polarity)
- [主板前面板接口指南](https://www.tomshardware.com/reviews/motherboard-front-panel-connectors,2312.html)
