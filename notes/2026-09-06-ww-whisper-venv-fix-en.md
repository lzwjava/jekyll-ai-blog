---
audio: false
generated: true
image: false
lang: en
layout: post
title: ww whisper venv fix
translated: false
type: note
---

Fixed and verified. Here's the full story:

## What was happening

`ww whisper` is a wrapper around **faster-whisper** (CTranslate2 backend), but it runs under your **system python3.11** (`/usr/bin/python3.11`, per the `ww` console script shebang), which has its own separate ML stack in `~/.local/lib/python3.11/site-packages`:
- `ctranslate2 4.5.0` — **old**. Its runtime loads cuDNN by versioned names (`libcudnn_ops.so.9.1.0`, etc.) and requires a cuDNN layout it can't find, then dies with:
  `Unable to load any of {...}` → `Invalid handle. Cannot load symbol cudnnCreateTensorDescriptor` → `Aborted (core dumped)`
- `faster-whisper 1.0.3` — also stale

Your project venv (`/home/lzw/projects/ww/.venv`) has the **working, pinned** versions — `ctranslate2 4.8.0` (no broken cuDNN dependency) + `faster-whisper 1.2.1`. I confirmed the exact same transcribe runs fine under `.venv/bin/python` and crashes only through the `ww` wrapper.

**Why the wrapper didn't use the venv:** the `_ensure_deps()` helper in the whisper scripts only re-exec'd into the venv when a module was *missing*. Your system python *has* these packages — just old ones — so it silently used the broken 4.5.0. (The crash only surfaced mid-decode, after language detection, which is why it looked odd.)

## Fix (in `/home/lzw/projects/ww`)

Changed `_ensure_deps()` in `ww/audio/whisper_translate.py`, `whisper_low_mem.py`, and `whisper_diarize.py` to **always prefer the project `.venv`** unless already running inside it (detected via `sys.prefix`). Also:
- Added the missing `if __name__ == "__main__": main()` guard in `whisper_translate.py` (its old re-exec convention ran through the console script, so the module could never run directly — the re-exec now targets the module file like the other two scripts).
- Each re-exec logs `[ww] Re-running with project venv python: ...` to stderr for transparency.

## Verified

- `ww whisper clip.mp3 --language zh` — previously crashed, now transcribes fine.
- `ww whisper --low-memory --model tiny` — same stale-dep bug, now fixed too.
- `ww whisper diarize` already worked (whisperx was missing from system python, forcing the venv) and is unaffected.

You can now just rerun your original command:
```
ww whisper daniel.mp3 --language zh
```

Optional cleanup (not required now): if you don't want stale system-python copies shadowing things in future, you could uninstall `faster-whisper`/`ctranslate2` from `~/.local/lib/python3.11/site-packages` — but the venv-first logic now protects you regardless.
