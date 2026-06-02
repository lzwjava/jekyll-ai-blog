---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud 网络服务概览
translated: true
type: note
---

问题：Google Cloud 提供哪些典型的网络服务，例如子网、VNet 等效项、NAT 等？

回答：

Google Cloud 的主要网络服务是 **Virtual Private Cloud (VPC)**，它等同于 AWS VPC 或 Azure VNet。VPC 网络是一种全球性的、可扩展的虚拟网络，为 Compute Engine VM 实例、Google Kubernetes Engine (GKE) 集群和其他资源提供连接。

### 主要功能和组件：
- **VPC Networks**：具有区域子网的全球资源（跨区域）。支持自动模式（每个区域自动创建子网）或自定义模式（手动控制）。VPC 支持 IPv4 和 IPv6、防火墙规则、路由以及通过对等连接、VPN 或 Interconnect 进行连接。
- **Subnets**：VPC 中的区域划分，每个区域具有主（和可选的辅助）IP 范围。用于组织 VM 等资源。专用子网包括仅代理（用于负载均衡器）和 Private NAT 子网。
- **Cloud NAT**：一种托管式分布式网络地址转换服务（不基于 VM 或设备）。
  - **Public NAT**：允许私有 VM（无外部 IP）访问互联网出站，同时阻止入站流量。
  - **Private NAT**：处理 VPC 之间或混合/本地连接之间重叠 IP 范围的转换。
- **其他典型服务**：
  - 用于流量控制的防火墙规则。
  - 路由（子网路由、通过 Cloud Router 的自定义静态/动态路由）。
  - VPC Network Peering，用于连接跨项目/组织的 VPC。
  - 混合连接：Cloud VPN、Cloud Interconnect、Network Connectivity Center。
  - 负载均衡、Private Service Connect 等。

这些服务提供了隔离、安全和可扩展的网络功能，类似于其他云平台，但具有 Google 的全球骨干优势。

参考资料：

- [VPC networks | Google Cloud Documentation](https://cloud.google.com/vpc/docs/vpc)
- [Subnets | Google Cloud Documentation](https://cloud.google.com/vpc/docs/subnets)
- [Cloud NAT overview | Google Cloud Documentation](https://cloud.google.com/nat/docs/overview)
- [Virtual Private Cloud (VPC) | Google Cloud](https://cloud.google.com/vpc)
