---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD Radeon Cloud Instance Recovery
translated: false
type: note
---

## Complete Summary — AMD Radeon Cloud Instance

### 1. Initial Problem: SSH Connection Failed

You tried to connect to `36.150.116.206:31094` — got **Connection refused**.

**Diagnosis:**
- ✅ Host **was reachable** (39ms ping via DMIT jump host)
- ❌ Port 31094 **not open**
- ✅ **Other ports** open nearby: **31090, 31091, 31092, 31095, 31098, 31099, 31100**
- Found SSH on **31090, 31098, 31100** but **key not authorized**
- Your `~/.ssh/config` has a catch-all SOCKS5 proxy, so SSH was routing through proxy — we bypassed with `ProxyCommand=none`

### 2. Discovered the API Endpoint

You tested the API:
```bash
curl https://radeon-global.anruicloud.com/spaces/u-9758-811746f0/8000/v1/chat/completions
```
✅ **Qwen3-8B** responded successfully via the **AMD Radeon Cloud proxy**.

### 3. SSH Port 31154 Worked

You connected via `ssh -p 31154` — got in with your key.

**Server Specs:**
| Component | Value |
|-----------|-------|
| **OS** | Ubuntu 24.04 LTS |
| **CPU** | 2× AMD EPYC 9334 (128 threads) |
| **RAM** | 503 GiB |
| **GPU** | AMD Radeon Graphics (gfx1100, RDNA 3) — **48 GB VRAM** |
| **ROCm** | 7.2.1, Driver 6.16.13 |
| **PyTorch** | 2.9.1 (ROCm build, in `/opt/venv`) |
| **Disk** | `/` = 3.5TB overlay, `/workspace` = 98GB loop |

GPU compute test: ✅ **Passed** (HIP vector add, 48GB accessible, 96 CUs)

### 4. Tried FLUX.2-dev — Too Large (Crashed)

- Model: **32B parameters**, **166GB** total
- Downloaded via `hf-mirror.com` with `hf_transfer` — **252 seconds** (~660MB/s)
- Tried inference with CPU offloading: **OOM crash** ❌
  - The **transformer alone is 60GB** in BF16
  - Only 48GB VRAM available
  - **SSH daemon died** when container got OOM-killed

### 5. Instance Restarted — SSH Broken

After the OOM crash, the container restarted but SSH was **not running** internally (it was cloud-proxied, not real SSH). You gained access through **Jupyter Lab terminal** at:
- `https://radeon-global.anruicloud.com/spaces/u-9758-811746f0/` (port 8888, token: `amd-oneclick`)

### 6. Current State (in Jupyter terminal)

| Item | Status |
|------|--------|
| Jupyter terminal | ✅ **You're in** |
| SSH server | ❌ Not installed (we tried `apt install openssh-server` + `mkdir -p /run/sshd`, but cloud proxy port mapping is stale) |
| FLUX.2-dev | Still on disk at `/FLUX.2-dev` (166GB) |
| `/workspace` disk | 98GB (19GB free) — too small |
| `/` disk | 3.5TB (2.8TB free) ✅ |

### 7. What's Next: FLUX.1-dev

Since you're in the Jupyter terminal, I can still help you run FLUX.1-dev — it's **12B params** (~35GB total, needs ~24GB VRAM at FP16) and will **fit comfortably** on your 48GB GPU.

**From the Jupyter terminal, paste:**

```bash
rm -rf /FLUX.2-dev && export PATH=/opt/venv/bin:$PATH && export HF_ENDPOINT=https://hf-mirror.com && export HF_HUB_ENABLE_HF_TRANSFER=1 && python3 -c "
from huggingface_hub import snapshot_download
print('Downloading FLUX.1-dev...')
snapshot_download('black-forest-labs/FLUX.1-dev', local_dir='/FLUX.1-dev')
print('Done!')
"
```

Once downloaded, run:
```bash
export PATH=/opt/venv/bin:$PATH && cd /workspace && python3 -c "
import torch
from diffusers import FluxPipeline
pipe = FluxPipeline.from_pretrained('/FLUX.1-dev', torch_dtype=torch.bfloat16)
pipe.enable_sequential_cpu_offload()
image = pipe('A cute cat on Mars', num_inference_steps=28).images[0]
image.save('flux_output.png')
print('Saved!')
"
```
