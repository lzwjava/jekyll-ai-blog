---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将前面板线缆连接到L-IG41M3
translated: true
type: note
---

问题：如何将前面板线缆连接到您照片中显示的 **Lenovo/ECS L-IG41M3** `F_PANEL` 接头上？

我查阅了 **L-IG41M3 Rev. 1.1 原理图**，发现这**不是标准的 9 针 ATX F_PANEL**。它是一个 2×7 排针，带有缺失/防呆键位。原理图明确规定了各引脚的定义。([ManualMachine][1])

从您的照片来看，该接头是标有 `F_PANEL` 的黑色两排连接器。

### Pinout

请按照您照片中的方向放置，使 **`F_PANEL` 文字位于接头下方**：

```text
                F_PANEL
        ┌───────────────────┐
        │  1   3   5   7   9   11  13 │
        │  ●   ●   ●   ●   ●    ●   ○ │
        │  ●   ●   ●   ●   ●    ●   ● │
        │  2   4   6   8   10   12  14 │
        └───────────────────────────────┘

        1   HLED+
        2   HLED-

        3   PLED-Y
        4   VCC

        5   PLED-G
        6   GND

        7   PLED+
        8   GND

        9   POWER / PS
       10   SPK

       11   GND
       12   RESET

       13   KEY / no pin
       14   GND
```

此映射直接来自 L-IG41M3 原理图中的 `H7X2-P13E-BK` F_PANEL 定义。([ManualMachine][1])

### 对于您的线缆

**POWER SW**

使用：

```text
POWER SW
  │
  ├──── pin 9  (PS / PWRBTN)
  │
  └──── pin 11 (GND)
```

因此：

```text
pin 9  ─── POWER SW ─── pin 11
```

**POWER SW 的极性无关紧要。**

---

**RESET SW**

使用：

```text
pin 12 ─── RESET SW ─── pin 14
```

同样，**极性无关紧要**。

---

### HDD LED

使用：

```text
HDD LED +  → pin 1
HDD LED -  → pin 2
```

在这里，极性**很重要**。

如果磁盘活动时灯不亮，请调换正负极。

### Power LED

这块主板略微特殊。

原理图实际上提供了：

```text
pin 3 = PLED-Y
pin 4 = VCC
pin 5 = PLED-G
pin 7 = PLED+
pin 8 = GND
```

原版联想设计支持**双色电源 LED**（绿色/黄色），而不是许多 ATX 主板上那种简单的两针 `PLED+ / PLED-` 排列。([ManualMachine][1])

如果您的机箱配备的是**普通的 2 线 POWER LED**：

```text
POWER LED + → pin 7
POWER LED - → pin 8
```

对于普通的 2 针 LED，我会使用这一对。

### 因此，四个重要的连接如下

```text
             L-IG41M3 F_PANEL

HDD LED +  ───────── pin 1
HDD LED -  ───────── pin 2

POWER LED + ──────── pin 7
POWER LED - ──────── pin 8

POWER SW ─────────── pin 9 + pin 11

RESET SW ─────────── pin 12 + pin 14
```

并且**不要向 pin 13 连接任何东西**——它是 `KEY` 位置/防呆键位。

### 对于您的 GPU 测试

实际上您完全不需要机箱开关。

连接好 PSU 后，您可以短暂短接：

```text
pin 9 ──┐
        │ ← 用螺丝刀触碰这两个引脚
pin 11 ─┘
```

约 **0.5 秒**。

这在电气上等同于按下 `POWER SW`。

这对于您的裸机 GPU 测试特别有用：将主板放在桌面上，连接 PSU + CPU/RAM/GPU，然后短暂短接两个电源按钮引脚即可启动。

**不要随意短接 F_PANEL 的引脚。** 原理图确认 pin 9 是电源按钮信号，pin 11 是接地。([ManualMachine][1])

参考资料：

* [ECS L-IG41M3 Rev. 1.1 schematic](https://manualmachine.com/ecs/lig41m3/24375062-schematics--rev-1/?utm_source=chatgpt.com)
* [L-IG41M3 schematic mirror/reference](https://www.repairlap.com/threads/ecs-l-ig41m3-rev-1-1-schematics.20342/?utm_source=chatgpt.com)

[1]: https://manualmachine.com/ecs/lig41m3/24375062-schematics--rev-1/?utm_source=chatgpt.com "ECS L-IG41M3 Schematics REV 1.1 - ManualMachine.com"
