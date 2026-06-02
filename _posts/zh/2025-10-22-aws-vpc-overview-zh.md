---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: AWS虚拟私有云概述
translated: true
type: note
---

### 什么是 AWS 中的 VPC？

Amazon Virtual Private Cloud（VPC）是一项基础的 AWS 服务，它允许您在 AWS 云中创建一个逻辑隔离的区域，用于启动和管理您的 AWS 资源，例如 EC2 实例、数据库和负载均衡器。它本质上为您在 AWS 内提供了一个私有的、可定制的虚拟网络环境，类似于您如何设置传统数据中心网络，但具备云的可扩展性和安全性。

#### 核心组件与特性

- **子网**：将您的 VPC 划分为更小的网段（公共或私有），以组织资源并控制访问。
- **隔离性**：您的 VPC 专属于您的 AWS 账户，并与其他 VPC 隔离，确保安全性和合规性。
- **IP 地址分配**：您可以自定义 IP 地址范围（CIDR 块），并可以使用 IPv4、IPv6 或两者。
- **路由与网关**：包括路由表、互联网网关（用于公共访问）、NAT 网关（用于私有出站流量）以及 VPC 对等连接（用于连接多个 VPC）。
- **安全性**：内置工具如安全组（实例级防火墙）和网络 ACL（子网级防火墙），用于控制入站/出站流量。

#### 为什么使用 VPC？

默认情况下，所有 AWS 资源都会启动到一个 VPC 中（您无法再选择退出）。它提供了对网络的控制，通过保持资源私有来增强安全性，并支持混合设置（例如，通过 VPN 或 Direct Connect 连接到本地数据中心）。对于生产工作负载来说，避免将资源直接暴露在互联网上是至关重要的。

如需动手设置，请查看 AWS 管理控制台或 CLI 来创建您的第一个 VPC。

#### 参考资料

- [什么是 Amazon VPC？](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
- [Amazon VPC 概述](https://aws.amazon.com/vpc/)
- [Amazon VPC 工作原理](https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html)
- [Amazon VPC 简介](https://www.geeksforgeeks.org/devops/amazon-vpc-introduction-to-amazon-virtual-cloud/)
