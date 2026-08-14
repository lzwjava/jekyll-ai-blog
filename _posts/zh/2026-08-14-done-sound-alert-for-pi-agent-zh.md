---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 智能体声音提示完成
translated: true
type: note
---

一切正常。以下是我构建的内容。

## 摘要

我创建了一个 pi 扩展，当代理完成一轮操作并等待输入时，它会播放提示音。

**文件：** `/home/lzw/.pi/agent/extensions/done-sound.ts`

### 工作原理

- 它挂钩了 **`agent_settled`** 事件。根据 pi 文档，这是“代理真正完成”的正确挂钩——与 `agent_end`（捆绑的 `notify.ts` 示例使用的挂钩）不同，`agent_settled` 只在所有重试、自动压缩以及队列中的引导/后续消息处理完毕后触发*一次*。这样就不会在工作过程中产生多余的提示音。
- 当状态稳定时，它会自动检测可用的 Linux 播放器（`pw-play` → `paplay` → `ogg123` → `aplay` → `ffplay` → `mpv` → `vlc`），并播放默认音效（`/usr/share/sounds/freedesktop/stereo/complete.oga`），同时在 GNOME/Yaru 音效主题之间进行回退。
- 它以**分离**方式（`child.unref()`）启动播放器，因此不会阻塞 pi 或保持进程存活，并会静默处理错误（音效播放为尽力而为）。
- 在 `print` 模式（`-p`）下会跳过，因为此时没有人类在等待。

### 新增命令

- `/done-sound` — 播放测试提示音
- `/done-sound on` / `/done-sound off` — 为当前进程启用/禁用
- `/done-sound status` — 显示当前状态、音效文件和播放器

### 配置（可选环境变量）

- `PI_DONE_SOUND_FILE` — 自定义音效文件的路径
- `PI_DONE_SOUND_CMD` — 完整的自定义播放命令，例如 `aplay /custom/done.wav`（覆盖文件检测）
- `PI_DONE_SOUND_ENABLED=0` — 启动时禁用

### 验证

我已确认该模块能够在 jiti（pi 的加载器）下加载，并注册了 `agent_settled` 处理程序以及 `/done-sound` 命令，同时 `pw-play` 和 `complete.oga` 确实可以在你的系统上播放。

### 激活方式

由于它位于 `~/.pi/agent/extensions/`（全局自动发现目录）中，你可以**重启 pi**，或者在运行的会话中执行 **`/reload`**。之后只需与 pi 对话——当它完成响应时，你就会听到提示音。运行 `/done-sound` 立即测试，或运行 `/done-sound status` 确认检测到的播放器。

想要不同的音效（例如自定义提示音），或者在每次轮次完成时（每个 `turn_end`）也触发播放，而不仅仅是在完全稳定后？我可以进行调整。
