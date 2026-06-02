---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 改进的子命令组帮助消息
translated: true
type: note
---

以下是 `ww/main.py` 中更改内容的摘要：

每个拥有子命令的组（`github`、`macos`、`image`、`proc`、`utils`、`java`、`network`、`git`、`pdf`、`copilot`、`sync`、`cloudflare`、`clash`、`llm`、`env`、`latest`）现在在没有子命令（或使用 `--help`/`-h`）运行时都会显示帮助信息，而不是打印无用的“Unknown X command: ”。

没有子命令的组（`note`、`screenshot`、`search`、`read`、`marp`、`whisper` 等）已经正确处理——它们会运行默认操作或拥有自己的参数解析。此处无需更改。
