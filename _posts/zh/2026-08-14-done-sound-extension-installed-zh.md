---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 已安装完成音效扩展
translated: true
type: note
---

已安装。`done-sound` 扩展现已位于 `~/.pi/agent/extensions/done-sound.ts`（实时配置），与现有的 `note` 扩展并存。

关于该扩展在 macOS 上的行为说明：
- 当代理真正进入稳定状态（`agent_settled` 事件）且队列中的后续操作执行完毕后，会播放提示音。
- 默认使用 Linux 音频路径和播放器。在您的 Mac 上建议通过以下方式覆盖：
  - `PI_DONE_SOUND_FILE`（例如 `/System/Library/Sounds/Glass.aiff`）
  - `PI_DONE_SOUND_CMD`（例如 `afplay /System/Library/Sounds/Glass.aiff`）—— 此设置将完全绕过播放器自动检测功能，这是在 macOS 上最简便可靠的方案。
- 您可以通过以下命令进行测试/切换：`/done-sound`、`/done-sound on|off`、`/done-sound status`。

请重启 pi（或重新加载会话）以使新扩展生效。