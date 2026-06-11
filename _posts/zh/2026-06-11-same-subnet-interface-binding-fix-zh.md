---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 同子网接口绑定修复
translated: true
type: note
---

还原。以下是实际问题的解释：

```
根本原因：同一子网中有两个网络接口
==========================================

在节点 1.47 上：
  wlp3s0:           192.168.1.47/24  (DOWN，但 IP 仍然存在)
  enx00e04c362f89:  192.168.1.28/24  (UP，以太网)

Gloo 会创建成对套接字用于数据传输。即使设置了
GLOO_SOCKET_IFNAME=enx00e04c362f89，Gloo 的 C++ 传输层
也可能将成对套接字绑定到 192.168.1.47（WiFi IP）而非
192.168.1.28（以太网 IP）。主节点连接到以太网 IP，
但套接字却在 WiFi IP 上监听（WiFi 处于 DOWN 状态，导致超时）。

你之前执行的 `ip addr flush` 有效，但 NetworkManager 的
DHCP 客户端立即重新分配了该 IP。还需要告知
NetworkManager 停止管理 WiFi。

修复方法（在 1.47 终端使用 sudo 执行）：

  sudo nmcli device set wlp3s0 managed no
  sudo ip addr flush dev wlp3s0
  ip addr show wlp3s0    # 确认没有 inet 行

然后我将重新开始训练。
```
