---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 了解网状路由器回传与带宽
translated: true
type: note
---

问题：Mesh router 必须使用有线连接吗？如果多个 AP 占用了所有的家庭带宽，那么它们天线的作用是什么？我该如何理解 Mesh router？

回答：

你询问的本质是 Mesh Wi-Fi 系统的工作原理，以及有线连接与无线连接的角色。让我们详细分析一下：

1. **Wired backhaul 与 Wireless backhaul**

   * 许多 Mesh router 同时支持 **Wired backhaul（有线回程）** 和 **Wireless backhaul（无线回程）**。
   * **Wired backhaul** 意味着节点之间通过 Ethernet cable 连接。这能提供 **最高的速度和可靠性**，因为节点间的传输流量不会与 Wi-Fi 客户端（Client）竞争。
   * **Wireless backhaul** 意味着节点通过 Wi-Fi 进行通信。这很方便，因为不需要布线，但可用带宽是 **共享的**：节点之间的每一次跳转（Hop）都会降低总吞吐量（Throughput）。因此，如果多个 AP 同时处于活动状态，它们会消耗大量家庭带宽，从而导致性能下降。

2. **天线的作用**

   * Mesh router 上的天线有两个用途：

     1. 与 **Client devices**（手机、电脑、智能家居设备）进行通信。
     2. 与 **其他 Mesh 节点** 进行通信（如果使用 Wireless backhaul）。
   * 即使你使用了 Wired backhaul，天线仍然需要为 Client 提供服务。在 Wireless backhaul 模式下，同样的天线要兼顾节点间连接和设备连接，这就是为什么带宽会被更快“吃掉”的原因。

3. **Mesh 网络中的带宽共享**

   * 在 Wireless backhaul 设置中，带宽在 **每一次跳转时都会被拆分**。例如，如果你的主路由从 ISP 获取 500 Mbps，那么距离它一次跳转的节点可能只能为 Client 提供 250–300 Mbps，因为它必须中继流量。
   * 如果多个节点都在积极为 Client 提供服务，总可用带宽将被分配给所有设备和跳转链路。

4. **实际理解**

   * **Wired Mesh：** 通过 Ethernet 连接节点。天线仅为 Client devices 服务。拥有最高速度和最小干扰。
   * **Wireless Mesh：** 不需要 Ethernet 线下。天线同时为 Client 和节点服务。使用方便，但吞吐量会随距离和跳转次数增加而减少。
   * 如果你的目标是在多个 AP 之间保持高带宽，**强烈建议使用 Wired backhaul**。

简而言之：Mesh router **并非严格要求有线连接**，但使用有线连接可以让天线专注于 Client 覆盖而不是节点间的通信，从而防止带宽损耗。在 Wireless backhaul 场景下，多个 AP 消耗所有带宽是非常典型的现象。

你可以把它想象成一个 **水管系统**：如果所有的水都必须流经一根水管（无线），你走得越远，打开的水龙头（AP）越多，每个水龙头的流量就越小。增加 Ethernet cable 就好比给每个水龙头都装了独立的水管——到处都是满流。
