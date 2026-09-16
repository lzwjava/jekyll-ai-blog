---
audio: false
generated: true
image: false
lang: en
layout: post
title: Resource vs Communication Subnet
translated: false
type: note
---

Question: What is the difference between a Resource Subnet and a Communication Subnet?

Answer:

In classical network architecture (particularly from the OSI and early networking theory perspective), a computer network is conceptually divided into two parts:

**Resource Subnet (资源子网)**

- Contains the **end systems** (hosts, servers, workstations, terminals)
- Responsible for **data processing, storage, and providing services** to users
- Focuses on *what* the network does — sharing files, running applications, providing computing power
- Examples: user computers, database servers, application servers

**Communication Subnet (通信子网)**

- Contains the **network infrastructure** (routers, switches, transmission links, modems)
- Responsible for **data transmission between nodes** — moving packets from source to destination
- Focuses on *how* data gets delivered — routing, switching, error control, flow control
- Examples: routers, switches, fiber/copper links, ISP backbone networks

**Key Comparison**

| Aspect | Resource Subnet | Communication Subnet |
| --- | --- | --- |
| Role | Data processing & services | Data transmission |
| Devices | Hosts, servers, terminals | Routers, switches, links |
| OSI Layers | Layers 4–7 (Transport to Application) | Layers 1–3 (Physical to Network) |
| User-facing? | Yes | No (transparent to users) |
| Analogy | Cities (origin/destination) | Roads & highways (the path) |

**In short:** The communication subnet is the "highway system," and the resource subnet is the "cities" connected by it. Together they form a complete network system.

References:

- [Computer Networks – Tanenbaum, 5th Ed. (Overview)](https://www.pearson.com/en-us/subject-catalog/p/computer-networks/P200000003073)
- [Subnet Architecture – GeeksforGeeks](https://www.geeksforgeeks.org/introduction-of-subnetting/)
