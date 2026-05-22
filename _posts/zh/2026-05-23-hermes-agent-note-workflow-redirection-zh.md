---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes-Agent 笔记工作流重定向
translated: true
type: note
---

我们修改了 `ww note` 命令，将其重定向到 hermes-agent 的 `/note` 插件：

1. 首次尝试：完全屏蔽 `ww note`，需要 `--manual` 标志才能运行。但失败了，因为 `_pop_subcmd()` 将 `--manual` 当作子命令名称处理。

2. 第二次尝试：将屏蔽改为交互式提示——“继续使用独立 note 工作流？[Y/n]”。虽然可行，但你希望更简洁的用户体验。

3. 最终版本：提示改为“按 Enter 继续，按 Ctrl+C 退出...”——无需解析 Y/n，只需按 Enter 继续或按 Ctrl+C 中止。

最终效果：运行 `ww note` 现在会显示一条提示，指向 hermes-agent 中的 `/note`，然后等待按 Enter 确认，再继续执行原有的独立工作流。`ww note log` 和 `ww note obfuscate` 等子命令不受影响。