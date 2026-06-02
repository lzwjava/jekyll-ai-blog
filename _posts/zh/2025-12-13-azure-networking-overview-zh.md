---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Azure 网络服务概述
translated: true
type: note
---

问题：Azure 提供哪些典型的网络服务，例如子网、VPC 等效项、NAT 等？

回答：

Azure 提供了一整套**网络服务**，以构建安全、可扩展和互联的云基础设施。其核心基础是 **Azure Virtual Network (VNet)**，它等同于 AWS VPC——一个逻辑隔离的云中私有网络，您可以在其中部署虚拟机、容器和 PaaS 服务等资源。

### 主要 Azure 网络服务及其等效项

- **Virtual Network (VNet)**：等同于 AWS VPC。它定义了一个私有 IP 地址空间，并支持 Azure 资源、互联网和本地网络之间的安全通信。
- **Subnets**：在 VNet 中，您可以创建多个子网来细分地址空间。资源（例如 VM）部署到特定的子网中。与 AWS 不同，Azure 没有固有的“公共”与“私有”子网之分；可访问性取决于配置（例如，公共 IP、NSG、路由）。
- **NAT Gateway**：等同于 AWS NAT Gateway。为私有子网中的资源提供可扩展、托管的出站互联网连接（源 NAT/SNAT）。将其附加到一个或多个子网，即可提供可靠的出站流量，而无需直接暴露实例。
- **VPN Gateway**：通过公共互联网（IPsec/IKE）实现站点到站点、点到站点或 VNet 到 VNet 的加密连接。支持用于重叠 IP 地址的 NAT 规则。
- **ExpressRoute**：到 Azure 的私有、专用连接（绕过公共互联网），类似于 AWS Direct Connect。
- **Virtual Network Peering**：连接多个 VNet（甚至跨区域或订阅），以实现低延迟私有通信，等同于 VPC Peering。
- **Network Security Groups (NSGs)**：应用于子网或 NIC 级别的有状态防火墙，用于控制入站/出站流量。
- **Azure Firewall**：具有威胁情报、应用程序规则和网络过滤的集中式网络安全服务。
- **Load Balancer and Application Gateway**：用于分发流量（分别为第 4 层和第 7 层）。
- **Private Link/Private Endpoints**：私有访问 Azure PaaS 服务，无需公共暴露。
- **Azure Bastion**：通过 RDP/SSH 对 VM 进行安全访问，无需公共 IP。

这些服务支持混合设置、安全分段和全局连接，同时与 Network Watcher 等监控工具集成。

参考资料：

- [Azure Virtual Network 概述](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview)
- [Azure NAT Gateway 概述](https://learn.microsoft.com/en-us/azure/nat-gateway/nat-overview)
- [Azure VPN Gateway 概述](https://learn.microsoft.com/en-us/azure/vpn-gateway/vpn-gateway-about-vpngateways)
- [Azure Networking Services 概述](https://learn.microsoft.com/en-us/azure/networking/fundamentals/networking-overview)
- [Virtual Network Peering 概述](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-network-peering-overview)
