---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gemma 4 模型设置摘要
translated: true
type: note
---

以下是本次会话的完整摘要。

---

## 会话：Gemma 4 E4B — 下载、验证、更新 llama.cpp

### 1. 下载模型

- **文件**：`gemma-4-E4B-it-Q3_K_M.gguf`，位于 `/mnt/data/models/`
- **大小**：3.8 GB（Q3_K_M 量化，4.30 BPW）
- **方式**：通过代理（127.0.0.1:7890）使用 `curl` — `hf` CLI 失败，因为 Python 的 `requests` 无法正确通过 Shell 代理路由
- **SHA256**：`db7ba769f71e7d4e8ec11db42152ba20f422a12d58960a665b5395e111582072`

### 2. 模型架构（来自 GGUF 元数据）

| 属性 | 值 |
| --- | --- |
| 架构 | Gemma 4 (gemma4) |
| 参数量 | 7.52 B（标记为“E4B”） |
| 层数 | 42 |
| 嵌入维度 | 2560 |
| 前馈维度 | 10240 |
| 注意力头数 | 8（GQA = 4，2 个 KV 头） |
| 上下文长度 | 131,072 |
| 滑动窗口 | 512（混合型 — 35 个 SWA 层 + 7 个全局层） |
| RoPE 基准频率 | 1,000,000（全局），10,000（SWA） |
| Logit 软上限 | 30.0 |
| 共享 KV 层 | 18（层绑定 KV 设计） |
| 逐层输入嵌入 | 是（Gated Delta Net） |
| 词表 | BPE，262,144 个 token |
| 许可证 | Apache 2.0 |

### 3. 初始推理测试（旧版 b8）

- 提示评估：291 t/s
- 生成：91 t/s
- VRAM：模型 2,343 MiB + 计算缓冲区约 14 MiB（RTX 4070）

### 4. 更新 llama.cpp

- **仓库**：`git@github.com:ggerganov/llama.cpp.git`
- **从**：b8 (834a24366) 升级
- **升级至**：版本 1194 (067de9371)
- **拉取了 142+ 个新标签**（b9156 → b9600 范围）
- 主要变化预期：改进的 Gemma 4 支持、Gated Delta Net 优化、Flash Attention 改进

### 5. 构建

- **构建系统**：CMake + Ninja，`-DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release`
- **磁盘问题**：在 CUDA 模板编译期间，根分区达到 100%（剩余 430M）
- **清理**：删除 101G — `~/.cache/uv/`（45G）、`~/.cache/nanochat/`（39G）、`~/.cache/pip/`（17G）
- **结果**：剩余 77G，679 个目标全部构建成功
- **重新构建的二进制文件**：`llama-cli`、`llama-server`、`llama-simple`、`llama-perplexity`、`llama-bench` 等

### 6. 最终验证

- `llama-cli --version` → 版本 1194 (067de9371)
- 新版构建上的 Gemma 4 E4B Q3_K_M 推理：约 68 t/s，运行正常

### 当前状态

- 已更新 llama.cpp 位于 `~/projects/llama.cpp/build/bin/`
- 模型就绪位于 `/mnt/data/models/gemma-4-E4B-it-Q3_K_M.gguf`
- 根分区剩余 77 GB，`/mnt/data` 剩余 795 GB
