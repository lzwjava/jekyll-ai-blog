---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: NetWare 数据保护机制
translated: true
type: note
---

Question: In Novell NetWare, to prevent data from being written to unreliable disk blocks, two complementary technologies are used for data protection. What are they?

Answer: 

The correct answer is **B. Hot fix and read-after-write verification**。

**Detailed explanation:**

Novell NetWare（尤其是 NetWare 3.x 和 4.x 等版本）使用了两种主要的互补技术来防止将数据写入损坏或不可靠的 disk sectors：

1. **Hot Fix**（热调整 / Hot Fix Redirection Area）  
   - Novell 在磁盘上保留了一个名为 **Hot Fix redirection area** 的小区域。  
   - 当发生写入错误或进行 surface scans 时，会检测到 bad blocks。  
   - NetWare 不会让写入失败，而是将数据重定向到 Hot Fix 区域中的一个良好 block，并更新 Hot Fix table。  
   - 这一过程是透明的 —— operating system 继续看到原始的 logical block address。  
   - 目的：**防止未来写入已知的 bad blocks** 并即时纠正错误。

2. **Read-After-Write Verification**（写后读验证）  
   - 在每次写入操作后，file server 会立即读取刚刚写入的数据。  
   - 如果读回的数据与发送的数据不匹配，则认为写入失败。  
   - Server 随后将该 block 标记为 bad（通过 Hot Fix 进行重定向），并尝试将数据写入另一个位置。  
   - 目的：**立即检测写入错误**，确保数据不会在不可靠的介质上发生静默损坏。

这两项技术协同工作：  
- **Read-after-write** 实时主动检测写入问题。  
- **Hot Fix** 提供了从中恢复并永久避开 bad blocks 的机制。

**Why the other options are incorrect:**

- **A. Hot fix and disk mirroring** → Disk mirroring 用于 redundancy（数据的两个副本），而非专门用于防止向 bad blocks 写入。  
- **C. Disk mirroring and read-after-write verification** → Mirroring 防止的是整个磁盘故障，而不是单个驱动器上的个别 bad sectors。  
- **D. Disk mirroring and disk duplexing** → 两者都是 RAID-1 形式的 mirroring（duplexing 使用独立的 controllers），侧重于 fault tolerance，而非 bad-block 处理。

**Memory tip (as provided):**  
"热写防错双保险" → Hot fix + write-then-read verification 是针对 bad-block 写入的两项互补保护措施。

References:  

- None（标准的 Novell NetWare 存储保护机制，在旧版 NetWare 管理指南中有广泛记载）