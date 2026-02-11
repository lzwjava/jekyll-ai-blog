---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Open WebUI 默认端口指南
translated: true
type: note
---

Question: Open WebUI 的默认 Port 是多少？

Answer: 

**Open WebUI**（应用程序本身）的 **Default Port** 是 **8080**。

- 当通过 Docker 运行（最常见的方法）时，Container 内部监听 8080 Port。
  - 典型命令：`docker run -d -p 3000:8080 ...`
  - 这会将 Host Port 3000（或你选择的任何端口）映射到 Container Port **8080**。
  - 你可以通过 `http://localhost:3000`（或你映射的任何 Host Port）进行访问。

- 当直接通过 Python/pip (`open-webui serve`) 运行时，它默认也会监听 **8080** Port。
  - 你可以通过 `http://localhost:8080` 进行访问。

你可以使用 `PORT` 环境变量（例如在 Docker 中使用 `-e PORT=9999`）或在执行 `serve` 命令时使用 `--port` 标志来更改端口。

你消息中显示的版本 (v0.5.10) 比较旧 —— 截至 2026 年的当前版本仍然使用 **8080** 作为默认的 Internal/Container Port。

References:  

- [https://docs.openwebui.com/getting-started/quick-start](https://docs.openwebui.com/getting-started/quick-start)
- [https://docs.openwebui.com/getting-started/env-configuration](https://docs.openwebui.com/getting-started/env-configuration)
- [https://github.com/open-webui/open-webui](https://github.com/open-webui/open-webui)