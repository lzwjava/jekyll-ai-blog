---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 防火墙与NAT差异解释
translated: true
type: note
---

**防火墙有什么用途，为什么它会使用 NAT？**

**防火墙** 和 **NAT** 在很多家用路由器中相互关联，但它们解决的是**不同的问题**。

### 1. 防火墙有什么作用？

防火墙本质上是一个**数据包流转策略引擎**：

```text
Internet
   |
   v
[ Firewall ]
   |
   +---- allow ----> LAN
   |
   +---- drop -----> X
```

对于每个数据包，它可以检查以下内容：

```text
src IP
dst IP
src port
dst port
protocol
connection state
interface
```

然后应用规则：

```text
ALLOW  LAN -> Internet
ALLOW  established Internet -> LAN
DROP   unsolicited Internet -> LAN
```

例如，你的 PC：

```text
192.168.1.100:52341
        |
        | TCP
        v
8.8.8.8:443
```

防火墙可以说：

> 局域网内的机器可以发起 HTTPS 连接。

但如果某个随机的互联网主机尝试：

```text
1.2.3.4:54321 -> 192.168.1.100:22
```

防火墙可以将其丢弃。

所以其根本目的是：

**防火墙 = 控制哪些流量可以跨越网络边界。**

---

### 2. 那为什么还需要 NAT？

NAT = **Network Address Translation（网络地址转换）**。

假设你的局域网（LAN）中有：

```text
PC1  192.168.1.100
PC2  192.168.1.101
PC3  192.168.1.102
```

这些都是私有地址，无法在公共互联网上直接路由。

你的路由器可能有：

```text
WAN: 203.0.113.50
LAN: 192.168.1.1
```

当 PC1 发送：

```text
192.168.1.100:50000
       ->
8.8.8.8:443
```

路由器会将其转换为：

```text
203.0.113.50:40001
       ->
8.8.8.8:443
```

它会维护一张 NAT 表：

```text
192.168.1.100:50000
        |
        v
203.0.113.50:40001
```

当响应返回时：

```text
8.8.8.8:443
       ->
203.0.113.50:40001
```

路由器会查找映射并将其转换回去：

```text
203.0.113.50:40001
       ->
192.168.1.100:50000
```

---

### 3. NAT 并不等同于防火墙

这个区别很重要。

**NAT 的主要目的：**

```text
translate addresses/ports
```

**防火墙的主要目的：**

```text
allow / deny traffic
```

但 NAT 通常会带来额外的安全效果。

假设路由器具有：

```text
WAN IP = 203.0.113.50
LAN IP = 192.168.1.100
```

互联网上的机器不能简单地发送：

```text
Internet
   |
   v
192.168.1.100
```

因为 `192.168.1.100` 是私有地址，无法在全球范围内路由。

而且典型的家用路由器还额外有一条防火墙规则：

```text
WAN -> LAN
unsolicited connection
        |
        v
       DROP
```

所以人们有时会说：

> “NAT 保护了我的网络。”

更准确地说：

**NAT 提供地址转换；有状态防火墙提供实际的流量过滤。**

---

### 4. 为什么家用路由器要把它们组合在一起？

因为它们天然位于同一个边界：

```text
                  Router
             +----------------+
Internet --->| WAN            |
             |                |
             | Firewall       |
             | NAT            |
             | Routing        |
             | DHCP           |
             +-------+--------+
                     |
                     |
                  LAN
              +------+------+
              |             |
             PC1           PC2
```

路由器可以看到**所有进出局域网（LAN）的流量**，因此它是在同一个位置执行以下操作的理想场所：

1. Routing
2. NAT
3. Stateful firewalling
4. DHCP
5. Sometimes DNS forwarding

---

### 5. 有趣的部分：NAT 会创建连接状态

对于 TCP，家用路由器实际上可能会跟踪这样的映射：

```text
LAN:
192.168.1.100:52341

      NAT

WAN:
203.0.113.50:41002

      |
      v

8.8.8.8:443
```

然后返回的数据包会匹配这个状态。

从概念上讲：

```text
outbound:
LAN -> WAN
CREATE NAT STATE

return:
WAN -> LAN
MATCH EXISTING STATE -> ALLOW
```

但是：

```text
Internet -> WAN
NO EXISTING STATE
        |
        v
      DROP
```

这就是为什么你的 PC 可以建立：

```text
PC -> Google
Google -> PC
```

而某个随机的互联网主机通常无法建立：

```text
Random Internet host -> PC
```

除非设置了端口转发或显式防火墙规则。

所以我会使用的思维模型是：

```text
NAT:
"Who is this packet really from?"

Firewall:
"Should this packet be allowed?"

Routing:
"Where should this packet go?"
```

我还可以完整地演示**一个 TCP SYN → SYN/ACK → ACK 的数据包序列如何通过家用路由器**，准确展示路由、NAT 和有状态防火墙分别对每个数据包做了什么。
