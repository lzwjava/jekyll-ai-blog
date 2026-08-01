---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 无llama服务器，可用9.5 GB
translated: true
type: note
---

**不，llama-server 没有在运行。** 没有任何匹配 `llama` 的进程。唯一的 AI 守护进程是 `ollama serve`（PID 3339），并且它处于空闲状态——未加载到 GPU 上。

当前 GPU 状态（RTX 4070，12 GB）：

| | MiB |
|---|---|
| 已用 | 2367 |
| **可用** | **9473** |

而占用的 2.3 GB **不是** AI 相关的——全部是桌面/图形进程：
- Xorg：1430 MiB（占用最大）
- warp-terminal：204 MiB
- zed-editor：191 MiB
- 浏览器 / gnome-shell / nautilus 等：其余部分

因此，对你的使用场景来说，没有什么需要杀掉的进程——你实际上有 **约 9.5 GB 可用空间**，这非常充足。你的 large-v3 fp16 转录只需要约 3.2 GB（如果使用 `--compute-type int8`，则只需约 1.1 GB）。`--low-memory` 重写方案可以轻松满足。

如果你仍然想要更多余量，唯一有价值的操作是关闭浏览器/zed/warp-terminal 的标签页（这些是占用显存的桌面应用），但这对于 whisper 运行来说并不是必需的。