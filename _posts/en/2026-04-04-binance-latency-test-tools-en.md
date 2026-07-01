---
audio: false
generated: true
image: false
lang: en
layout: post
title: Tools to Test Binance Latency
translated: false
type: note
---

Question: After deploying a server in the same AWS region (Tokyo/Osaka) as Binance, what network tools can I use to test the latency?

Answer:

## Network Tools to Test Latency to Binance's API

Once your server is deployed in AWS Tokyo (`ap-northeast-1`) or Osaka (`ap-northeast-3`), you have several layers of tools to measure latency — from basic OS-level commands to application-level API testing.

---

## 1. `ping` — Basic Round-Trip Test

The simplest starting point. Run from your EC2 instance:

```bash
ping api.binance.com
```

This gives you ICMP round-trip time (RTT). When co-located in Tokyo, you should see sub-1ms results. However, note that some hosts block ICMP, so ping may not always be reliable as a final measurement.

---

## 2. `traceroute` / `tracert` — Identify Network Hops

To find latency in your network and determine where delays begin, use `traceroute` for Linux or `tracert` for Windows. It maps each network hop between source and destination and shows the round-trip time for every hop.

```bash
# Linux
traceroute api.binance.com

# TCP-based (more reliable, port 443)
traceroute -T -p 443 api.binance.com
```

---

## 3. `mtr` (My Traceroute) — The Best All-in-One Tool

MTR combines the functionalities of ping and traceroute to provide insights into network performance, helping identify latency and packet loss across each hop.

This is the most recommended tool for quantitative traders diagnosing network paths. AWS Support Engineers also use it as the primary diagnostic tool.

```bash
# Install on Amazon Linux / Ubuntu
sudo apt install mtr   # Ubuntu
sudo yum install mtr   # Amazon Linux

# Run an ICMP MTR report (100 cycles)
mtr api.binance.com --report -c 100

# Run a TCP MTR (better, simulates real HTTPS traffic on port 443)
mtr api.binance.com -T -P 443 -c 100 --report
```

If MTR is available in your environment, use it instead of traceroute — it is more comprehensive for diagnosing both latency and packet loss simultaneously.

**Sample output to look for:**

- `Loss%` — should be 0.0% on all hops
- `Avg` (average RTT in ms) — in Tokyo, expect well under 5ms to `api.binance.com`
- `StDev` — low jitter is important for quant trading

---

## 4. `hping3` — TCP-Level Latency Test

You can use `hping` to test both ICMP and TCP ports. When using MTR in ICMP mode, run `ping` or `hping` to validate end-to-end loss and latency against the same TCP port.

```bash
# Install
sudo apt install hping3

# Test TCP latency on port 443 (HTTPS, same as Binance REST API)
sudo hping3 -S -p 443 -c 100 api.binance.com
```

This is more accurate than ICMP ping because it simulates real TCP connections that your trading bot uses.

---

## 5. `curl` — Measure Actual HTTP API Response Time

Test the real REST API call latency end-to-end:

```bash
curl -w "\n--- Timing ---\n\
DNS Lookup:    %{time_namelookup}s\n\
TCP Connect:   %{time_connect}s\n\
TLS Handshake: %{time_appconnect}s\n\
Time to First Byte: %{time_starttransfer}s\n\
Total:         %{time_total}s\n" \
-o /dev/null -s https://api.binance.com/api/v3/time
```

This breaks down each phase of the HTTP round trip, which is the most realistic measurement for REST API trading.

---

## 6. `tcpdump` — Capture and Analyze WebSocket Traffic

To intercept traffic coming from Binance's WebSocket endpoint and measure actual market data delivery latency, use `tcpdump` capturing on port 9443:

```bash
sudo tcpdump -i eth0 tcp port 9443 -w capture.pcap
```

After capturing, open the `.pcap` file with **Wireshark** on your local machine to inspect individual packet timestamps and measure WebSocket frame latency precisely.

---

## 7. Python Script — Application-Level API Latency

For the most realistic quant trading measurement, test latency at the Python code level — this measures what your bot actually experiences:

```python
import time
import requests

url = "https://api.binance.com/api/v3/order"  # or /ping, /time
headers = {"X-MBX-APIKEY": "YOUR_API_KEY"}

latencies = []
for _ in range(100):
    start = time.perf_counter()
    r = requests.get("https://api.binance.com/api/v3/time")
    end = time.perf_counter()
    latencies.append((end - start) * 1000)  # convert to ms

print(f"Min:    {min(latencies):.2f} ms")
print(f"Median: {sorted(latencies)[50]:.2f} ms")
print(f"P99:    {sorted(latencies)[99]:.2f} ms")
print(f"Max:    {max(latencies):.2f} ms")
```

In the AWS Tokyo region, Binance WebSocket market data arrives with a median latency around 4 milliseconds, with 99% of messages arriving within 13 milliseconds.

---

## 8. Online Tools (Before Deploying a Server)

Before provisioning your EC2 instance, you can use these web tools to get a sense of baseline latency:

- **[awsspeedtest.com/latency](https://awsspeedtest.com/latency)** — gives a quick, indicative view of latency from your browser to AWS regions, useful for initial guidance.
- **[globalping.io](https://globalping.io)** — allows anyone to run ping, traceroute, dig, curl, and MTR from probes distributed worldwide, useful to test latency from specific AWS cloud region names like `ap-northeast-1`.

---

## Summary: Tool Selection Guide

| Tool | Layer | Best For |
| --- | --- | --- |
| `ping` | ICMP | Quick basic check |
| `traceroute` | Network | Visualize hops and where delay occurs |
| `mtr` | Network | **Best all-around** — combines ping + traceroute with stats |
| `hping3` | TCP | Simulate real TCP port latency |
| `curl -w` | HTTP | REST API end-to-end timing breakdown |
| `tcpdump` + Wireshark | Packet | Deep WebSocket analysis |
| Python script | App-level | **Most realistic** for quant bot performance |

The recommended workflow is: **mtr → curl timing → Python script**, in that order, to validate both network-level and application-level latency from your deployed EC2 instance.

References:

- [A Latency Analysis of Binance Exchange Across AWS Regions – Viktoria Tsybko](https://viktoriatsybko.substack.com/p/an-analysis-of-binance-exchange-across)
- [WebSocket Data Feed Latency – EmberDocs / Deltix](https://ember.deltixlab.com/docs/performance/ws-market-data/)
- [Diagnosing Packet Loss and Latency with MTR – AWS re:Post](https://repost.aws/articles/ARYuHnu150R9ahMl-2hNNEVw/diagnosing-packet-loss-and-latency-with-mtr)
- [Troubleshoot Network Performance in Amazon VPC – AWS re:Post](https://repost.aws/knowledge-center/vpc-troubleshoot-network-performance)
- [Globalping – Global Network Testing Platform](https://globalping.io/)
- [AWS Latency Speed Test](https://awsspeedtest.com/latency)
- [High-Frequency Trading in Crypto: Latency, Infrastructure – Adrian Keller / Medium](https://medium.com/@laostjen/high-frequency-trading-in-crypto-latency-infrastructure-and-reality-594e994132fd)
