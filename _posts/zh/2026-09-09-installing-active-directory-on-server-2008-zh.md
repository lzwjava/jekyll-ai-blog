---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 Server 2008 上安装 Active Directory
translated: true
type: note
---

问题：**什么是 Active Directory？如何在 Windows Server 2008 上安装它？前提条件有哪些？**

答案：

## 1. 什么是 Active Directory？

**Active Directory (AD)** 是微软的目录服务，用于管理 Windows 域中的计算机、用户、组和策略。

其核心概念如下：

```text
                    Active Directory
                          │
                    Domain Controller
                          │
          ┌───────────────┼───────────────┐
          │               │               │
       Users            Groups         Computers
          │
       Policies
          │
    Authentication
```

不是每台电脑都有自己的独立账户：

```text
PC1:
  alice
  bob

PC2:
  alice
  bob

PC3:
  alice
  bob
```

而是创建一个中央域：

```text
                  example.local
                       │
              Domain Controller
                       │
        ┌──────────────┼──────────────┐
        │              │              │
      Alice           Bob          Admins
        │              │
      PC-01           PC-02
```

然后，Alice 可以使用以下方式登录到加入域的计算机：

```text
EXAMPLE\alice
```

域控制器会验证她的身份并应用组织的策略。

AD 围绕几个重要概念构建：

| 概念                    | 含义                                               |
| ----------------------- | -------------------------------------------------- |
| **Domain**              | 管理/安全边界                                      |
| **Domain Controller (DC)** | 运行 AD DS 的服务器                             |
| **AD DS**               | Active Directory 域服务                            |
| **User**                | 身份/账户                                          |
| **Group**               | 用户/计算机的集合                                   |
| **OU**                  | 组织单位；用于组织对象的容器                        |
| **Group Policy**        | 集中配置/安全规则                                   |
| **DNS**                 | 定位 AD 服务的关键                                  |
| **Kerberos**            | 主要身份验证协议                                    |

---

## 2. Windows Server 2008 术语

在 Windows Server 2008 上，需要安装 **Active Directory 域服务 (AD DS)** 角色。

主要分为两个步骤：

```text
Windows Server 2008
        │
        ▼
安装 AD DS 角色
        │
        ▼
运行 dcpromo
        │
        ▼
将服务器提升为域控制器
```

`dcpromo` 在 Server 2008 中尤为重要。

---

## 3. 前提条件

对于基本的实验室环境，不需要太多资源。

### 硬件

例如：

```text
CPU:      1 核或以上
RAM:      2 GB 或以上
磁盘:     ~40 GB 或以上
网络:     以太网/虚拟网卡
```

对于实际生产环境的域控制器，显然需要使用更强大的硬件/冗余配置。

### 操作系统

需要安装 Windows Server 2008 系统。

例如：

```text
Windows Server 2008 Standard
Windows Server 2008 Enterprise
Windows Server 2008 Datacenter
```

建议在严肃环境中使用 **x64** 版本。

---

## 4. 为服务器设置静态 IP

这一点很重要。

例如：

```text
IP:       192.168.1.10
掩码:     255.255.255.0
网关:     192.168.1.1
DNS:      192.168.1.10
```

注意：

```text
DNS = 自身
```

一旦这台机器成为域控制器和 DNS 服务器，它通常会为域提供 DNS 服务。

不要构建一个域控制器地址随机变化的 AD 环境。

---

## 5. 为服务器设置合理的主机名

例如：

```text
DC01
```

可以这样操作：

```text
控制面板
    → 系统
    → 更改设置
    → 计算机名
    → 更改
```

设置：

```text
计算机名: DC01
```

然后重启。

建议使用类似：

```text
DC01.example.local
```

而不是让机器保留为：

```text
WIN-ABC123
```

---

## 6. 安装 Active Directory 域服务

在 Server 2008 上：

```text
服务器管理器
    → 角色
    → 添加角色
```

选择：

```text
Active Directory 域服务
```

然后：

```text
安装
```

角色安装完成后，**这台机器还不是域控制器**。

这个区别很重要：

```text
已安装 AD DS 角色
        ≠
域控制器
```

还需要进行提升操作。

---

## 7. 运行 `dcpromo`

打开：

```text
开始
→ 运行
```

然后执行：

```cmd
dcpromo
```

应该会启动 Active Directory 域服务安装向导。

该向导本质上会询问：

> 你想创建或加入哪种类型的 AD 域？

对于第一台服务器，选择：

```text
在新林中新建域
```

然后输入域名。

在实验室环境中：

```text
example.local
```

或：

```text
ad.example.com
```

学习用途下，`example.local` 是可以的。

---

## 8. 选择林/域功能级别

对于纯 Server 2008 实验室，可以选择合适的 Server 2008 功能级别。

概念上：

```text
林
└── 域
    └── 域控制器
```

**林** 是最高级别的 AD 边界。

对于第一次安装：

```text
新林
    ↓
新域
    ↓
此服务器成为第一个域控制器
```

---

## 9. DNS

向导会询问 DNS 相关设置。

对于正常的 AD 部署，通常希望将 DNS 与域控制器一起安装/配置。

为什么？

因为 AD 不仅仅是这样：

```text
LDAP + 用户
```

DNS 对于 AD 服务发现至关重要。

客户端需要发现诸如：

```text
域控制器在哪里？
Kerberos 在哪里？
LDAP 在哪里？
域服务在哪里？
```

DNS 记录使其能够发现这些服务。

概念上：

```text
PC01
 │
 │ DNS 查询
 ▼
DNS
 │
 ├── _ldap._tcp
 ├── _kerberos._tcp
 └── DC01
       │
       ▼
Domain Controller
```

这是学习 AD 时需要理解的最重要的一点之一。

---

## 10. 目录服务还原模式密码

向导会要求创建一个：

```text
目录服务还原模式 (DSRM)
```

密码。

这**不是**普通的域管理员密码。

请将其保存在安全的地方。

它用于特殊的 AD 恢复/维护操作。

---

## 11. 数据库位置

会看到以下路径：

```text
C:\Windows\NTDS
C:\Windows\SYSVOL
```

对于简单的实验室环境，接受默认值即可。

重要的部分大致如下：

```text
NTDS
 └── Active Directory 数据库

SYSVOL
 └── 组策略
 └── 登录脚本
 └── 复制的域文件
```

AD 数据库通常为：

```text
NTDS.dit
```

这是 Active Directory 的核心文件之一。

---

## 12. 重启

`dcpromo` 完成后：

```text
重启
```

现在，服务器已成为域控制器。

之前：

```text
Windows Server
```

之后：

```text
Windows Server
     +
AD DS
     +
DNS
     +
域控制器
     +
Kerberos
     +
LDAP
     +
SYSVOL
```

---

## 13. 验证

重启后，打开：

```cmd
dsa.msc
```

这会打开：

```text
Active Directory 用户和计算机
```

应该能看到你的域：

```text
example.local
```

还可以运行：

```cmd
dcdiag
```

这会执行一系列域控制器诊断。

以及：

```cmd
ipconfig /all
```

检查 DNS 是否指向你的 AD DNS 服务器。

还可以检查：

```cmd
nslookup
```

和：

```cmd
net share
```

一个健康的域控制器应该会显示诸如：

```text
NETLOGON
SYSVOL
```

---

## 14. 加入另一台 Windows 机器

现在假设你有：

```text
DC01
192.168.1.10
example.local
```

和另一台机器：

```text
PC01
192.168.1.20
```

配置 PC01 的 DNS：

```text
DNS 服务器 = 192.168.1.10
```

**这一步至关重要。**

然后：

```text
PC01
  │
  │ DNS
  ▼
192.168.1.10
  │
  ▼
DC01
  │
  ▼
example.local
```

在 PC01 上：

```text
系统
→ 计算机名
→ 更改
→ 域
```

输入：

```text
example.local
```

Windows 会要求输入域凭据。

身份验证成功后，重启。

现在可以登录为：

```text
EXAMPLE\alice
```

而不是纯本地账户：

```text
PC01\alice
```

---

## 15. 最小的实验室架构

如果正在学习 AD，建议构建一个虚拟机实验室：

```text
             虚拟网络
                  │
       ┌──────────┴──────────┐
       │                     │
     DC01                  PC01
       │                     │
 Windows Server 2008      Windows 7
       │
 AD DS
 DNS
 Kerberos
 LDAP
```

示例：

```text
DC01
IP:       192.168.100.10
DNS:      192.168.100.10
域:       lab.local

PC01
IP:       192.168.100.20
DNS:      192.168.100.10
域:       lab.local
```

然后试验：

```text
用户
组
OU
组策略
域加入
Kerberos
DNS
LDAP
NTLM
文件权限
登录脚本
```

这样会比仅仅点击安装向导更深入地理解。

一个重要注意事项：**Windows Server 2008 已经非常陈旧且目前不受支持。** 它对理解旧版 AD 和历史环境很有用，但如果是新建实验室，除非专门要复现 2008 环境，否则通常应使用更新的 Windows Server 版本。