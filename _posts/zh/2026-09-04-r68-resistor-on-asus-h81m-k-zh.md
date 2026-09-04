---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ASUS H81M-K上的R68电阻
translated: true
type: note
---

**问题：** 在ASUS H81M-K主板上，位于4针ATX 12V连接器附近的标有**R68**的组件是什么？

**回答：**

组件**R68**是一个**电阻器**——具体来说，是一个放置在ASUS H81M-K主板**ATX12V** 4针电源连接器附近的小型SMD（表面贴装）电阻。根据典型的H81系列ASUS主板设计惯例：

- **它是什么：** R68是一个下拉或滤波电阻。在ASUS H81M系列主板上，ATX12V连接器附近R60–R70范围内的电阻通常用于CPU VRM（电压调节模块）电源传输电路中的**12V电源轨电压检测、滤波或限流**。
- **作用：** 它有助于在12V输入信号到达CPU供电阶段之前稳定或滤波该信号，或者作为PWM控制器反馈环路的电压分压器的一部分。
- **物理外观：** 通常是一个微小的0402或0603 SMD电阻，其值因主板版本而异（根据功能不同，常见范围为几欧姆到几千欧姆）。

> ⚠️ **重要说明：** ASUS官方并未公开发布H81M-K的原理图和板视图文件。**R68具体**的准确值和电路功能需要板视图/原理图文件（存在于维修社区档案中）。在无法获取实际原理图的情况下，无法确切确认其电阻值。

如果您需要精确值进行主板维修，建议：
1. 查看**Badcaps.net**上的H81M-K维修指南（该网站存在PDF维修指南）。
2. 如果可用，使用板视图工具（如OpenBoardView）配合H81M-K的`.brd`文件。

---

**参考：**
- [ASUS H81M-K用户手册 – ManualsLib（第25页，ATX电源连接器）](https://www.manualslib.com/manual/565354/Asus-H81m-K.html?page=25)
- [ASUS H81M-K主板布局（第12页）](https://www.manualowl.com/m/Asus/H81M-K/Manual/372249?page=12)
- [ASUS H81M-K维修指南 – Badcaps.net](https://www.badcaps.net/forum/document-software-archive/schematics-and-boardviews/3483342-asus-h81m-k-motherboard-repair-guide)