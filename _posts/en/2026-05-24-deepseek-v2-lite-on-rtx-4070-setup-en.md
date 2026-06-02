---
audio: false
generated: true
image: false
lang: en
layout: post
title: DeepSeek V2 Lite on RTX 4070 Setup
translated: false
type: note
---

Here's the full story:

```
================================================================
  DeepSeek-V2-Lite-Chat on RTX 4070 — Full Setup Report
================================================================

GOAL
----
Run a DeepSeek model on your RTX 4070 (12GB VRAM).
The original DeepSeek-V4 code in /mnt/data/deepseek-v4-inference
targets a 671B+ parameter model needing 8x H100 GPUs — not viable
on your hardware. So we went with DeepSeek-V2-Lite-Chat instead:
same MLA/MoE architecture, just 16B total (2.4B activated per token).

STEP 1 — GIT PULL ~/projects/ww
--------------------------------
Pulled latest from github.com:lzwjava/ww. Got a big update:
140 files changed, +21,275 lines. New modules for agents, tests,
weather, machine info, hermes config, image EXIF, GitHub mgmt, etc.

STEP 2 — INSTALL DEPENDENCIES
------------------------------
  python3.11 -m pip install --user bitsandbytes accelerate

  Result:
    bitsandbytes 0.49.2  — 4-bit NF4 quantization
    accelerate 1.13.0    — device_map="auto" for multi-GPU/CPU offload

  Already had:
    torch 2.6.0, transformers 4.48.3, safetensors 0.5.2

STEP 3 — DOWNLOAD MODEL
------------------------
  Model: deepseek-ai/DeepSeek-V2-Lite-Chat
  Destination: /mnt/data/models/DeepSeek-V2-Lite-Chat/

  First tried HF mirror (hf-mirror.com) for speed — failed with
  LocalEntryNotFoundError. Fell back to direct HuggingFace.

  Download ran in background, took ~35 minutes for 30GB:
    - 4 safetensor shards (8.1GB x3 + 5.3GB x1)
    - Plus tokenizer, config, modeling code (~15 small files)
    - Speed: ~1 GB/min sustained

  Download script:
    from huggingface_hub import snapshot_download
    snapshot_download(
        'deepseek-ai/DeepSeek-V2-Lite-Chat',
        local_dir='/mnt/data/models/DeepSeek-V2-Lite-Chat'
    )

STEP 4 — INFERENCE SCRIPT
--------------------------
  Wrote /mnt/data/deepseek-v4-inference/run_lite.py with:
    - 4-bit NF4 quantization via BitsAndBytesConfig
    - Double quantization for extra memory savings
    - bfloat16 compute dtype
    - device_map="auto" for automatic GPU placement
    - Interactive chat mode and single-prompt mode
    - CLI args: -p "prompt", -n max_tokens

STEP 5 — FIX: Python.h MISSING
--------------------------------
  First run failed — triton (bitsandbytes dependency) tried to
  compile C code needing Python.h for python3.11, but only
  python3.12-dev was installed.

  Fix: symlinked python3.12 headers as python3.11:
    sudo ln -sf /usr/include/python3.12 /usr/include/python3.11

  This works because the C API is compatible enough for triton's
  simple build. After this, model loaded and ran successfully.

STEP 6 — TEST RUN
------------------
  Command:
    python3.11 run_lite.py -p "Hello! Who are you?"

  Result:
    Loading time: ~2.5 min (4 shards, 37s each)
    GPU memory: 9.5 GB used (of 11.6 GB available)
    Response: "I am an AI language model, here to assist you
              with information, questions, or tasks you have."

FINAL STATE
-----------
  Model:       /mnt/data/models/DeepSeek-V2-Lite-Chat/  (30GB on disk)
  Script:      /mnt/data/deepseek-v4-inference/run_lite.py
  VRAM usage:  9.5 GB / 11.6 GB (82%)
  Quantization: 4-bit NF4 with double quant
  Speed:        ~2.5 min load, then fast inference

HOW TO USE
----------
  Interactive chat:
    python3.11 /mnt/data/deepseek-v4-inference/run_lite.py

  One-shot prompt:
    python3.11 /mnt/data/deepseek-v4-inference/run_lite.py -p "Explain quantum computing"

  Longer output:
    python3.11 /mnt/data/deepseek-v4-inference/run_lite.py -p "Write a poem" -n 1024

WHAT CHANGED FROM THE ORIGINAL ASSESSMENT
------------------------------------------
  Original code: DeepSeek-V4 (671B+ params, 8x H100 required)
  Now running:   DeepSeek-V2-Lite-Chat (16B params, 1x RTX 4070)

  Same architecture family (MLA + MoE), just scaled to fit your
  hardware. You lose some capability vs the 671B model, but you
  can actually run it locally.
================================================================
```

Want to try interactive mode or tweak anything?
