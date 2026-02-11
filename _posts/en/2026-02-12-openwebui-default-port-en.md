---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Open WebUI Default Port Guide
translated: false
type: note
---

Question: What is the default port for Open WebUI?

Answer: 

The **default port** for **Open WebUI** (the application itself) is **8080**.

- When running via Docker (the most common method), the container listens on port 8080 internally.
  - Typical command: `docker run -d -p 3000:8080 ...`
  - This maps host port 3000 (or any port you choose) → container port **8080**.
  - You access it at `http://localhost:3000` (or whatever host port you mapped).

- When running directly via Python/pip (`open-webui serve`), it also listens on port **8080** by default.
  - You access it at `http://localhost:8080`.

You can change the port using the `PORT` environment variable (e.g., `-e PORT=9999` in Docker) or the `--port` flag when using the `serve` command.

The version shown in your message (v0.5.10) is quite old — current versions (as of 2026) still use **8080** as the default internal/container port.

References:  

- [https://docs.openwebui.com/getting-started/quick-start](https://docs.openwebui.com/getting-started/quick-start)
- [https://docs.openwebui.com/getting-started/env-configuration](https://docs.openwebui.com/getting-started/env-configuration)
- [https://github.com/open-webui/open-webui](https://github.com/open-webui/open-webui)