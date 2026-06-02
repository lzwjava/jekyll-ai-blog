---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 自动展开 OpenClaw 工具输出
translated: true
type: note
---

**问题：** 如何让 OpenClaw 自动展开工具输出，而不是需要逐个点击？

**回答：**

OpenClaw（开源个人 AI 助手框架）目前没有内置的全局设置来默认自动展开 UI 中的所有工具输出部分。工具结果（尤其是来自 `exec`、`browser`、文件读取等命令的较长输出）通常显示为折叠状态，以保持聊天窗口整洁，您需要逐个点击查看完整内容。

以下是基于当前版本（截至 2026 年 3 月）的实用变通方法和选项：

1. **使用 TUI（Terminal User Interface）代替 Web UI**
   终端界面（`openclaw tui` 或 `openclaw tui chat`）通常会完全展开工具输出，或以更可滚动/可读的格式显示，而不会折叠行为。
   许多用户在大量使用工具时更喜欢它，因为它完全避免了点击展开的麻烦。
   以此方式运行：
   ```
   openclaw tui chat
   ```
   或直接在终端模式下开始聊天。

2. **要求 agent 总结或内联重要部分**
   在您的 prompt 或 `AGENTS.md` / `SOUL.md` 中添加指令，强制 agent 将工具结果的关键部分直接包含在消息中，而不是依赖可折叠块。
   示例 prompt 添加：
   - "Always inline the most important 10–20 lines of tool output directly in your reply. Do not rely only on the collapsed tool card."
   - "For every tool call result, show a concise summary + the full relevant output without requiring expansion."

   这不会展开 UI 卡片，但使信息无需点击即可可见。

3. **检查最新版本中的 UI 改进**
   最近的版本（例如 2026.3.13）为聊天输入文本区域添加了自动展开行为，表明团队正在改进 UX。
   目前还没有特定的“auto-expand tool outputs”功能，但请关注 GitHub releases 或频繁运行 `openclaw update` —— 这种改进可能在不久的将来补丁中到来。

4. **自定义主题 / 浏览器扩展 / userscript（高级）**
   如果您使用 web UI：
   - 编写一个小型浏览器 userscript/Tampermonkey 脚本，在页面加载或变更时自动点击工具卡片的展开按钮。
   - 或使用开发者工具覆盖 CSS（例如移除折叠部分上的 `display: none` 或 `max-height`）。

   这不是官方的，并且在更新后容易失效。

5. **请求此功能**
   该项目在 GitHub (https://github.com/openclaw/openclaw) 上非常活跃。
   打开一个 issue 或为现有 issue +1，请求“auto-expand tool output cards”或“web UI 中工具结果的持久展开状态”。维护者对 UX 反馈响应迅速。

**简短回答：** 目前没有直接的配置/标志——切换到 TUI 以获得最佳体验，或提示 agent 内联更多内容。

**参考：**

- [https://github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
- [https://docs.openclaw.ai/tools](https://docs.openclaw.ai/tools)
- [https://github.com/openclaw/openclaw/releases](https://github.com/openclaw/openclaw/releases)
