---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 至强E5-2673无集成显卡
translated: true
type: note
---

**问题：** Xeon E5-2673 是否集成 GPU？

**答案：** 不。**Xeon E5-2673 没有集成 GPU。**

对于 E5-2673 系列：

```text
Xeon E5-2673
├── CPU 核心：有
├── 内存控制器：有
├── PCIe 控制器：有
└── 集成 GPU：❌ 无
```

因此，在 **X99 主板 + E5-2673** 平台上，主板的 HDMI/DVI/VGA 接口通常 **无法输出画面**，你需要配备独立显卡。

这一点对你的 **GPU 维修/测试平台** 来说其实很重要：X99 + Xeon 组合必须有能正常工作的独立显卡才能显示输出；而采用英特尔核显的 **H81/B85 + i5** 平台，即使不插独立显卡也能正常启动并显示画面。

我还可以将 **X99 + E5-2673** 与 **H81 + i5-4xxx** 作为 GPU 维修测试平台进行具体对比。
