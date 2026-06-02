---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: NetWare Data Protection Mechanisms
translated: false
type: note
---

Question: In Novell NetWare, to prevent data from being written to unreliable disk blocks, two complementary technologies are used for data protection. What are they?

Answer:

The correct answer is **B. Hot fix and read-after-write verification**.

**Detailed explanation:**

Novell NetWare (especially versions such as NetWare 3.x and 4.x) used two main complementary techniques to protect against writing data to bad or unreliable disk sectors:

1. **Hot Fix** (热调整 / Hot Fix Redirection Area)
   - Novell maintains a small reserved area on the disk called the **Hot Fix redirection area**.
   - When a write error occurs or during surface scans, bad blocks are detected.
   - Instead of failing the write, NetWare redirects the data to a good block in the Hot Fix area and updates the Hot Fix table.
   - This happens transparently — the operating system continues to see the original logical block address.
   - Purpose: **prevents future writes to known bad blocks** and corrects errors on-the-fly.

2. **Read-After-Write Verification** (写后读验证)
   - After every write operation, the file server immediately reads back the data just written.
   - If the read-back data does not match what was sent, the write is considered failed.
   - The server then marks the block as bad (redirects it via Hot Fix) and retries the write to another location.
   - Purpose: **detects write errors immediately**, ensuring data is not silently corrupted on unreliable media.

These two techniques work together:

- **Read-after-write** actively detects write problems in real time.
- **Hot Fix** provides the mechanism to recover from and permanently avoid bad blocks.

**Why the other options are incorrect:**

- **A. Hot fix and disk mirroring** → Disk mirroring is for redundancy (two copies of data), not specifically for preventing writes to bad blocks.
- **C. Disk mirroring and read-after-write verification** → Mirroring protects against complete disk failure, not individual bad sectors on a single drive.
- **D. Disk mirroring and disk duplexing** → Both are forms of RAID-1 style mirroring (duplexing uses separate controllers), focused on fault tolerance, not bad-block handling.

**Memory tip (as provided):**
"热写防错双保险" → Hot fix + write-then-read verification are the two complementary protections against bad-block writes.

References:

- None (standard Novell NetWare storage protection mechanisms, widely documented in legacy NetWare administration guides)
