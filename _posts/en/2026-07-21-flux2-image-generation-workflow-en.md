---
audio: false
generated: true
image: false
lang: en
layout: post
title: FLUX.2 Image Generation Workflow
translated: false
type: note
---

Question: Explain `download_flux.py`, `run_flux.py`, and the `/workspace` files.

Answer:

This is a typical **Hugging Face Diffusers FLUX.2 image generation workflow**:

```
/workspace
├── download_flux.py     # download model weights
├── run_flux.py          # load model + generate image
├── FLUX.2-dev/          # downloaded model checkpoint
├── venv/                # Python virtual environment
└── lost+found/          # filesystem recovery directory
```

The flow is:

```
HuggingFace
    |
    | snapshot_download()
    v
/workspace/FLUX.2-dev
    |
    | Flux2Pipeline.from_pretrained()
    v
GPU memory (partially)
    |
    | pipe(prompt)
    v
flux_output.png
```

---

## 1. `download_flux.py`

Purpose:

**Download FLUX.2-dev model files from Hugging Face into local disk.**

```python
import os, time, subprocess
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
```

This changes Hugging Face endpoint:

Normally:

```
https://huggingface.co
```

becomes:

```
https://hf-mirror.com
```

Useful if huggingface.co is slow/unreachable.

---

### Import downloader

```python
from huggingface_hub import snapshot_download
```

`snapshot_download()` downloads an entire Hugging Face repository.

Similar to:

```bash
git clone https://huggingface.co/black-forest-labs/FLUX.2-dev
```

but optimized for model files.

---

### Download

```python
path = snapshot_download(
    "black-forest-labs/FLUX.2-dev",
    local_dir="/workspace/FLUX.2-dev",
    resume_download=True,
    local_dir_use_symlinks=False
)
```

Meaning:

Source:

```
black-forest-labs/FLUX.2-dev
```

Destination:

```
/workspace/FLUX.2-dev
```

Example structure:

```
FLUX.2-dev/
├── model_index.json
├── scheduler/
├── text_encoder/
├── transformer/
├── vae/
└── tokenizer/
```

The model is not one file.

A diffusion model consists of multiple components:

```
             prompt
               |
               v
        Text Encoder
               |
               v
       conditioning vectors
               |
               v
Random noise ---> Transformer ---> VAE Decoder
               |
               v
            image
```

---

### Resume download

```python
resume_download=True
```

If interrupted:

```
50GB model
downloaded 30GB
network fails
```

restart continues:

```
30GB -> 50GB
```

instead of restarting.

---

### Check size

```python
subprocess.run(["du", "-sh", path])
```

Equivalent:

```bash
du -sh /workspace/FLUX.2-dev
```

Example:

```
Size: 80G
```

---

# 2. `run_flux.py`

Purpose:

**Load FLUX.2-dev and generate an image.**

---

## Environment

```python
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"
```

Same mirror setting.

---

## Import PyTorch + Diffusers

```python
import torch
from diffusers import Flux2Pipeline
```

`Flux2Pipeline` is the high-level inference wrapper.

It combines:

```
Flux Transformer
+
Text Encoder
+
VAE
+
Scheduler
+
Tokenizer
```

into one API.

---

## Load model

```python
pipe = Flux2Pipeline.from_pretrained(
    "/FLUX.2-dev",
    torch_dtype=torch.bfloat16
)
```

Important:

Your model path:

```
/FLUX.2-dev
```

NOT:

```
/workspace/FLUX.2-dev
```

This means your image probably has:

```
/FLUX.2-dev
```

mounted already.

Check:

```bash
ls -lh /FLUX.2-dev
```

If not:

change to:

```python
pipe = Flux2Pipeline.from_pretrained(
    "/workspace/FLUX.2-dev",
    torch_dtype=torch.bfloat16
)
```

---

## Why bfloat16?

```python
torch_dtype=torch.bfloat16
```

FLUX is huge.

FP32:

```
1 parameter = 32 bits
```

BF16:

```
1 parameter = 16 bits
```

Memory:

```
FP32:
20B params × 4 bytes
≈80GB

BF16:
20B params × 2 bytes
≈40GB
```

Almost half VRAM.

---

# 3. CPU offload

```python
pipe.enable_sequential_cpu_offload()
```

This is the key line.

Without it:

```
GPU VRAM:

Text encoder
+
Transformer
+
VAE

all loaded

=> OOM
```

With offload:

```
CPU RAM
 |
 |
 v

Text encoder
      |
      v
GPU
      |
      v
remove

Transformer
      |
      v
GPU
      |
      v
remove

VAE
      |
      v
GPU
```

Only one component stays on GPU.

Tradeoff:

|       |            |
| ----- | ---------- |
| VRAM  | much lower |
| speed | slower     |
| RAM   | higher     |

Useful for Radeon 7900 / MI300 / small VRAM cards.

---

# 4. Generate image

```python
prompt = "A cute cat wearing a spacesuit on Mars, digital art"
```

Text prompt.

---

```python
image = pipe(
    prompt=prompt,
    num_inference_steps=28,
    guidance_scale=3.5,
).images[0]
```

The diffusion loop:

Start:

```
random noise

x_T
```

28 steps:

```
x_T
 |
 v
denoise
 |
 v
x_27
 |
 v
...
 |
 v
x_0
```

Finally:

```
latent
 |
 VAE decoder
 |
 RGB image
```

---

## `num_inference_steps`

```python
num_inference_steps=28
```

More steps:

```
10 steps
fast
lower quality

50 steps
slow
higher quality
```

28 is a reasonable default.

---

## `guidance_scale`

```python
guidance_scale=3.5
```

Controls prompt following.

Low:

```
2
|
more creative
less obedient
```

High:

```
8+
|
follows prompt strongly
sometimes artifacts
```

FLUX usually likes lower CFG compared with Stable Diffusion.

---

## Save

```python
image.save("/workspace/flux_output.png")
```

Output:

```
/workspace/flux_output.png
```

---

# 5. `venv`

```
venv/
```

Python virtual environment.

Usually contains:

```
venv/
├── bin/python
├── bin/pip
└── lib/python3.12/site-packages/
```

Activate:

```bash
source venv/bin/activate
```

Then:

```bash
python run_flux.py
```

uses the isolated packages.

---

# 6. `lost+found`

```
lost+found/
```

Normal Linux filesystem directory.

Created by `ext4`.

Used by:

```bash
fsck
```

for recovering orphaned files after disk corruption.

Ignore it.

---

## For your AMD Radeon Cloud setup

Given your previous server:

```
AMD Radeon Cloud
ROCm 7.2.1
AMD GPU
```

the important checks are:

```bash
rocminfo | head
```

and:

```bash
python -c "import torch; print(torch.cuda.is_available()); print(torch.version.hip)"
```

Expected:

```
True
7.2.x
```

Then:

```bash
python run_flux.py
```

should use ROCm.

The design here is specifically to make a huge FLUX model run on limited VRAM by trading speed for memory using `enable_sequential_cpu_offload()`.
