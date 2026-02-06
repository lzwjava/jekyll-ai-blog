---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 精通 llama.cpp 命令行选项
translated: true
type: note
---

**Question:** 请提供 llama.cpp 命令行选项的全面介绍。

**Answer:**

llama.cpp 是一个高效的 C/C++ 库，用于在本地运行 Large Language Models (LLMs)。它包含几个主要的执行文件，这些文件共享大部分参数但用途不同：

- **llama-cli** — 终端中的交互式对话 / 文本生成（最常用于测试）
- **llama-server** — 兼容 OpenAI 的 HTTP API 服务器 + 简单的 Web UI
- **llama-bench** — 性能基准测试
- 其他 (llama-perplexity, llama-embedding, llama-eval-callbacks, …)

绝大多数重要的选项在 llama-cli 和 llama-server 中是**通用**的。

### 1. 模型加载 – 最最重要的标志 (Flags)

- `-m, --model FNAME`  
  GGUF 模型文件的路径 (`.gguf`)

- `-hf, --hf-repo REPO` + `--hf-file FILE`  
  直接从 Hugging Face 下载模型 (例如：`-hf bartowski/Llama-3.1-8B-Instruct-GGUF --hf-file Llama-3.1-8B-Instruct-Q5_K_M.gguf`)

- `--mmproj FNAME`  
  multimodal projector 路径 (用于 vision/language 模型，如 llava, bakllava, obsidian 等)

### 2. Context & KV Cache 控制

- `-c, --ctx-size N` / `--context-length N`  
  最大 context 长度（以 token 为单位，默认通常为 4096 或 8192，0 = 模型默认值）

- `--no-context-shift`  
  当 context 满时禁用 context 轮转（较新的模型通常推荐此项）

- `--rope-scaling yarn` / `--rope-scale N` / `--rope-freq-base` / `--rope-freq-scale`  
  高级 RoPE 缩放 (当 context 大于原始训练长度时非常重要)

### 3. GPU / 加速层

- `-ngl, --n-gpu-layers N`  
  放入 GPU 的层数 (对速度至关重要)  
  - `999` / `-1` = 尝试将所有层放入 GPU  
  - `0` = 仅使用 CPU

- `-fa, --flash-attn`  
  启用 Flash Attention (在现代 GPU 上通常更快且 VRAM 占用更低)

- `-sm row` / `-sm block`  
  多 GPU 上的模型层拆分模式 (row / block / layer)

- `--main-gpu INDEX` / `--tensor-split "0,0.5,0.5,…"`  
  多 GPU 拆分控制

- `--rpc-tensors` / `--no-rpc-tensors`  
  通过 RPC 将 tensor 卸载到另一台机器

### 4. 性能 / 线程 (Performance / Threading)

- `-t, --threads N`  
  用于生成的 CPU 线程数 (默认 ≈ 所有物理核心)

- `-tb, --threads-batch N`  
  用于 Prompt 处理 / Batch 的线程数 (通常与 `-t` 相同或略高)

- `-b, --batch-size N`  
  逻辑批处理大小 (默认 2048，常用 512–4096)

- `-ub, --ubatch-size N`  
  物理微批处理大小 (通常为 512–1024，对处理超长 Prompt 很重要)

- `--cont-batching` / `--no-cont-batching`  
  启用连续批处理 (在服务器 / 并发请求场景下通常更快)

- `--no-mmap`  
  禁用内存映射 (在某些文件系统或 WSL 上有时需要)

### 5. Sampling – 控制创意与质量

- `--temp N`  
  Temperature (0.0 = 确定性结果, 0.7–1.2 = 更有创意, 默认 ~0.8)

- `--top-k N`  
  仅保留前 K 个 token (常用 20–50)

- `--top-p N`  
  累积概率阈值 (常用 0.9–0.95)

- `--min-p N`  
  相对于最可能 token 的最小概率 (0.05–0.1 在 2025 年之后非常流行)

- `--tfs N` / `--typical N` / `--mirostat 2 --mirostat-tau 5.0 --mirostat-et 0.1`  
  高级采样器 (mirostat v2 是 2025–2026 年非常棒的默认设置)

- `--repeat-penalty N` / `--presence-penalty` / `--frequency-penalty`  
  抑制重复

- `--dry` 系列 (dry-multipliers, dry-base, dry-sequence-breakers)  
  较新的重复惩罚方法 (2025+)

### 6. Prompt & Chat 控制 (主要针对 llama-cli)

- `-cnv, --color --no-display-prompt --simple-io`  
  美观的终端对话模式

- `--chat-template TEMPLATE` / `--chat-template-file FILE`  
  选择/修改对话模板 (chatml, llama-3, mistral, gemma, …)

- `-s, --simple-io`  
  原始输入/输出 (无特殊格式)

- `--reverse-prompt STR` / `--in-prefix` / `--in-suffix`  
  自定义停止词 / Prompt 包装

- `-p, --prompt TEXT` / `-f, --file FILE`  
  初始非交互式 Prompt

- `-n, --n-predict N` / `-c, --ctx-size N`  
  生成多少个 token (-1 = 无限生成直到停止)

### 7. llama-server 特有选项 (兼容 OpenAI API)

- `--host 0.0.0.0 --port 8080`  
  监听地址/端口

- `--path PREFIX`  
  API 基础路径 (默认为 /v1)

- `--slots` / `--parallel N`  
  最大并发请求数 / 槽位

- `--embedding`  
  启用 embedding 端点

- `--reasoning-format deepseek` / `--jinja`  
  针对推理模型 / 全量 jinja 模板的特殊处理

- `--api-key-file` / `--ssl-key-file` / `--ssl-cert-file`  
  身份验证与 HTTPS

### 8. 快速参考 – 2025–2026 流行组合

**快速本地对话 (优质 GPU):**

```bash
./llama-cli -m model-Q5_K_M.gguf -ngl 99 -fa --temp 0.7 --min-p 0.05 --top-k 40 --top-p 0.9 -c 32768 --color -cnv
```

**高性能服务器 (RTX 4090 / 5090 级别):**

```bash
./llama-server -m model-Q6_K.gguf --n-gpu-layers 999 -fa --flash-attn --ubatch-size 1024 -c 32768 --temp 0.6 --min-p 0.1 --cont-batching --host 0.0.0.0
```

**超长 Context 纯 CPU 运行:**

```bash
./llama-cli -m model-Q4_K_M.gguf -ngl 0 -c 131072 --rope-scaling yarn --rope-scale 16 --no-mmap --threads 24
```

选项更新非常快 — 请务必运行 `./llama-cli --help` 或 `./llama-server --help` 以查看当前版本最准确的列表。

**References:**

- [llama.cpp GitHub repository](https://github.com/ggml-org/llama.cpp)
- [llama-cli comprehensive guide discussion](https://github.com/ggml-org/llama.cpp/discussions/15709)
- [llama-server README](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md)
- [Qwen llama.cpp usage examples](https://qwen.readthedocs.io/en/latest/run_locally/llama.cpp.html)
- [llama.cpp manpage (Debian)](https://manpages.debian.org/testing/llama.cpp-tools/llama-cli.1.en.html)