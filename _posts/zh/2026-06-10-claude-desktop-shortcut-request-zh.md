---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude桌面快捷键请求
translated: true
type: note
---

**问题：** 在 Claude 桌面应用中，使用 Cmd+1 / Cmd+2 / Cmd+3 在 Chat、Cowork 和 Code 模式之间切换，这是好的设计吗——并且它已经存在了吗？

**回答：**

好主意——但目前似乎还不存在。有一个开放的功能请求正是针对这一点：用户希望有快捷键（或者至少是菜单项，以便可以分配 macOS 键盘快捷键）来在 Chat、Cowork、Code 以及对话之间切换，因为目前你必须点击侧边栏中的每个模式——而提出请求的人甚至建议使用 Cmd+1/2/3 作为绑定。一个相关问题证实了为什么 macOS 级别的重新映射帮不了你：该应用没有可供绑定快捷键的菜单项（通过检查 app.asar 中的 Electron 菜单定义已核实），因此系统设置中的键盘快捷键无法生效。

所以你的直觉与高级用户的需求一致——Cmd+1/2/3 是标准的标签页界面惯例（浏览器、iTerm、Slack 都这么做），而通过鼠标切换模式对于像你这样的以键盘为中心的工作流程来说是一种摩擦。如果桌面应用的最新版本添加了此功能，那就太好了，但根据最新报告，它仍然是一个开放请求。

桌面应用中确实存在的快捷键：双击 Option 键可调出 Claude 快速输入框（覆盖在你当前工作的内容上），Caps Lock 键用于语音听写（默认禁用）。在 Claude Code 内部（终端）中，按键绑定可以通过 keybindings.json 完全自定义，使用上下文相关的绑定（如 `chat:submit`），无需重启即可应用——但那是 CLI，而非桌面应用的模式切换器。

**在功能推出前的临时方案：** 由于没有可绑定的菜单项，你需要一个 UI 脚本黑客方案——使用 Hammerspoon 或 Karabiner 通过无障碍 API 点击侧边栏元素：

```lua
-- Hammerspoon：通过点击 Claude.app 中的侧边栏位置进行粗略的模式切换
local function clickClaudeSidebar(y_offset)
  local app = hs.application.find("Claude")
  if not app then return end
  app:activate()
  local win = app:mainWindow():frame()
  hs.eventtap.leftClick({x = win.x + 40, y = win.y + y_offset})
end

hs.hotkey.bind({"cmd"}, "1", function() clickClaudeSidebar(80)  end) -- Chat
hs.hotkey.bind({"cmd"}, "2", function() clickClaudeSidebar(120) end) -- Cowork
hs.hotkey.bind({"cmd"}, "3", function() clickClaudeSidebar(160) end) -- Code
```

虽然脆弱（坐标会在 UI 更新时失效），但功能可用。更好的做法：给 GitHub issue (#18818) 点赞，推动其优先级提升。

**参考资料：**

- [Issue #18818: 添加快捷键在 Chat、Cowork、Code 之间切换](https://github.com/anthropics/claude-code/issues/18818)
- [Issue #38447: 用于切换对话的键盘快捷键](https://github.com/anthropics/claude-code/issues/38447)
- [导航 Claude 桌面应用 — claude.com](https://claude.com/resources/tutorials/navigating-the-claude-desktop-app)
- [Claude Code 按键绑定文档](https://code.claude.com/docs/en/keybindings)