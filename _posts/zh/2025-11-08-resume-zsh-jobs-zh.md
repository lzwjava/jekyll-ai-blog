---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 恢复zsh中被暂停的任务
translated: true
type: note
---

要在 Ghostty 的 zsh 中恢复被暂停的任务（比如你用 Ctrl+Z 暂停的 `bundle exec jekyll serve --incremental` 命令），请在同一终端会话中按以下步骤操作：

1. 列出所有后台/暂停的任务以确认目标任务存在：
   ```
   jobs
   ```
   这将显示类似 `[1]+  已暂停   bundle exec jekyll serve --incremental` 的信息。

2. 将其恢复到前台运行（该任务将再次接管你的终端）：
   ```
   fg
   ```
   - 如果有多个任务，请使用 `fg %1` 指定目标任务（将 `1` 替换为 `jobs` 输出中对应的任务编号）。

若希望改为在后台运行该任务（以便在服务运行期间同时使用终端执行其他操作），请使用 `bg %1`（同样需要替换为实际的任务编号）。

恢复后，Jekyll 应该会从中断处继续运行。如果进程出现卡顿或报错，可能需要使用 `kill %1` 终止该任务后重新启动。
