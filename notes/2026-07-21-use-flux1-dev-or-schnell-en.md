---
audio: false
generated: true
image: false
lang: en
layout: post
title: Use FLUX.1-dev or Schnell
translated: false
type: note
---

Question: Which recovery option should I choose after FLUX.2-dev OOM on Radeon Cloud 48GB VRAM?

Answer:

Choose **Option 2: Try a smaller model like FLUX.1-dev**.

Reasoning:

* Your GPU is **48GB VRAM** (likely AMD MI300-class partition / Radeon Cloud).
* `FLUX.2-dev` is a very large diffusion transformer:

  * BF16 weights alone ≈ 60GB+
  * Full checkpoint ≈ 166GB on disk
  * Runtime memory is higher because you need:

    * model weights
    * activations
    * attention KV/state
    * VAE
    * text encoder(s)

Even CPU offload will be painful because AMD ROCm + diffusion offload is less mature than CUDA.

Your goal is probably the AMD Hackathon multimodal track. A working demo beats fighting the biggest model.

Recommended path:

```
2. FLUX.1-dev
```

Then optimize:

### Option A (best balance)

Use:

```
FLUX.1-dev + fp16/bf16
```

Expected:

* Disk: ~23GB
* VRAM: ~24-32GB depending on pipeline
* Fits 48GB comfortably

### Option B (best for demo speed)

Use:

```
FLUX.1-schnell
```

Pros:

* 1-4 steps generation
* much faster
* easier realtime demo

Cons:

* lower quality than dev

For hackathon judging, I would choose:

```
FLUX.1-schnell
        +
Qwen3-8B / Qwen-VL captioning
        +
Gradio/FastAPI demo
```

A complete creative workflow scores higher than a huge model that crashes.

Avoid:

* ❌ Option 4 CPU offload only

  * It may technically load, but generation latency could become minutes/image.
* ❌ Option 3 bitsandbytes 4-bit

  * bitsandbytes is mainly CUDA ecosystem; ROCm support is not the smooth path.
* ❌ Option 1 FP8

  * Interesting, but FLUX FP8 support on AMD is not the path I would bet a hackathon demo on.

After restart, I would cleanly switch:

```bash
pip install diffusers transformers accelerate sentencepiece
```

Then test:

```python
from diffusers import FluxPipeline
import torch

pipe = FluxPipeline.from_pretrained(
    "black-forest-labs/FLUX.1-schnell",
    torch_dtype=torch.bfloat16
)

pipe.to("cuda")

image = pipe(
    "a futuristic AI robot running on AMD Radeon GPU",
    num_inference_steps=4
).images[0]

image.save("test.png")
```

For your AMD GPU demo, a stable FLUX.1-schnell pipeline + agent workflow is likely a stronger submission than FLUX.2-dev.
