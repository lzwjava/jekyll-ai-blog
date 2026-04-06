---
audio: false
generated: true
image: false
lang: en
layout: post
title: Severe Network Degradation and Local Issues
translated: false
type: note
---

Question:
Explain this MTR result to 185.199.108.153 and compare it with the previous trace to 104.21.78.239.

Answer:

This trace is **worse than your previous one** and shows **two real problems**:

1. **Severe local network instability**
2. **Heavy packet loss on international route (China → Japan → GitHub CDN)**

Let's analyze carefully.

---

# 1. Final destination (this determines real quality)

```
13. cdn-185-199-108-153.github.com
Loss 52.3%
Avg 148.9 ms
```

This is **very bad**:

* ❌ **52% packet loss**
* ⚠️ unstable latency
* ❌ half of packets dropped

This will cause:

* git clone hanging
* npm/pip slow
* GitHub downloads fail
* API timeout
* CI/CD failures

So this route is **severely degraded**.

---

# 2. The biggest red flag — your local network

```
1. 192.168.1.1
Loss 27.1%
Avg 28.8 ms
Worst 245 ms
```

This is **extremely abnormal**.

Local router should be:

* 0% loss
* < 3 ms latency

Your result:

* ❌ 27% packet loss
* ❌ huge jitter
* ❌ 245 ms spikes

This means your **WiFi / LAN is already broken** before reaching ISP.

So **everything after this is affected**.

---

# 3. Route path

Your route:

```
home router
  ↓
China Telecom (Guangdong)
  ↓
China Telecom backbone
  ↓
203.86.97.18  ← leaving China
  ↓
NTT Japan backbone
tokyjp05
tokyjp10
  ↓
Fastly CDN
  ↓
GitHub CDN
```

So this path is:

```
China Telecom → NTT Japan → Fastly → GitHub
```

This is **normal GitHub route** from China.

---

# 4. Where loss becomes real

Loss persists **all the way to destination**:

```
hop 1  27%
hop 2  17%
...
hop 9  54%
hop 12 51%
hop 13 52%
```

Because **final hop still has 52%**, this is **real packet loss**.

---

# 5. Compare with your previous test (Cloudflare)

Previous (Cloudflare):

```
loss: 6%
latency: 270 ms
```

This one (GitHub CDN):

```
loss: 52%
latency: 148 ms
```

Comparison:

| Test   | Destination | Loss | Latency | Quality  |
| ------ | ----------- | ---- | ------- | -------- |
| first  | Cloudflare  | 0%   | 260ms   | good     |
| second | Cloudflare  | 6%   | 270ms   | medium   |
| third  | GitHub CDN  | 52%  | 148ms   | terrible |

So:

* Cloudflare route = mostly OK
* GitHub route = **very unstable**

This is very common in China.

---

# 6. Why GitHub worse than Cloudflare

Because:

Cloudflare:

```
China Telecom → Cloudflare direct peering
```

GitHub CDN:

```
China Telecom → NTT → Fastly → GitHub
```

More hops + congested transit.

GitHub CDN often unstable in China.

---

# 7. But the real root cause

Your **local network already broken**:

```
hop 1 loss 27%
```

Even if upstream perfect, you'd still have issues.

So you must fix:

* WiFi interference
* router CPU overload
* bufferbloat
* 2.4GHz congestion
* bad cable
* QoS misconfig

---

# 8. What this means practically

You currently have:

* ❌ unstable WiFi
* ❌ ISP congestion
* ❌ GitHub route congestion

Triple problem.

That's why GitHub feels very slow.

---

# 9. Quick tests

Run this:

```
ping 192.168.1.1
```

If loss > 0% → WiFi problem.

Then try:

```
wired ethernet
```

You will likely see:

* loss drop to 0%
* latency stable

---

# Final conclusion

This trace shows:

* ❌ 52% real packet loss to GitHub CDN
* ❌ local router already unstable (27% loss)
* ⚠️ China Telecom → Japan congestion
* ⚠️ GitHub CDN route worse than Cloudflare

Main problem order:

1. your WiFi / LAN (biggest)
2. ISP international congestion
3. GitHub route weaker than Cloudflare