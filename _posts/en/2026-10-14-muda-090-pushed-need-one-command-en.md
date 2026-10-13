---
audio: false
generated: true
image: false
lang: en
layout: post
title: muda 0.9.0 pushed, need one command
translated: false
type: note
---

Pushed **`muda 0.9.0`** (`62fe80b`).

## About "do it" — the blocker is hard

I re-checked before proceeding: `sudo` requires an interactive password and I have no TTY, and `/sys/.../driver/unbind` is not user-writable. So I **cannot** execute the nvidia↔nouveau switch myself. Only you can run that one command. Everything else I can do.

## What I did instead (testable, measurable)

**Faster SGEMM** — added a second register-blocked kernel and select by size:
- `m,n < 1024`: `sgemm_rb` (64×64, 4×4/thread, 70 regs)
- `m,n ≥ 1024`: `sgemm_rb128` (128×64, 8×4/thread, ~90 regs, better FMA:load ratio)

```
    size  naive GFLOP/s  tuned GFLOP/s   speedup
     256          275.8          603.4     2.19x
     512          320.4         1291.4     4.03x
    1024          286.2         1577.7     5.51x
    2048          318.6         1785.2     5.60x
```

That's up from ~1.17 / ~1.43 TFLOP/s at 1024 / 2048. Python binding now shows **~1.73 TFLOP/s** at 2048³. Caught and fixed a real bug along the way (tile x/y were swapped, which silently produced wrong results — visible in the benchmark's CPU cross-check).

Full suite still green: **77 checks + 4 mudac programs**.

## The one command I need from you

Stop anything using the M40, then:

```sh
cd ~/projects/muda
sudo tools/muda-gpu-mode.sh nouveau      # switch to the open driver
MUDA_DRIVER=nouveau ./build/mudainfo     # test the native backend
MUDA_DRIVER=nouveau ./build/test_memory
```

Paste that output. To undo: `sudo tools/muda-gpu-mode.sh nvidia`, or just reboot (nouveau stays blacklisted).

Once nouveau is bound I can open its render node as a normal user, so I'll be able to **actually develop and test** the native path with you — GEM allocation first, then a compute channel. If your `mudainfo` output shows `GETPARAM`/GEM constants differ on your kernel, I'll fix them from the output.