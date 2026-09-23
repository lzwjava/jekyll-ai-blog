---
audio: false
generated: true
image: false
lang: zh
layout: post
title: PPTP VPN协议详解
translated: true
type: note
---

问题：VPN中的PPTP是什么？

答案：**PPTP（点对点隧道协议）** 是一种老旧的VPN协议，它在你的设备和VPN服务器之间创建一条隧道。

从高层次来看：

```text
你的设备
    │
    │  PPTP隧道
    ▼
VPN服务器
    │
    ▼
互联网
```

### 工作原理

PPTP本质上结合了：

1. **PPP** —— 承载你的网络流量。
2. **GRE** —— 封装PPP数据包。
3. **MPPE** —— 加密PPP载荷。

历史上，PPTP通常使用：

```text
TCP 1723  → 控制连接
GRE       → 承载隧道数据
```

一个重要的细节是，**GRE既不是TCP也不是UDP**，它是IP协议号47。

### 为什么今天不应该使用PPTP

PPTP的认证/加密设计从根本上就有缺陷。特别是与PPTP配合使用的**MS-CHAPv2**，存在实际的密码学弱点，使得捕获的VPN流量容易遭受离线密码攻击。

因此：

```text
PPTP
 ├── 易于实现
 ├── 速度快
 ├── 历史上广泛支持
 └── ❌ 密码学上已过时
```

现代VPN通常改用**WireGuard**、**IKEv2/IPsec**或**OpenVPN**。

如果你是因为调试遗留VPN而关注PPTP，我也可以用tcpdump/Wireshark命令带你走一遍**实际的数据包流程（`TCP 1723 → GRE → PPP → MS-CHAPv2`）**。