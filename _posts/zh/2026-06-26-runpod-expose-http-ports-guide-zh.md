---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RunPod 暴露 HTTP 端口指南
translated: true
type: note
---

问题：如何在 RunPod 中配置“暴露 HTTP 端口（最多 10 个）”？

答案：

“暴露 HTTP 端口”字段告诉 RunPod 容器内的哪些端口应可通过其代理通过 HTTP 访问。你需要输入一个逗号分隔的端口号列表（最多 10 个）。

工作原理：

- 输入你的应用监听的端口，例如 `8888,7860,8000`。
- RunPod 的代理将每个端口映射到一个公共 URL：`https://<​POD_ID>-<​PORT>.proxy.runpod.net`
- 代理终止 TLS 并通过 HTTP 转发到你的容器，因此你的应用只需在相应端口上绑定纯 HTTP。

关键要求——绑定到 `0.0.0.0`，而不是 `localhost`：

```bash
# Jupyter
jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root

# 常见的应用服务器
python -m http.server 8000 --bind 0.0.0.0
# FastAPI / uvicorn
uvicorn app:app --host 0.0.0.0 --port 8000
# Gradio
demo.launch(server_name="0.0.0.0", server_port=7860)
```

如果你绑定到 `127.0.0.1`，代理将无法访问，你会收到 502 错误。

典型配置：

| 字段 | 值 |
|-------|-------|
| Expose HTTP Ports | `8888,7860,8000` |
| Expose TCP Ports | `22` (SSH — 使用直接 TCP，而非 HTTP 代理) |

注意：

- HTTP 端口通过 `*.proxy.runpod.net` 反向代理（适用于 Web UI、API、笔记本）。
- TCP 端口（如 SSH `22`）会获得直接的 `<IP_ADDRESS>:<PORT>` 映射——该字段用于 SSH 或任何非 HTTP 服务。
- 代理在容器端仅支持 HTTP/WebSocket。对于原始 TCP 服务（Redis、Postgres、自定义协议），请使用 Expose TCP Ports。
- 你可以在模板配置中或部署 pod 时设置此选项；对于正在运行的 pod，通常需要编辑模板并重新部署以更改暴露的端口。
- 代理具有空闲/超时行为（约 100 秒），可能会中断长时请求——对于流式传输或长时间任务，建议使用 TCP 端口或保持连接活跃。

参考链接：

- [RunPod 文档 — 暴露端口](https://docs.runpod.io/pods/configuration/expose-ports)
- [RunPod 文档 — 连接到 Pod](https://docs.runpod.io/pods/connect-to-a-pod)