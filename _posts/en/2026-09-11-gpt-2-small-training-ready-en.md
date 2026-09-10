---
audio: false
generated: true
image: false
lang: en
layout: post
title: GPT-2 Small Training Ready
translated: false
type: note
---

Done. Nothing is running; the GPU is free for you to launch it.

## `run1.sh` (`/mnt/data/igpt/run1.sh`, executable)

```bash
tmux new -s igpt
cd /mnt/data/igpt
./run1.sh
# detach: Ctrl-b d     reattach: tmux attach -t igpt
# resume after a crash: ./run1.sh --init_from resume
```

The run: **124 M-param GPT-2-small** (`12L/12H/768d`, block 512) on **FineWeb** (3.68 B GPT-2 BPE tokens, memmapped — no re-tokenization), 30 000 iters × 32 768 tokens ≈ **983 M tokens**, lr 6e-4 cosine → 6e-5, warmup 1000, dropout 0.1, bf16. Best-val checkpoint → `out-fineweb-124m/ckpt.pt`, final state → `ckpt_last.pt`, full log tee'd to `out-fineweb-124m/train.log`. Measured ~800 ms/iter ⇒ **ETA ≈ 6.5–7 h**.

Overridable without editing: `PY=… DATA_DIR=… OUT_DIR=… ./run1.sh`, and any extra flags are forwarded (`./run1.sh --max_iters 50000`).

Environment status:

- `llama-server` killed → **~9.0 GB free** (was 2.4 GB).
- Copied `nanoGPT/data/fineweb/{train.bin,val.bin}` → `igpt/data/fineweb/` and wrote the missing `meta.pkl`.
- Wikipedia copy from earlier is still at `igpt/data/wikipedia/` (86 M tokens) if you want a shorter/cleaner-val run instead: `DATA_DIR=data/wikipedia OUT_DIR=out-wikipedia-124m ./run1.sh`.
- `train.py` changes present in your working tree (both needed for long runs): eval wrapped in `torch.no_grad()`, and the final save no longer clobbers the best-val `ckpt.pt`.

Sample after it finishes:

```bash
/usr/bin/python3.12 train.py --data_dir data/fineweb --tokenizer bpe \
  --out_dir out-fineweb-124m --sample --prompt "The history of" --max_new_tokens 200
```
