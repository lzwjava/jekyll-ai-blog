---
audio: false
generated: true
image: false
lang: en
layout: post
title: Novell NetWare Data Protection Methods
translated: false
type: note
---

**Question:** What data protection methods does Novell (NetWare) use? (Including Hot Fix / 热调整, etc.)

---

**Answer:**

Novell NetWare uses several layered techniques to protect data on the server:

---

### 1. Hot Fix (热调整 / 热修复)

Due to constant reading and writing, some disk blocks gradually lose their ability to store data reliably. NetWare's Hot Fix feature prevents data from being written to those unreliable blocks. When a bad block is detected, the data (still held in memory) is redirected to a reserved area called the **Hot Fix Redirection Area**. The OS then records the defective block's address so it will never be used again. This redirection can happen during a write request, a read request, or a read-after-write verification. By default, 2% of a disk's space is set aside as the Hot Fix Redirection Area.

---

### 2. Duplicate File Directories

NetWare protects data by maintaining **duplicate file directories** on disk, so that if one directory copy is corrupted, the other can still be used to locate files.

---

### 3. Disk Mirroring & Duplexing (磁盘镜像 / 双工)

**Mirroring** stores the same data on separate disks on the **same controller channel**; **duplexing** stores the same data on separate disks on **separate controller channels**, and can even use two different drivers. Duplexing is the recommended method because two channels rarely fail simultaneously.

Mirroring protects data against failure of the drive itself, but not against other disk channel component failures (such as HBAs, cables, or power supplies). Duplexing protects data against failure in **any** component along the disk channel, and therefore provides a higher level of protection.

To mirror or duplex partitions, Hot Fix must be enabled first — a section of the partition is set aside as the Hot Fix/Mirror object, which holds tables tracking bad blocks, redirected blocks, which partitions are mirrored, and their sync status.

---

### 4. SMS Backup / Restore (存储管理服务)

The **Novell Storage Management Services (SMS)** infrastructure is supported by all major backup/restore vendors. SMS allows these vendors to fully protect all Novell metadata, including file system access control lists, inherited rights filters, databases, email post offices, mailboxes, and eDirectory objects and attributes.

---

### 5. NSS Pool Snapshots (快照)

**NSS pool snapshots** allow backup of active data at any time. Snapshot tools are integrated into the web-based management interfaces, are independent of hardware vendors, and users can view and select file versions from active snapshot volumes. Snapshot data inherits the rights of the original data.

---

### Summary Table

| Method | Chinese Term | Purpose |
|---|---|---|
| Hot Fix | 热调整 / 热修复 | Redirect bad disk blocks automatically |
| Duplicate directories | 双重目录 | File directory redundancy |
| Disk Mirroring | 磁盘镜像 | Same-channel disk redundancy |
| Disk Duplexing | 磁盘双工 | Cross-channel disk redundancy (stronger) |
| SMS Backup/Restore | 存储管理服务 | Full network data backup & recovery |
| NSS Pool Snapshots | 存储池快照 | Point-in-time backup of active data |

---

**References:**
- [How NetWare Protects Network Data](https://www.novell.com/documentation/nw6p/trad_enu/data/he5cv8fw.html)
- [Hot Fix – Redirecting Bad Blocks](https://www.novell.com/documentation/nw6p/sdiskenu/data/hi4exu95.html)
- [Mirroring and Duplexing](https://teaming.novell.com/documentation/nw6p/sdiskenu/data/hefkruob.html)
- [Novell OES – Data Protection and Security](https://teaming.novell.com/documentation/oes2015/stor_ovw_lx/data/amqlfhu.html)