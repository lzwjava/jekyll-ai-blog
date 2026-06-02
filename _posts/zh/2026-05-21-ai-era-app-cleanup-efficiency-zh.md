---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI时代App清理效率
translated: true
type: note
---

问题：在人工智能时代，安装和尝试大量应用，然后使用AI工具高效清理它们——让安装/卸载循环变得更快、更轻松——这正在成为常态吗？

回答：

完全正确，这确实是一种值得明确指出的行为转变。

**旧循环（痛苦）：**

- 安装应用 → 忘记它的存在 → 多年后，神秘的启动项 → 手动寻找卸载说明 → 残留文件散落各处

**AI时代循环（快速）：**

- 自由安装、广泛尝试 → AI扫描启动项、登录项、LaunchAgents、LaunchDaemons → 批量识别无用负担 → 精准清理

Hermes（或类似工具如 [Keka](https://www.keka.io/)、CleanMyMac 等）+ AI 助手 = 清理的阻力骤降。你从“我迟早该清理一下我的 Mac”变成了在一次会话中真正完成清理。

**你的具体清理是合理的：**

- 搜狗输入法 → 冗余，微信输入法已覆盖，且搜狗有大量后台进程
- HP 打印机软件 → 典型的“安装一次，永远运行”问题，即使手动删除应用，LaunchDaemons 也常会残留
- KindlePreviewer → 你现在通过 LLM 阅读，这已是无用负担

**你指出的更深层模式：**

> 人们尝试更多软件，因为清理成本趋近于零

这确实是注意力经济学的一次转变。安装的摩擦早已很低（App Store、Homebrew）。卸载的摩擦此前却很高——残留文件、LaunchAgents、登录项分散在 `/Library`、`~/Library`、`/etc` 中。AI 加系统感知工具将卸载端的摩擦彻底消除。因此，净尝试率随之上升。

这类似于 `git` 降低了分支成本 → 人们更频繁地创建分支。低成本清理 → 人们更自由地安装。

**针对你的 M2 清理会话的实用提示：**

```bash
# 查看所有用户级 LaunchAgents
ls ~/Library/LaunchAgents/

# 查看系统级 LaunchDaemons
ls /Library/LaunchDaemons/

# 查找 HP 相关残留
find /Library ~/Library -name "*HP*" -o -name "*hp*" 2>/dev/null | grep -v ".Trash"

# 查找搜狗残留
find /Library ~/Library -name "*Sogou*" -o -name "*sogou*" 2>/dev/null

# 卸载后，检查还有哪些自动加载项
launchctl list | grep -v com.apple
```

通过 GUI 或 `brew uninstall` 卸载后，始终运行 `find` 命令——HP 和搜狗以残留守护进程而臭名昭著，即使应用已删除，这些进程仍会持续运行。

**核心观点：** 你实际上是在对你的 Mac 应用与你对 LLM 工作流相同的原则——让 AI 做审计，你做决策，快速执行。人类留在判断层，AI 处理侦察。这是正确的分工。
