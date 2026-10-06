---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 运行在CPU回退下的llama-server
translated: true
type: note
---

完成。以下是摘要：

## 找到之前的设置
从上次 pi 会话（10月4日）中，llama.cpp 是作为一个名为 `llama` 的 tmux 会话运行的，使用的是 **llama-b11344 CUDA 捆绑包**（而不是 `~/projects/llama.cpp` 源码构建）。具体命令是：

```bash
tmux new-session -d -s llama -x 200 -y 50 \
  'cd ~/projects/llama-b11344 && LD_LIBRARY_PATH=. \
   ./llama-server -m /home/lzw/models/qwen2.5-1.5b-instruct-q4_k_m.gguf \
   -ngl 99 -t 4 --host 0.0.0.0 --port 8080 2>&1 | tee ~/llama-server.log'
```

## 重新运行 — 状态：✅ 运行中

- **tmux 会话**：`llama`（创建于 23:13）
- **端点**：`http://0.0.0.0:8080` — 正在监听，pid 4670
- **健康检查**：`{"status":"ok"}`
- **模型**：Qwen2.5-1.5B-Instruct Q4_K_M
- **推理测试**：响应 `Hello!`
- **速度**（CPU）：约 131 t/s 提示，约 76 t/s 生成

⚠️ 注意：传入了 `-ngl 99`，但 Tesla M40（Maxwell sm_52）**不**受 CUDA 12.8 构建支持（该构建仅提供 sm_120a 内核），因此会静默回退到 CPU。这与之前所有运行一致。如果您想要实际的 GPU 卸载，需要使用面向 sm_52 的 CUDA 架构从源码构建 llama.cpp（`~/projects/llama.cpp` 下的源码树可用）。

日志：`~/llama-server.log`。使用 `tmux a -t llama` 重新连接。