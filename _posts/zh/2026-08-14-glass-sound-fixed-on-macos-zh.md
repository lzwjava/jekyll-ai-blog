---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS上玻璃声音已修复
translated: true
type: note
---

已修复。刚才你应该听到“Glass”音效的。

## 问题原因

这个扩展原本只支持 **Linux**。在 macOS 设备上：

- 默认音频文件 `/usr/share/sounds/freedesktop/stereo/complete.oga` 不存在。
- Linux 的播放器（`pw-play`、`paplay`、`aplay` 等）不在 PATH 环境变量中——只有 Homebrew 安装的 `ffplay`/`vlc` 可用，但由于传递的是不存在的文件路径，它们静默失败（扩展设计上会吞掉所有错误）。

结果：`detectPlayer()` 返回 `ffplay`/`vlc`，`resolveSoundFile()` 返回缺失的 Linux 文件，进程启动失败，因此听不到任何声音。

## 我对 `pi/agent/extensions/done-sound.ts` 的修改

1. 新增 `isMacOS = process.platform === "darwin"` 检测。
2. 将 macOS 原生播放器 **`afplay`** 置于播放器候选列表首位（仅限 macOS），排在 Linux 播放器之前。`afplay` 随 macOS 系统自带，原生支持 `.aiff`/`.wav`/`.mp3`/`.m4a` 格式。
3. 根据平台拆分音频文件的回退链：
   - **macOS：** `/System/Library/Sounds/Glass.aiff` → `Hero` → `Ping` → `Submarine` → `Tink`
   - **Linux：** 保持原有的 freedesktop/Yaru 链（未修改）。
4. 默认文件常量现在在 macOS 上指向 `Glass.aiff`，其他平台保持原有 Linux 文件。

Linux 行为完全不变；macOS 现在开箱即用。

## 在 Pi 中测试

重新加载扩展（重启 Pi 或使用 `/reload` 命令，如果可用），然后运行：

```
/done-sound          # 播放测试音效
/done-sound status   # 应显示：enabled | file: /System/Library/Sounds/Glass.aiff | player: afplay
```

## 可选自定义

如果想更换音效，可以在 `pi/agent/settings.json` 的环境变量或 shell 中设置：

```
PI_DONE_SOUND_FILE=/System/Library/Sounds/Ping.aiff
```

或使用自定义命令：

```
PI_DONE_SOUND_CMD=afplay /System/Library/Sounds/Hero.aiff
```

需要我将 `PI_DONE_SOUND_FILE` 写入 `pi/agent/settings.json` 以实现自动设置吗？或者选择其他默认音效（例如 `Hero` 或 `Ping`）？
