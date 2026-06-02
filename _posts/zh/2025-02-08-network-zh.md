---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 云 IP、网络接口与 WiFi 优化
translated: true
type: post
---

### 目录

1. [Hetzner Cloud 中的浮动 IP](#hetzner-cloud-中的浮动-ip)
   - IP 配置命令
   - Netplan 配置设置
   - 网络配置文件

2. [网络接口管理](#网络接口管理)
   - 删除 TUN 接口
   - 接口状态监控
   - 网络故障排除

3. [局域网 IP 扫描器](#局域网-ip-扫描器)
   - Python 网络扫描脚本
   - 多线程主机发现
   - 端口扫描功能
   - 局域网设备识别

4. [绕过局域网 IP](#绕过局域网-ip)
   - 局域网代理配置
   - 子网掩码计算
   - 网络范围规划

5. [使用 IPv6 地址进行 SSH 连接](#使用-ipv6-地址进行-ssh-连接)
   - IPv6 SSH 配置
   - SSH 配置文件管理
   - 不同地址类型的代理命令设置
   - 性能优化

6. [提升 WiFi 速度](#提升-wifi-速度)
   - 旧调制解调器与新调制解调器性能对比
   - 网络设置配置
   - 有线与无线桥接模式
   - 网络瓶颈排查

7. [OpenWrt 重置](#openwrt-重置)
   - 网页界面重置方法
   - 命令行重置步骤
   - 恢复出厂默认设置

---

## Hetzner Cloud 中的浮动 IP

### IP

```bash
sudo ip addr add 78.47.144.0 dev eth0
```

### Netplan

```bash
touch /etc/netplan/60-floating-ip.yaml
nano /etc/netplan/60-floating-ip.yaml
```

```yaml
network:
   version: 2
   renderer: networkd
   ethernets:
     eth0:
       addresses:
       - 78.47.144.0/32
```

```bash
sudo netplan apply
```

---

## 网络接口管理

删除 `tun` 接口。

```bash

$ ipconfig

outline-tun0: flags=4305<UP,POINTOPOINT,RUNNING,NOARP,MULTICAST>  mtu 1500
        inet 10.0.85.1  netmask 255.255.255.255  destination 10.0.85.1
        unspec 00-00-00-00-00-00-00-00-00-00-00-00-00-00-00-00  txqueuelen 500  (UNSPEC)
        RX packets 208  bytes 8712 (8.7 KB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 385  bytes 23322 (23.3 KB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

$ sudo ip link delete outline-tun0
```

---

## 局域网 IP 扫描器

此 Python 脚本用于扫描局域网中的活动 IP 地址。它使用 `ping` 命令检查主机是否可达，并采用多线程加速扫描过程。信号量限制并发线程数量，以避免系统过载。脚本接受网络地址（例如 "192.168.1.0/24"）作为输入，并打印网络中每个 IP 地址的在线状态。

此脚本可帮助识别网络中的设备，例如以有线桥接模式运行的 TP-LINK 网状路由器，通过扫描活动 IP 地址。

```python
import subprocess
import ipaddress
import threading
import os
import socket
import argparse

MAX_THREADS = 50  # 最大线程数

def is_host_up(host, port=None):
    """
    使用 ping 或 telnet 检查主机是否在线。
    如果指定端口，则使用 telnet 检查该端口是否开放。
    否则使用 ping。
    如果主机在线则返回 True，否则返回 False。
    """
    if port:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                return True
            else:
                return False
        except socket.error as e:
            return False
        finally:
            sock.close()
    else:
        try:
            # -c 1: 仅发送 1 个数据包
            # -W 1: 等待 1 秒响应
            subprocess.check_output(["ping", "-c", "1", "-W", "1", host], timeout=1)
            return True
        except subprocess.CalledProcessError:
            return False
        except subprocess.TimeoutExpired:
            return False

def scan_ip(ip_str, up_ips, port=None):
    """
    扫描单个 IP 地址并打印其状态。
    """
    if is_host_up(ip_str, port):
        print(f"{ip_str} 在线")
        up_ips.append(ip_str)
    else:
        print(f"{ip_str} 离线")

def scan_network(network, port=None):
    """
    使用线程扫描网络中的活动主机，限制并发线程数量。
    """
    print(f"正在扫描网络: {network}")
    threads = []
    semaphore = threading.Semaphore(MAX_THREADS)  # 限制并发线程数量
    up_ips = []

    def scan_ip_with_semaphore(ip_str):
        semaphore.acquire()
        try:
            scan_ip(ip_str, up_ips, port)
        finally:
            semaphore.release()

    for ip in ipaddress.IPv4Network(network):
        ip_str = str(ip)
        thread = threading.Thread(target=scan_ip_with_semaphore, args=(ip_str,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return up_ips

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="扫描网络中的活动主机。")
    parser.add_argument("network", nargs='?', default="192.168.1.0/24", help="要扫描的网络（例如 192.168.1.0/24）")
    parser.add_argument("-p", "--port", type=int, help="要检查的端口（可选）")
    args = parser.parse_args()

    network_to_scan = args.network
    port_to_scan = args.port

    up_ips = scan_network(network_to_scan, port_to_scan)
    print("\n在线 IP:")
    for ip in up_ips:
        print(ip)
```

---

## 绕过局域网 IP

脚本识别活动 IP 地址。为确保网络通信正常，请验证代理设置是否配置为绕过这些局域网 IP。

```bash
192.168.0.0/16,10.0.0.0/8,172.16.0.0/12,127.0.0.1,localhost,*.local,timestamp.apple.com,sequoia.apple.com,seed-sequoia.siri.apple.com, 192.168.1.0/16
```

---

## 子网掩码

第二台机器通常位于 192.168.1.16。

使用以下命令可正常工作：

```bash
python scripts/ip_scan.py 192.168.1.0/27 -p 22
```

因为 32 - 27 = 5，2^5 = 32，所以会尝试 `192.168.1.0` 到 `192.168.1.31`。

但使用 `192.168.1.0/28` 时无效，因为 2^4 = 16，所以会尝试 `192.168.1.0` 到 `192.168.1.15`，不包含 `192.168.1.16`。

---

## 使用 IPv6 地址进行 SSH 连接

尝试使用 IPv6 地址连接 Hetzner Cloud 中的机器。`ssh 2a01:4f8:c17:2000::/64` 不生效，但 `ssh root@2a01:4f8:c17:2000::1` 可行。

IPv6 地址从 Hetzner Cloud 控制台复制。

`~/.ssh/config` 文件可配置为对 IPv4 和 IPv6 地址应用不同的代理规则。此设置允许为 IPv4 地址指定代理命令，同时对 IPv6 地址采用不同处理。

```bash
Host 192.168.1.*
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
Host *.*.*.*
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
    ProxyCommand corkscrew localhost 7890 %h %p
Host *
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
```

运行 `ssh root@192.168.1.3` 时，以下输出显示 SSH 客户端从 `~/.ssh/config` 文件应用配置选项：

```bash
debug1: Reading configuration data /Users/lzwjava/.ssh/config
debug1: /Users/lzwjava/.ssh/config line 1: Applying options for 192.168.1.*
debug1: /Users/lzwjava/.ssh/config line 5: Applying options for *.*.*.*
debug2: add_identity_file: ignoring duplicate key ~/.ssh/id_rsa
debug1: /Users/lzwjava/.ssh/config line 10: Applying options for *
debug2: add_identity_file: ignoring duplicate key ~/.ssh/id_rsa
debug1: Reading configuration data /etc/ssh/ssh_config
debug1: /etc/ssh/ssh_config line 21: include /etc/ssh/ssh_config.d/* matched no files
debug1: /etc/ssh/ssh_config line 54: Applying options for *
debug2: resolve_canonicalize: hostname 192.168.1.3 is address
debug3: expanded UserKnownHostsFile '~/.ssh/known_hosts' -> '/Users/lzwjava/.ssh/known_hosts'
debug3: expanded UserKnownHostsFile '~/.ssh/known_hosts2' -> '/Users/lzwjava/.ssh/known_hosts2'
debug1: Authenticator provider $SSH_SK_PROVIDER did not resolve; disabling
debug3: channel_clear_timeouts: clearing
debug1: Executing proxy command: exec corkscrew localhost 7890 192.168.1.3 22
```

SSH 连接速度明显变慢，因此恢复为以下更简单的配置：

```bash
Host 192.168.1.*
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
Host *
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
    ProxyCommand corkscrew localhost 7890 %h %p
```

问题出现在使用 `ProxyCommand corkscrew localhost 7890 %h %p` 指令与 IPv6 地址时，因为此代理命令可能无法正确处理 IPv6 地址。

上述配置仍无效，但以下配置可行：

```bash
Host 192.168.1.*
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
Host !192.*.*.*
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
    ProxyCommand corkscrew localhost 7890 %h %p
Host *
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa
```

---

## 提升 WiFi 速度

### 旧调制解调器问题

父母家中的调制解调器较旧，可能有 10 年历史。初始网络设置为：

调制解调器 -> 3 米无线 -> TP-Link AX3000（无线桥接模式）-> 2 米、一堵墙、无线 -> 笔记本电脑

导致下载速度较低，Speedtest 结果仅为 10 Mbps。

改进后的设置采用有线连接：

调制解调器 -> 2 米网线 -> TP-Link AX3000（有线桥接模式）-> 4 米无线、一堵墙 -> 笔记本电脑

下载速度提升至 90 Mbps。

### 新调制解调器性能

我家中的调制解调器较新，TP-Link 路由器在无线桥接模式下表现良好。网络设置为：

调制解调器 -> 4 米无线 -> TP-Link AX3000（无线桥接模式）-> 2 米无线 -> 笔记本电脑

网络质量良好。

### 故障排查建议

提升 Wi-Fi 速度没有通用解决方案。建议使用网线测试网络各部分，以识别瓶颈。比较有线连接与 Wi-Fi 的速度，并尝试用网线直接连接设备，看是否提升性能。

---

## OpenWrt 重置

### 通过网页界面重置

建议通过以太网线连接路由器。重置后，Wi-Fi SSID 将恢复为默认设置，可能与预期不同。

### 通过命令行（SSH）重置

可通过命令行界面（SSH）将 OpenWrt 恢复为默认设置。步骤如下：

1. 通过 SSH 连接 OpenWrt 路由器。
2. 运行以下命令：

    ```bash
    root@OpenWrt:~# firstboot
    This will erase all settings and remove any installed packages. Are you sure? [N/y]
    y
    /dev/ubi0_1 is mounted as /overlay, only erasing files
    root@OpenWrt:~# reboot
    ```
3. 路由器将以默认设置重启。

**命令说明：**

* `firstboot`：启动重置过程，擦除所有配置和已安装软件包。
* `reboot`：重启路由器，应用重置。
