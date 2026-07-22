---
audio: false
generated: true
image: false
lang: en
layout: post
title: FLUX Image Generator Setup
translated: false
type: note
---

All set! Here's what's in the `flux/` directory:

| File | Purpose |
| ------ | --------- |
| `run_flux_schnell.py` | Main script — download & generate images |
| `requirements.txt` | Python dependencies (diffusers, torch, etc.) |
| `README.md` | Full documentation |

---

### Quick start

```bash
cd /mnt/data/zz/flux

# Install deps
python3 -m pip install --break-system-packages -r requirements.txt

# Run with your HF token
python3 run_flux_schnell.py --token hf_YOUR_TOKEN_HERE
```

### What the script does

1. **Downloads** the 12B‑parameter **FLUX.1-schnell** model from Hugging Face
2. **Generates** images from your text prompts (default: cat with sign, cyberpunk street, fantasy dragon)
3. **Saves** PNGs to `./outputs/`

### Important

⚠️ The model is **gated** — you must:

- Go to <https://huggingface.co/black-forest-labs/FLUX.1-schnell>
- Click **"Agree and access repository"**
- Create a token at <https://huggingface.co/settings/tokens>

Then pass it via `--token hf_xxxx` or `export HUGGING_FACE_HUB_TOKEN=hf_xxxx`.

### Key args

| Arg | Default | Description |
| ----- | --------- | ------------- |
| `prompts...` | 3 defaults | Text prompts |
| `--token` | env var | Hugging Face token |
| `--steps` | 4 | Inference steps (1–4) |
| `--seed` | 0 | Base seed (auto‑incremented per prompt) |

The script uses **bfloat16** + **CPU offloading** to fit the 12B model in limited VRAM. Schnell is distilled — it produces great results in just **1–4 steps** with `guidance_scale=0.0`.
