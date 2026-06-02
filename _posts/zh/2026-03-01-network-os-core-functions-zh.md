---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网络操作系统核心功能详解
translated: true
type: note
---

**问题：** 什么是 **network operating system**？除了 operating system 的一般功能外，**network operating system** 的特定功能有哪些？

**答案：**

**network operating system (NOS)** 是一个专门设计或优化用于在网络环境中运行的操作系统。它充当用户与网络资源之间的接口，使用户、应用程序和设备能够以协调和安全的方式访问、共享和管理网络中的资源。

它可以理解为：

- 各种网络服务软件和网络协议的集合
- 在网络环境中实现资源共享和网络通信的软件平台
- 用户使用网络资源的管理的和控制系统

### 常规 operating system 的通用功能（与 network OS 共享）

- Process management
- Memory management
- File management
- Device management
- Job management / user interface

### 使 **network operating system** 区别于一般（stand-alone）operating system 的特定功能

- **File service**
  在网络中提供集中式文件存储、共享、访问控制、同步和锁定机制（NOS 的最基本和核心功能）。

- **Print service**
  实现网络打印机共享、打印队列管理、优先级调度和 spooling 服务。

- **Database service**（在某些 NOS 定义中）
  在网络上提供分布式或集中式数据库访问、事务管理和数据一致性机制。

- **Communication service**
  提供网络节点之间可靠的数据传输，包括 message passing、remote procedure call (RPC)、named pipes、sockets 等。

- **Network management service**
  包括用户账户管理、权限控制、网络监控、故障检测、性能统计、安全审计和集中式网络管理。

- **Internet/Intranet service**
  提供 TCP/IP protocol stack、web 服务（HTTP/HTTPS）、email 服务（SMTP/POP3/IMAP）、FTP 服务、DNS 解析、DHCP 服务、远程访问（VPN、terminal services）等的支持。

- **Directory service**（在现代 NOS 中非常重要）
  提供集中式用户认证、名称解析和资源定位服务（例如 Active Directory、LDAP、NIS、eDirectory）。

- **Name service / name resolution**
  将资源名称映射到网络地址（不同于 DNS，更专注于内部网络命名）。

- **Remote management and remote execution**
  允许管理员管理远程服务器、远程执行命令以及进行软件分发/修补。

总之，**network operating system** 最经典和常用列出的 **核心特定功能** 是：

- File service
- Print service
- Database service（有时包括）
- Communication service
- Network management service
- Internet service

这些功能使多用户、多计算机网络环境中实现高效资源共享、集中管理和安全协作成为可能。

**参考文献：**

- 无（基于 network operating system 的标准教科书定义）
