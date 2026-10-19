---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang-Omni Audio Serving Framework
translated: false
type: note
---

**Question:** What is `sglang-omni` and what does it do?

**Answer:**

**SGLang-Omni** is a high-performance serving framework for audio models (TTS, ASR) and unified multimodal models, developed by the `sgl-project` organization. It's essentially an extension of the [SGLang](https://github.com/sgl-project/sglang) ecosystem targeting speech and omni-model workloads.

---

### Core Design

SGLang-Omni is a multi-stage serving runtime for omni, speech, and TTS models. Its design target is **multi-stage decoding**: generation split across heterogeneous stages with different compute patterns, dependency structures, and resource needs. It owns the pipeline topology, stage lifecycle, inter-stage transport, model-family integration layer, and OpenAI-compatible serving surface, while composing with SGLang for high-performance autoregressive scheduling and model execution where applicable.

---

### Key Architectural Pillars


- **Multi-stage runtime** — Models generation as coordinated stages: preprocessing, encoders, autoregressive engines, talkers, decoders, vocoders, and aggregators.
- **Stage-specialized scheduling** — Each stage runs behind a scheduler matched to its workload, from SGLang-backed autoregressive scheduling to lightweight preprocessing and streaming vocoder loops.
- **Transport-aware execution** — A control plane coordinates requests while a relay data plane moves tensor payloads across shared-memory, NCCL, NIXL, and Mooncake backends.
- **API surface** — OpenAI-compatible endpoints expose multimodal chat, speech generation, batch speech, streaming speech, uploaded voices, and transcription.


---

### What It Can Serve


- **Omni chat/speech**: Qwen3-Omni, Ming-Omni — multimodal input, text/audio output.
- **Music generation**: MiniMax Music 3 — lyrics + caption → 32 kHz stereo song.
- **TTS (Text-to-Speech)**: Higgs Audio v3, MOSS-TTS, Fish Speech S2-Pro, Qwen3-TTS, Voxtral TTS, and more — via `/v1/audio/speech`, batch, streaming, and uploaded voices.
- **ASR/Transcription**: Qwen3-ASR, Fun-ASR, ARK-ASR, MOSS-Transcribe-Diarize — via `/v1/audio/transcriptions`, with speaker labels and timestamps support.
- **SGLang-Omni Router**: A multi-worker OpenAI-compatible front door for health, readiness, lifecycle, and capability discovery.


---

### Hardware Support


| Backend | Status |
|---|---|
| NVIDIA CUDA | Fully supported (default, full model coverage) |
| Apple Silicon | Experimental (Qwen3-ASR via MLX or Torch MPS on macOS arm64) |
| Intel GPU (XPU) | Experimental (Intel Arc GPUs via PyTorch XPU) |


---

### In a Nutshell

SGLang-Omni fills a gap that the base SGLang framework doesn't cover: **multi-modal audio inference** (speech in, speech out, and everything in between). If SGLang is the backbone for LLM serving, SGLang-Omni is its specialized sibling for voice and audio-model pipelines — all behind a familiar OpenAI-compatible API.

---

**References:**
- [sgl-project/sglang-omni](https://github.com/sgl-project/sglang-omni)
- [Official Documentation](https://sgl-project.github.io/sglang-omni/)
- [SGLang (base framework)](https://github.com/sgl-project/sglang)
