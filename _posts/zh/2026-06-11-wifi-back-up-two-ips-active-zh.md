---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WiFi备份，两个IP活跃
translated: true
type: note
---

**问题：** 如果 WiFi 当时是 DOWN 状态，为什么我仍然能通过 192.168.1.47 访问那台机器？

**答案：**

因为 WiFi 后来又恢复了——日志中的 `state DOWN` 只是某一时刻的快照。NetworkManager 会自动重连，所以现在**两块网卡同时在线**，并且那台机器同时持有**两个 IP**：

- `192.168.1.47` → WiFi (`wlp3s0`)
- `192.168.1.28` → 以太网

两者都接受入站 SSH 连接。这是正常的多宿主（multi-homing）——并没有什么排他性。

在 xiaoxin 机器上确认：

```bash
ip -br addr          # 期望 wlp3s0 和 enp* 都是 UP 状态，各自有 IP
ip route             # 查看 'default via ... metric N' 行
```

你很可能看到两条不同 metric 的默认路由，例如：

```
default via 192.168.1.1 dev enp3s0 metric 100    # 以太网胜出（metric 更小）
default via 192.168.1.1 dev wlp3s0 metric 600
```

这种 metric 排序解释了你注意到的非对称性：

- **入站**：你可以连接到任意一个 IP——Linux 在哪个接口收到包就在哪个接口应答，回复时保持你拨号时的源 IP（弱主机模型）。所以 `.47` 从你的 Mac 上访问完全正常。
- **出站**：当 worker 向位于 `.36` 的 master 发起 Gloo 连接时，内核选择默认路由 → 以太网 → master 看到 worker 的 IP 是 `.28`。

因此：同一台机器，两个入口。你敲的是 `.47` 的门；训练进程从 `.28` 的门走出去。

为了保证训练稳定性，最好明确指定接口，而不是依赖 metric：

```bash
# 在 run_dist_cpu_worker.sh 中
export GLOO_SOCKET_IFNAME=enp3s0     # 从 `ip -br link` 获取准确名称
# 并在 master（.36）上
export GLOO_SOCKET_IFNAME=<其以太网接口名>
```

否则，运行中 WiFi 闪断会改变路由，导致 allreduce 挂起。两端都固定使用有线 = 稳定的步骤。
