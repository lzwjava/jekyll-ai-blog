---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI存储库扩展与更新
translated: true
type: note
---

完成。以下是摘要：

已将 37 个仓库添加到 repos.json（总数从 62 增加到 99）。所有 99 个仓库均已克隆，并准备好执行 `ww projects update`。

按类别划分的新增仓库：

  ai-models (+6): Qwen2-Audio, Qwen2.5-Math, llama, gemma, transformers, whisper.cpp

  ai-training (+6): ColossalAI, flash-attention, LlamaFactory, LLMs-from-scratch, minbpe, mamba

  ai-inference (+5): vllm, ollama, mlx, ggml, mlx-examples

  ai-apps (+5): LibreChat, litellm, anything-llm, Whisper, facefusion

  ai-agents (+6): OpenHands, autogen, markitdown, browser-use, opencode, gemini-cli

  dev-tools (+3): warp, iclaw, mcp

  infra-network (+6): mihomo, chroma, qdrant, localGPT, quivr, llm-app

重点推荐：

- vllm (★81k) — 高吞吐量推理，服务部署必备
- ollama (★173k) — 本地模型运行器，同类中最受欢迎
- transformers (★161k) — HuggingFace 模型框架，基础性工具
- LlamaFactory (★72k) — 统一微调框架，支持 100 多种 LLM
- browser-use (★96k) — AI 代理的网页自动化工具
- OpenHands (★75k) — AI 驱动的软件开发
- litellm (★49k) — 统一的 LLM API 代理
- markitdown (★134k) — 文件转 Markdown 转换工具
- mihomo — 你的代理核心，已在 ~/projects 中
- flash-attention (★24k) — 快速注意力机制实现
