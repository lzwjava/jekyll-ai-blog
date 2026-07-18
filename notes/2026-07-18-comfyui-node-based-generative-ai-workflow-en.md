---
audio: false
generated: true
image: false
lang: en
layout: post
title: "ComfyUI: Node-Based Generative AI Workflow"
translated: false
type: note
---

Question: What is ComfyUI?

Answer:

ComfyUI is a **node-based graphical interface for generative AI image/video/audio workflows**, mainly used for running and building pipelines around diffusion models such as Stable Diffusion, FLUX, ControlNet, LoRA, IP-Adapter, AnimateDiff, etc.

Think of it like **PyTorch for visual AI, but with a graph editor**.

Instead of writing:

```python
prompt
  -> text encoder
  -> diffusion model
  -> sampler
  -> VAE decoder
  -> image
```

you build the same pipeline visually:

```
[Load Checkpoint]
        |
        v
[CLIP Text Encode] <--- prompt
        |
        v
[KSampler]
        |
        v
[VAE Decode]
        |
        v
[Save Image]
```

Each box is a node. You connect tensors between nodes.

---

## Why people use ComfyUI

### 1. Full control over inference graph

A normal app:

```
prompt -> image
```

ComfyUI:

```
prompt
 |
CLIP
 |
positive conditioning
 |
ControlNet
 |
LoRA
 |
IP Adapter
 |
Sampler
 |
Scheduler
 |
VAE
 |
Image
```

You can modify every step.

This is similar to:

* TensorFlow graph mode
* Unreal Blueprint
* Blender node editor
* LangGraph for agents

---

## 2. Reproducible workflows

A ComfyUI workflow is just JSON.

Example:

```json
{
  "nodes": [
    {
      "type": "CheckpointLoader",
      "model": "flux-dev"
    },
    {
      "type": "KSampler",
      "steps": 30,
      "cfg": 4
    }
  ]
}
```

You can share the JSON and somebody else gets the same pipeline.

This is why researchers and creators like it.

---

## 3. It runs locally

Typical setup:

```
GPU
 |
CUDA / ROCm
 |
PyTorch
 |
ComfyUI
 |
Models
```

Example:

```bash
git clone https://github.com/comfyanonymous/ComfyUI

cd ComfyUI

pip install -r requirements.txt

python main.py
```

Open:

```
http://localhost:8188
```

---

## Hardware requirements

Roughly:

| GPU             | Experience                          |
| --------------- | ----------------------------------- |
| RTX 3060 12GB   | OK                                  |
| RTX 4070 12GB   | good                                |
| RTX 3090 24GB   | excellent                           |
| RX 7900 XT 20GB | possible (ROCm)                     |
| MI50 16GB       | technically interesting but painful |
| H100            | overkill                            |

Your RTX 4070 + MI50 experiments are relevant:

* RTX 4070 → easiest ComfyUI experience
* MI50 → ROCm compatibility experiment, not practical daily generation

---

## Popular workflows

### Text → Image

```
Prompt
 |
FLUX / SDXL
 |
KSampler
 |
Image
```

### Image → Image

```
Input photo
 |
VAE Encode
 |
Diffusion
 |
VAE Decode
 |
New image
```

### Character consistency

```
Reference image
       |
IP Adapter
       |
LoRA
       |
FLUX/SDXL
       |
Generated character
```

### Video generation

```
Text
 |
AnimateDiff / Wan / CogVideo
 |
Frames
 |
Video
```

---

## ComfyUI vs Automatic1111

|                    | ComfyUI   | Automatic1111 |
| ------------------ | --------- | ------------- |
| Beginner friendly  | ❌         | ✅             |
| Control            | ⭐⭐⭐⭐⭐     | ⭐⭐⭐           |
| Research workflows | ⭐⭐⭐⭐⭐     | ⭐⭐            |
| Automation         | ⭐⭐⭐⭐⭐     | ⭐⭐            |
| API usage          | Excellent | OK            |
| Complex pipelines  | Excellent | Limited       |

For an engineer, ComfyUI is usually the better choice.

---

## Why it matters for AI engineers

ComfyUI is basically a **visual programming language for generative models**.

The important concept:

LLM:

```
tokens
 ↓
Transformer
 ↓
tokens
```

Diffusion:

```
noise
 ↓
UNet / DiT
 ↓
denoised latent
 ↓
image
```

ComfyUI exposes the whole forward pass.

For someone doing model training/inference, it is useful because you can experiment with:

* different samplers
* conditioning methods
* LoRA merging
* quantized models
* ControlNet
* image/video pipelines

without writing a whole application.

---

Given your background (nanoGPT, ROCm, GPU experiments), ComfyUI is probably worth trying. The interesting part is not the UI — it is understanding the **diffusion computation graph** and swapping components like you would swap Transformer blocks.
