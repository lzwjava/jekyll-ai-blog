---
audio: false
generated: true
image: false
lang: en
layout: post
title: TCP/IP Model Layers
translated: false
type: note
---

Question: What are the four layers of the TCP/IP model?

Answer:

The TCP/IP model is organized into four layers, each responsible for a distinct part of network communication:

**1. Network Access Layer (Link Layer)**
Handles the physical transmission of data between devices on the same network. It deals with hardware addressing (MAC addresses), network drivers, and the physical medium (Ethernet, Wi-Fi, etc.).

**2. Internet Layer**
Responsible for logical addressing and routing packets across different networks. The key protocol here is **IP (Internet Protocol)**, along with ICMP and ARP. It determines the best path for data to travel from source to destination.

**3. Transport Layer**
Manages end-to-end communication between hosts. The two primary protocols are:

- **TCP** (Transmission Control Protocol) — reliable, connection-oriented
- **UDP** (User Datagram Protocol) — fast, connectionless

**4. Application Layer**
The topmost layer where user-facing protocols operate. It includes **HTTP, FTP, DNS, SMTP, SSH**, and others. Applications interact directly with this layer to send and receive data.

Here's a quick visual summary:

| Layer | Name | Key Protocols |
| ------- | ------ | --------------- |
| 4 | Application | HTTP, DNS, FTP, SMTP |
| 3 | Transport | TCP, UDP |
| 2 | Internet | IP, ICMP, ARP |
| 1 | Network Access | Ethernet, Wi-Fi, MAC |

References:

- [TCP/IP Model – GeeksforGeeks](https://www.geeksforgeeks.org/tcp-ip-model/)
- [RFC 1122 – Requirements for Internet Hosts](https://datatracker.ietf.org/doc/html/rfc1122)
- [TCP/IP Guide – No Starch Press](http://www.tcpipguide.com/free/t_TCPIPArchitectureandtheTCPIPModel.htm)
