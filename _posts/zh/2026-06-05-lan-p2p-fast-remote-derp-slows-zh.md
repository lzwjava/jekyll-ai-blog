---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 局域网P2P快速，远程DERP缓慢
translated: true
type: note
---

问题：当我的笔记本电脑和目标服务器在同一局域网时，Tailscale 速度很快，但当我的笔记本在局域网外时，延迟大约为 500ms，这是为什么？

回答：

是的，你的观察是正确的，原因如下：

1. **同一局域网（LAN）场景**
   * 当你的笔记本电脑和目标服务器处于同一局域网时，Tailscale 通常能够使用**直接的端到端（P2P）连接**。
   * Tailscale 会尝试通过**局域网路由或 NAT 穿透**（如 UDP 打洞）来建立连接。
   * 由于流量始终保持在本地网络内，延迟极低——通常只有几毫秒。

2. **局域网外（远程访问）场景**
   * 当你的笔记本电脑处于局域网外（例如家庭网络或公共网络）时，由于 NAT、防火墙或对称 NAT 设置，Tailscale **可能无法建立直接的 P2P 连接**。
   * 在这种情况下，流量会通过 **Tailscale 的 DERP（迂回加密中继协议）服务器** 进行中继，这些服务器充当转发节点。
   * 这些 DERP 服务器可能在地理上相距甚远，因此数据包需要传输更长的距离，增加了**数百毫秒的延迟**，这就解释了你所遇到的约 500ms 延迟。

3. **影响延迟的其他因素**
   * 你的笔记本电脑与 DERP 节点之间的互联网连接速度和路由。
   * 公共网络上的拥塞或丢包。
   * VPN 加密开销虽然很小，但并非为零。

**总结：**

* 局域网内：直接 P2P → 快速，低延迟（约 1–10ms）。
* 远程：通过 DERP 中继 → 延迟更高（在你的情况下约 500ms）。

你可以使用以下命令检查你的 Tailscale 连接是直连还是中继：

```bash
tailscale status --json
```

查看结果中的 `"via":"derp"`（中继）或 `"via":"direct"`（P2P）。

这解释了为什么当你在局域网外时速度会下降。

参考资料：

* [Tailscale：工作原理](https://tailscale.com/kb/1017/how-it-works/)
* [Tailscale DERP 详解](https://tailscale.com/blog/derp/)