---
audio: false
generated: true
image: false
lang: en
layout: post
title: Fineweb GPT-3 Training Setup
translated: false
type: note
---

Loader works — 1407 train shards + 1 val, uint16, first token is 50256 (EOT) as expected.

### 4) What to do — commands to run

```bash
cd /mnt/data/nanoGPT
source venv/bin/activate

# (optional) confirm the GPU is free
nvidia-smi

# dry run: 5 iters at small batch to verify nothing crashes before committing
python train.py config/train_fineweb_gpt3.py \
    --compile=False --batch_size=2 --gradient_accumulation_steps=1 \
    --max_iters=5 --eval_interval=10 --log_interval=1

# real run (single 4070, 12GB). Use a tmux/screen session — this is many hours.
tmux new -s nano
python train.py config/train_fineweb_gpt3.py 2>&1 | tee out-fineweb-gpt3/train.log
# detach: Ctrl-b d   |   reattach: tmux attach -t nano
```

### Notes / knobs to tune later
- `max_iters=19073` ≈ **10B tokens seen** at 524k tokens/step. To actually use the full ~140B you tokenized, bump it to ~267000 (and set `lr_decay_iters` to match). That's a multi-day run on a 4070.
- If the dry run OOMs, drop `batch_size` to 4 and double `gradient_accumulation_steps` to 128 (keeps tokens/step constant).
- If `compile=True` errors on your PyTorch/CUDA combo, override with `--compile=False`.
- Resume after interruption: `python train.py config/train_fineweb_gpt3.py --init_from=resume`.
- The patch I made to `train.py` is backward-compatible — old configs without `shard_dir` still read `train.bin`/`val.bin`.