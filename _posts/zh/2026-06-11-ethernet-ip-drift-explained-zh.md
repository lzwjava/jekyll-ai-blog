---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 以太网IP漂移解析
translated: true
type: note
---

**问题：** 为什么以太网显示 192.168.1.28，而我的两台机器分别是 192.168.1.36 和 192.168.1.47？为什么 NanoChat 分布式训练会通过该 IP 连接？

**回答：**

你的 `xiaoxin` 机器有 **两个网络接口**，每个接口由于具有不同的 MAC 地址，都会获得 **独立的 DHCP 租约**：

- WiFi（`wlp3s0`）→ 曾是 `192.168.1.47`（你记忆中的 IP）
- 以太网（`enp*`）→ `192.168.1.28`（来自路由器的一个独立租约）

因此 `.47` 和 `.28` 是 **同一台物理机器**。日志显示 `wlp3s0` 处于 `state DOWN` 状态——WiFi 已断开，因此通往该主机的唯一活跃路径现在是通过以太网的 `.28`。这就是为什么代理重新指向了 SSH（并出现了主机密钥不匹配——同一台主机，新的 IP，因此执行了 `ssh-keygen -R`）。

为什么训练会“监听”该 IP：使用 Gloo 的 `torch.distributed` 通过 `MASTER_ADDR:MASTER_PORT` 进行会合。主节点（`.36`）监听，工作节点向外拨号。工作节点出站连接的源 IP 由内核路由表决定，该表选择到达 `.36` 的接口——现在是以太网网卡，因此主节点看到的连接来自 `.28`。Gloo 还会按接口绑定数据平面 socket；如果未设置 `GLOO_SOCKET_IFNAME`，它会选择默认路由的接口，而 WiFi 断开后默认路由发生了变化。

验证它们是否为同一台机器：

```bash
ssh xiaoxin@192.168.1.28 "hostname; ip -br addr; ip route get 192.168.1.36"
```

要防止 IP 漂移：

```bash
# 1. 固定 Gloo 使用的接口（在你的运行脚本中设置）
export GLOO_SOCKET_IFNAME=enp3s0   # 工作节点的以太网名称，通过 `ip -br link` 查看
export MASTER_ADDR=192.168.1.36

# 2. 更好的做法：在路由器中为以太网 MAC 设置 DHCP 保留，
#    这样 .28（或你选择的任何 IP）在重启后保持稳定。
```

额外好处：以太网本来就是分布式 CPU 训练的合适链路——Gloo allreduce 在 WiFi 上会增加延迟/抖动，从而拖慢步骤。将两个节点都保持有线连接，并在两端固定 `GLOO_SOCKET_IFNAME`。