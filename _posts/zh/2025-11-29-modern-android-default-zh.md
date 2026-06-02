---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: ConstraintLayout：现代安卓默认布局方案
translated: true
type: note
---

正确答案是 **C. ConstraintLayout**。

**说明**：
自2017年起，Google已正式推荐将**ConstraintLayout**作为现代Android开发的默认布局管理器。从Android Studio 2.3开始，它就成为Android Studio布局编辑器的默认选项，至今（2025年）仍是首选方案。

**ConstraintLayout的优势**：
- 极致灵活——可替代LinearLayout、RelativeLayout乃至复杂的嵌套布局
- 性能卓越——采用扁平化视图层级（避免影响性能的深层嵌套）
- Android Studio提供强大的设计时工具（拖拽操作、约束链、屏障、参考线）
- 支持高级功能，如百分比定位、宽高比约束及运动布局集成

**已过时/遗留方案**：
- **RelativeLayout**已被官方标记为"非最优选择"，基本被取代
- **LinearLayout**仍适用于简单场景（如垂直/横向列表），但不适合复杂界面
- **FrameLayout**主要用于单子项叠层或碎片布局

当前Google官方文档和Android开发者培训在新示例中已几乎全部采用ConstraintLayout。

因此对于2025年及以后的新项目：**除非有特殊原因，请始终优先使用ConstraintLayout**。
