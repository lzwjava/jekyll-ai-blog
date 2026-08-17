---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 'NetWare: 网络操作系统先驱'
translated: true
type: note
---

**Novell NetWare** 是由 Novell, Inc. 开发的开拓性**网络操作系统 (NOS)**，于 1983 年首次发布。它在整个 1980 年代和 1990 年代主导了 LAN（局域网）服务器市场，尤其是在企业和办公环境中。

## 主要特性

- **专为文件/打印共享而构建**：与 Windows 或 UNIX 等通用操作系统不同，NetWare 从头开始设计，旨在通过网络向客户端机器提供文件和打印服务。
- **客户端-服务器模型**：客户端 PC（通常运行 DOS 或后来的 Windows）使用 IPX/SPX 协议（后来为 TCP/IP）连接到 NetWare 服务器。
- **高性能**：其文件系统和 I/O 栈在当时极为快速高效，通常优于竞争对手。
- **高可靠性**：以强大的数据完整性功能而闻名——正是你之前问题中提到的那些（Hot Fix、read-after-write verification、disk mirroring、disk duplexing），此外还有日志记录和容错（SFT — System Fault Tolerance）。

## 历史意义

- **NCP 协议**：NetWare Core Protocol，用于文件/打印服务。
- **NDS（Novell Directory Services）**：一种开创性的目录服务（于 1993 年在 NetWare 4.x 中引入），用于管理网络中的用户、组和资源——对后来的目录系统（如 Microsoft 的 Active Directory）产生了重大影响。
- **衰落**：从 1990 年代后期开始，NetWare 输给了 Microsoft Windows NT/2000 Server，后者将文件/打印服务与更通用的应用程序支持捆绑在一起。Novell 于 2014 年被 Micro Focus 收购，NetWare 如今基本已过时——其继任者 Open Enterprise Server（OES）运行在 Linux 上。

## 为什么它出现在考试题目中

NetWare 的磁盘管理功能（Hot Fix、read-after-write verification、disk mirroring/duplexing）成为**计算机网络/操作系统**认证课程（例如 CNE — Certified Novell Engineer）中的经典考试主题，尤其是在中国的 CS 课程中，这就是你之前问题来自该背景的原因。
