---
audio: false
generated: true
image: false
lang: zh
layout: post
title: L-IG41M3上的示波器测量
translated: true
type: note
---

问题：你只是想要**学习如何从 L-IG41M3 获取真实的 oscilloscope 测量**，而不是诊断具体故障。

答案：完美。从**简单的 DC 测量**开始。你的 oscilloscope 应该显示实际的电压值和波形。

### 1. 从 +5VSB 开始

最简单的点是 **24-pin ATX connector**。

设置你的 scope：

```text
Probe:       ×10
Coupling:    DC
Vertical:    2 V/div
Time:        1 ms/div
```

连接：

```text
scope GND clip → motherboard GND
probe tip      → purple PSU wire (+5VSB)
```

你应该会看到大约：

```text
      ~5 V
       ─────────────────────
```

所以你已经在测量一个真实的值了：

```text
V ≈ 5.0 V
```

这是一个很好的第一个 oscilloscope 练习，因为它应该是稳定的。

### 2. 测量 +12 V

将 probe tip 移动到 ATX connector 上的**黄色线**。

预期：

```text
V ≈ 12 V
```

你应该会看到：

```text
12V ───────────────────────
```

### 3. 测量 +5 V

探测**红色线**：

```text
V ≈ 5 V
```

### 4. 测量 +3.3 V

探测**橙色线**：

```text
V ≈ 3.3 V
```

所以你完全可以给自己做一个小的 oscilloscope 练习：

```text
purple → ~5 V
yellow → ~12 V
red    → ~5 V
orange → ~3.3 V
black  → GND
```

**不要将 scope ground clip 放在除 GND 之外的任何东西上。**

---

### 5. 然后尝试 F_PANEL 信号

当你感到舒适后，连接：

```text
GND clip → pin 11
probe    → pin 9
```

使用：

```text
1 V/div
500 ms/div
DC coupling
```

现在短暂触碰：

```text
pin 9 ↔ pin 11
```

你应该会看到一个**脉冲/跳变**，而不是恒定的电压。

这比简单地测量 DC rail 有趣得多：

```text
HIGH ────────────┐
                 │
                 └──────────── HIGH
                 ↑
             button press
```

然后你可以尝试使用 scope 的：

* `Vmax`
* `Vmin`
* `Vpp`
* frequency
* period
* trigger

这将教你这些数字的实际含义。

### 如果你只是想练习

你甚至不需要主板。拿起你的 oscilloscope + probe 并测量：

```text
5VSB → DC voltage
12V  → DC voltage
5V   → DC voltage
3.3V → DC voltage
```

然后测量 **F_PANEL pin 9 同时按下按钮**。这可能是学习这块板子上 scope 的最佳下一步。

如果你发送一张你的 **DSO153 screen + probe + L-IG41M3 board** 的照片，我可以准确告诉你 probe 应该放在哪里，以及你应该看到什么值。
