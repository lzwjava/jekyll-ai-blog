---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过EasyConnect VPN的RDP
translated: true
type: note
---

问题：**如果 EasyConnect 创建了一个虚拟 IP 地址，如何使用该虚拟地址通过远程桌面 (RDP) 进行跳转？**

答案：

EasyConnect 的“虚拟地址”通常**不是目标 Windows 机器的地址**，而是**VPN 客户端在企业网络内的虚拟 IP**。

流程如下：

```
你的笔记本电脑
    |
    | EasyConnect SSL VPN
    |
虚拟 VPN 适配器
IP：10.x.x.x（分配给你的笔记本电脑）
    |
    | 路由表
    |
企业网络
    |
    | RDP TCP/3389
    |
Windows 服务器
IP：192.168.x.x / 10.x.x.x
```

因此，通常**你不会 RDP 到 EasyConnect 的虚拟 IP**。

错误的做法：

```
mstsc.exe
计算机：
10.8.0.15   <-- EasyConnect 客户端 IP
```

那是你自己的 VPN 地址。

---

## 找到真正的目标 IP

在 EasyConnect 连接后：

运行：

```cmd
ipconfig
```

示例：

```
以太网适配器 Sangfor SSL VPN:

   IPv4 地址 . . . . . . . . . . . : 10.100.1.25
```

这是你的 VPN IP。

然后检查路由：

```cmd
route print
```

示例：

```
网络目标          网关
10.20.0.0          10.100.1.1
172.16.0.0         10.100.1.1
```

含义：

```
10.20.x.x
172.16.x.x
```

可以通过 VPN 访问。

---

## RDP 连接到服务器

如果管理员给你：

```
Windows 服务器：
10.20.30.40
```

那么：

运行：

```
mstsc.exe
```

输入：

```
计算机：
10.20.30.40
```

或者：

```
10.20.30.40:3389
```

登录：

```
DOMAIN\用户名
```

或者：

```
用户名
```

---

## 在 Sangfor 运维安全管理系统（堡垒机）中

通常你不会直接连接到服务器 IP。

设计如下：

```
用户
 |
EasyConnect VPN
 |
Sangfor OSM
 |
资产数据库
 |
RDP 代理
 |
服务器
```

堡垒机隐藏了真实 IP。

你点击：

```
资产
  |
Windows 服务器
  |
RDP
```

Sangfor 内部会执行：

```
Sangfor 服务器
     |
     | RDP
     |
10.20.30.40:3389
```

---

## 如果你想直接 RDP

你需要三样东西：

### 1. 路由存在

检查：

```cmd
tracert 10.20.30.40
```

预期结果：

```
10.100.x.x（VPN 网关）
10.20.30.40
```

---

### 2. 端口开放

```powershell
Test-NetConnection 10.20.30.40 -Port 3389
```

预期结果：

```
TcpTestSucceeded : True
```

---

### 3. 权限

即使网络正常：

```
TCP 3389 开放
```

Windows 仍然需要：

```
远程桌面用户
```

权限。

---

所以关键点：

* **EasyConnect 虚拟 IP = 你笔记本电脑的 VPN 身份**
* **RDP 目标 IP = 服务器/资产的 IP**
* **Sangfor OSM 通常代理 RDP；你不应该手动使用 EasyConnect IP 进行跳转**

如果你在 EasyConnect 连接后运行：

```cmd
ipconfig
route print
```

你可以看到它暴露了哪些网络范围。
