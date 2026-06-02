---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 选择空活动模板
translated: true
type: note
---

Question: 在 Android Studio 中创建新的 Android project 时，通常会为基础的空 app 选择哪个模板？

Answer:

正确答案是 **A) Empty Activity**。

在最新版本的 Android Studio（包括截至 2025–2026 年的版本）中，当创建新项目并选择 "Phone & Tablet" 类别时，最常用且最推荐的基础空 app 模板是 **Empty Activity**。该模板提供了一个极简的设置，包含一个单一的空白 activity（通常是 `MainActivity.kt` 或 `.java`）及其对应的 layout 文件（`activity_main.xml`），默认仅包含一个 "Hello World!" TextView。它非常适合从零开始构建，而无需任何预先添加的 UI components，如 toolbars、floating action buttons 或 navigation elements。

- **Basic Activity**: 包含额外的 UI elements，例如 app bar、floating action button，通常还有一个 menu——这超出了一个真正的基础空 app 的范畴。
- **Navigation Drawer Activity**: 添加了一个带有菜单的侧滑 navigation drawer，适用于具有多个 section 的 app。
- **Blank Fragment**: 侧重于创建基于 fragment 架构的项目，而不是简单的 single-activity app。

"Empty Activity"（在较新的模板中育时也被标记为 "Empty Views Activity"）仍然是作为最简单起点的标准选择。

References:

- [Android Developers - Create a project](https://developer.android.com/studio/projects/create-project)
