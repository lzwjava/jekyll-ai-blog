---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Qwen 中无新建对话快捷方式
translated: true
type: note
---

问题：在 chat.qwen.ai 中，类似 Grok 的 Command + J 快捷键，新建对话的键盘快捷键是什么？

回答：

根据我的调研，**chat.qwen.ai 当前在其网页界面中尚未记录专门用于创建新对话的键盘快捷键**。

### 我的发现：

1. **Qwen Code（CLI 工具）拥有快捷键**，但这些快捷键适用于不同的产品——基于终端的编码助手，而非网页聊天界面。例如，`Ctrl+L` 用于清屏，`Ctrl+C` 用于取消请求 [[1]]。

2. **chat.qwen.ai 的网页界面**主要依赖 UI 交互。用户通常通过以下方式开始新对话：
   - 点击侧边栏中的“**+**”按钮或“**New Chat**”选项
   - 使用输入框左侧的“**+**”按钮（近期应用更新中提及）[[30]]

3. **官方尚未发布**针对网页聊天界面的快捷键文档，其中包含 Command/Ctrl + J（或类似组合）用于新建对话的功能。

### 变通方案与建议：

- **浏览器级快捷键**：可尝试 `Ctrl+T`（Mac 上为 `Cmd+T`）打开新标签页，然后访问 chat.qwen.ai 开启新会话。
- **自定义脚本**：部分用户通过浏览器扩展或用户脚本（如 Greasy Fork 上的脚本）为网页应用添加自定义快捷键 [[31]]。
- **检查 UI**：在 chat.qwen.ai 界面中寻找“**?**”或“**Help**”图标，部分网页应用会在此展示可用快捷键。

### 建议：

若希望增加此功能，可考虑：
1. 在 chat.qwen.ai 的**设置**或**帮助**菜单中查找隐藏快捷键
2. 通过官方渠道向 Qwen 团队反馈，请求添加“**New Chat**”键盘快捷键

*注：快捷键可能随更新变化，建议定期查看官方文档或应用内帮助。*

参考链接：

- [https://qwenlm.github.io/qwen-code-docs/en/users/reference/keyboard-shortcuts/](https://qwenlm.github.io/qwen-code-docs/en/users/reference/keyboard-shortcuts/) [[1]]
- [https://apps.apple.com/kz/app/qwen-chat-ask-qwen-know-more/id6743778442](https://apps.apple.com/kz/app/qwen-chat-ask-qwen-know-more/id6743778442) [[30]]
- [https://greasyfork.org/en/scripts/by-site/qwen.ai](https://greasyfork.org/en/scripts/by-site/qwen.ai) [[31]]