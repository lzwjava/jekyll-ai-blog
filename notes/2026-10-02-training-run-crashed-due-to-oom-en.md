---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training run crashed due to OOM
translated: false
type: note
---

## Overall training status

**The current run is dead — it crashed and nothing is training right now.** The GPU is idle (only 1.4 GB / 12 GB used, 16% util), no `base_train.py` process is alive.

### What happened to the current run

- Started from step 0, got to **step ~116 / 3712 (3%)** with loss trending down nicely (4.41 → 4.12).
- Died during the periodic **core evaluation** (`bigbench_language_identification`) with a **CUDA OOM** at `gpt.py:515`.
- **No checkpoint was saved** for this run, so those ~116 steps are lost.

### What you still have (prior artifacts, all from July)

| Model | Stage | Steps | Size |
| --- | --- | --- | --- |
| `d12` base | pretrained | up to **87,000** (ckpts every 5k) | 793 MB each |
| `d12` chat | SFT | 8,985 | 793 MB |
| `d4` base | pretrained | 20 | 23 MB |

Plus an older completed pipeline (`shell/run_rtx4070.log`, June) for a tiny **d8 (40M)** model that finished end-to-end, but its eval scores were near-random (ARC-Easy 25.6%, MMLU 25.3%, GSM8K/HumanEval/SpellingBee all 0%) — expected for a 40M model.

### Bottom line

- The meaningful artifact is the **d12 base model at 87k steps**.
- The latest attempt (the run you were watching) **crashed at 3% with OOM** and can't be resumed without a checkpoint — it'd have to be restarted from scratch.

To make the next attempt survive, I'd recommend fixing the OOM first (e.g. `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`, or capping eval `max_per_task` / eval batch). Want me to look at `base_train.py` and `core_eval.py` to pin down the cleanest fix before you restart?
