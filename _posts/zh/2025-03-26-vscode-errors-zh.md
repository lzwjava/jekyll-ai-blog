---
audio: false
generated: true
lang: zh
layout: post
title: 隐藏VSCode项目中的错误红线
translated: true
type: note
---

我为之前的误解道歉。看来我之前的方案未能正确满足您在 Visual Studio Code (VSCode) 中为使用 Gradle 的 Java Spring 项目禁用错误指示器（红色波浪线）的需求，特别是针对“找不到符号”错误。请允许我提供一个修正后的完整解决方案来有效隐藏这些错误指示器。

由于您希望禁用编辑器中的红色下划线，且错误与 Java 相关（很可能由 VSCode 中的 Java 语言服务器检测到），我将重点介绍直接控制错误显示而不依赖可能不适用的假设的解决方案。以下是实现此目标的步骤：

---

###
