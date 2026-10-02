---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重启 llama-server 进程
translated: true
type: note
---

你在 `nvidia-smi` 中看到的 `llama-server` 进程（PID 7946）**已不再运行** — 它已退出，因此其端口已关闭。

不过，我看到你在 `~/projects/llama.cpp/` 有 `llama.cpp` 项目。如果你想重启它：

```bash
cd ~/projects/llama.cpp
./llama-server -m /path/to/your/model.gguf --port 8080
```

默认情况下，`llama-server` 监听 **8080 端口**。一旦它运行起来：

- **Web UI**：`http://localhost:8080`
- **OpenAI-compatible API**：`http://localhost:8080/v1/chat/completions`
- **检查是否在监听**：`lsof -i :8080`

你还可以通过 `--port <number>` 指定其他端口。需要我为你创建一个快速启动脚本吗？
