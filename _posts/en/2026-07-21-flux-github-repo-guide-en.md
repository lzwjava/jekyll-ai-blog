---
audio: false
generated: true
image: false
lang: en
layout: post
title: FLUX GitHub Repo Guide
translated: false
type: note
---

Question: What's the FLUX GitHub repo?

Answer:

The official FLUX repo is:

[Black Forest Labs FLUX GitHub repository](https://github.com/black-forest-labs/flux?utm_source=chatgpt.com)

GitHub:

```bash
git clone https://github.com/black-forest-labs/flux
cd flux
pip install -e ".[all]"
```

It contains the **official inference code** for FLUX.1 models from Black Forest Labs. ([GitHub][1])

Main structure:

```text
flux/
├── src/flux/
│   ├── model.py
│   ├── sampling.py
│   ├── util.py
│   └── cli.py
├── demo_st.py
├── demo_gr.py
├── pyproject.toml
└── model_licenses/
```

([GitHub][1])

The model family:

| Model          | Purpose                          | License                |
| -------------- | -------------------------------- | ---------------------- |
| FLUX.1-schnell | Fast generation                  | Apache 2.0             |
| FLUX.1-dev     | Higher quality                   | Non-commercial license |
| FLUX.1-Fill    | Inpainting/outpainting           | Non-commercial         |
| FLUX.1-Canny   | Edge control                     | Non-commercial         |
| FLUX.1-Depth   | Depth guided generation          | Non-commercial         |
| FLUX.1-Kontext | Image editing/context generation | Non-commercial         |

([GitHub][1])

For your AMD Radeon Cloud box (`gfx1100`, 48GB VRAM), I would start with **FLUX.1-schnell**.

Typical workflow:

```bash
# install
git clone https://github.com/black-forest-labs/flux
cd flux

python3 -m venv .venv
source .venv/bin/activate

pip install -e ".[all]"
```

Download weights from Hugging Face:

```text
black-forest-labs/FLUX.1-schnell
black-forest-labs/FLUX.1-dev
```

([GitHub][1])

Then run:

```bash
python demo_st.py \
  --name flux-schnell \
  --prompt "a cyberpunk city at night, cinematic lighting"
```

For AMD ROCm, the easier path is usually:

```
FLUX
  |
  +-- diffusers (HuggingFace)
  |
  +-- ComfyUI
  |
  +-- ROCm PyTorch
```

because ComfyUI has many optimizations and workflows.

Your 48GB VRAM should comfortably handle:

```
FLUX.1-schnell 1024x1024     ✅
FLUX.1-dev 1024x1024         ✅
FLUX LoRA inference          ✅
FLUX image editing            ✅
```

The interesting hackathon direction on that AMD GPU would be:

```
Qwen3-VL / LLM
        |
        v
 prompt + planning agent
        |
        v
      FLUX
        |
        v
 generated images/video assets
```

A local multimodal creative agent would fit this hardware very well.

[1]: https://github.com/black-forest-labs/flux?utm_source=chatgpt.com "GitHub - black-forest-labs/flux: Official inference repo for FLUX.1 models · GitHub"
