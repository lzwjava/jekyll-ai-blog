---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fixing Pyannote Torchcodec Warning and Diarization
translated: false
type: note
---

Fixed. Here's the full picture of what that warning was and what I changed.

## Root cause

The warning is not a whisperx problem — it's pyannote.audio ≥ 4 trying to import **torchcodec** (its audio decoder) and failing:

- torchcodec 0.7.0 is installed and is the correct version for torch 2.8.0. It ships one `.so` set per FFmpeg major (4–7). On your machine the FFmpeg-6 variant matches the system `libav*`, and its core + pybind libs load fine — but its **custom-ops lib also links `libpython3.11.so.1.0`**, and that file doesn't exist anywhere on this box (`/usr/bin/python3.11` is Ubuntu's *static* ESM build, no `libpython3.11`/`-dev` package installed). So torchcodec refuses to load and pyannote prints that scary warning on every run.
- It was *cosmetic* for `ww whisper diarize` (whisperx preloads audio in-memory so pyannote never decodes by path), but it also meant pyannote genuinely could not decode audio files if any code path needed it.

## Changes made (`ww/audio/whisper_diarize.py`, +88/−9)

1. **torchcodec now loads** — `_prepend_libpython_dir()` locates an ABI-compatible `libpython3.11.so.1.0` under uv/pyenv-managed Pythons and puts it on `LD_LIBRARY_PATH` before re-exec'ing into the venv. I installed one via `uv python install 3.11` (`~/.local/share/uv/python/cpython-3.11.15-.../lib`). Verified: pyannote imports with zero warnings and decodes the mp3 via torchcodec.
2. **Diarization was silently skipping** — your run printed `[1/2]`, not `[1/3]`: the script only diarized if `HF_TOKEN` was set, and it isn't (you *are* logged in via `~/.cache/huggingface/token`). It now falls back to that cached token.
3. **Proxy was being killed** — `_disable_proxy()` ran unconditionally, but this machine has **no direct route to huggingface.co** (only via your `127.0.0.1:7890` proxy), so model downloads died with "Network is unreachable". Proxy handling is now opt-in via `--no-proxy` (matching `whisper_low_mem.py`'s convention).
4. **`--diarize-model` passthrough** — whisperx 3.8.6 hardcodes `pyannote/speaker-diarization-community-1`; you can now point at `pyannote/speaker-diarization-3.1` instead.

Verified end-to-end on a 20s clip: no torchcodec warning, token auto-detected (`[1/3]`), transcription runs, diarization reaches HF through the proxy.

## One thing only you can do

The remaining blocker is **gated HF repos** (403, not a code issue). Your cached token isn't authorized for the pyannote models, so accept access in your browser while logged in as the same account as `~/.cache/huggingface/token` (token starts `hf_m...`):

- https://huggingface.co/pyannote/speaker-diarization-community-1 (whisperx's default — **this one is required**; pyannote's 3.1 pipeline pulls its xvec/PLDA assets from here too)
- https://huggingface.co/pyannote/segmentation-3.0 (underlying segmentation model)
- https://huggingface.co/pyannote/speaker-diarization-3.1 (only if you use `--diarize-model`)

Then just run it again:

```
ww whisper diarize daniel.mp3
```

The `TF32` reproducibility warning and the Lightning "checkpoint upgrade" notice in the logs are harmless pyannote noise and can be ignored.
