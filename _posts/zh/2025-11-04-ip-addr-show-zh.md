---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 解读 ip addr show enp4s0 命令输出
translated: true
type: note
---

### 解析你的 `ip addr show enp4s0` 输出

这条命令显示了以太网接口（enp4s0）的详细信息，该接口负责处理我们之前讨论的路由表中的本地局域网连接。它已启动并运行顺畅——这对基础连接来说非常理想。我将逐行解析，然后进行总结。

#### 关键部分解析

- **接口状态**：
  `2: enp4s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000`
  - 索引 2（继 lo 之后的第二个接口）。
  - 标志：支持广播/组播，完全 UP（链路已检测到并可运行）。
  - MTU：1500 字节（标准以太网帧大小——无巨型帧）。
  - 队列规则：fq_codel（用于低延迟流量的公平队列，现代 Linux 上常见）。
  - 状态：UP（准备发送/接收）。

- **链路层（MAC 地址）**：
  `link/ether 04:7c:16:d9:54:5b brd ff:ff:ff:ff:ff:ff`
  - 你的硬件 MAC：04:7c:16:d9:54:5b（此网卡唯一）。
  - 广播地址：ff:ff:ff:ff:ff:ff（以太网广播的全 1 地址）。

- **IPv4 地址**：
  `inet 192.168.1.35/24 brd 192.168.1.255 scope global dynamic noprefixroute enp4s0`
  `valid_lft 4790sec preferred_lft 4790sec`
  - IP：192.168.1.35，子网掩码 /24（255.255.255.0）。与你路由表中的 "src 192.168.1.35" 匹配。
  - 广播地址：192.168.1.255（用于子网范围内的广播）。
  - 作用域：global（可路由到此主机之外）。
  - 动态：通过 DHCP 分配（来自你的路由器 192.168.1.1）。
  - 无前缀路由：不会自动添加直连路由（但内核仍然添加了，如 `ip route` 所示）。
  - 租约：约 79 分钟后到期（4790 秒），之后将续订。

- **IPv6 地址**：
  `inet6 fe80::a884:a0f6:e8b4:4a7d/64 scope link noprefixroute`
  `valid_lft forever preferred_lft forever`
  - 链路本地 IPv6：fe80::...（根据 MAC 自动生成；仅用于本地链路通信，如邻居发现）。
  - 前缀 /64，作用域 link（无法通过此接口路由出去）。
  - 永久有效（不会过期）。

#### 快速总结表

| 方面         | 值/详情                        | 含义说明 |
|--------------|--------------------------------|---------------|
| **状态**     | UP, MTU 1500                  | 接口处于活动状态，正在处理标准数据包。 |
| **MAC**      | 04:7c:16:d9:54:5b             | 你的设备在物理线路上的硬件地址。 |
| **IPv4**     | 192.168.1.35/24 (DHCP)        | 本地局域网 IP；发往此子网的流量通过 enp4s0 接口。 |
| **IPv6**     | fe80::a884:a0f6:e8b4:4a7d/64  | 仅限本地使用的 IPv6；对 IPv6 邻居发现等有用。 |
| **租约**     | 剩余约 79 分钟                | DHCP 即将刷新——如果需要，可使用 `dhclient -r enp4s0 && dhclient enp4s0` 检查。 |

这个配置解释了为什么你的默认路由指向此接口以访问互联网，以及为什么本地 192.168.1.x 流量是直连的。如果你在局域网内 ping，它会通过 ARP 获取 MAC 地址，并通过此接口发送帧。

一切看起来都正常吗，还是有什么问题（例如，没有 IPv6 全局地址，或连接断开）？如果你分享其他接口的 `ip addr` 或 `ping` 结果，我可以进一步分析。接下来要做什么——测试 Docker 网桥，还是其他什么？
