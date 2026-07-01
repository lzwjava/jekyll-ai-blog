---
audio: false
generated: true
image: false
lang: zh
layout: post
title: NetWare：局域网革命终结
translated: true
type: note
---

Novell NetWare 是网络计算历史上的基础性篇章。它是由 Novell, Inc. 开发的一种开创性和主导性的网络操作系统（NOS），在这些功能变得普遍之前很久，就为个人电脑提供了文件共享、打印和其他服务。在 1980 年代和 1990 年代的大部分时间里，它是无数商业和教育局域网（LANs）的支柱。

以下是其历程的快速概述：

| **Aspect** | **Description** |
| :--- | :--- |
| **What it was** | A discontinued network operating system (NOS) developed by Novell, Inc., designed to provide file, print, and directory services for LANs . |
| **Developer** | Novell, Inc. |
| **Initial Release** | 1983 |
| **Final Release** | Version 6.5 SP8 (May 6, 2009) |
| **Key Protocols** | IPX/SPX (native), later added TCP/IP support natively in version 5 . |
| **Core Innovation** | Shifted from disk sharing to **file sharing**, introducing file-level access and locking for better efficiency and data integrity . |
| **Successor** | Open Enterprise Server (OES), which runs NetWare services on a SUSE Linux Enterprise Server kernel . |
| **Current Status** | Discontinued; general support ended in 2010, with extended support until the end of 2015 . |

### 📜 A Historical Powerhouse

- **Origins (Early 1980s)**: NetWare 的故事始于 1981 年，一群 Brigham Young University 的学生——Drew Major、Dale Neibaur、Kyle Powell，以及后来的 Mark Hurst——在从事一个咨询项目。他们最初旨在为 CP/M 创建一个磁盘共享系统，但转向构建一个针对当时新兴的 IBM 兼容 PC 的文件共享系统。为了测试他们的创作，他们甚至编写了一个文本模式游戏 **Snipes**，它被公认为个人电脑上最早的网络应用程序之一。
- **The File-Sharing Revolution**: NetWare 的根本创新是从流行的“disk sharing”模型转向真正的 **file sharing**。NetWare 服务器不是将网络存储视为远程磁盘驱动器，而是智能地管理文件级别的访问、锁定和数据完整性。这种受主frame 和 minicomputer 系统启发的做法，远比竞争对手的产品更高效和可靠。
- **Hardware Independence and Performance**: 其成功的关键在于硬件独立性。与某些竞争对手不同，NetWare 可以运行在任何基于 Intel 的 PC 上，支持各种网卡和硬盘。它还以卓越性能闻名，通常由于优化的 kernel 和高效的磁盘缓存，大幅超越竞争对手。

### 🏗️ Core Architecture and Key Features

- **Architecture**: NetWare 是围绕专用服务器构建的，该服务器运行一个专用的多任务 kernel。客户端工作站（最初运行 DOS）使用一个小 Terminate-and-Stay-Resident (TSR) 程序与服务器通信，并将网络驱动器映射为本地驱动器。该系统的核心组件包括：
  - **File Server Kernel**: 通过 **NetWare Core Protocol (NCP)** 管理文件系统、安全性和客户端请求。
  - **Workstation Shell**: 驻留在客户端机器上，将本地请求重定向到网络服务器。
  - **Communication Protocols**: 最初依赖 **IPX/SPX** 协议栈，该栈源自 Xerox 的 XNS。
- **Innovative Features**: NetWare 持续引入使其脱颖而出的先进功能：
  - **System Fault Tolerance (SFT)**: 通过写后读验证、磁盘镜像（SFT II）和磁盘双工，提供强大的数据保护，确保高可靠性。
  - **NetWare Directory Services (NDS)**: 在 4.x 版本（1993 年）引入，NDS 是一种革命性的全局目录服务，允许管理员从单一点管理整个网络中的用户、组和资源（如服务器和打印机）。这大大领先于早期版本使用的平面“bindery”系统，并是 Microsoft Active Directory 等目录服务的先驱。
  - **Modularity (NLMs)**: 3.x 版本引入 **NetWare Loadable Modules (NLMs)**，允许管理员动态加载和卸载服务，如防病毒软件、备份代理和数据库支持，而无需重启服务器。

### 📈 The Rise, Dominance, and Decline

- **Market Dominance**: 到 1990 年代初至中叶，NetWare 是网络操作系统市场的无可争议领导者，一度占有超过 **70% 的市场份额**。其性能、可靠性和先进功能使其成为全球企业和学校 PC 网络的默认选择。
- **Challenges and Decline**: 几个因素导致其最终衰落：
  - **The Rise of Windows NT**: Microsoft 的 Windows NT 提供了引人注目的替代方案。它提供文件和打印服务（NetWare 功能的一个子集），同时还作为应用服务器、邮件服务器甚至桌面操作系统。这种垂直整合和熟悉的 Windows 界面使其具有吸引力。
  - **The TCP/IP Shift**: 随着互联网兴起，TCP/IP 成为通用网络协议。NetWare 全面采用它较晚，因为它最初基于自己的 IPX/SPX 协议。虽然 5.0 版本（1998 年）引入了原生 TCP/IP 支持，但这是一个相对较晚的重大转变。
- **Legacy and Successor**: Novell 最终将其服务迁移到 Linux 平台。NetWare 的继任者 **Open Enterprise Server (OES)** 于 2005 年发布。OES 允许曾经由 NetWare 托管的所有服务运行在 SUSE Linux Enterprise Server kernel 上，标志着原始 NetWare kernel 的终结。NetWare 的最终版本 6.5 SP8 于 2009 年发布，支持于 2015 年正式结束。

总之，NetWare 不仅仅是一个产品；它是驱动第一代大规模 PC 网络的引擎。其在文件共享、目录服务和系统容错方面的开创性概念，为现代网络操作系统奠定了基础，在 IT 世界留下了不可磨灭的印记。

希望这个全面介绍能让您清楚了解 NetWare 的重要性。您对特定版本或其技术协议如 NDS 的更详细探讨感兴趣吗？
