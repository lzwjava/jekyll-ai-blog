---
audio: false
generated: true
image: false
lang: en
layout: post
title: RX 7900 XTX for AI/ML Work
translated: false
type: note
---

Question: What's the RX 7900 XTX like, particularly for AI/ML work?

Answer:

**Hardware (RDNA3, gfx1100):**

- 96 CUs, 24GB GDDR6 @ 960 GB/s, 355W TBP
- 61 TFLOPS FP32, no dedicated tensor cores — matrix ops go through WMMA on shader cores (weaker than Nvidia's Tensor Cores per-FLOP, but 24GB VRAM is the actual selling point)
- 5nm TSMC, chiplet MCD/GCD design like Zen

**Current price/perf context (mid-2026):** DRAM/GDDR shortage pushed everything up — new cards now run ~$1,100-1,400, used ~$750-850, but Nvidia inflated harder (4090 hit $1,800-2,700+, 5090 $3,000+), so relative value actually improved for the XTX.

**Software stack — this is what matters for you:**

ROCm has moved to the 7.2.x line (7.2.4 is latest patch), a single combined Windows+Linux release that auto-detects RDNA 3, RDNA 4, and Strix Halo. gfx1100 (your card) stays officially supported.

Setup on Ubuntu:

```bash
# ROCm 7.2 install
sudo apt update
wget https://repo.radeon.com/amdgpu-install/latest/ubuntu/noble/amdgpu-install_<version>_all.deb
sudo apt install ./amdgpu-install_*.deb
sudo amdgpu-install --usecase=rocm,hiplibsdk -y

# verify
rocminfo | grep gfx
rocm-smi
```

PyTorch (ROCm wheel):

```bash
pip install torch --index-url https://download.pytorch.org/whl/rocm6.2
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"
```

(HIP presents as `torch.cuda.*` — no code changes needed vs CUDA scripts, that's the whole point of HIP)

**llama.cpp (best inference path):**

```bash
git clone https://github.com/ggerganov/llama.cpp && cd llama.cpp
cmake -B build -DGGML_HIP=ON -DAMDGPU_TARGETS=gfx1100 -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release -j
```

Real numbers: Llama 3.1 8B runs ~96 tok/s on the 7900 XTX — about 75% of an RTX 4090's throughput at a fraction of the price.

**Gaps vs CUDA:**

- FlashAttention's ROCm fork now spans RDNA 3 and RDNA 4 — forward pass works on gfx11, but full backward pass is CDNA-only (so training/fine-tuning with FA2 is limited; inference is fine)
- vLLM works via ROCm Docker images but expect more friction than Nvidia
- For training at scale you'd still reach for MI300X (which you already have) — the 7900 XTX is really a **local inference / dev box** card, not a training card

**Bottom line for your setup:** given you're already on MI300X for training, a 7900 XTX box makes sense as a cheap local inference rig for testing your GPT-2/agent stuff without burning cluster time — 24GB fits quantized 32-70B models comfortably.

References:

- [ROCm Local LLM Setup 2026 — 96 tok/s benchmarks](https://localaimaster.com/blog/amd-rocm-local-llm-setup)
- [RX 7900 XTX for Local AI 2026 guide](https://localaimaster.com/blog/radeon-7900-xtx-local-ai)
- [AMD ROCm Supported GPUs 2026](https://www.kunalganglani.com/blog/rocm-consumer-gpu-cuda-alternative-2026)
