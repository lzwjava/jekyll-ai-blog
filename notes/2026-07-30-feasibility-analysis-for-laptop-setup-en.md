---
audio: false
generated: true
image: false
lang: en
layout: post
title: Feasibility Analysis for Laptop Setup
translated: false
type: note
---

Now I have a complete picture. Let me summarize the full feasibility analysis:

---

## 🔍 Full Analysis: Can DeepSpec Run on This Laptop?

### ✅ What we accomplished
- **Cleaned ~91 GB** from `/mnt/data/zz-backup/datasets/fineweb-edu/` (oldest 3 crawl dumps)
- The **1.8 TB data drive** now has **731 GB free** ✅
- HuggingFace cache is already symlinked to `/mnt/data/` ✅

### ⚠️ Remaining bottleneck: Root partition (99% full)
Root (`/dev/nvme0n1p2`, 916 GB) has only **14 GB free**. Since model checkpoints/tensorboard/cache all default to `~/` (on root), we'd need to clean up or symlink. Large items on root:
- `/home/lzw/projects/` — **488 GB** (many old projects)
- `/home/lzw/Downloads/` — **38 GB**
- `/home/lzw/qDownloads/` — **14 GB**

### 🧩 What *Can* Actually Run

| Stage | Feasibility | Why |
|---|---|---|
| **pip install -r requirements.txt** | ✅ Likely | Dependencies are reasonable |
| **Data Download** (step 1) | ✅ Yes | Small output, plenty of space on `/mnt/data/` |
| **Regenerate Answers** (step 2) | ⚠️ Partial | Needs SGLang (not installed), 1 GPU instead of 8 → very slow |
| **Target Cache** (step 3) | ❌ **No** | **38 TB** — physically impossible |
| **Training** | ❌ **No** | Needs 38 TB cache; single 11.6 GB GPU will OOM with full model |
| **Evaluation** | ✅ **Possible** | Download pre-trained checkpoint + target model from HF; single GPU mode works |

### 💡 Most Viable Path: **Evaluation with Pre-Trained Checkpoints**

1. Install deps (`pip install -r requirements.txt`)
2. Download `Qwen/Qwen3-4B` target model (~8 GB) → goes to HF cache on `/mnt/data/` ✅
3. Download a pre-trained draft, e.g. `deepseek-ai/dspark_qwen3_4b_block7` → also HF cache ✅
4. Run eval on 1 benchmark (e.g., GSM8K): `CUDA_VISIBLE_DEVICES=0 python eval.py --target_name_or_path Qwen/Qwen3-4B --draft_name_or_path deepseek-ai/dspark_qwen3_4b_block7`
5. May need to adjust eval.sh to use `CUDA_VISIBLE_DEVICES=0` instead of 4 GPUs

**Risks**: 11.6 GB VRAM is tight for Qwen3-4B (8 GB) + draft model + generation context. Might need `--max-new-tokens` reduction or OOM.

### 🧹 To make it work, I suggest:
1. Symlink `~/checkpoints/` and `~/.cache/deepspec/` → `/mnt/data/` so model cache/checkpoints don't fill root
2. Clean up old Downloads (52 GB combined) on root for breathing room

Want me to proceed? I can start by symlinking the directories, installing deps, and attempting an evaluation run.