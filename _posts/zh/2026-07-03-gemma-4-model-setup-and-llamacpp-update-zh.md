---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gemma 4 模型设置与 llama.cpp 更新
translated: true
type: note
---

以下是完整的会议总结。

---

## 会议：Gemma 4 E4B — 下载、验证、更新 llama.cpp

### 1. 下载模型
- **文件**: `gemma-4-E4B-it-Q3_K_M.gguf` 位于 `/mnt/data/models/`
- **大小**: 3.8 GB（Q3_K_M 量化，4.30 BPW）
- **方法**: 通过代理（127.0.0.1:7890）使用 `curl` —— `hf` CLI 失败，因为 Python 的 `requests` 没有正确通过 shell 代理路由
- **SHA256**: `db7ba769f71e7d4e8ec11db42152ba20f422a12d58960a665b5395e111582072`

### 2. 模型架构（来自 GGUF 元数据）

| 属性 | 值 |
|---|---|
| 架构 | Gemma 4 (gemma4) |
| 参数 | 7.52 B（标记为"E4B"） |
| 层数 | 42 |
| 嵌入维度 | 2560 |
| 前馈维度 | 10240 |
| 注意力头数 | 8（GQA = 4，2 KV 头） |
| 上下文长度 | 131,072 |
| 滑动窗口 | 512（混合 —— 35 个 SWA 层 + 7 个全局层） |
| RoPE 基频 | 1,000,000（全局），10,000（SWA） |
| Logit 软上限 | 30.0 |
| 共享 KV 层 | 18（层绑定 KV 设计） |
| 逐层输入嵌入 | 是（Gated Delta Net） |
| 词表 | BPE，262,144 个 token |
| 许可证 | Apache 2.0 |

### 3. 初始推理测试（旧版本 b8）
- 提示评估：291 t/s
- 生成：91 t/s
- VRAM：模型占用 2,343 MiB + 计算缓冲区约 14 MiB（RTX 4070）

### 4. 更新 llama.cpp
- **仓库**: `git@github.com:ggerganov/llama.cpp.git`
- **从版本**: b8 (834a24366)
- **升级到**: 版本 1194 (067de9371)
- **拉取了 142+ 个新标签**（b9156 → b9600 范围）
- 预期主要变化：改进 Gemma 4 支持、Gated Delta Net 优化、flash attention 改进

### 5. 构建
- **构建系统**: CMake + Ninja，`-DGGML_CUDA=ON -DCMAKE_BUILD_TYPE=Release`
- **磁盘问题**: 在 CUDA 模板编译期间根分区达到 100%（430M 空闲）
- **清理**: 释放 101G —— `~/.cache/uv/`（45G）、`~/.cache/nanochat/`（39G）、`~/.cache/pip/`（17G）
- **结果**: 空闲 77G，679 个目标全部构建成功
- **重新编译的二进制文件**: `llama-cli`、`llama-server`、`llama-simple`、`llama-perplexity`、`llama-bench` 等

### 6. 最终验证
- `llama-cli --version` → 版本 1194 (067de9371)
- 在新版本上运行 Gemma 4 E4B Q3_K_M 推理：约 68 t/s，正常工作

### 当前状态
- 更新的 llama.cpp 位于 `~/projects/llama.cpp/build/bin/`
- 模型就绪于 `/mnt/data/models/gemma-4-E4B-it-Q3_K_M.gguf`
- 根分区空闲 77 GB，/mnt/data 空闲 795 GB