---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 VS Code 中双击打开文件
translated: true
type: note
---

**Question: 在 GitHub Desktop 中，查看历史提交（history commit）时，双击中间面板已更改文件列表中的文件，会用 VS Code 打开它吗？**

**Answer:**

**是的，这是 GitHub Desktop 近期版本中支持的功能。**

当你执行以下操作时：

- 进入 **History** 标签页
- 选择一个过去的提交（commit）
- 在中间面板中看到更改的文件列表（该提交的 "changed files" 列表）

双击该列表中的文件将**在你配置的 External editor 中（例如 Visual Studio Code）**打开该文件（如果你已经设置了编辑器）。

这一行为是作为一项呼声极高的社区贡献功能在 2023 年左右加入的。它在以下两种情况下均有效：

- 在 **History** 视图中（针对过去提交中更改的文件 —— 注意：它打开的是文件的**当前/工作副本**版本，而不是该提交中的历史版本）
- 在 **Changes** 视图中（针对未提交的本地更改）

要专门针对 VS Code 进行此设置：

1. 前往 **File → Options → Integrations**（macOS 上为 **GitHub Desktop → Preferences**）
2. 在 **External editor** 下，选择 **Visual Studio Code**（如果已安装，它通常会自动检测；如果没有，请指向可执行文件路径）
3. 设置完成后，双击 Changes 列表或提交的文件列表中的文件，将直接在 VS Code 中启动/打开该文件。

在此功能添加之前（在旧版本中），双击通常只是在 GitHub Desktop 内部显示 diff，你必须通过右键点击 → "Open in Visual Studio Code"（或使用菜单/键盘快捷键）才能在编辑器中打开完整文件。部分用户曾反馈，在某些更新中，快速点击会被误判为双击，从而导致意外打开文件。

如果双击没有为你打开 VS Code：

- 确认 VS Code 已正确设置为 External editor。
- 确保你双击的是列表中的文件名/条目（而不是 diff 区域）。
- 将 GitHub Desktop 更新到最新版本，因为这是一个相对较新的功能。

这使得审阅提交历史并快速跳转到 VS Code 编辑文件变得更加顺畅 —— 这是一个非常棒的体验改进！

**References:**

- [GitHub Changelog: Community adds "Double click to Open External Editor"](https://github.blog/changelog/2023-08-16-github-desktop-community-adds-check-out-a-commit-and-double-click-to-open-external-editor)
- [GitHub Desktop issue discussions on double-click behavior](https://github.com/desktop/desktop/issues?q=is%3Aissue+double+click+file+external+editor)
