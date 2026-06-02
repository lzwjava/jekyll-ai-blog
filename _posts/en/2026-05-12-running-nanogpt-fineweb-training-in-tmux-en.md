---
audio: false
generated: true
image: false
lang: en
layout: post
title: Running nanoGPT Fineweb Training in tmux
translated: false
type: note
---

```bash
cd /mnt/data/nanoGPT
tmux new -s nano        # or: tmux attach -t nano

# do NOT activate the venv — use system python3.11
PYTORCH_ALLOC_CONF=expandable_segments:True \
python3.11 -u train.py config/train_fineweb_gpt3.py --compile=False 2>&1 \
  | tee -a out-fineweb-gpt3/train.log
```

Detach with `Ctrl-b d`, reattach with `tmux attach -t nano`.

Resume after kill/restart: append `--init_from=resume`.

Expected: ~11s/iter eager → ~59 hrs for the full 19073-iter run, checkpoint every 500 iters.
