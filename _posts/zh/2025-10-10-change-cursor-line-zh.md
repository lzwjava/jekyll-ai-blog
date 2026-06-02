---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 将VS Code光标更改为线条
translated: true
type: note
---

### 修复 VS Code 中的块状（矩形）光标

明白了——您的情况是光标切换成了块状/矩形样式（常见于覆盖模式或默认设置），但您想要更便于编辑的细垂直线样式。这只需简单调整设置即可解决。请严格按以下步骤操作：

#### 通过设置界面（最便捷）

1. 打开 VS Code
2. 按下 `Ctrl + ,`（Windows/Linux）或 `Cmd + ,`（macOS）打开设置
3. 在顶部搜索框输入：**cursor style**
4. 找到 **Editor: Cursor Style**（位于 Text Editor > Cursor 分类下）
5. 点击下拉菜单选择 **Line**（当前可能显示为 "Block"）
6. 更改立即生效——可在文件中输入文字验证是否变为细线光标

若仍未更新，请关闭后重新启动 VS Code。

#### 通过 settings.json（精准配置）

1. 打开命令面板：`Ctrl + Shift + P`（macOS 为 `Cmd + Shift + P`）
2. 输入并选择：**Preferences: Open User Settings (JSON)**
3. 在 `{}` 内添加或更新该行（若文件为空请先创建）：

   ```json:disable-run
   "editor.cursorStyle": "line"
   ```

4. 保存文件（`Ctrl + S` 或 `Cmd + S`）

#### 额外提示

- **覆盖模式？** 若误触进入“覆盖模式”（会遮挡字符），按键盘 **Insert** 键切换回插入模式
- **光标闪烁异常？** 若线条显示不连贯，在设置中搜索 **cursor blinking** 并设为 **Blink** 或 **Smooth**
- **扩展程序冲突？** 可临时禁用 Vim 等扩展（扩展视图 > 右键点击 > 禁用）进行测试

以上操作应能立即恢复清爽的线状光标。若问题依旧存在，请提供操作系统版本或截图以便进一步排查！

[VS Code 光标样式文档](https://code.visualstudio.com/docs/editor/codebasics#_cursor-style)

```
