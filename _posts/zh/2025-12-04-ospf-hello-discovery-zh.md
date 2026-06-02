---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 通过Hello进行OSPF邻居发现
translated: true
type: note
---

问题：在OSPF中，哪种数据包类型用于发现邻居？

答案：
**A) Hello**

Hello数据包在OSPF中用于邻居发现和维护邻居邻接关系。它会定期在启用了OSPF的接口上发送（通常在广播网络上每10秒发送一次），以发现相邻路由器、验证双向通信，并选举指定路由器（DR）和备份指定路由器（BDR）。一旦邻居被发现并使用其他数据包类型（例如，用于Database Description的DBD、用于Link State Request的LSR、用于Link State Update的LSU）进入更深层状态。

- DBD、LSR和LSU在邻接关系形成和LSDB同步过程中稍后使用，而不是用于初始发现。
