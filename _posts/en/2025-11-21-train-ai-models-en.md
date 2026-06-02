---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Train AI Models on 12GB VRAM
translated: false
type: note
---

Here are some truly "hard-core" open-source projects you can fully train (or fine-tune large parts of) on a single RTX 4070 (12 GB VRAM). They’re excellent for deeply understanding how things actually work under the hood — way beyond just running demos.

| Project | Type | Why it’s educational & hard-core | Approx. VRAM needed for training | Rough training time on 4070 | Link |
|---------|------|----------------------------------|-------------------------------------|-----------------------------|------|
| Karpathy’s **nanoGPT** (you already know) | LLM (GPT-2 style from scratch) | The gold standard “minimal clean code” GPT | ~10 GB for 124M model | hours | https://github.com/karpathy/nanoGPT |
| Karpathy’s **minGPT** | LLM | Even smaller, great for debugging every single line | <6 GB | minutes–hours | https://github.com/karpathy/minGPT |
| Karpathy’s **llm.c** | Raw CUDA GPT-2 | Train a decent GPT-2 entirely in raw CUDA (no PyTorch). Insanely educational for low-level GPU programming | 8–10 GB (124M model) | 1–3 days for 124M on Shakespeare | https://github.com/karpathy/llm.c |
| OpenLLaMA / LLaMA-Adapter / Lit-GPT (fine-tuning) | LLM fine-tuning | Fine-tune 3B–7B models with LoRA/QLoRA on one 4070 | 7B QLoRA ≈ 8–10 GB | few hours on Alpaca/ShareGPT | https://github.com/Lightning-AI/lit-gpt |
| Hiero **OpenDiT** / **PixArt-alpha** | DiT-based text-to-image (Stable Diffusion alternative trained from scratch) | Train a Diffusion Transformer from scratch instead of U-Net. Modern SOTA architecture | 24M DiT ≈ 10–11 GB with gradient checkpointing | 1–2 weeks on LAION aesthetics subset | https://github.com/NVIDIA/OpenDiT |
| **Stable Diffusion from scratch** (tiny versions) | U-Net diffusion | Several repos let you train tiny SD models (instead of just fine-tuning) | 64×64 tiny SD ≈ 6–9 GB | days | https://github.com/tea-mang/nano-diffusion, https://github.com/huggingface/diffusers (see training examples) |
| **BitNet** (1-bit Transformers) | 1-bit LLM | Microsoft’s 1-bit weights models. Train your own BitNet b1.58 (like LLaMA but ternary weights) | 3B model fits in <6 GB | hours–days | https://github.com/microsoft/BitNet |
| **Mamba** (state-space models) | Next-gen architecture after Transformers | Very hot alternative to Transformers. Train your own Mamba from scratch | 130M–2.8B models fit easily | hours | https://github.com/state-spaces/mamba (training scripts included) |
| **RWKV** (RNN that scales like Transformer) | Raven / Eagle / Finch models | Train a real recurrent model that behaves like a Transformer but uses constant VRAM | 3B–7B training possible on 12 GB with chunkwise | days | https://github.com/BlinkDL/RWKV-LM |
| **Grok-1** open-weights clone attempts (340B mixture-of-experts) | MoE from scratch understanding | You can’t train the full 314B, but you can train tiny MoE versions and understand routing | 8-expert tiny MoE ≈ 10 GB | hours | https://github.com/cg123/mergekit (build your own Frankenstein MoE) + https://github.com/EleutherAI/gpt-neox for MoE code |
| **RetNet** (Microsoft’s Transformer replacement) | Retention networks | Another strong Transformer alternative | similar to Mamba | | https://github.com/microsoft/torchscale (includes RetNet training) |

### My personal top-5 “most educational & doable on 4070” ranking

1. **llm.c** – Train GPT-2 in pure C+CUDA. Nothing teaches you backprop, kernels, flash-attention implementations better.
2. **Mamba** – Because state-space models are probably the future and the code is clean.
3. **BitNet b1.58** – Training 1-bit LLMs is mind-blowing and extremely VRAM efficient.
4. **OpenDiT / PixArt-alpha** – If you want diffusion but with modern transformer backbones instead of 2015 U-Net.
5. **RWKV** – Recurrent architecture that beats same-size Transformers and trains linearly.

All of these run comfortably on a single RTX 4070 (sometimes with flash-attention, bitsandbytes/QLORA, gradient checkpointing, or the new chunkwise RWKV tricks).

Pick one and go deep — you’ll come out understanding these models at a level most researchers never reach. Happy hacking!
