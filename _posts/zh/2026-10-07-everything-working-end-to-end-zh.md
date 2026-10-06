---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 端到端一切正常
translated: true
type: note
---

现在一切都端到端地正常工作了。🎉

## ✅ 最终结果

| 项目 | 状态 |
|---|---|
| llama.cpp + CUDA (sm_52/MMQ) 为 M40 构建 | ✅ `~/projects/llama.cpp` |
| Qwen2.5-14B-Instruct Q5_K_M（10.5GB）已下载 | ✅ `~/projects/models/` |
| llama-server 正在运行（已分离，PID 2785） | ✅ 端口 8080 |
| 自动挂起已永久禁用 | ✅ systemd 屏蔽 + GNOME 关闭 |
| API 测试 | ✅ `"Hi there!"` |

## 📊 性能（实测）

| 指标 | 速度 |
|---|---|
| 提示词处理 | **38.5 tok/s** |
| 生成（14B Q5_K_M） | **13.6 tok/s** |

## 🌐 如何从网络上的任何机器使用

**Web 聊天 UI**（浏览器）：
```
http://192.168.1.137:8080
```

**兼容 OpenAI 的 API**（适用于任何期望 OpenAI 的工具）：
```bash
curl http://192.168.1.137:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}],"max_tokens":100}'
```
端点：`http://192.168.1.137:8080/v1` · 模型名称 = GGUF 路径

**终端聊天**（在机器本身上）：
```bash
~/projects/run-chat.sh
```

## 📁 项目结构（按要求，位于 `~/projects/`）
```
~/projects/
├── llama.cpp/          # 源码 + 构建（二进制文件在 build/bin/）
├── models/             # GGUF 模型分片
├── run-chat.sh         # 交互式 CLI 聊天
└── run-server.sh       # API + Web 服务器
```

## 🔜 可选的后续步骤（尽管说）

1. **开机自启动** — 我可以创建一个 `systemd` 服务，让 llama-server 在每次重启后自动启动。
2. **更大的模型** — 使用 24GB 显存，你可以运行 Qwen2.5-**32B**-Q4（约 20GB），速度约 2–4 tok/s，或 **Mixtral 8x7B Q3**。
3. **whisper.cpp** — 在同一块 GPU 上添加快速的语音转文字功能。
4. **限制 M40 功耗**（`sudo nvidia-smi -pl 150`）— 减少对旧电源的压力，速度损失可忽略不计。

⚠️ 注意：服务器目前**没有 API 密钥**，并允许来自任何地方的 CORS —— 在局域网内没问题，但不要将 8080 端口暴露到互联网。

需要我设置 **systemd 自启动服务**，让它始终可用吗？