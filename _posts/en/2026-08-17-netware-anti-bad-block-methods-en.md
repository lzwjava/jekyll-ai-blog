---
audio: false
generated: true
image: false
lang: en
layout: post
title: NetWare Anti-Bad Block Methods
translated: false
type: note
---

The correct answer is **B. 热调整和写后读验证 (Hot Fix and read-after-write verification)**.

Explanation:

In Novell NetWare, the two complementary techniques used to protect against unreliable disk blocks are:

1. **Hot Fix (热调整/热修复)** — A reserved area of disk (the Hot Fix Redirection Area) that automatically redirects data away from bad blocks. When a bad block is detected, the data is written to this reserved area instead.

2. **Read-after-write verification (写后读验证)** — After data is written to disk, the system immediately reads it back and compares it with what was written. If they don't match, the block is flagged as bad and the data is redirected via Hot Fix.

Disk mirroring (磁盘镜像) and disk duplexing (磁盘双工) are different techniques — they protect against **physical disk failure** (whole-disk redundancy), not against unreliable blocks within a single disk.

So the answer is **B**.
