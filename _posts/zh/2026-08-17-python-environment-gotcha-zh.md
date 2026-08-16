---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python环境陷阱
translated: true
type: note
---

这台机器上所需的一切都已就绪——唯一棘手的是 Python 环境。以下是具体情况以及运行方法：

## 关键陷阱：使用哪个 Python

- `minisgl` 0.1.0 已从本仓库以**可编辑**模式安装（`/usr/local/lib/python3.12/dist-packages` → `/mnt/data/mini-sglang`），因此无需安装步骤。
- **系统** site-packages 中包含兼容组合：`torch 2.9.1 + sgl_kernel 0.3.21 + flashinfer 0.6.16`。
- 你的**用户** site-packages（`~/.local`）中的 `torch 2.11.0` 会遮蔽系统版本，导致 `sgl_kernel` 出错（未定义符号 `c10_cuda_check_implementation`）。

因此**不要**直接运行 `python -m minisgl`——请使用仓库的包装脚本，它会以 `/usr/bin/python3.12 -s` 运行（跳过用户 site）：

## 运行 OpenAI 兼容服务器

```bash
cd /mnt/data/mini-sglang
./run_python.sh -m minisgl --model "Qwen/Qwen3-0.6B"
```

`Qwen3-0.6B` 已缓存在 `~/.cache/huggingface` 中，可以轻松放入你的 RTX 4070（12 GB，当前约使用 1.5 GB）。默认设置：端口 `1919`，主机 `localhost`。

## 测试

```bash
curl http://localhost:1919/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen/Qwen3-0.6B", "messages": [{"role": "user", "content": "Hello!"}], "max_tokens": 64}'
```

## 其他选项

- **终端聊天**：`./run_python.sh -m minisgl --model "Qwen/Qwen3-0.6B" --shell-mode`（注意：CLI 标志是 `--shell-mode`，不是 README 中显示的 `--shell`）
- **自定义端口**：`--port 30000`
- **张量并行**（多 GPU）：`--tp-size 4`
- **禁用 radix 缓存**（消融实验）：`--cache-type naive`

需要我现在启动服务器并验证它是否能正常响应吗？