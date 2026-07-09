---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang Hugging Face 模型仓库 ID
translated: true
type: note
---

问题：当 SGLang 要求提供模型名称时，可以使用哪些 Hugging Face 仓库？

答案：

SGLang 直接从 Hugging Face Hub 加载模型。大多数情况下，您只需提供**仓库 ID**（`所有者/模型名称`），而不是 URL。

例如：

```text
Qwen/Qwen3-8B
Qwen/Qwen3-32B
meta-llama/Llama-3.1-8B-Instruct
deepseek-ai/DeepSeek-R1-Distill-Qwen-7B
google/gemma-3-4b-it
mistralai/Mistral-7B-Instruct-v0.3
```

或者在某些 UI 中，完整 URL 也可以使用：

```text
https://huggingface.co/Qwen/Qwen3-8B
```

但仓库 ID 是标准形式。

### 与 SGLang 配合良好的模型

SGLang 对大多数现代 decoder-only LLM 有出色的支持。

| 系列     | 示例仓库                                     |
| -------- | -------------------------------------------- |
| Qwen     | `Qwen/Qwen3-8B`                              |
| Llama    | `meta-llama/Llama-3.1-8B-Instruct`           |
| Gemma    | `google/gemma-3-4b-it`                       |
| Mistral  | `mistralai/Mistral-7B-Instruct-v0.3`         |
| DeepSeek | `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B`    |
| Phi      | `microsoft/Phi-4-mini-instruct`              |
| GLM      | `THUDM/GLM-4-9B-Chat`                        |

### 通常不适用的模型

SGLang 期望的是 Hugging Face Transformers 模型。以下类型通常无法直接使用：

* ❌ GGUF 模型
* ❌ 仅适用于 llama.cpp 的模型
* ❌ 缺少支持内核的 GPTQ 模型
* ❌ 如果您的 SGLang 版本不支持 AWQ 模型，则无法使用
* ❌ 仅适用于 ExLlamaV2 的格式

例如：

```text
unsloth/gemma-4-e4b-it-gguf
```

是一个 **GGUF** 仓库，专为 `llama.cpp` 设计，**不适用于** SGLang。

请改用原始的 Transformers 模型，例如：

```text
google/gemma-3-4b-it
```

或其他受支持的 FP16/BF16/官方检查点。

### 示例

如果您的环境变量是：

```bash
MODEL=Qwen/Qwen3-8B
```

那么 SGLang 会自动从 Hugging Face 下载模型：

```bash
python -m sglang.launch_server \
    --model-path Qwen/Qwen3-8B
```

或者

```bash
MODEL=Qwen/Qwen3-8B
HF_TOKEN=<占位符>
```

如果模型需要身份验证。

### 如果您使用 RunPod Serverless

在 "Model" 字段中，只需输入：

```text
Qwen/Qwen3-8B
```

或

```text
meta-llama/Llama-3.1-8B-Instruct
```

而不是 GGUF 仓库。

参考资料：

* [https://huggingface.co/](https://huggingface.co/)
* [https://github.com/sgl-project/sglang](https://github.com/sgl-project/sglang)