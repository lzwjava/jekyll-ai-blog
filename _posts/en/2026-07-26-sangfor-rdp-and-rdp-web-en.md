---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sangfor RDP and RDP Web
translated: false
type: note
---

**Question: What does “RDP / RDP Web” mean in Sangfor (深信服) 运维安全管理系统 connection?**

**Answer:**

In a Sangfor 运维安全管理系统 (Sangfor OSM / 运维安全审计), **RDP** and **RDP Web** refer to ways of connecting to a Windows server through Remote Desktop Protocol.

### 1. RDP

**RDP = Remote Desktop Protocol**

It is Microsoft's native remote desktop protocol.

Typical flow:

```
Your PC
  |
  | RDP client (mstsc.exe)
  |
  | TCP 3389
  |
Windows Server
```

Example:

```
mstsc.exe
→ server IP
→ username/password
→ Windows desktop
```

You get a full Windows GUI session.

---

### 2. RDP Web

**RDP Web = browser-based RDP connection**

Instead of installing Microsoft's Remote Desktop client:

```
Browser
   |
HTTPS
   |
Sangfor Gateway
   |
RDP protocol
   |
Windows Server
```

You open:

```
https://sangfor-management-system/
```

Login → select server → click "RDP Web"

The Sangfor system launches a web terminal (usually HTML5-based) and proxies the RDP session.

Advantages:

* No need to install mstsc
* Works on Linux/macOS browsers
* Easier auditing
* Sangfor can record the session

---

### 3. Why Sangfor has this option

A normal RDP connection:

```
Engineer
   |
   | RDP
   |
Server
```

has problems:

* No centralized control
* Hard to audit
* Password sharing risk
* Cannot easily record operations

Sangfor adds a bastion host:

```
Engineer
        |
        |
        v
+----------------+
| Sangfor OSM    |
| Bastion Host   |
|                |
| Audit          |
| Permission     |
| Recording      |
+----------------+
        |
        |
        v
 Windows Servers
```

The Sangfor system can:

* authenticate users
* check permission
* hide real server passwords
* record screen operations
* log commands
* provide approval workflow

---

### 4. Difference

| Feature            | RDP           | RDP Web                      |
| ------------------ | ------------- | ---------------------------- |
| Client             | Windows mstsc | Browser                      |
| Protocol           | RDP directly  | RDP tunneled through Sangfor |
| Install software   | Yes           | No                           |
| Audit              | Depends       | Built-in                     |
| Session recording  | Limited       | Usually supported            |
| Works on Mac/Linux | Harder        | Easy                         |

---

### 5. In an enterprise environment

Usually the architecture is:

```
Employee laptop
       |
       |
 HTTPS 443
       |
Sangfor 运维安全管理系统
       |
       |
 RDP 3389
       |
Windows Server 2012 / 2016 / 2022
```

So if you see:

```
Connection Type:
  RDP
  RDP Web
```

choose:

* **RDP** → if you have Windows Remote Desktop client and need better performance
* **RDP Web** → if you want browser access or the company requires bastion auditing

For banking / large enterprise environments (like HSBC-style environments), **RDP Web through a bastion host is very common** because every admin action must be recorded.
