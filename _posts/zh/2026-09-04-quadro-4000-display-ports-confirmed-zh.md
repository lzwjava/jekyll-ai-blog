---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 确认Quadro 4000显示端口
translated: true
type: note
---

问题：Quadro 4000 是否配备 **2× DisplayPort + 1× DVI**？

答案：**是的，如果你的物理显卡确实如此，那很可能是另一种 Quadro 4000 变体/OEM 设计。** 我之前的回答过于笼统。

原版全尺寸 NVIDIA Quadro 4000 (Fermi) 参考设计通常是 **2× DisplayPort + 1× DVI-I**。

因此，如果你的显卡接口是：

```text
[ DP ] [ DP ] [ DVI-I ]
```

那就是正常的。

如果你上传一张挡板的照片，我可以识别出具体的 Quadro 4000 型号，并告诉你每个接口支持什么。