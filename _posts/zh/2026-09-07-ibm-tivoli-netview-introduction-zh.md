---
audio: false
generated: true
image: false
lang: zh
layout: post
title: IBM Tivoli NetView 简介
translated: true
type: note
---

**问题：** 什么是 IBM Tivoli NetView，它有什么用途？

**答案：**

## IBM Tivoli NetView — 简介

### 它是什么？

IBM Tivoli NetView 是一款分布式网络管理软件，有助于确保关键业务系统的高可用性。它能发现 TCP/IP 网络、显示拓扑、监控网络健康状况并收集性能数据，以便您快速识别网络故障的根本原因。

现在正式称为 **IBM Z NetView**（原 IBM Tivoli NetView for z/OS），它提供一系列功能，帮助维持 IBM Z 网络的最高可用性，并配备丰富的工具集，用于从单一控制点管理复杂的多厂商、多平台网络和系统。

---

### 核心用途

NetView 提供高级关联工具，可自动处理任何网络或系统事件；支持 TCP/IP 和 SNA 网络；提供满足不同用户需求的用户界面；并与其他产品协同工作，全面呈现网络和系统状况。

---

### 主要组件

通过 NetView 程序，您可以从单一控制点管理来自多个独立软件供应商的复杂网络和系统。其主要组件包括：

- **命令设施** — 用于发送命令和接收消息；为其他组件提供基础功能和服务，如组件间通信、展示服务、数据库服务和自动化设施。
- **硬件监控器** — 收集并显示硬件和软件的事件及统计数据，以识别网络中的故障资源，并提供可能的原因和推荐操作。
- **会话监控器** — 跟踪网络中的 SNA 会话。
- **SNA 拓扑管理器** — 管理系统网络架构资源。
- **NetView 管理控制台** — 图形工作站界面。
- **关联引擎** — 关联事件以实现自动化响应。
- **集成 TCP/IP 服务** — 管理现代 IP 网络资源。

---

### 自动化能力

自动化操作网络 (AON) 内置于 NetView 中，包含 Helpdesk、AutoView、动态显示设施 (DDF)、控制文件和通用例程等组件。最初作为一组生产力辅助工具，后来成为 NetView 的标准功能。

---

### 与其他 IBM 产品的集成

如今，NetView 可与 GDPS 和 Tivoli Business Service Manager 等其他 IBM Z 工具集成。NetView 还通过 IBM System Z Automation 产品支持 CICS、DB2 和 IMS 子系统监控。此外，NetView 通过 Consolidated Audit、NetView 和 z/OS Log (Canzlog) 功能支持增强的日志记录和可视化，用于统一消息记录。

IBM Tivoli Network Manager IP Edition 也与 IBM Tivoli Netcool/OMNIbus 紧密集成，当与 IBM Netcool Operations Insight 基础设施解决方案一起安装时，它作为关键组件提供网络发现、设备监控、拓扑可视化和根本原因分析 (RCA) 能力。

---

### 总结

| 方面 | 详情 |
|---|---|
| 供应商 | IBM（Tivoli 品牌） |
| 平台 | 主要是 z/OS（大型机） |
| 网络支持 | SNA + TCP/IP |
| 主要用途 | 网络监控、自动化、故障管理 |
| 现代名称 | IBM Z NetView |

---

**参考来源：**
- [IBM Z NetView v6.3 概述 — IBM Docs](https://www.ibm.com/docs/SSZJDU_6.3.0/com.ibm.iznetview.doc_6.3.0/netv630_welcome_kc.htm)
- [Tivoli NetView — ESM Solutions](http://www.esm-solutions.com/software/tivoli/tivoli-netview.html)
- [一封给 NetView 的情书 — TechChannel](https://techchannel.com/networking/networking-management-and-monitoring/)
- [Tivoli Network Manager 支持 — IBM](https://www.ibm.com/mysupport/s/topic/0TO500000002JCmGAM/tivoli-network-manager)