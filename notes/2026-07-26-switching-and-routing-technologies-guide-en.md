---
audio: false
generated: true
image: false
lang: en
layout: post
title: Switching and Routing Technologies Guide
translated: false
type: note
---

## Question:

Intro to Guangdong Self-Study Exam course **13833 Switching and Routing Technologies (交换与路由技术)**

## Answer:

**13833 交换与路由技术** is a professional core course in the Guangdong Higher Education Self-Study Examination (广东高等教育自学考试), mainly for **计算机应用技术 (Computer Application Technology)**. It is a practical networking course focused on configuring and managing enterprise networks. ([Guangdong Exam Authority][1])

It is basically a **CCNA-level networking course**, but adapted for China's self-study exam system. The official syllabus emphasizes:

* network fundamentals
* switch configuration
* router configuration
* security configuration
* IPv6
* Huawei network simulator practice

([Guangdong Exam Authority][1])

---

# 1. Where it sits in the CS knowledge map

Think of the stack:

```
Application
   |
HTTP / DNS / SSH
   |
TCP / UDP
   |
IP routing  <----- 13833 starts here
   |
Ethernet switching <----- 13833 focuses here
   |
Physical layer
```

Compared with another self-study course:

| Course                                   | Focus                                 |
| ---------------------------------------- | ------------------------------------- |
| 02141 Computer Networks                  | theory: OSI, TCP/IP, protocols        |
| 13833 Switching and Routing Technologies | practical: configure switches/routers |

([LZW Java][2])

For an engineer, 13833 is closer to:

```
Computer Networks
        +
CCNA
        +
Huawei H3C enterprise networking practice
```

---

# 2. Core topics

## Part 1: Basic networking

You need:

### IP address

Example:

```
192.168.1.0/24
```

means:

```
network:
192.168.1.0

hosts:
192.168.1.1 - 192.168.1.254
```

Subnetting:

```
/24
255.255.255.0


/26
255.255.255.192
```

This is frequently tested.

---

# 3. Switching (交换)

A switch works at Layer 2.

Example:

```
PC1
 |
 |
Switch
 |
 |
PC2
```

The switch learns MAC addresses:

```
MAC table:

AA:BB:CC -> port 1
DD:EE:FF -> port 2
```

---

## VLAN

Very important.

Without VLAN:

```
        Switch

PC1 -------- PC2 -------- PC3
```

Everyone is in one broadcast domain.

With VLAN:

```
VLAN10

PC1
 |
Switch


VLAN20

PC2
 |
Switch
```

Logical separation.

Huawei command example:

```
system-view

vlan 10

interface GigabitEthernet 0/0/1

port link-type access

port default vlan 10
```

---

# 4. STP (Spanning Tree Protocol)

Problem:

Network loops:

```
        Switch A
       /        \
      /          \
 Switch B ------ Switch C
```

Ethernet originally has no TTL.

Broadcast storm:

```
packet
 ↓
A → B → C → A → ...
```

STP blocks one path:

```
        Switch A
       /
      /
 Switch B ------ Switch C
        blocked
```

Exam likes:

* root bridge
* port roles
* blocking state

---

# 5. Routing (路由)

Router connects different networks:

```
192.168.1.0

     |
   Router

     |

192.168.2.0
```

Router table:

```
Destination        Next hop

192.168.2.0/24     eth0
```

---

## Static routing

Manual:

```
ip route-static
192.168.2.0 255.255.255.0 10.0.0.2
```

Good for small networks.

---

## Default routing

"Everything else goes here"

```
0.0.0.0/0
        |
     Internet
```

---

## Dynamic routing

The router learns automatically.

### RIP

Old protocol:

```
distance-vector

metric:
hop count
```

Maximum:

```
15 hops
```

---

### OSPF

Important.

Used in enterprise networks.

Concept:

```
Router A
   |
 OSPF
   |
Router B
```

Features:

* link state
* shortest path
* areas

Algorithm:

```
Dijkstra
```

---

# 6. Huawei simulator

The course specifically uses Huawei router/switch simulation. ([Guangdong Exam Authority][1])

Typical tool:

```
eNSP
```

Example lab:

```
PC1

 |
Switch

 |
Router

 |
Switch

 |
PC2
```

Configure:

1. VLAN
2. trunk
3. router interface
4. static route
5. OSPF

---

# 7. Difficulty for you

Given your background:

* Java backend
* Linux
* cloud
* Kubernetes
* AWS/GCP
* AI infrastructure

This course should be **easy-medium**.

The difficult part is not programming.

It is memorizing networking details:

```
MAC
ARP
VLAN
STP
IP subnet
routing table
OSPF
ACL
NAT
IPv6
```

Your advantage:

You already understand distributed systems.

Example:

Kubernetes:

```
Pod
 |
Service
 |
Network
```

Underneath:

```
IP routing
iptables
CNI
bridge
overlay network
```

This course gives the lower layer.

---

# 8. Suggested study path

I would do:

```
Week 1
TCP/IP basics
subnetting


Week 2
Ethernet
MAC
ARP
VLAN


Week 3
STP
trunk
link aggregation


Week 4
Static routing
RIP
OSPF


Week 5
ACL
NAT
IPv6


Week 6
Huawei eNSP labs
past papers
```

---

# 9. Relation to AI infrastructure

Actually this subject connects to modern AI clusters.

Example:

GPU cluster:

```
GPU Server
    |
Ethernet / InfiniBand
    |
Switch
    |
Router
    |
Storage
```

Large training clusters need:

* topology design
* bandwidth
* congestion control
* routing

The same concepts appear in:

* NVIDIA networking
* RDMA
* RoCE
* AI datacenter design

So this is not an outdated course.

It is the foundation layer below AI infrastructure.

References:

* 广东省高等教育自学考试课程设置文件（13833 交换与路由技术） ([Guangdong Exam Authority][1])
* 广东自考教材表（13833 使用教材：网络设备配置与管理项目教程） ([edu-edu.com][3])
* 广东省自学考试管理系统 ([eeagd.edu.cn][4])

[1]: https://eea.gd.gov.cn/attachment/0/532/532589/4262692.pdf?utm_source=chatgpt.com "附件1
广东省高等教育自学考试本科（专升本）
专业调整列表
序号  | 专业代码  | 专业名称
-"
[2]: https://lzwjava.github.io/computer-networking-comparison-en?utm_source=chatgpt.com "Comparing Computer Networking Course Differences"
[3]: https://www.edu-edu.com/zikao/guangdong/jcdg/65918.html?utm_source=chatgpt.com "广东省2026年高等教育自学考试开考课程使用教材表"
[4]: https://www.eeagd.edu.cn/selfec/?utm_source=chatgpt.com "广东省自学考试管理系统"
