---
audio: false
generated: true
image: false
lang: en
layout: post
title: Proxy Gateway Laptop or Router Choice
translated: false
type: note
---

Question: Should I use my old Lenovo laptop (Linux Mint) or my Xiaomi router (OpenWrt) as my home proxy gateway in China, given I have a Hysteria2 server in Los Angeles? What is the better approach?

Answer:

## Honest Assessment: Both Can Work, But They Have Very Different Trade-offs

---

## Option A: Lenovo Laptop with Linux Mint (What You Already Tried)

### ✅ Strengths
- **x86 full-power CPU** — runs Clash/Mihomo with Hysteria2 natively, no architecture issues
- **More RAM and storage** — no package size constraints
- **Easier debugging** — full Linux toolset (`tcpdump`, `nftables`, `journalctl`, etc.)
- **You were 95% done** — the summary you pasted shows the architecture was completely correct. The only remaining step was the iPad renewing its DHCP lease to get the new DNS (`192.168.201.1`)

### ❌ Weaknesses
- A 2013 Lenovo laptop **consumes a lot of power** running 24/7 (~30–60W vs a router's 5–10W)
- USB tethering for iPad is a workaround, not a clean network topology
- Not a "set and forget" device — laptop can sleep, lid-close issues, etc.

### Verdict on your one-night attempt
You likely did **not fail** — you were just one step away. The iPad simply needed to renew its DHCP lease. The entire architecture (DHCP → dnsmasq → Clash DNS → fake-IP → TUN → Hysteria2) was correctly built.

---

## Option B: Xiaomi Router with OpenWrt

### ✅ Strengths
- Clean, permanent router role — always on, low power
- All devices in your home connect naturally via Wi-Fi/LAN without USB tethering
- OpenWrt supports Hysteria2 through the `openwrt-passwall` LuCI app, so installation is straightforward once you know the path
- There is also a project called OpenWrt-nikki (Mihomo/Clash Meta) specifically for transparent proxy on OpenWrt, which is more modern and actively maintained

### ❌ Weaknesses
- **MIPS/ARM routers have limited RAM** (often 128–256MB) — Clash Meta with many rules can push limits
- OpenWrt package ecosystem is constrained — harder to debug when things break
- Your previous experience showed it was difficult to configure — though with AI assistance this is now more feasible
- Some Xiaomi models require specific flashing procedures

### About your specific Xiaomi router
The answer depends on **which model** you have. Routers based on MediaTek platforms are the best fit for OpenWrt, since MediaTek provides open-source drivers for its Wi-Fi modules to the community. If your Xiaomi runs a MediaTek chipset (like MT7621, MT7622, MT7981), support is solid.

---

## My Recommendation: Hybrid Approach

The **best architecture for your situation** is actually to combine both:

```
[ISP Modem] → [Xiaomi OpenWrt router] → (LAN)
                      ↓
           [Lenovo Laptop as "soft router" / proxy gateway]
                      ↓
         All devices route through Clash + Hysteria2
```

Specifically:
1. **Keep the Xiaomi as your main Wi-Fi router** (it handles DHCP for the whole home)
2. **Run Clash + Hysteria2 on the Lenovo laptop** as a transparent proxy gateway on the LAN
3. **In Xiaomi's DHCP settings**, push the Lenovo's IP as the default gateway and DNS for all clients (option 3 and option 6)

This way:
- iPad, phone, PC all get proxied automatically — no USB tethering needed
- The Lenovo handles the heavy lifting of Clash rule matching
- The Xiaomi handles Wi-Fi and routing cleanly
- This is a proven pattern: run Clash on a always-on Linux device, then configure the OpenWrt router to push that device's IP as the DHCP default gateway and DNS to all LAN clients, so devices don't need to manually change any settings

---

## If You Must Pick Just One

| Factor | Laptop (Linux Mint) | Xiaomi (OpenWrt) |
|---|---|---|
| Hysteria2 support | Native, easy | Via passwall/nikki |
| Setup difficulty | Medium (you almost did it) | Medium-High |
| All-home coverage | Only USB-tethered devices | All Wi-Fi + LAN devices |
| Reliability | Needs lid/sleep config | Excellent |
| Power cost | High | Low |
| Debugging ease | High | Low |

**Pick the laptop** if you only need to serve the iPad via USB and want to finish quickly — you are very close.

**Pick OpenWrt** if you want all home devices covered cleanly and are willing to spend time on initial setup.

---

## Immediate Next Step to Fix Your Current iPad Issue

If you want to finish the laptop setup tonight, just run this on the iPad (or force a DHCP renewal):

```bash
# On the iPad: Settings → Wi-Fi → forget network → reconnect
# OR on the laptop:
sudo systemctl restart dnsmasq
# Then on iPad Settings → General → Transfer or Reset iPad → Reset → Reset Network Settings
```

Then test:
```bash
nslookup google.com 192.168.201.1   # should return 198.18.x.x (fake-IP)
curl https://api.ipify.org           # should show your LA server IP
```

You were one DHCP renewal away from success.

References:

- [Hysteria2 Installation — OpenWrt LuCI app (openwrt-passwall)](https://v1.hysteria.network/docs/installation/)
- [OpenWrt-nikki: Transparent Proxy with Mihomo on OpenWrt](https://github.com/nikkinikki-org/OpenWrt-nikki)
- [Clash Transparent Proxy on Linux Gateway — Chinese Blog](https://hellodk.cn/post/844)
- [Clash Transparent Proxy on Linux Router — DEV Community](https://dev.to/jysperm/setup-clash-redir-proxy-on-a-linux-router-4jnh)
