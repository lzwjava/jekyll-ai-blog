---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分布式队列双总线协议
translated: true
type: note
---

**问题：** DQDB 中的分布式排队访问协议是什么？

**答案：**

DQDB —— **分布式队列双总线** —— 是 IEEE 802.6 城域网标准。其核心创新在于 **分布式排队访问协议**，该协议协调所有节点如何在没有中央控制器的情况下共享两条总线。其工作原理如下：

---

### 1. 物理架构

DQDB 使用两条单向总线，以相反方向传输数据，带宽通过时隙分配，支持数据、视频和语音。每条总线末端的“总线首节点”（HOB）生成时分复用时隙，每个时隙被标记为忙碌或空闲。

---

### 2. 分布式队列机制

关键思想：**节点在没有中央仲裁器的情况下形成虚拟全局队列**。每个节点使用两个计数器：

**请求计数器（RC）**
每个站点监视两条总线上的忙碌比特和请求比特——每收到一个请求比特就递增计数器，每经过一个空闲时隙就递减计数器。

**倒计时计数器（CD）**
当站点希望在总线 A 上发送时，总线 A 请求计数器中的当前计数会被转移到总线 A 的倒计时计数器（重置请求计数器），并在总线 B 上第一个可用时隙中插入一个保留请求。倒计时计数器随站点在总线 A 上经过的每个空闲时隙递减。当它达到零时，站点即可抢占总线 A 上的下一个空闲时隙用于发送数据段。

所有站点同时为每个传输方向执行这一计数过程——这正是该系统被称为“分布式队列双总线”的原因。

---

### 3. 优先级等级

每个节点为不同优先级维护三组（或四组）REQUEST 和 COUNTDOWN 计数器。高优先级的请求比特会影响计数器的行为，从而实现基于优先级的传输排序。

---

### 4. 公平性问题与带宽均衡

在重负载下，DQDB 以高度不对称的方式在节点间分配流量——最先开始传输的站点获得最大比例的可用带宽，服务质量取决于站点间的传播延迟。

为弥补这一不公平性，IEEE 802.6 标准推荐了一种带宽均衡（BWB）机制。

---

### 总结表格

| 组件 | 作用 |
| --- | --- |
| 总线 A / 总线 B | 两条方向相反的数据通道 |
| 总线首节点（HOB） | 生成空闲时隙 |
| 请求计数器（REQUEST Counter） | 记录队列中排在前面有多少节点 |
| 倒计时计数器（COUNTDOWN Counter） | 倒计时直到该节点轮到发送 |
| 请求比特（位于对向总线） | 用于表示发送意图 |
| 带宽均衡（Bandwidth Balancing） | 纠正重负载下的不公平性 |

---

**参考文献：**

- [Distributed-queue dual-bus — Wikipedia](https://en.wikipedia.org/wiki/Distributed-queue_dual-bus)
- [IEEE 802.6 (DQDB) — GeeksforGeeks](https://www.geeksforgeeks.org/computer-networks/ieee-802-6-dqdb/)
- [Distributed Queue Dual Bus (DQDB) — Academia.edu](https://www.academia.edu/72986514/Distributed_Queue_Dual_Bus_DQDB_)
- [DQDB Networks with and without Bandwidth Balancing — ResearchGate](https://www.researchgate.net/publication/3158058_DQDB_Networks_with_and_without_Bandwidth_Balancing)
