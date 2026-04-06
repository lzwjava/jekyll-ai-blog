---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 更新Llama.cpp的可用方案
translated: true
type: note
---

2025年10月 — 这版本实在太旧了。Qwen 3.5的发布时间更晚。当前git fetch失败是因为这台服务器访问GitHub速度过慢。

老大，核心问题是这台服务器访问GitHub极慢（约30KB/秒）。有两个解决方案：

1. **从您的笔记本电脑更新llama.cpp** — 克隆/拉取最新版本并编译，新版将支持`qwen35`架构
2. **按我先前的建议**，直接从您的笔记本电脑通过SCP传输Ollama二进制文件

无论哪种方式，模型文件都已下载就绪——我们只需要能识别`qwen35`架构的新版引擎。您倾向于哪种方案？