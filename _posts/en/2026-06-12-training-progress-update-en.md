---
audio: false
generated: true
image: false
lang: en
layout: post
title: Training Progress Update
translated: false
type: note
---

Got it — letting it run. Here's the status:

```
Progress:   400 / 2,656 steps (15%)
Elapsed:    ~2 hours
ETA:        ~9 more hours (around 04:00 tomorrow)
Loss:       2.86 → 1.70 (healthy)
GPU:        100% utilization, 11.5GB
```

Checkpoints at `lzw-notes-lora/checkpoint-{10,200,400}/`. Final adapter will save to `lzw-notes-lora/`. You can check progress anytime with:

```bash
cat /mnt/data/zz/finetune/lzw-notes-lora/checkpoint-*/trainer_state.json | python3.11 -c "
import json, sys
for line in sys.stdin:
    try:
        state = json.loads(line)
        print(f'Step {state[\"global_step\"]}/{state[\"max_steps\"]} epoch={state[\"epoch\"]:.2f}')
    except: pass
" | tail -1
```
