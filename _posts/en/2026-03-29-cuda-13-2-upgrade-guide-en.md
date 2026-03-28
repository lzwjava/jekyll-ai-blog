---
audio: false
generated: true
image: false
lang: en
layout: post
title: CUDA 13.2 Upgrade and Compatibility Guide
translated: false
type: note
---

Here's the breakdown:

### 📊 CUDA 13.2 Availability

| Check | Result |
|-------|--------|
| `cuda-toolkit-13-2` in repo? | ✅ **Yes** — available |
| Driver 580 supports it? | ✅ **Yes** — driver 580 ships with CUDA 13.0 runtime, compatible with 13.2 toolkit |
| Currently installed | CUDA 12.8 (toolkit) + Driver 580.126.09 |

**Available toolkit versions in the repo:**
- 12.5, 12.6, 12.8, 12.9
- **13.0, 13.1, 13.2** ← latest

### ✅ Yes, you can upgrade to 13.2

The driver 580 supports it. The install would be:

```bash
apt install cuda-toolkit-13-2
```

Then update PATH to `/usr/local/cuda-13.2/bin`. You could also keep 12.8 alongside it — CUDA toolkits are versioned side by side (`/usr/local/cuda-12.8/` and `/usr/local/cuda-13.2/`), switchable via symlink or PATH.

### ⚠️ Things to consider

- **PyTorch/TensorFlow compatibility** — most frameworks currently target CUDA 12.x. CUDA 13.x support is still rolling out. If you're planning to run ML workloads, 12.8 is the safer bet right now.
- **Side-by-side is fine** — no need to remove 12.8, just add 13.2 and switch PATH
- **Driver is fine as-is** — no need to upgrade the driver for CUDA 13.2

Want me to install 13.2 (keep 12.8 alongside), or replace 12.8 entirely?