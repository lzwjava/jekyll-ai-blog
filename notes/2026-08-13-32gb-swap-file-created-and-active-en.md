---
audio: false
generated: true
image: false
lang: en
layout: post
title: 32GB Swap File Created and Active
translated: false
type: note
---

Done. The swap is now active and will persist across reboots.

## Summary

**Created and enabled a 32 GB swap file:**

```
NAME       TYPE  SIZE  USED  PRIO
/swapfile  file   2G     0B    -2   (existing)
/swapfile2 file  32G     0B    -3   (new)
Swap total: 33GiB
```

**What was done:**
1. `sudo fallocate -l 32G /swapfile2` — allocated a 32 GB swap file (~115G free on `/`, plenty of room)
2. `sudo chmod 600 /swapfile2` — correct permissions (must be root-only for swap)
3. `sudo mkswap /swapfile2` + `sudo swapon /swapfile2` — formatted and activated it
4. Added `/swapfile2 none swap sw 0 0` to `/etc/fstab` — so it **survives reboots** automatically

**Verification:**
- `swapon --show` confirms both swap files active (total 33GiB)
- `free -h` shows `Swap: 33Gi 0B used`
- The `findmnt` warning about `/swapfile2` being a *regular file* is **expected and harmless** — swap files *are* regular files; it's not an error.

**Note for the future (recommendation from before still applies):** the swap is now a safety net — if `train_tokenizer.py` overshoots again it will spill to disk (slower, but no freeze / OOM-kill / forced reboot). However, tokenizer training still ran ~40 GB on the full 11.5 GB corpus, so for best results you may still want to train on a random sample (a few hundred MB to ~1 GB) rather than the whole file. The swap protects the system either way.