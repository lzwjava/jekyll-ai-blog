---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Novell NetWare 数据保护方法
translated: true
type: note
---

**问题：** Novell（NetWare）使用哪些数据保护方法？（包括 Hot Fix / 热调整等）

---

**答案：**

Novell NetWare 使用多种分层技术来保护服务器上的数据：

---

### 1. 热调整（Hot Fix）/ 热修复

由于持续的读写操作，某些磁盘块会逐渐失去可靠存储数据的能力。NetWare 的 Hot Fix 功能可防止数据被写入这些不可靠的磁盘块。当检测到坏块时，数据（仍保留在内存中）会被重定向到称为**热调整重定向区**的保留区域。然后操作系统会记录缺陷块的地址，确保其不再被使用。此重定向可在写入请求、读取请求或写后读验证期间发生。默认情况下，磁盘空间的 2% 被预留为热调整重定向区。

---

### 2. 双重文件目录

NetWare 通过在磁盘上维护**双重文件目录**来保护数据，这样如果一个目录副本损坏，仍可使用另一个副本来定位文件。

---

### 3. 磁盘镜像与磁盘双工

**镜像**在**同一控制器通道**上的独立磁盘中存储相同数据；**双工**在**独立控制器通道**上的独立磁盘中存储相同数据，甚至可以使用两个不同的驱动程序。双工是推荐的方法，因为两个通道同时故障的情况很少见。

镜像可以防止驱动器本身的故障，但不能防止磁盘通道其他组件（如 HBA、电缆或电源）的故障。双工可以防止磁盘通道上**任何**组件的故障，因此提供了更高级别的保护。

要镜像或双工分区，必须首先启用 Hot Fix——分区的某部分被预留为 Hot Fix/镜像对象，该对象保存跟踪坏块、重定向块、哪些分区被镜像及其同步状态的表。

---

### 4. SMS 备份/恢复（存储管理服务）

所有主要的备份/恢复供应商均支持 **Novell 存储管理服务（SMS）** 基础架构。SMS 允许这些供应商全面保护所有 Novell 元数据，包括文件系统访问控制列表、继承权限过滤器、数据库、电子邮件邮局、邮箱以及 eDirectory 对象和属性。

---

### 5. NSS 存储池快照

**NSS 存储池快照**允许随时备份活动数据。快照工具已集成到基于 Web 的管理界面中，与硬件供应商无关，用户可以从活动快照卷中查看和选择文件版本。快照数据继承原始数据的权限。

---

### 汇总表

| 方法 | 中文术语 | 用途 |
|---|---|---|
| Hot Fix | 热调整 / 热修复 | 自动重定向坏磁盘块 |
| 双重目录 | 双重目录 | 文件目录冗余 |
| 磁盘镜像 | 磁盘镜像 | 同通道磁盘冗余 |
| 磁盘双工 | 磁盘双工 | 跨通道磁盘冗余（更强） |
| SMS 备份/恢复 | 存储管理服务 | 完整的网络数据备份与恢复 |
| NSS 存储池快照 | 存储池快照 | 活动数据的即时备份 |

---

**参考来源：**
- [How NetWare Protects Network Data](https://www.novell.com/documentation/nw6p/trad_enu/data/he5cv8fw.html)
- [Hot Fix – Redirecting Bad Blocks](https://www.novell.com/documentation/nw6p/sdiskenu/data/hi4exu95.html)
- [Mirroring and Duplexing](https://teaming.novell.com/documentation/nw6p/sdiskenu/data/hefkruob.html)
- [Novell OES – Data Protection and Security](https://teaming.novell.com/documentation/oes2015/stor_ovw_lx/data/amqlfhu.html)