---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 联想 L-IG41M3 前面板引脚定义
translated: true
type: note
---

问题：如何连接**联想 L-IG41M3** 上的前置面板开关和 LED？

回答：我可以给出精确的逐针脚对应关系，但我需要**看到您这块 L-IG41M3 主板上的 F_PANEL 接口**。联想/OEM 主板可能采用非标准的前面板针脚定义，因此我不希望您盲目套用通用的 ATX 布局。

请上传一张清晰显示**F_PANEL 针脚以及主板上印刷的标注文字**的照片。

一旦您上传照片，我会用类似下图的方式标注：

```text
F_PANEL
┌─────────────────┐
│ ● ● ● ● ● ● ● ● │
│ ↑ ↑   ↑ ↑   ↑ ↑ │
│ PLED   PWR   HDD │
│       SW    LED  │
└─────────────────┘
```

并告诉您**以下每个元件的确切连接位置**：

* `POWER SW`（电源开关）
* `RESET SW`（重启开关）
* `HDD LED +`（硬盘指示灯正极）
* `HDD LED -`（硬盘指示灯负极）
* `POWER LED +`（电源指示灯正极）
* `POWER LED -`（电源指示灯负极）

另外，如果您的目的是**在机箱外测试显卡**，我会向您展示**无需连接机箱的 POWER SW** 即可启动 L-IG41M3 的最简单方法。