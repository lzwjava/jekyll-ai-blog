---
audio: false
generated: true
image: false
lang: en
layout: post
title: RDP via EasyConnect VPN
translated: false
type: note
---

Question: **If EasyConnect creates a virtual IP address, how do I use that virtual address to jump with Remote Desktop (RDP)?**

Answer:

EasyConnect's "virtual address" is usually **not the address of the target Windows machine**. It is the **VPN client's virtual IP** inside the enterprise network.

The flow is:

```
Your Laptop
    |
    | EasyConnect SSL VPN
    |
Virtual VPN adapter
IP: 10.x.x.x  (assigned to your laptop)
    |
    | routing table
    |
Enterprise network
    |
    | RDP TCP/3389
    |
Windows Server
IP: 192.168.x.x / 10.x.x.x
```

So you normally **do not RDP to the EasyConnect virtual IP**.

Wrong:

```
mstsc.exe
Computer:
10.8.0.15   <-- EasyConnect client IP
```

That is your own VPN address.

---

## Find the real target IP

After EasyConnect connects:

Run:

```cmd
ipconfig
```

Example:

```
Ethernet adapter Sangfor SSL VPN:

   IPv4 Address . . . . . . : 10.100.1.25
```

This is your VPN IP.

Then check routes:

```cmd
route print
```

Example:

```
Network Destination    Gateway
10.20.0.0              10.100.1.1
172.16.0.0             10.100.1.1
```

Meaning:

```
10.20.x.x
172.16.x.x
```

are reachable through VPN.

---

## RDP to the server

If your administrator gives:

```
Windows server:
10.20.30.40
```

then:

Run:

```
mstsc.exe
```

Enter:

```
Computer:
10.20.30.40
```

or:

```
10.20.30.40:3389
```

Login:

```
DOMAIN\username
```

or:

```
username
```

---

## In Sangfor 运维安全管理系统 (堡垒机)

Usually you do not directly connect to the server IP.

The design is:

```
User
 |
EasyConnect VPN
 |
Sangfor OSM
 |
Asset database
 |
RDP proxy
 |
Server
```

The bastion host hides the real IP.

You click:

```
资产
  |
Windows Server
  |
RDP
```

Sangfor internally does:

```
Sangfor server
     |
     | RDP
     |
10.20.30.40:3389
```

---

## If you want direct RDP

You need three things:

### 1. Route exists

Check:

```cmd
tracert 10.20.30.40
```

Expected:

```
10.100.x.x (VPN gateway)
10.20.30.40
```

---

### 2. Port open

```powershell
Test-NetConnection 10.20.30.40 -Port 3389
```

Expected:

```
TcpTestSucceeded : True
```

---

### 3. Permission

Even if network works:

```
TCP 3389 open
```

Windows still needs:

```
Remote Desktop Users
```

permission.

---

So the key idea:

* **EasyConnect virtual IP = your laptop's VPN identity**
* **RDP target IP = the server/asset IP**
* **Sangfor OSM usually proxies RDP; you should not manually jump using EasyConnect IP**

If you run:

```cmd
ipconfig
route print
```

after EasyConnect connects, you can see exactly what network ranges it exposes.
