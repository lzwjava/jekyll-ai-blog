---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sangfor OSM RDP Troubleshooting
translated: false
type: note
---

Question: **How to connect RDP through Sangfor 运维安全管理系统 (Sangfor OSM / 堡垒机)? EasyConnect exists, but Remote Desktop connection fails.**

Answer:

In a Sangfor 运维安全管理系统 (operation security management / bastion host), the architecture is usually:

```
Your PC
  |
  | HTTPS
  |
EasyConnect (SSL VPN)
  |
  |
Sangfor 运维安全管理系统
  |
  | RDP protocol
  |
Windows Server / PC
```

EasyConnect only creates the **VPN tunnel**. It does **not** directly provide RDP. After VPN is connected, you still need to access the bastion system and launch an RDP session.

---

## Correct workflow

### 1. Start EasyConnect

Example:

```
EasyConnect
    |
    v
https://vpn.company.com
    |
Login
    |
Connected
```

Check that the VPN adapter appears:

Windows:

```
Win + R
ncpa.cpl
```

You should see something like:

```
Sangfor SSL VPN Adapter
```

or a virtual network adapter.

---

### 2. Open Sangfor 运维安全管理系统 Web portal

After EasyConnect connects, open:

```
https://<堡垒机地址>
```

or sometimes:

```
https://<vpn-address>:443
```

Login:

```
username
password
OTP / SMS token
```

---

### 3. Find the asset

Usually:

```
资产管理
    |
    └── Windows Server
            |
            └── RDP
```

or:

```
我的资源
    |
    └── Remote Desktop
```

Click:

```
Connect
```

The bastion system will create the RDP session.

---

# If RDP fails

There are several layers.

## Case 1: EasyConnect connected, but asset list empty

Meaning:

```
VPN OK
堡垒机 authentication OK
Asset permission missing
```

Need admin to grant:

```
User
 |
Resource permission
 |
Windows server
 |
RDP permission
```

---

## Case 2: RDP timeout

Example:

```
Connection timeout
Unable to connect
```

Check:

From your machine:

```powershell
Test-NetConnection <target-ip> -Port 3389
```

Expected:

```
TcpTestSucceeded : True
```

If false:

* Windows firewall blocks RDP
* Server not running RDP
* Network route missing

---

## Case 3: RDP login failed

Example:

```
The logon attempt failed
```

Usually:

Wrong:

```
username
password
domain
```

Common format:

```
DOMAIN\username
```

or:

```
server\administrator
```

---

## Case 4: Browser RDP plugin fails

Sangfor often uses:

* Web RDP
* ActiveX/plugin
* HTML5 RDP

Try:

### Chrome / Edge

Allow popups:

```
Settings
 → Site permissions
 → Pop-ups
 → Allow
```

If it downloads:

```
.rdp
```

file, open with:

```
mstsc.exe
```

---

## Check EasyConnect status

Run:

```cmd
ipconfig
```

You should see a VPN IP.

Example:

```
Ethernet adapter Sangfor VPN:

IPv4 Address . . . : 10.x.x.x
```

If no VPN IP:

```
EasyConnect connected
```

but tunnel is not established.

---

## Important: Windows 11 + EasyConnect

Your previous EasyConnect version note says:

```
M7.1之前不支持 Win11
```

meaning:

* versions before M7.1 do not support Windows 11
* M7.6.x should support Windows 11

So confirm:

```
EasyConnect version >= 7.1
```

---

For exact debugging, the important information is:

1. EasyConnect status:

```
Connected / Failed?
```

2. After VPN login, can you open:

```
https://堡垒机地址
```

3. What error appears when clicking RDP:

```
timeout?
login failed?
blank page?
plugin error?
```

4. Are you using:

```
Web RDP
```

or downloaded:

```
.rdp file + mstsc
```

The failure point tells whether it is **VPN**, **堡垒机 permission**, or **Windows RDP**.
