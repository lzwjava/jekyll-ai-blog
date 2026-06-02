---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-sonnet-4
title: 修复VSCode交叉光标问题
translated: true
type: note
---

VSCode 中鼠标光标变为十字/加号形状通常意味着 VSCode 处于特殊模式或存在配置问题。以下是常见原因及解决方案：

## 常见原因：

1. **列选择模式**：可能意外激活了列/块选择模式
   - 尝试按下 `Alt + Shift + I` 或 `Ctrl + Shift + Alt + 方向键` 退出此模式

2. **扩展冲突**：某些扩展会改变光标行为
   - 尝试临时禁用扩展：`Ctrl + Shift + P` → "Developer: Reload Window"
   - 或在安全模式下启动 VSCode：`code --disable-extensions`

3. **缩放/选择工具**：可能激活了缩放或选择工具
   - 多次按 `Escape` 键
   - 尝试 `Ctrl + Z` 撤销近期操作

4. **终端焦点问题**：终端获得焦点时可能改变光标行为
   - 点击编辑器区域重新获取焦点
   - 尝试 `Ctrl + 1` 聚焦到编辑器

## 快速修复：

1. **重启 VSCode**：简单但通常有效
   - `Ctrl + Shift + P` → "Developer: Reload Window"

2. **检查鼠标设置**：
   - 转到 File → Preferences → Settings
   - 搜索 "cursor" 并检查光标相关设置

3. **重置工作区**：
   - 关闭 VSCode
   - 删除项目中的 `.vscode` 文件夹（如果存在）
   - 重新打开项目

4. **系统级问题检查**：
   - 测试光标问题是否出现在其他应用程序中
   - 如果是，可能是 GNOME/系统设置问题

建议先多次按 `Escape` 键，然后重启 VSCode。这通常能解决十字光标问题。
