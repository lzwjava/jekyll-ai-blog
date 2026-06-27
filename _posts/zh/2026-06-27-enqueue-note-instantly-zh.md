---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 即时加入笔记
translated: true
type: note
---

已完成。以下是更改的内容：

`/Users/lzwjava/.hermes/plugins/note/__init__.py` — `/note` 现在将任务加入队列，而不是运行完整的流水线。它是即时完成的（仅写入 `~/.config/ww/note_queue.json`），没有 LLM 调用，没有 git 内联操作。

之前：LLM 标题生成 → 文件写入 → git add → commit → push（速度慢，在 pre-commit 钩子上失败）
之后：读取响应 → 写入 JSON → 完成（< 1 秒）

要自动清空队列，你有两个选择：

1. 后台监视器：`ww note watch`（监视队列文件，在有变化时处理）
2. 系统 crontab（你更喜欢的方案）：定期运行 `ww note process`

需要我添加一个系统 crontab 条目，每隔几分钟处理一次队列吗？
