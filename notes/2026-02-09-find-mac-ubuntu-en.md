---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Find MAC Address in Ubuntu Fast
translated: false
type: note
---

Question: How to find the MAC address on an Ubuntu computer?

Answer: 

The easiest and most modern way to find the **MAC address** (also called hardware address or physical address) on Ubuntu is using the `ip` command in the terminal. This works on current Ubuntu versions (including 22.04, 24.04, and later in 2026).

### Recommended Method (Command Line – works everywhere)

1. Open a **Terminal** (press `Ctrl + Alt + T` or search for "Terminal").

2. Run one of these commands:

   - Full detailed view (recommended):
     ```
     ip link show
     ```
     or
     ```
     ip addr show
     ```

   Look for the line starting with `link/ether` under each network interface.

   Example output (yours will be different):
   ```
   1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default qlen 1000
       link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
   2: enp3s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP mode DEFAULT group default qlen 1000
       link/ether **b8:27:eb:12:34:56** brd ff:ff:ff:ff:ff:ff
   3: wlp2s0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN mode DORMANT group default qlen 1000
       link/ether **a0:bb:cc:dd:ee:ff** brd ff:ff:ff:ff:ff:ff
   ```

   - The MAC address is the six groups of two hexadecimal digits after `link/ether` (e.g., `b8:27:eb:12:34:56`).
   - Common interface names:
     - Ethernet (wired): `enpXsY`, `eth0`, `eno1`, etc.
     - Wi-Fi (wireless): `wlpXsY`, `wlan0`, etc.
     - Ignore `lo` (loopback — it always shows `00:00:00:00:00:00`).

3. To see only the MAC addresses (clean output):
   ```
   ip link show | grep -i ether
   ```
   or (even cleaner, one per line):
   ```
   LANG=C ip link show | awk '/link\/ether/ {print $2}'
   ```

### Alternative Methods

- Using `/sys/class/net` (very reliable, no extra parsing needed):
  ```
  cat /sys/class/net/*/address
  ```
  → Shows MAC for every interface (one per line). Ignore `lo` if present.

- For a specific interface (e.g., Ethernet named `enp3s0`):
  ```
  cat /sys/class/net/enp3s0/address
  ```

- Older method (still works on many systems, but `ifconfig` is deprecated):
  ```
  ifconfig -a | grep -i "ether\|HWaddr"
  ```
  (You may need to install `net-tools` first with `sudo apt install net-tools` if `ifconfig` is missing.)

### Quick Tip for Wake-on-LAN
If you're finding the MAC for WOL (like in your original test steps), use the wired Ethernet interface MAC (not Wi-Fi), as Wake-on-LAN typically only works over Ethernet.

References:  

- [https://itsfoss.com/find-mac-address-linux](https://itsfoss.com/find-mac-address-linux)
- [https://askubuntu.com/questions/628383/output-only-mac-address-on-ubuntu](https://askubuntu.com/questions/628383/output-only-mac-address-on-ubuntu)
- [https://superuser.com/questions/164426/how-can-i-see-my-mac-address-on-ubuntu](https://superuser.com/questions/164426/how-can-i-see-my-mac-address-on-ubuntu)