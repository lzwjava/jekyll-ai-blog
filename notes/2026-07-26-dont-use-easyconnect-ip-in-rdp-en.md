---
audio: false
generated: true
image: false
lang: en
layout: post
title: Don't Use EasyConnect IP in RDP
translated: false
type: note
---

Question: **How to set EasyConnect VPN address in Windows Remote Desktop Connection (mstsc)?**

Answer:

You **do not put the EasyConnect virtual IP into Remote Desktop Connection**.

In `mstsc.exe`:

```
Computer:
<target Windows server IP or hostname>
```

Example:

```
Computer: 10.20.30.40
```

or:

```
Computer: server01.company.local
```

Then click:

```
Connect
```

---

The EasyConnect virtual IP is only used by the VPN adapter automatically. You do not configure it in RDP.

The flow is:

```
EasyConnect connected
        |
        v
Windows routing table knows:
10.20.0.0/16 -> VPN tunnel
        |
        v
mstsc.exe
Computer: 10.20.30.40
        |
        v
RDP through VPN
```

If you only have the EasyConnect virtual IP, for example:

```
10.100.1.25
```

that is your VPN client address. It cannot be used for RDP unless the machine at `10.100.1.25` itself is an RDP server.

To test:

```powershell
ipconfig
```

Find:

```
Sangfor SSL VPN Adapter
IPv4 Address: 10.x.x.x
```

Ignore that.

Use the **remote asset/server IP** provided by the Sangfor 运维安全管理系统.
