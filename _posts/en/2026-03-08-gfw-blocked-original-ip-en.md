---
audio: false
generated: true
image: false
lang: en
layout: post
title: GFW Blocked Your Original IP
translated: false
type: note
---

Question: I'm running DMIT.io with Hysteria2. My original IP had ping/traceroute timeouts and telnet failures, but after changing the IP everything works fine. The domain is fine. Is the original IP banned by GFW?

Answer:

## Yes — Almost Certainly a GFW IP Block

Your symptoms are a **classic and textbook GFW (Great Firewall of China) IP ban**. Here's a breakdown of what happened and why.

---

## 🔍 Why This Points to GFW, Not Other Issues

| Symptom | What It Means |
|---|---|
| Ping / traceroute → Operation timed out | ICMP packets being **dropped at the GFW level** |
| Telnet → Unable to connect | TCP connections being **reset or dropped** by GFW |
| Domain is fine | DNS is not the issue — it's the **IP layer** being blocked |
| After IP change → Works fine | New IP not yet flagged; confirms it's **IP-specific blocking** |

Since your domain resolves correctly and everything works after the IP change, the problem is clearly at the **IP address level**, not your server config, Hysteria2 setup, or DNS.

---

## 🧱 How GFW Blocks Hysteria2

Hysteria2 is based on **QUIC (UDP protocol)**. GFW has been observed marking IPs that generate significant UDP traffic over extended periods. The marking occurs after a certain time window, not immediately — for instance, IPs changed 15 hours ago may remain unmarked, while fixed IPs get marked within a specific timeframe. Marked machines experience **dropped UDP packets** for any traffic from overseas to domestic IPs, regardless of port or protocol, while TCP and ICMP traffic may also eventually be affected.

In short: GFW **detected the Hysteria2/QUIC UDP traffic pattern**, flagged the IP, and started dropping all packets to/from it.

---

## ⚠️ Important Warning: IP Changes Are Only a Temporary Fix

The GFW will continue blocking your IP address eventually after the swap. Changing IP is not a recommended long-term solution. Your new IP will likely get blocked again after some usage period.

---

## ✅ Longer-Term Mitigations

**1. Enable Port Hopping (Hysteria2 built-in feature)**
Hysteria2 has a feature called "port hopping" to help avoid UDP throttling and blocking. Configure it to rotate ports regularly so traffic patterns are harder for GFW to fingerprint.

**2. Use IPv6 if available**
IPv6 currently has fewer restrictions — "the wall is lower on IPv6." You can use Hysteria2 on IPv6 without port hopping and avoid throttling even when downloading large files, though it depends on the network being used.

**3. Set a reasonable bandwidth limit**
Make sure to set a fair bandwidth limit when using Hysteria2 — some providers consider large amounts of UDP traffic as attacks. High sustained UDP traffic is one of the main triggers for GFW to flag your IP.

**4. Consider alternative protocols**
Besides Hysteria2, you can try Xray with VLESS+REALITY+XTLS-RPRX-VISION, which is a strong combination. Client apps supporting this include V2rayNG (Android), V2rayN (Windows), and Shadowrocket (iOS).

---

## 🛠️ How to Verify GFW Block

You can use tools like **[ping.pe](https://ping.pe)** or **[check.greatfire.org](https://check.greatfire.org)** to test your original IP from inside China and confirm it's GFW-blocked before requesting another change.

References:

- [GFW UDP Blocking and Hysteria2 Issue – GitHub](https://github.com/apernet/hysteria/issues/1157)
- [IO Zoom – China GFW Block Explanation](https://www.iozoom.com/client/knowledgebase/127/China-Great-Firewall-GFW-block.html)
- [WireGuard/Hysteria2 in China – LowEndSpirit Discussion](https://lowendspirit.com/discussion/8008/wireguard-vpn-in-china)
- [Hysteria2 Official Troubleshooting Docs](https://v2.hysteria.network/docs/advanced/Troubleshooting/)
