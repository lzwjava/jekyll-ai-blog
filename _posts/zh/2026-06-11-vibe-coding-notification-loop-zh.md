---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 氛围编码通知循环
translated: true
type: note
---

是的，这样可行——但定时器意味着*你*需要轮询代理。更好的做法是：让任务在完成时通知*你*，这样你就不必按计划切换上下文了。

在你的 MacBook Air 上，为任何长时间运行的命令附加一个通知：

```bash
# macOS native notification + sound when done
long_task && osascript -e 'display notification "Task done" with title "Copilot" sound name "Glass"'

# or just an audible ping
long_task; say "done"
```

如果代理在 Warp 中运行，Warp 也内置了针对未聚焦标签的“命令完成时通知”功能（设置 → 功能），因此任何超过几秒的命令都会自动触发 macOS 通知——每个任务零设置。

对于你无法包装的代理（例如在 IDE 中运行的 Copilot），你的时钟应用延迟提醒是一个合理的后备方案，不过一个 10 分钟 `sleep` 单行命令可以让你留在终端中：

```bash
sleep 600 && say "check copilot"
```

是的，用阅读 AI 新闻来填补这段间隙也不错，但这是经典的注意力陷阱：10 分钟的浏览常常变成 25 分钟，而代理在第 7 分钟就已经完成了。通知方法将其颠倒过来：自由阅读，在任务结束的那一刻被中断。这是更高吞吐量的 vibe coding 循环——你希望代理的空闲时间为零，而不是你的。

鉴于你制作 CLI 代理，还有一个值得构建的模式：让 `ww`/`zz` 在完成时向本地 webhook 或 `terminal-notifier` 发送通知，这样你堆栈中的每个长时间任务都统一地提醒你。