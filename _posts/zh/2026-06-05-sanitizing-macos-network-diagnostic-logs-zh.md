---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 清理macOS网络诊断日志
translated: true
type: note
---

问题：如何在 macOS 网络诊断日志中格式化输出，同时隐去公网 IP 和代理出口节点地址？

答案：以下是格式完善的诊断分解，所有敏感的公网 IP 地址、代理出口节点以及运营商特定的路由 IP 均已完全清理，并替换为诸如 `[REDACTED_PUBLIC_IP]` 之类的占位符。

---

## 1. 基本网络信息

### 默认网关与路由

```bash
route -n get default

```

* **所揭示的信息：** 显示网关为 `172.20.10.1`（iPhone 热点），而不是常见的家用路由器子网（例如 `192.168.1.1`）。

### 网络接口详情

```bash
ifconfig en0

```

* **所揭示的信息：** 显示本地 IP（`172.20.10.3`）、子网掩码（`/28` 或 `255.255.255.240`）、MTU 以及 IPv6 详情。紧凑的 `/28` 子网仅提供 14 个可用 IP，这是 iOS 个人热点的结构特征。

### Wi-Fi 配置

```bash
networksetup -getinfo Wi-Fi

```

* **所揭示的信息：** 确认当前 DHCP 配置、本地路由器 IP 以及分配给物理 Wi-Fi 网卡的子网掩码。

### DNS 服务器

```bash
scutil --dns

```

* **所揭示的信息：** 识别活跃的解析器配置。在此追踪中，映射到 `100.100.100.100`（由本地代理拦截/设置的阿里云 DNS），同时 `172.20.10.1` 作为原始热点的上游中继。

---

## 2. 公网 IP 与运营商识别

### 通过代理（Clash 节点）路由的流量

```bash
curl -s https://ipinfo.io

```

* **所揭示的信息：** 返回 `[REDACTED_PROXY_IP]`，位于洛杉矶，由 DMIT 托管。这确认了标准 HTTP/HTTPS 流量正通过外部代理出口节点进行隧道传输。

### 绕过代理（直接运营商连接）

```bash
curl -s --noproxy '*' https://ipinfo.io

```

* **所揭示的信息：** 返回 `[REDACTED_CARRIER_IP]`，位于深圳，运行在 AS4134（中国电信骨干网）上。将真实的移动网络足迹与代理结果一起暴露，验证了本地代理层正在处理选择性路由。

---

## 3. 代理检测

### 系统级代理查询

```bash
networksetup -getwebproxy Wi-Fi
networksetup -getsecurewebproxy Wi-Fi
networksetup -getsocksfirewallproxy Wi-Fi

```

* **所揭示的信息：** 直接指向 `127.0.0.1:7890`（Clash HTTP 监听器）和 `127.0.0.1:7891`（SOCKS5 监听器），表明操作系统已将本地回环端口注册用于全局流量处理。

### Shell 环境变量

```bash
echo $http_proxy $https_proxy

```

* **所揭示的信息：** 验证命令行应用程序是否被明确指示使用本地拦截套接字（`http://127.0.0.1:7890`）。

### 连接时间回环匹配

```bash
curl -w "%{remote_ip}" [target_url]

```

* **所揭示的信息：** 返回 `127.0.0.1` 作为远程连接端点，确认 `curl` 正在立即将 TCP 握手卸载到本地客户端守护进程。

---

## 4. 延迟与抖动

### 标准连接性检查

```bash
ping -c 5 www.baidu.com

```

* **所揭示的信息：** 测量基本往返时间（RTT）。连续序列之间的显著差异表明数据包队列波动较大。

### 抖动诊断（高频）

```bash
ping -c 20 -i 0.2 [REDACTED_TARGET_IP]

```

* **所揭示的信息：** 快速连续 ICMP 窗口提供最小值、平均值、最大值和标准差计算。标准差指标高达 `341ms`，表明网络抖动极其严重，这是不稳定无线环境的典型特征。

### 国际路径质量

```bash
ping -c 5 8.8.8.8

```

* **所揭示的信息：** 测试跨境目标空间。高丢包率（例如 20%）伴随严重的 RTT 窗口（`275ms - 625ms`），暴露了瓶颈的国际网关。

### ICMP 过滤验证

```bash
ping -c 5 114.114.114.114

```

* **所揭示的信息：** 尽管正常网页浏览无异常，但返回 100% 丢包，表明某些国内基础设施目标在蜂窝节点上完全丢弃了 ICMP 回显请求。

---

## 5. DNS 解析

### 域名查询

```bash
dig +short www.baidu.com
dig +short www.google.com
dig +short github.com

```

* **所揭示的信息：** 确认国内和国际解析管道的状态。返回干净的地址证明底层名称解析在热点接口上保持稳定。

---

## 6. TCP 连接时间分解

```bash
curl -o /dev/null -s -w \
  "dns: %{time_namelookup}s\n\
  connect: %{time_connect}s\n\
  ttfb: %{time_starttransfer}s\n\
  total: %{time_total}s\n\
  speed: %{speed_download} bytes/s\n\
  ip: %{remote_ip}\n" \
  https://www.baidu.com

```

### 各阶段指标说明

* **`dns`（`time_namelookup`）：** 域名解析完成所经过的时间。
* **`connect`（`time_connect`）：** 与目标或本地代理建立原始 TCP 握手所需的时间。
* **`ttfb`（`time_starttransfer`）：** 首字节时间。捕获后端服务器处理延迟和传输延迟。
* **`total`（`time_total`）：** 完整有效载荷传输的总耗时。
* **`speed`（`speed_download`）：** 传输窗口期间的平均下载吞吐量。
* **`ip`（`remote_ip`）：** 直接套接字结构的终止 IP（`127.0.0.1` 表示本地核心交接）。

---

## 7. 带宽能力

### 下载带宽概况

```bash
curl -o /dev/null -s -w "%{speed_download}" "http://speedtest.tele2.net/1MB.zip"

```

* **所揭示的信息：** 拉取一个静态未压缩的测试对象。基准测试结果约为 `~291 KB/s`，对应大约 `2.3 Mbps` 的下载能力。

### 上传带宽概况

```bash
dd if=/dev/zero bs=1024 count=512 | \
  curl -X POST -o /dev/null -s -w "%{speed_upload}" \
  --data-binary @- "https://httpbin.org/post"

```

* **所揭示的信息：** 通过 HTTP POST 将受控的 512KB 零字节流管道传输到回显目标。指标跟踪到 `~68 KB/s`，对应大约 `0.5 Mbps` 的上传上限。

---

## 诊断工具集总结

| 命令 | 诊断目的 |
| --- | --- |
| `route` / `ifconfig` / `networksetup` | 识别本地物理拓扑、接口设置和内部网关。 |
| `scutil --dns` | 审查系统级上游 DNS 优先级结构。 |
| `ping`（目标矩阵） | 隔离链路延迟，跟踪标准差方差（抖动）和数据包丢失指标。 |
| `curl -w` 分解 | 诊断网络应用层各阶段的特定处理瓶颈。 |
| `curl` + `ipinfo.io` | 发现当前活跃的公网 WAN IP 概况和自治系统号（ASN）。 |
| `curl --noproxy` | 绕过本地转发软件，记录直接运营商链路参数。 |
| `networksetup -get*proxy` | 评估系统网络面板中的程序化代理拦截规则。 |
| `dig +short` | 验证区域或全球域名区域的解析可用性。 |
| `curl`（测速资源） | 使用真实世界资产交付有效载荷测量总下行带宽。 |
| `dd` | `curl POST` | 通过原始多部分有效载荷测量连续上行带宽限制。 |

> 所有参数均利用 macOS 原生 shell 能力，完全无需外部框架包或第三方可执行二进制文件安装。
