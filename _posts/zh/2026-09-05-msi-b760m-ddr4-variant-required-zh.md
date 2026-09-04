---
audio: false
generated: true
image: false
lang: zh
layout: post
title: MSI B760M DDR4版本需求
translated: true
type: note
---

问题：MSI B760M 主板可以使用 DDR4 内存吗？

答案：**只有在它是 DDR4 版本的情况下才可以。** B760M 是芯片组/平台名称；MSI 同时生产 DDR4 和 DDR5 主板。

例如：

* **MSI PRO B760M-E DDR4** → ✅ DDR4
* **MSI PRO B760M-E D5** → ❌ DDR4，**仅支持 DDR5**
* **MSI MAG B760M MORTAR WIFI DDR4** → ✅ DDR4
* **MSI MAG B760M MORTAR WIFI**（DDR5 版本） → ❌ DDR4

DDR4 和 DDR5 **不能物理互换**：防呆缺口位置不同，电气信号/PMIC 架构也不同。

所以对于你正在看的 **120 CNY 的 MSI PRO B760M-E D5**，你的三星 **8 GB PC3L DDR4** 内存条**无法**使用。你需要 DDR5 内存条。

如果你把这块主板的照片发给我，我可以根据主板上的标记识别内存类型。
