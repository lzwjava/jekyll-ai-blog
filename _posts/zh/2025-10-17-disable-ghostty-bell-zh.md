---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 禁用Ghostty的响铃通知
translated: true
type: note
---

### Ghostty 的“通知标签页”是什么？

在 Ghostty（一款 GPU 加速的终端模拟器）中，“通知标签页”很可能指的是视觉响铃通知功能。当终端中运行的命令或应用程序发送响铃字符（`\a`）时（例如来自长时间运行的进程或错误），Ghostty 会在受影响的标签页或窗口标题前添加一个铃铛表情符号（🔔）。这作为一种微妙的提醒，能将你的注意力重新吸引到该标签页，特别是在终端未聚焦或你正在其他标签页中工作时。这是 Ghostty 响铃处理系统的一部分，旨在提供非侵入式通知，而不仅仅依赖音频或系统弹窗。

此行为在 `bell-features` 配置下默认启用，特别是 `title` 选项。它对于诸如后台作业完成等工作流很有帮助，但在标签栏中可能会让人觉得像是不必要的“通知”。

### 如何禁用它

要取消或禁用此响铃标题通知（以及可能的其他响铃行为），请编辑你的 Ghostty 配置文件。默认位置在 Linux 上是 `~/.config/ghostty/config`，在 macOS 上是 `~/Library/Application Support/com.mitchellh.Ghostty/config`。

1. 在你喜欢的编辑器中打开配置文件。
2. 添加或修改以下行以专门禁用标题表情符号（同时保留其他响铃功能，如注意力请求）：

    ```
    bell-features = no-title
    ```

    - 这会从标签页标题中移除 🔔，但允许其他响铃效果（例如系统音频或窗口高亮）。

3. 要更彻底地禁用（无标题表情符号、无注意力请求等），请使用：

    ```
    bell-features = false
    ```

    - 这会完全关闭所有响铃功能。

4. 保存文件并在 Ghostty 中重新加载配置：
    - 按 `Cmd/Ctrl + Shift + ,`（或在另一个终端中运行 `ghostty --reload-config`）。
    - 新窗口/标签页将使用更新后的设置；现有的窗口/标签页可能需要重启。

如果这不是你指的确切通知（例如，如果是应用内提示如“已复制到剪贴板”或来自终端应用的桌面通知），你也可以禁用它们：

- 对于应用内提示（仅限 Linux GTK）：`app-notifications = false`
- 对于来自终端应用的桌面通知：`desktop-notifications = false`

可以通过运行触发响铃的命令进行测试，例如 `echo -e '\a'`。

[Ghostty 配置参考](https://ghostty.org/docs/config/reference)
[Ghostty 响铃功能讨论](https://github.com/ghostty-org/ghostty/discussions/3242)
