---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 超越 NAT 的防火墙技术详解
translated: true
type: note
---

问题：除了 NAT 以外，三大主要防火墙技术是什么，NAT 在中文中代表什么，它的特定功能是什么，以及防火墙产品中的 NAT 技术如何有助于网络保护？

答案：

根据工作原理，防火墙技术主要分为四类。除了 **Network Address Translation (NAT)** 以外，其他三大主要技术是：

1.  **Packet Filtering Technology (包过滤技术)**
    *   这是最基本的防火墙形式。它检查进入或离开网络的每个 packet，并根据用户定义的规则（如 source/destination IP addresses、ports 和 protocols）接受或拒绝它。它在 network layer (Layer 3) 运行，有时也在 transport layer (Layer 4)。

2.  **Proxy Service Technology (代理服务技术)**
    *   也称为 Application Layer Gateways。这种技术充当内部客户端和外部服务器之间的中介。proxy 接收来自内部用户的请求，进行验证，然后代表用户转发到外部服务器。这完全隐藏了内部网络结构，并允许对 application-layer 数据进行深度检查。

3.  **Stateful Inspection Technology (状态检测技术)**
    *   它结合了 packet filtering 的速度和 proxy services 的安全性。它不是孤立地检查 packets，而是跟踪活动连接的状态（如 TCP handshakes）。它基于流量上下文做出决策，确保传入的 packets 是合法已建立会话的一部分。

### NAT 详情

*   **中文含义**：NAT 的中文术语是 **网络地址转换** (Wǎngluò Dìzhǐ Zhuǎnhuàn)。有时它被称为 Network Address Translation Protocol，但严格来说，它是一种方法/功能而非独立的 protocol。
*   **特定功能**：NAT 的主要功能是将 **internal private IP addresses** 映射到 **legal public IP addresses**。这允许本地网络上的多个设备（使用不可路由的 private IPs 如 192.168.x.x）在访问 Internet 时共享单个 public IP address。它在 packets 通过 router 或 firewall 时修改 IP header。

### 防火墙中 NAT 的保护作用

虽然 NAT 最初设计用于节省 IPv4 addresses，但它在网络安全方面提供了显著的附带益处：

*   **隐藏内部拓扑**：NAT 将内部网络的寻址方案对外部世界隐藏。外部网络只能看到 firewall 的 public IP address，而看不到内部单个计算机的具体 private IPs。
*   **防止直接攻击**：由于外部攻击者无法看到或直接路由流量到特定的 internal private IP addresses，他们无法轻易对内部网络中的特定计算机发起直接攻击。攻击者首先需要 compromise firewall 或利用特定的 port mapping rule 才能到达内部 host。这创建了一种通常描述为“security through obscurity”的自然屏障，不过它在与 stateful inspection 结合时最有效。

参考文献：
