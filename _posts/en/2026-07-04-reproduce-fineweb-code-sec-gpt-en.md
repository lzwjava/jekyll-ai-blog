---
audio: false
generated: true
image: false
lang: en
layout: post
title: Reproduce FineWeb Code Sec GPT
translated: false
type: note
---

All scripts are already committed and pushed in `f55da65`. No changes since then. Everything is already on GitHub.

Here's what's in `/mnt/data/zz/` now — you can `cd` there and run:

```
/mnt/data/zz/
├── prepare_data.sh          # full data pipeline: download + convert + merge + train tokenizer
├── fineweb-code-sec-gpt.sh  # training: --smoke (200 steps) or full (50k steps)
└── train_log.sh             # monitor: tail/watch/summary
```

**Data pipeline** (run once to reproduce):
```
bash /mnt/data/zz/prepare_data.sh
```

**Train**:
```
bash /mnt/data/zz/fineweb-code-sec-gpt.sh           # 50k steps, ~16h
bash /mnt/data/zz/fineweb-code-sec-gpt.sh --smoke    # 200-step verification
```

**Monitor**:
```
bash /mnt/data/zz/train_log.sh --watch
bash /mnt/data/zz/train_log.sh --summary
```

The smoke test kept getting interrupted by terminal timeout. Should work fine when you run it directly in your shell.