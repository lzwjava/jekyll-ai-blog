---
audio: false
generated: true
image: false
lang: en
layout: post
title: "Storage Cleanup: 95 GB Freed"
translated: false
type: note
---

Done. Summary:

```
Root disk:  697G  29G used (668G free)  — was 124G, freed 95G
Volume:     100G  37G used (58G free)
Containerd: 1.8M (was 59G)
```

**Freed 95 GB** on root disk:

- 37G → llama.cpp models moved to volume + symlinked
- 36G → rocm Docker image deleted
- 22G → containerd overlayfs snapshots deleted (container image layers)
