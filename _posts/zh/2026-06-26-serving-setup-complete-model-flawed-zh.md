---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 服务部署完成，模型存在缺陷
translated: true
type: note
---

## 摘要

### ✅ HuggingFace 上传 — 已完成
所有文件已上传至 https://huggingface.co/lzwjava/sec-edgar-gpt-124m。使用阿里云香港中继传输 475MB 的 model.safetensors（Mac→HK 30分钟 SCP，HK→HF 12分钟上传）。MD5 校验一致。

### ✅ RunPod 服务基础设施 — 已完成
- RunPod：`ssh -p 28484 -i ~/.ssh/id_ed25519 root@213.173.110.200`
- RTX 2000 Ada（16GB），48 个 CPU 核心，251GB 内存
- FastAPI 服务器运行于 `/workspace/model/server.py`，端口 8080
- 兼容 OpenAI 的 API（`/v1/completions`、`/v1/chat/completions`、`/v1/models`）
- GGUF 也已转换至 `/workspace/model/sec-edgar-gpt-124m.gguf`（624MB）及 llama-server 位于 `/workspace/llama-b9811/`

### ⚠️ GGUF 转换 — 已解决（但目前不需要）
关于 `gguf` Python 库形状约定的重要学习：
- **Writer 反转形状**：`ti.shape[n_dims - 1 - j]` — numpy (a,b) → 文件 [b,a]
- `token_embd.weight`：直接传入 numpy（由 gguf 自动处理）
- 线性权重：需要手动 `.T` 转置（HF [out,in] → [in,out]）
- `output.weight`：直接传入（与 token_embd 相同）
- `tokenizer.ggml.merges`：必须用空格分隔（"Ġ t"），不可拼接（"Ġt"）
- `tokenizer.ggml.model` 键必须存在
- 词汇表必须与实际 token 数匹配（50257，而非填充后的 50304）
- `tokenizer.ggml.pre = "default"`（b9811 二进制不支持 "gpt2" 预分词器）

### ❌ 模型质量问题 — 非服务端问题
模型输出退化的内容（"ivableivable..." 循环），无论：
- 服务方式（直接 transformers、llama.cpp、FastAPI）
- 采样策略（贪婪、top-k、温度）
- 使用的提示词

Top-1 下一个 token 概率平坦（约 0.01-0.002），无明显胜出者，top token 为后缀片段（"em"、"ivable"、"igned"）。这表明尽管报告验证损失为 2.28，但模型在训练中未能正确收敛。在 RTX 4070 上进行的 1 epoch、124M 参数训练可能存在问题（学习率、数据预处理等）。

### 接下来做什么
服务基础设施已准备就绪——一旦你有更好的训练模型检查点，只需：
```bash
# 在 RunPod 上：
cd /workspace/model
# 用新检查点替换 hf-model/，然后：
python3 server.py  # 兼容 OpenAI 的 API 运行在 :8080
```