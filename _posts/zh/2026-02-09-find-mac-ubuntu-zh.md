---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 Ubuntu 中快速查找 MAC 地址
translated: true
type: note
---

Question: 如何在 Ubuntu 电脑上查找 MAC address？

Answer:

在 Ubuntu 上查找 **MAC address**（也称为 hardware address 或 physical address）最简单且最现代的方法是在 Terminal 中使用 `ip` 命令。这适用于当前的 Ubuntu 版本（包括 22.04、24.04 以及随后的 2026 版本）。

### 推荐方法 (Command Line – 适用于所有场景)

1. 打开 **Terminal**（按下 `Ctrl + Alt + T` 或搜索 "Terminal"）。

2. 运行以下命令之一：

   - 完整详细视图（推荐）：
     ```
     ip link show
     ```
     或
     ```
     ip addr show
     ```

   在每个 network interface 下查找以 `link/ether` 开头的行。

   输出示例（您的显示内容会有所不同）：
   ```
   1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
       link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
   2: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
       link/ether **b8:27:eb:12:34:56** brd ff:ff:ff:ff:ff:ff
   3: wlp2s0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DORMANT group default qlen 1000
       link/ether **a0:bb:cc:dd:ee:ff** brd ff:ff:ff:ff:ff:ff
   ```

   - MAC address 是 `link/ether` 后面由六组两位十六进制数字组成的地址（例如：`b8:27:eb:12:34:56`）。
   - 常见的 interface 名称：
     - Ethernet (有线): `enpXsY`, `eth0`, `eno1` 等。
     - Wi-Fi (无线): `wlpXsY`, `wlan0` 等。
     - 忽略 `lo` (loopback — 它始终显示 `00:00:00:00:00:00`)。

3. 如果只想查看 MAC addresses（简洁输出）：
   ```
   ip link show | grep -i ether
   ```
   或者（更简洁，每行一个）：
   ```
   LANG=C ip link show | awk '/link\/ether/ {print $2}'
   ```

### 其他方法

- 使用 `/sys/class/net`（非常可靠，无需额外解析）：
  ```
  cat /sys/class/net/*/address
  ```
  → 显示每个 interface 的 MAC（每行一个）。如果出现 `lo` 请忽略。

- 针对特定 interface（例如名为 `enp3s0` 的 Ethernet）：
  ```
  cat /sys/class/net/enp3s0/address
  ```

- 旧方法（在许多系统上仍然有效，但 `ifconfig` 已被弃用）：
  ```
  ifconfig -a | grep -i "ether\|HWaddr"
  ```
  （如果缺少 `ifconfig`，您可能需要先通过 `sudo apt install net-tools` 安装 `net-tools`。）

### 关于 Wake-on-LAN 的小提示
如果您是为了 WOL 查找 MAC（例如在原始测试步骤中），请使用有线 Ethernet interface 的 MAC，因为 Wake-on-LAN 通常只在 Ethernet 上工作。

References:

- [https://itsfoss.com/find-mac-address-linux](https://itsfoss.com/find-mac-address-linux)
- [https://askubuntu.com/questions/628383/output-only-mac-address-on-ubuntu](https://askubuntu.com/questions/628383/output-only-mac-address-on-ubuntu)
- [https://superuser.com/questions/164426/how-can-i-see-my-mac-address-on-ubuntu](https://superuser.com/questions/164426/how-can-i-see-my-mac-address-on-ubuntu)
