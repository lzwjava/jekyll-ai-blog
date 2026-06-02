---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在新窗口中打开GitHub Copilot聊天
translated: true
type: note
---

问题：如何在VS Code中设置快捷键，让GitHub Copilot Chat移动到独立（新）窗口？

答案：

若希望Copilot Chat**在编辑器/独立窗口中打开**，需为相应命令绑定快捷键。

### 步骤1 —— 查找命令

打开命令面板：

```
Cmd/Ctrl + Shift + P
```

搜索：

```
Chat: Open in Editor
```

该命令会将Copilot Chat以**标签页**形式打开，之后可将其拖拽至**独立窗口**。

VS Code支持在多类界面中打开聊天窗口，包括**编辑器标签页或独立窗口**。（[Visual Studio Code][1]）

---

### 步骤2 —— 绑定快捷键

打开键盘快捷键JSON文件：

```
Cmd/Ctrl + Shift + P
→ Preferences: Open Keyboard Shortcuts (JSON)
```

添加：

```json
{
  "key": "cmd+shift+o",
  "command": "workbench.action.chat.openInEditor"
}
```

（Windows系统）

```json
{
  "key": "ctrl+shift+o",
  "command": "workbench.action.chat.openInEditor"
}
```

---

### 步骤3 —— 移至独立窗口（可选）

在编辑器标签页中打开后：

* 拖拽标签页脱离原窗口
  或
* 按下：

```
Cmd/Ctrl + K 再按 O
```

此时聊天窗口将在**新的VSCode窗口**中打开

---

### 推荐配置（一步到位）

直接绑定快捷键：

```json
{
  "key": "ctrl+alt+c",
  "command": "workbench.action.chat.openInEditor"
},
{
  "key": "ctrl+alt+w",
  "command": "workbench.action.moveEditorToNewWindow"
}
```

现在：

* `Ctrl+Alt+C` → 在编辑器中打开聊天窗口
* `Ctrl+Alt+W` → 将窗口弹出至独立新窗口

---

### 其他实用的Copilot Chat快捷键

* 打开聊天视图：`Ctrl+Alt+I`
* 行内聊天：`Ctrl+I`
* 快速聊天：`Ctrl+Shift+Alt+L`（[Visual Studio Code][2]）

---

如有需要，还可配置：

* 切换聊天窗口快捷键
* 始终在新窗口打开聊天
* 分屏布局（代码与聊天并排显示）

[1]: https://code.visualstudio.com/docs/copilot/copilot-chat?utm_source=chatgpt.com "聊天功能概览"
[2]: https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features?utm_source=chatgpt.com "VS Code中的GitHub Copilot速查表"
