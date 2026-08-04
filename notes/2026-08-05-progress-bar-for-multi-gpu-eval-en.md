---
audio: false
generated: true
image: false
lang: en
layout: post
title: Progress bar for multi-GPU eval
translated: false
type: note
---

Done. Added a per-sample `tqdm` progress bar to `run_dataset()` in `deepspec/eval/base_evaluator.py`:

```python
indices = range(self.global_rank, len(dataset), self.world_size)
for idx in tqdm(
    indices,
    desc=f"[rank {self.global_rank}] {dataset_name}",
    total=len(indices),
    position=self.global_rank,
    leave=False,
    disable=(self.global_rank != 0),
    unit="sample",
):
```

Details:

- **desc** shows which dataset and rank, e.g. `[rank 0] gsm8k: 37%|███ | 37/100 [02:10<03:41, 3.54s/sample]`
- **total** = this rank's actual share of samples (`len(range(rank, N, world_size))`), so the bar correctly goes 0→100 per rank
- **position/disable** — only rank 0 renders the bar; on multi-GPU runs extra ranks won't collide with it (and only rank 0's terminal matters anyway)
- **leave=False** — bar clears after each dataset so the table row is clean
- Compile-checked ✅, tqdm 4.67.3 already in the environment

**Note:** your currently-running eval (PID 44088) already imported the old code — this applies from the next launch. Since the next run will be a fresh start anyway, you can Ctrl+C the current one, or let it finish and see the new bar on the next run.

Quick sanity test if you want before the next full run:

```bash
cd /mnt/data/DeepSpec
CUDA_VISIBLE_DEVICES=0 PYTHONPATH=/mnt/data/DeepSpec /usr/bin/python3.12 toy_run/eval_smoke.py \
  --dataset gsm8k --num-samples 3 --max-new-tokens 128
```

You should see `[rank 0] gsm8k: ... 3/3 [~10s, ...s/sample]` then the results table.
