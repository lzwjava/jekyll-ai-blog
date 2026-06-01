---
audio: false
generated: true
image: false
lang: en
layout: post
title: MI300X Defies Theoretical Training Estimates
translated: false
type: note
---

The MFU number is misleading — nanoGPT hardcodes A100 peak (312 TFLOPS) for MFU calc, not MI300X. The real signal is observed throughput.

**Smoke test results — actual measurements:**

```
Observed:    50,568 tok/s (batch=4, no compile)
Batch=32:    ~404,543 tok/s (linear scaling)
+ compile:   ~525,906 tok/s (+30%)
```

**Estimated training time: 8-10 hours**

That's much better than my theoretical 24-35 hour estimate. The MI300X is fast.

Your turn. Run in tmux:

```bash
cd /root/nanoGPT
python3 train.py config/train_fineweb_760m.py
```

Config: `/root/nanoGPT/config/train_fineweb_760m.py`
- 756.8M params, 24 layers, 1536 dim, 24 heads
- batch=32, block=1024, 445K steps, 14.6B tokens
- lr=3e-4, warmup=2K steps, cosine decay
- `out_dir = 'out-fineweb-760m'`