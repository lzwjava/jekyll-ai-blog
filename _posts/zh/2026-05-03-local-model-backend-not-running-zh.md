---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 本地模型后端未运行
translated: true
type: note
---

错误信息很明确：**本地模型后端未运行**。

系统尝试调用 `openai/gpt-oss-120b`，访问地址 `http://localhost:1234/api/v1/chat`，但收到 `Connection refused` 响应 —— 端口 1234 上没有监听的模型服务。

根据 README 说明：
> 需要有一个本地 OpenAI 兼容聊天后端，可通过 `http://localhost:1234/api/v1/chat` 访问

您需要启动一个本地推理服务器（例如 **LM Studio**、**Ollama**、**llama.cpp server**、**vLLM**），并确保：

- 监听 `http://localhost:1234`
- 提供 `/api/v1/chat` 路径（OpenAI 兼容）
- 运行已配置的模型（`qwen3.5-9b-mlx`、`openai/gpt-oss-120b` 等）

**快速检查** —— 您是否安装了 LM Studio 或 Ollama？如果已安装，请启动并加载模型，之后会话创建功能即可正常工作。
