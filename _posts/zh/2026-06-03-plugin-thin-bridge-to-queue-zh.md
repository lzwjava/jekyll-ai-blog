---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 插件薄桥到队列
translated: true
type: note
---

已完成。以下是变更内容：

**之前**（v1.0.0）：`/note` 直接导入了 `ww.note.create_note_from_clipboard` 和 `ww.github.gitmessageai`，通过 LLM 生成标题，创建笔记文件，运行 pre-commit，git commit + push——所有这些都内联在插件中。

**之后**（v2.0.0）：`/note` 执行 3 件事：
1. 提取助手响应文本，去除推理标签
2. 将其复制到剪贴板（`pbcopy`/`xclip`）
3. 运行 `ww note`（子进程），读取剪贴板 → 排队到 `~/.config/ww/note_queue.json`
4. 检查 `ww note watch` 是否正在运行（通过 PID 文件），若未运行则发出警告

实际的笔记创建、LLM 标题生成、git commit + push 均由后台的 `ww note watch` 处理。插件现在只是一个轻量的剪贴板→队列桥接器。

修改的文件：
- `/Users/lzwjava/.hermes/plugins/note/__init__.py` — 从 191 行重写为 176 行，移除了所有 `ww` 内部导入
- `/Users/lzwjava/.hermes/plugins/note/plugin.yaml` — 升级至 v2.0.0，更新了描述

请确保 `ww note watch` 在后台终端中运行，以便笔记能够被处理。