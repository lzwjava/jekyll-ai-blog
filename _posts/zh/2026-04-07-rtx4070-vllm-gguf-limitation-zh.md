---
audio: false
generated: true
image: false
lang: zh
layout: post
title: RTX 4070 vLLM GGUF 限制
translated: true
type: note
---

问：`gemma-4-26B-A4B-it-UD-IQ3_S.gguf` 可以在本地的 RTX 4070 服务器上通过 vLLM 运行吗？

答：

简短回答：**不行。**
你无法在 **RTX 4070（12GB 显存）** 上使用 **vLLM** 来运行 `gemma-4-26B-A4B-it-UD-IQ3_S.gguf`。

这存在 **两个独立的障碍**：

---

# 1. vLLM 不支持 GGUF 模型

你的模型：

```
gemma-4-26B-A4B-it-UD-IQ3_S.gguf
```

属于：

* GGUF 格式
* llama.cpp 量化格式（IQ3_S）
* Unsloth / llama.cpp 生态圈

但 **vLLM 仅支持：**

* HuggingFace FP16/BF16 格式
* AWQ 量化格式
* GPTQ 量化格式
* 部分张量并行分片权重

vLLM **完全无法加载 GGUF** 格式。

所以，在考虑显存之前——它根本就不会运行。

你必须使用以下之一：

* llama.cpp
* llama-cpp-python
* Ollama
* OpenWebUI + llama.cpp 后端
* OpenClaw（如果使用 llama 后端）

---

# 2. RTX 4070 显存本身也太小

RTX 4070：

```
12GB 显存
```

你的模型：

```
Gemma 4 26B IQ3_S
```

大致显存需求：

| 量化级别 | 所需显存 |
| ------ | ----------- |
| IQ3_S | ~13–15GB |
| IQ2 | ~10–11GB |
| Q4_K_M | ~18–20GB |

因此：

* **IQ3_S → 对于 4070 来说过大**
* 也许可以 **CPU 卸载** 运行，但速度会很慢
* 况且 vLLM 本身也不支持 GGUF 模型的 CPU 卸载

---

# 在 RTX 4070 上可行的方案

最佳选择：

### 方案一（推荐）

使用 llama.cpp：

```
llama-server \
-m gemma-4-26B-A4B-it-UD-IQ3_S.gguf \
--n-gpu-layers 30
```

这样做可以：

* 部分层加载到 GPU
* 其余层使用 CPU
* 获得可用的速度

---

### 方案二（更合适的选择）

使用更小的量化版本：

```
IQ2_XS
IQ2_S
```

这些可以完全装入 4070 的显存。

---

### 方案三（最适合 vLLM）

使用 **非 GGUF** 模型：

例如：

```
gemma-2-27b-it AWQ
gemma-2-9b-it
qwen3-14b-awq
```

这些模型可以在 vLLM 中运行。

---

# 最终结论

| 问题                  | 答案                     |
| -------------------- | ------------------------ |
| vLLM 支持 GGUF 吗？   | ❌ 不支持                  |
| RTX 4070 能否运行 IQ3_S？ | ❌ 不能                     |
| llama.cpp 可行吗？   | ✅ 可行                    |
| 可以 CPU 卸载吗？     | ✅ 可以（速度慢）            |
| 最佳选择              | 更小的 IQ2 或 14B 模型       |

如果你告诉我：

* 只用 vLLM？
* 用 OpenClaw？
* 用 Ollama？
* 用 llama.cpp？

我会给出 **针对 RTX 4070 的最佳模型选择**。
