---
audio: false
generated: true
image: false
lang: zh
layout: post
title: FreeBSD 存储防火墙专家
translated: true
type: note
---

问题：TrueNAS、OPNsense 和 Allan Jude 是什么？

答案：

**TrueNAS** 是一个流行的开源存储操作系统（最初称为 FreeNAS），由 iXsystems 开发。它主要设计用于 **network-attached storage (NAS)** 用途，并基于强大的 **OpenZFS** 文件系统构建，该文件系统提供出色的数据完整性、自愈能力、快照、复制和类似 RAID 的保护（RAID-Z）。TrueNAS 允许用户使用 SMB、NFS、iSCSI 等协议存储、共享和保护数据。它还支持虚拟化（VMs 和 containers），使其适合家庭实验室、媒体服务器、备份甚至企业环境。有免费的社区版（基于 FreeBSD 的 TrueNAS CORE 和基于 Linux 的 TrueNAS SCALE）以及带有商业支持和硬件设备的付费企业版。

**OPNsense** 是一个免费的开源 **firewall and routing platform**，基于 **FreeBSD**。它于 2015 年创建，作为 pfSense（其本身源于 m0n0wall）的分支。OPNsense 提供高级网络安全功能，包括有状态防火墙、VPN 支持（IPsec、OpenVPN、WireGuard）、入侵检测/预防（IDS/IPS）、流量整形、代理功能以及现代、用户友好的 Web 界面。它广泛用于家庭网络、小型企业和希望获得强大、可定制且定期更新的商业防火墙替代品的企业。

**Allan Jude** 是 **FreeBSD** 和 **OpenZFS** 社区的杰出人物。他是 FreeBSD 开发者、ZFS 专家、Klara Inc.（一家专注于 FreeBSD 和开源咨询/支持的公司）的联合创始人，以及 BSD 世界的知名教育者。他合著了书籍如 "FreeBSD Mastery: ZFS"，并长期担任 **BSD Now** 播客的主持人（以及其他节目）。他经常在会议上演讲，为 FreeBSD/ZFS 开发做出贡献，并因其在存储系统、FreeBSD 内部机制和相关技术的深刻知识而备受尊敬。FreeBSD 生态系统中的许多人钦佩他的工作和贡献。

这三者与 **FreeBSD** 密切相关——TrueNAS 和 OPNsense 均基于 FreeBSD 构建，而 Allan Jude 是该社区的关键贡献者和倡导者。这很可能就是 FreeBSD 粉丝经常一起欣赏这三者的原因。

参考资料：

- [TrueNAS official site](https://www.truenas.com/)
- [TrueNAS Wikipedia](https://en.wikipedia.org/wiki/TrueNAS)
- [OPNsense official site](https://opnsense.org/)
- [OPNsense Wikipedia](https://en.wikipedia.org/wiki/OPNsense)
- [Allan Jude on BSD Now](https://www.bsdnow.tv/hosts/allanjude)
- [Allan Jude LinkedIn](https://ca.linkedin.com/in/allanjude)
