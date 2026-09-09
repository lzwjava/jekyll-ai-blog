---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 静态路由非最高优先级
translated: true
type: note
---

**问题：** 在路由表中，静态路由的优先级是否最高？

**答案：**

不，静态路由并**不**总是拥有最高优先级。路由优先级由**管理距离 (AD)** 决定——AD 值越低，优先级越高。

以下是典型的 AD 优先级顺序（以 Cisco IOS 为例）：

| 路由类型 | 管理距离 |
| --- | --- |
| **直连接口** | **0** ← 最高优先级 |
| **静态路由** | **1** |
| EIGRP 汇总路由 | 5 |
| 外部 BGP (eBGP) | 20 |
| 内部 EIGRP | 90 |
| OSPF | 110 |
| IS-IS | 115 |
| RIP | 120 |
| 外部 EIGRP | 170 |
| 内部 BGP (iBGP) | 200 |
| 未知 / 不可达 | 255 ← 最低优先级 |

**关键点：**

- **直连路由 (AD = 0)** 拥有最高优先级——它们是与接口直接相连的路由，始终被优先选择。
- **静态路由 (AD = 1)** 排在第二位，优先级非常高但并非最高。
- 动态路由协议（OSPF、RIP、BGP 等）的 AD 值都更高，意味着优先级低于静态路由。
- 如果同一目标网段同时存在静态路由和动态路由，**静态路由胜出**（AD 1 对比 OSPF 的 110+ 等）。

**总结：** 直连路由 > 静态路由 > 动态路由协议。

---

**参考资料：**

- [Cisco - 管理距离](https://www.cisco.com/c/en/us/support/docs/ip/border-gateway-protocol-bgp/15986-admin-distance.html)
- [Cloudflare - 什么是路由表？](https://www.cloudflare.com/learning/network-layer/what-is-a-routing-table/)
