---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过F_PANEL针脚9-11关机
translated: true
type: note
---

问题：如何从 F_PANEL 接头上关闭 L-IG41M3 的电源？

回答：**你通常使用相同的两个 pin：9 和 11。**

* **开机：** 短暂短接 **pin 9 ↔ pin 11**（约 0.5 秒）。
* **正常关机：** 再次短暂短接 **pin 9 ↔ pin 11**（约 0.5 秒）。主板/操作系统会将其解读为按下电源按钮。
* **强制关机：** 持续按住 **pin 9 ↔ pin 11** 约 **4 秒**。这等同于按住机箱电源按钮。

```text
F_PANEL

Pin 9  ───┐
          │ ← 螺丝刀 / 开关
Pin 11 ───┘

短暂短接 → 开机 / 请求关机
按住约 4 秒 → 强制关机
```

**不要通过短接其他 pin 来关闭电源。** `PS` + `GND` 这对引脚才是用于此用途的。

如果你上传一张接头的照片，我可以根据方向识别你实际主板上的 **pin 9 和 11**。
