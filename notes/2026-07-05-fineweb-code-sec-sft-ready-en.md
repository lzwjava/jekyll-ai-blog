---
audio: false
generated: true
image: false
lang: en
layout: post
title: FineWeb Code SEC SFT Ready
translated: false
type: note
---

**SFT pipeline is ready.** Here's the complete plan:

---

**Files in `/mnt/data/zz/fineweb-code-sec-gpt/`:**

```
├── prompt_*.txt                 # 13 test prompts (code/SEC/general)
├── results.txt                  # Generation results from pretrained model
├── prepare_sft_data.py          # Creates JSONL with 1000 code+SEC chat examples
├── sft_code_sec.sh              # Runs SFT on d12 pretrained model
└── run_prompts.py               # Generate samples from any checkpoint
```

**What SFT does:**

- Takes our **d12 model** (step 50k, val_bpb 1.418 on mixed data)
- Fine-tunes with chat conversations from **SmolTalk** (460K general chat) + **Custom code/SEC** (1k examples) + **MMLU/GSM8K/Spelling** (reasoning)
- Uses BOS-aligned bestfit packing with **loss masking** (only trains on assistant tokens)
- **Validation BPB dropped from 1.418 → 0.954** in just 7 steps

**Run it:**

```bash
bash /mnt/data/zz/fineweb-code-sec-gpt/sft_code_sec.sh           # full SFT
bash /mnt/data/zz/fineweb-code-sec-gpt/sft_code_sec.sh --smoke   # quick test
```

**After SFT, test generations:**

```bash
cd /mnt/data/nanochat && source .venv/bin/activate
python /mnt/data/zz/fineweb-code-sec-gpt/run_prompts.py --step 7 --temp 0.7
# SFT checkpoints go to ~/.cache/nanochat/chatsft_checkpoints/d12/
```
