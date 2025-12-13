---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Display OSPF Peer Command Explanation
translated: false
type: note
---

Question: In Huawei routers, which command is used to display the current OSPF neighbor table?  
A) display ospf peer  
B) display ospf neighbor  
C) display ospf interface  
D) display ospf routing-table

**Answer:** 

The correct answer is **A) display ospf peer**.

In Huawei routers and switches, the command `display ospf peer` is used to display the OSPF neighbor table, showing details such as neighbor router IDs, states (e.g., Full), interfaces, priorities, and dead timers.

- `display ospf neighbor` is not a valid command in Huawei devices.
- `display ospf interface` shows information about OSPF-enabled interfaces, not the neighbor table.
- `display ospf routing-table` (or `display ospf routing`) displays the OSPF routing table, not neighbors.

**References:**  

- [Huawei Support: display ospf peer (various models)](https://support.huawei.com/enterprise/en/doc/EDOC1100096312/9dc18ce0/display-ospf-peer)  
- [Huawei Support: Troubleshooting OSPF neighbor issues](https://info.support.huawei.com/network/ptmngsys/Web/tsrev_ar/en/content/ar/17_edesk_ospf_peer_status_abnormal/edesk_ospf_peer_status_abnormal_edesk001.html)  
- [Huawei Command Reference Examples](https://support.huawei.com/enterprise/en/doc/EDOC1100197525/9dc18ce0/display-ospf-peer)