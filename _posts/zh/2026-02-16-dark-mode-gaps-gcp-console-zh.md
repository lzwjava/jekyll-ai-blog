---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Google Cloud 控制台中的深色模式间隙
translated: true
type: note
---

**Question:** 为什么 Google Cloud Console 已经有了 dark theme，但 tutorial 或侧边面板（side panel）仍然显示为 light mode，且不支持 dark mode？

**Answer:**

Google Cloud Console 自 2026 年初起已原生支持 **dark mode**（该功能近期已正式发布）。你可以通过以下步骤启用：

1. 打开 Google Cloud Console。
2. 点击工具栏中的 **Settings and utilities** 图标（齿轮状）。
3. 从菜单中选择 **Appearance**。
4. 选择 **Dark**、**Light** 或 **Same as device**（以匹配你的 OS 主题）。

主控制台界面——包括导航栏、页眉和大多数面板——都应该能正常切换到 dark mode。

然而，**tutorial pane**（在启动新功能或遵循 console 中的 codelab 指南时，经常出现在侧边/右侧的引导式教程或上下文帮助面板）有时即使在控制台其余部分处于 dark mode 时仍保持 light mode。这是 Google Cloud 界面中已知的一致性问题：

- 某些叠加或嵌入的帮助/教程组件（如侧边抽屉、onboarding wizards 或内联文档面板）尚未完全实现主题化，无法遵循控制台的 dark mode 设置。
- 在类似的 Google 产品中也曾报告过这种行为（例如，其他服务中的侧边面板偶尔无法完美同步主题）。
- 主控制台 UI 已完全兼容 dark mode，但辅助元素（如 tutorials 或特定的 legacy/iframe-based 帮助内容）可能出于可读性或开发原因默认为 light mode。

**可能的解决方案：**
- 尝试在切换主题后刷新页面或关闭并重新打开 tutorial pane。
- 如果问题持续存在，这可能是一个暂时的限制——Google 一直在积极改进各服务的 dark mode 覆盖范围（例如，Vertex AI、Cloud Shell Editor 等最近的更新显示出更好的支持）。
- 为了在查看教程时获得更好的眼睛舒适度，你可以使用 Dark Reader 等浏览器扩展程序（尽管它可能会破坏某些交互式控制台元素，请谨慎使用）。
- 关注官方文档的更新，因为主题一致性仍在不断优化中。

如果此问题持续存在或影响到特定的 tutorial，请考虑直接在控制台中提供反馈（通过 "?" 帮助菜单 → Send feedback），以帮助 Google 优先处理修复。

**References:**

- [Change the appearance of the Google Cloud console](https://docs.cloud.google.com/docs/get-started/console-appearance)
- [Google Cloud blog/news mentions of Dark Mode GA](https://cloud.google.com/blog/topics/inside-google-cloud/whats-new-google-cloud)
