---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 二极管模式读数为1.5V
translated: true
type: note
---

问题：在`100C07`元件中，使用**通断/二极管档位**时，万用表显示约**1.5 V**。这意味着什么？

回答：**如果你的8901S确实处于二极管测试模式，`1.5 V`表示万用表正在测量约1.5V的正向压降/通路。这并不表示该元件具有1.5 Ω的电阻。**

关键在于，你的8901S的共用档位可能同时包含**通断测试 + 二极管测试**。在二极管模式下，万用表注入一个小电流，并显示半导体结/通路两端产生的电压。([Fluke][1])

例如：

```text
二极管模式：

红表笔 ──> [ 半导体 / 电路 ] ──> 黑表笔

显示：1.5 V
         ↑
     压降
```

### 但1.5 V并不自动意味着"故障"

`100C07`显然仍然位于**RTX 3060 PCB**上，因此你不一定是在测量一个孤立的二极管。连接到该节点的其他元件和半导体结也会产生影响。Fluke特别警告，在电路中进行二极管测量可能会受到其他通路的影响。([Fluke][1])

作为对比，普通硅二极管的正向压降通常在**0.5–0.8 V**左右。([Fluke][1])

因此：

```text
0.6 V   → 常见硅二极管正向压降
1.5 V   → 可能是半导体/网络通路
OL      → 该极性下无导通路径
0.0 V   → 极低电阻通路 / 可能短路
```

### 对你GPU最有用的测试

确保GPU完全**断电**。

在**两个方向**上测量`100C07`：

```text
测试1：
红表笔 → 100C07
黑表笔 → GND
       = ____ V

测试2：
黑表笔 → 100C07
红表笔 → GND
       = ____ V
```

同时告诉我，对于每个方向，万用表是**持续蜂鸣**、**蜂鸣一次**还是**不蜂鸣**。

**不要将`1.5 V`解释为`1.5 Ω`或将其乘以200。** 在二极管模式下，`1.5 V`是一个压降测量值。([Fluke][1])

参考资料：

* [Fluke — 如何使用数字万用表测试二极管](https://www.fluke.com/en-us/learn/blog/digital-multimeters/how-to-test-diodes?utm_source=chatgpt.com)
* [Fluke — 万用表手册：二极管/通断测试](https://assets.fluke.com/manuals/12______umeng0100.pdf?utm_source=chatgpt.com)

[1]: https://www.fluke.com/en-us/learn/blog/digital-multimeters/how-to-test-diodes?utm_source=chatgpt.com "How to Test Diodes with a Digital Multimeter | Fluke"
