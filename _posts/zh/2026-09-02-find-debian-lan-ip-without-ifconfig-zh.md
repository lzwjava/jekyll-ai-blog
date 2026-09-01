---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 不使用ifconfig查找Debian局域网IP
translated: true
type: note
---

问题：当 `ifconfig` 未安装时，如何查找 Debian 机器的局域网 IP？

答案：在 modern Debian 上，只需使用内置的 `ip` 命令即可。你**不需要 `ifconfig`**。

```bash
ip addr
```

查找类似以下内容：

```text
2: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP>
    inet 192.168.1.123/24
```

你的局域网 IP 就是：

```text
192.168.1.123
```

### 更简单的方法

```bash
hostname -I
```

示例：

```text
192.168.1.123
```

对于你的 SSH 配置，这很可能就是你需要的全部：

```bash
hostname -I
```

然后从另一台电脑执行：

```bash
ssh your_username@192.168.1.123
```

### 如果 `hostname -I` 没有输出

检查网络接口：

```bash
ip link
```

以及路由：

```bash
ip route
```

一台典型的已连接 Debian 机器会显示：

```text
default via 192.168.1.1 dev enp3s0
192.168.1.0/24 dev enp3s0 src 192.168.1.123
```

其中的 `src` 地址就是你的局域网 IP。

如果你特别想要 `ifconfig`，可以通过以下命令安装：

```bash
sudo apt install net-tools
```

但我建议**学习/使用 `ip` 代替**。`ifconfig` 是较旧的接口；`ip` 是现代 Linux 网络工具。