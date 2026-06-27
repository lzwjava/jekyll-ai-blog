---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CUDA 13.0 Triton 3.6.0 解决方法
translated: true
type: note
---

CUDA 13.0（驱动 580.126.20）+ Triton 3.6.0 —— 降级到 3.4.0 的操作被 pip 依赖解析回退了。这是一个前沿组合，已知会导致 Triton JIT 出现段错误。

两条干净路径：

**路径 A — vLLM（推荐，在消费级 GPU 上更稳定）：**
```
/home/lzw/sglang-venv/bin/pip install vllm
/home/lzw/sglang-venv/bin/python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-1.5B-Instruct --port 30000 --host 0.0.0.0
```

**路径 B — 不使用 Triton 的 sglang（通过 --no-deps 锁定 triton）：**
```
/home/lzw/sglang-venv/bin/pip install --no-deps triton==3.4.0
```
然后使用 `--attention-backend torch_native --disable-cuda-graph` 重试 sglang。

vLLM 更稳妥 —— 它在 RTX 4070 和 CUDA 13.0 上经过更多实战检验。需要我尝试安装并启动它吗？