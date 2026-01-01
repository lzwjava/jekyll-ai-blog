---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Campus Network Subnet Planning Guide
translated: false
type: note
---

Question: 1. In subnet planning, what is essential for a medium-sized campus network?  
A) Using only public IP addresses  
B) Proper IP address subnetting and allocation  
C) Assigning the same subnet to all departments  
D) Avoiding VLANs entirely  

2. (The provided answer is B)

Answer: 

### Question 1
The correct answer is **B) Proper IP address subnetting and allocation**.

In a medium-sized campus network, effective subnet planning is critical for efficient use of IP address space, improved network performance, enhanced security, and easier management. Proper subnetting involves dividing a larger network into smaller, logical subnetworks (subnets) based on organizational needs (e.g., by department, building, or function). This allows:

- Better traffic segmentation and reduced broadcast domains.
- Scalable growth and efficient IP utilization (especially with private IPv4 addresses via RFC 1918).
- Integration with VLANs for Layer 2 separation and Layer 3 routing.
- Application of access controls and QoS policies.

**Why the other options are incorrect:**
- **A) Using only public IP addresses**: Public IPs are limited and expensive; campus networks typically use private IP addresses with NAT for internet access.
- **C) Assigning the same subnet to all departments**: This creates a single large broadcast domain, leading to congestion, security risks, and poor manageability.
- **D) Avoiding VLANs entirely**: VLANs are commonly used with subnetting to provide logical separation without additional physical infrastructure.

### Question 2
The provided answer **B** is correct, as explained above.

References:  
- [Cisco Campus Network Design Basics](https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/Campus/campover.html)  
- [RFC 1918 - Address Allocation for Private Internets](https://tools.ietf.org/html/rfc1918)