---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 显示OSPF邻居命令解释
translated: true
type: note
---

问题：在华为路由器中，哪个命令用于显示当前 OSPF 邻居表？  
A) display ospf peer  
B) display ospf neighbor  
C) display ospf interface  
D) display ospf routing-table

**答案：** 

正确答案是 **A) display ospf peer**。

在华为路由器和交换机中，`display ospf peer` 命令用于显示 OSPF 邻居表，其中包含邻居路由器 ID、状态（例如，Full）、接口、优先级和死亡计时器等详细信息。

- `display ospf neighbor` 在华为设备中不是一个有效命令。
- `display ospf interface` 显示有关启用 OSPF 的接口信息，而不是邻居表。
- `display ospf routing-table` (或 `display ospf routing`) 显示 OSPF 路由表，而不是邻居。

**参考资料：**  

- [华为支持：display ospf peer (各种型号)](https://support.huawei.com/enterprise/en/doc/EDOC1100096312/9dc18ce0/display-ospf-peer)  
- [华为支持：排查 OSPF 邻居问题](https://info.support.huawei.com/network/ptmngsys/Web/tsrev_ar/en/content/ar/17_edesk_ospf_peer_status_abnormal/edesk_ospf_peer_status_abnormal_edesk001.html)  
- [华为命令参考示例](https://support.huawei.com/enterprise/en/doc/EDOC1100197525/9dc18ce0/display-ospf-peer)