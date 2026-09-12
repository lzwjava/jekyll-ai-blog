---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Windows Server 2008账户类型
translated: true
type: note
---

问题：Windows Server 2008 支持哪两种类型的账户？

答案：Windows Server 2008 支持两种类型的账户：

1. **本地账户 (Local Accounts)** — 存储在本地计算机上，通过本地安全帐户管理器 (SAM) 数据库进行管理，仅在该特定计算机上有效。

2. **域账户 (Domain Accounts)** — 存储在域控制器 (Active Directory) 上，可在整个网络中进行身份验证，允许用户登录到加入该域的任何计算机。

参考：

- [Windows Server 2008 用户账户概述 – Microsoft Docs](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2008-R2-and-2008/cc732386(v=ws.10))
