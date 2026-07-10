---
audio: false
generated: true
image: false
lang: en
layout: post
title: SFT Training Completed Successfully
translated: false
type: note
---

**SFT complete — 8,985 steps, 184.7 minutes (~3 hours)**

### SFT Summary

| Pretrained (step 50k) | SFT (step 8985) |
|---|---|
| val_bpb: **1.418** | val_bpb: **0.405** |
| Train loss: 1.06 | Train loss: 1.07 |

Validation BPB dropped 71% — the model learned to produce chat-formatted responses.

Loss at end: ~1.07, LR decayed to 0.00 (warmdown completed). Epoch 2 just started when dataset ended.

Checkpoint: `/home/lzw/.cache/nanochat/chatsft_checkpoints/d12/model_008985.pt` (793MB)

**Next steps:** Test generations from the SFT model and compare with pretrained:

```bash
cd /mnt/data/nanochat && source .venv/bin/activate
python /mnt/data/zz/fineweb-code-sec-gpt/run_prompts.py --step 8985 --temp 0.7 --max-tokens 200
```