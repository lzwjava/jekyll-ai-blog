---
audio: false
generated: true
image: false
lang: en
layout: post
title: Choosing Snapshots to Delete
translated: false
type: note
---

**Question:** I have 4 snapshots and snapshots 1, 3, 4 look like the same base (6.56–6.58 GB). Which ones should I delete?

**Answer:**

Looking at the sizes and dates:

| # | Size | Date | Notes |
| --- | ------ | ------ | ------- |
| 1 | 6.56 GB | 2026-05-19 | Oldest, slightly smaller |
| 2 | 132.77 GB | 2026-05-20 | **Keep** — big, likely has your ML env/models |
| 3 | 6.58 GB | 2026-05-30 | `test-snapshot-api` — test one |
| 4 | 6.58 GB | 2026-05-30 | Named properly, most recent |

**Delete 1 and 3. Keep 4.**

- **1** → oldest, superseded by 4
- **3** → named `test-snapshot-api`, explicitly a test, same size as 4
- **4** → most recent, properly named with date stamp — this is your canonical base snapshot

So delete IDs `229286514` and `230740231`.
