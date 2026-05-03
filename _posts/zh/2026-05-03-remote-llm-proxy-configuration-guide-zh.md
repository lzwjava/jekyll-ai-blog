---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 远程大语言模型代理配置指南
translated: true
type: note
---

## 已完成配置

**问题：** Tree of Thought 使用自定义API格式 `{model, system_prompt, input}` — 而 llama.cpp 期望标准的 OpenAI 格式 `{messages:[...]}`。

**解决方案：** 一个由三部分组成的链式结构：

```
ToT (local:8000) → SSH 隧道 :1234 → 远程代理 :8088 → llama-server :8080
```

**远程服务器上的文件 (192.168.1.36)：**
- `~/tot_proxy.py` — 将 ToT 格式转换为 OpenAI 格式，监听端口 :8088
- 运行着 `DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf` 模型的 llama-server，监听端口 :8080
- 日志文件：`~/llama8b.log`, `~/tot_proxy.log`

---

## 切换模型

通过 SSH 连接到远程服务器并重启 llama-server 以加载不同的 `.gguf` 模型文件：

```bash
ssh lzw@192.168.1.36
pkill llama-server
nohup /home/lzw/projects/llama.cpp/build/bin/llama-server \
  -m /home/lzw/projects/llama.cpp/models/DeepSeek-R1-Distill-Qwen-32B-Q2_K.gguf \
  --host 0.0.0.0 --port 8080 -ngl 99 \
  > ~/llama8b.log 2>&1 &
```

远程服务器上可用的模型：
- `deepseek-r1-distill-qwen-1.5b-q4_0.gguf` — 体量小/速度快
- `DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf` — **当前推荐使用**
- `DeepSeek-R1-Distill-Qwen-32B-Q2_K.gguf` — 大模型，可能占用 12GB 内存

---

## 系统重启后进行完整重启

```bash
# 在远程服务器上执行
ssh lzw@192.168.1.36
nohup /home/lzw/projects/llama.cpp/build/bin/llama-server \
  -m /home/lzw/projects/llama.cpp/models/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf \
  --host 0.0.0.0 --port 8080 -ngl 99 > ~/llama8b.log 2>&1 &
nohup python3 ~/tot_proxy.py > ~/tot_proxy.log 2>&1 &

# 在本地 Mac 上（新终端中）执行
ssh -f -N -L 1234:localhost:8088 lzw@192.168.1.36
```

前端访问地址保持为 `http://localhost:1234/api/v1/chat`，所有模型字段均设置为 `local`。