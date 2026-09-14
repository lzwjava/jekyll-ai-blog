---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 戴尔C4130主板概览
translated: true
type: note
---

**问题：** Dell C4130 主板（系统板）简介是什么？

**答案：**

Dell PowerEdge C4130 是一款专为高性能计算（HPC）和 GPU 加速工作负载设计的 1U 机架式服务器。以下是其系统板及关键组件的概述：

---

**概览**

PowerEdge C4130 在超密集平台中提供了超级计算所需的灵活性与性能，专为高性能计算（HPC）和虚拟桌面基础架构（VDI）工作负载而构建。它面向研究、模拟仿真、金融、能源勘探等类似领域。

---

**系统板（主板）作用**

系统板（又称主板）是系统中的主印刷电路板，带有不同的连接器，用于连接系统的不同组件或外围设备。系统板为这些组件提供电气连接。

---

**关键规格**

**外形规格与处理器**
C4130 是一款 1U 机架式服务器，支持 Intel Xeon 处理器 E5-2600 v3/v4 产品家族，具有 2 个处理器插槽，采用 C612 系列芯片组，内部互连速度最高可达 9.6 GT/s。

**内存**
支持 DDR4 DIMM，速度最高达 2400 MT/s，提供 16 个 DIMM 插槽，可接受 4 GB、8 GB、16 GB、32 GB 及 64 GB 内存模块。

**GPU 支持**
系统最多支持四个图形处理单元（GPU）。所有 GPU 卡必须为同一类型和型号——不支持混合使用 GPU。支持标准 PCIe GPU 和 SXM2 外形规格的 GPU（使用 NVLink 板卡配置）。

**扩展总线**
C4130 支持通过扩展卡提升板在系统板上安装 PCIe Gen 3 扩展卡，并支持四种扩展卡提升板配置。

**存储**
存储包括最多 2 块 1.8 英寸 SATA SSD 启动盘，可选配 RAID 控制器（PERC H330）。可选的数据驱动器托架最多支持 4 块 2.5 英寸 SAS/SATA 驱动器。

**网络**
系统包括 2 个 1 GbE LOM（板载 LAN），背面最多支持 2 个 PCIe 3.0 半高适配器，支持 InfiniBand FDR 和 NVIDIA GPUDirect。对于某些加速器配置，可选的 96 通道 PCIe 3.0 交换机。

**电源**
由 1600 W 热插拔 PSU 供电，可选配 1+1 冗余 PSU 配置。

**管理**
系统管理包括符合 IPMI 2.0 规范、Dell OpenManage Essentials、Dell OpenManage Mobile 及 Dell OpenManage Power Center。主板还集成了 iDRAC（集成戴尔远程访问控制器），用于带外管理。

---

**参考资料：**
- [Dell PowerEdge C4130 用户手册 – 概览](https://www.dell.com/support/manuals/en-us/poweredge-c4130/c4130ownersmanual/dell-poweredge-c4130-overview?guid=guid-b5b8b87a-5190-41b9-aeed-94c256b9266a&lang=en-us)
- [Dell PowerEdge C4130 规格表（PDF）](https://gotomojo.com/wp-content/uploads/2018/04/EMEA-Spec-Sheets-C4130-Specifications.pdf)
- [Mojo Systems – C4130 规格与信息](https://www.gotomojo.com/servers/dell-emc-poweredge/c-series/c4130/)