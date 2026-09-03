---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 连接前面板接头
translated: true
type: note
---

问题：如何将 `POWER SW`、`RESET SW`、`HDD LED` 和 `POWER LED +/-` 连接到主板上的 `F_PANEL` 接口？

答案：

常见的前面板布局如下：

```text
F_PANEL
┌─────────────────────────────┐
│ 1  2  3  4  5  6  7  8  9 10 │
│ ●  ●  ●  ●  ●  ●  ●  ●  ●  ○ │
│ ●  ●  ●  ●  ●  ●  ●  ●  ●  ● │
│ 11 12 13 14 15 16 17 18 19 20 │
└─────────────────────────────┘
```

但**具体引脚定义因主板而异**。最常见的 Intel/ATX 布局如下：

```text
        F_PANEL

HDD LED +   HDD LED -
    |           |
    ●           ●

POWER LED +  POWER LED -
    |            |
    ●            ●


POWER SW
   ● ●

RESET SW
   ● ●
```

### 重要提示

对于**开关**：

```text
POWER SW  →  任意方向
RESET SW  →  任意方向
```

它们只是瞬时开关，**极性无关紧要**。

对于**LED**：

```text
HDD LED
  + → LED+
  - → LED-

POWER LED
  + → LED+
  - → LED-
```

**极性**很重要。如果 LED 不亮，请断电并反接连接器。

如果您正在处理您的 **Lenovo L-IG41M3** 主板，请发送一张主板 `F_PANEL` 引脚附近区域的清晰照片。联想的引脚定义可能与通用 ATX 布局不同，我可以**精确标记出 POWER SW、RESET SW、HDD LED 和 POWER LED 对应的两个引脚**。

我还可以指导您如何利用主板的 `F_PANEL` 引脚**用螺丝刀启动电脑**，这在机箱外测试主板时非常有用。
