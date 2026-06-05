---
audio: false
generated: true
image: false
lang: en
layout: post
title: Sanitizing macOS Network Diagnostic Logs
translated: false
type: note
---

Question: How can I format the macOS network diagnostic log while redacting the public IP and proxy exit node addresses?

Answer: Here is the well-formatted diagnostic breakdown with all sensitive public IP addresses, proxy exit nodes, and carrier-specific routing IPs completely sanitized and replaced with placeholders like `[REDACTED_PUBLIC_IP]`.

---

## 1. Basic Network Info

### Default Gateway & Routing

```bash
route -n get default

```

* **What it reveals:** Shows the gateway is `172.20.10.1` (iPhone hotspot) rather than a typical home router subnet (e.g., `192.168.1.1`).

### Network Interface Details

```bash
ifconfig en0

```

* **What it reveals:** Displays local IP (`172.20.10.3`), subnet mask (`/28` or `255.255.255.240`), MTU, and IPv6 details. The tight `/28` subnet limits the network to 14 usable IPs, which is a structural signature of an iOS Personal Hotspot.

### Wi-Fi Configuration

```bash
networksetup -getinfo Wi-Fi

```

* **What it reveals:** Confirms active DHCP configurations, local router IPs, and subnet masks assigned to the physical Wi-Fi card.

### DNS Servers

```bash
scutil --dns

```

* **What it reveals:** Identifies active resolver configurations. In this trace, it maps to `100.100.100.100` (Aliyun DNS intercepted/set by local proxy) alongside `172.20.10.1` acting as the raw hotspot upstream relay.

---

## 2. Public IP & Carrier Identification

### Traffic Routed via Proxy (Clash Node)

```bash
curl -s https://ipinfo.io

```

* **What it reveals:** Returns `[REDACTED_PROXY_IP]`, located in Los Angeles, hosted by DMIT. This confirms that standard HTTP/HTTPS traffic is actively tunneling through an external proxy exit node.

### Bypassing the Proxy (Direct Carrier Connection)

```bash
curl -s --noproxy '*' https://ipinfo.io

```

* **What it reveals:** Returns `[REDACTED_CARRIER_IP]`, located in Shenzhen, operating over AS4134 (CHINANET BACKBONE). Exposing this real mobile footprint alongside the proxy result validates that the local proxy layer is handling selective routing.

---

## 3. Proxy Detection

### System-Wide Proxy Queries

```bash
networksetup -getwebproxy Wi-Fi
networksetup -getsecurewebproxy Wi-Fi
networksetup -getsocksfirewallproxy Wi-Fi

```

* **What it reveals:** Points directly to `127.0.0.1:7890` (Clash HTTP listener) and `127.0.0.1:7891` (SOCKS5 listener), indicating the operating system has registered local loopback ports for global traffic handling.

### Shell Environment Variables

```bash
echo $http_proxy $https_proxy

```

* **What it reveals:** Verifies if command-line applications are explicitly instructed to use the local intercept socket (`http://127.0.0.1:7890`).

### Connection Timing Loopback Match

```bash
curl -w "%{remote_ip}" [target_url]

```

* **What it reveals:** Returning `127.0.0.1` as the remote connection end-point confirms that `curl` is immediately offloading its TCP handshakes to the local client daemon.

---

## 4. Latency & Jitter

### Standard Connectivity Check

```bash
ping -c 5 www.baidu.com

```

* **What it reveals:** Measures basic Round-Trip Time (RTT). Substantial variance between sequential sequences indicates high packet queue volatility.

### Jitter Diagnostics (High Frequency)

```bash
ping -c 20 -i 0.2 [REDACTED_TARGET_IP]

```

* **What it reveals:** Rapid-fire ICMP windowing provides minimum, average, maximum, and standard deviation calculations. A standard deviation metric up to `341ms` demonstrates extreme network jitter, typical of volatile wireless environments.

### International Path Quality

```bash
ping -c 5 8.8.8.8

```

* **What it reveals:** Testing cross-border target spaces. High packet loss (e.g., 20%) alongside severe RTT windows (`275ms - 625ms`) surfaces bottlenecked international gateways.

### ICMP Filtering Verification

```bash
ping -c 5 114.114.114.114

```

* **What it reveals:** Returning a 100% loss profile despite normal web browsing indicates that specific domestic infrastructure targets are dropping ICMP echo requests entirely across cellular nodes.

---

## 5. DNS Resolution

### Domain Lookups

```bash
dig +short www.baidu.com
dig +short www.google.com
dig +short github.com

```

* **What it reveals:** Confirms the state of domestic and international resolution pipelines. Clean address returns prove that underlying name resolution remains stable through the hotspot interface.

---

## 6. TCP Connection Timing Breakdowns

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

### Phase Metrics Explained

* **`dns` (`time_namelookup`):** Time elapsed until the domain name resolution is complete.
* **`connect` (`time_connect`):** Time taken to establish the raw TCP handshake with the target or local proxy.
* **`ttfb` (`time_starttransfer`):** Time to First Byte. Captures back-end server processing lag and transit latency.
* **`total` (`time_total`):** Total elapsed duration for the complete payload delivery.
* **`speed` (`speed_download`):** Average download throughput calculation during the transfer window.
* **`ip` (`remote_ip`):** The exact termination IP of the immediate socket socket structure (`127.0.0.1` indicating local core handoffs).

---

## 7. Bandwidth Capabilities

### Download Bandwidth Profile

```bash
curl -o /dev/null -s -w "%{speed_download}" "http://speedtest.tele2.net/1MB.zip"

```

* **What it reveals:** Pulls a static uncompressed test object. A benchmark result yielding `~291 KB/s` reflects an approximate download capability of `2.3 Mbps`.

### Upload Bandwidth Profile

```bash
dd if=/dev/zero bs=1024 count=512 | \
  curl -X POST -o /dev/null -s -w "%{speed_upload}" \
  --data-binary @- "https://httpbin.org/post"

```

* **What it reveals:** Pipes a controlled 512KB zero-byte stream to an echo destination via HTTP POST. A metric tracking `~68 KB/s` charts an upload ceiling of roughly `0.5 Mbps`.

---

## Summary of Diagnostic Toolkit

| Command | Diagnostic Purpose |
| --- | --- |
| `route` / `ifconfig` / `networksetup` | Identifies local physical topology, interface settings, and internal gateways. |
| `scutil --dns` | Audits system-wide upstream DNS priority structures. |
| `ping` (Target matrix) | Isolates link latency, tracking standard deviation variance (jitter), and packet drop-off metrics. |
| `curl -w` breakdown | Diagnoses specific processing bottlenecks across network application layers. |
| `curl` + `ipinfo.io` | Discovers active public WAN IP profiles and Autonomous System Numbers (ASN). |
| `curl --noproxy` | Bypasses local forwarding software to record direct carrier link parameters. |
| `networksetup -get*proxy` | Evaluates system network panels for programmatic proxy interception rules. |
| `dig +short` | Verifies resolution availability for regional or global domain zones. |
| `curl` (Speedtest assets) | Measures total downstream bandwidth using real-world asset delivery payloads. |
| `dd` | `curl POST` | Measures continuous upstream bandwidth limits via raw multi-part payloads. |

> All parameters leverage native macOS shell capabilities, completely removing the requirement for external framework packages or third-party executable bin installations.
