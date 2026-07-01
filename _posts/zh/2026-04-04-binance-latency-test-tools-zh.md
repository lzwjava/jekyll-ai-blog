---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 币安延迟测试工具
translated: true
type: note
---

# 测试与币安（Binance）网络延迟的工具

在 AWS 东京（`ap-northeast-1`）或大阪（`ap-northeast-3`）区域部署服务器后，您可以使用多个层面的工具来测量延迟，从基本的操作系统级命令到应用程序级的 API 测试。

---

## 1. `ping` — 基本往返测试

这是最简单的起点。从您的 EC2 实例运行：

```bash
ping api.binance.com
```

这将给出 ICMP 往返时间。若服务器位于东京，您应该会看到低于 1 毫秒的结果。但请注意，某些主机会屏蔽 ICMP，因此 ping 并非总是可靠的最终测量手段。

---

## 2. `traceroute` / `tracert` — 识别网络跳转

为了找出网络中的延迟并确定延迟开始的位置，可以在 Linux 上使用 `traceroute`，或在 Windows 上使用 `tracert`。它可以绘制源与目标之间的每个网络跳转，并显示每个跳转的往返时间。

```bash
# Linux
traceroute api.binance.com

# 基于 TCP（更可靠，端口 443）
traceroute -T -p 443 api.binance.com
```

---

## 3. `mtr` — 最佳一体化工具

MTR 结合了 ping 和 traceroute 的功能，提供对网络性能的深入洞察，帮助识别每个跳转的延迟和数据包丢失。

这是量化交易者诊断网络路径最推荐的工具。AWS 支持工程师也将其作为主要诊断工具。

```bash
# 在 Amazon Linux / Ubuntu 上安装
sudo apt install mtr   # Ubuntu
sudo yum install mtr   # Amazon Linux

# 运行 ICMP MTR 报告（100 次循环）
mtr api.binance.com --report -c 100

# 运行 TCP MTR（更好，模拟端口 443 的真实 HTTPS 流量）
mtr api.binance.com -T -P 443 -c 100 --report
```

如果您的环境中可用 MTR，请用它替代 traceroute — 它对于同时诊断延迟和数据包丢失更为全面。

**需要关注的示例输出：**

- `Loss%` — 所有跳转处应为 0.0%
- `Avg`（平均往返时间，单位毫秒）— 在东京，预计到 `api.binance.com` 远低于 5 毫秒
- `StDev` — 低抖动对量化交易很重要

---

## 4. `hping3` — TCP 层面的延迟测试

您可以使用 `hping` 测试 ICMP 和 TCP 端口。当在 ICMP 模式下使用 MTR 时，可以运行 `ping` 或 `hping` 来验证针对同一 TCP 端口的端到端丢包和延迟。

```bash
# 安装
sudo apt install hping3

# 在端口 443 上测试 TCP 延迟（HTTPS，与币安 REST API 相同）
sudo hping3 -S -p 443 -c 100 api.binance.com
```

这比 ICMP ping 更准确，因为它模拟了您的交易机器人使用的真实 TCP 连接。

---

## 5. `curl` — 测量实际的 HTTP API 响应时间

测试真实的 REST API 调用的端到端延迟：

```bash
curl -w "\n--- Timing ---\n\
DNS Lookup:    %{time_namelookup}s\n\
TCP Connect:   %{time_connect}s\n\
TLS Handshake: %{time_appconnect}s\n\
Time to First Byte: %{time_starttransfer}s\n\
Total:         %{time_total}s\n" \
-o /dev/null -s https://api.binance.com/api/v3/time
```

这将细分 HTTP 往返的每个阶段，是针对 REST API 交易最真实的测量。

---

## 6. `tcpdump` — 捕获和分析 WebSocket 流量

要拦截来自币安 WebSocket 端点的流量并测量实际的市场数据交付延迟，可以在端口 9443 上使用 `tcpdump` 进行捕获：

```bash
sudo tcpdump -i eth0 tcp port 9443 -w capture.pcap
```

捕获后，可以在本地机器上用 **Wireshark** 打开 `.pcap` 文件，检查单个数据包的时间戳并精确测量 WebSocket 帧的延迟。

---

## 7. Python 脚本 — 应用层 API 延迟

为了获得最真实的量化交易测量，请在 Python 代码层面测试延迟 — 这测量的是您的机器人实际体验到的延迟：

```python
import time
import requests

url = "https://api.binance.com/api/v3/order"  # 或 /ping, /time
headers = {"X-MBX-APIKEY": "YOUR_API_KEY"}

latencies = []
for _ in range(100):
    start = time.perf_counter()
    r = requests.get("https://api.binance.com/api/v3/time")
    end = time.perf_counter()
    latencies.append((end - start) * 1000)  # 转换为毫秒

print(f"Min:    {min(latencies):.2f} ms")
print(f"Median: {sorted(latencies)[50]:.2f} ms")
print(f"P99:    {sorted(latencies)[99]:.2f} ms")
print(f"Max:    {max(latencies):.2f} ms")
```

在 AWS 东京区域，币安 WebSocket 市场数据的到达中值延迟约为 4 毫秒，99% 的消息在 13 毫秒内到达。

---

## 8. 在线工具（部署服务器前）

在配置您的 EC2 实例之前，您可以使用这些网络工具来了解基准延迟：

- **[awsspeedtest.com/latency](https://awsspeedtest.com/latency)** — 提供从您的浏览器到 AWS 区域的快速、指示性延迟视图，对初始指导很有用。
- **[globalping.io](https://globalping.io)** — 允许任何人从全球分布的探测点运行 ping、traceroute、dig、curl 和 MTR，可用于测试特定 AWS 云区域（如 `ap-northeast-1`）的延迟。

---

## 总结：工具选择指南

| 工具 | 层面 | 最适用场景 |
| --- | --- | --- |
| `ping` | ICMP | 快速基本检查 |
| `traceroute` | 网络 | 可视化跳转及延迟发生点 |
| `mtr` | 网络 | **最佳全能工具** — 结合 ping 和 traceroute 并提供统计数据 |
| `hping3` | TCP | 模拟真实 TCP 端口延迟 |
| `curl -w` | HTTP | REST API 端到端时间细分 |
| `tcpdump` + Wireshark | 数据包 | 深度 WebSocket 分析 |
| Python 脚本 | 应用层 | **最真实**的量化机器人性能测量 |

推荐的工作流程是：**mtr → curl 计时 → Python 脚本**，按此顺序验证从您部署的 EC2 实例发出的网络层和应用层延迟。

参考：

- [A Latency Analysis of Binance Exchange Across AWS Regions – Viktoria Tsybko](https://viktoriatsybko.substack.com/p/an-analysis-of-binance-exchange-across)
- [WebSocket Data Feed Latency – EmberDocs / Deltix](https://ember.deltixlab.com/docs/performance/ws-market-data/)
- [Diagnosing Packet Loss and Latency with MTR – AWS re:Post](https://repost.aws/articles/ARYuHnu150R9ahMl-2hNNEVw/diagnosing-packet-loss-and-latency-with-mtr)
- [Troubleshoot Network Performance in Amazon VPC – AWS re:Post](https://repost.aws/knowledge-center/vpc-troubleshoot-network-performance)
- [Globalping – Global Network Testing Platform](https://globalping.io/)
- [AWS Latency Speed Test](https://awsspeedtest.com/latency)
- [High-Frequency Trading in Crypto: Latency, Infrastructure – Adrian Keller / Medium](https://medium.com/@laostjen/high-frequency-trading-in-crypto-latency-infrastructure-and-reality-594e994132fd)
