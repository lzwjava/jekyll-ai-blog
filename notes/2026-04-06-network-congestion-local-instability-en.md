---
audio: false
generated: true
image: false
lang: en
layout: post
title: Network Congestion and Local Instability
translated: false
type: note
---

Question:
How to interpret this second MTR result showing ~6% packet loss and high jitter to 104.21.78.239?

Answer:

This second test **is different from your previous one** — now there **is real packet loss and jitter**.
The key is the **final hop**, which shows actual end-to-end quality.

```
12. 104.21.78.239   Loss 6.2%   Avg 276 ms   Worst 580 ms   StDev 40 ms
```

This means:

* ❌ Real packet loss: **6.2%** (not good)
* ⚠️ High jitter: **40 ms**
* ⚠️ Latency spikes: **580 ms**
* ⚠️ Connection unstable

So **this time there IS a real network problem.**

---

# Where the problem starts

Look at hop 9:

```
9. 202.97.116.250   Loss 7.0%   Avg 276 ms
```

From this hop onward:

```
9  loss 7%
10 loss 43%
11 loss 13%
12 loss 6%
```

Since **loss starts at hop 9 and continues to destination**,
the issue is **real congestion after hop 9**.

This hop:

```
202.97.116.250
```

This is:

* China Telecom international gateway
* leaving mainland China
* entering global transit

So the problem is:

> **China Telecom international congestion**

Very common.

---

# Your route visualization

```
Your Mac
  ↓
Home router (192.168.1.1)
  ↓
ISP CGNAT (100.69.0.1)
  ↓
China Telecom Guangdong
  ↓
China Telecom backbone
  ↓
202.97.x.x  ← congestion starts here
  ↓
International transit
  ↓
Cloudflare
  ↓
104.21.78.239
```

The **bottleneck is the international exit**.

---

# Another warning sign

Your **first hop already unstable**:

```
1. 192.168.1.1  
Loss 2.3%  
Avg 21.9 ms  
Worst 194 ms
```

This is **not normal**.

Your local network should be:

```
0% loss
< 3 ms latency
```

This suggests:

* WiFi interference
* router overloaded
* bufferbloat
* LAN congestion

So you may have **two problems**:

1. Local WiFi/router instability
2. China Telecom international congestion

---

# Severity

6% packet loss causes:

* slow HTTPS
* broken downloads
* SSH lag
* git clone failures
* API timeout
* streaming buffering

You will definitely **feel this**.

---

# How to confirm

Run:

```
mtr -rwzc 100 1.1.1.1
```

and

```
mtr -rwzc 100 8.8.8.8
```

If both show loss → ISP problem
If only this host → route-specific congestion

---

# Quick fixes

Best → worst:

### 1. Use wired Ethernet

Eliminate hop 1 instability

### 2. Switch DNS (Cloudflare / Google)

```
1.1.1.1
8.8.8.8
```

May route to better PoP.

### 3. Try IPv6

Sometimes avoids congested IPv4 path

### 4. Use different network

* mobile hotspot
* different ISP
* company network

### 5. Use tunnel/VPN (not ideal but works)

Because:

VPN may exit China using **better route**

---

# Final verdict

Your second test shows:

* ❌ Real packet loss (6%)
* ❌ High jitter
* ⚠️ Local router instability
* ⚠️ China Telecom international congestion

So **this connection is unstable right now**.

Your first test was healthy.
This second test shows **temporary congestion** (very common in evening).