---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 窄屏移动端CSS修复
translated: true
type: note
---

已完成 ✅ — 已部署并上线：https://truthlab.cc/（运行 `40089370394` 成功）。

移动端 CSS（≤620px）的改动内容：
- **移除**了 header 中的 `flex-wrap: wrap` 以及 nav 中的 `order: 3; width: 100%`（这些设置曾导致导航被强制换行至第二行）。
- Nav 现在**内联显示在顶部行**：`⟡ Research Services About Contact [EN|中文 ☾]` 全部在同一行。
- 紧凑调整尺寸以适应：导航链接采用 `12.5px / 5px 8px` 内边距，间隙更紧凑。

此外新增了一个 **≤400px 断点**，适用于窄屏手机（导航字体 `12px`，更紧凑的内边距/间隙），确保即使在小型屏幕上也能保持单行显示。

如果您的特定手机上仍然觉得拥挤，可轻松调整：将导航字体降至 `11.5px`，或在 340px 以下隐藏文字标记灯——乐意微调。