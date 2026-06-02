---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: AWS 核心网络服务概述
translated: true
type: note
---

问题：AWS 提供哪些典型的网络服务，包括子网、VPC、NAT 等？

回答：

AWS 提供了一套全面的网络服务，其核心是 **Amazon Virtual Private Cloud (Amazon VPC)**，它允许用户在 AWS 云中创建逻辑隔离的虚拟网络。这些服务能够为 EC2 实例等资源实现安全、可扩展和灵活的网络配置。

### 核心 VPC 组件和功能
- **Virtual Private Cloud (VPC)**: AWS 云中逻辑隔离的部分，您可以在其中定义自己的虚拟网络。您可以控制 IP 地址范围 (CIDR 块)、子网、路由表和网关。VPC 跨区域中的多个可用区以实现高可用性。

- **子网（Subnets）**: VPC IP 地址范围的细分。
  - **公共子网（Public subnets）**: 具有通往 Internet Gateway 的路由，用于直接访问互联网。
  - **私有子网（Private subnets）**: 没有直接的互联网访问权限；用于安全资源，如数据库。

- **Internet Gateway (IGW)**: 连接到 VPC，使 VPC 中的资源能够与公共互联网通信。

- **NAT (Network Address Translation)**:
  - **NAT Gateway**: 一种托管的、高度可用的 AWS 服务，放置在公共子网中。它允许私有子网中的实例发起出站互联网流量（例如，用于更新或 API 调用），同时阻止来自互联网的入站流量。
  - **NAT Instance**: 一种较旧的、用户管理的替代方案，使用 EC2 实例进行 NAT；与 NAT Gateway 相比，管理开销更高，因此不推荐使用。

### 其他典型的网络服务
- **路由表（Route Tables）**: 控制 VPC 内部以及到外部目的地（例如，0.0.0.0/0 路由到 IGW 或 NAT Gateway）的流量路由。
- **安全组（Security Groups）和网络 ACLs（Network ACLs）**: 充当虚拟防火墙——安全组在实例级别，NACL 在子网级别。
- **VPC Peering**: 连接多个 VPC（甚至跨账户或区域）以进行私有通信。
- **Elastic Load Balancing (ELB)**: 在资源之间分配传入流量。
- **AWS Transit Gateway**: 简化多个 VPC 和本地网络之间的连接。
- **AWS Direct Connect**: 从本地到 AWS 的专用私有连接。
- **AWS PrivateLink**: 到 AWS 服务或合作伙伴服务的安全私有连接，而无需将流量暴露给互联网。

这些服务构成了构建安全架构的基础，例如具有面向公众的负载均衡器和通过 NAT 访问互联网的私有后端服务器的多层应用程序。

参考资料：

- [Amazon VPC 概览](https://aws.amazon.com/vpc/)
- [什么是 Amazon VPC？](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [NAT 网关](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html)
- [VPC 中的子网](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html)
- [AWS 网络和内容分发](https://aws.amazon.com/products/networking/)
