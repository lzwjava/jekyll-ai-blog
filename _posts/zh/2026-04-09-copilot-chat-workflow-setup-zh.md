---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Copilot聊天窗口工作流设置
translated: true
type: note
---

问：“Chat: 将聊天移至新窗口 (Cmd+L)”和“Chat: 新建聊天编辑器”这两个快捷键绑定是否实用？应如何使用？

答：

是的——这两个命令共同提供了最简洁的**独立 Copilot 聊天窗口工作流**。

### 1. Chat: 将聊天移至新窗口

此功能将**当前 Copilot 聊天**移至独立的 VS Code 窗口。

推荐绑定：

```json
{
  "key": "cmd+l",
  "command": "workbench.action.chat.moveToNewWindow"
}
```

功能说明：

* 保留当前对话
* 将聊天拆分为独立窗口
* 最适合多显示器工作流

---

### 2. Chat: 新建聊天编辑器

此功能创建一个**新聊天标签页**（类似于打开新文档）

推荐绑定：

```json
{
  "key": "cmd+shift+l",
  "command": "workbench.action.chat.openInEditor"
}
```

功能说明：

* 开启全新独立聊天
* 以编辑器标签页形式存在
* 后续可移至新窗口

---

### 最佳工作流

1. `Cmd + Shift + L` → 新建聊天编辑器
2. `Cmd + L` → 移至新窗口

效果：

* 一个窗口 = 代码编辑区
* 一个窗口 = Copilot 聊天区
* 可同时开启多个聊天会话

这是目前**最高效的 Copilot 高级用户配置方案**。
