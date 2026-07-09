---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang Hugging Face Model Repository IDs
translated: false
type: note
---

Question: Which Hugging Face repositories can be used with SGLang when it asks for a model name?

Answer:

SGLang loads models directly from the Hugging Face Hub. In most cases, you simply provide the **repository ID** (`owner/model_name`), not a URL.

For example:

```text
Qwen/Qwen3-8B
Qwen/Qwen3-32B
meta-llama/Llama-3.1-8B-Instruct
deepseek-ai/DeepSeek-R1-Distill-Qwen-7B
google/gemma-3-4b-it
mistralai/Mistral-7B-Instruct-v0.3
```

or the full URL also works in some UIs:

```text
https://huggingface.co/Qwen/Qwen3-8B
```

but the repository ID is the standard form.

### Models that work well with SGLang

SGLang has excellent support for most modern decoder-only LLMs.

| Family   | Example repo                              |
| -------- | ----------------------------------------- |
| Qwen     | `Qwen/Qwen3-8B`                           |
| Llama    | `meta-llama/Llama-3.1-8B-Instruct`        |
| Gemma    | `google/gemma-3-4b-it`                    |
| Mistral  | `mistralai/Mistral-7B-Instruct-v0.3`      |
| DeepSeek | `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` |
| Phi      | `microsoft/Phi-4-mini-instruct`           |
| GLM      | `THUDM/GLM-4-9B-Chat`                     |

### Models that usually do NOT work

SGLang expects a Hugging Face Transformers model. These generally won't work directly:

* ❌ GGUF models
* ❌ llama.cpp-only models
* ❌ GPTQ models without supported kernels
* ❌ AWQ models if your SGLang version doesn't support them
* ❌ ExLlamaV2-only formats

For example:

```text
unsloth/gemma-4-e4b-it-gguf
```

is a **GGUF** repository and is intended for `llama.cpp`, **not** SGLang.

Instead, use the original Transformers model, e.g.:

```text
google/gemma-3-4b-it
```

or another supported FP16/BF16/official checkpoint.

### Example

If your environment variable is:

```bash
MODEL=Qwen/Qwen3-8B
```

then SGLang downloads the model automatically from Hugging Face:

```bash
python -m sglang.launch_server \
    --model-path Qwen/Qwen3-8B
```

or

```bash
MODEL=Qwen/Qwen3-8B
HF_TOKEN=<PLACEHOLDER>
```

if the model requires authentication.

### If you're using RunPod Serverless

In the "Model" field, simply enter:

```text
Qwen/Qwen3-8B
```

or

```text
meta-llama/Llama-3.1-8B-Instruct
```

not a GGUF repository.

References:

* [https://huggingface.co/](https://huggingface.co/)
* [https://github.com/sgl-project/sglang](https://github.com/sgl-project/sglang)
