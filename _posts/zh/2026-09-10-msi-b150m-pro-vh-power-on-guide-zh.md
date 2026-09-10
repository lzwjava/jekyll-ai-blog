---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI B150M PRO-VH 开机指南
translated: true
type: note
---

问题：**MSI B150M PRO-VH 的前面板连接器在哪里？如何开机？**

回答：

在 **MSI B150M PRO-VH** 上，前面板连接器称为 **JFP1**，而不是 `P_FRONT_PANEL`。手册确认它有一个 10 针 JFP1 接头。（[ManualsLib][1]）

引脚定义如下：

```text
JFP1
┌─────────────────┐
│ 2  4  6  8  10 │
│ 1  3  5  7  9  │
└─────────────────┘

1  HDD LED +
3  HDD LED -

2  Power LED +
4  Power LED -

5  RESET SW
7  RESET SW

6  POWER SW
8  POWER SW

9  Reserved
10 No Pin
```

对于**仅测试主板**，你不需要机箱的电源按钮。

### 用螺丝刀开机

在 PSU 连接的情况下：

```text
24-pin ATX  → motherboard
8-pin CPU   → motherboard
```

然后用螺丝刀短暂触碰以下两个引脚：

```text
JFP1 pin 6 ↔ pin 8
```

这就是 **POWER SW** 引脚对。MSI 的手册明确将引脚 6/8 标识为电源开关。（[manualzz.com][2]）

**仅短暂短接它们**——大约 0.5–1 秒。不要将螺丝刀一直放在那里。

你不需要连接：

```text
HDD LED
POWER LED
RESET SW
```

就能让主板启动。

如果你实在找不到 **JFP1**，请发送一张你的 B150M PRO-VH 主板照片，我可以指出具体的引脚。

参考：

* [MSI B150M PRO-VH 手册列表](https://www.manualslib.com/products/Msi-B150m-Pro-Vh-13624495.html?utm_source=chatgpt.com)
* [MSI 前面板接头引脚定义](https://mans.io/files/viewer/203929/6?utm_source=chatgpt.com)

[1]: https://www.manualslib.com/products/Msi-B150m-Pro-Vh-13624495.html?utm_source=chatgpt.com "Msi B150M PRO-VH Manuals | ManualsLib"
[2]: https://manualzz.com/doc/o/1guq12/msi-b150m-pro-vdh-motherboard-user-manual-overview-of-components?utm_source=chatgpt.com "Overview of Components. MSI B150M PRO-VDH, MS-7982v1.1 | Manualzz"