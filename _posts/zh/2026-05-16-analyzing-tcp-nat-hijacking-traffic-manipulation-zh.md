---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 分析TCP NAT劫持流量操纵
translated: true
type: note
---

问题：如何分析和监控Linux系统层面的TCP NAT劫持与流量操纵，尤其是在旧硬件上使用OpenWrt时，从而理解流量劫持发生在哪里，以及每个网络层如何处理转发？

回答：

你实际上是在尝试剖析一个多层网络问题，TCP流量可能在系统的不同点被拦截、重定向或劫持。以下是一个结构化的方法：

---

### 1. **理解涉及的各个层**

在Linux网络中，流量经过多个层：

1. **应用层**

   * 包括 `redsocks`、`shadowsocks`、VPN客户端、浏览器或自定义网络守护进程等程序。
   * 如果它们绑定到特定端口或充当透明代理，则可能劫持流量。

2. **套接字/传输层（TCP/UDP）**

   * Linux内核TCP协议栈处理连接。
   * `tcpdump`、`ss`、`netstat` 等工具有助于检查活动连接和重传。

3. **Netfilter/Iptables层**

   * NAT规则（`PREROUTING`、`POSTROUTING`、`OUTPUT`）以及 `REDSOCKS` 等链。
   * 将流量重定向到用户空间代理或特定端口。

4. **路由层**

   * 内核的路由表决定了数据包的流向。
   * 配置错误的路由或默认网关会无意中重定向流量。

5. **DNS解析层**

   * `/etc/resolv.conf` 或自定义DNS服务。
   * 如果DNS被劫持，流量可能会解析到恶意IP。

6. **网络接口/硬件层**

   * 网卡、交换机或Wi-Fi卡。
   * 可能引入数据包丢失、错误路由或硬件卸载问题。

---

### 2. **流量捕获与日志记录**

要查看流量在哪里被拦截：

* **内核级TCP抓包：**

  ```bash
  tcpdump -i any tcp port 80 or port 443 -vv
  ```

  * 在接口层捕获所有TCP流量。

* **Netfilter日志：**

  ```bash
  iptables -t nat -A PREROUTING -p tcp -j LOG --log-prefix "PREROUTING: "
  iptables -t nat -A REDSOCKS -j LOG --log-prefix "REDSOCKS: "
  ```

  * 记录进入NAT链的数据包。可用于查看流量是否命中预期规则。

* **应用级日志：**

  * `redsocks` 或 `shadowsocks` 可以记录连接、错误和重定向。
  * 监控 `/var/log/syslog` 或 `/var/log/messages`。

---

### 3. **旧硬件上的OpenWrt**

* OpenWrt 轻量级，可以在旧x86 PC上运行，但2011年的硬件可能有小问题：

  * **BIOS/UEFI问题：** 一些旧主板难以支持PXE或现代Linux内核。
  * **网卡支持：** 确保OpenWrt内核包含你的以太网/Wi-Fi卡驱动。
  * **精简构建：** 使用 `x86-generic` 或 `x86-64` 镜像，移除不必要的软件包以节省内存。

---

### 4. **Iptables透明代理设置**

你已有类似设置：

```bash
iptables -t nat -A REDSOCKS -d <ip> -p tcp --dport <port> -j RETURN
iptables -t nat -A REDSOCKS -p tcp -j REDIRECT --to-ports 12345
iptables -t nat -A PREROUTING -p tcp -j REDSOCKS
```

**提示：**

* 分别测试每条规则以确认其按预期工作。
* 使用 `iptables -t nat -L -n -v` 查看数据包命中数。
* 确保没有其他链（如 `OUTPUT`）也在无意中重定向流量。

---

### 5. **DNS与流量劫持**

* `resolve.conf` 和任何DNS缓存（如OpenWrt中的 `dnsmasq`）可能会劫持或重定向查询。
* 要监控：

  ```bash
  tcpdump -i any port 53 -vv
  ```
* 检查你的DNS查询是否解析正确。

---

### 6. **分层分析方法**

1. **接口层：** 使用 `tcpdump` 捕获数据包。
2. **Netfilter层：** 记录 `PREROUTING`、`OUTPUT`、`REDSOCKS` 链的命中情况。
3. **路由层：** 验证 `ip route` 和 `ip rule` 条目。
4. **应用层：** 启用代理日志。
5. **DNS层：** 通过 `dig` 或 `nslookup` 确认解析。

通过跨层关联日志，你可以精确定位流量偏离预期的位置。

---

### 7. **可选工具**

* **Wireshark/TShark：** 图形界面或命令行数据包检查。
* **nethogs / iftop：** 按进程监控带宽。
* **strace/lsof：** 检查哪些进程持有套接字。
* **iptraf-ng：** 每个接口的实时流量统计。

---

简而言之，你的目标是检测每一层——从网卡、内核、NAT到代理——在每个交接点捕获流量。这是系统性地发现劫持发生位置的唯一方法。

---

参考资料：

* [OpenWrt x86安装指南](https://openwrt.org/docs/guide-user/installation/x86)
* [Linux Netfilter/Iptables HOWTO](https://wiki.nftables.org/wiki-nftables/index.php/Main_Page)
* [tcpdump手册](https://www.tcpdump.org/manpages/tcpdump.1.html)
