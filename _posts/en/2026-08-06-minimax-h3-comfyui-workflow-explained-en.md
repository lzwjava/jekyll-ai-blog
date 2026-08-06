---
audio: false
generated: true
image: false
lang: en
layout: post
title: MiniMax H3 ComfyUI Workflow Explained
translated: false
type: note
---

Question: How does this MiniMax H3 ComfyUI workflow actually work end-to-end — model arch, node graph mechanics, and what each stage does?

Answer:

Your breakdown is accurate. Here's the model + pipeline mechanics underneath it.

**Model architecture** — MiniMax H3 is a 33.1B dense single-stream omni transformer with a Qwen3-VL-32B text encoder, open-sourced on August 3, 2026 under the MiniMax H3 Community License Agreement. The open release ships two task checkpoints: FL2VA (text-to-video and first/last-frame conditioning) and Ref2VA (reference-based generation) — your file uses Ref2VA (`minimax_h3_ref2va_pruned_int8_convrot.safetensors`), which explains why the workflow has image-reference and multi-image-reference pipelines but no first/last-frame variant.

Key design choices (relevant to why the graph is shaped this way):

- Uses three-dimensional Multimodal Rotary Position Embeddings (MM-RoPE) to represent positional relationships across the temporal and two spatial dimensions, (t, h, w) — this is why resolution/frame-count fields feed directly into conditioning, not just the sampler.
- Modality-specific AdaLN improves generation quality with relatively low additional training and inference costs — the "pruned INT8" checkpoint you have specifically precomputes adaLN curve tables, ~40% smaller.
- Audio isn't bolted on: 32 kHz stereo generated in the same pass as the picture, no separate audio model — hence the separate audio VAE (`minimax_h3_audio_vae_fp32.safetensors`) decoding from the same latent, not a post-hoc TTS/foley step.
- 2K output isn't a super-res module: for H3's 2K-resolution output, instead of using a conventional dedicated super-resolution module, we use the H3 base model to regenerate its own low-resolution result through an in-context manner. That regen step (`H3-Regenerate-2K`) is API-only per the ComfyUI wiki — the H3-Context-IR preprocessing system and the H3-Regenerate-2K upscaling module remain hosted APIs — so your local workflow caps at the base 768p, not 2K, unless you pipe out to their hosted endpoint.

**Graph mechanics (why each block exists):**

```
Models          → load UNET (diffusion transformer) + CLIP (Qwen3VL-32B text enc) + video VAE + audio VAE
Conditioning    → text prompt / image refs / multi-image refs → encoded via CLIP → MM-RoPE-aware embedding
Sampling        → diffusion transformer denoise loop, conditioned on above + ResolutionSelector output
Decode+Create   → video VAE decode latents → frames; audio VAE decode → waveform; mux via VideoHelperSuite/KKVideo
User Inputs     → prompt text, resolution pick, frame count (124 @ match mode = ~5s at 24-25fps)
Prompt templates→ 提示词模版 group is just a static text block feeding an LLM (external, via API node or manual)
                  to expand your short prompt into H3's expected structured director-style prompt
Switch (开关)   → rgthree Fast Groups Bypasser — literally just disables/enables node groups so you can
                  keep 3 pipelines (t2v, single-ref, multi-ref) in one JSON and toggle which subgraph runs
                  without rewiring
```

The "prompt templates" aren't a ComfyUI node feature — they're just text blobs meant to be pasted into an LLM chat (or wired to an API-call node if you have one) because H3 responds much better to structured, shot-list-style prompts (camera, subject, lighting, motion) than to a single terse sentence. Given prompts run up to 7,000 characters, the templates exist to help you actually fill that budget instead of wasting the model's context window.

**To actually run it**, you need:

```bash
# custom nodes
git clone https://github.com/Comfy-Org/ComfyUI.git  # H3 support merged directly (PR #15224)
# or if using a separate node pack:
comfy node install rgthree-comfy
comfy node install comfyui-videohelpersuite

# models (from Comfy-Org/MiniMax-H3 repackaged repo)
models/diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors
models/text_encoders/qwen3vl_32b_minimax_h3_int8_convrot.safetensors
models/vae/minimax_h3_video_vae_fp16.safetensors
models/vae/minimax_h3_audio_vae_fp32.safetensors
```

Given you're running MI300X locally already — pruned INT8 + int8 text encoder should fit comfortably in one GPU's VRAM even at 768p/124 frames; the dense 33B transformer is the memory bottleneck, not the VAEs.

Native support landed the same day as open-sourcing: with native ComfyUI support merged the same day (Comfy-Org/ComfyUI #15224), so this workflow file is current, not stale community scaffolding around an older API.

References:

- [MiniMax H3 Open Source Announcement](https://www.minimax.io/news/minimax-h3-open-source)
- [MiniMax H3 ComfyUI Wiki — native support, checkpoints](https://comfyui-wiki.com/en/models/minimax)
- [MiniMax H3 on fal.ai — capabilities, prompt length](https://fal.ai/minimax-h3)
- [MiniMax H3 Developer Guide](https://blog.4sapi.com/blog/minimax-h3-open-source-video-model)
