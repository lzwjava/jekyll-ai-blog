---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 不要在RDP中使用EasyConnect IP
translated: true
type: note
---

问题：**如何在 Windows 远程桌面连接 (mstsc) 中设置 EasyConnect VPN 地址？**

答案：

**请勿将 EasyConnect 虚拟 IP 填入远程桌面连接。**

在 `mstsc.exe` 中：

```
计算机：
<目标 Windows 服务器 IP 或主机名>
```

示例：

```
计算机：10.20.30.40
```

或：

```
计算机：server01.company.local
```

然后点击：

```
连接
```

---

EasyConnect 虚拟 IP 仅供 VPN 适配器自动使用，无需在 RDP 中配置。

流程如下：

```
EasyConnect 已连接
        |
        v
Windows 路由表已知：
10.20.0.0/16 -> VPN 隧道
        |
        v
mstsc.exe
计算机：10.20.30.40
        |
        v
RDP 通过 VPN 进行
```

如果您只有 EasyConnect 虚拟 IP，例如：

```
10.100.1.25
```

这是您的 VPN 客户端地址，不能用于 RDP，除非 `10.100.1.25` 所在的机器本身就是 RDP 服务器。

要测试：

```powershell
ipconfig
```

找到：

```
Sangfor SSL VPN 适配器
IPv4 地址：10.x.x.x
```

忽略该地址。

请使用**远程资产/服务器 IP**，由 Sangfor 运维安全管理系统提供。