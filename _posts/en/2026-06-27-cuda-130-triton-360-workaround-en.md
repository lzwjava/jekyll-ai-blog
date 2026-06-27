---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA 13.0 Triton 3.6.0 Workaround
translated: false
type: note
---

CUDA 13.0 (driver 580.126.20) + Triton 3.6.0 — the downgrade to 3.4.0 got reverted by pip dependency resolution. This is a bleeding-edge combo known to cause segfaults with Triton JIT.

Two clean paths:

**Path A — vLLM (recommended, more stable on consumer GPUs):**

```
/home/lzw/sglang-venv/bin/pip install vllm
/home/lzw/sglang-venv/bin/python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-1.5B-Instruct --port 30000 --host 0.0.0.0
```

**Path B — sglang without Triton (pin triton with --no-deps):**

```
/home/lzw/sglang-venv/bin/pip install --no-deps triton==3.4.0
```

Then retry sglang with `--attention-backend torch_native --disable-cuda-graph`.

vLLM is the safer bet — it's more battle-tested on RTX 4070 and CUDA 13.0. Want me to try installing and launching it?
