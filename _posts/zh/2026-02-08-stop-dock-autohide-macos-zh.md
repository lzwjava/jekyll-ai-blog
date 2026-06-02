---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 停止 macOS 程序坞自动隐藏
translated: true
type: note
---

问题：在最新版本的 macOS 中如何取消 Dock 自动隐藏？

回答：

在最新的 macOS 版本中（截至 2026 年 2 月的 macOS Tahoe 26.x），请按照以下步骤停止 **Dock** 自动隐藏并使其始终可见：

1. 点击屏幕左上角的 **Apple menu** ()。
2. 选择 **System Settings**（在较旧版本中为 System Preferences）。
3. 在侧边栏中，向下滚动并点击 **Desktop & Dock**。
4. 找到名为 **Automatically hide and show the Dock** 的选项（可能显示为复选框或切换开关）。
5. **关闭它** / **取消勾选** 该框。

现在 Dock 将永久保留在屏幕底部（或侧面）。

### 使用键盘快捷键的快速替代方法（如果已启用）

- 按下 **Command (⌘) + Option (⌥) + D**
  这将立即切换自动隐藏设置。如果关闭了自动隐藏，则操作完成。

### 如果设置会自动重新启用

- 前往 **System Settings → Keyboard → Keyboard Shortcuts**（或在 System Settings 中搜索 "shortcuts"）。
- 查找 **Turn Dock hiding on/off**（通常位于 Mission Control 或 App Shortcuts 下）。
- **取消勾选** 或禁用该快捷键，以防止意外触发（这是该问题反复出现的常见原因）。

### 如果选项呈灰色或无法正常工作

这种情况偶尔发生在某些 beta 版本或特定的配置中（例如，开启了 Stage Manager 或特定的 window tiling 设置）。请尝试：

- 临时关闭 Stage Manager（System Settings → Desktop & Dock → Stage Manager）
- 重新启动 Mac
- 作为最后手段，在 Terminal 中重置 Dock 偏好设置：

  ```
  defaults delete com.apple.dock && killall Dock
  ```

  （这将把许多 Dock 设置恢复为默认状态 —— 然后你可以再次关闭自动隐藏。）

这些步骤在 macOS Ventura、Sonoma、Sequoia 和 Tahoe 中均适用。

References:

- [Change Desktop & Dock settings on Mac - Apple Support](https://support.apple.com/guide/mac-help/change-desktop-dock-settings-mchlp1119/mac)
- [Apple Support Communities - Dock keeps auto-hiding on macOS Tahoe](https://discussions.apple.com/thread/256140771)
- [Apple Stack Exchange - Why does my dock's "Automatically Hide" keep getting re-enabled?](https://apple.stackexchange.com/questions/441389/why-does-my-docks-automatically-hide-keep-getting-re-enabled)
