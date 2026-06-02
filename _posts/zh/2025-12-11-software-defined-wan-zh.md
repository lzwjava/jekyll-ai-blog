---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 理解软件定义广域网
translated: true
type: note
---

问题：什么是软件定义广域网（SD-WAN）？

回答：

软件定义广域网（SD-WAN）是一种现代网络方法，它使用基于软件的控制来管理和优化广域网（WAN）连接，取代或增强传统的以硬件为中心的WAN架构（如MPLS）。

### SD-WAN 的主要特点
- **集中管理**：一个软件控制器（通常基于云）提供一个单一的视图来从任何地方配置、监控和管理整个WAN。
- **传输独立性**：它可以同时使用多种连接类型——MPLS、宽带互联网、4G/5G LTE、卫星——并智能地为每个应用程序选择最佳路径。
- **应用感知路由**：实时识别应用程序，并根据业务策略、性能要求、延迟、抖动、丢包和成本来路由流量（例如，将Zoom通话通过性能最佳的链接发送，而将批量备份通过廉价宽带发送）。
- **内置安全性**：大多数解决方案直接在SD-WAN边缘设备中或通过云安全服务提供下一代防火墙功能、加密、分段和安全Web网关。
- **零接触配置**：新的分支机构设备可以直接运送到站点，插电后即可自动从云控制器下载其配置。
- **覆盖架构**：在任何底层传输之上创建一个安全的虚拟覆盖网络，抽象物理连接。

### 与传统WAN相比的主要优势

| 方面              | 传统WAN（例如MPLS）       | SD-WAN
|----------------------|------------------------------------|----------------------------------------|
| 成本                 | 高（昂贵的MPLS线路）       | 低（使用廉价宽带/互联网） |
| 部署时间      | 数周到数月                    | 数小时到数天 |
| 带宽灵活性| 固定，难以扩展               | 动态，易于增加带宽 |
| 性能          | 一致但受电路限制          | 每个应用程序优化，通常更好 |
| 云就绪      | 差（回传到总部）           | 直接云访问，更低延迟 |
| 管理           | 逐设备CLI               | 集中式GUI/API/编排 |

### 常见用例
- 将分支机构、零售店或远程工作人员连接到总部和云服务（Microsoft 365、AWS、Azure、Salesforce等）。
- 通过混合WAN取代或补充昂贵的MPLS。
- 改善实时应用程序（VoIP、视频会议、VDI）的性能。
- 实现快速部署弹出式或临时站点（建筑工地、灾难恢复、活动）。

### 主要SD-WAN供应商（截至2025年）
- Cisco (Viptela & Meraki)
- VMware/VeloCloud (now Broadcom)
- Fortinet
- Palo Alto Networks (Prisma SD-WAN)
- Aryaka
- Cato Networks
- Cloudflare
- Silver Peak (HPE Aruba EdgeConnect)
- Versa Networks
- Juniper (Mist & Session Smart)

简而言之，SD-WAN将控制平面与底层硬件和传输解耦，与传统WAN架构相比，为组织提供了更高的灵活性、更好的性能、更强的安全性以及显著更低的成本。自2018-2019年左右，它已成为企业广域网的默认选择，并继续与SASE（Secure Access Service Edge）和SSE集成发展。
