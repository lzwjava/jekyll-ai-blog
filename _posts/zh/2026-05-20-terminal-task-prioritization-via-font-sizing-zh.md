---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 基于字体大小的终端任务优先级排序
translated: true
type: note
---

**问题：** 在终端窗口/会话中使用不同字号能否成为另一种视觉区分多个任务的方式——而不仅仅是窗口位置？

**回答：**

是的，完全正确。在终端多任务处理中，字号是一个未被充分利用的维度。以下是你能做的完整图景：

## 字号作为视觉信号

思路：为不同窗口的字号赋予语义含义。

| 字号 | 用途 |
|------|------|
| 大号（18–24pt） | 主要关注任务——你正在积极编码的内容 |
| 中号（13–14pt） | 副屏——日志、监视器、测试运行器 |
| 小号（9–11pt） | 后台进程——LLM 流式输出、构建 CI、智能体循环 |

你的眼睛无需阅读任何内容就能立刻知道该看哪里。

## 如何为每个窗口设置字号

**iTerm2**（最灵活）：

```bash
# 通过 AppleScript —— 设置当前窗口的字号
osascript -e 'tell application "iTerm2"
  tell current session of current window
    set font size to 18
  end tell
end tell'
```

或者在 iTerm2 中创建**配置文件**（偏好设置 → 配置文件）——每种任务类型一个——每个配置文件有自己的字号、配色方案和徽章。然后使用以下命令启动：

```bash
# 使用特定配置文件打开新窗口
osascript -e 'tell application "iTerm2" to create window with profile "Focus"'
```

**Kitty**（基于配置，速度快）：

```bash
# 在 kitty.conf 或通过远程控制
kitty @ set-font-size 20        # 当前窗口
kitty @ --to unix:/tmp/kitty-focus set-font-size 20  # 特定实例
```

你可以启动带有不同配置的独立 kitty 实例：

```bash
kitty --config ~/.config/kitty/focus.conf &
kitty --config ~/.config/kitty/monitor.conf &
```

**Wezterm**（Lua 脚本，可编程性最强）：

```lua
-- wezterm.lua
local wezterm = require 'wezterm'

return {
  font_size = 14.0,  -- 默认值
  -- 通过事件或窗口装饰覆盖每个窗格
}
```

## 组合字号 + 颜色主题 + 徽章

真正的威力在于叠加信号：

```
窗口 1：大号字体 + 深色主题 + 徽章 "FOCUS"     → 活跃编码
窗口 2：中号字体 + 蓝色主题 + 徽章 "LOGS"      → 流式输出
窗口 3：小号字体 + 暗淡主题 + 徽章 "AGENT"      → 后台 LLM 智能体
```

在 iTerm2 中，徽章显示在每个窗格的右上角——通过以下命令设置：

```bash
printf "\e]1337;SetBadgeFormat=%s\a" $(echo -n "AGENT" | base64)
```

## 我为你工作流建议的布局

考虑到你运行 CLI 智能体（`ww`、`zz`、`iclaw`）+ LLM 流式输出 + 活跃编码：

```
┌─────────────────────────────────┐  ┌──────────────────┐
│  FOCUS（20pt，浅色主题）          │  │ AGENT（10pt，暗淡）│
│  $ vim / claude-code / cursor   │  │ $ ww run loop... │
│                                 │  │ 流式 token       │
├─────────────────────────────────┤  ├──────────────────┤
│  LOGS（12pt，蓝色调）            │  │ BUILD（11pt）     │
│  $ tail -f / pytest -s          │  │ $ gh run watch   │
└─────────────────────────────────┘  └──────────────────┘
```

仅凭字号就能让你一眼看出每个窗口的优先级——无需阅读任何内容。
