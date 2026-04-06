---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070的vLLM模型指南
translated: true
type: note
---

问题：RTX 4070 上可以用 vLLM 部署哪些开源模型？

回答：

你的 **RTX 4070（12GB 显存）** 配合 **vLLM** 比 llama.cpp 限制更严格：

* vLLM 需要 **模型权重 + KV 缓存完全存储在 GPU 中**
* 不支持 GGUF 格式
* 偏好 **AWQ / GPTQ / FP8 / INT4** 量化格式
* 实际可行的大小：**≤ 8B 安全**，**≤ 14B 勉强**，**>14B 通常不行**

vLLM 支持多种架构，包括 Qwen、Gemma、DeepSeek、Llama、Mistral 等。（[vLLM][1]）

---

# 适用于 vLLM + RTX 4070 (12GB) 的最佳模型

## 🟢 最佳（轻松运行）

以下模型可**流畅**运行：

### 1. Qwen2.5 7B AWQ（推荐）

```
Qwen/Qwen2.5-7B-Instruct-AWQ
```

原因：

* 强大推理能力
* 低显存占用
* vLLM 中速度快
* 生产环境稳定

运行命令：

```bash
vllm serve Qwen/Qwen2.5-7B-Instruct-AWQ \
  --quantization awq
```

---

### 2. Gemma 2 9B (FP8 / AWQ)

```
google/gemma-2-9b-it
```

运行命令：

```bash
vllm serve google/gemma-2-9b-it \
  --dtype float16
```

或者更好选择：

```
gemma-2-9b-it-awq
```

---

### 3. DeepSeek 7B

```
deepseek-ai/deepseek-llm-7b-chat
```

轻量且稳定。

---

# 🟡 临界（可能通过调参运行）

以下模型**有可能运行**，前提是：

* 小上下文（4k）
* 使用 fp8 kv 缓存
* GPU 利用率 0.9

### Qwen 14B AWQ

```
Qwen/Qwen2.5-14B-Instruct-AWQ
```

但许多用户反馈 **12GB GPU 在 vLLM 中无法完全容纳**。（[Reddit][2]）

---

### Mistral 12B

```
mistralai/Mistral-Small-12B-Instruct
```

可能需要参数：

```
--max-model-len 4096
--gpu-memory-utilization 0.9
```

---

# 🔴 在 RTX 4070 (vLLM) 上不可行

以下模型**无法运行**：

* Qwen 27B
* Gemma 27B
* DeepSeek R1 32B
* Llama 3 70B
* Gemma 26B（你的模型）

即使 **27B INT4** 量化模型，在考虑 KV 缓存前也可能需要约 27GB 显存。（[Reddit][3]）

---

# 我的推荐（综合最佳）

使用此模型：

```
Qwen2.5-7B-Instruct-AWQ
```

最佳平衡：

* 强推理能力
* 支持工具调用
* 速度快
* 适合 4070
* 支持 vLLM 批处理

---

# 如果你告诉我你的目标

我会推荐最适合的模型：

* 编码 → 最佳模型
* 代理/工具调用 → 最佳
* 推理 → 最佳
* OpenClaw → 最佳
* API 服务器 → 最佳

告诉我即可。

[1]: https://docs.vllm.ai/en/latest/models/supported_models.html?utm_source=chatgpt.com "支持的模型 - vLLM"
[2]: https://www.reddit.com/r/LocalLLaMA/comments/1mwm9hx?utm_source=chatgpt.com "Qwen 14b 在 3060 vLLM 上"
[3]: https://www.reddit.com/r/LocalLLaMA/comments/1rxwbh9/help_qwen3527bgptq_oom_on_32gb_vram_video/?utm_source=chatgpt.com "[求助] Qwen3.5-27B-GPTQ 在 32GB VRAM 上 OOM - 视频理解用例 (vLLM)"