---
audio: false
generated: true
image: false
lang: en
layout: post
title: "MIB Data Types: Static, Dynamic, Control"
translated: false
type: note
---

**Question:** In MIB (Management Information Base), what are the three types of data — static, dynamic, and the third is "control data"?

**Answer:**

You're right. The three types of data stored in a MIB are **Static**, **Dynamic**, and **Control**:

**1. Static Data (静态数据)**
Configuration information that changes rarely or never during normal operation. Examples: device name, interface type, physical address (MAC), system description.

**2. Dynamic Data (动态数据)**
Information that reflects real-time events and current state of the network. It changes frequently as the network operates. Examples: link up/down status, current connection table, ARP cache entries.

**3. Control Data (控制数据)**
Parameters that the management system can **write/set** to actively control or configure a managed device — not just read. Examples: setting an interface to enabled/disabled, modifying a routing table entry, changing a threshold value. This is what allows SNMP to perform **active management** (not just monitoring).

A concise summary:

| Type | Direction | Purpose | Example |
|---|---|---|---|
| Static | Read | Describes device identity/config | Device name, MAC address |
| Dynamic | Read | Reflects current network state | Link status, active sessions |
| Control | Read / **Write** | Allows management system to configure the device | Enable/disable interface, set threshold |

The key distinction of **control data** is that it supports **write operations** — the management system can push changes to the device, enabling active network management rather than passive observation.

---

**References:**
- [What is MIB? – Zenarmor](https://www.zenarmor.com/docs/network-basics/what-is-mibs-management-information-base)
- [MIB (管理信息库) – 百度百科](https://baike.baidu.com/item/mib/4490795)
- [SNMP MIB Overview – Microsoft Learn](https://learn.microsoft.com/zh-cn/windows/win32/snmp/the-snmp-management-information-base-mib-)
