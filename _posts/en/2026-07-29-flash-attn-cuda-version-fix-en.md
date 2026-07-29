---
audio: false
generated: true
image: false
lang: en
layout: post
title: Flash-Attn CUDA Version Fix
translated: false
type: note
---

## ✅ Done! `flash-attn==2.8.3` installed successfully

### What happened

The real issue wasn't about sticking or compiling — it was a **CUDA version mismatch**:

| Component | Expected | Reality |
| ----------- | ---------- | --------- |
| **PyTorch CUDA** | 13.0 (compiled with) | `torch 2.11.0+cu130` |
| **System CUDA 12.8** | ❌ | version check failed |
| **System CUDA 13.2** | ❌ | `13.2 != 13.0` |
| **Prebuilt wheel cu13torch2.10** | ✅ | used this |

### What I did

1. **Killed** the pointless sm_80 compilation in `/mnt/data/`
2. **Discovered** your PyTorch needs CUDA 13.0, not 12.8
3. **Found** a prebuilt wheel at:

   ```
   flash_attn-2.8.3+cu13torch2.10cxx11abiTRUE-cp312-cp312-linux_x86_64.whl
   ```

4. **Installed it** — no compilation needed, instant install

### Verification

- `flash-attn` 2.8.3 ✓
- `PyTorch` 2.11.0+cu130 ✓
- `CUDA` 13.0 ✓
- `Device` RTX 4070 ✓
- `flash_attn_func` imports successfully ✓

**Note:** `2.8.4` doesn't exist on PyPI — `2.8.3` and `2.8.3.post1` are the latest. The installed `2.8.3` is functionally equivalent.
