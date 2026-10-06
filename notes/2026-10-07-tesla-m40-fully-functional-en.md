---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tesla M40 Fully Functional
translated: false
type: note
---

🎉 **It's working perfectly!** The Tesla M40 is now fully functional:

```
NVIDIA-SMI 550.163.01        Driver Version: 550.163.01     CUDA Version: 12.4
GPU 0: Tesla M40 24GB        Bus-Id: 00000000:01:00.0       Off
Temp: 31C   Perf: P8        Pwr: 16W / 250W     Mem: 6MiB / 24576MiB   Util: 0%
```

## Final status — everything done ✅

| Task | Result |
|---|---|
| SSH key auth to `lzw@192.168.1.137` | ✅ |
| `lzw` added to sudo group | ✅ |
| NVIDIA driver 550.163.01 installed (matches M40 support) | ✅ |
| BIOS updated A.50 → **A.A** | ✅ |
| "Above 4G Decoding" enabled | ✅ |
| GPU BARs assigned (BAR1 = 32GB, BAR3 = 32MB) | ✅ |
| `nvidia-smi` detects **Tesla M40 24GB** (24576 MiB) | ✅ |
| CUDA driver v12.4 active | ✅ |

The card is idle at 31°C / 16W, fully recognized.

## Suggested next steps (optional)

1. **Enable persistence mode** so the GPU stays initialized and doesn't reset between tasks:
   ```bash
   sudo nvidia-smi -pm 1
   ```
2. **Install CUDA toolkit** if you plan to run compute workloads (PyTorch, TensorFlow, etc.):
   ```bash
   sudo apt install nvidia-cuda-toolkit     # Debian's packaged CUDA
   ```
   or use a specific CUDA version from NVIDIA.

3. **Test compute** with a quick check, e.g.:
   ```bash
   nvidia-smi -q | head -20
   ```

Want me to enable persistence mode and/or install the CUDA toolkit now?
