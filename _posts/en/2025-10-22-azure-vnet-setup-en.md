---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Azure Virtual Network Setup Guide
translated: false
type: note
---

### Azure Virtual Network Configuration Overview

To set up your described architecture in Azure, we'll use a single Virtual Network (VNet) for simplicity, with multiple subnets to separate public-facing resources (like your API and admin service) from internal ones (like the MQ/Redis VM). This allows secure internal communication via private IPs while controlling public access through Network Security Groups (NSGs). We'll also configure SSH access restricted to your team's IP ranges.

Key principles:

- **Public access**: Use public IPs and NSGs to allow inbound traffic only on specific ports (443 for API, 80 for admin) from the internet or team IPs.
- **Internal communication**: VMs in the same VNet can communicate freely on private IPs; use NSGs to fine-tune (e.g., allow backend to MQ on port 6379 for Redis).
- **SSH access**: Restrict to bastion or direct SSH on port 22 from team IPs.
- **Admin service**: Treat it like the API but on port 80, restricted to team.

This assumes you're using Azure Portal or CLI; I'll provide high-level steps with CLI examples for reproducibility. Costs apply for VNets, VMs, and public IPs.

#### Step 1: Create the Virtual Network and Subnets

Create a VNet with two subnets:

- **Public Subnet** (e.g., for API and admin VMs): Allows public IPs.
- **Private Subnet** (e.g., for MQ/Redis VM): No public IPs; internal only.

Using Azure CLI (install via `az login` first):

```bash
# Create resource group
az group create --name myResourceGroup --location eastus

# Create VNet
az network vnet create \
  --resource-group myResourceGroup \
  --name myVNet \
  --address-prefixes 10.0.0.0/16 \
  --subnet-name PublicSubnet \
  --subnet-prefixes 10.0.1.0/24

# Add private subnet
az network vnet subnet create \
  --resource-group myResourceGroup \
  --vnet-name myVNet \
  --name PrivateSubnet \
  --address-prefixes 10.0.2.0/24
```

#### Step 2: Create VMs and Assign Networking

- **Backend API VM** (in PublicSubnet): Public IP for 443 access.
- **MQ/Redis VM** (in PrivateSubnet): Private IP only.
- **Admin VM** (in PublicSubnet): Public IP for 80 access.

CLI examples:

```bash
# Backend API VM
az vm create \
  --resource-group myResourceGroup \
  --name backendVM \
  --image UbuntuLTS \
  --admin-username azureuser \
  --admin-password <strong-password> \
  --vnet-name myVNet \
  --subnet PublicSubnet \
  --public-ip-sku Standard

# Get public IP for API
API_PUBLIC_IP=$(az vm show -d -g myResourceGroup -n backendVM --query publicIps -o tsv)

# MQ/Redis VM (no public IP)
az vm create \
  --resource-group myResourceGroup \
  --name mqVM \
  --image UbuntuLTS \
  --admin-username azureuser \
  --admin-password <strong-password> \
  --vnet-name myVNet \
  --subnet PrivateSubnet

# Get private IP for internal comm
MQ_PRIVATE_IP=$(az vm show -g myResourceGroup -n mqVM --query privateIps -o tsv)

# Admin VM
az vm create \
  --resource-group myResourceGroup \
  --name adminVM \
  --image UbuntuLTS \
  --admin-username azureuser \
  --admin-password <strong-password> \
  --vnet-name myVNet \
  --subnet PublicSubnet \
  --public-ip-sku Standard

# Get public IP for admin
ADMIN_PUBLIC_IP=$(az vm show -d -g myResourceGroup -n adminVM --query publicIps -o tsv)
```

On the VMs:

- Install your API on backendVM (e.g., listen on 443 with SSL).
- Install Redis/MQ on mqVM (listen on 6379).
- Install admin service on adminVM (listen on 80).

#### Step 3: Configure Network Security Groups (NSGs)

NSGs act as firewalls. Associate one NSG per subnet (or per NIC for finer control). Create rules to allow:

- Public: 443 to backendVM, 80 to adminVM.
- Internal: Backend to MQ on 6379.
- SSH: Port 22 from team IPs (replace `TEAM_IPS` with your CIDR, e.g., 203.0.113.0/24).

CLI for NSGs:

```bash
# Create NSG for Public Subnet
az network nsg create \
  --resource-group myResourceGroup \
  --name publicNSG

# Rules for public NSG
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

# Associate public NSG to PublicSubnet
az network vnet subnet update \
  --resource-group myResourceGroup \
  --vnet-name myVNet \
  --name PublicSubnet \
  --network-security-group publicNSG

# Create NSG for Private Subnet
az network nsg create \
  --resource-group myResourceGroup \
  --name privateNSG

# Allow internal traffic from backend to MQ
az network nsg rule create \
  --resource-group myResourceGroup \
  --nsg-name privateNSG \
  --name AllowFromBackend \
  --priority 100 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes '10.0.1.0/24'  # PublicSubnet CIDR
  --source-port-ranges '*' \
  --destination-address-prefixes '*' \
  --destination-port-ranges 6379  # Redis port

# Allow SSH to private VM if needed (from team via bastion or VPN)
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

# Associate private NSG
az network vnet subnet update \
  --resource-group myResourceGroup \
  --vnet-name myVNet \
  --name PrivateSubnet \
  --network-security-group privateNSG
```

- **Internal Communication**: BackendVM (10.0.1.x) can now reach mqVM (10.0.2.x:6379) without public exposure.
- **Default Deny**: NSGs implicitly deny all other traffic.

#### Step 4: SSH Access for Team

- Direct SSH: Use `ssh azureuser@<VM_PUBLIC_IP> -p 22` from team IPs (already allowed in NSG).
- For private VM: Use Azure Bastion (recommended for security) in the VNet.
  - Create Bastion: `az network bastion create --name myBastion --resource-group myResourceGroup --vnet-name myVNet --location eastus --sku Standard --bastion-subnet-address-prefix 10.0.3.0/26` (add a new BastionSubnet first).
  - Connect via Azure Portal > Bastion > Connect to mqVM using private IP.

#### Step 5: Access the Services

- **Public API**: `https://$API_PUBLIC_IP` (port 443).
- **Admin Service**: `http://$ADMIN_PUBLIC_IP` (port 80, team-only).
- **Test Internal**: From backendVM, `redis-cli -h $MQ_PRIVATE_IP -p 6379`.

#### Additional Best Practices

- **Load Balancer/Application Gateway**: For production, front the API/admin with Azure Application Gateway for WAF/SSL termination.
- **Private Endpoints**: For Redis, use Azure Private Link to avoid subnet exposure.
- **Monitoring**: Enable Azure Network Watcher for traffic logs.
- **Scaling**: If VMs grow, use Availability Sets or Scale Sets.
- **Cleanup**: `az group delete --name myResourceGroup --yes --no-wait`.

For full docs: [Azure VNet Overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview), [NSG Rules](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview). If you need Terraform/ARM templates or specifics (e.g., exact team IPs), provide more details!
