---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Radeon Cloud 上的 vLLM 服务命令
translated: true
type: note
---

问题：如何在 Radeon Cloud（AMD OneClick Base ROCm 7.2.1）中填写 vLLM 的“Serve Command”字段？

答案：

**Serve Command** 就是 `vllm serve` CLI 命令，用于启动与 OpenAI 兼容的 API 服务器。vLLM 语法如下：

```bash
vllm serve <HuggingFace-model-id> [options]
```

（[vLLM][1]）

例如，如果你想部署 Qwen3 8B：

```bash
vllm serve Qwen/Qwen3-8B \
  --host 0.0.0.0 \
  --port 8000 \
  --dtype float16 \
  --max-model-len 32768
```

将整个命令填入 **Serve Command** 字段。

---

常见示例：

### 1. Qwen3 8B（良好的起点）

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

### 3. 在多个 AMD GPU 上运行更大模型

示例：4 块 GPU：

```bash
vllm serve Qwen/Qwen3-32B \
--host 0.0.0.0 \
--port 8000 \
--dtype float16 \
--tensor-parallel-size 4 \
--max-model-len 32768
```

`--tensor-parallel-size` 用于将模型拆分到多块 GPU 上。（[Mintlify][2]）

---

### 4. 用于长上下文智能体场景

由于你使用智能体（Claude Code/OpenClaw 风格的工作负载），KV 缓存会成为瓶颈。建议从以下命令开始：

```bash
vllm serve Qwen/Qwen3-30B-A3B \
--host 0.0.0.0 \
--port 8000 \
--dtype float16 \
--max-model-len 65536 \
--gpu-memory-utilization 0.95
```

---

### 针对 Radeon ROCm 的重要说明

容器：

```
amd-oneclick-base:rocm7.2.1-py3.12-v20260416
```

已经预配置了 ROCm 和 vLLM 环境。AMD 文档介绍了通过 ROCm 使用与 OpenAI 兼容的 API 进行 vLLM 服务。（[ROCm 文档][3]）

通常你**不需要**使用：

```bash
python -m vllm.entrypoints.openai.api_server
```

因为 `vllm serve` 是当前推荐的接口。（[vLLM][1]）

---

在 Radeon Cloud 上进行首次测试的好选择：

```
vllm serve Qwen/Qwen3-8B --host 0.0.0.0 --port 8000 --dtype float16
```

部署完成后，你应该会得到：

```
https://<space-id>/8000/v1
```

然后测试：

```bash
curl https://<space-id>/8000/v1/models
```

或使用 Python：

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

参考资料：

* （[vLLM][1]）
* （[ROCm 文档][3]）
* （[Mintlify][2]）

[1]: https://docs.vllm.ai/en/latest/cli/index.html?utm_source=chatgpt.com "vLLM CLI Guide - vLLM"
[2]: https://www.mintlify.com/vllm-project/vllm/api/cli/serve?utm_source=chatgpt.com "vllm serve - vLLM"
[3]: https://rocm.docs.amd.com/projects/ai-ecosystem/en/latest/inference/vllm.html?utm_source=chatgpt.com "vLLM inference and serving on ROCm — AMD ROCm AI Ecosystem"
