---
audio: false
generated: true
image: false
lang: en
layout: post
title: Four Minutes Left on Disk Write
translated: false
type: note
---

You're **77% done**. Here's the math:

- ISO total: **6,518,974,464 bytes** (6.07 GiB)
- Written so far: 5,041,553,408 bytes (4.7 GiB)
- **Remaining: ~1.4 GiB** (1,477,421,056 bytes)

At the current rate of ~5.85 MB/s:

```
1,477,421,056 bytes ÷ 5,847,161 B/s ≈ 253 seconds
```

**≈ 4 minutes left** (~4.2 min). Note the speed has dropped to ~5.8 MB/s, so it's likely USB 2.0 — don't expect it to speed up. Just let it finish; it'll end with a `2948850+1 records in / out` line and return to the prompt, then run `sync` and verify with `diskutil list disk12`.
