---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 已配置笔记浏览器设置
translated: true
type: note
---

正确的 `.env` 文件位于 `ww` 项目根目录：

  /Users/lzwjava/projects/ww/.env

并且已经在那里设置好了（第 33 行）：

  NOTE_BROWSER_OPEN=false

`ww/env.py` 通过 `dotenv` 加载此 `.env` 文件，而 `note_workflow.py` 使用 `os.getenv("NOTE_BROWSER_OPEN", "true")` 读取它。你无需修改——它已经是 `false` 了。

如果你需要更改，请编辑 `/Users/lzwjava/projects/ww/.env`。`jekyll-ai-blog` 的 `.env` 文件与此设置无关——它仅通过额外的环境加载路径用于 `BASE_PATH`/`SCREENSHOT_DIR`。
