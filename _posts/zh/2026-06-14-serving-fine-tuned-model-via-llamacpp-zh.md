---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过 llama.cpp 服务微调模型
translated: true
type: note
---

以下是微调模型服务的完整故事：

**问题：** 你的 ollama 二进制文件已损坏（段错误，缺少 ELF 节头）。重新安装 ollama 修复了问题，但你更想要 llama.cpp。

**我做了什么：**

1. **找到 llama.cpp** 已构建在 ~/projects/llama.cpp/ 目录下，并且 `llama-server` 和 `llama-cli` 二进制文件均已就绪。

2. **启动 llama-server**，使用以下标志：
   - `--model` — 你的 Q4_K_M GGUF 模型（2.4GB）
   - `--host 0.0.0.0 --port 8080` — 在所有接口上可访问
   - `--n-gpu-layers 999` — 将所有层卸载到你的 RTX 4070
   - `--ctx-size 4096` — 与训练时的 max_seq_len 一致
   - `--threads $(nproc)` — 使用所有 CPU 核心处理非 GPU 工作

3. **验证其工作正常** — 健康检查返回 `{"status":"ok"}`，测试提示（"The Art of Slow Living"）生成了连贯的博客风格文章，速度约 140 tokens/sec。

**你的服务设置：**

```
GGUF 文件 (2.4GB, Q4_K_M)
    → localhost:8080 上的 llama-server
    → 兼容 OpenAI 的 API
    → 在 RTX 4070 上完全 GPU 卸载
```

**端点：**

- `POST http://localhost:8080/v1/chat/completions` — 可直接替代 OpenAI
- `POST http://localhost:8080/completion` — 纯文本补全
- `GET http://localhost:8080/health` — 状态检查

**使用方法：**

```bash
# 聊天补全（类似 OpenAI API）
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"你的博客标题"}],"max_tokens":500}'

# 或者将任意兼容 OpenAI 的客户端指向 http://localhost:8080/v1
```

**停止服务：** `kill 1838246`