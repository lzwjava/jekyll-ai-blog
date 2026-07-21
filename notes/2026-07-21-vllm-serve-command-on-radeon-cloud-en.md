---
audio: false
generated: true
image: false
lang: en
layout: post
title: vLLM Serve Command on Radeon Cloud
translated: false
type: note
---

Question: How to fill the vLLM "Serve Command" field in Radeon Cloud (AMD OneClick Base ROCm 7.2.1)?

Answer:

The **Serve Command** is simply the `vllm serve` CLI command that starts the OpenAI-compatible API server. vLLM syntax is:

```bash
vllm serve <HuggingFace-model-id> [options]
```

([vLLM][1])

For example, if you want to deploy Qwen3 8B:

```bash
vllm serve Qwen/Qwen3-8B \
  --host 0.0.0.0 \
  --port 8000 \
  --dtype float16 \
  --max-model-len 32768
```

Put that whole command into **Serve Command**.

---

Common examples:

### 1. Qwen3 8B (good starting point)

```bash
vllm serve Qwen/Qwen3-8B \
--host 0.0.0.0 \
--port 8000 \
--dtype float16 \
--max-model-len 32768
```

---

### 2. Qwen3 14B

```bash
vllm serve Qwen/Qwen3-14B \
--host 0.0.0.0 \
--port 8000 \
--dtype float16 \
--max-model-len 32768
```

---

### 3. Larger model with multiple AMD GPUs

Example: 4 GPUs:

```bash
vllm serve Qwen/Qwen3-32B \
--host 0.0.0.0 \
--port 8000 \
--dtype float16 \
--tensor-parallel-size 4 \
--max-model-len 32768
```

`--tensor-parallel-size` splits the model across GPUs. ([Mintlify][2])

---

### 4. For long-context agent usage

Since you use agents (Claude Code/OpenClaw style workloads), KV cache becomes the bottleneck. Start with:

```bash
vllm serve Qwen/Qwen3-30B-A3B \
--host 0.0.0.0 \
--port 8000 \
--dtype float16 \
--max-model-len 65536 \
--gpu-memory-utilization 0.95
```

---

### Important for Radeon ROCm

The container:

```
amd-oneclick-base:rocm7.2.1-py3.12-v20260416
```

already has ROCm + vLLM environment prepared. AMD documents vLLM serving through ROCm with OpenAI-compatible APIs. ([ROCm Documentation][3])

You usually **do not** need:

```bash
python -m vllm.entrypoints.openai.api_server
```

because `vllm serve` is the current interface. ([vLLM][1])

---

A good first test on Radeon Cloud:

```
vllm serve Qwen/Qwen3-8B --host 0.0.0.0 --port 8000 --dtype float16
```

After deployment you should get:

```
https://<space-id>/8000/v1
```

Then test:

```bash
curl https://<space-id>/8000/v1/models
```

or with Python:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://<space-id>/8000/v1",
    api_key="<API_KEY>"
)

response = client.chat.completions.create(
    model="Qwen/Qwen3-8B",
    messages=[
        {"role": "user", "content": "hello"}
    ]
)

print(response.choices[0].message.content)
```

References:

* ([vLLM][1])
* ([ROCm Documentation][3])
* ([Mintlify][2])

[1]: https://docs.vllm.ai/en/latest/cli/index.html?utm_source=chatgpt.com "vLLM CLI Guide - vLLM"
[2]: https://www.mintlify.com/vllm-project/vllm/api/cli/serve?utm_source=chatgpt.com "vllm serve - vLLM"
[3]: https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/inference/vllm.html?utm_source=chatgpt.com "vLLM inference and serving on ROCm — AMD ROCm AI Ecosystem"
