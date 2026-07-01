---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gemma4闪存注意力修复
translated: true
type: note
---

## 综合评估：RTX 4070 上的 Gemma4 故障排查

### 系统配置

| 组件 | 详细信息 |
| ----------- | -------- |
| **操作系统** | Ubuntu, Linux 6.8.0-107-generic x86_64 |
| **显卡** | NVIDIA RTX 4070 (12GB 显存), CUDA 13.0, 驱动 580.126.20 |
| **内存** | 总计 62GB, 约 57GB 可用 |
| **处理器** | 32 核心 |
| **llama.cpp** | 提交版本 `94ca829b6`, 构建参数 `GGML_CUDA=ON`, `GGML_CUDA_FA=ON`, 发布版本 `-O3` |

### 可用模型

| 模型 | 大小 | 状态 |
| ------- | ------ | -------- |
| `gemma-4-26B-A4B-it-UD-IQ2_M.gguf` | 9.3GB | 已测试，可运行 |
| `gemma-4-26B-A4B-it-UD-IQ3_S.gguf` | 11GB | 未测试 — 考虑到 KV 缓存，在 12GB 显存上可能过大 |
| `DeepSeek-R1-Distill-Llama-8B-Q4_K_M.gguf` | — | 先前使用 |
| `Mistral-Small-24B-Instruct-2501-Q2_K.gguf` | — | 本次会话前正在运行 |

### 根本原因分析

**崩溃情况：** `llama.log` 中捕获到两个相同的 CUDA 错误，回溯信息一致：

```
ggml_cuda_error → ggml_backend_cuda_buffer_set_tensor → ggml_backend_sched_graph_compute_async
  → llama_context::graph_compute → process_ubatch → decode → llama_decode
```

**原因：** Flash Attention CUDA 内核在 gemma4 的模型架构上运行失败。Gemma4 是一个 **MoE (Mixture of Experts)** 模型，具有以下特点：

- **混合 SWA/非 SWA 层** — 25 个 SWA 层 + 5 个非 SWA 层
- **不同层间的 V 嵌入维度不同** — llama.cpp 明确警告：`"the V embeddings have different sizes across layers and FA is not enabled - padding V cache to 2048"`

FA 内核未能正确处理这种异质层结构，导致在张量设置操作中出现 CUDA 缓冲区越界写入。

### 采取的措施

1. **检查系统** — 识别了 GPU、内存、构建配置、模型文件
2. **分析崩溃日志** (`llama.log`) — 在 FA 路径中发现 CUDA 缓冲区溢出
3. **查看服务器日志** (`llama-server.log`) — 发现 Mistral 之前正在运行，存在上下文溢出错误（17-18K 令牌 vs 16K 限制）
4. **尝试 `--no-flash-attn` 参数** — 当前版本已重命名该标志，尝试失败
5. **通过 `--help` 找到正确参数** (`--flash-attn off`)
6. **成功启动** — 模型加载成功，并正确响应
7. **修改绑定配置** — 从 `127.0.0.1` 改为 `0.0.0.0:8081`

### 当前运行配置

```bash
llama-server \
  -m gemma-4-26B-A4B-it-UD-IQ2_M.gguf \
  --flash-attn off \
  -ngl 99 \
  -c 4096 \
  --host 0.0.0.0 \
  --port 8081
```

### 资源使用情况

| 资源 | 使用情况 |
| ---------- | ------- |
| 显存 | 11.3GB / 12GB (模型 9.5GB + KV 缓存 920MB + 计算 522MB) |
| 内存 | 约 1GB 映射到 CPU |
| 速度 | 生成约 111 令牌/秒，提示词处理约 127 令牌/秒 |

### 关注点与建议

1. **显存使用紧张** (11.3/12GB)。在 4 个槽位和 4096 上下文长度下，更长的对话可能导致 OOM。建议：
    - 如果遇到问题，可以考虑减少至 `-c 2048` 或 `--parallel 2`
    - 或者使用 `-ngl 28` 代替 `99` 将少数层卸载到 CPU

2. **IQ2_M 是一种非常激进的量化方案** — 与原始的 26B 模型相比，预计会有明显的质量下降。IQ3_S (11GB) 质量会更好，但在考虑 KV 缓存开销后将无法装入显存。

3. **V 缓存填充** (至 2048) 浪费了一些显存。这是关闭 FA 时已知的限制 — 缓存无法使用各层实际的 V 维度，必须填充至最大值。

4. **上游修复** — 这很可能是 llama.cpp 中针对 gemma4 的 CUDA FA 内核的一个已知问题。值得关注仓库中提到 "gemma4 flash attention" 的 PR — 一旦修复，重新启用 FA 将节省显存并可能提高速度。

5. **旧的 `llama.sh` 脚本** 仍然指向端口 8000 上的 `DeepSeek-R1-Distill-Llama-8B`。如果 gemma4 将成为你的默认模型，可能需要更新此脚本。
