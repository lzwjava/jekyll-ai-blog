---
audio: false
generated: true
image: false
lang: en
layout: post
title: AMD Dev Cloud Volume Size Error Fix
translated: false
type: note
---

**Question:** AMD Dev Cloud volume creation complains about invalid size — how do I fix it?

Can you share the exact error message and screenshot? That would help pinpoint whether it's a UI validation issue, a size limit, or a unit format problem.

That said, common causes:

---

## Common "Invalid Size" Issues on AMD Dev Cloud

### 1. Unit format — enter a plain integer, no units

Some UIs expect just `100` not `100GB` or `100GiB`. Try:

```
100        ✓
100GB      ✗
100 GB     ✗
100GiB     ✗
```

### 2. Minimum size requirement

Most block storage has a minimum (usually **1 GB or 10 GB**). Entering `0` or a very small number fails silently with "invalid size".

### 3. Maximum size cap

AMD Dev Cloud may cap volume size per project tier. Common limits: 500 GB or 1 TB. If you entered something large like `2000`, try `500` first.

### 4. Project quota not set up

If your account is on a free/trial tier, block storage may not be enabled at all — the "invalid size" error is a misleading way to say "this feature isn't available on your plan."

---

## What to Try

1. Enter `50` (plain integer, no units) and see if it accepts
2. Check your project quota/limits in the Dev Cloud dashboard under account settings
3. If it's a trial account, you may need to contact AMD Dev Cloud support to enable persistent storage

What does the exact error say and which field triggers it?
