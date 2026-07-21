---
audio: false
generated: true
image: false
lang: en
layout: post
title: nvidia-smi Blocked by Secure Boot
translated: false
type: note
---

**Summary:**

- **GPU detected:** RTX 4070 (AD104)
- **nvidia-smi binary:** ✅ installed
- **Driver:** ✅ nvidia-driver-580 (580.167.08) installed, DKMS modules built for both kernels
- **nvidia-smi fails because:** ❌ Secure Boot is **enabled**, kernel rejects the unsigned module
- **Fix needed:** sign the module or disable Secure Boot → then `nvidia-smi` will work

Your call — option A (sign) or B (disable Secure Boot)?
