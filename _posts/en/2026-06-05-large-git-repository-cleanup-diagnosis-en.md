---
audio: false
generated: true
image: false
lang: en
layout: post
title: Large Git Repository Cleanup Diagnosis
translated: false
type: note
---

FOUND IT. Here's the diagnosis:

```
 58 GB total in .git/objects/pack/

 REAL PACKS:   ~35 GB (23 packs, 29.5M objects)
 TEMP PACKS:   ~23 GB (10 abandoned tmp_pack_* files from interrupted git gc)

 No loose objects, no LFS, 1666 commits, 99 reflog entries
```

The temp packs are abandoned `git gc` operations that got interrupted (likely by sleep/kill). They're pure waste:

```
 tmp_pack_MrX5Ki    14 GB   (May 28)
 tmp_pack_Yx84Jq    6.7 GB  (May 30)
 + 8 others          2.2 GB
 ───────────────────────────
 TOTAL              23 GB   dead weight
```

That alone frees 23 GB — your disk goes from 900MB free to ~23 GB free.

After that, the remaining 35 GB in 23 packs likely also has bloat from the interrupted cycles. A proper `git gc --aggressive` would repack everything into one compact pack.

Want me to:

1. Delete the 10 temp packs (safe, instant, ~23 GB freed)
2. Then run `git gc --aggressive` on the repo (may take 5-10 min, could save another 5-10 GB)

The real packs are still enormous (35 GB for a blog with 1666 commits) — that suggests large images/binaries were committed historically and live in git history. We can investigate that after the quick wins.
