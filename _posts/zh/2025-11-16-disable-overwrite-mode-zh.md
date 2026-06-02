---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 禁用VS Code覆盖模式
translated: true
type: note
---

在 Visual Studio Code 中，默认行为是**插入模式**（输入文本时会插入文字，并将现有文本向后推移）。
**替换模式**（输入文本时会覆盖现有文字）可通过按下键盘上的 **Insert** 键激活——该按键可在插入模式和替换/覆盖模式之间切换。

### 如何从替换（覆盖）模式切换回插入模式

1. 只需按下键盘上的 **Insert** 键一次。
   → 底部右侧状态栏的显示将从 **OVR**（覆盖）变为 **INS**（插入）。

### 若希望彻底避免意外进入覆盖模式

您可完全禁用 Insert 键的切换功能：

#### 方法 1：键盘快捷键（推荐）

按下 `Ctrl + Shift + P` → 输入 **"切换插入/覆盖"** → 您将看到
`首选项：切换粘贴时插入和覆盖输入`或类似命令。
更可靠的方法是直接修改设置：

#### 方法 2：在 `settings.json` 中添加以下配置

```json
// 禁用 Insert 键切换覆盖模式
"editor.occurencesHighlight": true,
"editor.overtypeMode": false,

// 关键配置项：
"keyboard.dispatch": "keyCode"
```

实际最常用且有效的解决方案：

```json
// 在 VS Code 中完全禁用 Insert 键
{
    "key": "insert",
    "command": "-editor.action.toggleOverwrite",
    "when": "editorTextFocus"
}
```

或直接全局关闭覆盖模式：

```json
"editor.occurrencesHighlight": true,
"editor.overwriteMode": false   // 非真实配置项，可忽略

// 禁用覆盖切换的真实配置：
"editor.insertSpaces": true,  // 无关配置

// 正确方式：
{
    "key": "insert",
    "command": "noop"   // 或移除默认绑定
}
```

#### 最简便的永久解决方案（多数开发者使用）

1. 打开设置（`Ctrl + ,`）
2. 搜索 **"overwrite"**
3. 取消勾选 **Editor: Overtype**（若存在）或更推荐：
4. 在 `settings.json` 中添加这行（Ctrl + Shift + P → "Preferences: Open Settings (JSON)"）：

```json
// 完全禁用 Insert 键切换覆盖模式
{
    "key": "insert",
    "command": "-editor.action.toggleOverwrite"
}
```

添加此配置后，Insert 键在 VS Code 中将失效，您将始终处于插入模式。

这是最常用可靠的解决方案，特别适用于经常误触 Insert 键的开发者（尤其是键盘紧凑的笔记本电脑用户，在台湾/亚洲地区尤为常见）。

若您使用 macOS（按键不同）或需要状态栏点击解决方案，请随时告知！
