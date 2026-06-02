---
audio: false
generated: true
image: false
lang: en
layout: post
title: Windows Tracert Network Path Diagnostic Guide
translated: false
type: note
---

On Windows, **`tracert`** (short for *trace route*) is a diagnostic command-line tool used to trace the path that packets take from your computer to a destination host (like a website or IP address). It’s mainly used to identify where delays or connection problems occur in a network route.

Here’s how it works step by step:

### 1. ICMP Echo Requests with Incremental TTL

* `tracert` sends **ICMP Echo Request packets** (similar to `ping`).
* It manipulates the **Time-To-Live (TTL)** field in the IP header.
* TTL starts at 1, then increases (2, 3, 4, …) with each probe.

### 2. TTL Expiry and “Time Exceeded” Responses

* When a router receives a packet, it decrements TTL by 1.
* If TTL reaches **0**, the router discards the packet and returns an **ICMP Time Exceeded** message to the sender.
* This lets `tracert` know the identity (IP/hostname) of that router.

### 3. Building the Route

* For TTL = 1, you see the first hop (your default gateway).
* For TTL = 2, you see the next router, and so on.
* This continues until:

  * The destination host responds with an **ICMP Echo Reply**, or
  * The maximum hop limit (default 30) is reached.

### 4. Measuring Latency

* `tracert` sends **three probes** per hop (by default).
* It shows the **round-trip time (RTT)** in milliseconds for each probe.
* If a router does not respond, you’ll see `*` instead of a time.

### 5. Example Output

```text
Tracing route to example.com [93.184.216.34]
over a maximum of 30 hops:

  1     1 ms    <1 ms     1 ms  192.168.1.1
  2    10 ms     9 ms    11 ms  isp-gateway.example.net [203.0.113.1]
  3    25 ms    23 ms    24 ms  core-router.example.net [198.51.100.1]
  ...
  8    45 ms    46 ms    47 ms  example.com [93.184.216.34]
```

### 6. Notes on Behavior

* Some routers may block or deprioritize ICMP responses, causing `* * *`.
* `tracert` in **Windows** uses ICMP Echo Requests, whereas `traceroute` on Linux/Unix often uses **UDP probes** (though it can be changed).
* Firewalls or ISP filtering can sometimes hide parts of the route.

---

👉 Do you want me to also explain **how to interpret cases like `* * *` or large delays** in a `tracert` result, so you can use it for real troubleshooting?
