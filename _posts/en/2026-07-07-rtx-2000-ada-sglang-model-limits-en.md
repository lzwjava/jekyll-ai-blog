---
audio: false
generated: true
image: false
lang: en
layout: post
title: RTX 2000 Ada SGLang Model Limits
translated: false
type: note
---

Yes, the hardware summary is mostly correct, but there are a few important SGLang-specific caveats.

The key bottleneck is **VRAM**, not CPU/RAM/storage. RTX 2000 Ada has:

* 16 GB GDDR6 VRAM
* Compute Capability 8.9 (Ada, supports FP8 Tensor Core)
* PCIe workstation GPU, not a datacenter card

For SGLang serving, the realistic matrix is:

| Model       | Precision     | Fits?                | Practical Notes                       |
| ----------- | ------------- | -------------------- | ------------------------------------- |
| Llama 3 8B  | FP16          | ✅ Yes                | Good baseline                         |
| Qwen2.5 7B  | FP16/BF16     | ✅ Yes                | Probably best choice                  |
| Mistral 7B  | FP16          | ✅ Yes                | Good                                  |
| Qwen2.5 14B | FP16          | ❌ No                 | ~28GB weights                         |
| Qwen2.5 14B | INT8/FP8      | ⚠️ Maybe             | Need quantized checkpoint + KV tuning |
| Qwen2.5 32B | AWQ/GPTQ INT4 | ✅ Yes                | Probably sweet spot                   |
| Qwen2.5 72B | INT4          | ⚠️ Technically loads | Almost no KV cache, poor serving      |

The original estimate:

> FP16 7-8B
> INT4 30-34B

is the right practical range.

But:

> Qwen2.5-72B-AWQ ~14GB

is misleading for SGLang. The model weights may fit, but serving is not just weights.

Memory:

```
VRAM =
  model weights
+ CUDA kernels
+ activation buffers
+ KV cache
+ temporary workspace
```

For example:

Qwen2.5-72B-AWQ:

```
weights:       ~14GB
runtime:       ~1GB+
KV cache:      almost zero
```

You may load it, but:

```
context length: tiny
batch size: 1
throughput: bad
```

It becomes more like a demo than an API server.

---

For this machine I would test:

### Option 1: Best quality / practical

```
Qwen2.5-32B-Instruct-AWQ
```

SGLang:

```bash
python -m sglang.launch_server \
  --model-path Qwen/Qwen2.5-32B-Instruct-AWQ \
  --quantization awq \
  --host 0.0.0.0 \
  --port 30000 \
  --max-model-len 8192
```

Expected:

* good reasoning
* good coding
* acceptable latency

---

### Option 2: Fast production API

```
Qwen2.5-7B-Instruct
```

```bash
python -m sglang.launch_server \
  --model-path Qwen/Qwen2.5-7B-Instruct \
  --host 0.0.0.0 \
  --port 30000
```

You get:

* larger KV cache
* longer context
* higher concurrency

---

### Option 3: Coding model

```
Qwen2.5-Coder-14B-Instruct-AWQ
```

or

```
DeepSeek-Coder-V2-Lite-Instruct
```

with AWQ/INT4.

---

Before launching, check:

```bash
nvidia-smi

python - <<EOF
import torch
print(torch.cuda.get_device_name())
print(torch.cuda.get_device_capability())
EOF
```

Then install:

```bash
pip install "sglang[all]"
```

Test:

```bash
python -m sglang.launch_server \
  --model-path Qwen/Qwen2.5-7B-Instruct \
  --port 30000
```

Health check:

```bash
curl http://localhost:30000/health
```

---

One thing I would verify: **RTX 2000 Ada + SGLang compatibility**. SGLang uses FlashInfer/Triton kernels heavily; Ada CC 8.9 is supported, but some optimized kernels may have different performance compared with A100/H100.

For a RunPod hourly instance, I would benchmark:

1. Qwen2.5-7B FP16
2. Qwen2.5-14B AWQ
3. Qwen2.5-32B AWQ

using:

```bash
python -m sglang.bench_serving \
 --backend sglang \
 --dataset-name random \
 --num-prompts 100
```

That will tell the real tokens/sec and concurrency.
