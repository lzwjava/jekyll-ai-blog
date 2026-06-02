---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4-fast
title: Azure Virtual Networking Basics
translated: false
type: note
---

### Azure Virtual Networking Basics

Azure provides a scalable and secure networking environment through its **Virtual Network (VNet)** service, which is the core equivalent to AWS VPC. It creates a private, isolated space in the Azure cloud for your resources like VMs, App Services, or Kubernetes clusters. Below, I'll explain the key components (virtual network, gateways, subnets, etc.) with similarities and differences to AWS, structured similarly for easy comparison.

#### Virtual Network (VNet)

- **What it is**: The foundational isolated network in Azure, spanning a region and allowing resources to communicate privately. You define its address space with CIDR blocks (e.g., 10.0.0.0/16).
- **Key features**:
  - Default outbound internet access for resources (unlike AWS, where it's opt-in).
  - Supports IPv4 and IPv6; isolated by default.
  - No charge for the VNet itself—pay for attached resources like gateways.
- **Similar to AWS VPC**: Both are private clouds for resource isolation, scaling, and connectivity. Azure VNets auto-span availability zones (AZs); AWS VPCs require explicit AZ setup.
- **Why use it?**: Secure intra-resource communication, internet access, and on-premises links. Every Azure subscription has access, but you create custom VNets for control.
- **Example**: Like AWS VPC, it's your "private estate" in the cloud—you set the boundaries, but Azure handles some defaults like outbound internet.

#### Subnets

- **What they are**: Divisions of a VNet's address space, where resources are deployed. Each subnet is scoped to the VNet and can span all AZs in a region.
- **Types**:
  - **Public subnet**: Resources can have public IPs for inbound/outbound internet (via Azure Load Balancer or public endpoints).
  - **Private subnet**: No direct public access; ideal for databases or internal apps.
- **Key features**:
  - CIDR-defined (e.g., 10.0.1.0/24).
  - Multiple per VNet for segmentation; traffic between them can be filtered.
- **Similar to AWS subnets**: Both segment networks for security and organization. Azure's auto-span AZs simplifies HA; AWS ties subnets to specific AZs.
- **Why use them?**: Isolates workloads—e.g., frontends in public subnets, backends in private.
- **Example**: Subnets are "districts" in your VNet city: public ones with street access (internet), private ones behind walls.

#### Gateways

Gateways in Azure handle external connectivity, but with some defaults differing from AWS.

- **Internet Gateway equivalent**:
  - **What it is**: No direct IGW; outbound internet is enabled by default for VNet resources. Inbound requires a public IP or Load Balancer.
  - **How it works**: Traffic routes via Azure's system routes (0.0.0.0/0 to internet). Use public IPs for bidirectional access.
  - **Similar to AWS IGW**: Both enable public internet, but Azure is more "always-on" outbound; AWS requires explicit attachment and routes.
  - **Why use it?**: Simple public exposure for web apps. Free for basic routing.

- **NAT Gateway**:
  - **What it is**: A managed service in a public subnet for outbound-only internet from private subnets (e.g., VM updates).
  - **How it works**: Shares an Elastic IP for translation; highly available across AZs.
  - **Similar to AWS NAT Gateway**: Both provide secure outbound without inbound exposure. Azure's is more integrated and scalable by default.
  - **Why use it?**: Protects private resources while allowing one-way access. Costs ~$0.045/hour + data.

- **Other gateways**:
  - **VPN Gateway**: For site-to-site or point-to-site VPNs to on-premises (like AWS VGW).
  - **ExpressRoute Gateway**: Private, high-bandwidth links to on-premises (like AWS Direct Connect).

#### Other Related Components ("Etc.")

- **Route Tables**: Control subnet traffic flow (e.g., to internet or peered VNets). System defaults exist; custom ones override for specific routes. Similar to AWS route tables, but Azure propagates BGP routes dynamically from on-premises.
- **Network Security Groups (NSGs)**: Stateful firewalls for subnets or resources, with rules by IP/port/protocol. Like a combo of AWS Security Groups (instance-level, stateful) and NACLs (subnet-level, but Azure's are stateful). Use Application Security Groups for logical tagging.
- **VNet Peering**: Links VNets (same/different regions/accounts) for private traffic, like AWS VPC peering.
- **Service Endpoints/Private Link**: Secure private access to Azure services (e.g., Storage) without internet, akin to AWS VPC Endpoints.
- **Network Virtual Appliances**: VM-based firewalls or routers in the VNet, similar to AWS Network Firewall.

#### How It All Fits Together

1. Create a VNet with CIDR.
2. Add subnets (public/private) spanning AZs.
3. Resources get default outbound internet; add public IPs/Load Balancers for inbound.
4. Use NAT Gateway for private outbound.
5. Apply route tables and NSGs for traffic control.
6. Peer VNets or add gateways for hybrid setups.

Azure's model emphasizes defaults (e.g., outbound internet) for faster setup, while AWS offers more granular opt-ins. Both prioritize security and resilience.

For hands-on, try the Azure portal's VNet wizard.

[Azure Virtual Network Overview](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview)
