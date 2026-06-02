---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Subnet Mask and Subnetting Explained
translated: false
type: note
---

Question: Transcribe the video and organize it a bit: https://www.youtube.com/watch?v=s_Ntt6eTn94

Answer:

### Video Details
- **Title**: Subnet Mask - Explained
- **Channel**: PowerCert Animated Videos
- **Upload Date**: September 30, 2021
- **Description**: A subnet mask is a number that resembles an IP address. It reveals how many bits in the IP address are used for the network by masking the network portion of the IP address. This video also does a short lesson on subnetting. Subnetting is breaking down a large network into smaller networks or subnets.

### Organized Transcript

**Introduction to IP Addresses**
An IP address is an identifier for a computer or device on a network. Every device needs an IP address for communication. Specifically, this refers to an IPv4 address, which is a 32-bit numeric address written as four numbers separated by periods (e.g., 192.168.1.0). Each group is called an octet, with values ranging from 0 to 255.

An IP address has two parts:
- **Network address (Network ID)**: Assigned to the network itself, unique per network.
- **Host address (Host ID)**: Assigned to devices (computers, servers, etc.) within the network.

**What is a Subnet Mask?**
A subnet mask resembles an IP address and indicates how many bits in the IP address are used for the network portion by "masking" it. Computers understand IP addresses and subnet masks in binary (1s and 0s), not decimal.

**Converting to Binary**
- Use an 8-bit octet chart: Positions from right to left represent 1, 2, 4, 8, 16, 32, 64, 128.
- Set bits to 1 for values that add up to the decimal number; others to 0.
- Example: 192 = 128 + 64 → Binary: 11000000
- 255 = All bits 1 → Binary: 11111111
- 0 = All bits 0 → Binary: 00000000

**How Subnet Mask Works**
Align IP address and subnet mask in binary.
- Where subnet mask has 1s: This is the network portion.
- Where subnet mask has 0s: This is the host portion.

**Examples**
1. Subnet mask 255.255.255.0 → First 3 octets network, last octet hosts.
2. Subnet mask 255.255.0.0 → First 2 octets network, last 2 octets hosts.
3. Subnet mask 255.0.0.0 → First octet network, last 3 octets hosts.
4. Subnet mask with partial octet (e.g., 255.255.224.0) → First 2 octets + 3 bits of third octet for network.

**Why Separate Network and Host Portions? (Subnetting)**
For manageability: Large networks cause excessive broadcast traffic (devices send broadcasts to find each other, reaching everyone). This slows the network.

**Solution: Subnetting**
Break large networks into smaller subnets using routers.
- Broadcasts do not cross routers; they stay within the subnet.
- Reduces traffic, improves performance, and eases troubleshooting.
- Example: One large network → Multiple smaller subnets connected by routers. Communication between subnets goes through the router (default gateway).

**Additional Note**
The video promotes a computer networking audiobook available on Audible.

References:
- [YouTube Video](https://www.youtube.com/watch?v=s_Ntt6eTn94)
