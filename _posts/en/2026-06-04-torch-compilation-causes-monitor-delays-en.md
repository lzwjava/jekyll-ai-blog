---
audio: false
generated: true
image: false
lang: en
layout: post
title: Torch Compilation Causes Monitor Delays
translated: false
type: note
---

Question: Why is the training monitor waiting so long (15s → 30s → 60s → 120s) before checking if training has started?

Answer:

**torch.compile cold-start compilation is slow for depth=12.**

When you run the first iteration:
1. PyTorch compiles the forward/backward graph on GPU (this is the JIT cost)
2. `depth=12` is a 768-dim model — bigger than `depth=4` you tested earlier
3. torch.compile cold-start on your RTX 4070: ~60–120s typical

The monitoring script is being conservative — sleeping longer between checks to let compilation finish before polling the log. It's safe but slow for iteration.

**Faster alternatives:**

```bash
# Option 1: Watch the actual GPU activity (immediate feedback)
watch -n 1 'nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader'

# Option 2: Tail log continuously (works once compilation starts)
tail -f /mnt/data/nanochat/train.log

# Option 3: Aggressive polling (check every 5s instead of sleeping 120s)
for i in {1..20}; do tail -3 /mnt/data/nanochat/train.log && sleep 5; done

# Option 4: Skip the polling, just attach to tmux immediately
tmux attach -t train
```

**To speed up iteration:**

- Set `--torch-compile=0` in your next run if compile overhead is killing your vibe
- Or use `torch._dynamo.config.suppress_errors = True` to handle edge cases gracefully
- If training stability is fine without compilation, compile is just an optimization — skip it for now

The 6% at 14m suggests compilation was ~90–120s, then training started slow (needs warmup). By step 1000+ you'll see actual throughput.

What's your actual target — fast compilation feedback or best training speed?
