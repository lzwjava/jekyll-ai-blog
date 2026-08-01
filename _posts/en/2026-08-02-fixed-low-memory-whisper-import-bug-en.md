---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixed low-memory whisper import bug
translated: false
type: note
---

Fixed and verified. Here's the full picture:

## Root cause

`ww` is installed as a global console script (`/home/lzw/.local/bin/ww`) running under **system python3.11**, while the ML deps live in the project venv. The plain `ww whisper` worked because it shells out to the `whisper` CLI (installed in system python), but `--low-memory` did `import whisper` **inside the `ww` interpreter** — where openai-whisper was never installed. (`ww whisper diarize` had the same latent bug with `whisperx`.)

## What I changed

**`ww/audio/whisper_low_mem.py`** — rewrote the low-memory path to use **faster-whisper** instead of openai-whisper, and added a `_ensure_deps()` guard that re-execs the script with the project venv python if deps are missing in the running interpreter. Same CLI surface (`--model/--language/--task/--device`) plus new `--compute-type` (auto/float16/int8) and `--no-proxy` (HF downloads can stall through your local proxy — same reason `diarize` unsets it). Still writes `.txt/.srt/.vtt/.tsv/.json` like before.

**`ww/audio/whisper_diarize.py`** — added the same venv re-exec guard (would have crashed the same way).

**`ww/main.py`** — updated the `--low-memory` help text.

Verified end-to-end through the real `ww` entry point; ruff/pyright clean (only pre-existing findings remain).

## Your questions

**Why was openai-whisper needed?** Only for the default `ww whisper` path — it invokes the openai-whisper CLI, which you have installed globally, so that path works. It's no longer needed for `--low-memory`.

**Why not whisperx for low-memory?** whisperx *is* faster-whisper under the hood — it's just faster-whisper plus wav2vec2 word-level alignment (+~1.2 GB VRAM and an extra download) plus optional pyannote diarization (HF token + models). Plain transcription needs none of that; the engine alone is the memory-efficient part, so that's what `--low-memory` now uses directly. Use `ww whisper diarize` when you actually want speaker labels.

**Note:** `large-v3` will now be downloaded from HuggingFace (`Systran/faster-whisper-large-v3`, ~3 GB) on first run — separate cache from your existing `~/.cache/whisper/*.pt` files. If the download stalls behind your proxy, add `--no-proxy`.

One heads-up: your first real run with `--low-memory` on `ruixiu2.mp4` will be slower only because of that model download.
