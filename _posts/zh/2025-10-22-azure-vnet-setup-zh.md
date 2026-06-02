---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Azure虚拟网络设置指南
translated: true
type: note
---

### Azure 虚拟网络配置概述

为在 Azure 中搭建您描述的架构，我们将使用单个虚拟网络（VNet）以简化操作，并通过多个子网来隔离面向公众的资源（如 API 和管理服务）与内部资源（如 MQ/Redis 虚拟机）。这样既可通过私有 IP 实现安全的内部通信，又能通过网络安全性组（NSG）控制公共访问。我们还将配置仅限于您团队 IP 范围的 SSH 访问。

核心原则：

- **公共访问**：使用公共 IP 和 NSG，仅允许来自互联网或团队 IP 的特定端口入站流量（API 使用 443 端口，管理服务使用 80 端口）。
- **内部通信**：同一 VNet 中的虚拟机可通过私有 IP 自由通信；使用 NSG 进行微调（例如，允许后端通过 6379 端口访问 MQ/Redis）。
- **SSH 访问**：限制为仅允许来自团队 IP 通过堡垒机或直接 SSH 连接 22 端口。
- **管理服务**：类似于 API 但使用 80 端口，且限制为仅团队可访问。

假设您使用 Azure 门户或 CLI；我将提供高级步骤及 CLI 示例以确保可重现性。VNet、虚拟机和公共 IP 均会产生费用。

#### 步骤 1：创建虚拟网络和子网

创建一个包含两个子网的 VNet：

- **公共子网**（例如，用于 API 和管理虚拟机）：允许分配公共 IP。
- **私有子网**（例如，用于 MQ/Redis 虚拟机）：不分配公共 IP；仅限内部访问。

使用 Azure CLI（请先通过 `az login` 安装）：

```bash
# 创建资源组
az group create --name myResourceGroup --location eastus

# 创建 VNet
az network vnet create \
  --resource-group myResourceGroup \
  --name myVNet \
  --address-prefixes 10.0.0.0/16 \
  --subnet-name PublicSubnet \
  --subnet-prefixes 10.0.1.0/24

# 添加私有子网
az network vnet subnet create \
  --resource-group myResourceGroup \
  --vnet-name myVNet \
  --name PrivateSubnet \
  --address-prefixes 10.0.2.0/24
```

#### 步骤 2：创建虚拟机并配置网络

- **后端 API 虚拟机**（位于 PublicSubnet）：分配公共 IP 用于 443 端口访问。
- **MQ/Redis 虚拟机**（位于 PrivateSubnet）：仅分配私有 IP。
- **管理虚拟机**（位于 PublicSubnet）：分配公共 IP 用于 80 端口访问。

CLI 示例：

```bash
# 后端 API 虚拟机
az vm create \
  --resource-group myResourceGroup \
  --name backendVM \
  --image UbuntuLTS \
  --admin-username azureuser \
  --admin-password <strong-password> \
  --vnet-name myVNet \
  --subnet PublicSubnet \
  --public-ip-sku Standard

# 获取 API 的公共 IP
API_PUBLIC_IP=$(az vm show -d -g myResourceGroup -n backendVM --query publicIps -o tsv)

# MQ/Redis 虚拟机（无公共 IP）
az vm create \
  --resource-group myResourceGroup \
  --name mqVM \
  --image UbuntuLTS \
  --admin-username azureuser \
  --admin-password <strong-password> \
  --vnet-name myVNet \
  --subnet PrivateSubnet

# 获取内部通信所需的私有 IP
MQ_PRIVATE_IP=$(az vm show -g myResourceGroup -n mqVM --query privateIps -o tsv)

# 管理虚拟机
az vm create \
  --resource-group myResourceGroup \
  --name adminVM \
  --image UbuntuLTS \
  --admin-username azureuser \
  --admin-password <strong-password> \
  --vnet-name myVNet \
  --subnet PublicSubnet \
  --public-ip-sku Standard

# 获取管理服务的公共 IP
ADMIN_PUBLIC_IP=$(az vm show -d -g myResourceGroup -n adminVM --query publicIps -o tsv)
```

在虚拟机上：

- 在 backendVM 上安装您的 API（例如，在 443 端口监听并启用 SSL）。
- 在 mqVM 上安装 Redis/MQ（在 6379 端口监听）。
- 在 adminVM 上安装管理服务（在 80 端口监听）。

#### 步骤 3：配置网络安全性组（NSG）

NSG 充当防火墙。为每个子网关联一个 NSG（或为每个 NIC 关联以实现更精细控制）。创建规则以允许：

- 公共访问：443 端口访问 backendVM，80 端口访问 adminVM。
- 内部通信：后端到 MQ 的 6379 端口。
- SSH：来自团队 IP 的 22 端口访问（将 `TEAM_IPS` 替换为您的 CIDR，例如 203.0.113.0/24）。

NSG 的 CLI 配置：

```bash
# 为公共子网创建 NSG
az network nsg create \
  --resource-group myResourceGroup \
  --name publicNSG

# 公共 NSG 的规则
az network nsg rule create \
  --resource-group myResourceGroup \
  --nsg-name publicNSG \
  --name AllowHTTPS \
  --priority 100 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes '*' \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 443

az network nsg rule create \
  --resource-group myResourceGroup \
  --nsg-name publicNSG \
  --name AllowHTTPAdmin \
  --priority 101 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes 'TEAM_IPS' \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 80

az network nsg rule create \
  --resource-group myResourceGroup \
  --nsg-name publicNSG \
  --name AllowSSH \
  --priority 102 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes 'TEAM_IPS' \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 22

# 将公共 NSG 关联到 PublicSubnet
az network vnet subnet update \
  --resource-group myResourceGroup \
  --vnet-name myVNet \
  --name PublicSubnet \
  --network-security-group publicNSG

# 为私有子网创建 NSG
az network nsg create \
  --resource-group myResourceGroup \
  --name privateNSG

# 允许从后端到 MQ 的内部流量
az network nsg rule create \
  --resource-group myResourceGroup \
  --nsg-name privateNSG \
  --name AllowFromBackend \
  --priority 100 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes '10.0.1.0/24'  # 公共子网 CIDR
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 6379  # Redis 端口

# 如果需要，允许 SSH 访问私有虚拟机（来自团队，通过堡垒机或 VPN）
az network nsg rule create \
  --resource-group myResourceGroup \
  --nsg-name privateNSG \
  --name AllowSSHPrivate \
  --priority 101 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes 'TEAM_IPS' \
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 22

# 关联私有 NSG
az network vnet subnet update \
  --resource-group myResourceGroup \
  --vnet-name myVNet \
  --name PrivateSubnet \
  --network-security-group privateNSG
```

- **内部通信**：BackendVM（10.0.1.x）现在可以无需公共暴露即可访问 mqVM（10.0.2.x:6379）。
- **默认拒绝**：NSG 默认隐式拒绝所有其他流量。

#### 步骤 4：团队的 SSH 访问

- 直接 SSH：从团队 IP 使用 `ssh azureuser@<VM_PUBLIC_IP> -p 22`（已在 NSG 中允许）。
- 对于私有虚拟机：推荐使用 VNet 中的 Azure Bastion（更安全）。
  - 创建 Bastion：`az network bastion create --name myBastion --resource-group myResourceGroup --vnet-name myVNet --location eastus --sku Standard --bastion-subnet-address-prefix 10.0.3.0/26`（需先添加新的 BastionSubnet）。
  - 通过 Azure 门户 > Bastion > 使用私有 IP 连接到 mqVM。

#### 步骤 5：访问服务

- **公共 API**：`https://$API_PUBLIC_IP`（端口 443）。
- **管理服务**：`http://$ADMIN_PUBLIC_IP`（端口 80，仅限团队访问）。
- **内部测试**：从 backendVM 执行 `redis-cli -h $MQ_PRIVATE_IP -p 6379`。

#### 其他最佳实践

- **负载均衡器/应用程序网关**：在生产环境中，使用 Azure 应用程序网关为 API/管理服务提供前端，以实现 WAF/SSL 终止。
- **私有端点**：对于 Redis，使用 Azure 私有链接以避免子网暴露。
- **监控**：启用 Azure 网络观察程序以获取流量日志。
- **扩展**：如果虚拟机数量增加，请使用可用性集或规模集。
- **清理**：`az group delete --name myResourceGroup --yes --no-wait`。

完整文档请参考：[Azure VNet 概述](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview)、[NSG 规则](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview)。如果您需要 Terraform/ARM 模板或具体细节（例如确切的团队 IP），请提供更多信息！
