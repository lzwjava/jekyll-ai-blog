---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 网桥自学习算法
translated: true
type: note
---

问题：network bridge（网桥）的 self-learning algorithm 是如何工作的？

答案：

network bridge 使用 **self-learning algorithm**（也称为 *transparent bridging*）来动态构建和维护 **MAC address table**（forwarding table），无需任何手动配置。

---

### 核心数据结构

bridge 维护一个 **MAC Address Table**：

| MAC Address | Port | Timestamp |
| --- | --- | --- |
| AA:BB:CC:DD:EE:01 | Port 1 | t=10s |
| AA:BB:CC:DD:EE:02 | Port 3 | t=12s |

---

### 分步算法

**步骤 1 — frame 到达某个 port**
bridge 在（比如说）Port 1 上收到一个 frame。

**步骤 2 — 从 Source MAC 学习**
bridge 读取 frame 的 **source MAC address** 并记录：

```
MAC Table: source_MAC → Port 1, timestamp = now
```

如果该条目已存在，则只需刷新 timestamp。

**步骤 3 — 根据 Destination MAC 转发**
bridge 在其表中查找 **destination MAC**：

```
if dest_MAC in table:
    if dest_MAC.port == incoming_port:
        DROP  # same segment, no need to forward
    else:
        FORWARD to dest_MAC.port only  # unicast
else:
    FLOOD to all ports except incoming_port  # unknown dest
```

**步骤 4 — Aging（条目过期）**
每个条目都有一个 TTL（通常为 **300 秒**）。如果在超时时间内没有看到来自该 MAC 的 frame，则删除该条目：

```
if now - timestamp > aging_time:
    remove entry
```

---

### 可视化流程

```
Frame arrives on Port 1
        │
        ▼
[Record src_MAC → Port 1]
        │
        ▼
  Lookup dest_MAC
   /           \
Found         Not Found
  │               │
  ▼               ▼
Forward to    FLOOD to all
dest port     other ports
```

---

### 关键属性

| 属性 | 详情 |
| --- | --- |
| **无需预配置** | 表会根据流量自动构建 |
| **Flooding** | 用于未知目的地（以及广播） |
| **Aging** | 防止设备移动时产生陈旧条目 |
| **环路风险** | 仅靠 self-learning 不能防止环路 → 还需要 STP（Spanning Tree Protocol） |

---

### 示例演练

假设有一个 bridge，带有 Ports 1、2、3，并且表为空：

1. Host A（Port 1）向 Host B（Port 2）发送数据：表学习到 `A→Port1`；B 未知 → 向 Ports 2 和 3 进行 flooding。
2. Host B 回复：表学习到 `B→Port2`；A 现在已知 → 仅转发到 Port 1。
3. 之后所有 A↔B 流量都直接交换，不再 flooding。

这就是为什么 bridge 启动时较慢（大量 flooding），但随着表填充会很快变得高效。

参考：

- [IEEE 802.1D - MAC Bridges Standard](https://www.ieee802.org/1/pages/802.1D.html)
- [Transparent Bridging - Cisco Documentation](https://www.cisco.com/c/en/us/support/docs/lan-switching/spanning-tree-protocol/5234-5.html)
- [How Network Bridges Work - Cloudflare Learning](https://www.cloudflare.com/learning/network-layer/what-is-a-network-bridge/)
