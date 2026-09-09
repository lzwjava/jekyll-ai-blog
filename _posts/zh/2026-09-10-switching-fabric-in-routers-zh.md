---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 路由器中的交换结构
translated: true
type: note
---

**交换结构** 英文对应 **"Switching Fabric"**。它是路由器内部的核心组件，负责将数据包从输入端口传输到正确的输出端口。

可以将其理解为路由器内部的"高速公路系统"。以下是其功能及主要类型：

---

**作用：**

- 连接所有输入端口与输出端口
- 以极快速度在内部将数据包从到达位置传送至目标位置

---

**三种主要类型：**

| 类型 | 说明 | 速度 |
| ------ | ------ | ------ |
| **基于内存交换** | 数据包复制到CPU内存后再转发，如早期路由器 | 最慢 |
| **基于总线交换** | 数据包通过共享内部总线传输，高负载时存在瓶颈 | 中等 |
| **基于交叉开关/互联网络交换** | 交叉点网格支持多路并发传输，用于高端路由器 | 最快 |

---

**重要性：**

交换结构的吞吐量直接决定路由器的**整体转发能力**。现代高性能路由器（如思科或瞻博网络的产品）采用交叉开关或多级互联结构，可实现太比特级吞吐量。

---

参考来源：

- [计算机网络：自顶向下方法——路由器架构（Kurose & Ross）](https://gaia.cs.umass.edu/kurose_ross/index.php)
- [交换结构 – 维基百科](https://en.wikipedia.org/wiki/Switching_fabric)
- [思科：路由器工作原理](https://www.cisco.com/c/en/us/products/routers/what-is-a-router.html)
