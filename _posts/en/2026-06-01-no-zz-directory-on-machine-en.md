---
audio: false
generated: true
image: false
lang: en
layout: post
title: No ZZ Directory on Machine
translated: false
type: note
---

No `zz` directory exists on this machine. Here's the full picture:

```
ROOT DISK (697G, 88G used, 610G free)
├── /var            60G   ← containerd 59G + system logs
├── /opt            22G   ← ROCm 7.2.0 (GPU runtime, needed)
├── /root           385M  ← llama.cpp source + build scripts
├── /usr            6.3G  ← system packages
└── /home           empty

VOLUME (100G, 37G used, 63G free)
└── llama-models    37G   ← GGUF models (symlinked from /root/llama.cpp/models)
```

There's no `zz` data here. The only large data on this box is:

| What | Where | Size |
|------|-------|------|
| ROCm runtime | /opt/rocm-7.2.0 | 22G |
| Container images | /var/lib/containerd | 59G |
| Llama models | volume (symlinked) | 37G |

Everything is fine where it is. Root disk has 610G free — no need to move anything else to the volume. The volume is actually more constrained (63G free).

Is `zz` something you were expecting to have on this machine, or did you mean something else?
