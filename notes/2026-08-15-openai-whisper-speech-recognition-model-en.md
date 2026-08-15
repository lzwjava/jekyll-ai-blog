---
audio: false
generated: true
image: false
lang: en
layout: post
title: "OpenAI Whisper: Speech Recognition Model"
translated: false
type: note
---

This is **OpenAI's Whisper** — a general-purpose speech recognition model and codebase. Specifically:

**What it does**
- **Multilingual speech recognition** (99 languages) into text
- **Speech translation** (non-English speech → English text)
- **Language identification** and voice activity detection
- All handled by a single Transformer sequence-to-sequence model, using special tokens as task specifiers (see `approach.png` / `language-breakdown.svg` in the repo)

**Key facts**
- Uses OpenAI's `tiktoken` tokenizer, PyTorch, and requires `ffmpeg` for audio decoding
- Ships **6 model sizes**: `tiny`, `base`, `small`, `medium`, `large`, and `turbo` (an optimized `large-v3`), some with English-only variants (e.g. `tiny.en`)
- Used via CLI (`whisper audio.mp3 --model turbo`) or as a Python package (`whisper.load_model(...)` / `transcribe`)

**The code layout** (`whisper/` directory, ~14 source files):
- `model.py` — Transformer model definition
- `transcribe.py` — the transcription pipeline (segmentation, VAD-style detection)
- `decoding.py` — beam search / greedy decoding and logit processing
- `audio.py` — audio loading via ffmpeg
- `tokenizer.py` — tokenizer setup
- `timing.py` — word-level timestamps (DTW-based)
- `triton_ops.py` — optional NVIDIA Triton CUDA kernels for speed

**Repo state**
- Clean working tree on `main`, up to date with `origin/main`
- Recent commits include JSONL output support, SDPA cross-attention fixes for beam search, and a security fix for `torch.load` (`weights_only=True`) — plus a `Release 20250625` tag
- Also has tests, notebooks (e.g. LibriSpeech example), and a model card

It's the official OpenAI Whisper codebase (MIT-licensed), ready to use for speech-to-text tasks.
