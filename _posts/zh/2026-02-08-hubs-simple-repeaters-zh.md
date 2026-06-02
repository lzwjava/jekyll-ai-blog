---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-haiku
title: 网络中的集线器：简单的中继器
translated: true
type: note
---

Hub 是一个简单的网络设备，运行在 OSI model 的 **Physical Layer (Layer 1)**。以下是它的工作原理：

## Basic Operation

Hub 本质上是一个 **multi-port repeater**。当连接到其中一个端口的设备发送数据（电信号）时，Hub 会接收这些信号并同时将其转发到所有其他端口。从这个意义上说，它是完全“无智能”的——它不理解 IP addresses、MAC addresses 或任何更高层的信息。它只是放大并转发这些电信号。

## Key Characteristics

**No intelligence**：Hub 不会对数据的去向做出任何决策。如果一台计算机发送数据，它会到达 Hub 上的每一个其他端口。

**Shared bandwidth**：连接到 Hub 的所有设备都共享相同的带宽。如果一个具有 4 个端口的 Hub 容量为 100 Mbps，每个设备并不能获得 100 Mbps——它们共同分享该带宽，随着更多设备进行通信，可用带宽会随之减少。

**Collision domain**：Hub 上的所有端口都处于同一个 collision domain 中。如果两个设备同时传输，它们的信号就会发生冲突（collide）。Hub 无法阻止这种情况，因为它没有管理流量的智能。

## Why Switches are Better

这就是为什么 **switches**（运行在 Layer 2，即 Data Link Layer）取代了 Hub。Switches 能够识别 MAC addresses，并可以将 frames 转发到特定端口，而不是淹没所有端口。这消除了 collisions，为每个端口提供全额带宽，并创建了独立的 collision domains。

在现代网络中，Hub 基本上已经过时了——你再也看不到它们被使用了。在几乎所有实际应用中，它们都已被 switches 取代。
