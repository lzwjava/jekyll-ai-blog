---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 子网掩码与子网划分详解
translated: true
type: note
---

Question: Transcribe the video and organize it a bit: https://www.youtube.com/watch?v=s_Ntt6eTn94

Answer: 

### Video Details

- **Title**: Subnet Mask - Explained
- **Channel**: PowerCert Animated Videos
- **Upload Date**: September 30, 2021
- **Description**: Subnet mask 是一个类似于 IP address 的数字。它通过屏蔽 IP address 的网络部分，揭示了 IP address 中有多少位用于网络。该视频还简要介绍了 Subnetting。Subnetting 是将一个大型网络分解为更小的网络或 Subnet 的过程。

### Organized Transcript

**Introduction to IP Addresses**  
IP address 是网络上计算机或设备的标识符。每台设备都需要一个 IP address 才能进行通信。具体来说，这里指的是 IPv4 address，它是一个 32-bit 的数字地址，写作由句点分隔的四个数字（例如：192.168.1.0）。每个组被称为一​​个 Octet，取值范围从 0 到 255。

一个 IP address 由两部分组成：  
- **Network address (Network ID)**：分配给网络本身，每个网络唯一。  
- **Host address (Host ID)**：分配给网络内的设备（计算机、服务器等）。

**What is a Subnet Mask?**  
Subnet mask 类似于 IP address，通过“屏蔽”来指示 IP address 中有多少位用于网络部分。计算机以 Binary（1 和 0）而不是 Decimal 格式理解 IP address 和 Subnet mask。

**Converting to Binary**  
- 使用 8-bit octet 图表：从右到左的位置分别代表 1, 2, 4, 8, 16, 32, 64, 128。  
- 将相加等于该 Decimal 数字的对应位设为 1；其他设为 0。  
- 示例：192 = 128 + 64 → Binary: 11000000  
- 255 = 所有位均为 1 → Binary: 11111111  
- 0 = 所有位均为 0 → Binary: 00000000  

**How Subnet Mask Works**  
将有效 IP address 和 Subnet mask 以 Binary 形式对齐。  
- Subnet mask 为 1 的地方：这是网络部分。  
- Subnet mask 为 0 的地方：这是主机部分。  

**Examples**  
1. Subnet mask 255.255.255.0 → 前 3 个 Octet 为网络，最后一个 Octet 为主机。  
2. Subnet mask 255.255.0.0 → 前 2 个 Octet 为网络，最后 2 个 Octet 为主机。  
3. Subnet mask 255.0.0.0 → 第 1 个 Octet 为网络，最后 3 个 Octet 为主机。  
4. 带有部分 Octet 的 Subnet mask（例如：255.255.224.0）→ 前 2 个 Octet + 第 3 个 Octet 的前 3 位用于网络。

**Why Separate Network and Host Portions? (Subnetting)**  
为了便于管理：大型网络会产生过多的 Broadcast traffic（设备发送广播以寻找彼此，会发送给所有人）。这会降低网络速度。

**Solution: Subnetting**  
使用 Router 将大型网络分解为更小的 Subnet。  
- Broadcasts 不会跨越 Router；它们保留在 Subnet 内部。  
- 减少流量，提高性能，并简化 Troubleshooting。  
- 示例：一个大型网络 → 由 Router 连接的多个较小 Subnet。Subnet 之间的通信通过 Router（Default gateway）进行。

**Additional Note**  
该视频推广了在 Audible 上可以获取的电脑联网配套有声书。

References:  
- [YouTube Video](https://www.youtube.com/watch?v=s_Ntt6eTn94)